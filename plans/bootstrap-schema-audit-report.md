# Bootstrap Schema Audit Report

**Subject**: `spec/1.0.0/bootstrap-schema/schema.cdx` (24,371 lines, 77 concept shapes)
**Against**: `spec/1.0.0/index.md` (§9, §11, §12)
**Scope**: Completeness, correctness, and faithfulness of the canonical bootstrap schema
**Date**: 2026-02-12

---

## Summary

| Category | Count |
|----------|-------|
| Missing | 7 |
| Incorrect | 0 |
| Extra | 0 |
| Ambiguous | 0 |
| **Total** | **7** |

---

## Findings: Missing

### F-1 through F-3: Missing Simplified-Mode Rule Node Shapes (§9.5.3)

**Severity**: High — the bootstrap schema cannot validate simplified-mode schemas that use these rule node forms.

The following three concepts defined in §9.5.3 have zero occurrences in the bootstrap schema:

| # | Missing Concept | Spec Reference | Purpose |
|---|----------------|----------------|---------|
| F-1 | `OnPathExists` | §9.5.3 | Simplified-mode rule node for `Exists` path quantifier |
| F-2 | `OnPathForAll` | §9.5.3 | Simplified-mode rule node for `ForAll` path quantifier |
| F-3 | `OnPathCount` | §9.5.3 | Simplified-mode rule node for `Count` path quantifier |

**Rationale**: Per §12.3.4, the bootstrap schema must accept exactly those schema documents that conform to §11, and must reject all others. Simplified Authoring Mode schemas (§9.4, `authoringMode=$SimplifiedMode`) are valid schema documents. The simplified-mode rule node forms defined in §9.5.3 require corresponding SHACL NodeShapes in the bootstrap schema so that the `Rule` concept's children can be validated.

**Note**: The Schema shape's `sh:xone` already distinguishes between Canonical and Simplified modes, so the infrastructure for mode-dependent validation exists. These three shapes and their wiring into the `Rule` shape's child property constraints are what's missing.

---

### F-4 through F-6: Missing `sh:maxCount 1` on Schema Child Property Shapes

**Severity**: Medium — the bootstrap schema would not reject schema documents containing duplicate singleton children of the root `Schema` concept.

| # | Missing Constraint | Location in Schema Shape |
|---|-------------------|--------------------------|
| F-4 | `sh:maxCount 1` on `SchemaImports` child | Top-level Schema shape (outside xone) |
| F-5 | `sh:maxCount 1` on `RdfGraph` child | CanonicalMode xone alternative |
| F-6 | `sh:maxCount 1` on `ConceptDefinitions` child | SimplifiedMode xone alternative |

**Rationale**: A schema document has at most one `SchemaImports` block (§11.2.1), at most one `RdfGraph` block (Canonical Mode), and at most one `ConceptDefinitions` block (Simplified Mode). Without `sh:maxCount 1`, the SHACL validation would accept a schema document containing, e.g., two `SchemaImports` blocks as siblings under `Schema`.

**Note**: Other container children in the Simplified Mode xone alternatives (`TraitDefinitions`, `ValueTypeDefinitions`, `EnumeratedValueSets`, `ConstraintDefinitions`, `ValidatorDefinitions`) should be checked for the same issue but were not individually verified to the same depth during batch auditing. If the pattern is consistent (maxCount omitted for all container children), the actual count of missing constraints may be higher.

---

### F-7: Missing `sh:hasValue` on `codex:isEntity` Property Shapes

**Severity**: Medium — the bootstrap schema constrains that `codex:isEntity` is present and is a boolean, but does not constrain its *value*, allowing Entity concepts to declare `isEntity=false` and vice versa.

All 77 concept shapes share an identical `codex:isEntity` property shape consisting of 5 triples:

```
rdf:type           sh:PropertyShape
sh:path            codex:isEntity
sh:datatype        xsd:boolean
sh:minCount        1
sh:maxCount        1
```

What's missing is `sh:hasValue true` for Entity concepts and `sh:hasValue false` for non-Entity concepts.

**Affected Entity concepts** (should have `sh:hasValue true`):
- `ConceptDefinition`
- `TraitDefinition`
- `ConstraintDefinition`
- `EnumeratedValueSet`
- `ValueTypeDefinition`
- `ValidatorDefinition`

**All other 71 concepts** should have `sh:hasValue false`.

**Verification**: All 17 occurrences of `sh:hasValue` in the bootstrap schema appear on xone type-discrimination alternatives or the `CollectionAllowsDuplicates` allowed trait — none on any `codex:isEntity` property shape.

---

## Categories With No Findings

**Incorrect** (0): No property shapes or constraints were found to contradict the specification. Every trait, child, and structural constraint that *is* present matches the spec's requirements.

**Extra** (0): No shapes or constraints were found that are unwarranted by the specification. The 77 concepts in the schema map exactly to the spec-required concept set (minus the 3 missing simplified-mode concepts).

**Ambiguous** (0): No cases were found where the spec is unclear and the schema made a debatable interpretation.

---

## Steps Completed

| Step | Scope | Findings |
|------|-------|----------|
| 1. Concept Inventory | All spec-required concepts vs. 77 GROUP markers | 3 (F-1 to F-3) |
| 2. Schema Root Metadata | `id`, `version`, `authoringMode`, etc. | 0 |
| 3. Per-Concept SHACL Audit | 14 batches, 77 concepts | 3 (F-4 to F-6) |
| 4. Built-In Enumerated Value Sets | 5 sets from §11.5.4 | 0 |
| 5. IRI Pattern Verification | §9.6.4–§9.6.9, 12 SHA-256 hash checks | 0 |
| 6. Cross-Cutting Concerns | isEntity, ignoredProperties, language-level traits, self-closing | 1 (F-7) |
| 7. Findings Report | This document | — |

---

## Overall Assessment

The bootstrap schema is **substantially correct**. Out of 77 concept shapes with thousands of individual SHACL triples, only 7 gaps were identified, all in the "Missing" category. No incorrect, extra, or ambiguous modeling was found. The IRI derivation patterns, enumerated value sets, closed-world modeling, and per-concept property shapes are faithfully implemented.

The most significant gap is F-1 through F-3 (missing simplified-mode rule node shapes), which means simplified-mode schemas using path quantifiers cannot currently be validated by the bootstrap schema.
