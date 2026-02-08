# Post-Audit Fix Plan (Revised)

## Context

Six parallel audits identified findings across the specification, grammars, bootstrap schemas, and conformance test suite. The canonical SHACL bootstrap is intended as a **complete standalone validator** — loadable by a standard SHACL engine (pySHACL, TopBraid) to produce identical pass/fail verdicts as a Codex implementation's built-in bootstrap.

Previous work (already merged): Added 9 `rdf:Property` triples for `for`, `reference`, `target`.

## Decisions

### Enum Representation → IRIs

Three mutually inconsistent representations exist today:

| Source | `$ForbidsContent` represented as |
|--------|----------------------------------|
| Spec §9.7.8 (valueTerm) | Typed literal: `"$ForbidsContent"^^urn:cdx:value-type:EnumeratedToken` |
| Bootstrap SPARQL queries | IRI: `<urn:codex:bootstrap:enum:ContentConstraintType#ForbidsContent>` |
| Bootstrap `sh:in` lists | Plain string: `"ForbidsContent"^^xsd:string` (no `$`, wrong datatype) |

**Decision:** IRIs. Each enum member becomes a globally unique IRI resource. This gives RDF-level type safety, exact SPARQL identity comparison, cross-enum-set structural disambiguation, and standard SHACL `sh:in` semantics. Requires a spec change to §9.7.8 (new case for EnumeratedValueSet-constrained Enumerated Tokens). SPARQL queries are already correct. `sh:in` lists and `rdfs:range` need fixing.

### Trait Value Whitespace → Remove all optional whitespace

Remove all optional whitespace from canonical trait value literals. Required whitespace per grammar productions is preserved.

Canonical forms: `x..y` / `x..ysz` (ranges), `[1,2,3]` (lists), `set[$A,$B]` (sets), `map[a:1,b:2]` (maps), `record[x:1]` (records), `(1,2)` (tuples). The grammar accepts optional whitespace for parsing tolerance; canonical form strips it.

Whitespace that is NOT optional (required by specific grammar productions, MUST be preserved):
- Modern color function arguments: `rgb(0 0 0)` — `ColorWhitespace` is `[ \t]+` (mandatory)
- `color-mix(in srgb, ...)` — `ColorWhitespace` after `in` (mandatory)
- TypeParameters comma-space: `$Map<$Text, $Integer>` — grammar encodes `",", " "` (mandatory)
- TypeUnion comma-space inside TypeParameters: `<[$Text, $Integer]>` — grammar encodes `",", " "` (mandatory)

Whitespace that IS always preserved regardless:
- Inside double-quoted text (`"..."`)
- Inside backtick text (`` `...` ``)
- A character literal that IS a whitespace character (width is always 1)

Note: `TypeUnion` is NOT a `Value` alternative in either grammar (EBNF §A.1.7 / PEG §A.2.7). It only appears as a `TypeArgument` inside `TypeParameters`. Therefore `[$Text, $List<$Text>]` as a standalone trait value parses as `ListValue` (optional whitespace separators), not `TypeUnion`.

### PEG/EBNF Alignment → Fix PEG to match EBNF

- Remove second `Traits` alternative (forbid newline before first trait)
- Remove `"` from `CharEscapeSequence` char class
- Remove trailing whitespace allowances in `AnnotationLine`/`AnnotationBlock`
- Rename PEG rules to match EBNF names
- Fix prefix ordering bugs (`srgb-linear` before `srgb`, etc.)

### Spec vs Bootstrap → Update spec to match bootstrap

All items approved. Spec text catches up to the working bootstrap.

### AllowedValues under RequiresTrait/AllowsTrait → Add with narrowing semantics

The bootstrap already has `AllowedValues` as optional child of `RequiresTrait` and `AllowsTrait`. The spec only mentions it under `TraitDefinition`. Add it to the spec with semantics: concept-level `AllowedValues` further narrows `TraitDefinition.AllowedValues` — must be a subset. If both exist, the concept-level constraint governs. SHACL translation: additional `sh:property` with `sh:path` = trait IRI and `sh:in` = concept-level allowed values list.

### Vestigial Items → Remove

- Remove `tag` trait definition from both bootstraps (no usage, no spec reference)
- Remove `Cardinality` enum from both bootstraps (orphaned `sh:in`, no trait references it)

---

## Execution Plan

### Phase 1: Spec Text Fixes ✅ COMPLETE

Pure corrections. No design decisions.

**File: `spec/1.0.0/index.md`**

1. **Line 152**: `§12.4` → `§12.3` (bootstrap schema-of-schemas is §12.3; §12.4 is Schema Caching)
2. **Line 4029**: `§12.4` → `§12.3` (same reference)
3. **Line 6072**: `#### 14.6.1` → `#### 14.5.1` (former §14.6 renumbered to §14.5 after §14.5 removal)
4. **Line 2058**: `### 8.7.1` → `#### 8.7.1` (8.7 is `###`, so 8.7.1 must be `####`)
5. **Line 3796**: `### 10.2.1.1` → `##### 10.2.1.1` (10.2 is `###`, 10.2.1 is `####`, 10.2.1.1 must be `#####`)

**File: `CLAUDE.md`**

6. **Line 132**: Change `§14.5: Errors are not warnings. No best-effort recovery.` to `§14.5: Reporting Requirements — primary error class, concept name, trait name, rule reference, precise location.` (§14.5 is now "Reporting Requirements" after old §14.5 "Error Severity" was removed)

**File: `SPEC_CHANGE_LOG.md`**

7. Changelog entry

---

### Phase 2: Spec §9.7.8 — Enumerated Token Value-Term Mapping ✅ COMPLETE

**File: `spec/1.0.0/index.md`**

In §9.7.8 (`valueTerm(v)`), add a new case between the IRI Reference case and the typed literal fallback:

**Current text (lines 2938–2941):**
```
`valueTerm(v)` MUST be:

- an IRI when `v` is an IRI Reference Value
- otherwise a typed literal
```

**New text:**
```
`valueTerm(v)` MUST be:

- an IRI when `v` is an IRI Reference Value
- an IRI when `v` is an Enumerated Token Value and the governing trait
  is constrained by an `EnumeratedValueSet` (see below)
- otherwise a typed literal
```

Add a new paragraph after the `valueLex(v)` / Lookup Token sections (after line 2974):

> When an Enumerated Token Value `v` appears on a trait that is constrained by an `EnumeratedValueSet` `E` (via `AllowedValues` containing an `EnumeratedConstraint` referencing `E`), `valueTerm(v)` MUST be the IRI:
>
> `E.id + "#" + tokenName(v)`
>
> where `tokenName(v)` is the token name without the `$` sigil.
>
> This rule applies regardless of where the Enumerated Token Value appears in the trait's value structure. If the trait value is a collection (List, Set, Map, Record, Tuple, or Range) whose elements are Enumerated Token Values, each element `v` MUST independently produce an IRI via the same rule.
>
> If the trait is constrained only by `ValueIsOneOf` (not by an `EnumeratedConstraint` referencing an `EnumeratedValueSet`), Enumerated Token Values fall through to the typed literal case above. `ValueIsOneOf` does not provide an `EnumeratedValueSet` from which to derive an IRI base.
>
> If the trait is not constrained by any `EnumeratedValueSet`, the Enumerated Token Value falls through to the typed literal case above.

**File: `SPEC_CHANGE_LOG.md`**

Changelog entry

---

### Phase 3: Spec §10.5 — Canonical Value Whitespace ✅ COMPLETE

**File: `spec/1.0.0/index.md`**

1. **§10.5 Phase 1** (line ~3853–3867): Add to the Phase 1 canonicalization rule list:
   - `canonical value literal whitespace (no whitespace in trait values except inside text/backtick string literals and whitespace character literals)`

2. **§8.7.1** (line 2058–2070): Add a sentence clarifying canonical form. After "Whitespace MUST NOT terminate the Value." add:
   > In canonical surface form, optional whitespace within balanced Value literals MUST be removed. Canonical form uses no whitespace between elements, entries, delimiters, operators, or separators within a Value literal. Mandatory whitespace required by a specific production (for example, the space after comma in TypeParameters) is not optional and MUST be preserved.

**File: `SPEC_CHANGE_LOG.md`**

Changelog entry

---

### Phase 4: Spec §11 — Align with Bootstrap ✅ COMPLETE

**File: `spec/1.0.0/index.md`**

| Section | Change | Detail |
|---------|--------|--------|
| §11.3 | Add `authoringMode` to required traits list | Already required by prose at line 4086 but missing from the bullet list at lines 4060–4079 |
| §11.3 | Add `key` (optional; Lookup Token Value) | Bootstrap has `AllowsTrait name="key"` on Schema |
| §11.4.1 | Add `description` (optional; Text Value) | Bootstrap has `AllowsTrait name="description"` on ConceptDefinition |
| §11.4.1 | Add `role` (optional; Text Value) | Bootstrap has `AllowsTrait name="role"` on ConceptDefinition |
| §11.4.3 | Add `AllowedValues` as optional child of `RequiresTrait` and `AllowsTrait` | Bootstrap has `AllowsChildConcept conceptSelector="AllowedValues" max=1` on both |
| §11.4.3 | Add narrowing semantics paragraph | Concept-level `AllowedValues` narrows `TraitDefinition.AllowedValues`. Must be subset. SHACL: additional `sh:property` with `sh:in` on the concept's NodeShape |
| §11.5.1 | Change `id` from optional to required | Bootstrap has `RequiresTrait name="id"` |
| §11.5.1 | Add `description` (optional; Text Value) | Bootstrap has `AllowsTrait name="description"` |
| §11.5.1 | Add "A `TraitDefinition` is an Entity." | Consequence of `id` being required |
| §11.5.2 | Change "One or more value constraints" to "Exactly one of:" | Bootstrap uses `ExactlyOneChildOf` with `ValueIsOneOf` / `EnumeratedConstraint` |
| §11.6.2 | Change `id` from optional to required | Bootstrap has `RequiresTrait name="id"` |
| §11.6.2 | Add "A `ValueTypeDefinition` is an Entity." | Consequence of `id` being required |
| §11.6.3 | Add `id` (required; IRI Reference Value) | Bootstrap has `RequiresTrait name="id"` |
| §11.6.3 | Add `key` (optional; Lookup Token Value) | Bootstrap has `AllowsTrait name="key"` |
| §11.6.3 | Add `description` (optional; Text Value) | Bootstrap has `AllowsTrait name="description"` |
| §11.6.3 | Add "An `EnumeratedValueSet` is an Entity." | Consequence of `id` being required |
| §9.5.2 | Add `id` (required; IRI Reference Value) | Bootstrap has `RequiresTrait name="id"` |
| §9.5.2 | Add "A `ValidatorDefinition` is an Entity." | Consequence of `id` being required |

**§9.7.10 consequence** (line 2994–2996): Since `TraitDefinition.id` is now required, the second bullet ("has no `id`") becomes unreachable dead code. Remove it. The rule simplifies to: `traitPredicateIri(t)` MUST be the `TraitDefinition.id` for `t`. Zero or multiple definitions → `SchemaError`.

**Spec example whitespace normalization** (§11.5.1, lines 4405–4428): CDX code examples contain list literal values with optional whitespace that must be normalized per Phase 3's canonical value whitespace rule. `TypeUnion` is NOT a `Value` alternative (EBNF §A.1.7 / PEG §A.2.7) — it only appears inside `TypeParameters`. Therefore `[$Text, $List<$Text>]` as a trait value parses as `ListValue`, where separators have optional whitespace. Changes:

- Line 4416: `values=[$Grams, $Kilograms, $Milliliters, $Liters, $Units]` → `values=[$Grams,$Kilograms,$Milliliters,$Liters,$Units]`
- Line 4427: `defaultValueTypes=[$Text, $List<$Text>]` → `defaultValueTypes=[$Text,$List<$Text>]`

**File: `SPEC_CHANGE_LOG.md`**

Changelog entry

---

### Phase 5: PEG Grammar Fixes (Appendix A.2) ✅ COMPLETE

**File: `spec/1.0.0/index.md`**

1. **`RgbColorSpace`**: reorder `'srgb-linear'` before `'srgb'` (PEG is ordered-choice; `'srgb'` prefix-matches `'srgb-linear'`)
2. **`XyzColorSpace`**: reorder `'xyz-d50'`, `'xyz-d65'` before `'xyz'` (same prefix issue)
3. **`RelativeColorComponent`**: reorder `ColorPercentage` before `ColorRealNumber` (percentage is more specific)
4. **`Traits`**: remove second alternative that allows newline before first trait
5. **`CharEscapeSequence`**: change `["'\\nrt]` to `['\\nrt]` (double-quote is not a valid escape in single-quoted character literals)
6. **`AnnotationLine`**: remove `[ \t]*` between `]` and `Newline` (trailing whitespace not permitted per EBNF)
7. **`AnnotationBlock`**: remove `[ \t]*` after opening `[` and closing `]` (trailing whitespace not permitted per EBNF)
8. **Rule renames** — rename PEG rules to match EBNF names:

| Current PEG Name | Target EBNF Name |
|---|---|
| `LeadingAnnotationBlocks` | `OptionalLeadingAnnotations` |
| `TrailingBlankLines` | `OptionalTrailingBlankLines` |
| `BOL` | `ConceptLineStart0` |
| `StartOfFile` | (remove; fold into `ConceptLineStart0`) |
| `IriBody` | `IriTokenBody` |

9. **Extract named rules** — the following are inlined in PEG but named in EBNF. Extract each as a named PEG rule:

| Named Rule to Add |
|---|
| `FunctionColor` |
| `ColorSpace` |
| `NonZeroDigit` |
| `WhitespaceNoNewlineChar` |
| `UnescapedTextCharacter` |
| `UnescapedChar` |
| `UnescapedAnnotationChar` |
| `UnescapedAnnotationBlockChar` |
| `ConceptMarkerOrConcept` |
| `GeneralOrGroupingAnnotationBlock` |

**File: `SPEC_CHANGE_LOG.md`**

Changelog entry

---

### Phase 6: Canonical Bootstrap — Enum Representation ✅ COMPLETE

**File: `spec/1.0.0/bootstrap-schema/schema.cdx`**

1. **Change `sh:in` list members** from `xsd:string` literals to IRIs across all 16 enum list chains.

   For each enum member, change:
   ```
   <RdfTriple subject=urn:codex:bootstrap:enum:EnumName#list/N predicate=rdf:first lexical="MemberName" />
   ```
   to:
   ```
   <RdfTriple subject=urn:codex:bootstrap:enum:EnumName#list/N predicate=rdf:first object=urn:codex:bootstrap:enum:EnumName#MemberName />
   ```

   The 16 enum sets: `AuthoringMode`, `ChildConstraintType`, `CompatibilityClass`, `ConceptKind`, `ContentConstraintType`, `ContextConstraintType`, `EntityEligibility`, `IdentityConstraintType`, `OrderConstraintType`, `Ordering`, `Priority`, `ReferenceConstraintType`, `ValueType`, `VersionScheme`, `WhitespaceMode`, and any remaining sets.

2. **Change `rdfs:range`** from `xsd:token` to `rdfs:Resource` on all enum-valued trait properties:
   - `authoringMode`, `compatibilityClass`, `conceptKind`, `entityEligibility`, `ordering`, `priority`, `type`, `versionScheme`, `whitespaceMode`
   - `baseValueType` and `valueType` (constrained to `ValueType` enum)

3. **SPARQL queries**: no changes needed (already use IRIs correctly).

**File: `SPEC_CHANGE_LOG.md`**

Changelog entry

---

### Phase 7: Canonical Bootstrap — SHACL Shape Completeness ✅ COMPLETE

**File: `spec/1.0.0/bootstrap-schema/schema.cdx`**

1. **Add `sh:closed=true` + `sh:ignoredProperties`** to all 74 primary NodeShapes.

   Ignored properties list (RDF list attached to each NodeShape):
   - `rdf:type`
   - `urn:codex:bootstrap:1.0.0#codex/parentNode`
   - `urn:codex:bootstrap:1.0.0#codex/ordinalIndex`
   - `urn:codex:bootstrap:1.0.0#codex/declaredId`
   - `urn:codex:bootstrap:1.0.0#codex/annotationParent`
   - `urn:codex:bootstrap:1.0.0#codex/annotationIndex`
   - `urn:codex:bootstrap:1.0.0#codex/annotationText`
   - `urn:codex:bootstrap:1.0.0#codex/annotationForm`
   - `urn:codex:bootstrap:1.0.0#codex/annotationKind`
   - `urn:codex:bootstrap:1.0.0#codex/annotationDirective`
   - `urn:codex:bootstrap:1.0.0#codex/annotationTarget`

2. **Add property shapes for all optional traits** (concepts that have `AllowsTrait` entries in simplified bootstrap). Each gets:
   - `sh:path` pointing to the trait IRI
   - `sh:maxCount 1`
   - `sh:in` where the trait is enum-valued (referencing the enum list's first node IRI — now an IRI list per Phase 6)
   - `sh:datatype` where appropriate (non-enum traits)

3. **Add `sh:maxCount 1`** to all existing required trait property shapes where missing.

4. **Add SHACL-SPARQL constraints for `ExactlyOneChildOf`** (concepts using `ExactlyOneChildOf` in simplified bootstrap — approximately 12). Pattern:
   ```sparql
   SELECT $this WHERE {
     { SELECT $this (COUNT(?child) AS ?count) WHERE {
       ?child <urn:codex:bootstrap:1.0.0#codex/parentNode> $this .
       { ?child a <urn:codex:bootstrap:concept:TypeA> }
       UNION { ?child a <urn:codex:bootstrap:concept:TypeB> }
     } GROUP BY $this }
     FILTER(?count != 1)
   }
   ```

5. **Add `ValidatorDefinition` content rules** — SHACL representation for content mode (`AllowsContent` with `$Preformatted`).

6. **Add 3 missing positivity constraints** (F-16, F-17, F-18):
   - `AllowsChildConcept.min` must be >= 0
   - `AllowsChildConcept.max` must be >= 1
   - `RequiresChildConcept.max` must be >= 1

7. **Remove `tag` trait declaration** (3 triples: `rdf:type`, `rdfs:label`, `rdfs:range`)

8. **Remove `Cardinality` enum list chain** (orphaned `sh:in` list — all `rdf:first`/`rdf:rest` triples for the Cardinality enum)

**File: `SPEC_CHANGE_LOG.md`**

Changelog entry

---

### Phase 8: Simplified Bootstrap Updates

**File: `spec/1.0.0/bootstrap-schema/simplified/schema.cdx`**

1. **Add 7 min≤max `ConstraintDefinition` entries** matching canonical bootstrap's extras (constraints that enforce `min` <= `max` on concepts that have both traits)

2. **Add 3 positivity constraints** matching canonical (Phase 7 item 6)

3. **Remove `tag` trait definition** (vestigial — no usage, no spec reference)

4. **Remove `Cardinality` enum definition** (orphaned — no trait references it)

5. **Fix list-typed trait value whitespace** — change all `defaultValueTypes=[$X, $Y]` to `defaultValueTypes=[$X,$Y]` (no space after comma in canonical collection literals). Applies to `description`, `role`, `for`, `reference`, `target`, and any other traits with list-typed default values.

**File: `SPEC_CHANGE_LOG.md`**

Changelog entry

---

### Phase 9: Conformance Test Corrections

**Files: `conformance/1.0.0/` (multiple)**

#### 9.1 Fix `MARKDOWN:` directive

- `cases/valid/block-annotation-md-directive/data.cdx`: Change `MD:` to `MARKDOWN:` in both the input and the expected canonical output at `expected/canonical/block-annotation-md-directive/data.cdx`
- Add to manifest if not already present.

Note: No negative test for `MD:`. The grammar (EBNF §A.1.25 / PEG §A.2.25) accepts any annotation content — `AnnotationBlockLine` matches any characters. Directive recognition is post-parse exact-match to `FLOW:`, `CODE:`, or `MARKDOWN:` only (§8.9.5). `MD:` does not match any of these three strings, so it is simply valid non-directive annotation content. It is not an error.

#### 9.2 Alphabetize traits in expected canonical outputs

- `expected/canonical/selfclosing-multiline-traits/data.cdx`: Reorder traits to `author`, `id`, `title`
- `expected/canonical/value-literal-kitchen-sink/data.cdx`: Reorder 12 traits alphabetically: `color`, `date`, `id`, `iri`, `list`, `lookup`, `map`, `range`, `record`, `set`, `tuple`, `uuid`
- `expected/canonical/value-type-matrix/data.cdx`: Reorder 56 traits alphabetically AND reformat to multiline (56 traits violates the 3+ inline rule — canonical form requires each trait on its own line with `/>` on own line)
- Verify: `collection-literal-order-preserved` (likely already correct)

#### 9.3 Fix range canonical form

- `expected/canonical/range-whitespace/data.cdx`: Change `r=1 .. 10 s 2` to `r=1..10s2`

#### 9.4 Fix `color-mix-single-stop` error class

- `expected/errors/color-mix-single-stop/data.cdx`: Change `primaryClass=$SchemaError` to `primaryClass=$ParseError` (`color-mix()` with a single stop is a grammar violation, not a schema rule violation)

#### 9.5 Fix all test schema files (~20 files)

Apply uniformly to every `schema.cdx` in `cases/valid/` and `cases/invalid/`:

- Add `authoringMode=$SimplifiedMode` (required per §11.3, currently missing from all)
- Add `versionScheme=$Semver` (required per §13.3, currently missing from all)
- Change `$BackwardCompatible` to `$Initial` (required per §13.5 for first version)
- Alphabetize traits. With all required traits, canonical form is:
  ```cdx
  <Schema
  	authoringMode=$SimplifiedMode
  	compatibilityClass=$Initial
  	id=example:schema:test-name
  	version="0.1"
  	versionScheme=$Semver
  >
  ```
  (5 traits → multiline format)
- Alphabetize traits on all child concepts within each schema file

#### 9.6 Fix `schema-document-minimal`

This is a schema **document** test (`data.cdx` IS the schema), not a schema file referenced by another test. Phase 9.5 targets `schema.cdx` files and misses this.

Update both `cases/valid/schema-document-minimal/data.cdx` (input) and `expected/canonical/schema-document-minimal/data.cdx` (expected canonical):

- Add `authoringMode=$SimplifiedMode` (required per §11.3)
- Add `versionScheme=$Semver` (required per §13.3)
- Change `$BackwardCompatible` → `$Initial` (required per §13.5)
- Alphabetize traits (5 traits → multiline format)

Expected canonical:
```cdx
<Schema
	authoringMode=$SimplifiedMode
	compatibilityClass=$Initial
	id=example:schema:minimal
	version="0.1"
	versionScheme=$Semver
/>
```

#### 9.7 Resolve orphaned tests

| Test | Action |
|------|--------|
| `blankline-between-annotations-and-root` | **Move from `cases/invalid/` to `cases/valid/`.** Create expected canonical output. This is a valid general annotation: `[note]` is not attached (blank line separates it from `<Root />`), not grouping (no `GROUP:`/`END:`). Per §8.9.8, general annotations require blank lines above and below; file boundaries count as blank-line boundaries. File start = boundary above, one blank line below before `<Root />`. Valid. |
| `color-mix-single-stop` | Add to manifest (already has input, schema, and expected error file) |
| `range-whitespace` | Add to manifest (already has input and expected canonical) |

#### 9.8 Update manifest

- Add entries for all newly created or orphaned tests
- Verify all existing entries still have correct paths

**File: `SPEC_CHANGE_LOG.md`**

Changelog entry

---

### Phase 10: Tooling and Verification

**File operations:**

1. Move `reorder_canonical_triples.py` from `/Users/guy/Workspace/@paperhat/specifications/obsolete/codex-lang.dev/tools/` into the active `tools/` directory

**Verification checks:**

1. `python3 tools/reorder_canonical_triples.py --dry-run` — 0 out-of-order triples
2. `python3 tools/readiness_check.py` — clean (or only pre-existing changelog keyword flags)
3. Grep: every SHACL NodeShape in canonical bootstrap has `sh:closed` triple
4. Count: trait property shapes in canonical = required + optional per simplified
5. Count: 0 string-literal `rdf:first` values in enum list chains (all IRIs now)
6. Count: 0 `xsd:token` range declarations on enum-valued traits (all `rdfs:Resource` now)
7. Grep: no `MD:` as a directive in conformance suite (note: `MD:` as non-directive annotation content is valid)
8. Grep: `MARKDOWN:` IS present in the valid directive test (replaced correctly)
9. Grep: no schema file missing `versionScheme`
10. Grep: no schema file missing `authoringMode`
11. Grep: no schema file using `$BackwardCompatible`
12. Grep: no `tag` trait references in either bootstrap
13. Grep: no `Cardinality` list chain in either bootstrap
14. Grep: verify `traitPredicateIri` in §9.7.10 has no "has no `id`" dead code case
15. Verify: `schema-document-minimal` has all 5 required traits (`authoringMode`, `compatibilityClass`, `id`, `version`, `versionScheme`)
16. Verify: `blankline-between-annotations-and-root` is in `cases/valid/`, not `cases/invalid/`
17. Grep: no optional whitespace in list literal trait values in spec CDX examples (e.g., no `[$Grams, ` with space after comma)

---

## Files Modified (Summary)

| File | Phases |
|------|--------|
| `spec/1.0.0/index.md` | 1, 2, 3, 4, 5 |
| `spec/1.0.0/bootstrap-schema/schema.cdx` | 6, 7 |
| `spec/1.0.0/bootstrap-schema/simplified/schema.cdx` | 8 |
| `CLAUDE.md` | 1 |
| `SPEC_CHANGE_LOG.md` | 1–9 |
| `conformance/1.0.0/` (multiple) | 9 |
| `tools/reorder_canonical_triples.py` | 10 (move) |
