Status: NORMATIVE
Lock State: LOCKED
Version: 0.1
Editor: Charles F. Munat

# Codex Formal Grammar Specification — Version 0.1

This specification defines the **formal grammar** of the Codex surface form.

Two grammar notations are provided:

* **EBNF** (Normative) — ISO/IEC 14977 Extended Backus-Naur Form
* **PEG** (Informative) — Parsing Expression Grammar for implementation

---

## 1. Purpose

This specification exists to:

* provide an unambiguous definition of Codex syntax
* enable mechanical parser construction
* support conformance testing
* eliminate ambiguity in the surface form specification

---

## 2. Authority

### 2.1 Syntactic Authority

The EBNF grammar is **normative for syntax**. A conforming parser MUST accept all documents that match the EBNF grammar and MUST reject all documents that do not.

The PEG grammar is **informative**. It provides an implementation-ready, unambiguous grammar. In case of discrepancy between EBNF and PEG, the EBNF grammar takes precedence.

### 2.2 Semantic Authority

Prose specifications are **normative for semantics**. The grammars define what is syntactically valid but do not assign meaning.

* **Surface Form Specification**: normative for structural semantics (encoding, indentation, escaping)
* **Naming and Value Specification**: normative for value type semantics and naming rules
* **Language Specification**: normative for language invariants

In case of discrepancy between grammar and prose:

* For syntactic precision (what parses): EBNF takes precedence
* For semantic intent (what it means): prose specifications take precedence

---

## 3. Included Documents

* [**EBNF Grammar**](./ebnf/) — Normative formal grammar
* [**PEG Grammar**](./peg/) — Informative implementation grammar

---

## 4. Relationship to Surface Form Specification

This grammar formalizes the rules described in prose in the **Surface Form Specification**. The Surface Form Specification takes precedence over this grammar for semantic intent. This grammar takes precedence for syntactic precision.

---

## 5. Scope

This grammar defines:

* Document structure
* Concept markers (opening, closing, self-closing)
* Trait syntax
* All value literal forms
* Annotation syntax
* Whitespace and structural elements

This grammar does **not** define:

* Schema validation rules
* Semantic constraints
* Content mode determination (schema responsibility)
* Identifier resolution

---

**End of Codex Formal Grammar Specification v0.1**
