#!/usr/bin/env python3

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "conformance" / "0.1"


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
class ManifestCase:
    case_id: str
    input: str
    expected_canonical: str | None
    expected_error: str | None
    expected_primary_error_class: str | None


def _read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8")


def _move_to_foldered(rel_path: str) -> str:
    p = Path(rel_path)
    # <dir>/<name>.cdx or .json -> <dir>/<name>/data.cdx
    return str(p.parent / p.stem / "data.cdx")


def _move_file(from_rel: str, to_rel: str) -> None:
    src = (PACK / from_rel).resolve()
    dst = (PACK / to_rel).resolve()
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src == dst:
        return
    if not src.exists():
        # Allow re-running after partial migration.
        if dst.exists():
            return
        raise FileNotFoundError(str(src))
    shutil.move(str(src), str(dst))


def _convert_error_json_to_cdx(from_rel: str, to_rel: str) -> None:
    src = (PACK / from_rel).resolve()
    dst = (PACK / to_rel).resolve()

    # Allow re-running after partial migration.
    if not src.exists():
        if dst.exists():
            return
        raise FileNotFoundError(str(src))

    payload = _read_json(src)
    if not isinstance(payload, dict):
        raise ValueError(f"error payload must be object: {src}")

    primary = payload.get("primaryClass")
    notes = payload.get("notes", "")

    if primary not in ALLOWED_ERROR_CLASSES:
        raise ValueError(f"unexpected primaryClass {primary!r} in {src}")
    if not isinstance(notes, str):
        raise ValueError(f"notes must be string in {src}")

    # Minimal, schema-free Codex doc for smokecheck purposes.
    # (This file is a test artifact, not a normative Codex schema document.)
    def esc(s: str) -> str:
        return s.replace("\\", "\\\\").replace('"', '\\"')

    text = f'<ErrorExpectation primaryClass=${primary} notes="{esc(notes)}" />\n'
    _write_text(dst, text)

    # Remove old JSON
    if src.exists():
        src.unlink()


def main() -> int:
    manifest_json = PACK / "manifest.json"
    data = _read_json(manifest_json)
    if not isinstance(data, dict):
        raise SystemExit("manifest.json must be object")

    cases_raw = data.get("cases")
    if not isinstance(cases_raw, list):
        raise SystemExit("manifest.json cases must be list")

    cases: list[ManifestCase] = []
    for entry in cases_raw:
        if not isinstance(entry, dict):
            raise SystemExit("manifest case must be object")
        cases.append(
            ManifestCase(
                case_id=str(entry.get("id")),
                input=str(entry.get("input")),
                expected_canonical=entry.get("expectedCanonical"),
                expected_error=entry.get("expectedError"),
                expected_primary_error_class=entry.get("expectedPrimaryErrorClass"),
            )
        )

    # Move .cdx inputs and canonical outputs to foldered convention
    for c in cases:
        new_input = _move_to_foldered(c.input)
        _move_file(c.input, new_input)

        if c.expected_canonical is not None:
            new_canon = _move_to_foldered(str(c.expected_canonical))
            _move_file(str(c.expected_canonical), new_canon)

        if c.expected_error is not None:
            err_path = str(c.expected_error)
            if err_path.endswith(".json"):
                new_err = _move_to_foldered(err_path)
                _convert_error_json_to_cdx(err_path, new_err)
            else:
                new_err = _move_to_foldered(err_path)
                _move_file(err_path, new_err)

    # Write new Codex manifest
    manifest_dir = PACK / "manifest"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest_cdx = manifest_dir / "configuration.cdx"

    lines: list[str] = []
    lines.append(
        f"<ConformanceManifest version=\"{data.get('version','0.1')}\" specRoot=\"{data.get('specRoot','../../spec/0.1')}\">"
    )

    for case_index, c in enumerate(cases):
        attrs: list[str] = []
        attrs.append(f'id="{c.case_id}"')
        attrs.append(f'input="{_move_to_foldered(c.input)}"')

        if c.expected_canonical is not None:
            attrs.append(f'expectedCanonical="{_move_to_foldered(str(c.expected_canonical))}"')

        if c.expected_error is not None:
            attrs.append(f'expectedError="{_move_to_foldered(str(c.expected_error))}"')
            if c.expected_primary_error_class is not None:
                attrs.append(f'expectedPrimaryErrorClass=${c.expected_primary_error_class}')

        if len(attrs) <= 2:
            lines.append("\t<Case " + " ".join(attrs) + " />")
        else:
            lines.append("\t<Case")
            for a in attrs:
                lines.append(f"\t\t{a}")
            lines.append("\t/>")

        if case_index != len(cases) - 1:
            lines.append("")

    lines.append("</ConformanceManifest>")
    _write_text(manifest_cdx, "\n".join(lines))

    # Update legacy JSON manifest paths to keep it consistent (deprecated)
    new_cases_json: list[dict] = []
    for c in cases_raw:
        c2 = dict(c)
        c2["input"] = _move_to_foldered(str(c2["input"]))
        if c2.get("expectedCanonical") is not None:
            c2["expectedCanonical"] = _move_to_foldered(str(c2["expectedCanonical"]))
        if c2.get("expectedError") is not None:
            c2["expectedError"] = _move_to_foldered(str(c2["expectedError"]))
        new_cases_json.append(c2)

    data["cases"] = new_cases_json
    manifest_json.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
