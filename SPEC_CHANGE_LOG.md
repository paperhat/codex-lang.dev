# Spec Change Log

This file records all changes made to the Codex specification during implementation.

---

## 2026-02-03: §14.6.1 — Make `message` required

**Section:** 14.6.1 Error Payload Shape (Recommended)

**Change:** Changed `message` from `(optional)` to `(required)`.

**Rationale:** The human-readable error message is essential for reducing cognitive load. A tool that emits machine-readable `code` without a human-readable `message` is technically conforming but user-hostile. Humans come first.

---

## 2026-02-05: §5.4 + A.1.12 — Remove `+` sign from numeric values

**Sections:** §5.4 Numeric Values, A.1.12 Numeric Values grammar

**Changes:**
1. Added prose: "Explicit `+` signs are not permitted; absence of a sign indicates a positive value."
2. Changed `Integer` grammar from `[ Sign ]` to `[ "-" ]`
3. Changed `DecimalNumber` grammar from `[ Sign ]` to `[ "-" ]`

**Rationale:** Round-trippability. If `+42` were accepted and stored as `Integer(42)`, we could not preserve the exact spelling on output. The spec requires "Numeric spellings MUST be preserved exactly." Rejecting `+` is the simplest, most deterministic approach.

---

## 2026-02-05: PEG grammar — Align `Integer` and `DecimalNumber` with EBNF amendment

**Section:** PEG grammar (Appendix A.2)

**Changes:**
1. Changed `Integer` PEG from `'0' / Sign? [1-9] Digit*` to `'0' / '-'? [1-9] Digit*`
2. Changed `DecimalNumber` PEG from `Sign? IntDigits '.' Digits` to `'-'? IntDigits '.' Digits`

**Rationale:** The EBNF grammar (A.1.12) was amended on 2026-02-05 to use `[ "-" ]` instead of `[ Sign ]`, but the corresponding PEG grammar was missed. This change brings the PEG grammar into alignment.

---

## 2026-02-06: §5.17 + A.1.24 + A.2.21 — Restrict Range endpoints to ordered numeric types

**Sections:** §5.17 Range Values, A.1.24 Range Values grammar, A.2.21 Range Values PEG grammar

**Changes:**
1. Added prose to §5.17: Range endpoints and step values MUST be ordered numeric types (Integer, DecimalNumber, Fraction, ExponentialNumber, or PrecisionNumber), Temporal Values, or Character Values. ComplexNumber, ImaginaryNumber, and Infinity MUST NOT appear as range endpoints or step values.
2. Introduced `OrderedNumericValue` production in both EBNF and PEG grammars, listing the five permitted numeric types.
3. Changed `RangeStart`, `RangeEnd`, and `StepValue` to reference `OrderedNumericValue` instead of `NumericValue`.
4. Fixed incorrect example in §5.17: "both Integer, both Text" → "both Integer, both PlainDate" (Text was never a valid range endpoint).

**Rationale:** ComplexNumber and ImaginaryNumber lack a total ordering, making interval semantics undefined. Infinity as an inclusive range endpoint is contradictory. Only numeric types on the real number line with well-defined ordering are meaningful as range bounds.

---

## 2026-02-07: §12.2 — Rename `parse()` to `validate()`, fix error class

**Section:** §12.2 Semantic Validation Entry Point

**Changes:**
1. Renamed `parse()` to `validate()` to distinguish from schema-less parsing.
2. Changed `ParseError` to `SchemaError` for missing governing schema.
3. Added acknowledgment of the schema-less entry point (referencing §10.2.1).

**Rationale:** §2.5 and §10.2.1 establish a schema-less pipeline. The old `parse()` signature and `ParseError` classification made it read as if schema-less parsing were forbidden.

---

## 2026-02-07: §8.4 — Clarify whitespace-only blank line staging

**Section:** §8.4 Blank Lines

**Change:** Added clarifying sentence after the whitespace-only line rule, stating this is a canonicalization rule (trailing whitespace stripping per §10.5) and that in canonical form a blank line contains no characters — consistent with the `BlankLine` grammar production.

**Rationale:** The prose described normalization behavior while the grammar described canonical form. The two descriptions sat at different stages without making the staging explicit.

---

## 2026-02-07: §5.7.2 — Replace π decimal literal with correctly-rounded definition

**Section:** §5.7.2 Color Conversion Arithmetic

**Change:** Changed `π = 3.141592653589793` to require the correctly-rounded value of the mathematical constant π in precision `p = 256`, round-to-nearest ties-to-even.

**Rationale:** The decimal literal had only 16 significant digits (binary64 precision). At 256 bits, two implementations could produce different correctly-rounded results for trigonometric conversions, violating determinism.

---

## 2026-02-07: §8.1 — Declare UTF-8 as canonical encoding

**Section:** §8.1 Character Encoding

**Change:** Changed "UTF-8 is the default encoding" to "The canonical encoding is UTF-8 with no BOM. Canonicalization MUST normalize UTF-16 encoded input to UTF-8, removing the BOM."

**Rationale:** §10.5 Phase 1 requires "canonical encoding" but §8.1 never declared which encoding is canonical. "Default" is not "canonical." Two implementations could produce different byte-level canonical outputs.

---

## 2026-02-07: §2.1, §3.2, §8.5.1, §8.6, §10.5, §10.7, bootstrap schemas — Alphabetical trait ordering

**Sections:** §2.1 Structural Ordering, §3.2 Concept Instances, §8.5.1 Inline Traits, §8.6 Multiline Traits, §10.5 Canonicalization, §10.7 Allowed/Forbidden Changes, both bootstrap schemas

**Changes:**
1. §2.1: Split Traits from children/collection element ordering claim. Trait order is always canonical (alphabetical).
2. §3.2: Added explicit trait name uniqueness rule with `SurfaceFormError`.
3. §8.5.1 and §8.6: Changed "order MUST be preserved" to "canonical form MUST order them alphabetically by Trait name."
4. §10.5: Added "alphabetical ordering of Traits by Trait name" to Phase 1. Changed preservation to "Concept and Content order." Removed "reorder Traits" from forbidden list.
5. §10.7: Updated allowed changes to include alphabetical ordering. Removed "or Traits" from forbidden reordering.
6. Both bootstrap schemas: Mechanically reordered all traits to alphabetical order (269 + 1305 concept markers).

**Rationale:** The RDF instance graph emits one unordered triple per trait with no ordering metadata. Trait order cannot survive the round-trip. Alphabetical canonical order is deterministic, total (trait names are unique per concept), and requires no RDF metadata.

---

## 2026-02-07: §2.6, §9.7.5, §9.7.6, new §9.7.7, §9.7.8–§9.7.12 — Annotation RDF representation

**Sections:** §2.6 Round-Trippability, §9.7.5 Reserved Predicates, §9.7.6 Ordered Children Encoding, new §9.7.7 Annotation Nodes, renumbered §9.7.8–§9.7.12

**Changes:**
1. §9.7.5: Added 7 reserved predicates (`codex:annotationParent`, `annotationIndex`, `annotationText`, `annotationForm`, `annotationKind`, `annotationDirective`, `annotationTarget`) with IRI derivations.
2. §9.7.6: Extended to unified sibling index (counting both Concept instances and annotations). Extended to cover root Concept instances using `documentBaseIri` as parent. Added clarification distinguishing unified index from `ordinalIndex(C)`.
3. New §9.7.7: Annotation edge node definition — IRI formula, 5 mandatory triples, 2 conditional triples (directive, target).
4. Renumbered §9.7.7–§9.7.11 to §9.7.8–§9.7.12. Updated 2 cross-references.
5. §2.6: Added "The round-trip guarantee is achieved through the triple store projection alone, with no sidecar artifacts required."

**Rationale:** §2.6 requires annotations to survive the round-trip, but §9.7 emitted no triples for annotations. The triple store alone could not reconstruct a canonical document that includes annotations.

---

## 2026-02-07: §9.8, §9.7.5, §9.9.9, §9.9.10, §9.10, §6.3.3, §5.10, §5.9, §9.1, §7.6, §8 — Remove `Bindings`/`Bind` mechanism, enforce single-root document

**Sections:** §9.8 (complete rewrite), §9.7.5, §9.9.9, §9.9.10, §9.10, §6.3.3, §5.10, §5.9, §9.1, §7.6, §8

**Changes:**
1. §9.8: Renamed from "Lookup Token Bindings" to "Lookup Token Resolution". Removed §9.8.1 (`Bindings` concept), §9.8.2 (`Bind` concept). Replaced with resolution table built from Concepts that declare both `key` and `id` traits. Removed duplicate-binding error (redundant with §6.3.2 `IdentityError` for duplicate keys).
2. §9.7.5: Removed `codex:lookupToken` and `codex:lookupIri` reserved predicates and their IRI derivations.
3. §9.9.9: Changed "lookup binding table" to "resolution table".
4. §9.9.10: Changed "binding entry in the lookup binding table" to "entry in the resolution table".
5. §9.10: Changed "no binding is found" to "no Concept with a matching `key` is found".
6. §6.3.3: Changed binding mechanism reference to inline resolution description.
7. §5.10: Changed definition from "binds to a schema-defined value" to "document-scoped symbolic reference that identifies a Concept by its `key` trait".
8. §5.9: Changed "lookup-token binding" to "lookup-token resolution".
9. §9.1: Changed "interpret lookup token bindings" to "resolve lookup tokens".
10. §7.6: Removed `Bindings`/`Bind` blocks from examples 2 and 3; moved `key` trait onto the relevant Concepts inline.
11. §8: Added explicit single-root requirement (a Codex document must contain exactly one root Concept instance).

**Rationale:** The grammar enforces exactly one root Concept per document, but the `Bindings`/`Bind` mechanism required a separate top-level Concept. Any document needing both a `Bindings` section and a real root Concept was structurally non-conforming. The `key` trait already lives on the Concept it identifies, so the resolution table can be constructed directly from `key`+`id` declarations without a separate binding section.
