# Codex Canonical Collection Semantics Contract (DRAFT)

## Status

- **DRAFT**  
- Normative once locked  
- Applies to all Codex schemas and documents that define or use domain collections

---

## 1. Purpose

This contract defines the **canonical semantics of collections** in Codex.

Its goals are to:

- make “many-of-the-same” precise and unambiguous
- clearly separate **collection semantics** from assembly and structure
- ensure ordering is intentional and schema-defined
- prevent accidental misuse of collections as containers or modules

This contract governs **semantic collections**, not formatting or grouping for convenience.

---

## 2. What a Collection Is

A **collection** in Codex is a Concept that:

- groups **multiple members of a single Concept class**
- represents **membership** as a semantic fact
- is defined and constrained by schema
- may be ordered or unordered

Collections are **domain-level constructs**.

They are not:

- modules
- structural sections
- packaging mechanisms
- presentation devices

---

## 3. Schema Authority (Normative)

All collection semantics are defined by schema.

For each collection Concept, a schema MUST define:

- the **member Concept type**
- whether the collection is:
  - **ordered**
  - **unordered**

- whether empty collections are allowed
- whether duplicate membership is allowed
- whether members may or must be Entities

Codex documents **use** collections; they do not define them.

---

## 4. Ordered Collections (Normative)

An **ordered collection** is one where member order is semantically significant.

### Rules

- Lexical order of member Concepts **is the semantic order**
- Order MUST be preserved exactly
- No numbering, indexing, or ordering Traits are permitted
- Order MUST be represented explicitly in the semantic graph

### Typical Use Cases

- procedural steps
- sequences
- ranked lists
- ordered movements or phases

### Example (Illustrative)

```xml
<Steps>
	<Step>Boil water.</Step>
	<Step>Add pasta.</Step>
	<Step>Drain.</Step>
</Steps>
```

---

## 5. Unordered Collections (Normative)

An **unordered collection** is one where order has no semantic meaning.

### Rules

- Membership is semantic; order is not
- Lexical order MUST be preserved textually
- Canonical formatting MUST NOT reorder members
- Graph semantics MUST NOT depend on order

### Typical Use Cases

- ingredients
- tags
- contributors
- references

---

## 6. Membership Semantics

For all collections:

- Each member represents a distinct membership assertion
- Membership does not imply identity
- Membership does not imply containment outside the collection context

Membership is a **semantic relation**, not a structural one.

---

## 7. Identity and Collections

Identity and collection membership are orthogonal.

- A collection MAY be an Entity if schema allows
- A collection member MAY be an Entity if schema allows
- Membership alone does not create or require identity

Examples:

- A collection of non-Entity Steps (common)
- A collection of Entity Recipes (common)
- A non-Entity collection containing Entity members (common)

---

## 8. Nesting Rules

Collections MAY be nested **only if explicitly allowed by schema**.

When nested:

- each collection retains its own ordering rules
- member type restrictions apply independently at each level

Absent explicit schema permission, nested collections are invalid.

---

## 9. Collections vs Structural Concepts

Collections are **not** structural Concepts.

Differences:

- Collections group **homogeneous** members
- Structural Concepts group **heterogeneous** Concepts
- Collections assert semantic membership
- Structural Concepts assert organization or scope

Using a structural Concept where a collection is required is a schema error.

---

## 10. Canonical Behavior (Normative)

Codex tools MUST:

- preserve lexical order of collection members
- never reorder members automatically
- enforce schema-defined ordering semantics
- reject collections that violate member-type constraints

Collections are deterministic and mechanically enforceable.

---

## 11. Non-Goals

This contract does **not**:

- define collection syntax
- prescribe triple encodings
- define list or bag implementations
- define performance characteristics
- replace domain modeling decisions

It defines **semantic intent**, not representation.

---

## 12. Summary

- Collections represent “many of the same thing”
- Collection semantics are schema-defined
- Ordering is explicit and intentional
- Identity is orthogonal to membership
- Collections are semantic, not structural
