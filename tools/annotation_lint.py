#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Annotation:
    path: Path
    start_line: int  # 1-based
    end_line: int  # 1-based
    form: str  # "inline" | "block"
    raw_text: str | None  # inline only, inside brackets
    canonical_text: str | None  # inline only, inside brackets


_GROUPING_RE = re.compile(r"^(GROUP|END):\s*(.+)$")


def _is_blank(line: str) -> bool:
    return line.strip() == ""


def _count_blank_lines_above(lines: list[str], start_line_1: int) -> int:
    i = start_line_1 - 2
    c = 0
    while i >= 0 and _is_blank(lines[i]):
        c += 1
        i -= 1
    return c


def _count_blank_lines_below(lines: list[str], end_line_1: int) -> int:
    i = end_line_1
    c = 0
    while i < len(lines) and _is_blank(lines[i]):
        c += 1
        i += 1
    return c


def _file_boundary_counts_as_blank_above(start_line_1: int) -> bool:
    return start_line_1 == 1


def _file_boundary_counts_as_blank_below(lines: list[str], end_line_1: int) -> bool:
    return end_line_1 == len(lines)


def _find_inline_closing_bracket(text: str, open_index: int) -> int | None:
    # Returns index of the closing ']' not escaped as '\]'.
    i = open_index + 1
    while i < len(text):
        ch = text[i]
        if ch == "\\" and i + 1 < len(text) and text[i + 1] == "]":
            i += 2
            continue
        if ch == "]":
            return i
        i += 1
    return None


def _canonicalize_inline_text(raw: str) -> str:
    # Spec §8.9.4.1: trim + collapse whitespace runs to a single space.
    raw = raw.strip()
    # Collapse any run of whitespace characters.
    raw = re.sub(r"\s+", " ", raw)
    return raw


def _is_concept_opening_marker(line: str) -> bool:
    # Heuristic for surface-form concept opening marker.
    s = line.lstrip()
    return s.startswith("<") and not s.startswith("</")


def _parse_annotations(path: Path, text: str) -> tuple[list[Annotation], list[str]]:
    errors: list[str] = []
    lines = text.splitlines()
    annotations: list[Annotation] = []

    line_index = 0
    while line_index < len(lines):
        line = lines[line_index]
        stripped = line.lstrip()

        # An annotation opening '[' must be the first non-whitespace character on its line.
        if not stripped.startswith("["):
            line_index += 1
            continue

        # Block annotation opener: '[' only on the line (aside from whitespace)
        if stripped.strip() == "[":
            start = line_index + 1
            end_index = None
            j = line_index + 1
            while j < len(lines):
                close_stripped = lines[j].lstrip()
                if close_stripped.strip() == "]":
                    end_index = j
                    break
                j += 1
            if end_index is None:
                errors.append(
                    f"{path.relative_to(ROOT)}:{start}: unterminated block annotation (missing closing ']')"
                )
                break

            annotations.append(
                Annotation(
                    path=path,
                    start_line=start,
                    end_line=end_index + 1,
                    form="block",
                    raw_text=None,
                    canonical_text=None,
                )
            )
            line_index = end_index + 1
            continue

        # Otherwise it must be an inline annotation with closing ']' on the same line.
        open_pos = line.find("[")
        if open_pos == -1 or open_pos != len(line) - len(stripped):
            # Should be unreachable given the startswith('[') check.
            line_index += 1
            continue

        close_pos = _find_inline_closing_bracket(line, open_pos)
        if close_pos is None:
            errors.append(
                f"{path.relative_to(ROOT)}:{line_index + 1}: inline annotation missing closing ']' on same line"
            )
            line_index += 1
            continue

        trailing = line[close_pos + 1 :]
        if trailing.strip() != "":
            # In this repo, annotations are treated as standalone lines (consistent with §8.9 being editorial metadata).
            # If you intended content starting with '[', escape it as '\[' (see spec example in §8.9 prelude).
            errors.append(
                f"{path.relative_to(ROOT)}:{line_index + 1}: non-whitespace after inline annotation closing ']' (escape a leading '[' in content with \\[)"
            )
            line_index += 1
            continue

        raw = line[open_pos + 1 : close_pos]
        canon = _canonicalize_inline_text(raw)
        annotations.append(
            Annotation(
                path=path,
                start_line=line_index + 1,
                end_line=line_index + 1,
                form="inline",
                raw_text=raw,
                canonical_text=canon,
            )
        )
        line_index += 1

    return annotations, errors


def _lint_file(path: Path) -> list[str]:
    errors: list[str] = []

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append(f"{path.relative_to(ROOT)}: file is not valid UTF-8")
        return errors

    annotations, parse_errors = _parse_annotations(path, text)
    errors.extend(parse_errors)
    if parse_errors:
        return errors

    lines = text.splitlines()

    # Determine grouping annotations and validate GROUP/END nesting.
    grouping: list[tuple[Annotation, str, str]] = []  # (annotation, kind, label)
    for a in annotations:
        if a.form != "inline" or a.canonical_text is None:
            continue
        m = _GROUPING_RE.match(a.canonical_text)
        if not m:
            continue
        kind = m.group(1)
        label = _canonicalize_inline_text(m.group(2))
        if label == "":
            errors.append(
                f"{path.relative_to(ROOT)}:{a.start_line}: grouping annotation label must be non-empty"
            )
            continue
        grouping.append((a, kind, label))

    stack: list[tuple[str, int]] = []
    for a, kind, label in grouping:
        if kind == "GROUP":
            stack.append((label, a.start_line))
        else:
            if not stack:
                errors.append(
                    f"{path.relative_to(ROOT)}:{a.start_line}: END without open GROUP ({label})"
                )
                continue
            top_label, top_line = stack.pop()
            if top_label != label:
                errors.append(
                    f"{path.relative_to(ROOT)}:{a.start_line}: END label mismatch (got {label!r}, expected {top_label!r} from line {top_line})"
                )

    for label, ln in stack:
        errors.append(
            f"{path.relative_to(ROOT)}:{ln}: GROUP not closed (missing END: {label})"
        )

    # Classify attached annotation stacks.
    annotations_by_start = sorted(annotations, key=lambda a: (a.start_line, a.end_line))
    is_grouping_line = {a.start_line for (a, _, _) in grouping}
    attached: set[int] = set()  # start_line for annotations classified as attached

    i = 0
    while i < len(annotations_by_start):
        a = annotations_by_start[i]
        if a.start_line in is_grouping_line:
            i += 1
            continue

        # Build a contiguous stack of non-grouping annotations with no blank lines between them.
        stack_items = [a]
        j = i
        while j + 1 < len(annotations_by_start):
            nxt = annotations_by_start[j + 1]
            if nxt.start_line in is_grouping_line:
                break
            blanks_between = _count_blank_lines_below(lines, stack_items[-1].end_line)
            if blanks_between != 0:
                break
            # Ensure the next annotation starts immediately after, ignoring non-blank content.
            # If there is any non-blank content between, this is not a stacked annotation sequence.
            if nxt.start_line != stack_items[-1].end_line + 1:
                break
            stack_items.append(nxt)
            j += 1

        # Determine what comes next after the last annotation in the stack.
        last = stack_items[-1]
        # Next non-blank line after last.end_line
        k = last.end_line
        while k < len(lines) and _is_blank(lines[k]):
            k += 1

        if (
            k < len(lines)
            and _is_concept_opening_marker(lines[k])
            and _count_blank_lines_below(lines, last.end_line) == 0
        ):
            for item in stack_items:
                attached.add(item.start_line)

        i = j + 1

    # Enforce canonical blank-line requirements (§8.9.8) and kind exhaustiveness.
    for a in annotations_by_start:
        above = _count_blank_lines_above(lines, a.start_line)
        below = _count_blank_lines_below(lines, a.end_line)

        is_grouping = a.start_line in is_grouping_line
        is_attached = a.start_line in attached

        if is_grouping:
            ok_above = _file_boundary_counts_as_blank_above(a.start_line) or above == 1
            ok_below = (
                _file_boundary_counts_as_blank_below(lines, a.end_line) or below == 1
            )
            if not ok_above or (
                above > 1 and not _file_boundary_counts_as_blank_above(a.start_line)
            ):
                errors.append(
                    f"{path.relative_to(ROOT)}:{a.start_line}: grouping annotation must have exactly one blank line above"
                )
            if not ok_below or (
                below > 1
                and not _file_boundary_counts_as_blank_below(lines, a.end_line)
            ):
                errors.append(
                    f"{path.relative_to(ROOT)}:{a.end_line}: grouping annotation must have exactly one blank line below"
                )
            continue

        if is_attached:
            # Must be directly above the next concept opening marker with no blank line.
            if _count_blank_lines_below(lines, a.end_line) != 0:
                errors.append(
                    f"{path.relative_to(ROOT)}:{a.end_line}: attached annotation must have no blank line below"
                )
            continue

        # Not grouping, not attached => must be general.
        ok_above = _file_boundary_counts_as_blank_above(a.start_line) or above == 1
        ok_below = _file_boundary_counts_as_blank_below(lines, a.end_line) or below == 1
        if ok_above and ok_below:
            continue

        errors.append(
            f"{path.relative_to(ROOT)}:{a.start_line}: annotation is neither attached, grouping, nor general (blank-line requirements not met)"
        )

    return errors


def _iter_cdx_files(
    paths: list[Path], *, include_invalid_conformance_cases: bool
) -> list[Path]:
    out: list[Path] = []
    for p in paths:
        p = p.resolve()
        if p.is_file():
            if p.suffix.lower() == ".cdx":
                out.append(p)
            continue
        if p.is_dir():
            for f in p.rglob("*.cdx"):
                rel = f.relative_to(ROOT)
                if any(part.startswith(".") for part in rel.parts):
                    continue
                if not include_invalid_conformance_cases:
                    parts = rel.parts
                    for i in range(len(parts) - 2):
                        if parts[i] == "cases" and parts[i + 1] == "invalid":
                            break
                    else:
                        out.append(f.resolve())
                        continue
                    continue
                out.append(f.resolve())
    return sorted(set(out))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Lint Codex annotations (syntax + §8.9 blank-line/kind rules)"
    )
    parser.add_argument(
        "--include-invalid",
        action="store_true",
        help="Also scan conformance/ cases/invalid/ fixtures (which may intentionally contain invalid annotations)",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Files or directories to scan (default: spec/ and conformance/)",
    )
    args = parser.parse_args(argv[1:])

    if args.paths:
        roots = [Path(p) if Path(p).is_absolute() else (ROOT / p) for p in args.paths]
    else:
        roots = [
            ROOT / "spec",
            ROOT / "conformance" / "1.0.0" / "manifest",
            ROOT / "conformance" / "1.0.0" / "expected",
            ROOT / "conformance" / "1.0.0" / "cases" / "valid",
        ]

    files = _iter_cdx_files(
        roots, include_invalid_conformance_cases=args.include_invalid
    )
    all_errors: list[str] = []
    for f in files:
        all_errors.extend(_lint_file(f))

    if all_errors:
        print("annotation_lint: FAILED", file=sys.stderr)
        for e in all_errors:
            print(f"- {e}", file=sys.stderr)
        return 1

    print(f"annotation_lint: ok ({len(files)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
