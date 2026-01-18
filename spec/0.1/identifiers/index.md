# Codex Identifier Specification — Version 0.1

## 1. Purpose

This specification defines **identity in Codex**.

Its goals are to:

* make identity explicit and unambiguous
* support graph construction and querying
* avoid ontology explosion
* preserve semantic density
* decouple identity from structure, storage, and transport

This document governs **what an identifier is**, not how it is resolved,
stored, normalized, or dereferenced.

---

## 2. What an Identifier Is (Normative)

An **identifier (`id`)** is a **stable, globally meaningful name** for an **Entity**.

In Codex:

* identifiers are **semantic**
* identifiers are **explicitly declared**
* identifiers identify **things with meaning**, not containers or syntax

An identifier names an **ontological individual**.

---

## 3. Entity vs. Non-Entity (Normative)

A Concept is an **Entity if and only if it declares an `id` Trait**.

### 3.1 Why Not Everything Is an Entity

Not all Concepts carry sufficient semantic weight to justify identity.

Entities represent **high-semantic-density concepts**:

* things that participate meaningfully in an ontology
* things worth naming, referencing, and reasoning over
* things that appear as nodes in a graph

Non-Entities represent **low-semantic-density constructs**:

* narrative text (`<Description>`)
* structural grouping
* auxiliary or descriptive material
* values that exist *about* Entities, not *as* Entities

This distinction exists to:

* prevent uncontrolled class explosion
* keep ontologies tractable
* avoid meaningless nodes in graphs
* preserve conceptual clarity

Example:

* `Flour` → Entity (ontological concept)
* `"all-purpose flour"` → Value or Content (qualifier, not ontology node)

Schemas control this boundary explicitly.

---

## 4. Identifier Form (Normative)

All identifiers MUST be **IRI references**.

Rules:

* identifiers MUST be written as **unquoted tokens**
* identifiers MUST contain no whitespace
* identifiers are treated as **opaque strings**
* Codex does not validate full IRI grammar

Codex does **not** require identifiers to be dereferenceable.

---

## 5. Stability and Immutability (Normative)

Identifiers are **stable**.

Once assigned:

* an identifier MUST continue to refer to the same Entity
* identifiers MUST NOT be reused
* identifiers MUST NOT be repurposed

Changing an identifier creates a **new Entity**.

---

## 6. Identity Is Not Presentation

Identifiers:

* are not labels
* are not human-facing text
* MUST NOT encode presentation, ordering, or formatting
* MUST NOT change for cosmetic reasons

Human-readable naming belongs in other Traits or Content.

---

## 7. Reference Relationship (Normative)

Identifiers are the **only mechanism** by which Concepts may refer to Entities.

* reference Traits bind to identifiers
* references are semantic, not structural
* referencing a non-Entity is a validation error

Reference meaning is governed by the Reference Traits specification.

---

## 8. Schema Authority

Schemas MUST define:

* which Concepts MAY declare an `id`
* which Concepts MUST declare an `id`
* which Concepts MUST NOT declare an `id`

Codex syntax never infers identity.

---

## 9. Non-Goals

This specification does **not**:

* define identifier resolution
* define namespaces or prefixes
* mandate UUIDs
* define registries
* define base IRIs
* define normalization or canonicalization

Those concerns belong to **tooling or dialects**, not the language core.

---

## 10. Summary

* Identity is explicit and semantic
* Entities are high-semantic-density Concepts
* Not everything should be an Entity
* Identifiers are IRIs, opaque, and stable
* Schemas are the sole authority on identity

---

**End of Codex Identifier Specification v0.1**
