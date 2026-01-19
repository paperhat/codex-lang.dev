#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


ALLOWED_ERROR_CLASSES = {
    "ParseError",
    "SurfaceFormError",
    "FormattingError",
    "SchemaError",
    "IdentityError",
    "ReferenceError",
    "CollectionError",
    "ContextError",
    "ConstraintError",
}


@dataclass(frozen=True)
class Case:
    case_id: str
    input_path: Path
    expected_canonical_path: Path | None
    expected_error_path: Path | None
    expected_primary_error_class: str | None


def _fail(message: str) -> None:
    raise SystemExit(f"conformance_smokecheck: {message}")


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        _fail(f"missing file: {path}")


def _assert_lf_newlines(text: str, path: Path) -> None:
    if "\r" in text:
        _fail(f"CR/CRLF found in {path} (fixtures must use LF only)")


def _assert_trailing_newline(text: str, path: Path) -> None:
    if not text.endswith("\n"):
        _fail(f"missing trailing newline in {path}")


def _load_manifest(path: Path) -> list[Case]:
    data = json.loads(_read_text(path))
    if not isinstance(data, dict):
        _fail("manifest must be a JSON object")

    cases_raw = data.get("cases")
    if not isinstance(cases_raw, list):
        _fail("manifest.cases must be an array")

    manifest_dir = path.parent

    cases: list[Case] = []
    seen_ids: set[str] = set()

    for entry in cases_raw:
        if not isinstance(entry, dict):
            _fail("each manifest case must be an object")

        case_id = entry.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            _fail("each case must have a non-empty string id")
        if case_id in seen_ids:
            _fail(f"duplicate case id: {case_id}")
        seen_ids.add(case_id)

        input_rel = entry.get("input")
        if not isinstance(input_rel, str) or not input_rel.strip():
            _fail(f"case {case_id}: missing input")
        input_path = (manifest_dir / input_rel).resolve()

        canonical_rel = entry.get("expectedCanonical")
        expected_canonical_path: Path | None
        if canonical_rel is None:
            expected_canonical_path = None
        else:
            if not isinstance(canonical_rel, str) or not canonical_rel.strip():
                _fail(f"case {case_id}: expectedCanonical must be a string or null")
            expected_canonical_path = (manifest_dir / canonical_rel).resolve()

        error_rel = entry.get("expectedError")
        expected_error_path: Path | None
        if error_rel is None:
            expected_error_path = None
        else:
            if not isinstance(error_rel, str) or not error_rel.strip():
                _fail(f"case {case_id}: expectedError must be a string or null")
            expected_error_path = (manifest_dir / error_rel).resolve()

        expected_primary_error_class = entry.get("expectedPrimaryErrorClass")
        if expected_primary_error_class is not None:
            if not isinstance(expected_primary_error_class, str) or not expected_primary_error_class.strip():
                _fail(f"case {case_id}: expectedPrimaryErrorClass must be a string or null")
            if expected_primary_error_class not in ALLOWED_ERROR_CLASSES:
                _fail(
                    f"case {case_id}: expectedPrimaryErrorClass must be one of {sorted(ALLOWED_ERROR_CLASSES)}"
                )

        # Basic invariants:
        # - valid case: canonical may be present, error must be null
        # - invalid case: error must be present, canonical must be null
        if expected_error_path is None and expected_primary_error_class is not None:
            _fail(f"case {case_id}: expectedPrimaryErrorClass provided but expectedError is null")
        if expected_error_path is not None and expected_primary_error_class is None:
            _fail(f"case {case_id}: expectedError provided but expectedPrimaryErrorClass is null")
        if expected_error_path is not None and expected_canonical_path is not None:
            _fail(f"case {case_id}: cannot have both expectedError and expectedCanonical")

        cases.append(
            Case(
                case_id=case_id,
                input_path=input_path,
                expected_canonical_path=expected_canonical_path,
                expected_error_path=expected_error_path,
                expected_primary_error_class=expected_primary_error_class,
            )
        )

    return cases


def _validate_error_payload(path: Path, expected_class: str) -> None:
    payload = json.loads(_read_text(path))
    if not isinstance(payload, dict):
        _fail(f"error payload must be an object: {path}")

    primary = payload.get("primaryClass")
    if primary != expected_class:
        _fail(f"error payload {path} primaryClass={primary!r} does not match expected {expected_class!r}")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: conformance_smokecheck.py <path/to/manifest.json>", file=sys.stderr)
        return 2

    manifest_path = Path(argv[1]).resolve()
    cases = _load_manifest(manifest_path)

    # Validate all referenced files exist + are LF + trailing newline.
    for c in cases:
        input_text = _read_text(c.input_path)
        _assert_lf_newlines(input_text, c.input_path)
        _assert_trailing_newline(input_text, c.input_path)

        if c.expected_canonical_path is not None:
            canonical_text = _read_text(c.expected_canonical_path)
            _assert_lf_newlines(canonical_text, c.expected_canonical_path)
            _assert_trailing_newline(canonical_text, c.expected_canonical_path)

        if c.expected_error_path is not None:
            _validate_error_payload(c.expected_error_path, c.expected_primary_error_class or "")

    print(f"ok: {len(cases)} conformance cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
