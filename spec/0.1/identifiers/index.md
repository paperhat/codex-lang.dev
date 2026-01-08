# Codex Identifier Contract (DRAFT)

## Status

- **DRAFT**
- Normative once locked
- Applies to all Codex schemas, documents, and tooling that use `id` Traits

---

## 1. Purpose

This contract defines what an **identifier (`id`)** is in Codex.

Its goals are to:

- make identity precise and unambiguous
- ensure identifiers are globally safe and semantically meaningful
- support stable graph construction and reference
- avoid accidental coupling to storage, runtime, or transport concerns

This contract governs **identifier meaning and form**, not persistence or resolution mechanisms.

---

## 2. What an Identifier Is

An **identifier** is a **stable, globally unique name** for an Entity.

In Codex:

- identifiers are **semantic**, not positional
- identifiers are **declared**, not inferred
- identifiers identify the **Entity itself**, not its representation

Identifiers are used exclusively via the `id` Trait.

---

## 3. Identifiers Are IRIs (Normative)

All Codex identifiers MUST be **IRIs**.

- They MUST be globally unique in intent
- They MUST be usable as graph identifiers
- They MUST be comparable as opaque strings

Codex does not require identifiers to be dereferenceable.

---

## 4. Identifier Form (Normative)

Codex does not mandate a single concrete syntax, but identifiers MUST conform to the following constraints:

- MUST be a valid IRI
- MUST NOT depend on file paths, offsets, or document structure
- MUST NOT encode ordering or position
- MUST NOT rely on implicit context for uniqueness

Examples (illustrative):

- `recipe:spaghetti`
- `user:chas`
- `module:recipes`
- `policy:recipe:standard`

The choice of namespace scheme is a schema and project concern.

---

## 5. Stability and Immutability (Normative)

Identifiers are **stable**.

Once assigned:

- an identifier MUST continue to refer to the same Entity
- identifiers MUST NOT be reused for different Entities
- identifiers MUST NOT be repurposed

Changing an identifier creates a **new Entity**.

---

## 6. Identity vs Labels

Identifiers are **not labels**.

- Identifiers are not intended for display
- Human-readable names belong in other Traits (e.g. `name`, `title`)
- Identifiers SHOULD remain stable even if labels change

Do not encode presentation concerns into identifiers.

---

## 7. Relationship to References

- Reference Traits (`reference`, `target`, `for`) use identifiers as their Values
- References MUST point to valid Entity identifiers
- Referencing a non-Entity is a schema or validation error

Identifiers are the **only** way Concepts may refer to other Entities.

---

## 8. Scope and Namespaces

Codex does not impose a global namespace registry.

- Projects MAY define their own namespace conventions
- Schemas SHOULD document expected identifier patterns
- Tools MUST treat identifiers as opaque values

Codex does not interpret namespace prefixes.

---

## 9. Prohibited Identifier Uses (Normative)

The following are invalid uses of identifiers:

- using identifiers as ordering keys
- embedding document structure or hierarchy
- encoding version numbers into identifiers
- using identifiers as mutable state
- auto-generating identifiers implicitly without schema authorization

Identifiers are not metadata dumps.

---

## 10. Non-Goals

This contract does **not**:

- require identifiers to resolve over HTTP
- mandate UUIDs or specific encodings
- define identifier minting workflows
- define cross-module resolution rules
- prescribe registry or catalog mechanisms

---

## 11. Summary

- Identifiers are explicit, semantic, and stable
- All identifiers are IRIs
- Identifiers identify Entities, not representations
- Schema governs identifier usage
- Identifiers are opaque, not structural
