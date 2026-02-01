#!/usr/bin/env python3
"""Tight consistency scan for value-type tokens/types across spec, notes, and bootstrap schema.

This script intentionally performs *string-level* checks (no parsing dependencies) so it can
run in any environment. It is designed to be safe and deterministic.

Outputs:
- Spec built-in ValueType token set (from §11.6.1)
- Value-type tokens used by simplified bootstrap schema TraitDefinitions
- Tokens referenced by notes/types
- Missing tokens per layer
"""

from __future__ import annotations

import re
from pathlib import Path


def _read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def _extract_spec_builtin_value_type_tokens(spec_md: str) -> set[str]:
    # Extract the section body for "#### 11.6.1 Built-In Value Type Tokens".
    # Keep this tolerant to editorial wording changes by:
    # - matching the section heading literally
    # - consuming until the next Markdown heading of equal/higher level
    m = re.search(
        r"#### 11\.6\.1 Built-In Value Type Tokens\n(?P<body>.*?)(?:\n#### |\n### |\Z)",
        spec_md,
        flags=re.S,
    )
    if not m:
        raise RuntimeError(
            "Could not locate §11.6.1 Built-In Value Type Tokens section"
        )

    body = m.group("body")
    return set(re.findall(r"\$[A-Za-z0-9]+", body))


def _extract_simplified_schema_value_type_tokens(schema_cdx: str) -> set[str]:
    # Only tokens used as value-type tokens in trait definitions.
    tokens: set[str] = set()

    for m in re.finditer(r"defaultValueType=([^\s\]]+)", schema_cdx):
        tokens.update(re.findall(r"\$[A-Za-z0-9]+", m.group(1)))

    for m in re.finditer(r"defaultValueTypes=\[([^\]]+)\]", schema_cdx):
        tokens.update(re.findall(r"\$[A-Za-z0-9]+", m.group(1)))

    return tokens


def _extract_all_dollar_tokens(text: str) -> set[str]:
    return set(re.findall(r"\$[A-Za-z0-9]+", text))


def main() -> None:
    spec_md = _read("spec/1.0.0/index.md")
    notes_md = _read("notes/types/index.md")
    simplified_schema = _read("spec/1.0.0/bootstrap-schema/simplified/schema.cdx")

    spec_tokens = _extract_spec_builtin_value_type_tokens(spec_md)
    schema_value_tokens = _extract_simplified_schema_value_type_tokens(simplified_schema)
    notes_tokens = _extract_all_dollar_tokens(notes_md)

    missing_schema = sorted(schema_value_tokens - spec_tokens)
    missing_notes = sorted(notes_tokens - spec_tokens)

    print("== ValueType Token Consistency Scan ==")
    print(f"Spec built-in ValueType tokens: {len(spec_tokens)}")
    print(f"Simplified bootstrap schema value-type tokens used: {len(schema_value_tokens)}")
    print(f"Notes/types $tokens referenced: {len(notes_tokens)}")
    print()

    print(f"Missing (schema uses but spec does not list as built-in): {len(missing_schema)}")
    for t in missing_schema:
        print(f"  {t}")
    print()

    print(f"Missing (notes references but spec does not list as built-in): {len(missing_notes)}")
    # Keep output bounded.
    for t in missing_notes[:200]:
        print(f"  {t}")
    if len(missing_notes) > 200:
        print("  ... (truncated)")


if __name__ == "__main__":
    main()
