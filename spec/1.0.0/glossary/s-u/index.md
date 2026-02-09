Status: DRAFT

# Codex Glossary (S-U)

This file contains glossary entries for terms starting with S-U.

See `../index.md` for format notes and other ranges.

[A–C](../a-c/index.md) | [D–F](../d-f/index.md) | [G–I](../g-i/index.md) | [J–L](../j-l/index.md) | [M–O](../m-o/index.md) | [P–R](../p-r/index.md) | **S–U** | [V–Z](../v-z/index.md)

## Terms

### Schema

The `Schema` Concept that defines a governing Codex schema and its validation rules.

---

### Schema definition language

The part of Codex that defines how schemas, constraints, and value types are declared.

---

### Schema Document

A Codex document whose Concepts define a schema (Concept definitions, Trait definitions, constraints, value types, and validators).

---

### Schema Import

A declaration within a `SchemaImports` block that binds a namespace label to an imported schema IRI. Each `SchemaImport` has a required `reference` trait (the schema IRI) and a required `namespace` trait (the author's label, canonicalized to the imported schema's declared namespace). Defined in §11.3.1.

---

### Schema Import Set

A `SchemaImports` block that declares which schemas are in scope for a document and what namespace each schema uses.

---

### Schema Registry

A tooling-level mapping from schema IRI to local source path. The registry is not part of canonical semantics.

---

### Schema validation

Semantic validation of a well-formed Codex document against an explicit governing schema.

---

### Schema version

The version identifier declared by a schema's `version` trait.

---

### Schema-less formatting

Formatting and canonicalization performed without a governing schema, enforcing only surface rules.

---

### SchemaError

An error class for violations of schema-defined rules.

---

### SchemaImports

A language-level child concept permitted on any root concept (schema or data document). Contains one or more `SchemaImport` children declaring which external schemas are in scope. The governing schema's definitions are the default namespace; only imported definitions require qualified names. Defined in §11.3.1.

---

### Self-closing marker

A `<Concept />` marker representing a Concept with no children and no content.

---

### Set Value

An unordered collection value spelled as `set[...]`.

---

### Simplified authoring mode

The schema authoring mode where schemas are declared using ConceptDefinition, TraitDefinition, and other simplified containers.

---

### Singleton rule

The rule that at most one of `reference`, `target`, or `for` may appear, expressed via ReferenceConstraint(type=ReferenceSingleton).

---

### SurfaceFormError

An error class for violations of surface-form requirements after parsing succeeds.

---

### Target agnosticism

The principle that Codex does not assume any specific target format, runtime, or storage backend.

---

### target trait

A reference trait expressing that a Concept is about or oriented toward another Concept.

---

### TargetConcept

A constraint target that selects Concepts of a given type.

---

### TargetContext

A constraint target that selects a context for evaluation.

---

### Temporal keyword

A symbolic temporal literal such as `{now}` or `{today}` that is not evaluated unless a schema requires it.

---

### Temporal Value

A declarative temporal literal spelled with `{...}` and classified by its syntax.

---

### Text Value

A sequence of Unicode scalar values spelled as quoted text or backtick text and normalized for whitespace.

---

### Trait

A name-value binding declared on a Concept.

---

### Trait Bundle Schema

A domain schema whose primary purpose is to define reusable Trait definitions (for example, identity, title, language, timestamps) for composition in other schemas.

---

### Trait instance

A specific occurrence of a Trait on a Concept.

---

### Trait name

The camelCase name that identifies a Trait.

---

### TraitCardinality

A trait constraint that limits the number of values bound to a trait.

---

### TraitDefinition

A schema concept that declares a trait's name, value type, and semantics.

---

### TraitDefinitions

The container Concept in simplified schemas that holds TraitDefinition entries.

---

### TraitEquals

A trait constraint requiring a trait value to equal a specified value.

---

### TraitExists

A trait constraint requiring a trait to be present.

---

### TraitLessOrEqual

A trait constraint asserting that one numeric trait value is less than or equal to another.

---

### TraitMissing

A trait constraint requiring a trait to be absent.

---

### TraitPath

A path that selects trait values by trait name.

---

### TraitRules

The ConceptDefinition section that declares allowed, required, or forbidden traits.

---

### TraitValueType

A trait constraint that constrains a trait's value type.

---

### Tuple Value

An ordered sequence of one or more values spelled with parentheses (`(...)`).

---

### Unordered collection ($Unordered)

A collection whose member order is not semantically significant and may be deterministically sorted in canonicalization.

---

### URL Value

A value spelling `url(...)` that represents an absolute URL.

---

### UUID Value

A 36-character hexadecimal identifier with hyphens in the canonical UUID shape.

---
