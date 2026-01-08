Status: NORMATIVE  
Version: 0.1  
Editor: Charles F. Munat

# Codex Language Specification — Version 0.1  
## Language Definition

This document defines the **Codex language itself**.

It specifies the **foundational language model, semantics, and invariants** that
apply to all Codex documents, schemas, and tooling.

This document is **Normative**.

---

## Role of This Document

This document is the **authoritative definition of the Codex language**.

It defines:

- what Codex is as a language
- what Codex constructs mean
- what Codex explicitly does and does not include
- the invariants that all Codex tooling MUST respect

This document is part of the Codex Language Specification v0.1 and MUST be read in
conjunction with the other Normative documents listed in `/spec/0.1/index.md`.

---

## What Codex Is

**Codex is a declarative semantic authoring language.**

Codex is designed to describe:

- meaning
- structure
- constraints
- behavior (as data)
- presentation policy
- bindings to environments

Codex is **not**:

- a web framework
- a UI framework
- a component system
- a configuration format layered on top of code

All of the above are **applications of Codex**, not the language itself.

---

## Authoring Surface

Codex authoring is performed exclusively using the **Codex surface syntax**
expressed in `.cdx` files.

All author-authored material—including:

- data
- views
- schemas
- constraints
- behaviors
- policies
- bindings
- configuration

—MUST be expressed in Codex.

No alternative authoring formats are permitted.

---

## Declarative and Closed World Model

Codex operates as a **closed declarative system**.

This means:

- all meaning must be explicitly declared
- nothing is inferred implicitly
- nothing is filled in heuristically
- nothing exists outside what is authored or deterministically derived

If something is not declared, it does not exist.

---

## Determinism and Explainability

Given the same Codex inputs:

- parsing MUST be deterministic
- validation MUST be deterministic
- compilation MUST be deterministic

Codex tooling MUST be able to explain:

- why something is valid or invalid
- why something appears or does not appear
- why something is ordered, grouped, or scoped as it is

Opaque or heuristic behavior is forbidden.

---

## Separation of Responsibility

Codex enforces strict separation between:

- language semantics
- schema-defined meaning
- constraints
- behavior modeling
- design and presentation
- rendering and execution

Codex defines **what is declared**, not **how it is executed or rendered**.

Responsibilities outside the language itself are defined in separate contracts
(e.g. Scribe, Warden, Architect).

---

## Multi-Target by Design

Codex is **target-agnostic**.

The same Codex document MAY be rendered to:

- HTML
- DOM mutation plans
- PDF
- LaTeX
- SVG
- voice systems
- future targets not yet defined

No Codex construct may assume a specific target.

---

## Relationship to Other Specification Documents

This document defines **language-level semantics only**.

It does **not** define:

- surface syntax rules (see **Surface Form**)
- inline text enrichment semantics (see **Inline Text Markup**)
- schema structure (see **Schema Authoring**)
- identifier rules (see **Identifiers**)
- error classification (see **Formatting Errors** and **Validation Errors**)

All such concerns are defined in their respective Normative documents.

---

## Stability

This document is **immutable** as part of Codex 0.1.

Any clarification or change requires a new published version.

---

## Summary

- Codex is a language, not a framework
- Codex is declarative, closed-world, and deterministic
- All authoring is done in Codex
- Meaning is explicit and explainable
- Execution, rendering, and storage are outside the language
- This document defines the language; other documents refine it

---

End of Codex Language Specification v0.1 — Language Definition
