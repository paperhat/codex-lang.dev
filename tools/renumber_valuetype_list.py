#!/usr/bin/env python3
"""Renumber ValueType enum list IRIs to consecutive integers.

Reads the canonical bootstrap schema, follows the rdf:first/rdf:rest chain
for urn:codex:bootstrap:enum:ValueType#list/* IRIs, builds an old→new mapping
(consecutive integers 1–N), and does global string replacement.
"""

import re
import sys
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "spec" / "1.0.0" / "bootstrap-schema" / "schema.cdx"
PREFIX = "urn:codex:bootstrap:enum:ValueType#list/"
NIL = "http://www.w3.org/1999/02/22-rdf-syntax-ns#nil"


def main():
    text = SCHEMA_PATH.read_text()

    # Extract all rdf:rest triples for ValueType list nodes
    # Pattern: subject=PREFIX<id> ... predicate=rdf:rest ... object=PREFIX<id> or rdf:nil
    rest_triples = {}  # subject_suffix -> object_suffix_or_nil
    first_triples = {}  # subject_suffix -> value

    # Find rest links
    for m in re.finditer(
        r'object=(urn:codex:bootstrap:enum:ValueType#list/(\S+)|http://www\.w3\.org/1999/02/22-rdf-syntax-ns#nil)\s+'
        r'predicate=http://www\.w3\.org/1999/02/22-rdf-syntax-ns#rest\s+'
        r'subject=urn:codex:bootstrap:enum:ValueType#list/(\S+)',
        text
    ):
        obj_full = m.group(1)
        obj_suffix = m.group(2)  # None if rdf:nil
        subj_suffix = m.group(3)
        if obj_suffix is None:
            rest_triples[subj_suffix] = None  # terminal
        else:
            rest_triples[subj_suffix] = obj_suffix

    # Find first values (for debugging/verification)
    for m in re.finditer(
        r'lexical="([^"]+)"\s+'
        r'predicate=http://www\.w3\.org/1999/02/22-rdf-syntax-ns#first\s+'
        r'subject=urn:codex:bootstrap:enum:ValueType#list/(\S+)',
        text
    ):
        first_triples[m.group(2)] = m.group(1)

    # Find the head of the chain (a suffix that appears as a subject but never as a rest-object)
    all_subjects = set(rest_triples.keys())
    all_objects = set(v for v in rest_triples.values() if v is not None)
    heads = all_subjects - all_objects

    if len(heads) != 1:
        print(f"ERROR: Expected 1 chain head, found {len(heads)}: {heads}", file=sys.stderr)
        sys.exit(1)

    head = heads.pop()

    # Walk the chain
    chain = []
    current = head
    while current is not None:
        chain.append(current)
        if current not in rest_triples:
            print(f"ERROR: Broken chain at {current}", file=sys.stderr)
            sys.exit(1)
        current = rest_triples[current]

    print(f"Chain length: {len(chain)}")
    print(f"Chain order (old suffix -> value):")

    # Build old->new mapping
    mapping = {}
    needs_rename = False
    for i, old_suffix in enumerate(chain, 1):
        new_suffix = str(i)
        value = first_triples.get(old_suffix, "???")
        if old_suffix != new_suffix:
            needs_rename = True
        mapping[old_suffix] = new_suffix
        marker = " *" if old_suffix != new_suffix else ""
        print(f"  {old_suffix:>5s} -> {new_suffix:>3s}  ({value}){marker}")

    if not needs_rename:
        print("\nAll indices are already consecutive. Nothing to do.")
        return

    # Sort by longest suffix first to avoid partial replacements
    # e.g., replace "12a" before "12"
    sorted_old = sorted(mapping.keys(), key=lambda s: (-len(s), s))

    # Use a two-phase replacement to avoid collisions:
    # Phase 1: old -> placeholder
    # Phase 2: placeholder -> new
    placeholders = {}
    for old in sorted_old:
        placeholders[old] = f"__RENUMBER_PLACEHOLDER_{old}__"

    result = text
    for old in sorted_old:
        old_iri = PREFIX + old
        placeholder_iri = PREFIX + placeholders[old]
        result = result.replace(old_iri, placeholder_iri)

    for old in sorted_old:
        placeholder_iri = PREFIX + placeholders[old]
        new_iri = PREFIX + mapping[old]
        result = result.replace(placeholder_iri, new_iri)

    # Also handle references to the list head from sh:in etc.
    # These reference #list/1 which should remain #list/1 (the head)
    # so they're covered by the mapping already.

    SCHEMA_PATH.write_text(result)

    # Verify
    count = sum(1 for old in mapping if old != mapping[old])
    print(f"\nRenamed {count} suffixes. File written.")


if __name__ == "__main__":
    main()
