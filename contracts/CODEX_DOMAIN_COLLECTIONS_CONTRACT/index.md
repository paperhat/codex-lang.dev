Status: NORMATIVE
Lock State: LOCKED
Version: 0.1
Editor: Charles F. Munat

# Codex Domain Collections Contract

This document defines **domain collection Concepts** in Codex.

A **domain collection** is a semantic construct used to group **multiple individuals of the same domain class** (e.g. `Recipe`, `Song`, `Event`) into a single, schema-defined collection.

Domain collections are **part of the domain model**.
They are not structural containers, modules, or packaging constructs.

This contract is a **domain-level specialization** of the canonical collection rules defined in the *Codex Canonical Collection Semantics Contract*.

---

## 1. Purpose

This contract exists to:

* define how **domain-level “many-of-the-same”** is expressed in Codex
* distinguish domain collections from structural grouping and assembly
* ensure ordering semantics are intentional and schema-defined
* prevent misuse of collections as modules, sections, or presentation devices

This contract governs **semantic domain collections only**.

---

## 2. What a Domain Collection Is

A **domain collection** is a Concept that:

* groups **multiple individuals of a single domain Concept class**
* is defined and constrained by a **domain schema**
* may be **ordered** or **unordered**
* compiles directly to semantic membership in the graph
* does **not** mix document roles (data, view, policy, configuration)

Example (Illustrative):

```xml
<Recipes>
	<Recipe id="recipe:spaghetti">…</Recipe>
	<Recipe id="recipe:cacio-e-pepe">…</Recipe>
</Recipes>
```

A domain collection MAY appear:

* as the **root Concept** of a Codex file, or
* as a **child Concept within a Module**, when explicitly authorized by schema

---

## 3. Schema Authority (Normative)

Domain collections are **schema-defined**, never ad hoc.

For each domain collection Concept, a schema MUST define:

* the **member Concept class**

* whether the collection is:

  * **ordered**, or
  * **unordered**

* whether empty collections are permitted

* whether duplicate membership is permitted

* whether members MAY or MUST be Entities

Codex documents **use** domain collections.
They do not define their semantics.

---

## 4. Ordering Semantics (Normative)

### 4.1 Ordered Domain Collections

If a domain collection is declared **ordered** by schema:

* lexical order of member Concepts **is semantically significant**
* order MUST be preserved exactly
* order MUST be represented explicitly in the semantic graph
* numbering or ordering Traits MUST NOT be used

Typical use cases (Illustrative):

* procedural steps
* musical movements
* ranked lists
* ordered phases or sequences

Example (Illustrative):

```xml
<Steps>
	<Step>Boil water.</Step>
	<Step>Add pasta.</Step>
	<Step>Drain.</Step>
</Steps>
```

---

### 4.2 Unordered Domain Collections

If a domain collection is declared **unordered**:

* membership is semantic; order is not
* lexical order has **no semantic meaning**
* lexical order MUST be preserved textually
* canonical formatting MUST NOT reorder members

Typical use cases (Illustrative):

* tags
* ingredients (when order is irrelevant)
* contributors
* references

---

## 5. Identity Rules

Identity and membership are orthogonal.

* Member Concepts MAY be Entities if schema authorizes identity
* Member Concepts MUST NOT be Entities if they are value-like or structural, unless explicitly permitted
* Identity requirements are defined by schema, not by surface syntax

Examples (Illustrative):

* `<Recipe id="…">` → Entity
* `<Step>` → non-Entity value Concept (unless schema allows identity)

Membership alone never creates identity.

---

## 6. Nesting Rules (Normative)

Domain collections MAY be nested **only if explicitly authorized by schema**.

When nesting is permitted:

* each collection retains its own ordering semantics
* member-class restrictions apply independently at each level

Collections MUST NOT mix member classes.

Invalid example (Illustrative):

```xml
<Recipes>
	<Recipe>…</Recipe>
	<Song>…</Song> <!-- invalid -->
</Recipes>
```

---

## 7. Compilation to Semantic Graphs

For a domain collection:

* the collection Concept MAY map to a graph node if semantically meaningful
* each member maps to its individual node
* membership is represented via:

  * ordering predicates (for ordered collections), or
  * membership predicates (for unordered collections)

The exact encoding is defined by the Codex ontology and is outside the scope of this contract.

---

## 8. Non-Goals

Domain collections do **not**:

* package mixed artifact types
* carry tooling or generation provenance
* encode presentation intent
* act as modules, assemblies, or configuration units

Those concerns are handled by **structural Concepts** and **Module assemblies**, defined elsewhere.

---

## 9. Summary

Domain collections are:

* semantic and schema-defined
* single-class and homogeneous
* optionally ordered
* never reordered automatically
* independent of identity
* first-class parts of the domain graph

They are the **correct and only way** to represent
**“many of the same thing”** in Codex.
