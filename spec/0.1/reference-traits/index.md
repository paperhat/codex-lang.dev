Status: NORMATIVE  
Lock State: UNLOCKED    
Version: 0.1  
Editor: Charles F. Munat

# **Codex Reference Traits Specification — Version 0.1 (FINAL, CORE)**

This specification defines the **reference Traits** used in the Codex language.

Reference Traits are part of the **core Codex language model** and are governed by
this specification.

This document is **Normative**.

---

# Codex Reference Traits Specification — Version 0.1

## 1. Purpose

This specification defines the **reference Traits** used in Codex.

Its goals are to:

* provide clear, plain-English naming for graph relationships
* prevent ambiguity between different kinds of references
* avoid programming-language or markup-system semantics
* ensure consistent reasoning by humans and machines

This specification defines **naming and semantic intent only**.
It does **not** define execution, inference, or runtime wiring.

---

## 2. Reference Traits Overview (Normative)

Codex defines exactly **three reference Traits**:

* `reference`
* `target`
* `for`

Each reference Trait:

* binds a Concept to another Concept by identifier (IRI) or lookup token
* has a distinct semantic intent
* is valid only where authorized by schema

Reference Traits are **mutually exclusive by default**.

---

## 3. `reference`

### Definition

`reference` is a Trait whose value is the identifier (IRI) or lookup token of another Concept.

### Intent

Use `reference` when a Concept:

* mentions another Concept
* depends on another Concept for meaning
* points to another Concept
* but does **not** apply to, act on, or scope it

`reference` carries **no implied direction or action**.

Plain-English reading:

> “This Concept references that Concept.”

---

## 4. `target`

### Definition

`target` is a Trait whose value is the identifier (IRI) or lookup token of another Concept.

### Intent

Use `target` when a Concept is:

* about another Concept
* applied to another Concept
* oriented toward another Concept as its focus

`target` is **directional and intent-bearing**.

Plain-English reading:

> “This Concept targets that Concept.”

---

## 5. `for`

### Definition

`for` is a Trait whose value is the identifier (IRI) or lookup token of another Concept.

### Intent

Use `for` when a Concept expresses:

* applicability
* scope
* specialization
* intended domain or audience

`for` answers the question:

> "Who or what is this for?"

It does **not** imply execution or transformation.

### Referencing Concept Types

When `for` references a **Concept type** (e.g., "this applies to all Books"), it references
the `ConceptDefinition` Entity for that Concept.

Since `ConceptDefinition` is itself an Entity (with a required `id` Trait), references
to Concept types are Entity references.

Example:

```cdx
<ConceptDefinition id=concept:Book key=~book name="Book" ... />

<LabelPolicy for=concept:Book ... />
<LabelPolicy for=~book ... />
```

Both forms reference the same Entity: the ConceptDefinition for Book.

---

## 6. Singleton Rule (Normative)

By default, a Concept MUST NOT declare more than one of:

* `reference`
* `target`
* `for`

A schema MAY explicitly authorize exceptions.
Any exception MUST be explicit and documented.

---

## 7. Schema Authority (Normative)

Schemas define:

* which Concepts may declare reference Traits
* which reference Trait is appropriate
* what kinds of Entities may be referenced
* whether singleton-rule exceptions are permitted

Codex surface syntax does not infer reference meaning.

---

## 8. Relationship to Identity

* Reference Traits bind to **identifiers** (IRIs or lookup tokens)
* Lookup tokens (`~token`) resolve to Concepts via the `key` Trait
* Reference resolution semantics are schema-defined

---

## 9. Non-Goals

This specification does **not**:

* define execution semantics
* prescribe inference rules
* mandate triple shapes
* replace domain-specific relationship modeling

---

## 10. Summary

* Codex defines exactly three reference Traits
* Each has a distinct semantic intent
* Reference Traits bind by identifier (IRI) or lookup token
* They are mutually exclusive by default
* Schemas govern authorization and meaning

---

**End of Codex Reference Traits Specification v0.1**

---
