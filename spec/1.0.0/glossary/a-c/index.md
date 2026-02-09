Status: DRAFT

# Codex Glossary (A-C)

This file contains glossary entries for terms starting with A-C.

See `../index.md` for format notes and other ranges.

**A–C** | [D–F](../d-f/index.md) | [G–I](../g-i/index.md) | [J–L](../j-l/index.md) | [M–O](../m-o/index.md) | [P–R](../p-r/index.md) | [S–U](../s-u/index.md) | [V–Z](../v-z/index.md)

## Terms

### AllowedValues

A TraitDefinition child that constrains a trait's permitted values, either by explicit ValueIsOneOf entries or an EnumeratedConstraint referencing an EnumeratedValueSet.

---

### AllowsChildConcept

A ChildRules entry that permits a specific child Concept type.

---

### AllowsContent

A ContentRules entry declaring that a Concept may contain content.

---

### AllowsTrait

A TraitRules entry that permits a specific trait on a Concept.

---

### Annotation

Author-supplied editorial metadata that does not affect parsing or semantic validation and is preserved through processing.

---

### Annotation directive

The optional first non-blank line in a block annotation that is one of FLOW:, CODE:, or MARKDOWN: and controls canonicalization.

---

### Annotation kind

The classification of annotations as attached, grouping, or general.

---

### Annotation node

A dedicated node in the RDF instance graph that represents an annotation and its attachment metadata.

---

### Attached annotation

An annotation immediately before a Concept opening marker with no blank line, which attaches to that Concept.

---

### Authoring mode

The schema trait that selects Simplified or Canonical authoring mode and determines the allowed schema structure.

---

### Backtick Text

A backtick-delimited surface spelling of a Text Value that may span multiple lines.

---

### BackwardCompatible

A compatibility class requiring that all data valid under the previous version remains valid under this version, while preserving meaning.

---

### Block annotation

A multi-line annotation with `[` and `]` on their own lines.

---

### Boolean Value

A value whose literal spelling is `true` or `false`.

---

### Bootstrap Schema

The built-in schema-of-schemas used to validate schema documents.

---

### Breaking

A compatibility class that permits previously valid data to become invalid and allows semantic changes; explicit migration is required.

---

### Breaking change

A schema change that violates backward or forward compatibility guarantees and therefore requires `compatibilityClass=$Breaking`.

---

### Canonical authoring mode

The schema authoring mode where a Schema contains an RDF graph (`RdfGraph`) and omits the simplified definition containers.

---

### Canonical form

The single deterministic surface representation to which every valid Codex document must normalize.

---

### Canonical representation

The deterministic RDF/SHACL triple form defined by the specification for the canonical Codex `RdfGraph` form.

---

### Canonicalization

Deterministic formatting that converts a Codex document to canonical form without changing meaning.

---

### Character Value

A value representing exactly one Unicode scalar value, spelled as a single-quoted character literal.

---

### ChildConstraint

An atomic constraint that applies to child Concept relationships.

---

### ChildPath

A path that selects child Concepts identified by concept name.

---

### ChildRules

The ConceptDefinition section that declares allowed, required, or forbidden child Concepts.

---

### ChildSatisfies

A constraint requiring child Concepts to satisfy a nested rule.

---

### Closing marker

A `</Concept>` marker that ends a block Concept.

---

### Codex

The Codex Semantic Markup Language, a declarative semantic markup language with deterministic, schema-driven validation (a Paperhat product).

---

### Codex document

A document written in Codex surface form containing exactly one root Concept instance, optionally with a SchemaImports block.

---

### Collection value

A Value whose literal form contains multiple elements (List, Set, Map, Record, Tuple, or Range).

---

### CollectionAllowsDuplicates

A collection constraint that declares whether duplicate members are permitted.

---

### CollectionAllowsEmpty

A collection constraint that declares whether a collection may be empty.

---

### CollectionError

An error class for violations of schema-defined collection rules such as membership, ordering, or duplicate constraints.

---

### CollectionOrdering

A collection constraint that declares whether a collection is ordered or unordered.

---

### CollectionRules

The ConceptDefinition section that declares collection semantics and ordering.

---

### Compatibility class

The schema-declared relationship between a version and its immediate predecessor: Initial, BackwardCompatible, ForwardCompatible, or Breaking.

---

### Concept

A named declarative construct and the primary structural unit of a Codex document; it has Traits and either child Concepts or Content.

---

### Concept instance

A specific occurrence of a Concept in a document with a single name, traits, and a body mode.

---

### Concept marker

The surface-form marker that delimits a Concept instance (opening, closing, or self-closing).

---

### Concept name

The PascalCase name that identifies a Concept (optionally qualified by a namespace).

---

### ConceptDefinition

A schema concept that declares a Concept class and its structural, semantic, and identity rules.

---

### ConceptDefinitions

The container Concept in simplified schemas that holds ConceptDefinition entries.

---

### ConceptOption

A child of ExactlyOneChildOf that declares one option via a conceptSelector.

---

### Conformance graph

The RDF instance graph (G1) produced by the instance graph mapping and emitted in canonical RdfGraph form for conformance testing.

---

### Constraint model

The schema system for defining targets and rules that must hold for a document to be valid.

---

### ConstraintDefinition

A schema concept that declares a named constraint, its targets, and its rule.

---

### ConstraintDefinitions

The container Concept in simplified schemas that holds ConstraintDefinition entries.

---

### ConstraintError

An error class for violations of schema-defined constraints.

---

### Content

Opaque narrative text carried by a Concept in content mode; it is not a Value.

---

### Content block

The content lines inside a content-mode Concept after indentation normalization.

---

### Content mode

A Concept body mode in which it contains Content and no child Concepts.

---

### ContentConstraint

A constraint type that applies to a Concept's content.

---

### ContentPath

A path that selects content for constraint evaluation.

---

### ContentRules

The ConceptDefinition section that declares whether a Concept allows or forbids content.

---

### ContextConstraint

A constraint type that applies to contextual rules such as scope or environment.

---

### ContextError

An error class for violations of schema-defined context constraints.

---

### Count

A quantifier that requires a specific count of matches along a path.

---
