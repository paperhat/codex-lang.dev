# Codex Language Specification

This repository publishes the **canonical specification and system contracts** for **Codex**, a declarative semantic language for expressing structured meaning independent of runtime, presentation, or target platform.

This site is intentionally minimal.
It exists to define **what Codex is**, **what compliant systems must do**, and **where authority resides**.

---

## What Codex Is

**Codex is a language.**

It is used to author:

- semantic structure
- meaning and constraints
- behavior (as data)
- presentation policy
- bindings to environments

Codex is **not** a framework, toolkit, or UI system.
Those are applications _of_ the language.

---

## Repository Structure

Authority is expressed structurally.

```
/spec/        Codex language specification (versioned, immutable)
/contracts/   Normative system and library contracts
/notes/       Informative, non-binding material
/about/       Scope and status definitions
```

If a document defines required behavior, it is **Normative**.
If it explains or discusses, it is **Informative**.

---

## Specification Versions

- Language specifications live under `/spec/<version>/`
- Published versions are **immutable**
- `/spec/current/` points to the most recent version

Versioned URLs are stable and citable.

---

## Contracts

Contracts define **obligations and boundaries** for systems and libraries that implement or operate on Codex.

Each contract is:

- a named artifact
- versioned independently
- authoritative within its scope

Compliance is explicit and non-ambiguous.

---

## Governance

Codex is maintained under a **strong editorial governance model**.

- The specification is public.
- The specification is open to review.
- The specification is not crowd-designed.

Final authority over **Normative** content rests with the **Specification Editor**.

See `GOVERNANCE.md` for details.

---

## Licensing

- **Specification text**: Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Trademarks**: Not licensed

See `LICENSE.md` and `SPECIFICATION_LICENSE.md`.

---

## Status

Codex is under active development.

The presence of a document here establishes intent and authority, not finality.

---

## Scope Note

This repository is a **reference**.

It is not:

- a tutorial site
- a community forum
- a marketing property

Those concerns live elsewhere.

---

_Clarity, coherence, and correctness take precedence over popularity._
