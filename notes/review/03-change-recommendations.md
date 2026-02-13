# Proposed Change Recommendations (No Source Edits Applied)

## Decision Gate
- The items below are proposals only.
- Per instruction, no changes were made to `index.md` or `schema.cdx`.
- Discuss each proposal before applying.

## Recommendation 1 (Highest Priority)
- Fix `Schema` entity/id consistency in bootstrap constraints.
- Preferred direction (spec-aligned):
  - Make `Schema` entity marker consistent with required `id` (i.e., `codex:isEntity=true` where `codex:declaredId` is required).
- Alternate direction (if intentional exception is desired):
  - Amend the spec to explicitly carve out the exception.
- Rationale:
  - Current state creates a direct contradiction across §6.2.1, §11.2, and §9.7.3.

## Recommendation 2
- Add explicit prohibition for redefining built-in enumerated value set names.
- Candidate implementation patterns:
  - SPARQL constraint on `EnumeratedValueSet.name` rejecting reserved names.
  - Equivalent deterministic rule in bootstrap validation pipeline (if intentionally outside graph constraints).
- Rationale:
  - §11.5.4 requires this; current `schema.cdx` appears to enforce only uniqueness.

## Recommendation 3
- Encode namespace lexical constraints and normalization hooks explicitly.
- Candidate implementation patterns:
  - Add deterministic pattern constraints for `Schema.namespace` and `SchemaImport.namespace` (camelCase form).
  - Keep cross-schema uniqueness/normalization as runtime checks when external import context is required; document that boundary.
- Rationale:
  - Required form constraints are normative in §11.2 and §11.2.1.

## Recommendation 4
- Add a conformance harness to prevent regressions in bootstrap/spec alignment.
- Minimum tests:
  - `Schema` with required `id` must satisfy entity marker constraints.
  - Built-in enum set names cannot be redefined.
  - Invalid namespace labels fail deterministically.
  - Mode-conditional `Schema` children (simplified vs canonical) continue to pass/fail as specified.

## Recommendation 5
- Keep explicit separation between graph-encodable constraints and runtime/context constraints.
- Add a maintained checklist mapping:
  - `encodable in schema.cdx`
  - `requires runtime/import context`
  - `requires version-lineage context`
- Rationale:
  - Matrix currently has many `partial` entries where behavior depends on processing context outside static shapes.

