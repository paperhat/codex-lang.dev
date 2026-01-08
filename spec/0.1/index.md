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
- provide a stable table of contents for implementers, auditors, and tooling

All language rules are defined in the documents listed below.

---

## Scope of Codex 0.1

Codex 0.1 defines:

- the core Codex language model
- structural and semantic rules
- naming and identifier constraints
- surface form rules
- inline text markup semantics
- schema authoring and versioning rules
- formatting and validation error taxonomies
- reference and linkage semantics

Together, these documents define **what Codex is**.

Codex 0.1 does **not** define:

- system architecture
- pipeline orchestration
- storage, querying, or rendering behavior
- operational or implementation concerns

Those concerns are defined by separate contracts under `/contracts/`.

---

## Included Normative Documents

The Codex 0.1 Language Specification consists of the following **Normative**
documents. All are required for a complete and compliant implementation.

### Core Language Definition

- [**Language Specification**](./language/)
- [**Structural Concepts**](./structural-concepts/)
- [**Naming Rules**](./naming/)
- [**Identifiers**](./dentifiers/)

### Surface Syntax and Content

- [**Surface Form**](./surface-form/)
- [**Inline Text Markup (Gloss)**](./inline-text-markup/)

### Schema and Versioning

- [**Schema Authoring**](./schema-authoring/)
- [**Schema Versioning**](./schema-versioning/)

### Relationships and Semantics

- [**Reference Traits**](./reference-traits/)

### Error Classification

- [**Formatting Errors**](./formatting-errors/)
- [**Validation Errors**](./validation-errors/)

---

## Stability and Immutability

Codex 0.1 is **immutable**.

Once published:

- documents under `/spec/0.1/` MUST NOT be edited
- clarifications or changes require a new version
- superseding versions live alongside this version

No implementation-led reinterpretation is permitted.

---

## Relationship to Other Versions

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
