# Bootstrap Schema vs Spec Mismatch Report

## Scope
- Normative source: `specifications/codex-lang.dev/spec/1.0.0/index.md`
- Informative bootstrap schema under review: `specifications/codex-lang.dev/spec/1.0.0/bootstrap-schema/schema.cdx`
- Method: requirement traceability matrix (`01-requirement-matrix.csv`, 215 rows) + structured schema extraction (`tmp-schema-*.tsv`).

## Coverage Summary
- Total reviewed requirements (schema-relevant subset): 215
- Covered: 93
- Partial (requires runtime/context semantics beyond shape graph): 122
- Missing: 0

## Current Findings

All P0 and P1 findings identified during the initial review have been resolved in `schema.cdx`. No graph-encodable requirements remain missing from the bootstrap schema.

One graph-tier requirement remains at partial coverage:

### REQ-0114 — Regex pattern evaluation straddles graph/runtime boundary
- Spec requirement: "The value MUST match a regular expression." (§11.6 `ValueMatchesPattern`)
- Schema evidence: The `ValueMatchesPattern` shape exists with correct traits (`pattern`, `flags`). The graph encodes that a pattern constraint exists and what its parameters are.
- Why partial, not covered: Evaluating a regex against actual data values is inherently a runtime operation. No static SHACL shape can execute regex matching. The constraint definition is graph-encodable; the constraint evaluation is runtime.
- Status: `coverage_status=partial` is the correct permanent state.

## Resolved Findings

The following findings were identified during the initial review and have since been corrected in `schema.cdx`.

### P0 — `Schema` entity marker contradicts required `id` (Resolved)
- Spec requirements:
  - `index.md:4163` (`Schema` MUST declare required traits including `id`)
  - `index.md:1917` (non-Entity MUST NOT have `id`)
  - `index.md:3021` (`codex:isEntity` MUST match actual entity status)
- Original schema evidence:
  - `schema.cdx:18821` set `Schema` `codex:isEntity` to `"false"` (`sh:hasValue`)
  - `schema.cdx:18790` requires `Schema` `codex:declaredId` (`sh:minCount 1`)
- Resolution: `codex:isEntity` corrected from `"false"` to `"true"` (`sh:hasValue "true"` at `schema.cdx:18841`). Affected requirements REQ-0001, REQ-0002, REQ-0026, REQ-0030 updated to `coverage_status=covered`.

### P1 — Built-in Enumerated Value Set redefinition is not blocked (Resolved)
- Spec requirement:
  - `index.md:4766` (built-in enumerated sets MUST NOT be redefined by schemas)
- Original schema evidence:
  - `schema.cdx:8657` constrains `EnumeratedValueSet.name` as string with cardinality.
  - `schema.cdx:8426` / `schema.cdx:8439` enforce uniqueness, but no reserved-name prohibition was present.
- Resolution: SHACL-SPARQL constraint added (`schema.cdx:8457-8466`) that rejects the five reserved built-in names (`ConceptKind`, `EntityEligibility`, `CompatibilityClass`, `Ordering`, `Cardinality`). REQ-0081 updated to `coverage_status=covered`.

### P1 — Namespace camelCase/normalization constraints are not encoded in `schema.cdx` (Resolved)
- Spec requirements:
  - `index.md:4190` (`Schema.namespace` MUST be camelCase; namespace uniqueness across loaded schemas)
  - `index.md:4267` (`SchemaImport.namespace` MUST be camelCase and canonically normalized)
- Original schema evidence:
  - `schema.cdx:18967`, `schema.cdx:18980` enforce `Schema.namespace` as required string.
  - `schema.cdx:19710`, `schema.cdx:19723` enforce `SchemaImport.namespace` as required string.
  - No pattern or normalization constraint was present in `schema.cdx`.
- Resolution: `sh:pattern "^(?!.*[A-Z]{3})[a-z][a-zA-Z0-9]*$"` added to both `Schema.namespace` (`schema.cdx:19012`) and `SchemaImport.namespace`. REQ-0031 and REQ-0044 updated to `coverage_status=covered`.

## Encodability Boundary Summary

Each of the 215 requirements has been classified into exactly one of three encodability tiers (column `encodability_tier` in the requirement matrix):

| Tier | Count | Meaning |
|------|-------|---------|
| `graph` | 89 | Fully encodable as SHACL shape/property/SPARQL constraints. No runtime context needed. |
| `runtime` | 99 | Requires runtime or import context: cross-document resolution, SPARQL execution semantics, content-mode detection, canonicalization behavior, error classification, process-level requirements. |
| `version` | 27 | Requires version-lineage context: semver ordering, compatibility class transitions, first-version-must-be-Initial, namespace-change-is-breaking. |

### Distribution by section

| Section | Total | graph | runtime | version |
|---------|-------|-------|---------|---------|
| §6 Identity | 2 | 2 | — | — |
| §9 Schema-First Architecture | 25 | 12 | 13 | — |
| §11 Schema Definition Language | 133 | 70 | 63 | — |
| §12 Bootstrapping | 13 | — | 13 | — |
| §13 Versioning | 42 | 5 | 10 | 27 |

### Graph-tier coverage status

Of the 89 graph-encodable requirements:

- **88 covered** — represented in `schema.cdx`
- **1 partial** — REQ-0114 (`ValueMatchesPattern` regex evaluation is inherently runtime; see Current Findings)
- **0 missing**

### Key insight

The boundary between graph-encodable and runtime/version requirements is clean: 41% of requirements are fully expressible as static SHACL constraints, 46% require runtime processing context, and 13% require version-lineage context. The bootstrap schema covers 99% of graph-encodable requirements (88/89), with the single remaining partial (REQ-0114) representing a fundamental graph/runtime boundary that cannot be closed by schema changes alone.

## Notes on Partial Coverage
- A large set of requirements in §§9.5, 11, 12.3, and 13 are process/context semantics (resolution, cross-schema context, version lineage, error-class behavior). These appear as `partial` in the matrix because they are not fully expressible as static SHACL shape constraints in `schema.cdx` alone.
