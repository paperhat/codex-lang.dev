#!/usr/bin/env python3

from __future__ import annotations

import json
import re
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
    schema_path: Path | None
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


_ATTR_RE = re.compile(r'(\w+)=(\$[A-Za-z]+|"(?:\\.|[^"])*")')


def _parse_cdx_attrs(tag_text: str) -> dict[str, str]:
    attrs: dict[str, str] = {}
    for m in _ATTR_RE.finditer(tag_text):
        key = m.group(1)
        raw = m.group(2)
        if raw.startswith('$'):
            value = raw[1:]
        else:
            # JSON text unescape is close enough for our controlled fixtures.
            value = json.loads(raw)
        attrs[key] = value
    return attrs


def _cases_from_manifest_entries(entries: Iterable[dict[str, Any]], manifest_dir: Path) -> list[Case]:
    cases: list[Case] = []
    seen_ids: set[str] = set()

    for entry in entries:
        case_id = entry.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            _fail("each case must have a non-empty text id")
        if case_id in seen_ids:
            _fail(f"duplicate case id: {case_id}")
        seen_ids.add(case_id)

        input_rel = entry.get("input")
        if not isinstance(input_rel, str) or not input_rel.strip():
            _fail(f"case {case_id}: missing input")
        input_path = (manifest_dir / input_rel).resolve()

        schema_rel = entry.get("schema")
        schema_path: Path | None
        if schema_rel is None:
            schema_path = None
        else:
            if not isinstance(schema_rel, str) or not schema_rel.strip():
                _fail(f"case {case_id}: schema must be a text or null")
            schema_path = (manifest_dir / schema_rel).resolve()

        canonical_rel = entry.get("expectedCanonical")
        expected_canonical_path: Path | None
        if canonical_rel is None:
            expected_canonical_path = None
        else:
            if not isinstance(canonical_rel, str) or not canonical_rel.strip():
                _fail(f"case {case_id}: expectedCanonical must be a text or null")
            expected_canonical_path = (manifest_dir / canonical_rel).resolve()

        error_rel = entry.get("expectedError")
        expected_error_path: Path | None
        if error_rel is None:
            expected_error_path = None
        else:
            if not isinstance(error_rel, str) or not error_rel.strip():
                _fail(f"case {case_id}: expectedError must be a text or null")
            expected_error_path = (manifest_dir / error_rel).resolve()

        expected_primary_error_class = entry.get("expectedPrimaryErrorClass")
        if expected_primary_error_class is not None:
            if not isinstance(expected_primary_error_class, str) or not expected_primary_error_class.strip():
                _fail(f"case {case_id}: expectedPrimaryErrorClass must be a text or null")
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
                schema_path=schema_path,
                expected_canonical_path=expected_canonical_path,
                expected_error_path=expected_error_path,
                expected_primary_error_class=expected_primary_error_class,
            )
        )

    return cases


def _load_manifest_json(path: Path) -> list[Case]:
    data = json.loads(_read_text(path))
    if not isinstance(data, dict):
        _fail("manifest must be a JSON object")

    cases_raw = data.get("cases")
    if not isinstance(cases_raw, list):
        _fail("manifest.cases must be an array")

    manifest_dir = path.parent
    return _cases_from_manifest_entries(cases_raw, manifest_dir)


def _load_manifest_cdx(path: Path) -> list[Case]:
    text = _read_text(path)
    _assert_lf_newlines(text, path)
    _assert_trailing_newline(text, path)

    # This is a fixture pack manifest, not a general Codex parser. We only accept
    # a constrained surface form: a <ConformanceManifest> with <Case ... /> children.
    case_entries: list[dict[str, Any]] = []
    lines = text.splitlines()
    line_index = 0
    while line_index < len(lines):
        line = lines[line_index].strip()
        if not line.startswith("<Case"):
            line_index += 1
            continue

        tag_text = line
        while not tag_text.rstrip().endswith("/>"):
            line_index += 1
            if line_index >= len(lines):
                _fail(f"unterminated <Case ... /> entry in manifest: {path}")
            tag_text = f"{tag_text} {lines[line_index].strip()}"

        attrs = _parse_cdx_attrs(tag_text)

        entry: dict[str, Any] = {
            "id": attrs.get("id"),
            "input": attrs.get("input"),
            "schema": attrs.get("schema"),
            "expectedCanonical": attrs.get("expectedCanonical"),
            "expectedError": attrs.get("expectedError"),
            "expectedPrimaryErrorClass": attrs.get("expectedPrimaryErrorClass"),
        }

        # normalize missing optional traits
        if entry["expectedCanonical"] is None:
            entry["expectedCanonical"] = None
        if entry["expectedError"] is None:
            entry["expectedError"] = None

        case_entries.append(entry)

        line_index += 1

    if not case_entries:
        _fail(f"no <Case ... /> entries found in manifest: {path}")

    manifest_dir = path.parent.parent  # conformance/<version>
    return _cases_from_manifest_entries(case_entries, manifest_dir)


def _load_manifest(path: Path) -> list[Case]:
    if path.suffix.lower() == ".json":
        return _load_manifest_json(path)
    if path.suffix.lower() == ".cdx":
        return _load_manifest_cdx(path)
    _fail("manifest must be .json or .cdx")


def _validate_error_payload(path: Path, expected_class: str) -> None:
    if path.suffix.lower() == ".json":
        payload = json.loads(_read_text(path))
        if not isinstance(payload, dict):
            _fail(f"error payload must be an object: {path}")
        primary = payload.get("primaryClass")
        if primary != expected_class:
            _fail(f"error payload {path} primaryClass={primary!r} does not match expected {expected_class!r}")
        return

    if path.suffix.lower() != ".cdx":
        _fail(f"error payload must be .json or .cdx: {path}")

    text = _read_text(path).strip()
    if not text.startswith("<ErrorExpectation"):
        _fail(f"error payload must start with <ErrorExpectation ... />: {path}")
    attrs = _parse_cdx_attrs(text)
    primary = attrs.get("primaryClass")
    if primary != expected_class:
        _fail(f"error payload {path} primaryClass={primary!r} does not match expected {expected_class!r}")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: conformance_smokecheck.py <path/to/manifest.(json|cdx)>", file=sys.stderr)
        return 2

    manifest_path = Path(argv[1]).resolve()
    cases = _load_manifest(manifest_path)

    # Validate all referenced files exist + are LF + trailing newline.
    for c in cases:
        input_text = _read_text(c.input_path)
        _assert_lf_newlines(input_text, c.input_path)
        _assert_trailing_newline(input_text, c.input_path)

        if c.schema_path is not None:
            schema_text = _read_text(c.schema_path)
            _assert_lf_newlines(schema_text, c.schema_path)
            _assert_trailing_newline(schema_text, c.schema_path)

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
