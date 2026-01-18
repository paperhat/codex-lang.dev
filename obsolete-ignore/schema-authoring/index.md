Status: NORMATIVE  
Version: 0.1  
Editor: Charles F. Munat

# Codex Schema Authoring Contract — Version 0.1

This document defines **how schemas are authored** in the Codex language.

Schema authoring rules are part of the Codex language specification and are governed
by this document.

This document is **Normative**.

---

## 1. Purpose

This contract defines **how Codex schemas are written**.

Its goals are to:

- make schema intent explicit and inspectable
- ensure consistent validation across tools
- prevent ambiguity between structure, meaning, and identity
- keep Codex declarative, deterministic, and low-cognitive-load

This contract governs **schema authoring responsibilities**, not surface syntax,
compilation, or runtime behavior.

---

## 2. Role of a Schema

A Codex schema is the **sole authority on meaning**.

A schema:

- defines **which Concepts exist**
- defines **which Traits are allowed** on those Concepts
- defines **which Concepts may be Entities**
- defines **collection semantics** (ordered vs unordered)
- defines **contextual meaning** for names

Codex surface syntax has no semantics without a schema.

---

## 3. Concept Definitions (Normative)

For each Concept, a schema MUST define:

- the Concept name
- whether the Concept is:
  - semantic
  - structural
  - value-like

- whether the Concept:
  - MUST be an Entity
  - MAY be an Entity
  - MUST NOT be an Entity

Schemas MUST NOT rely on naming conventions or heuristics to infer these properties.

---

## 4. Trait Authorization (Normative)

For each Concept, a schema MUST define:

- which Traits are allowed
- which Traits are required
- which Traits are forbidden

Traits are **never implicitly allowed**.

If a Trait is not explicitly authorized for a Concept, its presence is a validation
error.

---

## 5. Trait Semantics

Schemas define the meaning of Traits.

For each authorized Trait, a schema SHOULD define:

- expected Value type(s)
- cardinality (single vs multiple, if applicable)
- whether the Trait participates in identity or reference semantics

Schemas MAY define additional constraints, but MUST remain declarative.

---

## 6. Reference Traits

If a schema authorizes reference Traits (`reference`, `target`, `for`), it MUST define:

- which Concepts may declare them
- what kinds of Entities they may refer to
- whether exceptions to the singleton rule are permitted

Absent explicit schema authorization, reference Traits are mutually exclusive.

---

## 7. Domain Collections (Normative)

If a schema defines a domain collection Concept, it MUST specify:

- the member Concept type
- whether the collection is:
  - ordered
  - unordered

- whether empty collections are allowed
- whether duplicate membership is allowed

Schemas MUST NOT define collections that mix Concept types.

---

## 8. Ordering Semantics

Schemas are the **only authority** on ordering semantics.

For ordered collections:

- lexical order is semantically significant
- order MUST be preserved exactly

For unordered collections:

- lexical order has no semantic meaning
- lexical order MUST still be preserved textually

Schemas MUST NOT rely on numbering Traits to encode order.

---

## 9. Context Definition

Schemas define **contextual meaning**.

A schema MAY:

- define special meaning for Concepts within a specific parent Concept
- reuse Concept names that have different meaning in other schemas or contexts
- scope Structural Concepts to a particular assembly or domain

Schemas MUST document contextual meanings explicitly.

---

## 10. Validation Rules (Normative)

Schemas MUST define validation rules sufficient to determine:

- whether a Concept is well-formed
- whether Traits are valid and complete
- whether identity rules are satisfied
- whether collections conform to declared semantics

All schema validation MUST be deterministic and mechanically enforceable.

---

## 11. Error Responsibility

Schemas are responsible for making validation errors:

- precise
- attributable to a specific rule
- explainable without heuristics

Schemas MUST NOT rely on tool guesswork or best-effort interpretation.

---

## 12. Non-Goals

This contract does **not**:

- define a schema syntax
- mandate a schema language
- prescribe ontology modeling styles
- define inference rules
- define runtime or execution behavior

It defines **responsibilities and guarantees**, not mechanisms.

---

## 13. Summary

- Schemas are the sole source of meaning in Codex
- Nothing is implicit
- Concepts, Traits, identity, collections, and context are schema-defined
- Validation is deterministic and enforceable
- Codex remains declarative end-to-end

---

End of Codex Schema Authoring Contract v0.1.
