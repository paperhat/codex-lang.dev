Status: DRAFT

# Codex Glossary (D-F)

This file contains glossary entries for terms starting with D-F.

See `../index.md` for format notes and other ranges.

[A–C](../a-c/index.md) | **D–F** | [G–I](../g-i/index.md) | [J–L](../j-l/index.md) | [M–O](../m-o/index.md) | [P–R](../p-r/index.md) | [S–U](../s-u/index.md) | [V–Z](../v-z/index.md)

## Terms

### Data Document

A Codex document whose Concepts represent individuals in the governing schema.

---

### DescendantPath

A path that selects descendant Concepts identified by concept name.

---

### Determinism

The requirement that the same inputs yield the same outputs for parsing, validation, and canonicalization.

---

### Document node

The RDF node representing the document in the instance graph, identified by documentBaseIri.

---

### Document node shape IRI

The deterministic node shape IRI for the document node, derived from the schema IRI.

---

### Domain Schema

A schema document intended to define Concepts for data documents (for example, Recipe, Essay, Organization).

---

### EachMemberSatisfies

A collection constraint requiring each member to satisfy a nested rule.

---

### Email Address Value

A value spelling `email(...)` that represents an email address with a Unicode local part and ASCII domain.

---

### Entity

A Concept instance with explicit identity, permitted and required by the governing schema's entityEligibility rule.

---

### Enumerated Token Value

A value from a schema-defined closed set, spelled with a leading `$` and a PascalCase token.

---

### EnumeratedConstraint

An AllowedValues child that constrains a trait using an EnumeratedValueSet.

---

### EnumeratedValueSet

A schema concept defining a closed set of enumerated tokens with an identity IRI.

---

### EnumeratedValueSets

The container Concept in simplified schemas that holds EnumeratedValueSet entries.

---

### ExactlyOneChildOf

A ChildRules entry requiring that exactly one of its ConceptOption children appear.

---

### Exists

A quantifier requiring at least one match along a path.

---

### for trait

A reference trait expressing applicability, scope, or intended domain toward another Concept.

---

### ForAll

A quantifier requiring all matches along a path to satisfy a rule.

---

### ForbidsChildConcept

A ChildRules entry declaring that a child Concept type must not appear.

---

### ForbidsContent

A ContentRules entry declaring that a Concept must not contain content.

---

### ForbidsTrait

A TraitRules entry declaring that a trait is not permitted.

---

### FormattingError

An error class for inputs that parse and meet surface rules but cannot be deterministically canonicalized.

---

### ForwardCompatible

A compatibility class guaranteeing that data authored for this version can validate under the immediately preceding version.

---
