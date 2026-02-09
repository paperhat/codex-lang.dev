# Spec Change Log

This file records all changes made to the Codex specification during implementation.

---

## 2026-02-10: Text escape simplification — re-add `\\`, remove Unicode escape canonicalization rule

**Sections:** §10.5.2, A.1.8, A.2.8

**Changes:**

1. **A.1.8 + A.2.8**: Re-added `\\` (backslash escape) to the `EscapeSequence` production for quoted Text Values. Grammar now: `EscapeSequence = "\\", ( '"' | "\\" | UnicodeEscape )`. Backslash is literal unless followed by `\`, `"`, or `u`.
2. **§10.5.2**: Removed step 2 ("If `t` contains a Unicode escape sequence, render as backtick block"). The quoted-vs-backtick decision is now purely line-length based. Updated step 1: canonical quoted form escapes `\` as `\\` and `"` as `\"`. No other escapes are permitted in canonical quoted text — Unicode characters appear directly as UTF-8.

**Rationale:** With `\\` as a recognized escape, canonical quoted text can represent all characters: literal backslashes are escaped as `\\`, quotes as `\"`, and all other characters (including those formerly requiring `\uXXXX`) appear directly as UTF-8. Unicode escape sequences are still accepted during parsing but are resolved to their code points; the canonical output never emits them. This eliminates the need for the Unicode-escape-detection step and simplifies the canonicalization decision to a single line-length check.

---

## 2026-02-09: Schema Imports and Namespaced References

**Sections:** §2.2, §4.1.1 (new), §8.5.1–3, §9.1, §9.7.10–11, §10.5, §11.3, §11.3.1 (new), §11.4.3, §11.4.4, §12.2, §12.5.4–6 (new), §13.6, §14.4.1, §14.4.4, A.1.3–5, A.2.3–5
**Files:** `spec/1.0.0/index.md`, `spec/1.0.0/bootstrap-schema/schema.cdx`, `spec/1.0.0/bootstrap-schema/simplified/schema.cdx`

**Changes:**

1. **§4.1.1 Qualified Names** (new): Defined `namespace:ConceptName` and `namespace:traitName` forms. Namespace prefix follows camelCase (same form as Trait names). Language-level traits (`id`, `key`, `reference`, `target`, `for`) are never qualified.

2. **§8.5.1–3 Markers**: Opening, closing, and self-closing markers now accept `ConceptNameOrQualified`. Qualified closing markers must match qualified opening markers exactly.

3. **§9.1, §2.2**: Added `importedSchemas` to required inputs for schema-directed processing.

4. **§9.7.10–11**: Added imported schema trait predicate IRI derivation and conceptClassIri resolution for qualified concept names.

5. **§10.5 Canonicalization**: Added to Phase 2: namespace label normalization (author's label replaced with schema's declared `namespace`), SchemaImport entries ordered alphabetically by canonical namespace.

6. **§11.3 Schema**: Added required `namespace` trait (camelCase Text Value). Added `SchemaImports` to allowed children for both `$SimplifiedMode` and `$CanonicalMode`.

7. **§11.3.1 Schema Imports** (new): Full section defining `SchemaImports` (language-level child of any root concept, contains `SchemaImport` children) and `SchemaImport` (required `reference` IRI trait, required `namespace` Text trait). Governing schema is default namespace. Qualified names required only for imported definitions. Duplicate canonical namespace labels produce `SchemaError`.

8. **§11.4.3 TraitRules**: `RequiresTrait`, `AllowsTrait`, `ForbidsTrait` now accept qualified trait names (`namespace:traitName`) for imported traits.

9. **§11.4.4 ChildRules**: `AllowsChildConcept`, `RequiresChildConcept`, `ForbidsChildConcept`, `ConceptOption` now accept qualified concept names (`namespace:ConceptName`) for imported concepts.

10. **§12.2 Validate**: Expanded signature to `validate(documentBytes, governingSchema, importedSchemas) → validatedDocument`. `importedSchemas` maps schema IRIs to schema bytes.

11. **§12.5.4–6 Error Handling** (new): Three error subsections — Imported Schema Unavailable, Duplicate Namespace Label, Unresolved Qualified Name (all `SchemaError`).

12. **§13.6**: Changing the `namespace` trait value constitutes a breaking change.

13. **§14.4.1, §14.4.4**: Added import-related error examples to `ParseError` (SchemaImports on non-root) and `SchemaError` (missing import, duplicate namespace, unresolved qualified name).

14. **A.1.3–5 EBNF, A.2.3–5 PEG**: Added `QualifiedConceptName`, `NamespacePrefix`, `ConceptNameOrQualified` productions. Updated `OpeningMarker`, `ClosingMarker`, `SelfClosingMarker` to use `ConceptNameOrQualified`.

15. **Simplified bootstrap**: Added `namespace=bootstrap` to root Schema. Added `namespace` TraitDefinition, `SchemaImports` and `SchemaImport` ConceptDefinitions with required traits and child rules.

16. **Canonical bootstrap**: Added `namespace=bootstrap` to root Schema. Added `namespace` PropertyShape to Schema NodeShape. Added `SchemaImports` and `SchemaImport` NodeShapes with property shapes for `namespace`, `reference`, and child constraints.

**Rationale:** Schema composition without inheritance. Schemas import other schemas to reuse Concept and Trait definitions. Data documents reference imported Concepts via qualified names. Resolution is deterministic, closed-world, and registry-independent — the caller supplies imported schemas as byte maps via the `validate()` signature.

---

## 2026-02-08: Phase 10 — Canonical bootstrap triple reordering

**File:** `spec/1.0.0/bootstrap-schema/schema.cdx`

**Changes:**

1. **Reordered 1831 RdfTriple elements** per §9.6.2 sort order: ascending lexicographic on `(subject, predicate, objectKey)`. 1210 triples were in non-canonical positions. Zero duplicates found.

2. **Removed GROUP/END annotations** from the canonical bootstrap (the reorder tool strips grouping annotations since sorted order supersedes manual grouping).

**Tooling:** `tools/reorder_canonical_triples.py --apply`

**Verification:** All 17 Phase 10 checks pass (triple ordering, sh:closed parity, property shape count, no vestigial traits/enums, conformance suite consistency).

---

## 2026-02-08: Canonical comma spacing — one space after comma in collection literals

**Sections:** §8.7.1, §10.5
**Files:** `spec/1.0.0/index.md`, `spec/1.0.0/bootstrap-schema/simplified/schema.cdx`, `conformance/1.0.0/expected/canonical/` (5 files)

**Changes:**

1. **§8.7.1**: Changed canonical Value literal whitespace rule. Previously, all optional whitespace within balanced Value literals was removed. Now, exactly one space MUST follow each comma separator; all other optional whitespace is still removed. Removed the TypeParameters callout (no longer a special case — all commas now get a space).

2. **§10.5**: Updated Phase 1 canonicalization rule summary to match §8.7.1.

3. **Simplified bootstrap**: Reverted Phase 8 item 7 — restored space after comma in 4 `defaultValueTypes` list literals (`[$Text, $List<$Text>]`, `[$IriReference, $LookupToken]` x3).

4. **Conformance expected canonical outputs**: Added space after comma in collection literals across 5 files: `collection-literal-order-preserved`, `infinities-in-list`, `value-literal-kitchen-sink`, `value-type-matrix`, `map-keys-various-kinds`.

**Rationale:** Readability. Commas without spaces impose unnecessary cognitive load. All collection literals use balanced delimiters (`[...]`, `set[...]`, `map[...]`, `(...)`) so a stack-based parser handles interior spaces trivially. One space after comma is consistent with TypeParameters and with universal typographic convention.

---

## 2026-02-08: Text normalization + backtick wrapping

**Sections:** §5.1, §5.2, §10.5, §10.5.2, A.1.8, A.2.8, A.1.27

**Changes:**

1. **§5.1**: Applied whitespace normalization to all Text Value spellings (quoted and backtick). Runs of whitespace collapse to single spaces; leading/trailing spaces are trimmed; resulting Text Values are single-line.
2. **§5.2**: Backtick Text may span multiple source lines; escape rules remain ``\` `` only. Backtick text now explicitly relies on §5.1 normalization.
3. **§10.5.2 (new)**: Added deterministic Text Value formatting. Use quoted text when the trait line fits within 100 columns (tab width 2) and the value contains no Unicode escape sequence. Otherwise render a backtick block with deterministic word wrapping, canonical indentation, and escaped backticks only. *(Subsequently amended — see 2026-02-10 entry: Unicode escape detection removed; `\\` re-added to escapes; canonical quoted form now escapes `\` as `\\`.)*
4. **A.1.8 + A.2.8**: Removed `\n`, `\r`, `\t` and `\\` from Text escape sequences; only `\"` and Unicode escapes remain. Backslash is literal unless it begins one of those escapes. *(Subsequently amended — see 2026-02-10 entry: `\\` re-added as a recognized escape.)*
5. **A.1.27**: Removed the unused `AnyCharExceptBacktickNewline` character class.

**Rationale:** Backtick Text exists to allow multi-line authoring, so line breaks must be allowed and normalized rather than rejected. Applying a single normalization rule to all Text spellings makes semantics consistent. Deterministic wrapping prevents overlong trait lines while keeping canonical form stable. This change supersedes the 2026-02-07 Backtick Text newline exclusion.

---

## 2026-02-08: Phase 9 — Conformance test corrections

**Files:** `conformance/1.0.0/` (multiple)

**Changes:**

1. **Fixed `MARKDOWN:` directive** (9.1): Changed `MD:` to `MARKDOWN:` in both `cases/valid/block-annotation-md-directive/data.cdx` and `expected/canonical/block-annotation-md-directive/data.cdx`. `MD:` is not a recognized directive — only `FLOW:`, `CODE:`, and `MARKDOWN:` are valid (§8.9.5).

2. **Alphabetized traits in expected canonical outputs** (9.2): Reordered traits to alphabetical order in `selfclosing-multiline-traits` (3 traits), `value-literal-kitchen-sink` (12 traits), `value-type-matrix` (56 traits — also reformatted from inline to multiline per §8.5-6), and `collection-literal-order-preserved` (2 traits).

3. **Fixed range canonical form** (9.3): Changed `r=1 .. 10 s 2` to `r=1..10s2` in `expected/canonical/range-whitespace/data.cdx`. Canonical form strips optional whitespace from range literals.

4. **Fixed `color-mix-single-stop` error class** (9.4): Changed `primaryClass=$SchemaError` to `primaryClass=$ParseError` in `expected/errors/color-mix-single-stop/data.cdx`. A `color-mix()` with a single stop is a grammar violation, not a schema rule violation.

5. **Fixed all test schema files** (9.5): Applied uniform corrections to all 20 `schema.cdx` files under `cases/valid/` and `cases/invalid/`: added `authoringMode=$SimplifiedMode` (§11.3), added `versionScheme=$Semver` (§13.3), changed `$BackwardCompatible` to `$Initial` (§13.5), alphabetized all traits, reformatted to multiline where required (3+ traits).

6. **Fixed `schema-document-minimal`** (9.6): Updated both `cases/valid/schema-document-minimal/data.cdx` and `expected/canonical/schema-document-minimal/data.cdx` with all 5 required Schema traits in alphabetical multiline form.

7. **Resolved orphaned tests** (9.7): Moved `blankline-between-annotations-and-root` from `cases/invalid/` to `cases/valid/` — it is a valid general annotation per §8.9.8. Created expected canonical output.

8. **Updated manifest** (9.8): Added entries for `range-whitespace`, `color-mix-single-stop`, and `blankline-between-annotations-and-root`.

**Rationale:** Conformance test suite corrections to align expected outputs with canonical form rules (alphabetical traits, no optional whitespace), fix incorrect error classifications, add missing required Schema traits, and resolve orphaned/misclassified tests.

---

## 2026-02-08: Phase 8 — Simplified bootstrap parity and `TraitLessOrEqual` vocabulary extension

**Sections:** §11.10.1 (new `TraitLessOrEqual` subsection)
**Files:** `spec/1.0.0/index.md`, `spec/1.0.0/bootstrap-schema/simplified/schema.cdx`, `spec/1.0.0/bootstrap-schema/schema.cdx`

**Changes:**

1. **New `TraitLessOrEqual` atomic constraint** (§11.10.1): Cross-trait numeric comparison (`leftTrait <= rightTrait`). Two required Text traits (`leftTrait`, `rightTrait`). Vacuously satisfied when either trait is absent. SHACL expansion produces a SPARQL constraint selecting nodes where `?left > ?right`.

2. **Simplified bootstrap — `TraitLessOrEqual` concept**: Added `ConceptDefinition` (in "Atomic Constraints - Trait" group), `ConceptOption` in Rule's `ExactlyOneChildOf`, and `TraitDefinition` entries for `leftTrait` and `rightTrait` (in "Constraint Traits" group).

3. **Simplified bootstrap — 7 min/max ordering constraints**: New "Min/Max Ordering Constraints" group with `ConstraintDefinition` entries for: `allows-child-concept-min-max-ordering`, `requires-child-concept-min-max-ordering`, `trait-cardinality-min-max-ordering`, `value-length-min-max-ordering`, `value-in-numeric-range-min-max-ordering`, `member-count-min-max-ordering`, `on-path-count-min-max-ordering`.

4. **Simplified bootstrap — 3 positivity constraints**: Added `allows-child-concept-min-non-negative` (min >= 0), `allows-child-concept-max-positive` (max >= 1), and `requires-child-concept-max-positive` (max >= 1). These match the existing canonical SHACL-SPARQL constraints.

5. **Simplified bootstrap — removed vestigial `tag` TraitDefinition**: No concept references this trait. Already removed from canonical in Phase 7.

6. **Simplified bootstrap — removed orphaned `Cardinality` enum**: `EnumeratedValueSet` with `Single`/`List` members. No trait references it. Already removed from canonical in Phase 7.

7. **Simplified bootstrap — fixed list-typed trait value whitespace**: Removed space after comma in 4 `defaultValueTypes` list literals. *(Subsequently reverted — see "Canonical comma spacing" entry above; one space after comma is now canonical.)*

8. **Canonical bootstrap — `TraitLessOrEqual` NodeShape**: Added `sh:NodeShape` with `sh:closed true`, `sh:ignoredProperties`, and two required `PropertyShape` entries (`leftTrait`, `rightTrait`). Added `rdf:Property` declarations for both traits (3 triples each: `rdf:type`, `rdfs:label`, `rdfs:range`). Updated Rule's `ExactlyOneChildOf` SPARQL constraint message and query to include `TraitLessOrEqual`.

**Rationale:** Brings the simplified bootstrap into parity with the canonical bootstrap. The 7 min<=max constraints and 3 positivity constraints already existed as SHACL-SPARQL in the canonical bootstrap but had no simplified-mode equivalents. `TraitLessOrEqual` provides the vocabulary needed to express cross-trait numeric comparisons in simplified mode.

---

## 2026-02-08: Canonical bootstrap — Add codex/content and codex/isEntity to ignoredProperties

**File:** `spec/1.0.0/bootstrap-schema/schema.cdx`

**Changes:**
1. Added `codex/content` (§9.7.9) and `codex/isEntity` (§9.7.3) to the shared `sh:ignoredProperties` RDF list. Both predicates appear directly on concept instance nodes but were missing from the list, causing `sh:closed=true` shapes to reject any node with content or an entity marker. List expanded from 11 to 13 entries (`list/1..13`), maintaining alphabetical order.

---

## 2026-02-08: Canonical bootstrap — SHACL shape completeness

**File:** `spec/1.0.0/bootstrap-schema/schema.cdx`

**Changes:**
1. Added `sh:closed true` and `sh:ignoredProperties` to all 74 concept NodeShapes. The shared ignored properties list (13 entries: `rdf:type`, `codex/parentNode`, `codex/ordinalIndex`, `codex/declaredId`, `codex/content`, `codex/isEntity`, and 7 annotation predicates) is defined once at `urn:codex:bootstrap:shacl:ignoredProperties#list/1..13` and referenced by all shapes.
2. Added `sh:maxCount 1` to all 64 existing trait PropertyShapes that lacked it (required traits had `sh:minCount` but no `sh:maxCount`).
3. Added new PropertyShapes for all optional traits across 23 concepts (traits declared as `AllowsTrait` in simplified bootstrap but missing from canonical): `AllowsChildConcept` (min, max), `CollectionAllowsDuplicates` (keyTrait), `ConceptDefinition` (key, description, role), `Schema` (title, description, key), `TraitDefinition` (defaultValueType, defaultValueTypes, description, isReferenceTrait, priority), `EnumeratedValueSet` (key, description), `ValidatorDefinition` (message), `ValueTypeDefinition` (validatorName), and others. Each gets `rdf:type PropertyShape`, `sh:maxCount 1`, `sh:path`.
4. Added SHACL-SPARQL constraints for 12 `ExactlyOneChildOf` groups (AllowedValues, CollectionAllowsDuplicates, CollectionAllowsEmpty, CollectionOrdering, ContentRules, EachMemberSatisfies, MemberCount, OnPathCount, OnPathExists, OnPathForAll, OrderConstraint, Rule). Each generates a SPARQL query that counts matching child types and requires exactly one.
5. Added 3 positivity constraints: `AllowsChildConcept.min >= 0`, `AllowsChildConcept.max >= 1`, `RequiresChildConcept.max >= 1`.
6. Removed vestigial `tag` trait declaration (3 triples: `rdf:type`, `rdfs:label`, `rdfs:range`). No concept references this trait.
7. Removed orphaned `Cardinality` enum list chain (4 triples). No trait property constrains against this enum.

**Rationale:** Makes the canonical SHACL bootstrap a complete standalone validator, loadable by standard SHACL engines (pySHACL, TopBraid) to produce identical pass/fail verdicts as a Codex implementation's built-in bootstrap.

---

## 2026-02-08: Canonical bootstrap — Enum representation fix (IRIs, rdfs:range)

**File:** `spec/1.0.0/bootstrap-schema/schema.cdx`

**Changes:**
1. Changed all 98 `rdf:first` values in enum list chains from string literals (`lexical="MemberName"`) to IRIs (`object=urn:codex:bootstrap:enum:EnumName#MemberName`). Affects all 16 enum sets: `AuthoringMode` (2), `Cardinality` (2), `ChildConstraintType` (3), `CompatibilityClass` (4), `ConceptKind` (3), `ContentConstraintType` (3), `ContextConstraintType` (2), `EntityEligibility` (2), `IdentityConstraintType` (4), `OrderConstraintType` (2), `Ordering` (2), `ReferenceConstraintType` (5), `TraitPriority` (2), `ValueType` (56), `VersionScheme` (4), `WhitespaceMode` (2).
2. Changed `rdfs:range` from `xsd:token` to `rdfs:Resource` on 12 enum-valued trait properties: `authoringMode`, `baseValueType`, `compatibilityClass`, `conceptKind`, `defaultValueType`, `entityEligibility`, `ordering`, `priority`, `type`, `valueType`, `versionScheme`, `whitespaceMode`.
3. Left `rdfs:range` as `xsd:token` on 2 non-enum traits: `key` (Lookup Token), `set` (Lookup Token).
4. SPARQL queries: no changes needed (already use enum member IRIs).

**Rationale:** Enum members are now globally unique IRI resources, giving RDF-level type safety, exact SPARQL identity comparison, and standard SHACL `sh:in` semantics. Aligns `sh:in` lists with the SPARQL queries and spec §9.7.8 `valueTerm(v)` mapping.

---

## 2026-02-08: Appendix A.2 PEG grammar — Prefix ordering, alignment fixes, rule renames/extractions

**File:** `spec/1.0.0/index.md`

**Changes:**
1. `RgbColorSpace`: reordered `'srgb-linear'` before `'srgb'` (PEG is ordered-choice; `'srgb'` prefix-matches `'srgb-linear'`).
2. `XyzColorSpace`: reordered `'xyz-d50'`, `'xyz-d65'` before `'xyz'` (same prefix issue).
3. `RelativeColorComponent`: reordered `ColorPercentage` before `ColorRealNumber` (percentage is more specific).
4. `Traits`: removed second alternative that allowed newline before first trait (EBNF has no such alternative).
5. `CharEscapeSequence`: changed `["'\\nrt]` to `['\\nrt]` (double-quote is not a valid escape in single-quoted character literals; EBNF lists `"'"` not `'"'`).
6. `AnnotationLine`: removed `[ \t]*` between `]` and `Newline` (EBNF has no trailing whitespace).
7. `AnnotationBlock`: removed `[ \t]*` after opening `[` and after closing `]` (EBNF has no trailing whitespace).
8. Rule renames: `LeadingAnnotationBlocks` → `OptionalLeadingAnnotations`, `TrailingBlankLines` → `OptionalTrailingBlankLines`, `BOL` → `ConceptLineStart0` (folding `StartOfFile` inline), `IriBody` → `IriTokenBody`.
9. Extracted 10 named rules matching EBNF: `FunctionColor`, `ColorSpace`, `NonZeroDigit`, `WhitespaceNoNewlineChar`, `UnescapedTextCharacter`, `UnescapedChar`, `UnescapedAnnotationChar`, `UnescapedAnnotationBlockChar`, `ConceptMarkerOrConcept`, `GeneralOrGroupingAnnotationBlock`.
10. Updated `ColorMixFunc` and `RelativeColorFuncColor` to use the new `ColorSpace` rule instead of inline `(RgbColorSpace / XyzColorSpace)`.

**Rationale:** PEG is ordered-choice: `'srgb'` before `'srgb-linear'` causes the parser to match `'srgb'` and fail on the `-linear` suffix. Same issue with `'xyz'` vs `'xyz-d50'`/`'xyz-d65'`, and `ColorRealNumber` vs `ColorPercentage` (percentage has a trailing `%` that makes it more specific). The second `Traits` alternative admitted a leading newline before the first trait, which EBNF forbids. `CharEscapeSequence` incorrectly allowed `\"` inside single-quoted character literals. Trailing whitespace in annotation rules contradicted EBNF. Rule names diverged from EBNF without reason. Named rules were inlined in PEG but named in EBNF, making cross-referencing harder.

---

## 2026-02-08: §9.5.2, §9.7.10, §11.3–§11.6 — Align spec with bootstrap schema

**File:** `spec/1.0.0/index.md`

**Changes:**
1. §11.3 (Schema): Added `authoringMode` to the required traits bullet list (was required by prose but missing from the list). Added `key` (optional; Lookup Token Value).
2. §11.4.1 (ConceptDefinition): Added `description` (optional; Text Value) and `role` (optional; Text Value).
3. §11.4.3 (TraitRules): Added `AllowedValues` as optional child of `RequiresTrait` and `AllowsTrait`, with narrowing semantics paragraph.
4. §11.5.1 (TraitDefinition): Changed `id` from optional to required. Added `description` (optional; Text Value). Added "A `TraitDefinition` is an Entity."
5. §11.5.2 (AllowedValues): Changed "One or more value constraints" to "Exactly one of:" (bootstrap uses `ExactlyOneChildOf`).
6. §11.6.2 (ValueTypeDefinition): Changed `id` from optional to required. Added "A `ValueTypeDefinition` is an Entity."
7. §11.6.3 (EnumeratedValueSet): Added `id` (required), `key` (optional), `description` (optional). Added "An `EnumeratedValueSet` is an Entity."
8. §9.5.2 (ValidatorDefinition): Added `id` (required). Added "A `ValidatorDefinition` is an Entity."
9. §9.7.10: Removed dead "has no `id`" case from `traitPredicateIri(t)` — now that `TraitDefinition.id` is required, this case is unreachable.
10. §11.5.1 examples: Normalized list literal whitespace (`[$Grams, $Kilograms, ...]` → `[$Grams,$Kilograms,...]`, `[$Text, $List<$Text>]` → `[$Text,$List<$Text>]`) per Phase 3's canonical value whitespace rule.

**Rationale:** The bootstrap schema (both canonical and simplified) already declares these traits, entity statuses, and child constraints. The spec text lagged behind. `TraitDefinition.id` being required eliminates the fallback `schemaIri + "#trait/" + t` path in §9.7.10, simplifying predicate IRI derivation. `AllowedValues` under `RequiresTrait`/`AllowsTrait` enables concept-level narrowing of trait-definition-level value constraints. Spec CDX examples contained optional whitespace in list literals that contradicts the canonical value whitespace rule.

---

## 2026-02-08: §8.7.1, §10.5 — Canonical Value literal whitespace rule

**File:** `spec/1.0.0/index.md`

**Changes:**
1. §8.7.1 (Multiline Value Literals): Added canonical form statement — optional whitespace within balanced Value literals MUST be removed; mandatory whitespace required by specific productions MUST be preserved.
2. §10.5 (Canonicalization Rules): Added "canonical Value literal whitespace" to the Phase 1 rule list, with the same remove-optional/preserve-mandatory semantics.

**Rationale:** The specification defined optional whitespace tolerance for parsing (§8.7.1) and alphabetical trait ordering for canonical form (§10.5), but never stated the canonical form of whitespace within Value literals themselves. Collections (`[1, 2, 3]` vs `[1,2,3]`), ranges (`1 .. 10` vs `1..10`), and other balanced forms had no canonical whitespace rule. Canonical form strips all optional whitespace while preserving mandatory whitespace (e.g., color function argument spaces `rgb(0 0 0)`, TypeParameters comma-space `$Map<$Text, $Integer>`).

---

## 2026-02-08: §9.7.8 — Enumerated Token Value-Term Mapping via EnumeratedValueSet IRIs

**File:** `spec/1.0.0/index.md`

**Changes:**
1. Added new `valueTerm(v)` case: Enumerated Token Values constrained by an `EnumeratedValueSet` produce IRIs (`E.id + "#" + tokenName(v)`) instead of typed literals. Inserted between the IRI Reference case and the typed literal fallback.
2. Added five normative paragraphs after the Lookup Token section specifying: the IRI construction rule, collection element independence, `ValueIsOneOf` fallthrough, and unconstrained fallthrough.

**Rationale:** Three mutually inconsistent enum representations existed: spec §9.7.8 used typed literals (`"$ForbidsContent"^^urn:cdx:value-type:EnumeratedToken`), SPARQL queries used IRIs (`<urn:codex:bootstrap:enum:ContentConstraintType#ForbidsContent>`), and `sh:in` lists used plain strings (`"ForbidsContent"^^xsd:string`). IRIs give RDF-level type safety, exact SPARQL identity comparison, cross-enum-set structural disambiguation, and standard SHACL `sh:in` semantics. SPARQL queries were already correct. This spec change aligns §9.7.8 with the SPARQL queries; Phases 6–7 will align the `sh:in` lists.

---

## 2026-02-08: Spec text fixes — Cross-references, heading levels, CLAUDE.md

**Files:** `spec/1.0.0/index.md`, `CLAUDE.md`

**Changes:**
1. §2.5 (line 152): Fixed cross-reference `§12.4` → `§12.3`. The bootstrap schema-of-schemas is defined in §12.3; §12.4 is Schema Caching.
2. §11.1 (line 4029): Fixed same cross-reference `§12.4` → `§12.3`.
3. §14.5.1 (line 6072): Fixed section number `14.6.1` → `14.5.1`. Former §14.6 was renumbered to §14.5 when §14.5 "Error Severity" was removed (2026-02-07), but subsection 14.6.1 was not renumbered.
4. §8.7.1 (line 2058): Fixed heading level `###` → `####`. Parent §8.7 is `###`, so §8.7.1 must be `####`.
5. §10.2.1.1 (line 3796): Fixed heading level `###` → `#####`. Parent chain: §10.2 is `###`, §10.2.1 is `####`, so §10.2.1.1 must be `#####`.
6. `CLAUDE.md` (line 132): Updated §14.5 summary from "Errors are not warnings. No best-effort recovery." to "Reporting Requirements — primary error class, concept name, trait name, rule reference, precise location." reflecting the section's current content after the 2026-02-07 renumbering.

**Rationale:** Cross-references pointed to §12.4 (Schema Caching) instead of §12.3 (Bootstrap Schema-of-Schemas). Section 14.6.1 was orphaned after its parent §14.6 was renumbered to §14.5. Two heading levels were inconsistent with their parent section depth. CLAUDE.md described §14.5 using the removed "Error Severity" content instead of the current "Reporting Requirements" content.

---

## 2026-02-07: Canonical bootstrap schema — Add missing reference trait declarations (`for`, `reference`, `target`)

**File:** `bootstrap-schema/schema.cdx`

**Change:** Added 9 `rdf:Property` declaration triples (3 per trait) for the reference traits `for`, `reference`, and `target`. Each receives `rdf:type=rdf:Property`, `rdfs:label`, and `rdfs:range=xsd:anyURI`. Inserted alphabetically: `for` between `flags` and `id`; `reference` between `priority` and `role`; `target` between `tag` and `title`.

**Rationale:** The simplified schema declares all 52 traits; the canonical schema declared only 49 — missing the 3 reference traits defined in §7.1. These are core language primitives ("Codex defines exactly three reference Traits"). Every other trait had a complete 3-triple `rdf:Property` declaration; the reference traits were the only gap. Range is `xsd:anyURI` because both `$IriReference` and `$LookupToken` resolve to IRIs in the RDF graph, matching how `id` (also IRI-valued) uses `xsd:anyURI`.

---

## 2026-02-07: Canonical bootstrap schema — Fix IRI issues (SPARQL predicates, missing trait declarations, list renumbering)

**File:** `bootstrap-schema/schema.cdx`

**Changes:**
1. **SPARQL queries: replaced `rel:hasChild` with `codex:parentNode`** — All 13 SHACL-SPARQL constraint queries used the fabricated predicate `urn:codex:bootstrap:rel:hasChild` (parent-to-child). Replaced with `urn:codex:bootstrap:1.0.0#codex/parentNode` (child-to-parent), reversing subject/object per §9.7.4. The old predicate had no §9.7 emission rule and would never match any instance graph triple.
2. **Added `rdfs:range` for `role` and `tag` traits** — Both trait declarations had `rdf:type` and `rdfs:label` but were missing `rdfs:range`. All other 45 trait declarations have all three. Range is `urn:codex:bootstrap:datatype:text`, consistent with similar traits (`name`, `description`, `value`, etc.) and the simplified schema's `defaultValueTypes=[$Text, $List<$Text>]`.
3. **Added trait declarations for `versionScheme` and `whitespaceMode`** — Both are used as `sh:path` values in SHACL property shapes but had no `rdf:Property` declaration (no `rdf:type`, `rdfs:label`, or `rdfs:range` triples). Added 3 triples each with `rdfs:range=xsd:token`, matching other `$EnumeratedToken` traits (`authoringMode`, `compatibilityClass`, `ordering`, etc.).
4. **Renumbered ValueType enum list IRIs** — 8 letter-suffixed list node IRIs (`#list/12a`–`#list/12e`, `#list/29a`–`#list/29c`) arose from inserting new enum members without renumbering. Renumbered all 56 list nodes to consecutive integers `#list/1`–`#list/56` by following the `rdf:first`/`rdf:rest` chain.

**Rationale:** (1) `rel:hasChild` was a non-existent predicate — §9.7 emits `codex:parentNode` (child-to-parent), not a `hasChild` (parent-to-child). (2–3) Incomplete trait declarations created asymmetry with the other 45 fully-declared traits. (4) Letter-suffixed list IRIs violated the consecutive-integer convention used by all other RDF list encodings in the schema.

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
