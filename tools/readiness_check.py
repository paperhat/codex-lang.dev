#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import sys
import re
from pathlib import Path


_RFC2119_RE = re.compile(r"\b(MUST NOT|MUST|MAY)\b")
_DOLLAR_TOKEN_RE = re.compile(r"\$[A-Za-z][A-Za-z0-9]*")
_VALIDATION_TERM_RE = re.compile(r"\bvalidat(e|ed|es|ing)\b", re.IGNORECASE)
_VALIDATION_QUALIFIER_RE = re.compile(
    r"\b(schema|schemas|semantic|well-formed|well formed|well-formedness|schema-based|schema-driven|schema-first)\b",
    re.IGNORECASE,
)


ROOT = Path(__file__).resolve().parents[1]


def _fail(message: str) -> None:
    raise SystemExit(f"readiness_check: {message}")


def _run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, cwd=str(ROOT), text=True)
    if proc.returncode != 0:
        _fail(f"command failed ({proc.returncode}): {' '.join(cmd)}")


def _git_tracked_json_files() -> list[str]:
    # Prefer checking tracked files only so local editor config does not trip the gate.
    proc = subprocess.run(
        ["git", "ls-files", "*.json"],
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        # Not a git repo (or git not available). Fall back to a simple filesystem scan.
        json_paths: list[str] = []
        for p in ROOT.rglob("*.json"):
            # ignore dot-directories in filesystem scan
            if any(part.startswith(".") for part in p.relative_to(ROOT).parts):
                continue
            json_paths.append(str(p.relative_to(ROOT)))
        return sorted(json_paths)

    files = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    return sorted(files)


def _working_tree_json_files() -> list[str]:
    json_paths: list[str] = []
    for p in ROOT.rglob("*.json"):
        rel = p.relative_to(ROOT)
        if any(part.startswith(".") for part in rel.parts):
            continue
        json_paths.append(str(rel))
    return sorted(json_paths)


def _gate_no_json() -> None:
    # Enforce against the working tree so the check matches what will be shipped.
    # (CI checkouts will still contain any committed JSON, and will fail.)
    json_files = _working_tree_json_files()
    if json_files:
        details = "\n".join(f"- {p}" for p in json_files)
        _fail(
            "JSON files exist in the repo working tree (Codex-first repo).\n"
            "Remove them or move them behind an explicit compat-only exception.\n"
            f"Found:\n{details}"
        )


def _gate_required_docs() -> None:
    required = [ROOT / "AI_CONVENTIONS.md", ROOT / "READINESS.md"]
    missing = [p for p in required if not p.exists()]
    if missing:
        details = ", ".join(str(p.relative_to(ROOT)) for p in missing)
        _fail(f"missing required docs: {details}")


def _gate_conformance_smokecheck() -> None:
    manifest = ROOT / "conformance" / "1.0.0" / "manifest" / "configuration.cdx"
    if not manifest.exists():
        _fail(f"missing conformance manifest: {manifest.relative_to(ROOT)}")
    _run(["python3", "tools/conformance_smokecheck.py", str(manifest.relative_to(ROOT))])


def _gate_cdx_annotation_lint() -> None:
    _run(["python3", "tools/annotation_lint.py"])


def _gate_no_rfc2119_leakage() -> None:
    # RFC-2119 keywords are reserved for versioned specification documents.
    # This prevents accidental normativity "leakage" into pointer pages, READMEs, etc.
    allowed = set()
    for p in (ROOT / "spec").glob("*/index.md"):
        if p.is_file():
            allowed.add(p.resolve())

    leaks: list[str] = []
    for p in ROOT.rglob("*.md"):
        rel = p.relative_to(ROOT)
        if any(part.startswith(".") for part in rel.parts):
            continue
        if p.resolve() in allowed:
            continue

        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = p.read_text(encoding="utf-8", errors="replace")

        for idx, line in enumerate(text.splitlines(), start=1):
            if _RFC2119_RE.search(line):
                leaks.append(f"- {rel}:{idx}: {line.strip()}")

    if leaks:
        details = "\n".join(leaks)
        _fail(
            "RFC-2119 keyword leakage detected outside versioned spec index.md files.\n"
            "Use lowercase (must/may) or rephrase, and link to the versioned spec when needed.\n"
            f"Found:\n{details}"
        )


def _iter_unfenced_markdown_lines(text: str) -> list[tuple[int, str]]:
    """Return (line_number, line_text) lines that are outside fenced code blocks.

    This gate intentionally implements only the subset of CommonMark fencing we need:
    - backtick and tilde fences
    - opening fence length >= 3
    - closing fence length >= opening length

    This is necessary because some documents use longer fences (e.g. ````) to embed
    triple-backtick examples; a naive toggle-on-any-fence-line approach can incorrectly
    treat large suffixes of the file as "inside a fence".
    """

    in_fence = False
    fence_char: str | None = None
    fence_len: int | None = None
    out: list[tuple[int, str]] = []

    for idx, raw in enumerate(text.splitlines(), start=1):
        m = re.match(r"^(\s*)(`{3,}|~{3,})", raw)
        if m:
            token = m.group(2)
            token_char = token[0]
            token_len = len(token)
            if not in_fence:
                in_fence = True
                fence_char = token_char
                fence_len = token_len
            else:
                if fence_char == token_char and fence_len is not None and token_len >= fence_len:
                    in_fence = False
                    fence_char = None
                    fence_len = None
            continue

        if in_fence:
            continue

        out.append((idx, raw))

    return out


def _strip_inline_code_spans(line: str) -> str:
    """Remove simple single-line inline code spans delimited by backticks.

    This intentionally ignores the exact backtick-length rules; it is a pragmatic
    gate to prevent accidental `$...` math parsing in Markdown preview.
    """

    parts = line.split("`")
    # Keep only the non-code segments (even indexes).
    return "".join(part for i, part in enumerate(parts) if i % 2 == 0)


def _gate_no_unfenced_dollar_tokens_in_markdown() -> None:
    """Prevent `$Token` in Markdown prose.

    Some Markdown previewers interpret `$...` as math delimiters; a stray `$MustBeEntity`
    can crash or heavily degrade preview. Use inline code spans instead: `$MustBeEntity`.
    """

    leaks: list[str] = []

    for p in ROOT.rglob("*.md"):
        rel = p.relative_to(ROOT)
        if any(part.startswith(".") for part in rel.parts):
            continue

        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = p.read_text(encoding="utf-8", errors="replace")

        for idx, raw in _iter_unfenced_markdown_lines(text):
            check = _strip_inline_code_spans(raw)
            if _DOLLAR_TOKEN_RE.search(check):
                leaks.append(f"- {rel}:{idx}: {raw.strip()}")

    if leaks:
        details = "\n".join(leaks)
        _fail(
            "Unfenced $Token found in Markdown prose. Wrap tokens in backticks or move them into a fenced code block.\n"
            "Example: use `$MustBeEntity`, not $MustBeEntity.\n"
            f"Found:\n{details}"
        )


def _gate_validation_terms_are_qualified() -> None:
    """Prevent ambiguous validate/validation phrasing in spec prose.

    The spec must distinguish schema-free well-formedness checking from schema-based
    semantic validation. This gate rejects prose uses of "validate"/"validation" that
    are not explicitly qualified (e.g., "schema validation" or "well-formedness").
    """

    targets = [
        *(p for p in (ROOT / "spec").glob("*/index.md") if p.is_file()),
        *(p for p in (ROOT / "spec").glob("*/bootstrap-schema/index.md") if p.is_file()),
    ]

    leaks: list[str] = []

    for p in targets:
        rel = p.relative_to(ROOT)
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = p.read_text(encoding="utf-8", errors="replace")

        for idx, raw in enumerate(text.splitlines(), start=1):
            check = _strip_inline_code_spans(raw)
            if not _VALIDATION_TERM_RE.search(check):
                continue
            if _VALIDATION_QUALIFIER_RE.search(check):
                continue
            leaks.append(f"- {rel}:{idx}: {raw.strip()}")

    if leaks:
        details = "\n".join(leaks)
        _fail(
            "Ambiguous validate/validation wording found in spec prose.\n"
            "Qualify as schema validation (semantic) or well-formedness checking, and avoid bare 'validate' phrasing.\n"
            f"Found:\n{details}"
        )


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: readiness_check.py", file=sys.stderr)
        return 2

    _gate_required_docs()
    _gate_no_rfc2119_leakage()
    _gate_validation_terms_are_qualified()
    _gate_no_unfenced_dollar_tokens_in_markdown()
    _gate_cdx_annotation_lint()
    _gate_conformance_smokecheck()
    _gate_no_json()

    print("ok: readiness_check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
