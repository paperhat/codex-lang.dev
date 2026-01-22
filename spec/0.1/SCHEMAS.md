# Codex 0.1 — Schema Layers and SHACL Projection

Status: NON-NORMATIVE (Historical; migrated)

This document is retained for historical context and as a migration record.

All requirement keywords (MUST/MUST NOT/MAY) in this document are historical and are not normative for Codex 0.1.

The normative definition of schema-driven validation projection, including the total Layer A → Layer B expansion algorithm and SHACL-SPARQL rule algebra mapping, is now in:

- [codex-language-specification.md](codex-language-specification.md) (§9)

---

## 1. Goals

The schema system MUST support:

1. **Layer A (human authoring)**: a small, Codex-native schema vocabulary that covers “nearly everything most people want”.
2. **Layer B (full expression)**: complete expression power for SHACL (and by extension RDF-graph-shaped authoring), with no loss of capability.
3. **Single projection**: there is exactly one normative algorithmic projection from Codex schemas to a SHACL graph.
4. **Guardrails**: there is exactly one canonical way to say the same thing in each layer.
5. **No nondeterminism**: any ambiguity MUST produce an error.
6. **Canonicalization**: derived artifacts are canonical, deterministic, and reproducible.

This document also MUST avoid guessing:

- If a mapping depends on semantics not defined by the Codex language specification or schema-definition specification, the mapping MUST fail rather than invent semantics.

---

## 2. Key Idea: Aliasing is Possible (But the Types Differ)

Layer A and Layer B MAY be conceptually “aliased” by defining Layer A as *the authoritative schema authoring vocabulary* and Layer B as *the canonical, fully general SHACL/RDF representation*.

However, there is a mismatch that MUST be made explicit:

- A Codex `ConceptDefinition` describes a **Codex Concept**.
- A SHACL `sh:NodeShape` describes constraints over an **RDF node**.

Therefore, Layer A cannot literally be “the same thing” as SHACL.

Instead:

- Each Layer A `ConceptDefinition` MUST expand into exactly one Layer B node representing a `sh:NodeShape`.
- Each Layer A trait/child/constraint rule MUST expand into Layer B structures that are semantically equivalent under the chosen Codex→RDF instance mapping.

In other words: choosing `<ConceptDefinition …>` in Layer A is choosing the *source* for a derived `<NodeShape …>` in Layer B.

---

## 3. Authoring Profiles (Guardrail)

A schema document MUST be validated under exactly one authoring profile:

- **Profile A**: Layer A only.
- **Profile B**: Layer B only.

A schema document MUST NOT mix profiles.

Rationale: mixing introduces multiple ways to say the same thing and makes canonicalization ambiguous.

The authoring profile MUST be selected by an explicit declaration in the schema document.

The schema document's root `Schema` concept MUST have an `authoringProfile` trait.

`authoringProfile` MUST be exactly one of:

- `$ProfileA`
- `$ProfileB`

If `authoringProfile` is missing or has any other value, schema processing MUST fail.

---

## 4. Layer A (Codex-Native Schema Authoring)

Layer A is the existing schema-definition vocabulary (Schema / ConceptDefinition / TraitDefinition / …) as authored in Codex.

Layer A MUST remain:

- closed-world,
- deterministic,
- explainable (every derived constraint must cite its source rule),
- and independent of SHACL surface details.

Layer A is authoritative for Codex schema semantics.

### 4.1 Layer A Extensions Required For Total SHACL Projection

The following Layer A extensions are required for a total, deterministic SHACL projection.

#### 4.1.1 Pattern Flags

The following atomic constraints MUST support an optional `flags` string trait:

- `ValueMatchesPattern`
- `PatternConstraint`
- `ContentMatchesPattern`

If `flags` is omitted, it MUST be treated as the empty string.

The `pattern` and `flags` semantics MUST be SPARQL 1.1 `REGEX` semantics.

#### 4.1.2 Explicit Validator Definitions

Layer A MUST support explicit validator definitions that make `ValueIsValid` deterministic.

`ValidatorDefinitions` is a container concept.

`ValidatorDefinition` defines one validator.

`ValidatorDefinition` MUST have these traits:

- `name` (required; enumerated token)
- `message` (optional; string)

`ValidatorDefinition` MUST be in content mode.

The content of `ValidatorDefinition` MUST be a SPARQL fragment that is embedded into the derived `sh:sparql` constraint.

The embedding mechanism is defined in §8.6.4.

#### 4.1.3 Path and Quantifier Rule Forms

The schema-definition specification defines paths (`TraitPath`, `ChildPath`, `DescendantPath`, `ContentPath`) and quantifiers (`Exists`, `ForAll`, `Count`) but does not, by itself, define a concrete rule-node form that composes them with rules.

To produce a total, deterministic mapping, Layer A MUST include explicit rule-node forms that bind a path and scope a nested rule.

Layer A MUST provide the following rule nodes:

- `OnPathExists`
- `OnPathForAll`
- `OnPathCount`

Each of these MUST have exactly one `Path` child and exactly one `Rule` child.

`OnPathCount` MUST additionally have:

- `minCount` (optional; non-negative integer)
- `maxCount` (optional; positive integer)

The `Path` child MUST be exactly one of:

- `TraitPath`
- `ChildPath`
- `DescendantPath`
- `ContentPath`

The semantics of these nodes are defined in §8.6.7.

#### 4.1.4 Collection and Order Constraint Scoping

The schema-definition specification defines collection and order constraints, but it does not define a deterministic “collection membership selector” for those constraints.

To make projection total and deterministic, Layer A MUST extend the following constraint nodes to explicitly specify the collection members they apply to.

For each of the following constraints:

- `CollectionOrdering`
- `CollectionAllowsEmpty`
- `CollectionAllowsDuplicates`
- `MemberCount`
- `EachMemberSatisfies`
- `OrderConstraint`

the constraint node MUST have exactly one `Path` child, called the *collection member path*.

The member path MUST be exactly one of:

- `ChildPath`
- `DescendantPath`

If the path is not one of these, expansion MUST fail.

For `EachMemberSatisfies`, the constraint node MUST continue to have exactly one `Rule` child, and that `Rule` MUST be evaluated with `focusVar` bound to each member selected by the member path.

For `CollectionAllowsDuplicates`:

- If `allowed=true`, the constraint MUST NOT impose any condition.
- If `allowed=false`, the constraint MUST include an additional required trait `keyTrait` whose value is a trait name string.

The `keyTrait` trait defines the value used for duplicate detection.

If `keyTrait` is `id`, it MUST refer to the declared identifier (`codex:declaredId`) as defined in §6.1.2.

If `keyTrait` is not `id` and cannot be resolved to exactly one `TraitDefinition`, expansion MUST fail.

Example (Informative):

This example uses `keyTrait="id"`, which keys duplicate detection on `codex:declaredId`.

```cdx
<ConstraintDefinition
	id=example:constraint:ingredients-collection
	title="Ingredients collection rules"
>
	<Targets>
		<TargetConcept conceptSelector="Ingredients" />
	</Targets>
	<Rule>
		<AllOf>
			<CollectionAllowsEmpty allowed=false>
				<Path>
					<ChildPath conceptSelector="Ingredient" />
				</Path>
			</CollectionAllowsEmpty>

			<MemberCount min=1 max=200>
				<Path>
					<ChildPath conceptSelector="Ingredient" />
				</Path>
			</MemberCount>

			<EachMemberSatisfies>
				<Path>
					<ChildPath conceptSelector="Ingredient" />
				</Path>
				<Rule>
					<IdentityConstraint type="MustBeEntity" />
				</Rule>
			</EachMemberSatisfies>

			<CollectionAllowsDuplicates allowed=false keyTrait="id">
				<Path>
					<ChildPath conceptSelector="Ingredient" />
				</Path>
			</CollectionAllowsDuplicates>

			<OrderConstraint type="VariadicMustBeLast">
				<Path>
					<ChildPath conceptSelector="Ingredient" />
				</Path>
			</OrderConstraint>
		</AllOf>
	</Rule>
</ConstraintDefinition>
```

---

## 5. Layer B (Canonical SHACL Graph Authoring)

Layer B is a canonical RDF-graph representation specialized for SHACL.

### 5.1 Design Constraint: No Blank Nodes

Layer B MUST NOT require RDF blank nodes.

All RDF nodes in Layer B MUST be IRIs.

Rationale: Codex already has IRI reference values as a primitive, and forbidding blank nodes eliminates non-canonical representations.

Where SHACL commonly uses blank nodes (e.g., `sh:property` values, RDF lists), Layer B MUST use deterministically derived **skolem IRIs** instead.

### 5.2 Layer B Surface Vocabulary (Minimal)

Layer B is expressed as a single Codex graph concept:

- `RdfGraph` — container for triples.

And one triple concept:

- `RdfTriple` — a single RDF triple.

This minimality is deliberate: it guarantees full SHACL coverage because SHACL is an RDF vocabulary.

Layer B MUST be able to represent any SHACL graph, including SHACL-SPARQL constraints.

#### 5.2.1 `RdfGraph`

- `RdfGraph` MUST be in children mode.
- Children MUST be one or more `RdfTriple`.

#### 5.2.2 `RdfTriple`

`RdfTriple` MUST have these traits:

- `s` (required; IRI reference) — subject
- `p` (required; IRI reference) — predicate

And exactly one of:

- `o` (required; IRI reference) — object IRI
- `lex` (required; string) — object literal lexical form

If `lex` is present, `RdfTriple` MAY have:

- `datatype` (optional; IRI reference) — RDF datatype IRI
- `language` (optional; string) — RDF language tag

The following MUST hold:

- If `language` is present, `datatype` MUST be absent.
- If `datatype` is absent and `language` is absent, the literal datatype is `xsd:string`.

### 5.3 Layer B Canonical Form

In canonical Layer B:

- `RdfTriple` children MUST be sorted in ascending lexicographic order of `(s, p, oKey)`.
- `oKey` MUST be:
	- `o` when object is an IRI, and
	- the pair `(datatypeOrDefault, lex)` when object is a literal.

If two triples are identical after this normalization, duplicates MUST be removed.

### 5.4 Layer B Required Prefix IRIs (Informal)

The SHACL projection examples in this document use the following well-known IRIs:

- `rdf:type`
- `rdfs:Class`
- `xsd:string`, `xsd:integer`, `xsd:boolean`
- `sh:NodeShape`, `sh:PropertyShape`, `sh:targetClass`, `sh:property`, `sh:path`
- `sh:minCount`, `sh:maxCount`, `sh:datatype`, `sh:class`, `sh:pattern`, `sh:flags`
- `sh:sparql`, `sh:message`, `sh:select`

This document does not define namespace prefixes; Layer B uses IRIs directly.

---

## 6. Codex Instance Graph Mapping (Prerequisite)

The Layer A → SHACL projection depends on a deterministic mapping from Codex instance documents to an RDF graph.

This document defines a minimal mapping sufficient for SHACL validation.

The mapping takes two required inputs:

- `documentBaseIri` (IRI reference)
- `schemaIri` (IRI reference)

### 6.1 Node Identity

For any Codex Concept instance `C`:

- The RDF node IRI MUST be a deterministic skolem IRI derived from `documentBaseIri` and the instance's structural position.

The node IRI MUST NOT be derived from the `id` trait value.

Rationale: using `id` as the RDF node IRI collapses duplicate identifiers into a single RDF node, which makes document-wide identifier uniqueness and some resolution constraints uncheckable.

The skolem IRI derivation MUST be stable and unambiguous.

A conforming derivation MUST:

- use only IRI-safe characters,
- include `documentBaseIri` as a prefix,
- include the structural path (concept names + ordinal positions among siblings),
- and be injective (no collisions within a document).

### 6.1.2 Declared Identifier

If a concept instance has an `id` trait, the mapping MUST emit:

- `(nodeIri(C), codex:declaredId, C.id)`

`codex:declaredId` MUST be `schemaIri + "#codex/declaredId"`.

### 6.1.1 Document Node

The RDF node for the Document context MUST be `documentBaseIri`.

If `documentBaseIri` is not provided, any constraint targeting `TargetContext contextSelector="Document"` MUST fail mapping.

### 6.2 RDF Types

Each Codex Concept instance MUST emit:

- `(nodeIri, rdf:type, conceptClassIri)`

The `conceptClassIri` for a concept name `X` MUST be derived as defined in §7.2.

### 6.2.1 Parent Links

For each parent-child relationship, the mapping MUST also emit a direct parent link:

- `(nodeIri(D), codex:parentNode, nodeIri(C))`

This predicate IRI MUST be deterministically derived from `schemaIri`:

- `codex:parentNode` MUST be `schemaIri + "#codex/parentNode"`.

### 6.2.2 Entity Marker

To support identity constraints without guessing, the mapping MUST emit an entity marker:

- If the concept instance has an `id` trait, emit `(nodeIri(C), codex:isEntity, "true"^^xsd:boolean)`.
- Otherwise, emit `(nodeIri(C), codex:isEntity, "false"^^xsd:boolean)`.

`codex:isEntity` MUST be `schemaIri + "#codex/isEntity"`.

### 6.3 Traits

For each trait `t=v` on concept instance `C`, the instance graph MUST emit exactly one triple:

- `(nodeIri(C), traitPredicateIri(t), valueTerm(v))`

Exception:

- If `t` is `id`, the mapping MUST NOT emit a `traitPredicateIri("id")` triple.
- Instead, `id` MUST be represented only by `codex:declaredId` as defined in §6.1.2.

`valueTerm(v)` MUST be:

- an IRI when `v` is an IRI Reference Value,
- otherwise a typed literal.

The typed literal's datatype IRI MUST be computed by `valueDatatypeIri(v)`.

The typed literal's lexical form MUST be computed by `valueLex(v)`.

Both `valueDatatypeIri(v)` and `valueLex(v)` MUST be derived by parsing `v` according to the Codex language specification's value catalog.

#### 6.3.1 `valueDatatypeIri(v)`

`valueDatatypeIri(v)` MUST be:

- `xsd:string` for String Values
- `xsd:string` for Character Values
- `xsd:boolean` for Boolean Values
- `xsd:integer` for Integer Values

For all other value types, `valueDatatypeIri(v)` MUST be a deterministic URN:

- `urn:cdx:value-type:<T>`

where `<T>` is the Codex value type token name without the leading `$` (e.g., `Uuid`, `Color`, `Temporal`, `List`, `Map`).

#### 6.3.2 `valueLex(v)`

`valueLex(v)` MUST be:

- the decoded Unicode string value for String Values
- the single Unicode scalar value as a Unicode string for Character Values
- `"true"` or `"false"` for Boolean Values
- a base-10 integer string for Integer Values

For all other value types, `valueLex(v)` MUST be the canonical surface spelling of `v`.

This rule intentionally avoids guessing semantic normalizations for complex values.

#### 6.3.3 Lookup Tokens

Lookup Token Values MUST be represented as typed literals:

- datatype: `urn:cdx:value-type:LookupToken`
- lexical form: the canonical surface spelling (e.g., `~myToken`)

If a schema constraint requires the interpreted value (e.g., numeric comparisons, string length), the mapping MUST either:

- provide the interpreted value in a deterministic RDF representation, or
- fail mapping.

This document provides interpreted values only where explicitly defined in §8.6.

If a schema constraint requires lookup token *resolution* (mapping a token to an IRI), the mapping MUST use the binding table defined in §6.7.

### 6.4 Children

For each child concept instance `D` of parent concept instance `C`, the instance graph MUST emit:

- `(nodeIri(C), childPredicateIri(C,D), nodeIri(D))`

If child order matters under the schema, the instance graph MUST also emit a deterministic order encoding.

The canonical order encoding is defined in §6.5.

If an ordered view is required, the instance graph MUST use §6.5.

### 6.6 Content

If a concept instance is in content mode, the mapping MUST emit:

- `(nodeIri(C), codex:content, contentString)`

`contentString` MUST be an `xsd:string` literal containing the concept's content after applying the Codex content escaping rules.

`codex:content` MUST be `schemaIri + "#codex/content"`.

### 6.7 Lookup Binding Table (Deterministic)

This section defines the explicit lookup binding mechanism (3.A).

The instance mapping MAY incorporate a lookup binding table.

Each binding entry associates a Lookup Token Value with a single IRI.

Binding entries MUST be represented in the instance graph using the reserved predicates:

- `codex:lookupToken` (object MUST be a Lookup Token typed literal)
- `codex:lookupIri` (object MUST be an IRI)

The mapping MUST accept bindings from any source that is explicit and deterministic.

One conforming source is: a document-level section that is parsed into a list of bindings in source order.

For each binding entry at ordinal position `i`, the mapping MUST emit a binding node `b` and two triples:

- `(b, codex:lookupToken, tokenLiteral)`
- `(b, codex:lookupIri, targetIri)`

The binding node IRI MUST be deterministic and injective within a document.

One conforming derivation is:

- `b = documentBaseIri + "/__lookupBinding/" + i`

Additional binding table well-formedness rules:

- If two binding entries have the same `tokenLiteral`, instance mapping MUST fail.
- If any binding entry lacks either `tokenLiteral` or `targetIri`, instance mapping MUST fail.
- If any binding entry provides multiple `targetIri` values for the same `tokenLiteral`, instance mapping MUST fail.

### 6.5 Ordered Children Encoding (Deterministic)

This section defines the canonical order encoding used when an ordered view is required.

This encoding is not a linked list.

Instead, it is an index-annotated edge model that is easy to validate and canonicalize.

For each parent `C` and each direct child `D` in children order, let:

- `p = nodeIri(C)`
- `d = nodeIri(D)`
- `i = 0..n-1` (the ordinal position among direct children, in source order)

The mapping MUST emit the structural child triple as already defined in §6.4.

Additionally, when an ordered view is required, the mapping MUST emit an *edge node* `e` and three triples:

- `(e, codex:parent, p)`
- `(e, codex:child, d)`
- `(e, codex:index, "i"^^xsd:integer)`

The edge node IRI MUST be deterministic and injective.

One conforming derivation is:

- `e = p + "/__childEdge/" + i`

If multiple independent ordered views are needed, the derivation MUST incorporate a view key.

---

## 7. Deterministic IRI Derivation

To keep “one way to say it”, every derived IRI MUST be computed by a single algorithm.

### 7.1 Schema IRI

Let `schemaIri` be the `Schema.id` value.

### 7.2 Concept Class IRIs

For each `ConceptDefinition`:

- `conceptClassIri` MUST be the concept definition `id`.

### 7.3 Shape IRIs

For each `ConceptDefinition` with class IRI `K`:

- `nodeShapeIri(K)` MUST be `K + "#shape"`.

### 7.4 Trait Predicate IRIs

For each `TraitDefinition`:

- If the trait definition has an `id`, `traitPredicateIri` MUST be that `id`.
- Otherwise, `traitPredicateIri(name)` MUST be `schemaIri + "#trait/" + name`.

### 7.5 Child Predicate IRIs

Let parent class IRI be `P` and child class IRI be `Q`.

- `childPredicateIri(P,Q)` MUST be `P + "#child/" + percentEncode(Q)`.

`percentEncode` MUST be RFC 3987 percent-encoding over the Unicode string form.

### 7.6 Codex Reserved Predicates

The following reserved predicates are used by the instance mapping and SHACL projection:

- `codex:parent`
- `codex:child`
- `codex:index`
- `codex:parentNode`
- `codex:isEntity`
- `codex:declaredId`
- `codex:lookupToken`
- `codex:lookupIri`
- `codex:content`

Their IRIs MUST be deterministically derived from `schemaIri`:

- `codex:parent` MUST be `schemaIri + "#codex/parent"`
- `codex:child` MUST be `schemaIri + "#codex/child"`
- `codex:index` MUST be `schemaIri + "#codex/index"`
- `codex:parentNode` MUST be `schemaIri + "#codex/parentNode"`
- `codex:isEntity` MUST be `schemaIri + "#codex/isEntity"`
- `codex:declaredId` MUST be `schemaIri + "#codex/declaredId"`
- `codex:lookupToken` MUST be `schemaIri + "#codex/lookupToken"`
- `codex:lookupIri` MUST be `schemaIri + "#codex/lookupIri"`
- `codex:content` MUST be `schemaIri + "#codex/content"`

---

## 8. Layer A → Layer B Expansion Algorithm

Input: a Layer A schema document `S`.

Output: a Layer B `RdfGraph` containing a SHACL graph.

### 8.1 Preconditions

The expansion MUST fail if any of the following hold:

- The schema is not valid under the schema-of-schemas.
- Any `ConceptDefinition` lacks an `id`.
- Any required selector (concept name, trait name) cannot be resolved to a unique definition.
- Any rule produces a semantic constraint that cannot be expressed under the chosen instance graph mapping.

### 8.2 Expansion Steps

1. Compute `schemaIri` (§7.1).
2. For each `ConceptDefinition`, compute:
	- `conceptClassIri` (§7.2)
	- `shapeIri` (§7.3)
3. Emit SHACL node shape triples:
	- `(shapeIri, rdf:type, sh:NodeShape)`
	- `(shapeIri, sh:targetClass, conceptClassIri)`
4. Expand TraitRules into property shapes.
5. Expand ChildRules into property shapes.
6. Expand ConstraintDefinitions into SHACL constraints.
7. Canonicalize the resulting `RdfGraph` (§5.3).

### 8.3 Property Shape IRIs

A property shape MUST have a deterministic IRI.

For a node shape `S` and a trait name `t`:

- `propertyShapeIri(S,t)` MUST be `S + "/property/trait/" + t`.

For a node shape `S` and a child class IRI `Q`:

- `propertyShapeIri(S,Q)` MUST be `S + "/property/child/" + percentEncode(Q)`.

### 8.4 TraitRules → SHACL

For each trait rule on a concept definition, emit a property shape `PS`:

- `(shapeIri, sh:property, PS)`
- `(PS, rdf:type, sh:PropertyShape)`
- `(PS, sh:path, traitPredicateIri(traitName))`

Cardinality mapping:

- `RequiresTrait` MUST emit `(PS, sh:minCount, "1"^^xsd:integer)`.
- `ForbidsTrait` MUST emit `(PS, sh:maxCount, "0"^^xsd:integer)`.

Value type mapping:

- If Layer A declares a value type token that maps to an RDF datatype IRI, the expansion MUST emit `(PS, sh:datatype, datatypeIri)`.
- If Layer A constrains by enumerated set, the expansion MUST emit `(PS, sh:in, listNodeIri)` and emit the RDF list structure using skolem IRIs.

Any value-type token without a defined mapping MUST cause expansion failure.

### 8.5 ChildRules → SHACL

For each allowed/required/forbidden child relationship, emit a property shape `PS`:

- `(shapeIri, sh:property, PS)`
- `(PS, rdf:type, sh:PropertyShape)`
- `(PS, sh:path, childPredicateIri(parentClassIri, childClassIri))`

Child presence mapping:

- `RequiresChildConcept` MUST emit `(PS, sh:minCount, "1"^^xsd:integer)`.
- `ForbidsChildConcept` MUST emit `(PS, sh:maxCount, "0"^^xsd:integer)`.

If Layer A restricts child type, the expansion MUST emit `(PS, sh:class, childClassIri)`.

### 8.6 ConstraintDefinitions → SHACL

ConstraintDefinitions MUST expand to SHACL constraints.

#### 8.6.1 General Rule

Each Codex constraint type permitted by the schema-definition specification MUST map to either:

- a SHACL Core constraint expression, or
- a SHACL-SPARQL constraint (`sh:sparql`).

If a constraint type cannot be expressed without inventing semantics not defined by the source specifications, expansion MUST fail.

#### 8.6.5 Atomic Constraint Mapping (Where Total Today)

This section defines mappings that do not depend on the unfinished path/quantifier model.

All mappings below apply to the set of targets declared by the `Targets` element.

##### 8.6.5.1 Targets

- For `TargetConcept conceptSelector="X"`, the constraint MUST be applied to the node shape derived from the `ConceptDefinition` whose `name` is `X`.
- For `TargetContext contextSelector="Document"`, the constraint MUST be applied to a special node shape `schemaIri + "#shape/Document"` that targets the document node:
	- `(schemaIri + "#shape/Document", rdf:type, sh:NodeShape)`
	- `(schemaIri + "#shape/Document", sh:targetNode, documentBaseIri)`

If `contextSelector` is a concept name (not `Document`), the constraint MUST be applied to the shape for that concept.

##### 8.6.5.2 Trait Constraints

`TraitExists(trait=t)` MUST map to a property shape:

- `(PS, sh:path, traitPredicateIri(t))`
- `(PS, sh:minCount, "1"^^xsd:integer)`

`TraitMissing(trait=t)` MUST map to:

- `(PS, sh:path, traitPredicateIri(t))`
- `(PS, sh:maxCount, "0"^^xsd:integer)`

`TraitEquals(trait=t, value=v)` MUST map to:

- `(PS, sh:path, traitPredicateIri(t))`
- `(PS, sh:hasValue, valueTerm(v))`

`TraitCardinality(trait=t, min=m?, max=n?)` MUST map to:

- `(PS, sh:path, traitPredicateIri(t))`
- `(PS, sh:minCount, "m"^^xsd:integer)` when `min` is present
- `(PS, sh:maxCount, "n"^^xsd:integer)` when `max` is present

`TraitValueType(trait=t, valueType=$T)` MUST map to:

- `(PS, sh:path, traitPredicateIri(t))`

and then:

- if `$T` is `$IriReference`, emit `(PS, sh:nodeKind, sh:IRI)`
- otherwise emit `(PS, sh:datatype, datatypeIri($T))`

where `datatypeIri($T)` MUST be:

- `xsd:string` for `$String` and `$Char`
- `xsd:boolean` for `$Boolean`
- `xsd:integer` for `$Integer`
- `urn:cdx:value-type:<T>` for all other `$T`.

##### 8.6.5.3 Value Constraints

`ValueIsOneOf(values=[...])` MUST map to:

- `(PS, sh:in, listHeadIri)`

The list MUST be encoded as an RDF list using skolem IRIs (no blank nodes).

`ValueMatchesPattern(pattern=p, flags=f?)` MUST map to:

- `(PS, sh:pattern, p)`
- `(PS, sh:flags, f)` when `flags` is present and non-empty

`ValueLength(min=a?, max=b?)` MUST map to:

- `(PS, sh:minLength, "a"^^xsd:integer)` when present
- `(PS, sh:maxLength, "b"^^xsd:integer)` when present

`ValueInNumericRange(min=u?, max=v?)` MUST map to SHACL Core numeric bounds only when the active value datatype is one of:

- `xsd:integer`

If the active datatype is not `xsd:integer`, expansion MUST fail.

When permitted:

- `(PS, sh:minInclusive, "u"^^xsd:integer)` when present
- `(PS, sh:maxInclusive, "v"^^xsd:integer)` when present

`ValueIsNonEmpty` MUST map to:

- `(PS, sh:minLength, "1"^^xsd:integer)`

`PatternConstraint(trait=t, pattern=p, flags=f?)` MUST map to:

- `(PS, sh:path, traitPredicateIri(t))`
- `(PS, sh:pattern, p)`
- `(PS, sh:flags, f)` when `flags` is present and non-empty

##### 8.6.5.4 Child Constraints

`ChildConstraint(type=RequiresChildConcept, conceptSelector=X)` MUST map to:

- `(PS, sh:path, childPredicateIri(parentClassIri, childClassIri(X)))`
- `(PS, sh:minCount, "1"^^xsd:integer)`
- `(PS, sh:class, childClassIri(X))`

`ChildConstraint(type=ForbidsChildConcept, conceptSelector=X)` MUST map to:

- `(PS, sh:path, childPredicateIri(parentClassIri, childClassIri(X)))`
- `(PS, sh:maxCount, "0"^^xsd:integer)`

If `type=AllowsChildConcept`, the expansion MUST NOT emit a constraint.

##### 8.6.5.5 Content Constraints

`ContentRequired` MUST map to:

- `(PS, sh:path, codex:content)`
- `(PS, sh:minLength, "1"^^xsd:integer)`

`ContentMatchesPattern(pattern=p, flags=f?)` MUST map to:

- `(PS, sh:path, codex:content)`
- `(PS, sh:pattern, p)`
- `(PS, sh:flags, f)` when `flags` is present and non-empty

`ContentForbiddenUnlessAllowed` depends on schema content-mode semantics and is not specified here.

##### 8.6.5.6 Identity Constraints

`IdentityConstraint(type=MustBeEntity)` MUST map to:

- `(PS, sh:path, codex:isEntity)`
- `(PS, sh:hasValue, "true"^^xsd:boolean)`

`IdentityConstraint(type=MustNotBeEntity)` MUST map to:

- `(PS, sh:path, codex:isEntity)`
- `(PS, sh:hasValue, "false"^^xsd:boolean)`

Other identity constraint types depend on scope/path rules and are not specified here.

##### 8.6.5.7 Custom Validation

`ValueIsValid` MUST map via §8.6.4.

##### 8.6.5.8 ChildSatisfies

`ChildSatisfies(conceptSelector=X, Rule=R)` MUST be interpreted as: every direct child Concept instance of type `X` MUST satisfy `R`.

This semantics MUST be equivalent to:

- `OnPathForAll(Path=ChildPath(X), Rule=R)`

##### 8.6.5.9 Uniqueness Constraints

This section defines two uniqueness constraints:

- `UniqueConstraint(trait=t, scope=S)` (nearest-scope uniqueness)
- `UniqueInDocument(trait=t)` (document-wide uniqueness)

**Nearest-scope uniqueness**

`UniqueConstraint(trait=t, scope=S)` MUST mean:

- within the nearest ancestor (including self) of concept type `S`, no two nodes may share the same value for trait `t`.

For purposes of this constraint, the nearest scope node is the unique node `?scopeK` such that:

- `focusVar <codex:parentNode>* ?scopeK`
- `?scopeK rdf:type <conceptClassIri(S)>`
- and there is no other node `?midK` where:
	- `focusVar <codex:parentNode>* ?midK`
	- `?midK rdf:type <conceptClassIri(S)>`
	- `?midK <codex:parentNode>+ ?scopeK`
	- `?midK != ?scopeK`

Expansion MUST fail if no nearest scope node exists.

One conforming SHACL-SPARQL violation query is:

```
SELECT DISTINCT ?this
WHERE {
	<TARGET_BINDING>
	?this <traitPredicateIri(t)> ?vK .
	# bind nearest scope for ?this
	?this <codex:parentNode>* ?scopeK .
	?scopeK rdf:type <conceptClassIri(S)> .
	FILTER NOT EXISTS {
		?this <codex:parentNode>* ?midK .
		?midK rdf:type <conceptClassIri(S)> .
		?midK <codex:parentNode>+ ?scopeK .
		FILTER( ?midK != ?scopeK )
	}
	# find a distinct other node in the same nearest scope with the same value
	FILTER EXISTS {
		?otherK <traitPredicateIri(t)> ?vK .
		FILTER( ?otherK != ?this )
		?otherK <codex:parentNode>* ?otherScopeK .
		?otherScopeK rdf:type <conceptClassIri(S)> .
		FILTER NOT EXISTS {
			?otherK <codex:parentNode>* ?otherMidK .
			?otherMidK rdf:type <conceptClassIri(S)> .
			?otherMidK <codex:parentNode>+ ?otherScopeK .
			FILTER( ?otherMidK != ?otherScopeK )
		}
		FILTER( ?otherScopeK = ?scopeK )
	}
}
```

**Document-wide uniqueness**

`UniqueInDocument(trait=t)` MUST mean:

- no two nodes in the Document may share the same value for trait `t`.

One conforming SHACL-SPARQL violation query is:

```
SELECT DISTINCT ?this
WHERE {
	<TARGET_BINDING>
	?this <traitPredicateIri(t)> ?vK .
	FILTER EXISTS {
		?otherK <traitPredicateIri(t)> ?vK .
		FILTER( ?otherK != ?this )
	}
}
```

##### 8.6.5.10 Context Constraints

Context constraints are expressible using the deterministic parent links in §6.2.1.

`ContextConstraint(type=OnlyValidUnderParent, contextSelector=P)` MUST map to SHACL-SPARQL:

- Violation when the focus node has a direct parent that is not of type `P`, or has no parent.

One conforming query body for `H` is:

```
EXISTS {
	focusVar <codex:parentNode> ?pK .
	?pK rdf:type <conceptClassIri(P)> .
}
```

`ContextConstraint(type=OnlyValidUnderContext, contextSelector=A)` MUST map to SHACL-SPARQL:

- Violation when the focus node has no ancestor (via one or more parent links) of type `A`.

One conforming `H` is:

```
EXISTS {
	focusVar <codex:parentNode>+ ?aK .
	?aK rdf:type <conceptClassIri(A)> .
}
```

##### 8.6.5.11 Reference Constraints

Reference constraints are expressible without external resolution if identifiers are represented by `codex:declaredId` (see §6.1.2).

Reference constraints that accept lookup tokens MUST resolve them using the lookup binding table (§6.7).

Let `refPreds` be the set of reference-trait predicates:

- `traitPredicateIri("reference")`
- `traitPredicateIri("target")`
- `traitPredicateIri("for")`

If a schema uses different reference trait names, expansion MUST fail.

`ReferenceConstraint(type=ReferenceSingleton)` MUST map to SHACL-SPARQL:

- Violation when more than one reference trait predicate is present on the same focus node.

One conforming `H` uses a count:

```
(
	SELECT (COUNT(?pK) AS ?countK)
	WHERE {
		VALUES ?pK { <traitPredicateIri("reference")> <traitPredicateIri("target")> <traitPredicateIri("for")> }
		focusVar ?pK ?oK .
	}
)
&& (?countK <= 1)
```

`ReferenceConstraint(type=ReferenceTraitAllowed)` is underspecified because it does not, in the schema-definition vocabulary, specify *which* reference trait is allowed.

Therefore:

- Expansion MUST fail for `ReferenceTraitAllowed` unless the constraint provides an additional trait `traitName` whose value is one of `reference | target | for`.

With that extension, a conforming mapping is:

- forbid the other two predicates using `sh:maxCount 0` property shapes or SPARQL boolean checks.

`ReferenceConstraint(type=ReferenceTargetsEntity)` MUST map to:

- For each reference trait value `?vK`, compute a resolved IRI `?rK` as:
	- if `?vK` is an IRI, then `?rK = ?vK`.
	- if `?vK` is a Lookup Token typed literal, then there MUST exist exactly one binding node `?bK` such that:
		- `?bK <codex:lookupToken> ?vK`, and
		- `?bK <codex:lookupIri> ?rK`.

Then require that there exists a node `?nK` such that:
	- `?nK <codex:declaredId> ?rK`, and
	- `?nK <codex:isEntity> "true"^^xsd:boolean`.

One conforming `H` is:

```
!EXISTS {
	VALUES ?pK { <traitPredicateIri("reference")> <traitPredicateIri("target")> <traitPredicateIri("for")> }
	focusVar ?pK ?vK .

	# Resolve IRIs directly
	{
		FILTER(isIRI(?vK))
		BIND(?vK AS ?rK)
	}
	UNION
	# Resolve lookup tokens via explicit bindings
	{
		FILTER(isLiteral(?vK) && DATATYPE(?vK) = <urn:cdx:value-type:LookupToken>)
		FILTER(
			(
				SELECT (COUNT(DISTINCT ?iri2) AS ?c2)
				WHERE {
					?b2 <codex:lookupToken> ?vK .
					?b2 <codex:lookupIri> ?iri2 .
				}
			) = 1
		)
		?bK <codex:lookupToken> ?vK .
		?bK <codex:lookupIri> ?rK .
	}

	FILTER( !EXISTS {
		?nK <codex:declaredId> ?rK .
		?nK <codex:isEntity> "true"^^xsd:boolean
	} )
}
```

`ReferenceConstraint(type=ReferenceTargetsConcept, conceptSelector=X)` MUST map to:

- For each reference trait value `?vK`, compute a resolved IRI `?rK` using the same resolution rule as `ReferenceTargetsEntity`.

Then require that there exists a node `?nK` such that:
	- `?nK <codex:declaredId> ?rK`, and
	- `?nK rdf:type <conceptClassIri(X)>`.

One conforming `H` is:

```
!EXISTS {
	VALUES ?pK { <traitPredicateIri("reference")> <traitPredicateIri("target")> <traitPredicateIri("for")> }
	focusVar ?pK ?vK .

	# Resolve IRIs directly
	{
		FILTER(isIRI(?vK))
		BIND(?vK AS ?rK)
	}
	UNION
	# Resolve lookup tokens via explicit bindings
	{
		FILTER(isLiteral(?vK) && DATATYPE(?vK) = <urn:cdx:value-type:LookupToken>)
		FILTER(
			(
				SELECT (COUNT(DISTINCT ?iri2) AS ?c2)
				WHERE {
					?b2 <codex:lookupToken> ?vK .
					?b2 <codex:lookupIri> ?iri2 .
				}
			) = 1
		)
		?bK <codex:lookupToken> ?vK .
		?bK <codex:lookupIri> ?rK .
	}

	FILTER( !EXISTS {
		?nK <codex:declaredId> ?rK .
		?nK rdf:type <conceptClassIri(X)>
	} )
}
```

`ReferenceConstraint(type=ReferenceMustResolve)` requires a deterministic definition of “resolve”.

Therefore, this document defines `ReferenceMustResolve` deterministically as:

- for each reference trait value `?vK`, it MUST resolve to an IRI `?rK` by:
	- if `?vK` is an IRI, `?rK = ?vK`.
	- if `?vK` is a Lookup Token typed literal, there MUST exist exactly one binding mapping that token to `?rK` using §6.7.
	- otherwise, it MUST be treated as unresolved.

- the resolved IRI `?rK` MUST match the declared identifier of some node in the same Document.

One conforming `H` is:

```
!EXISTS {
	VALUES ?pK { <traitPredicateIri("reference")> <traitPredicateIri("target")> <traitPredicateIri("for")> }
	focusVar ?pK ?vK .

	# Resolve IRIs directly
	{
		FILTER(isIRI(?vK))
		BIND(?vK AS ?rK)
	}
	UNION
	# Resolve lookup tokens via explicit bindings
	{
		FILTER(isLiteral(?vK) && DATATYPE(?vK) = <urn:cdx:value-type:LookupToken>)
		FILTER(
			(
				SELECT (COUNT(DISTINCT ?iri2) AS ?c2)
				WHERE {
					?b2 <codex:lookupToken> ?vK .
					?b2 <codex:lookupIri> ?iri2 .
				}
			) = 1
		)
		?bK <codex:lookupToken> ?vK .
		?bK <codex:lookupIri> ?rK .
	}

	# Unresolved if no node declares the referenced IRI
	FILTER( !EXISTS { ?nK <codex:declaredId> ?rK } )
}
```

##### 8.6.5.12 Order and Collection Constraints

This section defines deterministic mappings for collection and order constraints.

These mappings require the Layer A extension in §4.1.4.

Let `path` be the collection member path child.

Let `mVar` be a deterministically allocated member variable.

The member binding pattern MUST be:

```
B(path, focusVar, mVar)
```

If `path` is not `ChildPath` or `DescendantPath`, expansion MUST fail.

`CollectionAllowsEmpty(allowed=true)` MUST NOT emit any constraint.

`CollectionAllowsEmpty(allowed=false)` MUST map to a SPARQL hold expression:

```
EXISTS {
	B(path, focusVar, mVar)
}
```

`MemberCount(min=a?, max=b?)` MUST map to a COUNT aggregate over members.

If both `min` and `max` are absent, expansion MUST fail.

One conforming construction is:

- compute `?countK` as:

```
(
	SELECT (COUNT(?mVar) AS ?countK)
	WHERE {
		B(path, focusVar, mVar)
	}
)
```

- then emit comparisons for the bounds that are present:
	- if `min=a` is present, include `(?countK >= a)`
	- if `max=b` is present, include `(?countK <= b)`

`EachMemberSatisfies(Rule=R)` MUST be interpreted as:

- `OnPathForAll(path, R)`

and MUST use the §8.6.7 `OnPathForAll` mapping.

`CollectionAllowsDuplicates(allowed=true)` MUST NOT emit any constraint.

`CollectionAllowsDuplicates(allowed=false, keyTrait=t)` MUST map to:

- compute `keyPredicateIri(t)` as:
	- if `t` is `id`, `keyPredicateIri(t)` MUST be `codex:declaredId`.
	- otherwise, `keyPredicateIri(t)` MUST be `traitPredicateIri(t)`.

- each member selected by `path` MUST have exactly one value for `keyPredicateIri(t)`.
- no two distinct members selected by `path` may share the same value for `keyPredicateIri(t)`.

One conforming `H` is the conjunction of two conditions:

```
(
	# key well-formedness: exactly one key value per member
	!EXISTS {
		B(path, focusVar, ?mK)
		FILTER(
			(
				SELECT (COUNT(DISTINCT ?k2K) AS ?c2)
				WHERE { ?mK <keyPredicateIri(t)> ?k2K }
			) != 1
		)
	}
)
&&
(
	# uniqueness: no two distinct members share a key value
	!EXISTS {
		B(path, focusVar, ?m1K)
		B(path, focusVar, ?m2K)
		FILTER(?m1K != ?m2K)
		?m1K <keyPredicateIri(t)> ?kK .
		?m2K <keyPredicateIri(t)> ?kK .
	}
)
```

This mapping defines duplicates by equality of the RDF term `?kK`.

`CollectionOrdering(ordering=$Unordered)` MUST NOT emit any constraint.

`CollectionOrdering(ordering=$Ordered)` MUST map only when `path` is `ChildPath`.

If `path` is `DescendantPath`, expansion MUST fail.

When mapped, it MUST require that each selected member has exactly one edge index under the current focus node.

This requirement MUST be expressed using the edge encoding in §6.5.

One conforming `H` is:

```
!EXISTS {
	B(path, focusVar, mVar)
	FILTER(
		(
			SELECT (COUNT(DISTINCT ?e2K) AS ?c2)
			WHERE {
				?e2K <codex:parent> focusVar .
				?e2K <codex:child> mVar .
				?e2K <codex:index> ?i2K .
			}
		) != 1
	)
}
```

`OrderConstraint(type=VariadicMustBeLast)` MUST map only when `path` is `ChildPath`.

If `path` is `DescendantPath`, expansion MUST fail.

This order constraint MUST be defined using the schema's child rules for the target concept:

- A child concept selector `X` is *variadic* iff the target concept's `ChildRules` include an `AllowsChildConcept` or `RequiresChildConcept` with `conceptSelector=X` and with `max` omitted.

If there are no variadic child concept selectors, the constraint MUST NOT emit any constraint.

If there are one or more variadic child concept selectors, the constraint MUST mean:

- within the direct children of the focus node, no non-variadic child may appear after any variadic child.

One conforming `H` is:

```
!EXISTS {
	# pick a variadic child edge
	?eVarK <codex:parent> focusVar .
	?eVarK <codex:child> ?cVarK .
	?eVarK <codex:index> ?iVarK .
	?cVarK rdf:type ?tVarK .
	VALUES ?tVarK { <conceptClassIri(V1)> <conceptClassIri(V2)> }

	# pick a non-variadic child edge
	?eNonK <codex:parent> focusVar .
	?eNonK <codex:child> ?cNonK .
	?eNonK <codex:index> ?iNonK .
	?cNonK rdf:type ?tNonK .
	FILTER( ?tNonK NOT IN ( <conceptClassIri(V1)>, <conceptClassIri(V2)> ) )

	# violation if a non-variadic child appears after a variadic child
	FILTER( ?iNonK > ?iVarK )
}
```

The `VALUES` list MUST include exactly the set of variadic child concept selectors.

For any `OrderConstraint` type other than `VariadicMustBeLast`, expansion MUST fail.

#### 8.6.6 Rule Algebra → SHACL-SPARQL (Total)

This section defines a total mapping for the rule algebra elements:

- `AllOf`
- `AnyOf`
- `Not`
- `ConditionalConstraint` (`When` / `Then`)

This mapping is total in the sense that it provides a deterministic SHACL-SPARQL construction for any rule algebra tree.

If the rule algebra tree contains an atomic constraint whose *atomic* mapping is undefined, expansion MUST fail.

##### 8.6.6.1 Canonical SPARQL Form

For any `ConstraintDefinition`, expansion MUST emit exactly one SHACL-SPARQL constraint query per target shape.

The query MUST be a `SELECT` query that returns one row per violating focus node using the SHACL-SPARQL convention:

- The focus node variable MUST be `?this`.
- A row returned by the query MUST indicate a violation.

The query MUST have the following canonical structure:

```
SELECT DISTINCT ?this
WHERE {
	<TARGET_BINDING>
	FILTER( !( <HOLD_EXPR> ) )
}
```

`<TARGET_BINDING>` MUST be computed by §8.6.5.1.

`<HOLD_EXPR>` MUST be computed by the function `H(rule, ctx, focusVar)` defined below, with `focusVar` set to `?this`.

##### 8.6.6.2 Deterministic Variable Allocation

Atomic constraints and path/quantifier expressions often require internal SPARQL variables.

To avoid accidental capture and to make the output canonical, expansion MUST allocate internal variable names deterministically.

Expansion MUST walk the rule tree in pre-order.

For the k-th node visited (1-indexed), the expansion context `ctx` MUST define a node-local suffix `k`.

Any internal variable introduced while translating that node MUST be named by appending `k` to a base name.

Examples:

- `?v1`, `?v2`, ... for values
- `?c1`, `?c2`, ... for child nodes

Variables introduced for one rule node MUST NOT be referenced outside the `EXISTS { ... }` block created for that node.

##### 8.6.6.3 The `H(rule, ctx)` Function

`H(rule, ctx, focusVar)` returns a SPARQL boolean expression that evaluates to true exactly when the rule holds for the current focus node.

If `focusVar` is omitted, it MUST be `?this`.

`H(rule, ctx, focusVar)` MUST be computed as follows.

**AllOf**

If `rule` is `AllOf` with child rules `r1..rn`, then:

- `H(rule, ctx, focusVar) = H(r1, ctx1, focusVar) && H(r2, ctx2, focusVar) && ... && H(rn, ctxn, focusVar)`

where `ctxi` are derived by continuing the deterministic pre-order traversal.

**AnyOf**

If `rule` is `AnyOf` with child rules `r1..rn`, then:

- `H(rule, ctx, focusVar) = H(r1, ctx1, focusVar) || H(r2, ctx2, focusVar) || ... || H(rn, ctxn, focusVar)`

**Not**

If `rule` is `Not` with exactly one child rule `r`, then:

- `H(rule, ctx, focusVar) = !H(r, ctx1, focusVar)`

**ConditionalConstraint**

If `rule` is `ConditionalConstraint` with condition rule `w` (under `When`) and consequent rule `t` (under `Then`), then:

- `H(rule, ctx, focusVar) = (!H(w, ctxW, focusVar)) || H(t, ctxT, focusVar)`

This is logically equivalent to: if the condition holds, the consequent must hold.

##### 8.6.6.4 Atomic Rules as `EXISTS` Blocks

If `rule` is atomic, `H(rule, ctx)` MUST be a SPARQL `EXISTS { ... }` form or an `EXISTS`-free boolean constant.

For atomic rules whose SHACL Core mapping is defined in §8.6.5, expansion MUST ALSO define `H(rule, ctx)` using only SPARQL 1.1 constructs.

This is required because rule algebra composition is expressed using SPARQL boolean composition.

If an atomic rule cannot be expressed as a SPARQL boolean expression without inventing additional semantics, expansion MUST fail.

For atomic rules mapped in §8.6.5, a conforming `H` translation includes at minimum:

- `TraitExists(trait=t)`: `EXISTS { focusVar <traitPredicateIri(t)> ?vK }`
- `TraitMissing(trait=t)`: `!EXISTS { focusVar <traitPredicateIri(t)> ?vK }`
- `TraitEquals(trait=t, value=v)`: `EXISTS { focusVar <traitPredicateIri(t)> <valueTerm(v)> }`

Here `?vK` MUST follow the deterministic variable allocation rule in §8.6.6.2.

##### 8.6.6.5 One-Way Representation Rule

When a `ConstraintDefinition` uses rule algebra (i.e., contains `AllOf`, `AnyOf`, `Not`, or `ConditionalConstraint` anywhere in its rule tree), expansion MUST express that constraint definition using SHACL-SPARQL only.

Expansion MUST NOT additionally emit independent SHACL Core constraints for the same `ConstraintDefinition`.

Rationale: emitting both creates multiple ways to say the same thing and risks divergence between engines.

#### 8.6.7 Paths and Quantifiers → SHACL-SPARQL (Total)

This section defines a total mapping for:

- `TraitPath`, `ChildPath`, `DescendantPath`, `ContentPath`
- `OnPathExists`, `OnPathForAll`, `OnPathCount`

These operators MUST be expressed using SHACL-SPARQL.

##### 8.6.7.1 Path Binding Function

Define a function `B(path, focusVar, outVar)` that emits a SPARQL graph pattern which binds `outVar` to each element selected by `path` from `focusVar`.

`B` MUST be computed as follows.

**TraitPath**

For `TraitPath traitName=t`:

```
focusVar <traitPredicateIri(t)> outVar .
```

**ChildPath**

For `ChildPath conceptSelector=X`:

```
outVar <codex:parentNode> focusVar .
outVar rdf:type <conceptClassIri(X)> .
```

**DescendantPath**

For `DescendantPath conceptSelector=X`:

```
outVar <codex:parentNode>+ focusVar .
outVar rdf:type <conceptClassIri(X)> .
```

**ContentPath**

For `ContentPath`:

```
focusVar <codex:content> outVar .
```

If `conceptSelector` cannot be resolved to a unique `ConceptDefinition`, expansion MUST fail.

##### 8.6.7.2 Quantifier Semantics

Each `OnPath*` node scopes a nested rule over the set of elements produced by `B`.

Let `path` be its `Path` child.

Let `r` be its nested `Rule` child.

Let `xVar` be the deterministically allocated variable for the bound element.

The nested rule MUST be evaluated with `focusVar` set to `xVar`.

**OnPathExists**

`OnPathExists(path, r)` MUST translate to:

```
EXISTS {
	B(path, focusVar, xVar)
	FILTER( H(r, ctxChild, xVar) )
}
```

**OnPathForAll**

`OnPathForAll(path, r)` MUST translate to:

```
!EXISTS {
	B(path, focusVar, xVar)
	FILTER( !H(r, ctxChild, xVar) )
}
```

**OnPathCount**

`OnPathCount(path, r, minCount=m?, maxCount=n?)` MUST translate to a COUNT aggregate over elements that satisfy `r`.

If both `minCount` and `maxCount` are absent, expansion MUST fail.

It MUST translate to a boolean expression of the form:

```
(
	SELECT (COUNT(?xVar) AS ?countK)
	WHERE {
		B(path, focusVar, xVar)
		FILTER( H(r, ctxChild, xVar) )
	}
)
```

combined with comparisons:

- if `minCount` is present: `?countK >= m`
- if `maxCount` is present: `?countK <= n`

`?countK` MUST follow the deterministic variable allocation rule in §8.6.6.2.

#### 8.6.2 SPARQL Constraint Shape

When a constraint is expressed using SHACL-SPARQL, the expansion MUST emit:

- `(shapeIri, sh:sparql, sparqlConstraintIri)`
- `(sparqlConstraintIri, sh:select, selectTextLiteral)`

If the source constraint has a `title` or `description`, the expansion MAY emit `sh:message`.

The SPARQL query MUST be deterministic given the source constraint.

#### 8.6.3 Pattern Constraints (SPARQL 1.1 REGEX)

For the pattern-bearing constraints (`ValueMatchesPattern`, `PatternConstraint`, `ContentMatchesPattern`), the expansion MUST use SPARQL 1.1 `REGEX` semantics.

If `flags` is present, it MUST be projected to `sh:flags` when using `sh:pattern`, and it MUST be passed as the third argument to `REGEX` when using `sh:sparql`.

#### 8.6.4 `ValueIsValid` via Explicit `ValidatorDefinition`

For `ValueIsValid validatorName=$X`, expansion MUST:

1. Resolve `$X` to exactly one `ValidatorDefinition` in the schema.
2. Embed the `ValidatorDefinition` content into a SHACL-SPARQL constraint.

If the validator cannot be resolved uniquely, expansion MUST fail.

The embedding contract MUST be purely textual and deterministic.

One conforming contract is:

- The validator content MUST be a SPARQL `SELECT` query string whose results follow the SHACL-SPARQL convention (returning a row per violation with `?this`).

The derived `sh:select` string MUST be exactly the validator content.

---

## 9. Layer B → SHACL Projection Algorithm

Layer B is already an RDF graph.

Projection MUST be exactly:

1. Validate the Layer B `RdfGraph` against Layer B structural rules.
2. Emit the triples in a chosen RDF concrete syntax (e.g., Turtle).

The projection MUST NOT change the set of triples.

---

## 10. “One Way To Say It” Checklist

The following guardrails MUST hold:

- Profile A schemas MUST NOT contain `RdfGraph`.
- Profile B schemas MUST contain exactly one `RdfGraph` and MUST NOT contain Layer A schema-definition concepts.
- Layer A expansion MUST generate a canonical Layer B graph; different Layer A spellings that are semantically identical MUST expand to byte-identical Layer B graphs.
- Layer B canonicalization MUST make semantically identical graphs byte-identical.

---

## 11. Open Items (Deliberately Explicit)

These are not hand-waved; they are explicitly unfinished and MUST be closed before this moves into the unified spec:

1. Define, in the unified spec, the profile selection surface (Profile A vs Profile B).
