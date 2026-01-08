Status: NORMATIVE
Lock State: LOCKED
Version: 0.1
Editor: Charles F. Munat

# Codex Design Policy Contract

This document defines the **exclusive responsibilities, boundaries, and guarantees** of **Design Policy** in Paperhat Codex.

Design Policy governs **how semantic projections are presented**, without altering meaning, structure, or correctness.

This document is **Normative** and is governed by global Codex change control.

---

## 1. Purpose

Design Policy exists to answer one question:

> **“Given this meaning and this view, how should it appear in a specific medium?”**

Design Policy defines **presentation decisions**, not semantic truth.

It enables:

* consistent design systems over semantic data
* responsive and adaptive presentation
* multi-target rendering (screen, print, voice, etc.)
* declarative, explainable layout behavior
* reflow, prioritization, and progressive disclosure

Design Policy is **data**, not code.

---

## 2. Scope (Hard)

Design Policy governs **presentation-level interpretation** of semantic projections and content semantics, including:

* grouping interpretation
* ordering and flow
* alignment and spatial relationships
* hierarchy and prioritization
* contrast, emphasis, and dominance
* balance and visual weight
* use of negative space
* responsive behavior
* progressive disclosure
* pagination and step flows
* widget selection strategy (when applicable)

For time-based or dynamic media, Design Policy MAY additionally govern:

* pacing and rhythm
* continuity
* transitions
* narrative sequencing
* audio/visual coordination

Design Policy never defines meaning.

---

## 3. Separation of Concerns (Hard)

Design Policy:

* **consumes** semantic projections, ViewModels, and Patch-derived semantics
* **does not** alter semantic truth
* **does not** invent structure
* **does not** introduce new data
* **does not** enforce constraints
* **does not** define behavior logic

Canonical separation of responsibility:

* **Architect** defines meaning
* **Surveyor** defines projections
* **Patch** enriches inline content semantics
* **Scribe** orchestrates the pipeline
* **Design Policy** defines appearance
* **Renderers** implement targets

---

## 4. Relationship to Semantic Projections and Patch

Design Policy operates on **semantic groupings and distinctions**, not on markup or layout primitives.

Sources of semantic input include:

* ViewModels derived from Surveyor projections
* Patch-derived semantic distinctions embedded in Content

Examples of semantic groupings and distinctions include:

* Concept groups
* Field groups
* Sections
* Lists
* Steps
* Narratives
* Hierarchies declared at the meaning level
* Inline semantic emphasis or references expressed via Patch

Design Policy interprets these semantics **by policy**, not by inference.

Design Policy MAY respond differently to Patch-derived semantics across targets, but MUST NOT reinterpret or redefine their meaning.

---

## 5. Ownership and Authoring

Design Policy is:

* authored by site or application owners
* expressed exclusively in **Codex** (`.cdx`)
* owned by the application, not by Architect or Surveyor
* consumed by Scribe and renderers

End users MAY author or modify Design Policy without writing code.

---

## 6. Target Awareness (Normative)

Design Policy is **target-aware but target-agnostic**.

This means:

* policies MAY declare intent relative to a target class (e.g. screen, print, voice)
* policies MUST NOT contain target-specific implementation details
* final interpretation is delegated to renderers

Design Policy MUST NOT reference DOM, HTML, CSS, ARIA, or platform APIs.

---

## 7. Widget Policy (Subset)

Widget Policy is a **subset** of Design Policy.

Widget Policy governs **selection strategies**, such as:

* radio group vs dropdown
* checkbox group vs autocomplete
* slider vs numeric input
* text field vs multi-line text

These decisions are:

* policy-driven
* configurable
* non-semantic
* overridable per target

Widget Policy MUST NOT introduce meaning and MUST NOT affect validity.

---

## 8. Responsive and Adaptive Rules

Design Policy MAY encode rules such as:

* reflow thresholds
* content relocation
* priority-based collapse
* summarization vs expansion
* pagination or wizard transitions

Rules operate on **semantic nodes, groups, and Patch-derived distinctions**, not on layout primitives.

Viewport size, shape, and medium characteristics MAY be considered.

---

## 9. Progressive Disclosure

Design Policy MAY define:

* what is shown first
* what is hidden initially
* what is revealed on demand
* how secondary content is accessed

Progressive disclosure affects **presentation only**.

Hidden content remains:

* semantically present
* queryable
* valid
* persistent

This includes content enriched via Patch.

---

## 10. Relationship to Behavior

Design Policy is **not behavior**.

* It does not compute values
* It does not react to events
* It does not execute logic

Design Policy MAY declare **presentation affordances** that renderers and behaviors can respond to, but it does not define the behavior itself.

Patch semantics MUST NOT be treated as behavior triggers.

---

## 11. Compilation and Use

Design Policy is:

* parsed from Codex
* compiled by Scribe into a Presentation Plan
* combined with a ViewModel and Patch-derived semantics
* consumed by renderers

Compilation is deterministic.

No runtime inference is permitted.

---

## 12. Prohibited Content (Hard)

Design Policy MUST NOT include:

* semantic assertions
* validation rules
* business logic
* behavior logic
* runtime bindings
* references to storage, APIs, or clocks
* HTML, CSS, or platform-specific constructs
* reinterpretation of Patch semantics

If it affects correctness, it is not Design Policy.

---

## 13. Explainability Requirement

Design Policy MUST be explainable in plain language.

The system MUST be able to answer questions such as:

* “Why is this shown first?”
* “Why is this grouped here?”
* “Why did this collapse on a small screen?”
* “Why is this emphasized differently here?”
* “Why is this summarized instead of expanded?”

Opaque or implicit behavior is forbidden.

---

## 14. Summary

Design Policy enables:

> **Design systems over meaning, not markup.**

It provides:

* consistency without rigidity
* adaptability without inference
* presentation control without semantic corruption
* multi-target support without duplication

Design Policy answers **how it appears**, never **what it means**.
