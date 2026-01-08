# CDX_LANGUAGE_SPEC (CANONICAL)

This document defines the **CDX language** used by Paperhat Codex.

CDX is a **human-first declarative language** for expressing meaning, constraints, behavior, presentation policy, and bindings.

This document is **CANONICAL**.
It is governed by global Codex Change Control.

---

## 1. What CDX Is

**CDX is a language, not a notation.**

It is designed to be:

- readable by non-programmers
- writable without technical training
- precise enough for formal compilation
- expressive without hidden complexity

CDX is the **only** authoring language in Paperhat Codex.

---

## 2. Design Principles (Hard)

CDX is governed by these non-negotiable principles:

1. **Plain English First**
   Canonical constructs must read like natural language.

2. **Low Cognitive Load**
   Authors should not need to understand programming, math notation, or markup theory.

3. **Structural Clarity**
   Meaning is expressed through structure, not syntax tricks.

4. **No Implicit Meaning**
   Nothing is inferred silently.

5. **Deterministic Interpretation**
   The same CDX always means the same thing.

---

## 3. Who CDX Is For

CDX is designed for:

- hobbyists
- designers
- subject-matter experts
- business analysts
- lawyers
- educators
- product owners

Programming experience is **not assumed**.

If a construct would confuse a careful, intelligent non-programmer, it is invalid.

---

## 4. Canonical Naming Rules (Hard)

### 4.1 Full Names Are Canonical

Canonical CDX concept names MUST:

- be written in full
- use plain English
- avoid abbreviations
- avoid acronyms
- avoid programming jargon

Examples (canonical):

- `<IsGreaterThan>`
- `<PreparationTime>`
- `<MatchesPattern>`
- `<RootMeanSquare>`

Examples (non-canonical, but may exist as aliases):

- `<Gt>`
- `<PrepTime>`
- `<Regex>`
- `<RMS>`

Aliases MAY exist, but documentation and examples MUST use canonical names.

---

### 4.2 Case and Form

- Concept names use **PascalCase**
- Trait names use **camelCase**
- Text content is freeform unless otherwise constrained

---

## 5. Structure Over Syntax (Critical)

CDX derives meaning from **structure**, not from symbols or punctuation.

- Nesting expresses relationship
- Order expresses sequence
- Grouping expresses proximity or association

There are:

- no operators
- no precedence rules
- no inline expressions
- no symbolic syntax

---

## 6. Ordering Semantics (Hard)

**Order is derived from authoring order.**

If concepts appear in sequence, that sequence is meaningful.

CDX MUST NOT include explicit ordering markers such as:

- `<Order>`
- numeric indices
- priority numbers (except where explicitly semantic)

If two items are authored in order, they are ordered.

If order matters, authors express it by placement.

---

## 7. Traits vs Child Concepts

### 7.1 Traits

Traits are used for:

- simple scalar values
- units
- flags
- identifiers
- modifiers

Example:

```
<Quantity amount="3" unit="tablespoon" />
```

---

### 7.2 Child Concepts

Child concepts are used for:

- complex structure
- grouping
- composition
- explanation
- nested meaning

Example:

```
<Constraint>
  <IsGreaterThan>
    <Referent>x</Referent>
    <Comparator>a</Comparator>
  </IsGreaterThan>
</Constraint>
```

---

## 8. Text Content

Text content in CDX:

- is literal by default
- does not imply structure
- does not introduce meaning unless explicitly defined

Example:

```
<Step>Stir gently for 20 seconds.</Step>
```

Text never becomes a reference implicitly.

---

## 9. Variables and Names

### 9.1 Variables Are Symbols

Variables in CDX are:

- symbolic placeholders
- named explicitly
- not values

They do not imply source, type, or lifetime.

---

### 9.2 Variables Are Never Bound Inline

CDX expressions reference variables.

Variables are bound later by **Scribe**, using CDX binding configuration.

This applies everywhere:

- constraints
- behaviors
- calculations
- presentation logic

---

## 10. No Hidden Execution Model

CDX:

- does not execute
- does not branch imperatively
- does not loop implicitly
- does not mutate state

Any notion of “doing” is declarative and explicit.

---

## 11. No Target Leakage (Hard)

CDX MUST NOT reference:

- HTML
- CSS
- DOM
- JavaScript
- ARIA
- platform APIs
- storage mechanisms
- transport protocols

Targets are selected later.

---

## 12. Explainability Requirement

Every CDX construct MUST be explainable in plain language.

The system must be able to say:

- “This means…”
- “This is valid because…”
- “This appears here because…”

If a construct cannot be explained simply, it is invalid.

---

## 13. Extensibility Rules

CDX may be extended by libraries, but extensions MUST:

- follow naming rules
- avoid abbreviations
- declare meaning explicitly
- not overload existing constructs
- not introduce implicit behavior

Extensions define **new words**, not new grammar.

---

## 14. Prohibited Patterns (Hard)

CDX MUST NOT include:

- inline scripts
- embedded expressions
- implicit defaults that change meaning
- positional magic
- symbolic operators
- developer-centric shorthand in canonical form

If it looks like code, it does not belong in CDX.

---

## 15. Summary

CDX is:

> **A language for people to describe reality clearly.**

It favors:

- clarity over brevity
- structure over symbols
- explicitness over inference
- humans over machines

Machines adapt to CDX — not the other way around.

---

## Status

**CANONICAL**

This document is authoritative.
Anything not explicitly permitted is forbidden.
