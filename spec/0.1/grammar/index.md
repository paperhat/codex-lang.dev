Status: NON-NORMATIVE (Historical; consolidated into codex-language-specification.md Appendix A)
Lock State: UNLOCKED
Version: 0.1
Editor: Charles F. Munat

# Codex Formal Grammar Specification — Version 0.1

This document is retained for historical/reference purposes.

The authoritative normative content is consolidated into `spec/0.1/codex-language-specification.md` Appendix A.

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
* Identifier resolution

---

## 6. Schema-Directed Parsing (Normative)

The grammars in this specification are **schema-parameterized**.

### 6.1 Parser Requirements

A conforming parser MUST:

1. Accept a schema as input alongside the document
2. Consult the schema when parsing each Concept to determine content mode
3. Fail with ParseError when encountering a Concept not defined in the schema

### 6.2 Grammar Interpretation

The `BlockConcept` production has two alternatives: `ChildrenBody` and `ContentBody`.

This is **not** syntactic ambiguity. The parser selects the correct alternative
by consulting the schema:

* Schema says children mode (`ForbidsContent`) → parse `ChildrenBody`
* Schema says content mode (`AllowsContent`) → parse `ContentBody`

### 6.3 Bootstrap Schema-of-Schemas

When parsing a document whose root Concept is `Schema`, the parser MUST use
the schema-selection rules defined by the **Schema Loading Specification**.
In particular, absent an explicitly provided schema, the parser uses the
built-in **bootstrap schema-of-schemas**, enabling schema documents to be parsed
without circular dependency.

See the **Language Specification § Schema-First Parsing** and the
**Schema Loading Specification** (`spec/0.1/schema-loading/index.md`) for details.

The normative definition of the bootstrap schema-of-schemas itself is:

* `spec/0.1/schema-loading/bootstrap-schema-of-schemas/index.md`

---

**End of Codex Formal Grammar Specification v0.1**
