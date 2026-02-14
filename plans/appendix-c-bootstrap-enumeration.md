# Plan: Appendix C — Bootstrap Schema Enumeration

## Goal

Add a normative Appendix C to the specification that exhaustively enumerates every construct the bootstrap schema-of-schemas must define. This appendix serves as a checkable inventory — §11 remains the semantic authority for what each construct means; Appendix C is the exhaustive authority for what constructs exist.

## Authority Model

- **§11**: Defines the semantics of each construct (what it means, how it behaves).
- **Appendix C**: Enumerates the complete set of constructs (what exists).
- **Neither overrides the other.** A discrepancy between §11 and Appendix C is a defect to report, not resolve. This mirrors the existing §1.3.1 pattern for prose vs. grammars.

## Prerequisite: Permission

The specification is LOCKED. The human has granted explicit permission to add Appendix C and to update §1.3.1 to reference it. No other specification sections may be modified without further permission.

## Verification Sources

Every table entry must be independently verified against ALL THREE sources:

1. **§11 prose** — the semantic definitions
2. **Canonical bootstrap schema** (`spec/1.0.0/bootstrap-schema/schema.cdx`) — the SHACL RDF representation
3. **Simplified bootstrap schema** (`spec/1.0.0/bootstrap-schema/simplified/schema.cdx`) — the human-readable representation

A table entry is correct if and only if all three sources agree. If they disagree, that is a defect to fix BEFORE the table is written.

## Sections of Appendix C

### C.1 ConceptDefinitions (~80 entries)

Table columns:
| Name | Kind | Entity | Required Traits | Allowed Traits | Required Children | Allowed Children | ExactlyOneChildOf | Spec Reference |

- **Name**: PascalCase concept name.
- **Kind**: $Semantic, $Structural, or $ValueLike.
- **Entity**: $MustBeEntity or $MustNotBeEntity.
- **Required Traits**: Traits with RequiresTrait (alphabetical, comma-separated).
- **Allowed Traits**: Traits with AllowsTrait (alphabetical, comma-separated).
- **Required Children**: RequiresChildConcept entries with min/max if specified.
- **Allowed Children**: AllowsChildConcept entries.
- **ExactlyOneChildOf**: ConceptOption lists, if any.
- **Spec Reference**: §11.x.y subsection where the concept is defined.

### C.2 TraitDefinitions (~49 entries)

Table columns:
| Name | Default Value Type | Allowed Values | Is Reference Trait | Spec Reference |

### C.3 EnumeratedValueSets (~13 entries)

Table columns:
| Name | Members (alphabetical) | Spec Reference |

### C.4 ConstraintDefinitions (~24 entries)

Table columns:
| Title | Targets | Rule Structure | Spec Reference |

### C.5 ValueTypeDefinitions (~4 entries)

Table columns:
| Name | Base Value Type | Validator | Spec Reference |

## Batches

Each batch is a self-contained unit of work. After each batch, stop and report findings before proceeding.

### Batch 1: Extract and verify ConceptDefinitions A–C (~20 concepts)

1. Read §11.3–§11.9 for all concepts starting A–C.
2. Read the canonical schema for the corresponding SHACL NodeShapes.
3. Read the simplified schema for the corresponding ConceptDefinition entries.
4. For each concept, record: name, kind, entity eligibility, required traits, allowed traits, required children, allowed children, ExactlyOneChildOf alternatives.
5. Flag any discrepancy between the three sources.
6. Produce draft table rows.

### Batch 2: Extract and verify ConceptDefinitions D–F (~15 concepts)

Same process as Batch 1.

### Batch 3: Extract and verify ConceptDefinitions G–N (~15 concepts)

Same process as Batch 1.

### Batch 4: Extract and verify ConceptDefinitions O–R (~15 concepts)

Same process as Batch 1.

### Batch 5: Extract and verify ConceptDefinitions S–Z (~15 concepts)

Same process as Batch 1.

### Batch 6: Extract and verify TraitDefinitions (~49 entries)

1. Read §11.4 for trait definitions.
2. Cross-reference with canonical and simplified schemas.
3. Produce draft table rows.
4. Flag discrepancies.

### Batch 7: Extract and verify EnumeratedValueSets (~13 entries)

1. Read §11.5.3–§11.5.4 for enumerated value sets.
2. Cross-reference with canonical and simplified schemas.
3. Produce draft table rows.
4. Flag discrepancies.

### Batch 8: Extract and verify ConstraintDefinitions (~24 entries)

1. Read §11.6–§11.9 for constraint definitions.
2. Cross-reference with canonical and simplified schemas.
3. Produce draft table rows.
4. Flag discrepancies.

### Batch 9: Extract and verify ValueTypeDefinitions (~4 entries)

1. Read §11.5.2 for value type definitions.
2. Cross-reference with canonical and simplified schemas.
3. Produce draft table rows.
4. Flag discrepancies.

### Batch 10: Assemble Appendix C

1. Combine all verified table rows into the Appendix C text.
2. Write the introductory paragraph and authority statement.
3. Final cross-check: count entries match between table and schemas.

### Batch 11: Update §1.3.1

1. Add reference to Appendix C in the consistency guarantee section.
2. Use the same defect-reporting pattern already established for prose vs. grammars.
3. Verify the new text does not alter any existing normative requirement.

### Batch 12: Final validation

1. Re-read the complete Appendix C against both schemas.
2. Verify every concept in the schemas appears in the table.
3. Verify every concept in the table appears in the schemas.
4. Verify every §11 prose construct appears in the table.
5. Count check: table row counts must match schema entity counts exactly.

## Invariants

- No batch modifies the specification until Batch 10–11.
- Batches 1–9 are pure extraction and verification — read-only against the spec.
- Any discrepancy found in Batches 1–9 is reported immediately, not silently fixed.
- The specification is only modified with explicit human approval (already granted for Appendix C and §1.3.1 update).
- No abbreviations. Every word spelled out in full.
