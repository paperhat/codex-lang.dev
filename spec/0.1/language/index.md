Status: NON-NORMATIVE (Historical; consolidated into codex-language-specification.md §§2–7)
Lock State: UNLOCKED
Version: 0.1
Editor: Charles F. Munat

# Codex Language Specification — Version 0.1

This document is retained for historical/reference purposes.

The authoritative normative content is consolidated into `spec/0.1/codex-language-specification.md`.

## Language Definition

This document defines the **Codex language itself**.

It specifies the **foundational language model, semantics, and invariants** that
apply to all Codex documents, schemas, and tooling.

---

## Role of This Document

This document is the **authoritative definition of Codex as a language**.

It defines:

* what Codex is
* what Codex constructs mean
* the invariants all Codex tooling MUST respect
* the boundaries of Codex responsibility

It does **not** define implementation, runtime, or pipeline behavior.

---

## What Codex Is

**Codex is a declarative language for meaning.**

Codex is designed to describe:

* ontologies and schemas
* structured data
* configuration and policy
* constraints and validation rules
* relationships between entities
* presentation intent (as data)

Codex is especially suited to **conversion into graph representations**
(e.g. RDF triples) but does not require any particular backend or target.

---

## What Codex Is Not

Codex is **not**:

* a programming language
* a scripting language
* a templating language
* a markup language for rendering
* a runtime or execution environment

Codex expresses **what is declared**, never **how it is executed**.

---

## Declarative and Closed-World Model

Codex operates as a **closed declarative system**.

This means:

* all meaning MUST be explicitly declared
* nothing is inferred implicitly
* no defaults are assumed unless explicitly specified by a governing specification
  (e.g., schema-language defaults in `spec/0.1/schema-definition/index.md`) or by
  schema rules
* no heuristics are permitted

If something is not declared, it does not exist.

---

## Determinism

Given the same Codex input:

* parsing MUST be deterministic
* validation MUST be deterministic
* canonicalization MUST be deterministic

Codex tooling MUST be able to explain:

* why a document is valid or invalid
* which rule was applied
* which declaration caused an outcome

Non-deterministic or heuristic behavior is forbidden.

---

## Schema-First Parsing

Codex is a **schema-first language**.

This means:

* semantic interpretation and validation MUST have access to the governing schema
* schema-directed structural interpretation (e.g., children vs Content) is performed
  using schema declarations
* a document cannot be **validated** without a schema
* schema provisioning and schema-document bootstrapping requirements are defined
  by the **Schema Loading Specification** (`spec/0.1/schema-loading/index.md`)

Codex also permits an abbreviated, schema-less stage used for well-formedness and
canonical formatting checks (see the **Formatting and Canonicalization
Specification**).

### Rationale

Codex documents are meaningless without a schema. The schema is the sole
authority on meaning. Schema-first parsing makes this architectural reality
explicit at the language level.

Schema-first parsing:

* eliminates syntactic ambiguity between children mode and content mode
* produces precise, attributable parse errors
* aligns with semantic web tooling expectations (OWL, SHACL)
* ensures semantic interpretation is schema-governed

### Schema-Directed Content Mode

Whether a Concept's body contains child Concepts or opaque Content is determined
by the schema, not by inspecting the body text.

The normative parsing/dispatch rules are defined in:

* the **Surface Form Specification** (schema-directed dispatch)
* the **Schema Definition Specification** (`ContentRules`)

### Implications

* Semantic validation requires schema availability
* Tools MAY support schema-less well-formedness and canonical formatting checks
  that do not require a governing schema
* Schema-document bootstrapping is defined by the **Schema Loading
  Specification** (`spec/0.1/schema-loading/index.md`) and the **Bootstrap
  Schema-of-Schemas Definition** (`spec/0.1/schema-loading/bootstrap-schema-of-schemas/index.md`)

### What Schema-First Is Not

Schema-first parsing does not mean:

* the parser performs full semantic validation during parsing
* constraint evaluation happens at parse time
* all schema errors are parse errors

The parser uses the schema to determine **structure** (which Concepts exist,
whether they take children or content). Full semantic validation (constraints,
cardinality, reference resolution) remains a separate phase.

See the **Schema Loading Specification** for how schemas are provided to parsers.

---

## Concepts, Traits, Values, and Content

Codex is composed of four fundamental elements. Complete definitions appear in the
**Naming and Value Specification § 2**. This section describes their role in the
language model.

### Concepts

A **Concept** is a named declarative construct.

Concepts:

* may declare Traits
* may contain child Concepts OR Content (never both)
* may or may not be Entities (see below)

Concepts are the primary structural unit of Codex.

---

### Traits

A **Trait** binds a name to a Value.

Traits:

* are schema-authorized
* have no independent identity
* do not imply semantics without schema definition

---

### Values

A **Value** is a literal datum.

Values:

* are immutable
* are not expressions
* are not evaluated by Codex

Codex defines rich first-class Value forms. See the **Naming and Value
Specification § 4** for the complete catalog of literal value spellings.

Codex parses Value spellings but does not interpret their meaning.
Interpretation is the responsibility of schemas and consuming systems.

---

### Content

**Content** is opaque narrative data.

Content:

* is not a Value
* is not typed
* is not interpreted by Codex
* may contain arbitrary text

Content exists to carry human-authored material that is outside the semantic
model.

---

## Entities and Semantic Density

The formal definition of **Entity** is in the Naming and Value Specification
(`spec/0.1/naming-and-values/index.md`, **§ 2.5 Entity**).

Entity eligibility is schema-governed; see the Schema Definition Specification
(**§ 4.1** `entityEligibility`).

This section describes the role of Entities in the language model.

Entities:

* have semantic identity
* participate in graph identity
* may be referenced by other Concepts
* are intended to represent ontologically meaningful units

Non-Entity Concepts:

* do not have identity
* do not participate directly in ontology graphs
* exist to structure, describe, or annotate Entities

This distinction exists to control **semantic density**.

Codex deliberately avoids treating every Concept as a first-class ontological
entity in order to:

* prevent ontology explosion
* preserve clarity of meaning
* keep graphs semantically tractable

Schemas are responsible for deciding which Concepts carry identity.

---

## Canonical Form

The normative canonical form requirement and canonicalization rules are defined
by the **Formatting and Canonicalization Specification**
(`spec/0.1/formatting-and-canonicalization/index.md`).

Canonical form exists to support:

* stable diffs
* reliable round-tripping
* tool interoperability

---

## Separation of Responsibility

Codex enforces strict separation between:

* language semantics
* schema-defined meaning
* validation and constraints
* storage, querying, or inference
* rendering or execution

Codex defines **what is declared**, not **what is done with it**.

---

## Target Agnosticism

Codex is **target-agnostic**.

The same Codex document MAY be transformed into:

* graph representations
* configuration formats
* serialized data
* rendered outputs
* other languages

No Codex construct may assume a specific target or runtime.

---

## Relationship to Other Specifications

This document defines **language-level semantics only**.

It must be read in conjunction with:

* Naming and Value Specification
* Surface Form Specification
* Formatting and Canonicalization Specification
* Identifier Specification
* Reference Traits Specification
* Schema Definition Specification
* Schema Loading Specification
* Validation Error Taxonomy

In case of conflict, this document defines the **language invariants**.

---

## Stability

This document is retained for historical/reference purposes and was Normative prior to consolidation.

Changes are governed by repository governance and editorial control.

---

## Summary

* Codex is a declarative language for meaning
* It is closed-world, deterministic, and explainable
* Codex is schema-first: parsing requires schema access
* Schemas are the sole source of semantics
* Entities represent semantic density boundaries
* Canonical form is mandatory
* Execution, storage, and rendering are outside the language

---

**End of Codex Language Specification v0.1**
