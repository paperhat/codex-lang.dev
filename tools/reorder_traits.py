#!/usr/bin/env python3
"""Reorder traits alphabetically by trait name in Codex .cdx files.

This is a one-time mechanical transformation tool. It handles:
- Multiline trait blocks (3+ traits, each on own line)
- Inline trait blocks (1-2 traits on same line as concept name)
- Quoted string values containing spaces
- Self-closing (/>) and regular (>) markers
"""

import re
import sys


def extract_trait_name(s):
    """Extract trait name from 'traitName=value' (possibly with leading whitespace)."""
    stripped = s.strip()
    return stripped[:stripped.index('=')]


def parse_inline_traits(s):
    """Parse traits from an inline string like 'trait1=val1 trait2="val with spaces"'."""
    traits = []
    i = 0
    while i < len(s):
        while i < len(s) and s[i] == ' ':
            i += 1
        if i >= len(s):
            break
        eq_idx = s.index('=', i)
        i = eq_idx + 1
        if i < len(s) and s[i] == '"':
            j = i + 1
            while j < len(s) and s[j] != '"':
                if s[j] == '\\':
                    j += 1
                j += 1
            value_end = j + 1
        else:
            j = i
            while j < len(s) and s[j] != ' ':
                j += 1
            value_end = j
        traits.append(s[s.rindex(' ', 0, eq_idx) + 1 if ' ' in s[:eq_idx] and any(
            s[k] == ' ' for k in range(i - (eq_idx - s[:eq_idx].rstrip().rfind(' ')), eq_idx)
        ) else 0 if not traits else -1:value_end])
        # Simpler approach: just track start position
        i = value_end
    # Re-do with clearer logic
    return _parse_inline_traits_v2(s)


def _parse_inline_traits_v2(s):
    """Parse traits from inline string - clear version."""
    traits = []
    i = 0
    n = len(s)
    while i < n:
        # Skip spaces
        while i < n and s[i] == ' ':
            i += 1
        if i >= n:
            break
        # Start of trait name
        start = i
        # Find =
        while i < n and s[i] != '=':
            i += 1
        if i >= n:
            break
        i += 1  # skip =
        # Parse value
        if i < n and s[i] == '"':
            # Quoted: find closing "
            i += 1
            while i < n:
                if s[i] == '\\' and i + 1 < n:
                    i += 2
                elif s[i] == '"':
                    i += 1
                    break
                else:
                    i += 1
        else:
            # Unquoted: find next space or end
            while i < n and s[i] != ' ':
                i += 1
        traits.append(s[start:i])
    return traits


def process_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    result = []
    i = 0
    changes = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()

        # Detect concept opening marker: starts with < followed by uppercase letter
        # Exclude closing markers (</) and non-concept lines
        if stripped.startswith('<') and len(stripped) > 1 and stripped[1].isupper():
            m = re.match(r'^(\s*)<([A-Z][A-Za-z0-9]*)(.*?)(\r?\n?)$', line)
            if not m:
                result.append(line)
                i += 1
                continue

            indent = m.group(1)
            concept = m.group(2)
            rest = m.group(3)
            nl = m.group(4)

            rest_stripped = rest.rstrip()

            # No traits: <Concept> or <Concept/> or <Concept />
            if rest_stripped in ('>', '/>', ' />'):
                result.append(line)
                i += 1
                continue

            # Check if line ends with > or /> (inline)
            if rest_stripped.endswith('/>'):
                closing = ' />'
                traits_str = rest_stripped[:-2].rstrip()
            elif rest_stripped.endswith('>'):
                closing = '>'
                traits_str = rest_stripped[:-1].rstrip()
            else:
                # Multiline: this line has no closing, traits follow on next lines
                result.append(line)
                i += 1
                trait_lines = []
                while i < len(lines):
                    tline = lines[i]
                    ts = tline.strip()
                    if ts == '>' or ts == '/>':
                        sorted_tl = sorted(trait_lines, key=lambda t: extract_trait_name(t))
                        if trait_lines != sorted_tl:
                            changes += 1
                        result.extend(sorted_tl)
                        result.append(tline)
                        i += 1
                        break
                    else:
                        trait_lines.append(tline)
                        i += 1
                continue

            # Inline traits
            traits_str = traits_str.lstrip()
            if not traits_str:
                result.append(line)
                i += 1
                continue

            traits = _parse_inline_traits_v2(traits_str)
            if len(traits) <= 1:
                result.append(line)
                i += 1
                continue

            sorted_traits = sorted(traits, key=lambda t: t[:t.index('=')])
            if traits != sorted_traits:
                changes += 1
                result.append(indent + '<' + concept + ' ' + ' '.join(sorted_traits) + closing + nl)
            else:
                result.append(line)
            i += 1
            continue

        result.append(line)
        i += 1

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(result)

    return changes


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.cdx> <output.cdx>")
        sys.exit(1)
    n = process_file(sys.argv[1], sys.argv[2])
    print(f"Reordered traits in {n} concept marker(s).")
