#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_ROOT = ROOT / "spec" / "1.0.0"
DEFAULT_SCHEMAS_ROOT_CANDIDATES = [
    # historical mono-repo layout (schemas folder beside codex-lang.dev)
    ROOT.parent / "schemas",
    # current mono-repo layout for Paperhat
    ROOT.parent / "paperhat.dev" / "DRAFT" / "schemas",
    # fall back: local to codex-lang.dev (if present)
    ROOT / "schemas",
]

SIGIL_RE = re.compile(r"\$[A-Za-z][A-Za-z0-9]*")
TRAIT_RE = re.compile(r"\b([a-z][A-Za-z0-9]*)=")
CONCEPT_RE = re.compile(r"<\s*/?\s*([A-Za-z][A-Za-z0-9]*)\b")


def _escape_text(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _read_all_spec_text() -> str:
    parts: list[str] = []
    for p in SPEC_ROOT.rglob("*.md"):
        parts.append(p.read_text(encoding="utf-8"))
    return "\n".join(parts)


def _read_unified_spec_text() -> str:
    return (SPEC_ROOT / "index.md").read_text(encoding="utf-8")


def _collect_schema_tokens(*, schemas_root: Path) -> dict[str, list[str]]:
    schema_files = sorted(schemas_root.rglob("*.cdx"))

    sigils: set[str] = set()
    traits: set[str] = set()
    concepts: set[str] = set()
    bool_literals: set[str] = set()

    for p in schema_files:
        t = p.read_text(encoding="utf-8")
        sigils |= set(SIGIL_RE.findall(t))
        traits |= set(TRAIT_RE.findall(t))
        concepts |= set(CONCEPT_RE.findall(t))

        if re.search(r"\btrue\b", t):
            bool_literals.add("true")
        if re.search(r"\bfalse\b", t):
            bool_literals.add("false")

    return {
        "schemaFiles": [str(p.relative_to(ROOT.parent)) for p in schema_files],
        "sigils": sorted(sigils),
        "traits": sorted(traits),
        "concepts": sorted(concepts),
        "boolLiterals": sorted(bool_literals),
    }


def _resolve_schemas_root(arg: str | None) -> Path:
    if arg:
        p = Path(arg)
        if not p.is_absolute():
            p = (ROOT.parent / p).resolve()
        if not p.exists():
            raise SystemExit(f"schemas root not found at {p}")
        return p

    for candidate in DEFAULT_SCHEMAS_ROOT_CANDIDATES:
        if candidate.exists():
            return candidate

    joined = "\n".join(f"- {c}" for c in DEFAULT_SCHEMAS_ROOT_CANDIDATES)
    raise SystemExit(
        "schemas root not found. Tried:\n" + joined + "\n\n" + "Pass --schemas-root to set it explicitly."
    )


def _write_report_cdx(
    *,
    out_path: Path,
    schema_file_count: int,
    schemas_root: str,
    spec_root: str,
    missing_sigils: list[str],
    missing_traits: list[str],
    missing_concepts: list[str],
) -> None:
    lines: list[str] = []
    lines.append(
    '<SchemasVsSpecAuditReport version="0.1" kind="heuristic" '
    f'schemaFileCount={schema_file_count} schemasRoot="{_escape_text(schemas_root)}" specRoot="{_escape_text(spec_root)}">'
    )
    lines.append("\t<Notes>")
    lines.append(
        '\t\t<Note text="This is a heuristic: it only checks whether a token word appears anywhere in spec Markdown." />'
    )
    lines.append(
        '\t\t<Note text="Items listed as missing are candidates for deeper review, not automatically spec bugs." />'
    )
    lines.append("\t</Notes>")
    lines.append("")

    lines.append("\t<MissingSigils>")
    for s in missing_sigils:
         lines.append(f'\t\t<Sigil value="{_escape_text(s)}" />')
    lines.append("\t</MissingSigils>")
    lines.append("")

    lines.append("\t<MissingTraits>")
    for t in missing_traits:
         lines.append(f'\t\t<Trait value="{_escape_text(t)}" />')
    lines.append("\t</MissingTraits>")
    lines.append("")

    lines.append("\t<MissingConcepts>")
    for c in missing_concepts:
         lines.append(f'\t\t<Concept value="{_escape_text(c)}" />')
    lines.append("\t</MissingConcepts>")
    lines.append("</SchemasVsSpecAuditReport>")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Heuristic audit: schema tokens vs spec markdown")
    parser.add_argument(
        "--schemas-root",
        help=(
            "Directory to scan for *.cdx schema files. May be absolute or relative to the repo root. "
            "If omitted, tries common mono-repo locations."
        ),
    )
    parser.add_argument(
        "--spec-scope",
        choices=["unified", "all"],
        default="unified",
        help=(
            "Which spec markdown to scan for token appearances. 'unified' scans only spec/1.0.0/index.md "
            "(recommended after consolidation). 'all' scans all markdown under spec/0.1/."
        ),
    )
    args = parser.parse_args()

    schemas_root = _resolve_schemas_root(args.schemas_root)

    if args.spec_scope == "all":
        spec_text = _read_all_spec_text()
        spec_root_label = str(SPEC_ROOT.relative_to(ROOT))
    else:
        spec_text = _read_unified_spec_text()
        spec_root_label = str((SPEC_ROOT / "index.md").relative_to(ROOT))

    spec_words = set(re.findall(r"\b[A-Za-z][A-Za-z0-9]*\b", spec_text))

    schema = _collect_schema_tokens(schemas_root=schemas_root)

    missing_sigils = sorted(s[1:] for s in schema["sigils"] if s[1:] not in spec_words)
    missing_traits = sorted(t for t in schema["traits"] if t not in spec_words)
    missing_concepts = sorted(c for c in schema["concepts"] if c not in spec_words)

    out_path = ROOT / "tools" / "schemas_vs_spec_audit_report.cdx"
    _write_report_cdx(
        out_path=out_path,
        schema_file_count=len(schema["schemaFiles"]),
        schemas_root=str(schemas_root.relative_to(ROOT.parent)),
        spec_root=spec_root_label,
        missing_sigils=missing_sigils,
        missing_traits=missing_traits,
        missing_concepts=missing_concepts,
    )

    print(f"wrote {out_path}")
    print(f"schema files: {len(schema['schemaFiles'])}")
    print(f"missing sigils (heuristic): {len(missing_sigils)}")
    print(f"missing traits (heuristic): {len(missing_traits)}")
    print(f"missing concepts (heuristic): {len(missing_concepts)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
