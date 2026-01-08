# Codex Reference Traits Contract (DRAFT)

## Status

- **DRAFT**  
- Normative once locked  
- Applies to all Codex schemas, documents, and tooling that use reference Traits

---

## 1. Purpose

This contract defines the **reference Traits** used in Codex.

Its goals are to:

- provide clear, plain-English naming for graph relationships
- prevent ambiguity between different kinds of references
- avoid legacy markup and programming-language semantics
- ensure consistent reasoning by humans, tools, and LLMs

This contract defines **naming and intent only**.
It does **not** define execution, behavior, or inference rules.

---

## 2. Reference Traits Overview

Codex defines **three reference Traits**:

- `reference`
- `target`
- `for`

Each reference Trait:

- binds a Concept to another Entity by identifier (IRI)
- has a distinct **semantic intent**
- is authorized only where allowed by schema

Reference Traits are **mutually exclusive by default**.

---

## 3. `reference`

### Definition

`reference` is a Trait whose Value is the identifier (IRI) of another Entity.

It represents a **generic declarative link**.

### Intent

Use `reference` when a Concept:

- mentions another Entity
- depends on another Entity for meaning
- needs to point to another Entity
- but does **not** act on, apply to, or specialize it

`reference` carries **no implied direction**, action, or applicability.

### Examples (Illustrative)

- A recipe referencing an ingredient Entity
- A policy referencing a role Entity
- A view referencing a Concept it mentions but does not operate on

Plain English reading:

> “This Concept references that Entity.”

---

## 4. `target`

### Definition

`target` is a reference Trait whose Value is the identifier (IRI) of another Entity.

### Intent

Use `target` when a Concept is:

- about another Entity
- applied to another Entity
- oriented toward another Entity
- defined in terms of another Entity as its focus

`target` is **directional and intent-bearing**.

### Examples (Illustrative)

- A view whose purpose is to present a specific Recipe
- A policy that constrains a particular Entity
- A plan that transforms or produces a specific Entity

Plain English reading:

> “This Concept targets that Entity.”

---

## 5. `for`

### Definition

`for` is a reference Trait whose Value is the identifier (IRI) of another Entity or Concept kind.

### Intent

Use `for` when a Concept expresses:

- applicability
- scope
- specialization
- intended audience or domain

`for` answers the question:

> “Who or what is this _for_?”

It does **not** imply action, wiring, execution, or transformation.

### Examples (Illustrative)

- A view definition that applies to all Recipes (a view _for Recipe_)
- A policy that applies to all Users (a policy _for User_)
- A configuration Concept that applies to a subsystem Concept

Plain English reading:

> “This Concept is for that Concept or Entity.”

---

## 6. Singleton Rule (Normative)

By default, a Concept MUST NOT declare more than one of the following Traits:

- `reference`
- `target`
- `for`

A schema MAY explicitly permit exceptions, but such exceptions must be documented.

This rule prevents ambiguous or conflicting reference intent.

---

## 7. Schema Authority

- Reference Traits are **never global**
- Their validity and interpretation are defined by schema
- Schemas determine:
  - which Concepts may declare reference Traits
  - which reference Trait is appropriate
  - whether exceptions to the singleton rule are allowed

Codex surface syntax does not infer reference meaning.

---

## 8. Non-Goals

This contract does **not**:

- define execution semantics
- imply runtime behavior
- prescribe inference rules
- mandate specific triple structures
- replace domain-specific relationship modeling

It exists solely to standardize **naming and intent**.

---

## 9. Summary

- Codex defines three reference Traits: `reference`, `target`, and `for`
- All reference Traits bind to another Entity by identifier (IRI)
- Each has a distinct plain-English intent
- Reference Traits are mutually exclusive by default
- Schema governs authorization and meaning
