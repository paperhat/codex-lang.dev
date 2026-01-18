Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1
Editor: Charles F. Munat

# **Codex Schema Definition Specification — Version 0.1**

This document defines the **schema definition model** for the Codex language.

It specifies how **schemas themselves are authored in Codex**, including:

* Concept definitions
* Trait definitions
* Entity eligibility
* Collection semantics
* Contextual meaning
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
* support compilation to external validation systems (e.g. SHACL)

Schemas are the **sole authority on meaning** in Codex.

---

## 2. Core Principles (Normative)

* Schemas are **declarative data**, not executable programs
* Validation is **closed-world** and deterministic
* All authorization is **explicit**
* All constraints are **mechanically enforceable**
* No inference, defaults, or heuristics are permitted

---

## 3. Schema

### 3.1 `Schema`

A `Schema` Concept defines a schema.

#### Traits (Normative)

* `id` (required; IRI reference)
* `version` (required; string or enumerated token)
* `compatibilityClass` (required; `$BackwardCompatible | $ForwardCompatible | $Breaking`)
* `title` (optional; string)
* `description` (optional; string)

#### Children (Normative)

A `Schema` MAY contain, in any order:

* `ConceptDefinitions`
* `TraitDefinitions`
* `ConstraintDefinitions`
* `ContextDefinitions`
* `ValueTypeDefinitions` (optional)

---

## 4. Concept Definitions

### 4.1 `ConceptDefinition`

Defines a Codex Concept.

#### Traits (Normative)

* `id` (optional; IRI reference)
* `name` (required; PascalCase string)
* `conceptKind` (required; `$Semantic | $Structural | $ValueLike`)
* `entityEligibility` (required; `$MustBeEntity | $MayBeEntity | $MustNotBeEntity`)

#### Children

* `TraitRules`
* `ChildRules`
* `ContentRules`
* `CollectionRules`
* `ContextRules`

---

## 5. Trait Definitions

### 5.1 `TraitDefinition`

Defines a Trait independently of any Concept.

#### Traits (Normative)

* `id` (optional; IRI reference)
* `name` (required; camelCase string)
* `defaultValueType` (required; value type token or value type identifier)
* `cardinality` (required; `$Single | $List`)
* `itemValueType` (required if `cardinality=$List`)
* `isReferenceTrait` (optional; boolean)

#### Children (Optional)

* `AllowedValues`
* `ValueConstraints`

---

## 6. Value Types

### 6.1 Built-in Value Type Tokens (Normative)

Schemas MAY reference the following built-in value types:

* `$String`
* `$Boolean`
* `$Number`
* `$EnumeratedToken`
* `$IriReference`
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
* `$Range`

---

### 6.2 `ValueTypeDefinition` (Optional)

Defines a named value type.

#### Traits

* `id` (optional; IRI reference)
* `name` (required; PascalCase string)
* `baseValueType` (required; built-in value type token)
* `validatorName` (optional; enumerated token)

---

## 7. Constraint Model

### 7.1 `ConstraintDefinition`

Defines a reusable constraint.

#### Traits (Normative)

* `id` (required; IRI reference)
* `title` (optional; string)
* `description` (optional; string)

#### Children (Normative)

* `Targets`
* `Rule`

---

### 7.2 Targets

A constraint MUST declare one or more targets.

Targets MAY reference:

* a Concept **by name**
* a ConceptDefinition **by identifier**

#### Target Concepts

* `TargetConcept` (`conceptSelector`)

#### Target Contexts (Optional)

* `TargetContext` (`contextSelector`)

---

## 8. Rule Algebra (Normative)

Each `Rule` MUST be exactly one of:

* `AllOf`
* `AnyOf`
* `Not`
* `Implies`
* `TraitConstraint`
* `ValueConstraint`
* `ChildConstraint`
* `CollectionConstraint`
* `ReferenceConstraint`
* `IdentityConstraint`
* `ContextConstraint`

### 8.1 Composition Rules

* `AllOf` — all child Rules must hold
* `AnyOf` — at least one child Rule must hold
* `Not` — child Rule must not hold
* `Implies` — if Rule A holds, Rule B must hold

---

## 9. Paths and Quantifiers

### 9.1 Paths

Constraints MAY reference data using paths:

* `TraitPath` (`traitName`)
* `ChildPath` (`conceptSelector`)
* `DescendantPath` (`conceptSelector`)
* `ContentPath`

---

### 9.2 Quantifiers

* `Exists`
* `ForAll`
* `Count` (`minCount`, `maxCount`)

Quantifiers are structural and deterministic.

---

## 10. Atomic Constraints

### 10.1 Trait Constraints

* `TraitExists`
* `TraitMissing`
* `TraitCardinality`
* `TraitValueType`
* `TraitValueSatisfies`

---

### 10.2 Value Constraints

* `ValueIsOneOf`
* `ValueMatchesPattern`
* `ValueLength`
* `ValueInNumericRange`
* `ValueIsNonEmpty`
* `ValueIsValid`

---

### 10.3 Child Constraints

* `AllowsChildConcept`
* `RequiresChildConcept`
* `ForbidsChildConcept`
* `ChildSatisfies`

---

### 10.4 Collection Constraints

* `CollectionMemberConcept`
* `CollectionOrdering`
* `CollectionAllowsEmpty`
* `CollectionAllowsDuplicates`
* `EachMemberSatisfies`
* `MemberCount`

---

### 10.5 Reference Constraints

* `ReferenceSingleton`
* `ReferenceTraitAllowed`
* `ReferenceMustResolve`
* `ReferenceTargetsConcept`
* `ReferenceTargetsEntity`

---

### 10.6 Identity Constraints

* `MustBeEntity`
* `MustNotBeEntity`
* `IdentifierUniqueness`
* `IdentifierForm`

---

### 10.7 Context Constraints

* `OnlyValidUnderParent`
* `OnlyValidUnderContext`

---

## 11. Relationship to External Systems (Normative)

* Codex schemas are **authoritative**
* SHACL or OWL representations MAY be derived
* Derived artifacts MUST NOT override Codex validation semantics

---

## 12. Stability

This specification is **immutable** as part of Codex v0.1.

---

## 13. Summary

* Schemas are first-class Codex data
* Validation is closed-world and deterministic
* Constraints are declarative and compositional
* Concepts may be targeted by name or identifier
* This ontology enables self-hosting schema validation

---

**End of Codex Schema Definition Specification v0.1**
