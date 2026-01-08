# Codex Glossary (DRAFT)

## Status

- **DRAFT**  
- Normative once locked  
- This document introduces **no new rules**
- It mirrors terminology defined in Codex contracts

---

## Purpose

This glossary defines the **canonical vocabulary** used throughout Codex.

Its purpose is to:

- provide quick, authoritative definitions
- reduce cognitive load for readers
- prevent terminology drift across documents, tooling, and discussion
- ensure consistent reasoning by humans and LLMs

All terms defined here are governed by their respective contracts.

---

## Core Terms

### Concept

A **Concept** is the primary surface construct in Codex.

A Concept is a named, declarative unit composed of Traits and child Concepts.
Some Concepts represent domain meaning; others are structural.

A Concept may or may not be an Entity.

Examples:

- `Recipe`
- `Step`
- `Policy`
- `Module`

---

### Trait

A **Trait** is a named distinguishing characteristic of a Concept.

A Trait binds a name to a Value and is declared inline on a Concept.
Traits have no independent identity and are authorized by schema.

Examples:

- `name="Bob"`
- `amount=200`
- `optional=false`

---

### Value

A **Value** is a literal datum bound to a Trait.

Values may be strings, numbers, or booleans.
They are immutable, schema-typed, and non-narrative.

Examples:

- `"Bob"`
- `200`
- `true`

---

### Content

**Content** is opaque narrative data carried by a Concept.

Content is not interpreted by Codex and may include prose, code, poetry, or other markup.
Codex preserves Content but does not assign it semantic meaning.

Typical carrier Concepts include:

- `Description`
- `Notes`

---

### Entity

An **Entity** is a Concept with identity.

A Concept is an Entity **if and only if** it declares an `id` Trait.
Entities are graph-addressable and may be referenced by other Concepts.

Examples:

- `Recipe` with an `id` → Entity
- `Step` without an `id` → not an Entity

---

## Identity and Reference Terms

### id

`id` is a Trait that assigns identity to a Concept.

Declaring an `id` Trait makes a Concept an Entity.
Only Concepts authorized by schema may declare an `id`.

---

### Marker

A **Marker** is a surface-form syntactic construct that denotes the boundary of a Concept instance.

Markers include:

- opening Concept markers (e.g. `<Recipe>`)
- closing Concept markers (e.g. `</Recipe>`)
- self-closing Concept markers (e.g. `<Title />`)

Markers are not Concepts and carry no semantic meaning.
They exist solely to delimit Concepts in the Codex surface form.

---

### reference

`reference` is a Trait whose Value is the identifier (IRI) of another Entity.

It represents a generic declarative link with no implied direction or action.

---

### target

`target` is a reference Trait indicating the Entity that a Concept is about, applied to, or oriented toward.

It is directional and intent-bearing.

---

### for

`for` is a reference Trait indicating applicability or scope.

It expresses that a Concept exists for, applies to, or specializes another Entity or Concept kind.
It does not imply action or wiring.

---

## Annotation Terms

### Annotation

An **Annotation** is a non-normative, author-supplied textual note preserved through the Codex pipeline.

Annotations:

- do **not** affect validation
- do **not** alter domain semantics
- are intentionally preserved for round-tripping, tooling, and inspection

Annotations are **not comments** and are not disposable.

---

### Editorial Annotation

An **Editorial Annotation** is an annotation intended for authors and tooling.

Editorial Annotations:

- are authored using bracket syntax (`[ ... ]`) in the surface form
- attach to the **next Concept** in document order
- are preserved through IR and triple storage
- are ignored by default in rendered outputs (HTML, PDF, voice)

They function like editorial margin notes.

---

### Output Annotation

An **Output Annotation** is an annotation explicitly authored as a Concept.

Output Annotations:

- are authored using the `<Annotation>` Concept
- attach to their **parent Concept**
- carry opaque Content
- MAY be rendered or spoken by downstream targets

Output visibility is explicit and intentional.

---

### Annotation Kind

An **Annotation Kind** is a schema-defined classification describing the intent of an annotation.

Typical kinds include:

- `note`
- `warning`
- `todo`
- `rationale`
- `question`
- `example`
- `provenance`

Annotation kinds do not affect domain semantics.

---

## Structural and Semantic Terms

### Structural Concept

A **Structural Concept** organizes or groups other Concepts.

Structural Concepts do not express domain meaning on their own; their meaning is contextual and schema-defined.

Examples:

- `Steps`
- `Data`
- `Policies`
- `Views`

---

### Semantic Concept

A **Semantic Concept** expresses domain meaning.

Semantic Concepts typically represent domain entities, values, or rules.

Examples:

- `Recipe`
- `Person`
- `Permission`

---

## Context and Scope

### Context

A **Context** is a schema-defined semantic scope in which Concept and Trait names are interpreted.

Names in Codex do not have global meaning; the same name may have different meaning in different contexts.

---

### Module (Contextual)

Within a Codex module-assembly context, `Module` is a Structural Concept representing a semantic assembly of heterogeneous artifacts.

Outside that context, `Module` has no intrinsic meaning unless defined by another schema.

---

## Naming Conventions (Summary)

- Concept names use **PascalCase**
- Trait names use **camelCase**
- Abbreviations are avoided in naming
- Initialisms and acronyms capitalize only the first letter
- Naming rules apply only to identifiers, not to Content

---

## Forbidden Vocabulary (Reminder)

The following terms must not be used to describe Codex constructs:

- element
- component
- tag
- node
- class
- prop
- property
- attribute
- field
- parameter
- comment
- code comment
- HTML comment
- XML comment

Use **Concept**, **Trait**, and **Annotation** instead.

---

## Closing Note

This glossary is a **reference mirror**, not a design surface.

All authoritative rules are defined in the Codex contracts.
