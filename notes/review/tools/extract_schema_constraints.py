#!/usr/bin/env python3
"""Extract structured constraints from bootstrap schema.cdx RDF triples."""
from __future__ import annotations

import csv
import pathlib
import re
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "bootstrap-schema" / "schema.cdx"
OUT_DIR = ROOT / "review"

RDF_FIRST = "http://www.w3.org/1999/02/22-rdf-syntax-ns#first"
RDF_REST = "http://www.w3.org/1999/02/22-rdf-syntax-ns#rest"
RDF_NIL = "http://www.w3.org/1999/02/22-rdf-syntax-ns#nil"
RDF_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
SH_NODE_SHAPE = "http://www.w3.org/ns/shacl#NodeShape"
SH_TARGET_CLASS = "http://www.w3.org/ns/shacl#targetClass"
SH_CLOSED = "http://www.w3.org/ns/shacl#closed"
SH_IGNORED = "http://www.w3.org/ns/shacl#ignoredProperties"
SH_PROPERTY = "http://www.w3.org/ns/shacl#property"
SH_SPARQL = "http://www.w3.org/ns/shacl#sparql"
SH_XONE = "http://www.w3.org/ns/shacl#xone"
SH_OR = "http://www.w3.org/ns/shacl#or"
SH_AND = "http://www.w3.org/ns/shacl#and"
SH_NOT = "http://www.w3.org/ns/shacl#not"
SH_PATH = "http://www.w3.org/ns/shacl#path"
SH_CLASS = "http://www.w3.org/ns/shacl#class"
SH_DATATYPE = "http://www.w3.org/ns/shacl#datatype"
SH_NODE_KIND = "http://www.w3.org/ns/shacl#nodeKind"
SH_NODE = "http://www.w3.org/ns/shacl#node"
SH_MIN_COUNT = "http://www.w3.org/ns/shacl#minCount"
SH_MAX_COUNT = "http://www.w3.org/ns/shacl#maxCount"
SH_HAS_VALUE = "http://www.w3.org/ns/shacl#hasValue"
SH_IN = "http://www.w3.org/ns/shacl#in"
SH_PATTERN = "http://www.w3.org/ns/shacl#pattern"
SH_FLAGS = "http://www.w3.org/ns/shacl#flags"
SH_MIN_LENGTH = "http://www.w3.org/ns/shacl#minLength"
SH_MAX_LENGTH = "http://www.w3.org/ns/shacl#maxLength"
SH_MIN_INCLUSIVE = "http://www.w3.org/ns/shacl#minInclusive"
SH_MAX_INCLUSIVE = "http://www.w3.org/ns/shacl#maxInclusive"
SH_MESSAGE = "http://www.w3.org/ns/shacl#message"
SH_SELECT = "http://www.w3.org/ns/shacl#select"

TRIPLE_ATTR_RE = re.compile(r"^\s*([A-Za-z]+)=(.*)$")
GROUP_RE = re.compile(r"\[GROUP: ([^\]]+)\]")


def strip_quotes(text: str | None) -> str:
    if not text:
        return ""
    t = text.strip()
    if len(t) >= 2 and t[0] == '"' and t[-1] == '"':
        return t[1:-1]
    return t


def parse_schema(path: pathlib.Path):
    triples = []
    group_ranges = []
    current_group = None
    in_triple = False
    attrs = {}
    start_line = 0

    lines = path.read_text(encoding="utf-8").splitlines()
    for lineno, raw in enumerate(lines, start=1):
        m = GROUP_RE.search(raw)
        if m:
            new_group = m.group(1)
            if current_group is not None:
                # close previous group at line before new group
                gname, gstart, _ = group_ranges[-1]
                group_ranges[-1] = (gname, gstart, lineno - 1)
            current_group = new_group
            group_ranges.append((current_group, lineno, len(lines)))

        if "<RdfTriple" in raw:
            in_triple = True
            attrs = {}
            start_line = lineno
            continue

        if in_triple:
            m2 = TRIPLE_ATTR_RE.match(raw)
            if m2:
                key = m2.group(1)
                value = m2.group(2).strip()
                attrs[key] = value
                continue
            if "/>" in raw:
                triples.append(
                    {
                        "group": current_group or "",
                        "line": start_line,
                        "subject": attrs.get("subject", ""),
                        "predicate": attrs.get("predicate", ""),
                        "object": attrs.get("object", ""),
                        "datatype": attrs.get("datatype", ""),
                        "lexical": attrs.get("lexical", ""),
                    }
                )
                in_triple = False

    return triples, group_ranges


def obj_or_lex(triple: dict) -> str:
    if triple.get("object"):
        return triple["object"]
    return strip_quotes(triple.get("lexical", ""))


def list_decoder(sp_map):
    def decode_list(head: str):
        values = []
        visited = set()
        cur = head
        while cur and cur != RDF_NIL and cur not in visited:
            visited.add(cur)
            firsts = sp_map.get((cur, RDF_FIRST), [])
            rests = sp_map.get((cur, RDF_REST), [])
            if not firsts:
                break
            values.append(obj_or_lex(firsts[0]))
            cur = rests[0].get("object", "") if rests else ""
        return values

    return decode_list


def one(triples, pred):
    vals = [obj_or_lex(t) for t in triples if t["predicate"] == pred]
    return vals[0] if vals else ""


def many(triples, pred):
    return [obj_or_lex(t) for t in triples if t["predicate"] == pred]


def main():
    triples, group_ranges = parse_schema(SCHEMA_PATH)
    sp_map = defaultdict(list)
    group_to_triples = defaultdict(list)
    for t in triples:
        sp_map[(t["subject"], t["predicate"])].append(t)
        group_to_triples[t["group"]].append(t)

    decode_list = list_decoder(sp_map)

    group_summary_rows = []
    property_rows = []
    sparql_rows = []
    shape_rows = []
    logical_rows = []

    for group, start, end in group_ranges:
        gtriples = group_to_triples[group]
        shape_candidates = [
            t["subject"]
            for t in gtriples
            if t["predicate"] == RDF_TYPE and t["object"] == SH_NODE_SHAPE
        ]
        shape = ""
        for s in shape_candidates:
            if f"#{group}#shape" in s:
                shape = s
                break
        if not shape and shape_candidates:
            shape = shape_candidates[0]

        shape_triples = [t for t in gtriples if t["subject"] == shape]
        target_classes = many(shape_triples, SH_TARGET_CLASS)
        closed = one(shape_triples, SH_CLOSED)
        ignored_heads = many(shape_triples, SH_IGNORED)
        ignored_props = []
        for h in ignored_heads:
            ignored_props.extend(decode_list(h))
        property_shapes = many(shape_triples, SH_PROPERTY)
        sparql_constraints = many(shape_triples, SH_SPARQL)

        group_summary_rows.append(
            {
                "group": group,
                "start_line": start,
                "end_line": end,
                "shape": shape,
                "target_classes": " | ".join(target_classes),
                "closed": closed,
                "ignored_properties": " | ".join(ignored_props),
                "property_shape_count": len(property_shapes),
                "sparql_constraint_count": len(sparql_constraints),
            }
        )

        node_shapes = sorted(
            {
                t["subject"]
                for t in gtriples
                if t["predicate"] == RDF_TYPE and t["object"] == SH_NODE_SHAPE
            }
        )
        for node_shape in node_shapes:
            nts = [t for t in gtriples if t["subject"] == node_shape]
            node_target_classes = many(nts, SH_TARGET_CLASS)
            node_closed = one(nts, SH_CLOSED)
            node_ignored_heads = many(nts, SH_IGNORED)
            node_ignored_props = []
            for h in node_ignored_heads:
                node_ignored_props.extend(decode_list(h))
            node_property_shapes = many(nts, SH_PROPERTY)
            node_sparql_constraints = many(nts, SH_SPARQL)

            shape_rows.append(
                {
                    "group": group,
                    "node_shape": node_shape,
                    "node_role": "root" if node_shape == shape else "subshape",
                    "target_classes": " | ".join(node_target_classes),
                    "closed": node_closed,
                    "ignored_properties": " | ".join(node_ignored_props),
                    "property_shape_count": len(node_property_shapes),
                    "sparql_constraint_count": len(node_sparql_constraints),
                }
            )

            for op_name, op_pred in (
                ("xone", SH_XONE),
                ("or", SH_OR),
                ("and", SH_AND),
                ("not", SH_NOT),
            ):
                op_values = many(nts, op_pred)
                for ov in op_values:
                    if op_name in ("xone", "or", "and"):
                        members = decode_list(ov)
                    else:
                        members = [ov]
                    logical_rows.append(
                        {
                            "group": group,
                            "node_shape": node_shape,
                            "operator": op_name,
                            "object": ov,
                            "members": " | ".join(members),
                        }
                    )

            for ps in node_property_shapes:
                pts = [t for t in gtriples if t["subject"] == ps]
                in_heads = many(pts, SH_IN)
                in_values = []
                for h in in_heads:
                    in_values.extend(decode_list(h))
                kind = ""
                km = re.search(r"/property/([^/]+)/", ps)
                if km:
                    kind = km.group(1)
                property_rows.append(
                    {
                        "group": group,
                        "node_shape": node_shape,
                        "property_subject": ps,
                        "property_kind": kind,
                        "path": one(pts, SH_PATH),
                        "class": " | ".join(many(pts, SH_CLASS)),
                        "datatype": " | ".join(many(pts, SH_DATATYPE)),
                        "node": " | ".join(many(pts, SH_NODE)),
                        "node_kind": " | ".join(many(pts, SH_NODE_KIND)),
                        "min_count": one(pts, SH_MIN_COUNT),
                        "max_count": one(pts, SH_MAX_COUNT),
                        "has_value": one(pts, SH_HAS_VALUE),
                        "min_length": one(pts, SH_MIN_LENGTH),
                        "max_length": one(pts, SH_MAX_LENGTH),
                        "min_inclusive": one(pts, SH_MIN_INCLUSIVE),
                        "max_inclusive": one(pts, SH_MAX_INCLUSIVE),
                        "pattern": one(pts, SH_PATTERN),
                        "flags": one(pts, SH_FLAGS),
                        "in_values": " | ".join(in_values),
                    }
                )

            for cs in node_sparql_constraints:
                cts = [t for t in gtriples if t["subject"] == cs]
                sparql_rows.append(
                    {
                        "group": group,
                        "node_shape": node_shape,
                        "constraint_subject": cs,
                        "message": one(cts, SH_MESSAGE),
                        "select": one(cts, SH_SELECT),
                    }
                )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with (OUT_DIR / "tmp-schema-group-summary.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "group",
                "start_line",
                "end_line",
                "shape",
                "target_classes",
                "closed",
                "ignored_properties",
                "property_shape_count",
                "sparql_constraint_count",
            ],
            delimiter="\t",
        )
        w.writeheader()
        w.writerows(group_summary_rows)

    with (OUT_DIR / "tmp-schema-property-constraints.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "group",
                "node_shape",
                "property_subject",
                "property_kind",
                "path",
                "class",
                "datatype",
                "node",
                "node_kind",
                "min_count",
                "max_count",
                "has_value",
                "min_length",
                "max_length",
                "min_inclusive",
                "max_inclusive",
                "pattern",
                "flags",
                "in_values",
            ],
            delimiter="\t",
        )
        w.writeheader()
        w.writerows(property_rows)

    with (OUT_DIR / "tmp-schema-sparql-constraints.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["group", "node_shape", "constraint_subject", "message", "select"],
            delimiter="\t",
        )
        w.writeheader()
        w.writerows(sparql_rows)

    with (OUT_DIR / "tmp-schema-node-shapes.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "group",
                "node_shape",
                "node_role",
                "target_classes",
                "closed",
                "ignored_properties",
                "property_shape_count",
                "sparql_constraint_count",
            ],
            delimiter="\t",
        )
        w.writeheader()
        w.writerows(shape_rows)

    with (OUT_DIR / "tmp-schema-shape-logical.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["group", "node_shape", "operator", "object", "members"],
            delimiter="\t",
        )
        w.writeheader()
        w.writerows(logical_rows)


if __name__ == "__main__":
    main()
