Status: NORMATIVE
Lock State: UNLOCKED
Version: 0.1
Editor: Charles F. Munat

# Codex Formatting and Canonicalization Specification — Version 0.1

This specification defines **formatting rules and canonicalization requirements**
for Codex documents.

It governs:

* the distinction between parsing, surface form, formatting, and validation
* deterministic canonical surface form
* classification of formatting and canonicalization failures

This specification is **core language**.

---

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

1. **Schema Resolution** — obtain the governing schema for the document
2. **Decode + Newline Normalization** — determine encoding and normalize CRLF to LF
3. **Formatting + Canonicalization (Mandatory)** — schema-directed structural read
   that produces:
   * a canonical surface form (text)
   * a parsed document model (AST) suitable for validation
4. **Semantic Validation** — schema rule evaluation (constraints, cardinality,
   identity, references)

Schema resolution MUST occur before any schema-directed structural read.
See **Schema Loading Specification**.

Formatting is not optional. A conforming Codex tool MUST run formatting and
canonicalization before semantic validation.

Formatting + canonicalization MUST be performed in a way that does not require
re-parsing. The parsed output produced during formatting is the parsed document
used for subsequent semantic validation.

---

## 2.1 Schema-Less Formatting Mode (Optional) (Normative)

Codex is schema-first: full parsing requires a governing schema.

However, an implementation MAY provide a **schema-less formatter** mode intended
only for document cleanup (lexical normalization).

If provided, a schema-less formatter:

* MUST NOT claim that its output is valid under any schema
* MUST NOT report schema/semantic error classes (e.g., `SchemaError`,
   `IdentityError`, `ReferenceError`, `ConstraintError`)
* MAY normalize encoding and line endings
* MAY normalize whitespace, blank-line layout, Trait layout, and annotation
   whitespace

Schema-less formatting is not validation. It exists to produce a consistent
surface form without consulting schema meaning.

---

## 3. Parse Errors vs Formatting Errors (Normative)

### 3.1 Parse Errors

Parse Errors occur when input cannot be read into a syntactic structure under
the governing schema.

Examples:

* unbalanced Concept markers
* invalid string literal escaping
* malformed Traits
* unterminated Annotations

Parse Errors are **fatal** and halt processing immediately.

---

### 3.2 Formatting Errors

Formatting Errors occur when:

* input can be structurally read
* but cannot be transformed into canonical surface form deterministically

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
* canonical inline-annotation whitespace collapse
* canonical string escaping
* preservation of Concept, Trait, and Content order

Canonicalization MUST NOT:

* reorder Concepts
* reorder Traits
* invent or remove Concepts, Traits, or Content
* infer missing structure

---

## 6. Annotation Canonicalization (Normative)

Annotation canonicalization MUST follow the **Surface Form Specification**.

In particular:

* Inline annotations collapse internal whitespace to single spaces and trim
   leading/trailing whitespace (as described in the Surface Form Specification)
* Block annotations preserve internal line structure
* Block annotations with `CODE:` or `MD:` directives are byte-preserving: tools
   MUST NOT reindent, trim, strip trailing whitespace, wrap, or interpret escapes
   within those blocks

If attachment cannot be determined deterministically, canonicalization MUST fail.

---

## 6.1 Allowed vs Forbidden Changes (Normative)

The formatter/canonicalizer exists to produce a single canonical surface form
without changing meaning.

Allowed changes (examples):

* Normalize newlines to LF and ensure a trailing newline
* Normalize structural indentation (tabs) for Concept markers and children bodies
* Canonicalize trait layout/spacing without reordering traits
* Canonicalize inline annotation whitespace (trim + internal collapse)
* Canonicalize grouping-annotation labels by whitespace normalization
* Normalize UUID spelling (e.g., hex lowercase) where explicitly specified

Forbidden changes (examples):

* Reorder Concepts or Traits
* Change Content bytes
* Change any bytes inside `CODE:` or `MD:` block annotations
* Guess annotation attachment or reinterpret annotation kinds
* Invent, remove, or rename Concepts/Traits/Values

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
