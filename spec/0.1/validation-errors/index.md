Status: NORMATIVE  
Version: 0.1  
Editor: Charles F. Munat

# Codex Validation Error Taxonomy — Version 0.1

This document defines the **canonical taxonomy of validation errors** in the Codex
language.

Validation error taxonomy is part of the Codex language specification and is
governed by this document.

This document is **Normative**.

---

## 1. Purpose

This contract defines a **canonical taxonomy of validation errors** in Codex.

Its goals are to:

- make validation failures precise and predictable
- ensure consistent error classification across tools
- avoid vague or heuristic error reporting
- support correct reasoning by humans and LLMs
- separate syntax, surface form, schema, and semantic failures cleanly

This contract governs **error classification only**, not wording, UI presentation,
or recovery behavior.

---

## 2. Core Principle

> Every Codex validation failure MUST belong to exactly **one primary error class**.

Secondary information MAY be attached, but the **primary class** MUST be unambiguous.

---

## 3. Error Classes (Top Level)

Codex defines the following **closed set** of top-level validation error classes:

1. **Parse Errors**
2. **Surface Form Errors**
3. **Schema Errors**
4. **Identity Errors**
5. **Reference Errors**
6. **Collection Errors**
7. **Context Errors**
8. **Constraint Errors**

No other top-level error classes are permitted.

---

## 4. Parse Errors

### Definition

Parse Errors occur when a `.cdx` file cannot be parsed into a syntactic structure.

### Characteristics

- input is not structurally readable
- parsing cannot continue
- no schema is consulted

### Examples

- unbalanced Concept markers
- invalid quoting
- malformed Traits
- invalid indentation
- unterminated editorial annotations (`[` without matching `]`)
- nested editorial annotations

Parse Errors are **fatal**.

---

## 5. Surface Form Errors

### Definition

Surface Form Errors occur when a file parses successfully but violates the
**Codex Surface Form Contract**.

### Characteristics

- syntax is readable
- canonical formatting rules are violated
- schema may not yet be consulted

### Examples

- expanded empty Concepts
- invalid casing in Concept or Trait names
- forbidden or ambiguous whitespace
- multiple root Concepts in a file
- editorial annotation appearing inside Content
- editorial annotation appearing inside a Concept marker
- annotation placement that cannot be deterministically attached
- annotation splitting a syntactic unit

Surface Form Errors are **fatal**.

---

## 6. Schema Errors

### Definition

Schema Errors occur when parsed Codex violates schema-defined rules.

### Characteristics

- schema is consulted
- structure or Traits are invalid for a Concept
- semantic meaning cannot be assigned

### Examples

- unauthorized Trait on a Concept
- missing required Trait
- unknown Concept name
- invalid Trait value type
- invalid or unauthorized `<Annotation>` Concept
- invalid `kind` value on an `<Annotation>` Concept

Schema Errors are **fatal**.

---

## 7. Identity Errors

### Definition

Identity Errors occur when identity rules are violated.

### Characteristics

- related to `id` Traits and Entity eligibility
- graph identity or referential stability is compromised

### Examples

- `id` declared on a Concept that must not be an Entity
- missing required `id`
- duplicate identifiers within a scope
- invalid identifier form
- `id` declared on an annotation where identity is not authorized

Identity Errors are **fatal**.

---

## 8. Reference Errors

### Definition

Reference Errors occur when reference Traits are invalid or inconsistent.

### Characteristics

- involve `reference`, `target`, or `for`
- relate to graph linkage and intent

### Examples

- reference to a non-existent Entity
- reference to a non-Entity Concept
- violation of the reference singleton rule
- reference to an Entity of an unauthorized Concept type
- annotation provenance referencing an invalid or non-addressable target

Reference Errors are **fatal**.

---

## 9. Collection Errors

### Definition

Collection Errors occur when domain collection rules are violated.

### Characteristics

- involve collection Concepts
- membership or ordering semantics are incorrect

### Examples

- mixed member Concept types in a collection
- invalid ordering for an unordered collection
- missing required members
- duplicate membership where forbidden
- annotation collections violating schema-defined membership rules

Collection Errors are **fatal**.

---

## 10. Context Errors

### Definition

Context Errors occur when Concepts or Traits are used outside their valid
schema-defined context.

### Characteristics

- meaning depends on containment or scope
- names are valid but misapplied

### Examples

- using a Structural Concept outside its defining context
- using a Trait whose meaning is not defined in the current context
- assuming Codex module semantics outside a Module context
- using `<Annotation>` outside a schema-defined annotation context
- assuming annotation rendering semantics in a non-rendering context

Context Errors are **fatal**.

---

## 11. Constraint Errors

### Definition

Constraint Errors occur when schema-defined constraints are violated beyond basic
structure.

### Characteristics

- involve semantic or logical invariants
- schema-defined rules are broken

### Examples

- mutually exclusive Traits both present
- invalid combinations of Traits
- value range violations
- domain-specific invariant failures
- annotation constraint violations (e.g. forbidden combinations of annotation kinds)

Constraint Errors are **fatal**.

---

## 12. Error Severity

Codex validation errors are **not warnings**.

- any validation error halts compilation
- Codex does not permit best-effort interpretation
- tools MUST NOT silently recover

Severity gradation (warning vs error) is outside the scope of the Codex language.

---

## 13. Error Reporting Requirements

Codex tools SHOULD report validation errors with:

- error class
- Concept name
- Trait name (if applicable)
- violated schema or specification rule
- precise location (line number or Concept path)

Error **classification** is mandatory.  
Error wording and presentation are tool-defined.

---

## 14. Non-Goals

This contract does **not**:

- define error message wording
- mandate user-facing UX
- define recovery strategies
- prescribe exception hierarchies
- define logging or telemetry formats

It defines **what kind of error occurred**, not how it is presented.

---

## 15. Summary

- every validation failure has exactly one primary error class
- error classes are finite and closed
- annotations introduce no new error classes
- annotation errors are classified using existing categories
- errors are deterministic and fatal
- validation is mechanical, not heuristic

---

End of Codex Validation Error Taxonomy v0.1.
