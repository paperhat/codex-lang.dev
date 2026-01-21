Status: NORMATIVE
Lock State: UNLOCKED
Version: 0.1
Editor: Charles F. Munat

# Codex Bootstrap Schema-of-Schemas Definition — Version 0.1

This document defines the **bootstrap schema-of-schemas** required by Codex.

Codex is schema-first. A schema document (root Concept `Schema`) cannot depend on
an external schema document to be parsed and validated without circularity.

Therefore every conforming implementation MUST include a **built-in, hard-coded**
bootstrap schema-of-schemas.

This document defines that bootstrap schema-of-schemas **normatively**, in terms
of:

- which Concepts exist in the schema-language
- which Traits those Concepts accept/require
- which child Concepts are permitted/required
- which built-in enumerations and value-type tokens are recognized

This document is **Normative**.

---

## 1. Terminology (Normative)

### 1.1 Bootstrap Schema-of-Schemas

The **bootstrap schema-of-schemas** is the built-in schema language runtime. It
is not loaded from disk/network.

It exists so an implementation can parse and validate **schema documents**
without circular dependency.

### 1.2 Meta-Schema

A **meta-schema** (in Codex’s broader ecosystem) is a schema document written in
Codex that is **valid under the bootstrap schema-of-schemas** and that defines a
class of schemas (e.g., data schemas, view schemas, configuration schemas).

Meta-schemas are external artifacts (typically `schema.cdx`) and are not required
to be available until an implementation needs to validate schemas of that class.

---

## 2. Conformance Requirement (Normative)

A conforming Codex implementation MUST embed a bootstrap schema-of-schemas that
is functionally equivalent to the definition in this document.

Equivalence is defined by behavior:

- A schema document that satisfies this document MUST be accepted as a valid
  schema document.
- A schema document that violates this document MUST produce a `SchemaError`
  (unless the document is not structurally readable, in which case it is a
  `ParseError`).

---

## 3. Schema Document Model (Normative)

### 3.1 Root `Schema`

A schema document is identified by the root Concept name `Schema`.

`Schema` Traits:

- `id` (required; IRI reference)
- `version` (required; string)
- `compatibilityClass` (required; enumerated token; see § 6)
- `title` (optional; string)
- `description` (optional; string)

`Schema` Children (optional; any order):

- `ConceptDefinitions`
- `TraitDefinitions`
- `EnumeratedValueSets`
- `ConstraintDefinitions`
- `ValueTypeDefinitions`

### 3.2 `ConceptDefinitions` Container

`ConceptDefinitions` is a container Concept.

Children:

- one or more `ConceptDefinition`

### 3.3 `ConceptDefinition`

`ConceptDefinition` Traits:

- `id` (required; IRI reference)
- `key` (optional; lookup token)
- `name` (required; PascalCase string)
- `conceptKind` (required; enumerated token; see § 6)
- `entityEligibility` (required; enumerated token; see § 6)

`ConceptDefinition` Children (optional; any order):

- `ContentRules`
- `TraitRules`
- `ChildRules`
- `CollectionRules`

### 3.4 `ContentRules`, `AllowsContent`, `ForbidsContent`

`ContentRules` Children:

- exactly one of `AllowsContent` or `ForbidsContent`

Default:

- if `ContentRules` is omitted for a `ConceptDefinition`, `ForbidsContent` is
  assumed.

### 3.5 `TraitRules`

`TraitRules` Children:

- zero or more of `RequiresTrait`, `AllowsTrait`, `ForbidsTrait`

`RequiresTrait` Traits:

- `name` (required; camelCase string)

`AllowsTrait` Traits:

- `name` (required; camelCase string)

`ForbidsTrait` Traits:

- `name` (required; camelCase string)

Default:

- Traits not listed are forbidden by default.

### 3.6 `ChildRules`

`ChildRules` Children:

- zero or more of `AllowsChildConcept`, `RequiresChildConcept`, `ForbidsChildConcept`

`AllowsChildConcept` Traits:

- `conceptSelector` (required; Concept name as string)
- `min` (optional; non-negative integer; default 0)
- `max` (optional; positive integer; omit for unbounded)

`RequiresChildConcept` Traits:

- `conceptSelector` (required; Concept name as string)
- `min` (optional; positive integer; default 1)
- `max` (optional; positive integer; omit for unbounded)

`ForbidsChildConcept` Traits:

- `conceptSelector` (required; Concept name as string)

Default:

- Child Concepts not listed are forbidden by default.

### 3.7 `CollectionRules`

`CollectionRules` is self-closing.

Traits:

- `ordering` (required; enumerated token; see § 6)
- `allowsDuplicates` (required; boolean)

---

## 4. Trait Definition Model (Normative)

### 4.1 `TraitDefinitions` Container

`TraitDefinitions` is a container Concept.

Children:

- one or more `TraitDefinition`

### 4.2 `TraitDefinition`

`TraitDefinition` Traits:

- `id` (optional; IRI reference)
- `name` (required; camelCase string)
- `defaultValueType` (required; value type token; see § 5)
- `cardinality` (required; enumerated token; see § 6)
- `itemValueType` (required if `cardinality=$List`; value type token; see § 5)
- `isReferenceTrait` (optional; boolean)

`TraitDefinition` Children (optional):

- `AllowedValues`

### 4.3 `AllowedValues`

`AllowedValues` Children:

- one or more of `ValueIsOneOf` or `EnumeratedConstraint`

`ValueIsOneOf` Traits:

- `values` (required; list of allowed values)

`EnumeratedConstraint` Traits:

- `set` (required; PascalCase string naming an `EnumeratedValueSet`)

---

## 5. Value Types (Normative)

### 5.1 Built-in Value Type Tokens

The bootstrap schema-of-schemas MUST recognize the following value type tokens:

- `$String`
- `$Char`
- `$Boolean`
- `$Number`
- `$Integer`
- `$EnumeratedToken`
- `$IriReference`
- `$LookupToken`
- `$Uuid`
- `$Color`
- `$Temporal`
- `$Date`
- `$YearMonth`
- `$MonthDay`
- `$LocalDateTime`
- `$ZonedDateTime`
- `$Duration`
- `$List`
- `$Set`
- `$Map`
- `$Tuple`
- `$Range`

### 5.2 `ValueTypeDefinitions` and `ValueTypeDefinition`

`ValueTypeDefinitions` is a container Concept holding zero or more
`ValueTypeDefinition` children.

`ValueTypeDefinition` Traits:

- `id` (optional; IRI reference)
- `name` (required; PascalCase string)
- `baseValueType` (required; built-in value type token)
- `validatorName` (optional; enumerated token)

---

## 6. Built-in Enumerations (Normative)

The bootstrap schema-of-schemas MUST recognize the following built-in enumerated
value sets and members.

### 6.1 `ConceptKind`

- `$Semantic`
- `$Structural`
- `$ValueLike`

### 6.2 `EntityEligibility`

- `$MustBeEntity`
- `$MayBeEntity`
- `$MustNotBeEntity`

### 6.3 `CompatibilityClass`

- `$BackwardCompatible`
- `$ForwardCompatible`
- `$Breaking`

### 6.4 `Ordering`

- `$Ordered`
- `$Unordered`

### 6.5 `Cardinality`

- `$Single`
- `$List`

---

## 7. Constraint Model (Normative)

This section defines the schema-language for declaring constraints.

### 7.1 Containers

- `ConstraintDefinitions` contains one or more `ConstraintDefinition` children.

### 7.2 `ConstraintDefinition`

Traits:

- `id` (required; IRI reference)
- `title` (optional; string)
- `description` (optional; string)

Children:

- `Targets` (required)
- `Rule` (required)

### 7.3 `Targets`

Children:

- one or more of `TargetConcept` or `TargetContext`

`TargetConcept` Traits:

- `conceptSelector` (required; Concept name as string)

`TargetContext` Traits:

- `contextSelector` (required; Concept name as string, or the literal string `"Document"`)

### 7.4 `Rule`

`Rule` MUST contain exactly one constraint node or composition node.

### 7.5 Composition Nodes

- `AllOf` — children: two or more `Rule`
- `AnyOf` — children: two or more `Rule`
- `Not` — children: exactly one `Rule`
- `ConditionalConstraint` — children: `When` then `Then`, each containing exactly one `Rule`

### 7.6 Paths

- `TraitPath` (trait: `traitName`)
- `ChildPath` (trait: `conceptSelector`)
- `DescendantPath` (trait: `conceptSelector`)
- `ContentPath` (no traits)

### 7.7 Quantifiers

- `Exists`
- `ForAll`
- `Count` (traits: `minCount` optional, `maxCount` optional)

### 7.8 Atomic Constraints

Atomic constraints are the leaves of the rule algebra.

Unless otherwise specified, atomic constraint nodes are self-closing.

#### 7.8.1 Trait Constraints

`TraitExists` Traits:

- `trait` (required; camelCase string)

`TraitMissing` Traits:

- `trait` (required; camelCase string)

`TraitEquals` Traits:

- `trait` (required; camelCase string)
- `value` (required; Value)

`TraitCardinality` Traits:

- `trait` (required; camelCase string)
- `min` (optional; non-negative integer)
- `max` (optional; positive integer)

`TraitValueType` Traits:

- `trait` (required; camelCase string)
- `valueType` (required; value type token; see § 5)

#### 7.8.2 Value Constraints

`ValueIsOneOf` Traits:

- `values` (required; list of allowed values)

`ValueMatchesPattern` Traits:

- `pattern` (required; regex string)

`PatternConstraint` Traits:

- `trait` (required; camelCase string)
- `pattern` (required; regex string)

`ValueLength` Traits:

- `min` (optional; non-negative integer)
- `max` (optional; positive integer)

`ValueInNumericRange` Traits:

- `min` (optional; number; inclusive)
- `max` (optional; number; inclusive)

`ValueIsNonEmpty`:

- no traits

`ValueIsValid` Traits:

- `validatorName` (required; enumerated token)

#### 7.8.3 Child Constraints

`ChildConstraint` Traits:

- `type` (required; string; one of `RequiresChildConcept`, `AllowsChildConcept`, `ForbidsChildConcept`)
- `conceptSelector` (required; Concept name as string)

`ChildSatisfies` Traits:

- `conceptSelector` (required; Concept name)

`ChildSatisfies` Children:

- one `Rule`

#### 7.8.4 Collection Constraints

`CollectionOrdering` Traits:

- `ordering` (required; `$Ordered | $Unordered`)

`CollectionAllowsEmpty` Traits:

- `allowed` (required; boolean)

`CollectionAllowsDuplicates` Traits:

- `allowed` (required; boolean)

`MemberCount` Traits:

- `min` (optional; non-negative integer)
- `max` (optional; positive integer)

`EachMemberSatisfies` Children:

- one `Rule`

#### 7.8.5 Uniqueness Constraints

`UniqueConstraint` Traits:

- `trait` (required; camelCase string)
- `scope` (required; Concept name as string defining the uniqueness scope)

#### 7.8.6 Order Constraints

`OrderConstraint` Traits:

- `type` (required; string; e.g. `VariadicMustBeLast`)

#### 7.8.7 Reference Constraints

`ReferenceConstraint` Traits:

- `type` (required; string; one of the following)

Allowed `type` values:

- `ReferenceTargetsEntity`
- `ReferenceMustResolve`
- `ReferenceTargetsConcept` (requires additional trait `conceptSelector`)
- `ReferenceSingleton`
- `ReferenceTraitAllowed`

If `type=ReferenceTargetsConcept`, additional Traits:

- `conceptSelector` (required; Concept name)

#### 7.8.8 Identity Constraints

`IdentityConstraint` Traits:

- `type` (required; string; one of the following)

Allowed `type` values:

- `MustBeEntity`
- `MustNotBeEntity`
- `IdentifierUniqueness`
- `IdentifierForm`

#### 7.8.9 Context Constraints

`ContextConstraint` Traits:

- `type` (required; string; one of the following)
- `contextSelector` (required for the listed types; Concept name)

Allowed `type` values:

- `OnlyValidUnderParent`
- `OnlyValidUnderContext`

#### 7.8.10 Content Constraints

`ContentConstraint` Traits:

- `type` (required; string; one of the following)

Allowed `type` values:

- `ContentForbiddenUnlessAllowed`
- `ContentRequired`
- `ContentMatchesPattern` (requires additional trait `pattern`)

If `type=ContentMatchesPattern`, additional Traits:

- `pattern` (required; regex string)

---

## 8. Error Classification (Normative)

- If a schema document is not structurally readable (e.g., malformed markers),
  the failure is a `ParseError`.
- If a schema document is structurally readable but violates the bootstrap
  schema-of-schemas rules, the failure is a `SchemaError`.

---

**End of Codex Bootstrap Schema-of-Schemas Definition v0.1**
