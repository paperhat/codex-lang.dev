Status: NORMATIVE  
Version: 0.1  
Editor: Charles F. Munat

# Codex Language Specification — Version 0.1  
## Entry Point and Table of Contents

This document is the **authoritative entry point** for the Codex Language
Specification, version 0.1.

It defines the **scope, structure, authority, and immutability** of the
specification and enumerates the **Normative documents** that together define
the Codex language.

This document does **not** itself define language rules.

---

## Purpose of This Document

This document exists to:

- establish the scope of Codex 0.1
- declare which documents are Normative
- define immutability and versioning rules
- provide a stable table of contents for implementers and auditors

All language rules are defined in the documents listed below.

---

## Scope of Codex 0.1

Codex 0.1 defines:

- the core Codex language model
- declarative semantics and invariants
- surface form and canonicalization
- naming and literal value spellings
- identity and reference semantics
- schema definition and validation
- schema versioning rules
- validation error classification

Codex 0.1 does **not** define:

- modules or dialects
- pipeline orchestration
- storage, querying, or rendering behavior
- application frameworks or tooling
- inline text markup systems

Those concerns are defined by **separate, non-core specifications**.

---

## Included Normative Specifications

### Core Language

- **Language Definition** (`./language/`)
- **Naming and Value Specification** (`./naming-and-values/`)
- **Surface Form Specification** (`./surface-form/`)
- **Formatting and Canonicalization Specification** (`./formatting-and-canonicalization/`)

### Identity and References

- **Identifier Specification** (`./identifiers/`)
- **Reference Traits Specification** (`./reference-traits/`)

### Schemas and Validation

- **Schema Definition Specification** (`./schema-definition/`)
- **Schema Versioning Specification** (`./schema-versioning/`)
- **Validation Error Taxonomy** (`./validation-errors/`)

---

## Stability and Immutability

Codex 0.1 is **immutable**.

Once published:

- documents under `/spec/0.1/` MUST NOT be edited
- clarifications or changes require a new version
- superseding versions live alongside this version

No implementation-led reinterpretation is permitted.

---

## Relationship to Other Specifications

- `/spec/current/` points to the most recent published version
- draft or experimental work lives under `/spec/DRAFT/`
- implementations MUST target a specific published version

---

## Authority

This specification is maintained under the governance rules defined in
`GOVERNANCE.md`.

Final authority over Codex 0.1 rests with the **Specification Editor**.

---

End of Codex Language Specification v0.1 — Entry Point
