Status: NORMATIVE
Lock State: LOCKED
Version: 0.1
Editor and Specification Steward: Charles F. Munat

# Codex System Contract

This document defines the **foundational nature, scope, and invariants** of **Paperhat Codex**.

It supersedes any interpretation of Paperhat as a “framework” or “toolkit”.

---

## 1. What Paperhat Codex Is

**Paperhat Codex is a language.**

It is a **declarative, semantic authoring language** for describing:

* meaning
* structure
* constraints
* behavior (as data)
* presentation policy
* bindings to environments

Paperhat Codex is **not**:

* a web framework
* a UI framework
* a component library
* a configuration system layered on top of code

All of those are *applications* of the language, not the language itself.

---

## 2. The Authoring Surface (Normative)

### 2.1 Codex Is the Only Authoring Language

**All authoring is done in Codex.**

Codex is expressed textually using the canonical `.cdx` surface form.

This includes, without exception:

* semantic data
* semantic views
* constraints
* behaviors
* bindings
* design policy
* pipeline configuration
* environment configuration

No other authoring formats are permitted.

Forbidden authoring surfaces:

* JSON
* YAML
* TOML
* XML
* imperative configuration
* embedded scripts
* inline code blocks

If it is authored by a human, it is Codex.

---

### 2.2 Target Users (Critical)

Paperhat Codex is designed for **non-developers**.

Authors may include:

* hobbyists
* designers
* subject-matter experts
* business analysts
* lawyers
* product managers
* educators

Programming experience is **not assumed**.

Codex MUST:

* read like plain English
* minimize cognitive load
* avoid abbreviations in its canonical form
* avoid programming jargon
* avoid implementation detail leakage

Developer convenience is never a justification for authoring complexity.

---

### 2.3 Inline Content Enrichment: Gloss (Normative)

Within Codex **Content**, inline enrichment MAY be expressed using the **Gloss language**.

**Gloss is a language.**
It is not formatting, styling, or presentation.

Gloss exists to allow authors to **annotate, qualify, and reference meaning inside content**, without breaking declarative purity or introducing target assumptions.

Gloss:

* operates *only* inside Content
* is fully declarative
* is parseable and round-trippable
* produces structured semantic data, not decorated strings

Gloss is used to express, for example:

* emphasis and semantic weight
* references to declared resources or identifiers
* annotations that participate in meaning, not appearance

Gloss is **not**:

* HTML
* Markdown
* rich text
* a styling language
* a presentation instruction system

Gloss does **not** define how something looks.
It defines **what something is**, semantically, within authored content.

All Gloss constructs compile into internal semantic structures and remain subject to:

* determinism
* validation
* target-agnostic rendering

---

## 3. Closed World Assumption (Normative)

Paperhat Codex operates as a **closed declarative system**.

This means:

* all meaning must be explicitly declared
* nothing is inferred implicitly
* nothing is “filled in” silently
* nothing exists outside what is authored or derived deterministically

If something is not declared, it does not exist.

This applies equally to Codex structure and to Gloss-enriched content.

---

## 4. Internal Representations (Non-Authoring)

### 4.1 Compilation Is Mandatory

All Codex documents, including Gloss-enriched content, are compiled into internal representations, including:

* abstract syntax structures
* intermediate representations
* semantic graphs (triples)
* constraint graphs
* view models
* presentation plans

These representations are:

* internal
* invisible to end users
* unstable across versions
* optimized for machines

Authors MUST NEVER see or write these representations.

---

### 4.2 Naming and Abbreviation Rule

* **Codex and Gloss use full, plain-English names**
* **Internal representations may use abbreviated names freely**

Abbreviations are permitted only where humans do not see them.

---

## 5. Determinism and Explainability (Normative)

Given the same Codex inputs:

* compilation MUST be deterministic
* outputs MUST be reproducible
* validation MUST be consistent

The system MUST be able to explain:

* why something is valid
* why something is invalid
* why something is shown
* why something is hidden
* why something is ordered or grouped

This applies equally to structure, content, and Gloss-derived semantics.

Opaque behavior is forbidden.

---

## 6. Separation of Responsibility (Normative)

Paperhat Codex enforces strict separation:

* **Architect and domain libraries** define meaning
* **Constraints** define validity
* **Behaviors** define optional computation
* **Bindings** define value sources
* **Design Policy** defines appearance
* **Kernel** orchestrates compilation and rendering
* **Warden** enforces validity
* **Renderers** emit target-specific output

Gloss contributes semantic data only.
It may not assume responsibilities owned by Design Policy or Renderers.

No library may assume responsibilities owned by another.

---

## 7. Non-JavaScript Correctness (Normative)

All Paperhat Codex applications MUST be correct **without JavaScript**.

This means:

* data validity does not depend on JavaScript
* form submission does not depend on JavaScript
* persistence does not depend on JavaScript
* constraint enforcement does not depend on JavaScript

Gloss semantics MUST remain correct in non-JavaScript environments.

JavaScript MAY enhance experience, but MUST NOT enable correctness.

---

## 8. Referential Transparency (Normative)

All authoritative semantics in Paperhat Codex MUST be referentially transparent.

* constraints depend only on the semantic graph
* calculations depend only on declared inputs
* no hidden state may influence correctness

Runtime-only sources (cookies, clocks, APIs, UI state) MUST NOT affect semantic truth.

This includes semantics derived from Gloss.

---

## 9. Multi-Target First Principle

Paperhat Codex is **target-agnostic by design**.

The same Codex document may be rendered to:

* HTML
* DOM mutations
* PDF
* LaTeX
* SVG
* Voice systems
* future targets not yet defined

No authoring construct — including Gloss — may assume a specific target.

---

## 10. Change Discipline (Normative)

Any change to Paperhat Codex MUST:

1. be proposed as a textual change to a canonical document
2. preserve existing guarantees explicitly
3. avoid implementation-led reinterpretation

Implementation follows documentation, never the reverse.

---

## 11. Summary

Paperhat Codex is:

> **A language for describing reality, not a toolkit for building websites.**

It prioritizes:

* clarity over cleverness
* explicitness over inference
* meaning over mechanics
* humans over machines

Structure is authored in Codex.
Inline meaning may be enriched with Gloss.
Presentation is decided elsewhere.

If something cannot be expressed clearly and declaratively in Codex and Gloss, it does not belong in the system.
