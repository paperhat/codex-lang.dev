# Spec Change Log

This file records all changes made to the Codex specification during implementation.

---

## 2026-02-07: A.1 + A.2 — Normalize grammar rule names and add missing RecordValue to precedence list

**Sections:** A.1 EBNF (Normative), A.2 PEG (Informative), A.1.28 Value Termination and Disambiguation

**Changes:**
1. EBNF: Renamed `ColorWs` → `ColorWhitespace`, `ColorWsOpt` → `ColorWhitespaceOptional`.
2. PEG: Renamed `ColorWS` → `ColorWhitespaceOptional`, `ColorWSP` → `ColorWhitespace` (aligning semantics and names with EBNF).
3. PEG: Renamed `IntDigits` → `IntegerDigits`, `Digits` → `DigitSequence` (matching EBNF names).
4. PEG: Renamed `RgbColorSpaceToken` → `RgbColorSpace`, `XyzColorSpaceToken` → `XyzColorSpace` (matching EBNF names).
5. PEG: Removed duplicate `WS` rule (identical to `WhitespaceChar`); replaced all `WS*` usages with `WhitespaceChar*`.
6. A.1.28: Added `RecordValue (record[...])` to Value disambiguation precedence list (was present in both grammars' `Value` production but missing from the precedence comment). Renumbered subsequent entries.

**Rationale:** Grammar rule names used abbreviations (`Ws`, `WS`, `WSP`, `Int`, `Digits`) inconsistent with the rest of both grammars, which spell out words (`Whitespace`, `Integer`, `DigitSequence`). PEG rule names diverged from their EBNF counterparts without reason. The `WS` rule duplicated `WhitespaceChar` exactly. `RecordValue` was omitted from the precedence list despite appearing in both `Value` productions.

---

## 2026-02-07: §14 — Remove redundant §14.5 Error Severity section

**Section:** §14 Errors

**Change:** Removed §14.5 "Error Severity" (halt on failure, no best-effort recovery, no silent reinterpretation). Renumbered former §14.6 "Reporting Requirements" to §14.5.

**Rationale:** All three bullets in former §14.5 restated requirements already stated with proper scoping elsewhere: halt-at-first-failure (§14.3), no best-effort/heuristic processing (§2.2, §9.10, §10.14, §12.3.3), no silent reinterpretation (§10.11). The redundancy created sync risk without adding normative content.

---

## 2026-02-07: §8.5.1 — Remove duplicate trait ordering rule

**Section:** §8.5.1 Opening Marker

**Change:** Replaced the duplicate normative statement about alphabetical trait ordering with a cross-reference to §8.6, which states the same rule.

**Rationale:** §8.5.1 and §8.6 contained identical normative statements about alphabetical trait ordering. Per "each requirement stated once," the authoritative statement belongs in §8.6 (Traits). §8.5.1 now references §8.6 instead.

---

## 2026-02-07: §5.2 + A.1.10 + A.2.10 — Exclude newlines from Backtick Text grammar

**Sections:** §5.2 Backtick Text, A.1.10 Backtick Text (EBNF), A.2.10 Backtick Text (PEG)

**Changes:**
1. §5.2: Removed "and line breaks" from the whitespace normalization rule (now "spaces and tabs" only).
2. EBNF: Changed `UnescapedBacktickChar` from `AnyCharExceptBacktick` to `AnyCharExceptBacktickNewline`.
3. PEG: Changed `BacktickChar` from `(!'`' .)` to `(!'`' !'\n' .)`.
4. Character class list: Replaced `AnyCharExceptBacktick` with `AnyCharExceptBacktickNewline`.

**Rationale:** Backtick Text appears only as trait values, which are single-line by surface form rules (§8.5–8.6). The grammar's `AnyCharExceptBacktick` was the only inline value character class that did not exclude newlines, creating an ambiguity about whether newlines were permitted in source form and normalized, or rejected at parse time. Excluding newlines makes the grammar self-documenting and consistent with every other inline value character class.

---

## 2026-02-07: §9.5.2 — Change `ValidatorDefinition.name` type from Enumerated Token to Concept name

**Section:** §9.5.2 Explicit Validator Definitions

**Change:** Changed `name` trait type from "Enumerated Token Value" to "Concept name per §4 Naming Rules".

**Rationale:** Every other definition type (`ConceptDefinition`, `TraitDefinition`, `ValueTypeDefinition`, `EnumeratedValueSet`) stores names as text. The `$` sigil belongs to the reference syntax (`validatorName=$X`), not the stored name. §11.6.2 makes this explicit: "Enumerated Token Values whose name matches the `ValueTypeDefinition.name`." `ValidatorDefinition` was the sole outlier, and the mismatch made the bootstrap's `defaultValueType=$Text` for the shared `name` trait appear non-conforming.

---

## 2026-02-07: §11.5.1 — Fix `defaultValueType`/`defaultValueTypes` cross-references from §5.17 to §5.18

**Section:** §11.5.1 `TraitDefinition`

**Change:** Changed "optionally parameterized per §5.17" to "optionally parameterized per §5.18" on both the `defaultValueType` and `defaultValueTypes` trait descriptions.

**Rationale:** §5.17 defines Range Values. §5.18 defines Parameterized Value Types (e.g., `$List<$Text>`). The cross-references pointed to the wrong section.

---

## 2026-02-07: §9.9.7 — Reframe `UniqueInDocument` as built-in identity semantics

**Section:** §9.9.7 Uniqueness Constraints

**Changes:**
1. Replaced `UniqueInDocument(trait=t)` (which used schema-authorable constraint notation but had no corresponding definition in §11) with prose that frames document-wide uniqueness as enforcement of the built-in identity invariants from §6.2.2 (`id`) and §6.3.2 (`key`).
2. Changed "the following uniqueness constraints" to reference `UniqueConstraint` (§11.10.5) specifically.
3. Changed "For both constraints" to "The identity of a trait within a uniqueness constraint" (no longer two peer constraint concepts).

**Rationale:** `UniqueInDocument` was referenced only in §9.9.7 and had no definition in §11, no bootstrap presence, and no schema-author use case. The only document-wide uniqueness rules are `id` and `key`, which are core model invariants enforced by §6 before schema validation runs. Presenting `UniqueInDocument` in `ConstraintName(params)` notation implied it was a schema-authorable concept, but it was not. The rewrite clarifies that derived validation artifacts must enforce the §6 invariants without introducing an undefined constraint concept.

---

## 2026-02-07: §11.4.4 — Add `ExactlyOneChildOf` and `ConceptOption` definitions

**Section:** §11.4.4 `ChildRules`

**Changes:**
1. Added `ExactlyOneChildOf` to the list of permitted children of `ChildRules`.
2. Added definitions for `ExactlyOneChildOf` (declares that exactly one of the listed Concept types must appear as a child; contains 2+ `ConceptOption` children) and `ConceptOption` (declares one option within an `ExactlyOneChildOf` group; single required `conceptSelector` trait).

**Rationale:** Both constructs were defined in the canonical and simplified bootstrap schemas (28 occurrences of `ExactlyOneChildOf`, 60+ occurrences of `ConceptOption`) and used as the meta-schema mechanism behind the "Exactly one of:" child-rule pattern, but §11.4.4 only listed `AllowsChildConcept`, `RequiresChildConcept`, and `ForbidsChildConcept`. The bootstrap's own `ChildRules` definition lists all four constructs.

---

## 2026-02-07: Spec §11.11 — Fix `ChildConstraint.type` values from Text to Enumerated Token

**Section:** §11.11 Complete Constraint Example (Informative)

**Changes:**
1. Line 5367: Changed `type="RequiresChildConcept"` to `type=$RequiresChildConcept`
2. Line 5393: Changed `type="RequiresChildConcept"` to `type=$RequiresChildConcept`

**Rationale:** The `ChildConstraint` concept's `type` trait is constrained by an `EnumeratedConstraint` against the `ChildConstraintType` enumerated set. Per §5.5, enumerated token values use the `$` sigil. The informative examples incorrectly used quoted text values, which would fail schema validation.

---

## 2026-02-06: A.1.13 + A.2.13 — Mandatory space after comma in TypeParameters and TypeUnion

**Sections:** A.1.13 Enumerated Tokens (EBNF), A.2.13 Enumerated Tokens (PEG)

**Changes:**
1. EBNF `TypeParameters`: changed `{ ",", TypeArgument }` to `{ ",", " ", TypeArgument }`
2. EBNF `TypeUnion`: changed `{ ",", EnumeratedToken }` to `{ ",", " ", EnumeratedToken }`
3. PEG `TypeParameters`: changed `(',' TypeArgument)*` to `(',' ' ' TypeArgument)*`
4. PEG `TypeUnion`: changed `(',' EnumeratedToken)*` to `(',' ' ' EnumeratedToken)*`

**Rationale:** Readability. `$Map<$Text, $Integer>` is easier to read than `$Map<$Text,$Integer>`. Enforcing exactly one space (rather than optional) preserves the one-canonical-form invariant.

---

## 2026-02-07: Bootstrap schemas — Rename `ValueInNumericRange` traits from `rangeMin`/`rangeMax` to `min`/`max`

**Files:** `bootstrap-schema/schema.cdx`, `bootstrap-schema/simplified/schema.cdx`

**Changes:**
1. Simplified bootstrap: Changed `AllowsTrait` names from `rangeMin`/`rangeMax` to `min`/`max` on `ValueInNumericRange`. Removed redundant `rangeMin`/`rangeMax` `TraitDefinition` entries (the `min`/`max` `TraitDefinition` entries already exist). Updated `TraitExists` references and constraint messages. Updated inline usage (`<ValueInNumericRange rangeMin=1 />` to `<ValueInNumericRange min=1 />`). Widened `defaultValueType` on the shared `min`/`max` `TraitDefinition` entries from `$NonNegativeInteger`/`$PositiveInteger` to `$Number`.
2. Canonical bootstrap: Removed 6 trait definition triples for `urn:codex:bootstrap:trait:rangeMin` and `urn:codex:bootstrap:trait:rangeMax`. Changed `sh:path` references to `urn:codex:bootstrap:trait:min` and `urn:codex:bootstrap:trait:max`. Updated SPARQL query IRI references and constraint messages. Widened `rdfs:range` on the shared `min`/`max` trait definitions from `xsd:nonNegativeInteger`/`xsd:positiveInteger` to `xsd:decimal`.

**Rationale:** The spec §11.10.2 defines `ValueInNumericRange` with traits `min` and `max`, consistent with all other min/max constraints (`TraitCardinality`, `ValueLength`, etc.). The bootstrap schemas used `rangeMin`/`rangeMax` from an earlier draft; the spec was normalized to `min`/`max` but the bootstraps were not updated to match. The `rdfs:range`/`defaultValueType` was widened to `xsd:decimal`/`$Number` because the shared traits now serve both cardinality counts and numeric range bounds; per-shape SHACL constraints enforce the tighter per-Concept type rules.

---

## 2026-02-07: Bootstrap schema — Rename abbreviated `RdfTriple` trait names to match §9.6.1

**File:** `bootstrap-schema/schema.cdx`

**Change:** Renamed all abbreviated `RdfTriple` trait names to the full names defined in §9.6.1: `s` to `subject`, `p` to `predicate`, `o` to `object`, `lex` to `lexical` (297 occurrences across 99 triples). Trait `datatype` was already correct and unchanged.

**Rationale:** Commit 7157e3c (Jan 30) renamed the §9.6.1 trait definitions from `s`/`p`/`o`/`lex` to `subject`/`predicate`/`object`/`lexical` and touched the canonical bootstrap schema in the same commit, but did not apply the trait rename to the existing `RdfTriple` instances. The abbreviated names were valid under the original §9.6.1 but became non-conforming after the rename.

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

## 2026-02-07: §9.7.8, §9.9 — Prohibit generic trait mechanisms from targeting the `id` trait

**Sections:** §9.7.8 Traits and Value Terms, §9.9 Derived Validation Artifacts

**Changes:**
1. §9.7.8: Added paragraph after the `id` exception stating that schema definitions must not target `id` through generic trait mechanisms (`TraitRules`, `TraitPath`, `TraitExists`, `TraitMissing`, `TraitEquals`), with `SchemaError` on violation.
2. §9.9: Added `id`-targeting by generic trait mechanisms to the precondition failure list.

**Rationale:** The `id` trait is mapped via `codex:declaredId`, not `traitPredicateIri("id")` (§9.7.8). Generic trait mechanisms generate SHACL/SPARQL that queries `traitPredicateIri(t)`, which has no representation for `id`. Without an explicit prohibition, a schema author could write constraints referencing `id` via `TraitExists` or `TraitPath`; the expansion would produce valid SPARQL that silently returns no matches. Dedicated identity mechanisms (§9.9.6, §9.9.7) must be used instead.

---

## 2026-02-07: §12.5.1, §12.5.2 — Reclassify missing/unavailable schema errors from ParseError to SchemaError

**Sections:** §12.5.1 Schema Unavailable, §12.5.2 Schema Load Failure

**Changes:**
1. §12.5.1: Changed error class from `ParseError` to `SchemaError`. Changed "Parsing MUST NOT proceed" to "Validation MUST NOT proceed."
2. §12.5.2: Changed error class from `ParseError` to `SchemaError`.

**Rationale:** §12.2 was rewritten to classify a missing governing schema as `SchemaError`, but §12.5.1 and §12.5.2 were not updated to match. A missing or unloadable schema is a schema-level concern — the document itself parsed successfully. `ParseError` (§14.4.1) is defined as "a `.cdx` file cannot be parsed into a syntactic structure," which does not apply when the document is structurally valid but the schema is absent.

---

## 2026-02-07: §5.7.1 + A.1.17 — Reclassify unrecognized named-color error from SchemaError to ParseError

**Sections:** §5.7.1 Named Color Values, A.1.17 Color Values grammar comment

**Change:** Changed "unrecognized color name is a SchemaError (§14)" to "unrecognized color name is a ParseError (§14)" in both the prose (§5.7.1) and the EBNF grammar comment (A.1.17).

**Rationale:** §5.7 states that color well-formedness checking is "lexical and does not require a schema." SchemaError (§14.4.4) is defined as "parsed Codex violates schema-defined rules" where "the governing schema is consulted." The named color set is spec-defined (Appendix B), not schema-defined — no governing schema is consulted. §8.7 classifies unrecognized value spellings as ParseError, and §5.7.1 defines the Named Color Value spelling as requiring the name to be in Appendix B.

---

## 2026-02-07: §9.6.3 — Explicit one-list-per-(subject, predicate) constraint

**Section:** §9.6.3 RDF List Encoding (No Blank Nodes)

**Change:** Added: "At most one RDF list MUST be attached as the object of triples sharing a given `(subject, predicate)` pair."

**Rationale:** The list node IRI formula `listAnchor = subject + "/list/" + iriHash(predicate)` derives from `(subject, predicate)` only — two lists on the same pair would produce colliding skolem IRIs. The system's constraints already prevent this (the only list-valued predicate used is `sh:in`, emitted once per unique property shape), but the assumption was implicit. Making it explicit turns an accidental invariant into a normative guard.

---

## 2026-02-07: §9.7.2.1, §9.7.6, §9.7.7 — Clarify "source order" → "canonical order" in instance graph mapping

**Sections:** §9.7.2.1 Node IRI Derivation, §9.7.6 Ordered Children Encoding, §9.7.7 Annotation Nodes

**Change:** Changed "source order" to "canonical order" at all five occurrences within §9.7.

**Rationale:** The instance graph mapping operates on the fully canonicalized document, but "source order" did not specify whether this meant pre- or post-canonicalization order. For `$Unordered` collections whose children are reordered during Phase 2 (§10.5.1), two implementations could compute different `ordinalIndex` values and therefore different skolem IRIs. "Canonical order" removes the ambiguity. The two remaining "source order" references (§10.5.1 tiebreaker and §10.7 general processing rule) are intentionally unchanged.

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
