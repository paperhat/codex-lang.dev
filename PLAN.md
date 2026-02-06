# Specification Revision Plan

Status: **Draft — collecting issues before implementation**

This plan will be expanded as additional issues are identified. No changes will be made until the plan is complete and approved.

---

## Issue 1: Annotations Not Represented in RDF Instance Graph

**Source:** §2.6 (line 162) vs §9.7

**Problem:** §2.6 requires annotations to survive the round-trip. §9.7 defines the instance graph mapping exhaustively (line 2969: "All aspects of the instance graph mapping required by this specification are defined in this section") but emits no triples for annotations. The triple store alone cannot reconstruct a canonical document that includes annotations.

**Decision:** Annotations must be represented in the triple store. The triple store is a lossless projection of canonical form; reconstruction from triples alone must produce byte-identical canonical output.

### Changes Required

#### §9.7 — New subsection: Annotation Nodes

Add a new subsection (likely §9.7.x) defining annotation representation in the instance graph:

- Each annotation becomes an edge node (similar to ordered-children edge nodes in §9.7.6)
- Edge node carries:
  - Position index among siblings (interleaved with child concept indices)
  - Annotation text (canonical form)
  - Annotation form: inline or block
  - Annotation kind: attached, grouping, or general
  - Block directive if present (`CODE:`, `MARKDOWN:`, `FLOW:`, or none)
  - Attachment target (for attached annotations): the concept node it attaches to

#### §9.7.5 — Extended Reserved Predicates

Add reserved predicates for annotation representation. Candidates:

- `codex:annotation` — links parent node to annotation edge node
- `codex:annotationIndex` — position among siblings
- `codex:annotationText` — the annotation text content
- `codex:annotationForm` — `inline` or `block`
- `codex:annotationKind` — `attached`, `grouping`, or `general`
- `codex:annotationDirective` — `CODE`, `MARKDOWN`, `FLOW`, or absent
- `codex:annotationAttachesTo` — for attached annotations, the target concept node

Exact predicate names and IRI derivations TBD during implementation.

#### §9.7.11 — Conformance Graph

Verify that the conformance graph definition accommodates annotation triples.

#### §2.6 — Tighten Language

Clarify that the round-trip guarantee is achieved through the triple store projection alone, with no sidecar artifacts required.

---

## Issue 2: Trait Ordering — Alphabetical Canonicalization

**Source:** §8.5 (line 1949), §8.6 (line 2000), §10.5 (lines 3841, 3854)

**Problem:** The spec requires trait order to be "preserved" but the RDF instance graph (§9.7.7) emits one unordered triple per trait with no ordering metadata. Trait order cannot be reconstructed from the triple store.

**Decision:** Canonical trait order is alphabetical by trait name. This is a Phase 1 (schema-free) canonicalization step. Since trait names are unique per concept instance, alphabetical sort is total and unambiguous. No trait-ordering metadata is needed in the RDF graph — reconstruction derives order from names alone.

### Changes Required

#### §3.2 — Explicit Trait Name Uniqueness Rule

Add: "A Concept instance MUST NOT declare two or more Traits with the same Trait name." This is currently implied by the entire design but never stated as an explicit well-formedness rule. It is a prerequisite for alphabetical ordering to be unambiguous.

#### §8.5.1 and §8.6 — Change "preserved" to "alphabetized"

Lines 1949 and 2000 currently say "their order MUST be preserved." Change to require alphabetical ordering in canonical form. Raw input may use any order; canonicalization normalizes to alphabetical.

#### §10.5 — Update Canonicalization Rules

- Phase 1 list (line 3836–3841): Add "alphabetical ordering of Traits by name"
- Remove "preservation of ... Trait ... order" from the Phase 1 list (line 3841) — Concept and Content order are still preserved; Trait order is now normalized
- Line 3854: Remove "reorder Traits" from the "MUST NOT" list, or rephrase to clarify that alphabetical normalization is the one permitted reordering

#### §10.7 — Update Allowed/Forbidden Changes

Line 3887 says "Canonicalize trait layout/spacing without reordering traits." Update to reflect that alphabetical reordering is now part of canonicalization.

Line 3894 says "Reorder Concepts or Traits" under forbidden changes. Split: reordering Concepts remains forbidden; reordering Traits is now required (alphabetical).

#### Appendix A (EBNF and PEG) — Grammar Impact

The grammar for `Traits` (`Traits = WhitespaceNoNewline, Trait, { Whitespace, Trait }`) is a syntactic production that accepts any order. No grammar change needed — the grammar defines what parses, not canonical order. Canonical ordering is a semantic/canonicalization rule, not a syntactic one. Verify this is consistent.

#### Bootstrap Schemas — Reorder Traits

Both `schema.cdx` and `simplified/schema.cdx` must have their traits reordered to alphabetical within every concept instance. This makes the reference schemas canonical per the new rule.

#### §14 — Error Classification

Verify that duplicate trait names on a concept instance are classified. Likely `WellFormednessError` since it is detectable without a schema.

---

## Issue 3: §12.2 `parse()` Signature Contradicts Schema-Less Pipeline

**Source:** §12.2 (line 5450–5460) vs §2.5 (line 145), §10.2.1 (line 3758)

**Problem:** §2.5 requires well-formedness parsing without a governing schema. §10.2.1 mandates a schema-less formatting/canonicalization mode. But §12.2 shows a single `parse(documentBytes, governingSchema)` entry point and says "If no governing schema is provided, parsing MUST fail with a ParseError." The word "parsing" and the `ParseError` classification make it read as if schema-less parsing is forbidden, contradicting the schema-less pipeline established elsewhere.

**Decision:** §12.2 is about the semantic validation entry point, not the schema-less formatting entry point. Fix the vocabulary: rename to `validate()`, change the error class to `SchemaError`, and acknowledge the schema-less path.

### Changes Required

#### §12.2 — Fix Function Signature and Error Class

- Rename `parse()` to `validate()` (or similar) to distinguish from schema-less parsing.
- Change `ParseError` to `SchemaError` on the "no governing schema" failure — a missing schema is a schema-provision failure, not a syntactic parse failure.
- Add acknowledgment of the schema-less entry point (referencing §10.2.1).

---

## Issue 4: Whitespace-Only Blank Lines — Prose/Grammar Clarity

**Source:** §8.4 (lines 1918–1920) vs EBNF `BlankLine` (line 7293) and PEG `BlankLine` (line 7879)

**Problem:** §8.4 says "a line containing only whitespace" is treated as empty "after normalization." The EBNF/PEG grammars define `BlankLine = Newline` with no whitespace permitted. This is not a true contradiction — the prose describes normalization behavior (input processing) and the grammar describes canonical form (post-normalization). But the two descriptions sit at different stages without making the staging explicit, which could confuse implementors.

**Severity:** Low — clarification only, no behavioral change.

**Decision:** Add a clarifying sentence to §8.4 making the staging explicit.

### Changes Required

#### §8.4 — Clarify normalization staging

After line 1920 ("Codex-conforming tools MUST treat a line containing only whitespace as empty after normalization"), add a clarifying sentence stating that this is a normalization rule applied during canonicalization (trailing whitespace stripping per §10.5), and that in canonical form a blank line contains no characters — consistent with the `BlankLine` grammar production.

No grammar changes needed.

---

## Issue 5: π Constant Insufficient for 256-bit Precision

**Source:** §5.7.2 (lines 506, 536)

**Problem:** §5.7.2 mandates 256-bit precision arithmetic for color conversions but defines `π = 3.141592653589793` — only 16 significant digits (binary64 precision). At 256 bits, this truncated value differs from the true mathematical π starting at the 16th digit. Two implementations — one using the literal, the other computing π to 256-bit precision — will produce different correctly-rounded results for `h * (π/180)`, `sin`, and `cos` in LCH/OKLCH conversions, violating determinism.

**Decision:** Replace the decimal literal with a correctly-rounded definition, consistent with how the spec already defines `sin`, `cos`, `sqrt`, etc.

### Changes Required

#### §5.7.2 — Replace π constant definition

Change line 536 from:

```
π = 3.141592653589793
```

to a definition requiring π to be the correctly-rounded value of the mathematical constant π in precision `p = 256`, round-to-nearest ties-to-even. This follows the same pattern as lines 522–524 (correctly-rounded `sin`, `cos`, `sqrt`, etc.) and is unambiguous — any multiprecision library can compute it.

---

## Pending Issues

*Additional issues will be added here as they are raised.*

---

## Implementation Order

Once all issues are collected and the plan is approved:

1. **Spec text first** — all normative prose changes to `spec/1.0.0/index.md`
2. **Grammars second** — EBNF and PEG in Appendix A, if affected
3. **Schemas third** — both bootstrap schemas updated to match spec and made canonical
4. **Cross-check** — verify internal consistency across all artifacts
