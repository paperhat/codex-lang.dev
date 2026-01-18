Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1
Editor: Charles F. Munat

# **Codex Formatting and Canonicalization Specification — Version 0.1 (FINAL, CORE)**

This specification defines **formatting rules and canonicalization requirements**
for Codex documents.

It governs:

* the distinction between parsing, surface form, formatting, and validation
* deterministic canonical surface form
* classification of formatting and canonicalization failures

This specification is **core language**.
It replaces and supersedes the former **Formatting Error Rules** specification.

---

# Codex Formatting and Canonicalization Specification — Version 0.1

## 1. Purpose

This specification defines how Codex documents are:

* **formatted**
* **canonicalized**
* **rejected** when canonicalization is not possible

Its goals are to:

* ensure exactly one canonical surface form
* eliminate heuristic or best-effort formatting
* enable mechanical, explainable normalization
* support lossless round-tripping

This specification governs **formatting and canonicalization only**.

---

## 2. Processing Phases (Normative)

Codex processing follows this strict sequence:

1. **Parse**
2. **Surface Form Validation**
3. **Formatting and Canonicalization**
4. **Schema Validation**

Formatting MUST NOT alter phase ordering.

---

## 3. Parse Errors vs Formatting Errors (Normative)

### 3.1 Parse Errors

Parse Errors occur when input cannot be read into a syntactic structure.

Examples:

* unbalanced Concept markers
* invalid string literal escaping
* malformed Traits
* unterminated Annotations

Parse Errors are **fatal** and halt processing immediately.

---

### 3.2 Formatting Errors

Formatting Errors occur when:

* input parses successfully
* but cannot be transformed into canonical surface form

Formatting Errors are **distinct** from schema or semantic errors.

---

## 4. Canonical Form Requirement (Normative)

Every valid Codex document MUST normalize to **exactly one canonical textual form**.

Canonicalization:

* is deterministic
* is mechanical
* preserves meaning and Content
* never guesses author intent

If canonicalization cannot be performed unambiguously, the document is invalid.

---

## 5. Canonicalization Rules (Normative)

Canonicalization includes, at minimum:

* deterministic indentation
* canonical spacing of Traits
* canonical placement of self-closing markers
* canonical Annotation whitespace collapse
* canonical string escaping
* preservation of Concept, Trait, and Content order

Canonicalization MUST NOT:

* reorder Concepts
* reorder Traits
* invent or remove Concepts, Traits, or Content
* infer missing structure

---

## 6. Annotation Canonicalization (Normative)

Annotations MUST:

* preserve attachment to the annotated Concept
* preserve escaped characters
* collapse internal whitespace to single spaces
* trim leading and trailing whitespace

If attachment cannot be determined deterministically, canonicalization MUST fail.

---

## 7. Normalization Failures (Normative)

A **canonicalization failure** occurs when:

* indentation is ambiguous
* annotation attachment is ambiguous
* whitespace cannot be normalized without changing meaning
* structural inconsistencies prevent a unique surface form

Canonicalization failures are **fatal formatting errors**.

---

## 8. Formatting vs Schema Errors (Normative)

Mandatory distinction:

* **Formatting errors** concern *how* Codex is written
* **Schema errors** concern *what* Codex means

Tools MUST NOT report schema errors when the root cause is a formatting failure.

---

## 9. Error Classification (Normative)

Formatting and canonicalization failures MUST be classified as:

```
FormattingError
```

They MUST NOT be downgraded to warnings.

---

## 10. Prohibited Behaviors (Normative)

Codex tools MUST NOT:

* silently normalize invalid input
* auto-correct formatting errors without reporting them
* accept multiple canonical forms
* discard or rewrite Content
* depend on source offsets or editor state

---

## 11. Reporting Requirements

Formatting error reports SHOULD include:

* error class (`FormattingError`)
* violated rule
* location (line number or Concept path)
* explanation of canonicalization failure

Exact wording is tool-defined.

---

## 12. Non-Goals

This specification does **not**:

* define editor behavior
* prescribe auto-format-on-save policies
* define diff or patch semantics
* define schema validation rules
* define rendering or execution behavior

---

## 13. Summary

* Canonical surface form is mandatory
* Canonicalization is mechanical and deterministic
* Formatting errors are fatal
* No heuristic or best-effort formatting is permitted
* Formatting is separate from schema validation

---

**End of Codex Formatting and Canonicalization Specification v0.1**
