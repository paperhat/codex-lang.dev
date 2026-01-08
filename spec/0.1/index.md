Status: NORMATIVE  
Version: 0.1  
Editor: Charles F. Munat

# Codex Language Specification — Version 0.1

This directory contains the **Codex Language Specification, version 0.1**.

Version 0.1 defines the initial, stable semantics of the Codex language.  
All documents in this directory are **Normative** unless explicitly stated otherwise.

---

## Scope of This Version

Codex 0.1 defines:

- the core language model
- structural and semantic rules
- naming and identifier constraints
- surface form and inline text semantics
- schema authoring and versioning rules
- formatting and validation error models
- reference and linkage semantics

Together, these documents define **what Codex is**.

They do not define:

- system architecture
- pipeline orchestration
- storage, querying, or rendering behavior
- operational or implementation concerns

Those are defined by contracts under `/contracts/`.

---

## Included Normative Documents

The Codex 0.1 specification consists of the following sections:

- **Language Overview** (`/language/`)
- **Structural Concepts** (`/structural-concepts/`)
- **Naming Rules** (`/naming/`)
- **Surface Form** (`/surface-form/`)
- **Inline Text Markup (Patch)** (`/inline-text-markup/`)
- **Identifiers** (`/identifiers/`)
- **Schema Authoring** (`/schema-authoring/`)
- **Schema Versioning** (`/schema-versioning/`)
- **Reference Traits** (`/reference-traits/`)
- **Formatting Errors** (`/formatting-errors/`)
- **Validation Errors** (`/validation-errors/`)

All sections are required for a complete and compliant implementation.

---

## Stability and Immutability

This version is **immutable**.

Once published:

- documents under `/spec/0.1/` MUST NOT be edited
- clarifications or changes result in a new version
- superseding versions live alongside this one

---

## Relationship to Other Versions

- `/spec/current/` points to the most recent published version
- Draft and experimental work lives under `/spec/DRAFT/`
- Implementations MUST target a specific version

---

## Authority

This specification is maintained under the governance rules defined in `GOVERNANCE.md`.

Final authority over this version rests with the **Specification Editor**.

---

End of Codex Language Specification v0.1.
