#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import sys
import re
from pathlib import Path


_RFC2119_RE = re.compile(r"\b(MUST NOT|MUST|MAY)\b")


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


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: readiness_check.py", file=sys.stderr)
        return 2

    _gate_required_docs()
    _gate_no_rfc2119_leakage()
    _gate_conformance_smokecheck()
    _gate_no_json()

    print("ok: readiness_check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
