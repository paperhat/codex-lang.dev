Status: NORMATIVE
Lock State: UNLOCKED
Version: 0.1
Editor: Charles F. Munat

# Codex Schema Definition Specification — Version 0.1

This document defines the **schema definition model** for the Codex language.

It specifies how **schemas themselves are authored in Codex**, including:

* Concept definitions
* Trait definitions
* Content, child, trait, and collection rules
* Enumerated value sets
* Entity eligibility
* Declarative constraints
* Schema versioning and compatibility

This document is **Normative**.

---

## 1. Purpose

This specification defines the **authoritative ontology for Codex schemas**.

Its goals are to:

* make schemas **first-class Codex data**
* enable deterministic, closed-world validation
* allow schemas to validate other schemas (bootstrapping)
* ensure interoperability across tools and implementations
* support compilation to external validation systems (e.g., SHACL)

Schemas are the **sole authority on meaning** in Codex.

The schema-language itself is bootstrapped by a built-in **bootstrap schema-of-schemas**.
See `spec/0.1/schema-loading/bootstrap-schema-of-schemas/index.md`.

---

## 2. Core Principles (Normative)

* Schemas are **declarative data**, not executable programs
* Validation is **closed-world** and deterministic
* All authorization is **explicit**
* All constraints are **mechanically enforceable**
* Everything is declared; nothing is inferred or defaulted

---

## 3. Schema

### 3.1 `Schema`

A `Schema` Concept defines a schema.

#### Traits (Normative)

* `id` (required; IRI reference)
* `version` (required; string)
* `compatibilityClass` (required; `$BackwardCompatible | $ForwardCompatible | $Breaking`)
* `title` (optional; string)
* `description` (optional; string)

#### Children (Normative)

A `Schema` MAY contain, in any order:

* `ConceptDefinitions`
* `TraitDefinitions`
* `EnumeratedValueSets`
* `ConstraintDefinitions`
* `ValueTypeDefinitions` (optional)

---

## 4. Concept Definitions

### 4.1 `ConceptDefinition`

Defines a Codex Concept.

A `ConceptDefinition` is itself an Entity.

#### Traits (Normative)

* `id` (required; IRI reference)
* `key` (optional; lookup token)
* `name` (required; PascalCase string)
* `conceptKind` (required; `$Semantic | $Structural | $ValueLike`)
* `entityEligibility` (required; `$MustBeEntity | $MayBeEntity | $MustNotBeEntity`)

#### Children (Normative)

* `ContentRules` (optional)
* `TraitRules` (optional)
* `ChildRules` (optional)
* `CollectionRules` (optional)

---

### 4.2 `ContentRules`

Declares whether a Concept allows content.

A Concept's content mode determines how the parser handles its body. This is
essential for schema-first parsing.

#### Children (Normative)

Exactly one of:

* `AllowsContent` — Concept body is opaque content (content mode)
* `ForbidsContent` — Concept body contains children or is empty (children mode)

#### Defaults

If `ContentRules` is omitted, `ForbidsContent` is assumed.

#### Parser Implication

The parser MUST consult `ContentRules` to determine content mode before parsing
the Concept body. See the **Language Specification § Schema-First Parsing**.

#### Example

```cdx
<ConceptDefinition
	id=example:concept:Description
	name="Description"
	conceptKind=$Semantic
	entityEligibility=$MustNotBeEntity
>
	<ContentRules>
		<AllowsContent />
	</ContentRules>
</ConceptDefinition>
```

---

### 4.3 `TraitRules`

Declares which Traits a Concept allows, requires, or forbids.

#### Children (Normative)

Zero or more of:

* `RequiresTrait` — Trait MUST be present
* `AllowsTrait` — Trait MAY be present
* `ForbidsTrait` — Trait MUST NOT be present

#### `RequiresTrait`

##### Traits

* `name` (required; camelCase string)

#### `AllowsTrait`

##### Traits

* `name` (required; camelCase string)

#### `ForbidsTrait`

##### Traits

* `name` (required; camelCase string)

#### Defaults

Traits not listed are forbidden by default. A Concept with no `TraitRules`
allows no Traits (except `id` and `key` which are governed by `entityEligibility`).

#### Example

```cdx
<TraitRules>
	<RequiresTrait name="amount" />
	<AllowsTrait name="unit" />
	<AllowsTrait name="optional" />
</TraitRules>
```

---

### 4.4 `ChildRules`

Declares which child Concepts are allowed under a Concept.

#### Children (Normative)

Zero or more of:

* `AllowsChildConcept` — child Concept MAY appear
* `RequiresChildConcept` — child Concept MUST appear (alias for min=1)
* `ForbidsChildConcept` — child Concept MUST NOT appear

#### `AllowsChildConcept`

##### Traits

* `conceptSelector` (required; Concept name as string)
* `min` (optional; non-negative integer, default 0)
* `max` (optional; positive integer, omit for unbounded)

#### `RequiresChildConcept`

##### Traits

* `conceptSelector` (required; Concept name as string)
* `min` (optional; positive integer, default 1)
* `max` (optional; positive integer, omit for unbounded)

Note: `RequiresChildConcept` is semantically equivalent to `AllowsChildConcept`
with `min=1`. It exists for clarity.

#### `ForbidsChildConcept`

##### Traits

* `conceptSelector` (required; Concept name as string)

#### Defaults

Child Concepts not listed are forbidden by default.

#### Example

```cdx
<ChildRules>
	<AllowsChildConcept conceptSelector="Title" />
	<AllowsChildConcept conceptSelector="Description" />
	<RequiresChildConcept conceptSelector="Ingredients" />
	<AllowsChildConcept conceptSelector="Instructions" min=1 />
</ChildRules>
```

---

### 4.5 `CollectionRules`

Declares collection semantics for a Concept that acts as a container.

`CollectionRules` is used when a Concept's children represent a logical collection
(e.g., a list of ingredients, a set of tags). The semantics inform validation
and graph compilation.

#### Traits (Normative)

* `ordering` (required; `$Ordered | $Unordered`)
* `allowsDuplicates` (required; boolean)

#### Form

`CollectionRules` is self-closing (no children).

#### Example

```cdx
<ConceptDefinition
	id=example:concept:Ingredients
	name="Ingredients"
	conceptKind=$Structural
	entityEligibility=$MustNotBeEntity
>
	<ContentRules>
		<ForbidsContent />
	</ContentRules>
	<ChildRules>
		<AllowsChildConcept conceptSelector="Ingredient" />
	</ChildRules>
	<CollectionRules ordering=$Unordered allowsDuplicates=true />
</ConceptDefinition>
```

---

## 5. Trait Definitions

### 5.1 `TraitDefinition`

Defines a Trait independently of any Concept.

Trait definitions establish the value type, cardinality, and constraints for a
Trait that may be used across multiple Concepts.

#### Traits (Normative)

* `id` (optional; IRI reference)
* `name` (required; camelCase string)
* `defaultValueType` (required; value type token)
* `cardinality` (required; `$Single | $List`)
* `itemValueType` (required if `cardinality=$List`; value type token)
* `isReferenceTrait` (optional; boolean)

#### Children (Optional)

* `AllowedValues` — constrains the set of valid values

#### Example

```cdx
<TraitDefinition
	name="amount"
	defaultValueType=$Number
	cardinality=$Single
/>

<TraitDefinition
	name="unit"
	defaultValueType=$EnumeratedToken
	cardinality=$Single
>
	<AllowedValues>
		<ValueIsOneOf values=[$Grams, $Kilograms, $Milliliters, $Liters, $Units] />
	</AllowedValues>
</TraitDefinition>
```

---

### 5.2 `AllowedValues`

Constrains the values a Trait may accept.

#### Children (Normative)

One or more value constraints:

* `ValueIsOneOf` — value must be in explicit list
* `EnumeratedConstraint` — value must be member of named enumeration

#### `ValueIsOneOf`

##### Traits

* `values` (required; list of allowed values)

#### `EnumeratedConstraint`

##### Traits

* `set` (required; name of an `EnumeratedValueSet`)

---

## 6. Value Types

### 6.1 Built-in Value Type Tokens (Normative)

Schemas MAY reference the following built-in value types:

* `$String`
* `$Char`
* `$Boolean`
* `$Number`
* `$Integer`
* `$EnumeratedToken`
* `$IriReference`
* `$LookupToken`
* `$Uuid`
* `$Color`
* `$Temporal`
* `$Date`
* `$YearMonth`
* `$MonthDay`
* `$LocalDateTime`
* `$ZonedDateTime`
* `$Duration`
* `$List`
* `$Set`
* `$Map`
* `$Tuple`
* `$Range`

---

### 6.2 `ValueTypeDefinition` (Optional)

Defines a named value type with custom validation.

#### Traits

* `id` (optional; IRI reference)
* `name` (required; PascalCase string)
* `baseValueType` (required; built-in value type token)
* `validatorName` (optional; enumerated token identifying a validator)

---

### 6.3 Enumerated Value Sets

Schemas MAY define named sets of enumerated values.

#### Container

`EnumeratedValueSets` is a container Concept holding one or more
`EnumeratedValueSet` children.

#### `EnumeratedValueSet`

Defines a named set of valid enumerated tokens.

##### Traits

* `name` (required; PascalCase string)

##### Children

One or more `Member` children.

#### `Member`

Defines a single member of an enumerated value set.

##### Traits

* `value` (required; string matching the token name without `$` prefix)
* `label` (optional; human-readable display string)
* `description` (optional; explanatory string)

#### Example

```cdx
<EnumeratedValueSets>
	<EnumeratedValueSet name="MeasurementUnit">
		<Member value="Grams" label="Grams" />
		<Member value="Kilograms" label="Kilograms" />
		<Member value="Milliliters" label="Milliliters" />
		<Member value="Liters" label="Liters" />
		<Member value="Units" label="Units" description="Countable items" />
	</EnumeratedValueSet>
</EnumeratedValueSets>
```

Usage:

```cdx
<TraitDefinition name="unit" defaultValueType=$EnumeratedToken cardinality=$Single>
	<AllowedValues>
		<EnumeratedConstraint set="MeasurementUnit" />
	</AllowedValues>
</TraitDefinition>
```

---

### 6.4 Built-in Enumerated Value Sets (Normative)

The following enumerated value sets are defined by the language and MUST be
recognized by all implementations.

#### ConceptKind

Describes the semantic role of a Concept.

* `$Semantic` — carries domain meaning; may become graph nodes
* `$Structural` — organizes or groups other Concepts; typically not graph nodes
* `$ValueLike` — represents a value-like construct

#### EntityEligibility

Governs whether Concept instances may or must have identity.

* `$MustBeEntity` — instances MUST declare an `id` Trait
* `$MayBeEntity` — instances MAY declare an `id` Trait
* `$MustNotBeEntity` — instances MUST NOT declare an `id` Trait

#### CompatibilityClass

Declares schema version compatibility.

* `$BackwardCompatible` — existing valid data remains valid
* `$ForwardCompatible` — data authored for new version may validate under older
* `$Breaking` — migration required; existing data may become invalid

#### Ordering

Declares collection ordering semantics.

* `$Ordered` — child order is significant and preserved
* `$Unordered` — child order is not significant

#### Cardinality

Declares Trait value cardinality.

* `$Single` — exactly one value
* `$List` — zero or more values

---

## 7. Constraint Model

### 7.1 `ConstraintDefinitions`

Container for constraint definitions within a schema.

#### Children

One or more `ConstraintDefinition` children.

---

### 7.2 `ConstraintDefinition`

Defines a reusable, named constraint.

#### Traits (Normative)

* `id` (required; IRI reference)
* `title` (optional; string)
* `description` (optional; string)

#### Children (Normative)

* `Targets` (required) — what the constraint applies to
* `Rule` (required) — the constraint logic

---

### 7.3 `Targets`

Declares what a constraint applies to.

#### Children (Normative)

One or more of:

* `TargetConcept` — constraint applies to instances of a Concept
* `TargetContext` — constraint applies within a context

#### `TargetConcept`

##### Traits

* `conceptSelector` (required; Concept name as string)

#### `TargetContext`

##### Traits

* `contextSelector` (required; Concept name or `"Document"`)

---

### 7.4 `Rule`

Contains the constraint logic.

A `Rule` MUST contain exactly one constraint or composition element.

---

## 8. Rule Algebra (Normative)

### 8.1 Composition Rules

Composition rules combine other rules.

#### `AllOf`

All child rules must hold.

##### Children

Two or more `Rule` children.

#### `AnyOf`

At least one child rule must hold.

##### Children

Two or more `Rule` children.

#### `Not`

The child rule must not hold.

##### Children

Exactly one `Rule` child.

#### `ConditionalConstraint`

If a condition holds, a consequent must hold.

##### Children

* `When` — contains the condition (one `Rule` child)
* `Then` — contains the consequent (one `Rule` child)

---

## 9. Paths and Quantifiers

### 9.1 Paths

Constraints MAY reference data using paths:

* `TraitPath` — references a Trait value
  * `traitName` (required; camelCase string)
* `ChildPath` — references direct children
  * `conceptSelector` (required; Concept name)
* `DescendantPath` — references descendants at any depth
  * `conceptSelector` (required; Concept name)
* `ContentPath` — references Content (no traits)

---

### 9.2 Quantifiers

Quantifiers scope constraints over collections.

* `Exists` — at least one element satisfies the rule
* `ForAll` — all elements satisfy the rule
* `Count` — count of elements satisfies bounds
  * `minCount` (optional; non-negative integer)
  * `maxCount` (optional; positive integer)

Quantifiers are structural and deterministic.

---

## 10. Atomic Constraints (Normative)

Atomic constraints are the leaves of the rule algebra.

### 10.1 Trait Constraints

#### `TraitExists`

Trait is present on the Concept.

##### Traits

* `trait` (required; camelCase string)

#### `TraitMissing`

Trait is absent from the Concept.

##### Traits

* `trait` (required; camelCase string)

#### `TraitEquals`

Trait has a specific value.

##### Traits

* `trait` (required; camelCase string)
* `value` (required; the expected value)

#### `TraitCardinality`

Trait value count is within bounds.

##### Traits

* `trait` (required; camelCase string)
* `min` (optional; non-negative integer)
* `max` (optional; positive integer)

#### `TraitValueType`

Trait value matches expected type.

##### Traits

* `trait` (required; camelCase string)
* `valueType` (required; value type token)

---

### 10.2 Value Constraints

#### `ValueIsOneOf`

Value is in an explicit list.

##### Traits

* `values` (required; list of allowed values)

#### `ValueMatchesPattern`

Value matches a regular expression.

##### Traits

* `pattern` (required; regex string)

#### `PatternConstraint`

Trait value matches a regular expression.

##### Traits

* `trait` (required; camelCase string)
* `pattern` (required; regex string)

#### `ValueLength`

String value length is within bounds.

##### Traits

* `min` (optional; non-negative integer)
* `max` (optional; positive integer)

#### `ValueInNumericRange`

Numeric value is within bounds.

##### Traits

* `min` (optional; number, inclusive)
* `max` (optional; number, inclusive)

#### `ValueIsNonEmpty`

Value is present and non-empty.

No traits.

#### `ValueIsValid`

Value passes custom validation.

##### Traits

* `validatorName` (required; enumerated token)

---

### 10.3 Child Constraints

#### `ChildConstraint`

Generic child constraint using type dispatch.

##### Traits

* `type` (required; `RequiresChildConcept | AllowsChildConcept | ForbidsChildConcept`)
* `conceptSelector` (required; Concept name)

#### `ChildSatisfies`

Child Concepts satisfy a nested rule.

##### Traits

* `conceptSelector` (required; Concept name)

##### Children

One `Rule` child.

---

### 10.4 Collection Constraints

#### `CollectionOrdering`

Declares expected ordering.

##### Traits

* `ordering` (required; `$Ordered | $Unordered`)

#### `CollectionAllowsEmpty`

Collection may be empty.

##### Traits

* `allowed` (required; boolean)

#### `CollectionAllowsDuplicates`

Collection may contain duplicates.

##### Traits

* `allowed` (required; boolean)

#### `MemberCount`

Collection member count is within bounds.

##### Traits

* `min` (optional; non-negative integer)
* `max` (optional; positive integer)

#### `EachMemberSatisfies`

Each collection member satisfies a nested rule.

##### Children

One `Rule` child.

---

### 10.5 Uniqueness Constraints

#### `UniqueConstraint`

Trait values must be unique within a scope.

##### Traits

* `trait` (required; camelCase string)
* `scope` (required; Concept name defining the uniqueness scope)

---

### 10.6 Order Constraints

#### `OrderConstraint`

Positional rules for ordered collections.

##### Traits

* `type` (required; e.g., `VariadicMustBeLast`)

---

### 10.7 Reference Constraints

#### `ReferenceConstraint`

Validates reference Trait usage.

##### Traits

* `type` (required; one of the following)

##### Types

* `ReferenceTargetsEntity` — referenced Concept must be an Entity
* `ReferenceMustResolve` — reference must resolve to existing Concept
* `ReferenceTargetsConcept` — reference must target specified Concept type
  * `conceptSelector` (additional trait; Concept name)
* `ReferenceSingleton` — only one reference Trait may be present
* `ReferenceTraitAllowed` — specific reference Trait is permitted

---

### 10.8 Identity Constraints

#### `IdentityConstraint`

Validates Entity identity rules.

##### Traits

* `type` (required; one of the following)

##### Types

* `MustBeEntity` — Concept instance must have `id`
* `MustNotBeEntity` — Concept instance must not have `id`
* `IdentifierUniqueness` — identifier must be unique within scope
* `IdentifierForm` — identifier must match pattern

---

### 10.9 Context Constraints

#### `ContextConstraint`

Validates parent or context rules.

##### Traits

* `type` (required; one of the following)
* `contextSelector` (required for most types; Concept name)

##### Types

* `OnlyValidUnderParent` — Concept may only appear as direct child of specified parent
* `OnlyValidUnderContext` — Concept may only appear within specified ancestor

---

### 10.10 Content Constraints

#### `ContentConstraint`

Validates content rules.

##### Traits

* `type` (required; one of the following)

##### Types

* `ContentForbiddenUnlessAllowed` — content forbidden unless explicitly allowed
* `ContentRequired` — content must be present and non-empty
* `ContentMatchesPattern` — content matches regex pattern
  * `pattern` (additional trait; regex string)

---

## 11. Complete Constraint Example

```cdx
<ConstraintDefinition
	id=example:constraint:recipe-requires-title
	title="Recipe requires Title"
>
	<Targets>
		<TargetConcept conceptSelector="Recipe" />
	</Targets>
	<Rule>
		<ChildConstraint type="RequiresChildConcept" conceptSelector="Title" />
	</Rule>
</ConstraintDefinition>

<ConstraintDefinition
	id=example:constraint:non-nullary-requires-parameters
	title="Non-nullary operators require parameters"
>
	<Targets>
		<TargetConcept conceptSelector="OperatorDefinition" />
	</Targets>
	<Rule>
		<ConditionalConstraint>
			<When>
				<Not>
					<TraitEquals trait="arity" value=$Nullary />
				</Not>
			</When>
			<Then>
				<ChildConstraint type="RequiresChildConcept" conceptSelector="Parameters" />
			</Then>
		</ConditionalConstraint>
	</Rule>
</ConstraintDefinition>
```

---

## 12. Relationship to External Systems (Normative)

* Codex schemas are **authoritative**
* SHACL or OWL representations MAY be derived
* Derived artifacts MUST NOT override Codex validation semantics

---

## 13. Summary

* Schemas are first-class Codex data
* Validation is closed-world and deterministic
* Content mode is declared via `ContentRules`
* Trait, child, and collection rules are explicit
* Constraints are declarative and compositional
* Enumerated value sets may be defined per-schema or built-in
* This ontology enables self-hosting schema validation

---

**End of Codex Schema Definition Specification v0.1**
