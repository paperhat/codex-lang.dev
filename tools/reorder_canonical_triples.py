#!/usr/bin/env python3
"""Reorder RdfTriple elements in the canonical bootstrap schema per §9.6.2.

Sorts triples in ascending lexicographic order of (subject, predicate, objectKey)
where objectKey is:
  - `object` when the object is an IRI (has object= trait)
  - `(datatypeOrDefault, lexical)` when the object is a literal (has lexical= trait)
  - If no explicit datatype=, default is http://www.w3.org/2001/XMLSchema#string

Also removes duplicate triples and GROUP/END annotations.
Preserves the top-level MARKDOWN block annotation.

Dry-run by default; pass --apply to write changes.
"""

import sys
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "spec" / "1.0.0" / "bootstrap-schema" / "schema.cdx"

XSD_STRING = "http://www.w3.org/2001/XMLSchema#string"

# Indentation for triples: two tabs (one for RdfGraph, one for child level)
TRIPLE_INDENT = "\t\t"
# Indentation for multiline trait lines: three tabs
TRAIT_INDENT = "\t\t\t"


def parse_trait_value(s, start):
    """Parse a trait value starting at position `start` in string `s`.

    Returns (value, end_position). Values can be:
    - Quoted: "..." (may contain spaces, escapes)
    - Unquoted: sequence of non-whitespace, non-/ characters
    """
    if start < len(s) and s[start] == '"':
        # Quoted value
        i = start + 1
        while i < len(s):
            if s[i] == '\\' and i + 1 < len(s):
                i += 2
            elif s[i] == '"':
                return s[start:i + 1], i + 1
            else:
                i += 1
        # Unterminated quote (shouldn't happen in valid file)
        return s[start:], len(s)
    else:
        # Unquoted value: ends at whitespace or end of string
        # But must not include trailing /> or >
        i = start
        while i < len(s) and s[i] not in (' ', '\t', '\n', '\r'):
            i += 1
        return s[start:i], i


def parse_inline_traits(trait_text):
    """Parse traits from an inline string like 'datatype=... lexical="val" predicate=... subject=...'

    Returns dict of {trait_name: trait_value}.
    """
    traits = {}
    i = 0
    n = len(trait_text)
    while i < n:
        # Skip whitespace
        while i < n and trait_text[i] in (' ', '\t'):
            i += 1
        if i >= n:
            break
        # Find =
        eq_pos = trait_text.find('=', i)
        if eq_pos < 0:
            break
        name = trait_text[i:eq_pos]
        if not name:
            break
        # Parse value
        value, end = parse_trait_value(trait_text, eq_pos + 1)
        traits[name] = value
        i = end
    return traits


def parse_triple_block(lines):
    """Parse an RdfTriple element from its lines.

    A triple can be:
    - Single line: <RdfTriple trait1=v1 trait2=v2 />
    - Multiline:
        <RdfTriple
            trait1=v1
            trait2=v2
            ...
        />

    Returns dict of {trait_name: trait_value} or None if not a triple.
    """
    first_line = lines[0].strip()
    if not first_line.startswith("<RdfTriple"):
        return None

    if len(lines) == 1:
        # Single-line triple: <RdfTriple traits... />
        # Extract between "<RdfTriple " and " />"
        inner = first_line[len("<RdfTriple "):]
        # Remove trailing />
        if inner.endswith("/>"):
            inner = inner[:-2].rstrip()
        elif inner.endswith(">"):
            inner = inner[:-1].rstrip()
        return parse_inline_traits(inner)
    else:
        # Multiline triple
        traits = {}
        for line in lines[1:]:
            stripped = line.strip()
            if stripped in ("/>" , ">"):
                continue
            # Each line is "traitName=value"
            eq_pos = stripped.find('=')
            if eq_pos < 0:
                continue
            name = stripped[:eq_pos]
            value = stripped[eq_pos + 1:]
            traits[name] = value
        return traits


def sort_key_for_triple(traits):
    """Compute the §9.6.2 sort key: (subject, predicate, objectKey).

    objectKey is:
    - object value when object is an IRI (has 'object' trait)
    - (datatypeOrDefault, lexical) when object is a literal (has 'lexical' trait)
    """
    subject = traits.get("subject", "")
    predicate = traits.get("predicate", "")

    if "object" in traits:
        # IRI object: objectKey = object (single string).
        # Flatten into the sort tuple as a 1-tuple so that IRI triples produce
        # (subject, predicate, object) and literal triples produce
        # (subject, predicate, datatype, lexical). Python tuple comparison
        # handles differing lengths correctly (shorter < longer when prefix matches).
        object_key = (traits["object"],)
    elif "lexical" in traits:
        datatype = traits.get("datatype", XSD_STRING)
        lexical = traits["lexical"]
        object_key = (datatype, lexical)
    else:
        # Shouldn't happen for valid triples
        object_key = ("",)

    return (subject, predicate) + object_key


def identity_key_for_triple(traits):
    """Compute a hashable identity key for duplicate detection.

    Two triples are identical if they have the same (subject, predicate, object)
    for IRI objects, or (subject, predicate, datatype, lexical) for literals,
    with default datatype applied.
    """
    subject = traits.get("subject", "")
    predicate = traits.get("predicate", "")

    if "object" in traits:
        return ("iri", subject, predicate, traits["object"])
    elif "lexical" in traits:
        datatype = traits.get("datatype", XSD_STRING)
        lexical = traits["lexical"]
        return ("literal", subject, predicate, datatype, lexical)
    else:
        # Fallback: use all traits
        return tuple(sorted(traits.items()))


def format_triple(traits):
    """Format a triple in canonical Codex surface form.

    Rules per §8.5-6:
    - Traits alphabetical by name
    - 1-2 traits: inline on one line
    - 3+ traits: multiline, each on own indented line, /> on own line
    - No whitespace around =
    - Self-closing />
    """
    sorted_names = sorted(traits.keys())
    n = len(sorted_names)

    if n <= 2:
        # Inline form
        parts = []
        for name in sorted_names:
            parts.append(f"{name}={traits[name]}")
        return TRIPLE_INDENT + "<RdfTriple " + " ".join(parts) + " />"
    else:
        # Multiline form
        lines = [TRIPLE_INDENT + "<RdfTriple"]
        for name in sorted_names:
            lines.append(TRAIT_INDENT + f"{name}={traits[name]}")
        lines.append(TRIPLE_INDENT + "/>")
        return "\n".join(lines)


def is_group_annotation(line):
    """Check if a line is a GROUP: or END: annotation."""
    stripped = line.strip()
    return (stripped.startswith("[GROUP:") and stripped.endswith("]")) or \
           (stripped.startswith("[END:") and stripped.endswith("]"))


def is_single_line_annotation(line):
    """Check if a line is a single-line annotation (non-block)."""
    stripped = line.strip()
    return stripped.startswith("[") and stripped.endswith("]") and "\n" not in stripped


def main():
    apply_mode = "--apply" in sys.argv

    if not SCHEMA_PATH.exists():
        print(f"Error: Schema file not found: {SCHEMA_PATH}", file=sys.stderr)
        sys.exit(1)

    content = SCHEMA_PATH.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Identify the structure:
    # 1. Header: everything before the first RdfTriple (Schema wrapper, RdfGraph, MARKDOWN block)
    # 2. Body: RdfTriple elements and annotations
    # 3. Footer: closing tags (</RdfGraph>, </Schema>)

    # Find the boundaries
    # The MARKDOWN block annotation is lines 12-28 (0-indexed: 11-27)
    # After that, triples and annotations begin

    # Strategy: Parse the file line by line, identifying:
    # - Header region (up to and including the MARKDOWN block and its trailing blank line)
    # - Triple region (all RdfTriple elements and annotations between them)
    # - Footer region (closing tags)

    # Find where the MARKDOWN block ends
    markdown_end = None
    in_block_annotation = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "[" or (stripped.startswith("[") and not stripped.endswith("]")):
            # Start of block annotation
            in_block_annotation = True
        if in_block_annotation and stripped == "]":
            markdown_end = i
            in_block_annotation = False
            break

    if markdown_end is None:
        print("Error: Could not find end of MARKDOWN block annotation", file=sys.stderr)
        sys.exit(1)

    # Header = everything up to and including the blank line after MARKDOWN block
    # The MARKDOWN block ends at markdown_end, followed by a blank line
    header_end = markdown_end + 1
    # Skip trailing blank line after MARKDOWN block
    if header_end < len(lines) and lines[header_end].strip() == "":
        header_end += 1

    header_lines = lines[:header_end]

    # Scan backward from end to find where triples/annotations stop and
    # footer begins (closing tags, trailing blank lines, trailing END annotations)
    footer_start = len(lines)
    for i in range(len(lines) - 1, -1, -1):
        stripped = lines[i].strip()
        if stripped == "":
            footer_start = i
            continue
        if stripped in ("</RdfGraph>", "</Schema>"):
            footer_start = i
            continue
        if is_group_annotation(lines[i]):
            footer_start = i
            continue
        # This is content (a triple line or annotation) - stop
        break

    # Body: everything between header and footer
    body_lines = lines[header_end:footer_start]

    # Now parse the body into triple blocks and annotations
    # A triple block is either:
    # - A single line starting with <RdfTriple
    # - A multiline block: <RdfTriple\n  trait=...\n  .../>
    # Annotations: lines starting with [ (after indent)
    # Blank lines: separators

    triples = []  # List of (traits_dict, original_lines, attached_annotations)
    current_attached_annotations = []
    i = 0
    body = body_lines

    while i < len(body):
        line = body[i]
        stripped = line.strip()

        if stripped == "":
            # Blank line - skip
            i += 1
            continue

        if is_group_annotation(line):
            # GROUP/END annotation - skip (will be removed)
            i += 1
            continue

        if is_single_line_annotation(line):
            # Attached annotation - collect it
            current_attached_annotations.append(line)
            i += 1
            continue

        if stripped.startswith("<RdfTriple"):
            # Start of a triple
            if stripped.endswith("/>"):
                # Single-line triple
                triple_lines = [line]
                i += 1
            else:
                # Multiline triple - collect until />
                triple_lines = [line]
                i += 1
                while i < len(body):
                    triple_lines.append(body[i])
                    if body[i].strip() in ("/>", ">"):
                        i += 1
                        break
                    i += 1

            traits = parse_triple_block(triple_lines)
            if traits is not None:
                triples.append((traits, triple_lines, current_attached_annotations))
                current_attached_annotations = []
            else:
                print(f"Warning: Could not parse triple at body line {i}: {triple_lines[0][:80]}", file=sys.stderr)
                i += 1
            continue

        # Unknown line - warn
        print(f"Warning: Unexpected line in body at position {i}: {stripped[:80]}", file=sys.stderr)
        i += 1

    total_triples = len(triples)

    # Remove duplicates
    seen = set()
    unique_triples = []
    duplicates_removed = 0
    for traits, original_lines, annotations in triples:
        key = identity_key_for_triple(traits)
        if key in seen:
            duplicates_removed += 1
            continue
        seen.add(key)
        unique_triples.append((traits, original_lines, annotations))

    # Sort by §9.6.2 key
    sorted_triples = sorted(unique_triples, key=lambda t: sort_key_for_triple(t[0]))

    # Detect how many triples moved
    triples_reordered = 0
    out_of_order_examples = []
    original_order_keys = [sort_key_for_triple(t[0]) for t in unique_triples]
    sorted_order_keys = [sort_key_for_triple(t[0]) for t in sorted_triples]

    for idx, (orig, sorted_k) in enumerate(zip(original_order_keys, sorted_order_keys)):
        if orig != sorted_k:
            triples_reordered += 1

    # Find first few out-of-order pairs in original
    for idx in range(len(original_order_keys) - 1):
        if original_order_keys[idx] > original_order_keys[idx + 1]:
            out_of_order_examples.append((idx, original_order_keys[idx], original_order_keys[idx + 1]))
            if len(out_of_order_examples) >= 5:
                break

    # Build output
    output_lines = list(header_lines)

    for idx, (traits, original_lines, annotations) in enumerate(sorted_triples):
        # Add blank line before each triple (separator between siblings)
        # But not before the first one (the header already ends with blank line)
        if idx > 0:
            output_lines.append("")

        # Attached annotations
        for ann in annotations:
            output_lines.append(ann)

        # Format the triple in canonical form
        formatted = format_triple(traits)
        output_lines.append(formatted)

    # Add blank line before footer if footer starts with non-blank
    output_lines.append("")

    # Footer: we need to reconstruct it without GROUP/END annotations
    # The footer should just be: \t</RdfGraph>\n</Schema>\n
    output_lines.append("\t</RdfGraph>")
    output_lines.append("</Schema>")
    output_lines.append("")  # Trailing newline

    result = "\n".join(output_lines)

    # Print statistics
    print(f"Schema file: {SCHEMA_PATH}")
    print(f"Total triples parsed: {total_triples}")
    print(f"Unique triples: {total_triples - duplicates_removed}")
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Triples in different position after sort: {triples_reordered}")
    print()

    if out_of_order_examples:
        print("First out-of-order pairs found (original order):")
        for idx, key_a, key_b in out_of_order_examples[:5]:
            subj_a = key_a[0] if key_a else "?"
            subj_b = key_b[0] if key_b else "?"
            # Shorten for display
            def shorten(s, n=60):
                return s if len(s) <= n else s[:n-3] + "..."
            print(f"  [{idx}] {shorten(subj_a)} | {shorten(key_a[1] if len(key_a) > 1 else '?')}")
            print(f"  [{idx+1}] {shorten(subj_b)} | {shorten(key_b[1] if len(key_b) > 1 else '?')}")
            print()
    else:
        print("Triples are already in sorted order.")
        print()

    if apply_mode:
        SCHEMA_PATH.write_text(result, encoding="utf-8")
        print(f"Written to {SCHEMA_PATH}")
    else:
        print("Dry run. Use --apply to write changes.")

        # Show a sample of the output (first few triples)
        result_lines = result.split("\n")
        # Find first triple in output
        triple_start = None
        for i, line in enumerate(result_lines):
            if "<RdfTriple" in line:
                triple_start = i
                break
        if triple_start is not None:
            sample_end = min(triple_start + 30, len(result_lines))
            print()
            print(f"Sample output (lines {triple_start + 1}-{sample_end}):")
            for line in result_lines[triple_start:sample_end]:
                print(f"  {line}")


if __name__ == "__main__":
    main()
