# Codex Entity Eligibility Contract (DRAFT)

## Status

- **DRAFT**  
- Normative once locked  
- Applies to all Codex schemas, documents, and tooling that assign identity

---

## 1. Purpose

This contract defines **when a Concept may be an Entity** in Codex.

Its goals are to:

- prevent accidental identity proliferation
- keep the semantic graph intentional and inspectable
- separate **things** from **structure** and **values**
- make identity a deliberate schema decision, not a syntactic convenience

---

## 2. Core Definitions

### Concept

A **Concept** is a named declarative unit in Codex.

Concepts may be semantic, structural, or value-like.

---

### Entity

An **Entity** is a Concept with identity.

> A Concept is an Entity **if and only if** it declares an `id` Trait.

No other mechanism confers identity.

---

## 3. Identity Is Explicit (Normative)

Identity in Codex is **never implicit**.

- Declaring an `id` Trait:
  - makes a Concept an Entity
  - asserts graph identity
  - allows other Concepts to reference it

- Absence of an `id`:
  - means the Concept is not an Entity
  - means it is not graph-addressable as a standalone thing

There are no anonymous Entities.

---

## 4. Schema Authority (Normative)

Whether a Concept **may**, **must**, or **must not** be an Entity is defined by schema.

Surface syntax does not determine eligibility.

Schemas MUST specify, for each Concept they define, one of the following:

- **Entity-required**
  The Concept MUST declare an `id`.

- **Entity-optional**
  The Concept MAY declare an `id`.

- **Entity-forbidden**
  The Concept MUST NOT declare an `id`.

Assigning an `id` contrary to schema is a validation error.

---

## 5. Typical Eligibility Classes (Informative)

The following patterns are typical, but not automatic.

### 5.1 Domain Concepts

Concepts that represent enduring domain things are often Entities.

Examples:

- `Recipe`
- `Person`
- `User`
- `Policy`
- `Module`

---

### 5.2 Structural Concepts

Structural Concepts are **not** Entities by default.

Examples:

- `Data`
- `Views`
- `Policies`
- `Steps`
- `Groups`

Structural Concepts MUST NOT declare an `id` unless explicitly authorized by schema.

---

### 5.3 Value-like Concepts

Concepts whose role is purely structural or value-carrying are not Entities.

Examples:

- `Step`
- `Description`
- `Notes`
- formatting or sectioning Concepts

These Concepts MUST NOT be Entities unless schema explicitly allows it.

---

## 6. Consequences of Identity (Normative)

Declaring an `id`:

- commits the Concept to graph identity
- allows long-lived references
- implies persistence beyond local structure
- makes the Concept queryable and addressable

Identity is a **semantic commitment**, not a convenience.

---

## 7. Prohibited Patterns (Normative)

The following are invalid in Codex:

- Assigning `id` to every Concept “just in case”
- Using `id` to encode position or order
- Treating `id` as a syntactic label rather than identity
- Assuming child Concepts inherit identity from parents

Each Entity stands on its own.

---

## 8. Relationship to Domain Collections

- Members of a domain collection MAY be Entities if schema allows.
- Membership in a collection does not imply identity.
- Ordered collections do not require Entity identity for their members.

Identity and ordering are orthogonal concerns.

---

## 9. Non-Goals

This contract does **not**:

- define identifier formats
- mandate global uniqueness strategies
- prescribe persistence mechanisms
- define reference resolution behavior
- replace schema-level modeling decisions

---

## 10. Summary

- Identity in Codex is explicit and intentional
- A Concept is an Entity **iff** it has an `id` Trait
- Schema governs eligibility
- Structural and value-like Concepts are not Entities by default
- Identity is a semantic commitment, not a syntactic one
