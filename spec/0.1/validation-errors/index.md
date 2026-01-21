Status: NORMATIVE  
Lock State: UNLOCKED    
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

This specification defines a **canonical taxonomy of validation errors** in Codex.

Its goals are to:

* make failures precise and predictable
* ensure consistent classification across tools
* avoid vague reporting and classification approaches that violate the Codex
	language invariants (see `spec/0.1/language/index.md`)
* separate parsing, surface form, formatting/canonicalization, and schema failures cleanly

This specification governs **error classification only**, not wording, UI presentation,
or recovery behavior.

---

## 2. Core Principle (Normative)

Every Codex failure MUST belong to exactly **one primary error class**.

Secondary information MAY be attached, but the **primary class** MUST be unambiguous.

---

## 3. Error Classes (Top Level) (Normative)

Codex defines the following **closed set** of top-level error classes:

1. **ParseError**
2. **SurfaceFormError**
3. **FormattingError**
4. **SchemaError**
5. **IdentityError**
6. **ReferenceError**
7. **CollectionError**
8. **ContextError**
9. **ConstraintError**

No other top-level error classes are permitted.

---

## 4. ParseError

### Definition

A ParseError occurs when a `.cdx` file cannot be parsed into a syntactic structure.

### Characteristics

* input is not structurally readable
* parsing cannot continue
* parsing MAY be performed without a governing schema for well-formedness checks

### Examples (Illustrative)

* unbalanced Concept markers
* invalid string literal escaping
* malformed Traits
* unterminated Annotation (missing closing `]`)
* structurally invalid nesting of markers

ParseError is **fatal**.

---

## 5. SurfaceFormError

### Definition

A SurfaceFormError occurs when a file parses successfully but violates the
**Surface Form Specification** (see that specification for detailed rules).

### Characteristics

* syntax is readable
* surface requirements are violated
* schema is available, but this class concerns schema-independent surface rules

### Examples (Illustrative)

* invalid casing in Concept or Trait names
* multiple root Concepts in a file
* forbidden whitespace around `=`
* annotation opening `[` not at first non-whitespace position
* annotation escape misuse (e.g. `\q` in an Annotation)

SurfaceFormError is **fatal**.

---

## 6. FormattingError

### Definition

A FormattingError occurs when input parses and passes surface-form requirements
but **cannot be transformed into canonical surface form**.

See the **Formatting and Canonicalization Specification** for canonicalization rules.

### Characteristics

* canonicalization is deterministic or must fail
* tools MUST NOT guess or “best-effort” normalize

### Examples (Illustrative)

* ambiguous annotation attachment
* non-deterministic blank-line/whitespace normalization that would change annotation kind
* whitespace patterns that cannot be normalized without changing structure
* any other canonicalization failure

FormattingError is **fatal**.

---

## 7. SchemaError

### Definition

A SchemaError occurs when parsed Codex violates schema-defined rules.

### Characteristics

* schema is consulted
* Concepts or Traits are invalid under the active schema
* meaning cannot be assigned

### Examples (Illustrative)

* unauthorized Trait on a Concept
* missing required Trait
* invalid Trait value type

SchemaError is **fatal**.

---

## 8. IdentityError

### Definition

An IdentityError occurs when identity rules are violated.

See the **Identifier Specification** for identity rules.

### Characteristics

* concerns Entity eligibility and identifier use
* compromises stable identity or uniqueness

### Examples (Illustrative)

* `id` declared on a Concept that MUST NOT be an Entity
* missing required `id` where schema requires an Entity
* duplicate identifiers within a schema-defined scope
* identifier form invalid under schema constraints

IdentityError is **fatal**.

---

## 9. ReferenceError

### Definition

A ReferenceError occurs when reference Traits are invalid or inconsistent.

See the **Reference Traits Specification** for reference trait semantics.

### Characteristics

* involves `reference`, `target`, or `for`
* relates to graph linkage and intent

### Examples (Illustrative)

* violation of the reference singleton rule (unless schema permits)
* reference to a non-existent Entity (where resolution is required)
* reference to an Entity of an unauthorized Concept type

ReferenceError is **fatal**.

---

## 10. CollectionError

### Definition

A CollectionError occurs when schema-defined collection rules are violated.

### Characteristics

* concerns domain collection Concepts
* membership and ordering semantics are incorrect

### Examples (Illustrative)

* mixed member Concept types in a collection
* missing required members
* duplicate membership where forbidden
* member count outside required bounds

CollectionError is **fatal**.

---

## 11. ContextError

### Definition

A ContextError occurs when a Concept or Trait is used outside its schema-defined context.

### Characteristics

* the name may be valid
* but it is misapplied due to containment or scope rules

### Examples (Illustrative)

* Concept permitted only under a specific parent appears elsewhere
* Trait permitted only in a particular context appears outside it

ContextError is **fatal**.

---

## 12. ConstraintError

### Definition

A ConstraintError occurs when schema-defined declarative constraints are violated beyond
basic structure and authorization.

### Characteristics

* logical or semantic invariants fail
* constraints are schema-defined and mechanically enforceable

### Examples (Illustrative)

* mutually exclusive Traits both present
* invalid combinations of Traits
* value range violations
* domain-specific invariant failures

ConstraintError is **fatal**.

---

## 13. Error Severity (Normative)

Codex errors are **not warnings**.

* any failure halts compilation or processing
* no best-effort recovery is permitted
* tools MUST NOT silently reinterpret invalid data

---

## 14. Reporting Requirements

Tools SHOULD report failures with:

* primary error class
* Concept name
* Trait name (if applicable)
* violated rule reference
* precise location (line number or Concept path)

Classification is mandatory.
Wording and presentation are tool-defined.

---

## 15. Non-Goals

This specification does **not**:

* define message wording
* mandate UX
* define recovery strategies
* prescribe exception hierarchies
* define logging formats

It defines **what kind of error occurred**, not how it is presented.

---

## 16. Summary

* every failure has exactly one primary error class
* error classes are finite and closed
* parsing, surface form, formatting/canonicalization, and schema are separated
* failures are fatal within their primary error class

---

**End of Codex Validation Error Taxonomy v0.1**
