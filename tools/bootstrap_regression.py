#!/usr/bin/env python3
"""Bootstrap schema regression harness.

Verifies structural invariants of the bootstrap schema
(spec/1.0.0/bootstrap-schema/schema.cdx) against specification
requirements. Prevents regressions in fixes applied to the schema.

Zero external dependencies — uses only text-based pattern matching on
canonical-mode RDF triples.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "spec" / "1.0.0" / "bootstrap-schema" / "schema.cdx"

BASE_IRI = "urn:codex:bootstrap:1.0.0"
SH = "http://www.w3.org/ns/shacl#"
RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
XSD = "http://www.w3.org/2001/XMLSchema#"

# Regex to extract self-closing <RdfTriple ... /> blocks.
# Captures the entire trait body between < and />.
_TRIPLE_RE = re.compile(
    r"<RdfTriple\s*\n((?:\t+\w+=.*\n)+)\t*/>",
    re.MULTILINE,
)

# Regex to extract a single trait assignment from the body.
_TRAIT_RE = re.compile(r"^\t+(\w+)=(.+)$", re.MULTILINE)


class Triple:
    """A parsed RDF triple from the bootstrap schema."""

    __slots__ = ("subject", "predicate", "object", "datatype", "lexical")

    def __init__(
        self,
        subject: str = "",
        predicate: str = "",
        object: str = "",
        datatype: str = "",
        lexical: str = "",
    ):
        self.subject = subject
        self.predicate = predicate
        self.object = object
        self.datatype = datatype
        self.lexical = lexical

    def __repr__(self) -> str:
        parts = [f"subject={self.subject}", f"predicate={self.predicate}"]
        if self.object:
            parts.append(f"object={self.object}")
        if self.lexical:
            parts.append(f"lexical={self.lexical}")
        return f"Triple({', '.join(parts)})"


def parse_triples(text: str) -> list[Triple]:
    """Extract all RdfTriple blocks from the schema text."""
    triples: list[Triple] = []
    for m in _TRIPLE_RE.finditer(text):
        body = m.group(1)
        attrs: dict[str, str] = {}
        for tm in _TRAIT_RE.finditer(body):
            name = tm.group(1)
            value = tm.group(2)
            # Strip surrounding quotes and unescape Codex text escapes.
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
            attrs[name] = value
        triples.append(Triple(**attrs))
    return triples


def find_property_nodes(
    triples: list[Triple], shape_node: str
) -> list[str]:
    """Return all property node IRIs linked from a shape via sh:property."""
    return [
        t.object
        for t in triples
        if t.subject == shape_node and t.predicate == f"{SH}property"
    ]


def find_path_for_property(triples: list[Triple], prop_node: str) -> str | None:
    """Return the sh:path object for a property node, or None."""
    for t in triples:
        if t.subject == prop_node and t.predicate == f"{SH}path":
            return t.object
    return None


def find_has_value_lexical(triples: list[Triple], prop_node: str) -> str | None:
    """Return the lexical value of sh:hasValue on a property node, or None."""
    for t in triples:
        if t.subject == prop_node and t.predicate == f"{SH}hasValue":
            return t.lexical
    return None


def find_min_count(triples: list[Triple], node: str) -> int | None:
    """Return the sh:minCount integer for a node, or None."""
    for t in triples:
        if t.subject == node and t.predicate == f"{SH}minCount":
            try:
                return int(t.lexical)
            except (ValueError, TypeError):
                return None
    return None


def find_pattern(triples: list[Triple], prop_node: str) -> str | None:
    """Return the sh:pattern lexical value for a property node, or None."""
    for t in triples:
        if t.subject == prop_node and t.predicate == f"{SH}pattern":
            return t.lexical
    return None


def find_max_count(triples: list[Triple], node: str) -> int | None:
    """Return the sh:maxCount integer for a node, or None."""
    for t in triples:
        if t.subject == node and t.predicate == f"{SH}maxCount":
            try:
                return int(t.lexical)
            except (ValueError, TypeError):
                return None
    return None


def find_class(triples: list[Triple], prop_node: str) -> str | None:
    """Return the sh:class object for a property node, or None."""
    for t in triples:
        if t.subject == prop_node and t.predicate == f"{SH}class":
            return t.object
    return None


def walk_rdf_list(triples: list[Triple], list_head: str) -> list[str]:
    """Walk an RDF list from a head node, returning rdf:first items in order."""
    items: list[str] = []
    current = list_head
    nil = f"{RDF}nil"
    while current and current != nil:
        first = None
        rest = None
        for t in triples:
            if t.subject == current:
                if t.predicate == f"{RDF}first":
                    first = t.object if t.object else t.lexical
                elif t.predicate == f"{RDF}rest":
                    rest = t.object
        if first:
            items.append(first)
        current = rest
    return items


def find_xone_alternatives(
    triples: list[Triple], shape_node: str
) -> list[str]:
    """Return the list of xone alternative node IRIs for a shape."""
    for t in triples:
        if t.subject == shape_node and t.predicate == f"{SH}xone":
            return walk_rdf_list(triples, t.object)
    return []


def build_child_concept_map(
    triples: list[Triple], shape_node: str
) -> dict[str, str]:
    """Build a mapping from child path IRI to concept name for a shape.

    Looks at all sh:property nodes on the shape that have sh:class,
    and maps their sh:path to the local name from the sh:class IRI.
    """
    result: dict[str, str] = {}
    for prop_node in find_property_nodes(triples, shape_node):
        path = find_path_for_property(triples, prop_node)
        cls = find_class(triples, prop_node)
        if path and cls:
            # Extract local name (after last # or /)
            local = cls.rsplit("#", 1)[-1] if "#" in cls else cls.rsplit("/", 1)[-1]
            result[path] = local
    return result


def find_select_queries(triples: list[Triple], shape_prefix: str) -> list[str]:
    """Return all sh:select lexical values for constraint nodes under a shape prefix."""
    return [
        t.lexical
        for t in triples
        if t.subject.startswith(shape_prefix)
        and t.predicate == f"{SH}select"
        and t.lexical
    ]


def find_shape_property_for_path(
    triples: list[Triple], shape_node: str, path_iri: str
) -> str | None:
    """Find a property node on any shape whose sh:path equals path_iri."""
    prop_nodes = find_property_nodes(triples, shape_node)
    for pn in prop_nodes:
        p = find_path_for_property(triples, pn)
        if p == path_iri:
            return pn
    return None


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

_failures: list[str] = []
_passes: list[str] = []
_warnings: list[str] = []


def _assert(condition: bool, test_name: str, detail: str) -> None:
    if condition:
        _passes.append(test_name)
    else:
        _failures.append(f"FAIL: {test_name}: {detail}")


def _warn(condition: bool, test_name: str, detail: str) -> None:
    """Record a warning for a known gap (not a regression)."""
    if condition:
        _passes.append(test_name)
    else:
        _warnings.append(f"WARN: {test_name}: {detail}")


def _find_schema_property_for_path(
    triples: list[Triple], path_iri: str
) -> str | None:
    """Find the property node on Schema#shape whose sh:path equals path_iri."""
    return find_shape_property_for_path(
        triples, f"{BASE_IRI}#Schema#shape", path_iri
    )


def test_entity_marker_consistency(triples: list[Triple]) -> None:
    """P0 regression: Schema isEntity=true and declaredId required.

    The specification requires (§6.2.1, §9.7.3, §11.2) that the
    Schema root shape marks itself as an Entity (codex:isEntity=true)
    and requires a declared id (codex:declaredId minCount=1). These
    two must be consistent: entity=true ↔ id required.
    """
    is_entity_iri = f"{BASE_IRI}#codex/isEntity"
    declared_id_iri = f"{BASE_IRI}#codex/declaredId"

    # --- isEntity property ---
    ie_prop = _find_schema_property_for_path(triples, is_entity_iri)
    _assert(
        ie_prop is not None,
        "Schema shape has isEntity property",
        f"No property with sh:path={is_entity_iri} found on Schema#shape",
    )
    if ie_prop is None:
        return

    ie_value = find_has_value_lexical(triples, ie_prop)
    _assert(
        ie_value == "true",
        "Schema isEntity hasValue is true",
        f"Expected sh:hasValue lexical='true', got '{ie_value}'",
    )

    ie_min = find_min_count(triples, ie_prop)
    _assert(
        ie_min == 1,
        "Schema isEntity minCount is 1",
        f"Expected sh:minCount=1, got {ie_min}",
    )

    # --- declaredId property ---
    di_prop = _find_schema_property_for_path(triples, declared_id_iri)
    _assert(
        di_prop is not None,
        "Schema shape has declaredId property",
        f"No property with sh:path={declared_id_iri} found on Schema#shape",
    )
    if di_prop is None:
        return

    di_min = find_min_count(triples, di_prop)
    _assert(
        di_min == 1,
        "Schema declaredId minCount is 1",
        f"Expected sh:minCount=1, got {di_min}",
    )

    # --- consistency ---
    _assert(
        ie_value == "true" and di_min == 1,
        "Entity marker consistency (isEntity=true ↔ declaredId required)",
        "isEntity and declaredId requirements are inconsistent",
    )


def test_builtin_enum_set_prohibition(triples: list[Triple]) -> None:
    """P1-b regression: built-in enum set names cannot be redefined.

    §11.5.4 requires that the five built-in enumerated value set names
    (ConceptKind, EntityEligibility, CompatibilityClass, Ordering,
    Cardinality) must not be redefined. The bootstrap schema enforces
    this via a SPARQL constraint on EnumeratedValueSet.
    """
    reserved_names = {
        "ConceptKind",
        "EntityEligibility",
        "CompatibilityClass",
        "Ordering",
        "Cardinality",
    }

    shape_prefix = f"{BASE_IRI}#EnumeratedValueSet#shape/"
    queries = find_select_queries(triples, shape_prefix)

    # Find the query that references the reserved names.
    prohibition_query = None
    for q in queries:
        if all(name in q for name in reserved_names):
            prohibition_query = q
            break

    _assert(
        prohibition_query is not None,
        "EnumeratedValueSet has SPARQL constraint for reserved names",
        "No SPARQL query found referencing all five built-in enum set names",
    )
    if prohibition_query is None:
        return

    # Verify each reserved name appears in the FILTER clause.
    for name in sorted(reserved_names):
        _assert(
            f'"{name}"' in prohibition_query,
            f"Reserved name '{name}' in enum prohibition query",
            f'Expected \\"{name}\\" in SPARQL query',
        )


def test_namespace_camelcase_pattern(triples: list[Triple]) -> None:
    """P1-a regression: Schema.namespace has camelCase pattern constraint.

    §11.2 requires the namespace trait value to follow camelCase form.
    The bootstrap schema enforces this via sh:pattern on the Schema
    shape's namespace property.
    """
    namespace_iri = f"{BASE_IRI}#namespace"

    # --- Schema.namespace ---
    schema_prop = _find_schema_property_for_path(triples, namespace_iri)
    _assert(
        schema_prop is not None,
        "Schema shape has namespace property",
        f"No property with sh:path={namespace_iri} found on Schema#shape",
    )
    if schema_prop is None:
        return

    pattern = find_pattern(triples, schema_prop)
    _assert(
        pattern is not None,
        "Schema.namespace has sh:pattern",
        "No sh:pattern found on Schema namespace property",
    )
    if pattern is None:
        return

    # The pattern must enforce lowercase-initial (camelCase).
    _assert(
        pattern.startswith("^") and "[a-z]" in pattern,
        "Schema.namespace pattern enforces lowercase-initial",
        f"Pattern '{pattern}' does not appear to enforce camelCase",
    )

    # --- SchemaImport.namespace ---
    si_shape = f"{BASE_IRI}#SchemaImport#shape"
    si_prop = find_shape_property_for_path(triples, si_shape, namespace_iri)
    _assert(
        si_prop is not None,
        "SchemaImport shape has namespace property",
        f"No property with sh:path={namespace_iri} found on SchemaImport#shape",
    )
    if si_prop is not None:
        si_pattern = find_pattern(triples, si_prop)
        _warn(
            si_pattern is not None,
            "SchemaImport.namespace has sh:pattern",
            "No sh:pattern found on SchemaImport namespace property "
            "(known gap: camelCase not yet enforced on SchemaImport.namespace)",
        )


def test_mode_conditional_children(triples: list[Triple]) -> None:
    """Mode-conditional children: SimplifiedMode XOR CanonicalMode.

    §9.4 requires exactly one authoring mode per schema. The bootstrap
    schema enforces this via sh:xone on Schema#shape with two
    alternatives — one for $SimplifiedMode, one for $CanonicalMode.
    Each alternative requires its mode-specific children and forbids
    the other mode's children.
    """
    schema_shape = f"{BASE_IRI}#Schema#shape"
    authoring_mode_iri = f"{BASE_IRI}#authoringMode"

    # --- xone structure ---
    alternatives = find_xone_alternatives(triples, schema_shape)
    _assert(
        len(alternatives) == 2,
        "Schema shape has sh:xone with exactly 2 alternatives",
        f"Expected 2 xone alternatives, got {len(alternatives)}",
    )
    if len(alternatives) != 2:
        return

    # --- identify which alternative is which mode ---
    mode_map: dict[str, str] = {}  # mode_value → alternative node IRI
    for alt in alternatives:
        props = find_property_nodes(triples, alt)
        for pn in props:
            path = find_path_for_property(triples, pn)
            if path == authoring_mode_iri:
                mode_val = find_has_value_lexical(triples, pn)
                if mode_val:
                    mode_map[mode_val] = alt

    _assert(
        "$SimplifiedMode" in mode_map,
        "One xone alternative has authoringMode=$SimplifiedMode",
        "No xone alternative with sh:hasValue=$SimplifiedMode found",
    )
    _assert(
        "$CanonicalMode" in mode_map,
        "One xone alternative has authoringMode=$CanonicalMode",
        "No xone alternative with sh:hasValue=$CanonicalMode found",
    )
    if "$SimplifiedMode" not in mode_map or "$CanonicalMode" not in mode_map:
        return

    # --- build child path → concept name map ---
    child_map = build_child_concept_map(triples, schema_shape)

    def _find_child_constraint(
        alt_node: str, concept_name: str
    ) -> tuple[str | None, int | None, int | None]:
        """Find the property on an xone alternative that targets a child concept.

        Returns (property_node, minCount, maxCount) or (None, None, None).
        """
        for pn in find_property_nodes(triples, alt_node):
            path = find_path_for_property(triples, pn)
            if path and child_map.get(path) == concept_name:
                return pn, find_min_count(triples, pn), find_max_count(triples, pn)
        return None, None, None

    # --- SimplifiedMode: requires ConceptDefinitions, forbids RdfGraph ---
    simplified = mode_map["$SimplifiedMode"]

    _, cd_min, _ = _find_child_constraint(simplified, "ConceptDefinitions")
    _assert(
        cd_min is not None and cd_min >= 1,
        "SimplifiedMode requires ConceptDefinitions (minCount>=1)",
        f"Expected minCount>=1 for ConceptDefinitions in SimplifiedMode, got {cd_min}",
    )

    _, _, rg_max = _find_child_constraint(simplified, "RdfGraph")
    _assert(
        rg_max == 0,
        "SimplifiedMode forbids RdfGraph (maxCount=0)",
        f"Expected maxCount=0 for RdfGraph in SimplifiedMode, got {rg_max}",
    )

    # --- CanonicalMode: requires RdfGraph, forbids ConceptDefinitions ---
    canonical = mode_map["$CanonicalMode"]

    _, rg_min, _ = _find_child_constraint(canonical, "RdfGraph")
    _assert(
        rg_min is not None and rg_min >= 1,
        "CanonicalMode requires RdfGraph (minCount>=1)",
        f"Expected minCount>=1 for RdfGraph in CanonicalMode, got {rg_min}",
    )

    _, _, cd_max = _find_child_constraint(canonical, "ConceptDefinitions")
    _assert(
        cd_max == 0,
        "CanonicalMode forbids ConceptDefinitions (maxCount=0)",
        f"Expected maxCount=0 for ConceptDefinitions in CanonicalMode, got {cd_max}",
    )

    # --- CanonicalMode also forbids simplified-only children ---
    simplified_only = [
        "TraitDefinitions",
        "EnumeratedValueSets",
        "ConstraintDefinitions",
        "ValidatorDefinitions",
        "ValueTypeDefinitions",
    ]
    for concept in simplified_only:
        _, _, c_max = _find_child_constraint(canonical, concept)
        _assert(
            c_max == 0,
            f"CanonicalMode forbids {concept} (maxCount=0)",
            f"Expected maxCount=0 for {concept} in CanonicalMode, got {c_max}",
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: bootstrap_regression.py", file=sys.stderr)
        return 2

    if not SCHEMA_PATH.exists():
        print(f"bootstrap_regression: schema not found: {SCHEMA_PATH}", file=sys.stderr)
        return 1

    text = SCHEMA_PATH.read_text(encoding="utf-8")
    triples = parse_triples(text)

    if not triples:
        print("bootstrap_regression: no triples parsed from schema", file=sys.stderr)
        return 1

    test_entity_marker_consistency(triples)
    test_builtin_enum_set_prohibition(triples)
    test_namespace_camelcase_pattern(triples)
    test_mode_conditional_children(triples)

    for p in _passes:
        print(f"  PASS: {p}")
    for w in _warnings:
        print(f"  {w}")

    if _failures:
        for f in _failures:
            print(f"  {f}")
        print(f"\nbootstrap_regression: {len(_failures)} failure(s), {len(_passes)} pass(es)")
        return 1

    suffix = ""
    if _warnings:
        suffix = f", {len(_warnings)} warning(s)"
    print(f"\nok: bootstrap_regression passed ({len(_passes)} tests{suffix})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
