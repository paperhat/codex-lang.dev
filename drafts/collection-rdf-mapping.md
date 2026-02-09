# Collection-to-RDF Mapping — Draft Spec Edits

## Problem

§9.7.8 line 2991 says: "each element `v` MUST independently produce an IRI via the same rule" for enumerated tokens inside collections. But `valueTerm()` for collections produces a single opaque typed literal (e.g., `"[$A, $B]"^^urn:cdx:value-type:List`), making per-element IRIs impossible.

## Design Choices (from user)

1. **Maps/Records**: Use standard RDF list with entry nodes. Each entry is an RDF list node whose `rdf:first` points to an entry node with two triples (key + value).
2. **Nested collection IRI**: `listNodeIri + "/__value"` for the inner value node when a collection element is itself a collection.
3. **List node IRI pattern**: Use `anchor + "/" + i` — same pattern as §9.6.3.
4. **Replaces typed-literal behavior**: Collection values no longer produce typed literals; they produce structured RDF list graphs.
5. **Vacuous when unconstrained**: Enum tokens without an `EnumeratedValueSet` still fall through to typed literals (per element).
6. **Bootstrap impact**: Scoped to `defaultValueTypes` and `values` traits.

---

## CHANGE 1: §9.7.5 — Add 5 Reserved Predicates

**Current text (lines 2839–2871):**

The list of 14 predicates ending with `codex:annotationTarget`.

**After `codex:annotationTarget` (line 2854), ADD:**

```markdown
- `codex:mapKey`
- `codex:mapValue`
- `codex:rangeStart`
- `codex:rangeEnd`
- `codex:rangeStep`
```

**After the last IRI derivation line (line 2871), ADD:**

```markdown
- `codex:mapKey` MUST be `schemaIri + "#codex/mapKey"`
- `codex:mapValue` MUST be `schemaIri + "#codex/mapValue"`
- `codex:rangeStart` MUST be `schemaIri + "#codex/rangeStart"`
- `codex:rangeEnd` MUST be `schemaIri + "#codex/rangeEnd"`
- `codex:rangeStep` MUST be `schemaIri + "#codex/rangeStep"`
```

Total reserved predicates after change: 19.

---

## CHANGE 2: §9.7.8 — Add Collection Case to `valueTerm(v)`

**Current text (lines 2946–2950):**

```markdown
`valueTerm(v)` MUST be:

- an IRI when `v` is an IRI Reference Value
- an IRI when `v` is an Enumerated Token Value and the governing trait is constrained by an `EnumeratedValueSet` (see below)
- otherwise a typed literal
```

**REPLACE WITH:**

```markdown
`valueTerm(v)` MUST be:

- an IRI when `v` is an IRI Reference Value
- an IRI when `v` is an Enumerated Token Value and the governing trait is constrained by an `EnumeratedValueSet` (see below)
- the collection head IRI of the collection graph (§9.7.8.1) when `v` is a collection value (List, Set, Map, Record, Tuple, or Range)
- otherwise a typed literal
```

Lines 2935–2937 (the trait triple emission rule) stay as-is. The trait triple's object is `valueTerm(v)`, which now returns the list head IRI for collections. The collection graph is emitted as additional triples per §9.7.8.1.

---

## CHANGE 3: §9.7.8 — Scalar Redirect for `valueDatatypeIri` / `valueLex`

**Current text (lines 2958–2978):**

```markdown
`valueDatatypeIri(v)` MUST be:

 `xsd:string` for Text Values
- `xsd:string` for Character Values
- `xsd:boolean` for Boolean Values
- `xsd:integer` for Integer Values

For all other value types, `valueDatatypeIri(v)` MUST be the deterministic URN:

- `urn:cdx:value-type:<T>`

where `<T>` is the Codex value type token name (for example, `Uuid`, `Color`, `Temporal`, `List`, `Map`).

`valueLex(v)` MUST be:

 the decoded Unicode text value for Text Values
 the single Unicode scalar value as Unicode text for Character Values
- `"true"` or `"false"` for Boolean Values
 base-10 integer text for Integer Values

For all other value types, `valueLex(v)` MUST be the canonical surface spelling of `v`.
```

**REPLACE WITH:**

```markdown
`valueDatatypeIri(v)` MUST be:

- `xsd:string` for Text Values
- `xsd:string` for Character Values
- `xsd:boolean` for Boolean Values
- `xsd:integer` for Integer Values

For all other scalar value types, `valueDatatypeIri(v)` MUST be the deterministic URN:

- `urn:cdx:value-type:<T>`

where `<T>` is the Codex value type token name (for example, `Uuid`, `Color`, `Temporal`).

Collection value types (List, Set, Map, Record, Tuple, and Range) are not represented as typed literals. Their mapping is defined in §9.7.8.1.

`valueLex(v)` MUST be:

- the decoded Unicode text value for Text Values
- the single Unicode scalar value as Unicode text for Character Values
- `"true"` or `"false"` for Boolean Values
- base-10 integer text for Integer Values

For all other scalar value types, `valueLex(v)` MUST be the canonical surface spelling of `v`.
```

Changes: "all other value types" → "all other scalar value types" (twice). `List`, `Map` removed from examples. Redirect paragraph added for collections.

---

## CHANGE 4: §9.7.8 — Replace Collection Paragraph with Redirect

**Current text (line 2991):**

```markdown
This rule applies regardless of where the Enumerated Token Value appears in the trait's value structure. If the trait value is a collection (List, Set, Map, Record, Tuple, or Range) whose elements are Enumerated Token Values, each element `v` MUST independently produce an IRI via the same rule.
```

**REPLACE WITH:**

```markdown
This rule applies to scalar trait values. For Enumerated Token Values within collections, see §9.7.8.1.
```

---

## CHANGE 5: New §9.7.8.1 — Collection Value Graphs

**INSERT AFTER line 2997** (end of current §9.7.8), **BEFORE §9.7.9**:

```markdown
##### 9.7.8.1 Collection Value Graphs

When a trait value `v` is a collection (List, Set, Map, Record, Tuple, or Range), `valueTerm(v)` MUST NOT be a typed literal. Instead, the value MUST be represented as a structured collection graph using the standard RDF list vocabulary (`rdf:first`, `rdf:rest`, `rdf:nil`) and reserved Codex predicates.

All collection graph nodes MUST be IRIs. No blank nodes are permitted (§9.6.1).

**List anchor and node IRIs.**

For a trait `t=v` on concept instance `C`, let:

- `traitPredIri = traitPredicateIri(t)`
- `collectionAnchor = nodeIri(C) + "/list/" + iriHash(traitPredIri)`

List node IRIs MUST follow the same pattern as §9.6.3:

- `listNodeIri(collectionAnchor, i) = collectionAnchor + "/" + i`

The list head node is at position 0. `valueTerm(v)` for the trait MUST be `listNodeIri(collectionAnchor, 0)`.

If the collection is empty (zero elements), `valueTerm(v)` MUST be `rdf:nil`.

**Ordered collections (List, Tuple).**

For a List or Tuple with elements `e₀, e₁, …, eₙ₋₁`:

For each position `i` from 0 to n−1, the mapping MUST emit:

- `(listNodeIri(collectionAnchor, i), rdf:first, elementTerm(eᵢ))`
- `(listNodeIri(collectionAnchor, i), rdf:rest, listNodeIri(collectionAnchor, i+1))` — or `rdf:nil` when `i = n−1`

**Unordered collections (Set).**

Sets use the same RDF list encoding as Lists. Element order in the RDF list MUST match canonical source order (§5.14).

**Keyed collections (Map, Record).**

For a Map or Record with entries `(k₀:v₀), (k₁:v₁), …, (kₙ₋₁:vₙ₋₁)`:

For each position `i` from 0 to n−1, let `entryIri = listNodeIri(collectionAnchor, i) + "/__entry"`. The mapping MUST emit:

- `(listNodeIri(collectionAnchor, i), rdf:first, entryIri)`
- `(listNodeIri(collectionAnchor, i), rdf:rest, listNodeIri(collectionAnchor, i+1))` — or `rdf:nil` when `i = n−1`
- `(entryIri, codex:mapKey, elementTerm(kᵢ))`
- `(entryIri, codex:mapValue, elementTerm(vᵢ))`

Entry order in the RDF list MUST match canonical source order.

**Range.**

For a Range `start..end` (with optional step), let the components be `start`, `end`, and (if present) `step`. A Range MUST be encoded as a single RDF resource (not a list). Let `rangeIri = nodeIri(C) + "/range/" + iriHash(traitPredIri)`. The mapping MUST emit:

- `(rangeIri, codex:rangeStart, elementTerm(start))`
- `(rangeIri, codex:rangeEnd, elementTerm(end))`
- If a step is present: `(rangeIri, codex:rangeStep, elementTerm(step))`

`valueTerm(v)` for a Range MUST be `rangeIri`.

**`elementTerm(e)`.**

Each element `e` within a collection MUST be mapped to an RDF term as follows:

- If `e` is an IRI Reference Value, `elementTerm(e)` MUST be the IRI.
- If `e` is an Enumerated Token Value and the governing trait is constrained by an `EnumeratedValueSet` `E`, `elementTerm(e)` MUST be the IRI `E.id + "#" + tokenName(e)`.
- If `e` is a nested collection (List, Set, Map, Record, Tuple, or Range), `elementTerm(e)` MUST be the head IRI of the nested collection's graph. Let `nestedAnchor = listNodeIri(collectionAnchor, i) + "/__value"`, where `i` is the position of the element in the parent collection. For nested List, Set, Map, Record, or Tuple collections, the nested collection anchor is `nestedAnchor` and the list head IRI is `nestedAnchor + "/0"`. For a nested Range, the range IRI is `nestedAnchor` directly. The nested collection graph MUST be emitted following the same rules defined in this section.
- Otherwise, `elementTerm(e)` MUST be the typed literal `valueLex(e)^^valueDatatypeIri(e)`, using the scalar rules defined in §9.7.8.

This rule replaces the typed-literal representation for collection values. A collection value on a trait MUST always produce a collection graph; it MUST NOT produce a typed literal.
```

---

## Summary of All Spec Edits

| # | Location | Nature |
|---|----------|--------|
| 1 | §9.7.5 (lines 2854, 2871) | Add 5 reserved predicates + IRI derivations |
| 2 | §9.7.8 (lines 2946–2950) | Add collection case to `valueTerm(v)` |
| 3 | §9.7.8 (lines 2958–2978) | "all other value types" → "all other scalar value types" + redirect |
| 4 | §9.7.8 (line 2991) | Replace paragraph — redirect to §9.7.8.1 |
| 5 | New §9.7.8.1 (after line 2997) | Full collection graph encoding subsection |
