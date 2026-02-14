# Plan: Canonical Bootstrap Schema Audit

## Problem

The canonical bootstrap schema (`spec/1.0.0/bootstrap-schema/schema.cdx`) is ~26,732 lines of RDF triples in Codex surface form. Automated agent extraction in Batch 1 produced unreliable results — it confused internal SHACL infrastructure properties (`codex/isEntity`, `codex/parentNode`) with user-facing traits, misidentified child constraint structures, and reported incorrect required/allowed classifications.

The canonical schema must be byte-for-byte consistent with the simplified schema (they must expand to the same RDF graph). Any discrepancy between them is a defect.

## Approach

Since the simplified schema is now verified against the spec prose (Appendix C work, in progress), we use the simplified schema as the **reference** and audit the canonical schema against it. This is the right direction because:

1. The simplified schema uses Codex-native vocabulary (ConceptDefinition, RequiresTrait, etc.) — the same vocabulary as the spec prose
2. The canonical schema uses SHACL vocabulary (sh:NodeShape, sh:property, sh:minCount, etc.) — a different representation
3. The expansion algorithm deterministically maps simplified → canonical
4. Therefore: if simplified matches prose, and canonical matches simplified (post-expansion), all three agree

## Strategy: Section-by-Section SHACL Verification

Rather than extracting all ~80 NodeShapes in one pass (which overwhelmed the agent), we verify in small alphabetical batches. For each concept, we check:

1. **NodeShape exists** with the correct IRI (`urn:codex:bootstrap:1.0.0#ConceptName`)
2. **sh:property entries** match the simplified schema's traits:
   - RequiresTrait → sh:property with sh:minCount 1
   - AllowsTrait → sh:property without sh:minCount (or sh:minCount 0)
   - Trait name mapping: simplified `name="traitName"` → canonical `sh:path codex:traitName`
3. **Child constraints** match:
   - RequiresChildConcept → sh:property with sh:path for child, sh:minCount matching `min`
   - AllowsChildConcept → sh:property with sh:path for child, no minCount requirement
   - ExactlyOneChildOf → sh:xone with correct member list
4. **Language-level properties** are present but not user-facing:
   - `codex/isEntity`, `codex/parentNode`, `codex/content` in sh:ignoredProperties — these are infrastructure
5. **conceptKind and entityEligibility** are declared via dedicated triples (not sh:property)

## Batches

### Batch 1: Understand the canonical schema structure (prerequisite)

Before auditing individual concepts, understand the SHACL patterns used:

1. Read a small, well-understood concept (e.g., ContentPath — no traits, no children) to establish the baseline SHACL pattern
2. Read a concept with required traits (e.g., AllowsContent — one required trait)
3. Read a concept with allowed traits (e.g., AllowsChildConcept — required + allowed traits)
4. Read a concept with ExactlyOneChildOf (e.g., AllowedValues)
5. Read a concept with RequiresChildConcept (e.g., AllOf — min=2 children)
6. Document the SHACL patterns for each simplified construct

This batch produces a **pattern dictionary** that all subsequent batches use.

### Batch 2: Audit ConceptDefinitions A–C (~24 concepts)

For each concept A–C, read the canonical NodeShape and verify it matches the simplified schema using the pattern dictionary from Batch 1.

### Batch 3: Audit ConceptDefinitions D–F (~15 concepts)

Same process.

### Batch 4: Audit ConceptDefinitions G–N (~15 concepts)

Same process.

### Batch 5: Audit ConceptDefinitions O–R (~15 concepts)

Same process.

### Batch 6: Audit ConceptDefinitions S–Z (~15 concepts)

Same process.

### Batch 7: Audit TraitDefinitions (~49 entries)

Verify each TraitDefinition in the canonical schema matches the simplified schema's TraitDefinition entries.

### Batch 8: Audit EnumeratedValueSets (~13 entries)

Verify each EnumeratedValueSet and its Members.

### Batch 9: Audit ConstraintDefinitions (~24 entries)

Verify each ConstraintDefinition's Targets and Rule structure.

### Batch 10: Audit ValueTypeDefinitions (~4 entries) and root Schema

Verify ValueTypeDefinitions and the root Schema traits.

### Batch 11: Fix discrepancies

Apply all corrections found in Batches 2–10. Each fix must be verified against the spec prose.

### Batch 12: Final count validation

1. Count NodeShapes in canonical = count ConceptDefinitions in simplified
2. Count TraitDefinition entries match
3. Count EnumeratedValueSet entries match
4. Count ConstraintDefinition entries match
5. Count ValueTypeDefinition entries match

## Invariants

- The simplified schema is the reference (already verified against spec prose)
- Discrepancies are reported, not silently fixed
- Each batch stops and reports before the next begins
- The canonical schema is only modified in Batch 11, after all discrepancies are catalogued
- No abbreviations in any output
