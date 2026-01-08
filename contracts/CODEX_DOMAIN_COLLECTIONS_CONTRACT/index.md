# Codex Domain Collections Contract (DRAFT)

## Status

- **DRAFT**
- Normative once locked
- Applies to all Codex documents using domain collection concepts

---

## 1. Purpose

This document defines **domain collection concepts** in Codex.

A domain collection is a semantic construct used to collect **multiple individuals of the same domain class** (e.g. Recipes, Songs, Events) into a single structured grouping.

Domain collections are **part of the domain model**, not meta-containers or packaging constructs.

---

## 2. What a Domain Collection Is

A domain collection:

- groups **individuals of a single class**
- is defined by the **domain ontology/schema**
- may be **ordered** or **unordered**
- compiles directly to triples as collection membership
- does **not** mix document kinds (data vs view vs policy)

Example:

```xml
<Recipes>
	<Recipe id="recipe:spaghetti">…</Recipe>
	<Recipe id="recipe:cacio-e-pepe">…</Recipe>
</Recipes>
```

A domain collection may appear either as the **root concept** of a Codex file or as a **child concept within a Module**.

---

## 3. Schema Authority

Domain collections are **schema-defined**, not ad hoc.

For each collection concept (e.g. `<Recipes>`), the schema MUST define:

- the **member class** (e.g. `Recipe`)
- whether the collection is:
  - an **ordered sequence**
  - or an **unordered bag**

- whether duplicate membership is allowed
- whether empty collections are allowed

Codex files **use** domain collections; they do not define them.

---

## 4. Ordering Semantics

### 4.1 Ordered collections

If a collection is declared **ordered** in the schema:

- lexical order of child concepts is **semantically significant**
- order must be preserved exactly
- ordering must be represented in triples (e.g. RDF list or explicit ordering predicates)

Typical use cases:

- recipe steps
- musical movements
- procedural sequences
- ranked lists

Example:

```xml
<Steps>
	<Step>Boil water.</Step>
	<Step>Add pasta.</Step>
	<Step>Drain.</Step>
</Steps>
```

No numbering is required or allowed to encode order.

---

### 4.2 Unordered collections (bags)

If a collection is declared **unordered**:

- membership is semantic
- lexical order has **no semantic meaning**
- lexical order must still be preserved textually
- canonical formatting **must not reorder concepts**

Typical use cases:

- tags
- ingredients (when order does not matter)
- contributors
- references

---

## 5. Identity Rules

- Member concepts **may** have IDs if they are graph-addressable entities.
- Member concepts **must not** have IDs if they are purely structural or value-like, unless the schema explicitly allows it.
- Identity requirements are defined by the ontology, not by surface syntax.

Example:

- `<Recipe id="…">` → entity
- `<Step>` → value node, no ID (unless schema says otherwise)

---

## 6. Nesting Rules

- Domain collections may be nested **only if explicitly allowed by the schema**.
- Nested collections must always respect their own ordering rules.
- Collections may not mix member classes.

Invalid example:

```xml
<Recipes>
	<Recipe>…</Recipe>
	<Song>…</Song> <!-- invalid -->
</Recipes>
```

---

## 7. Compilation to Triples

For a domain collection:

- the collection concept maps to a node (if semantically meaningful), or may be implicit
- each member maps to its individual node
- membership is represented via:
  - ordering predicates (for ordered collections)
  - membership predicates (for unordered collections)

The exact mapping is defined by the Codex ontology.

---

## 8. Non-Goals

Domain collections do **not**:

- package mixed artifact types
- carry provenance about tooling or generation
- encode presentation intent
- act as modules or configuration units

Those concerns are handled by **assemblies**, defined separately.

---

## 9. Summary

Domain collections are:

- semantic
- schema-defined
- single-class
- optionally ordered
- never reordered automatically
- part of the domain graph

They are the **correct way** to represent “many of the same thing” in Codex.
