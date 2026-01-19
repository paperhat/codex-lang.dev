Status: NORMATIVE  
Lock State: LOCKED    
Version: 0.1  
Editor: Charles F. Munat

# Codex Language Specification — Version 0.1

## Entry Point and Table of Contents

This document is the **authoritative entry point** for the Codex Language
Specification, version 0.1.

It defines the **scope, structure, authority, and stability conventions** of the
specification and enumerates the **Normative documents** that together define the
Codex language.

This document does **not** itself define language rules.

---

## Purpose of This Document

This document exists to:

* establish the scope of Codex 0.1
* declare which documents are Normative
* provide a stable table of contents for implementers, auditors, and tooling

All language rules are defined in the documents listed below.

---

## Scope of Codex 0.1

Codex 0.1 defines:

* the core Codex language model
* structural and semantic rules for Concepts, Traits, Values, and Content
* naming and identifier constraints
* surface form rules
* formatting and canonicalization rules
* schema definition and schema versioning rules
* reference trait semantics
* validation error classification

Codex 0.1 does **not** define:

* identifier base scoping or base resolution mechanisms
* storage, querying, or rendering behavior
* pipeline orchestration or runtime behavior

Those concerns belong to consuming systems.

---

## Included Normative Documents

The Codex 0.1 Language Specification consists of the following **Normative**
documents. All are required for a complete and compliant implementation.

### Core Language Definition

* [**Language Specification**](./language/)

### Naming, Values, and Identity

* [**Naming and Value Specification**](./naming-and-values/)
* [**Identifier Specification**](./identifiers/)
* [**Reference Traits Specification**](./reference-traits/)

### Surface Syntax and Canonicalization

* [**Surface Form Specification**](./surface-form/)
* [**Formal Grammar Specification**](./grammar/)
* [**Formatting and Canonicalization Specification**](./formatting-and-canonicalization/)

### Schema

* [**Schema Definition Specification**](./schema-definition/)
* [**Schema Versioning Specification**](./schema-versioning/)

### Error Classification

* [**Validation Error Taxonomy**](./validation-errors/)

---

## Stability and Immutability

Codex 0.1 stability is governed by repository governance.

* published versions SHOULD be treated as stable
* revisions are permitted only under editor control
* tools MUST target a specific published version

---

## Authority

This specification is maintained under the governance rules defined in
`GOVERNANCE.md`.

Final authority over Codex 0.1 rests with the **Specification Editor**.

---

End of Codex Language Specification v0.1 — Entry Point
