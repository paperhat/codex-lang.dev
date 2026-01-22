Status: NON-NORMATIVE (Historical; consolidated into codex-language-specification.md §10)
Lock State: UNLOCKED
Version: 0.1
Editor: Charles F. Munat

# Codex Formatting and Canonicalization Specification — Version 0.1

This document is retained for historical/reference purposes.

The authoritative normative content is consolidated into `spec/0.1/codex-language-specification.md` §10.

This specification defines **formatting rules and canonicalization requirements**
for Codex documents.

It governs:

* the distinction between parsing, surface form, formatting, and validation
* canonical surface form requirements (see `spec/0.1/language/index.md` for the
   determinism and no-heuristics invariants)
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
* ensure formatting/canonicalization conforms to the language invariants
   (`spec/0.1/language/index.md`), including the prohibition of heuristics
* enable mechanical, explainable normalization
* support lossless round-tripping

This specification governs **formatting and canonicalization only**.

---

## 2. Processing Phases (Normative)

Codex supports two related pipelines:

1. **Schema-less formatting / well-formedness check** (no schema required)
2. **Semantic validation** (schema required)

Formatting and canonicalization are not optional in the full pipeline.
However, schema availability is required only for semantic validation.

---

## 2.1 Schema-Less Formatting Mode (Required) (Normative)

An implementation MUST provide a **schema-less formatting / canonicalization**
mode that can be run without a governing schema.

This mode exists to support well-formedness and formatting checks (gofmt-like),
independent of semantic validation.

If provided, a schema-less formatter:

* MUST NOT claim that its output is valid under any schema
* MUST NOT report schema/semantic error classes (e.g., `SchemaError`,
   `IdentityError`, `ReferenceError`, `ConstraintError`)
* MUST normalize encoding and line endings as defined by the **Surface Form
   Specification** (`spec/0.1/surface-form/index.md`)
* MUST apply the canonical form requirement defined in § 4
* MAY normalize whitespace, blank-line layout, Trait layout, and annotation
   whitespace

Schema-less formatting is not validation. It exists to produce a consistent
surface form without consulting schema meaning.

## 2.2 Full Validation Pipeline (Normative)

To validate a document under a schema, a conforming tool MUST follow this
sequence:

1. **Decode + Newline Normalization**
2. **Formatting + Canonicalization (Mandatory)** — using the schema-less mode
   defined in § 2.1
3. **Schema Resolution** — obtain the governing schema for the document
4. **Semantic Validation** — schema rule evaluation (constraints, cardinality,
   identity, references)

Schema resolution is required before semantic validation.
See the **Schema Loading Specification**.

---

## 3. Parse Errors vs Formatting Errors (Normative)

### 3.1 Parse Errors

This specification uses the `ParseError` class as defined by the **Validation
Error Taxonomy** (`spec/0.1/validation-errors/index.md`).

During formatting + canonicalization, a failure MUST be classified as
`ParseError` when input cannot be read into the syntactic structure required to
produce a parsed document model (AST) under the governing schema.

---

### 3.2 Formatting Errors

This specification uses the `FormattingError` class as defined by the
**Validation Error Taxonomy** (`spec/0.1/validation-errors/index.md`).

During formatting + canonicalization, a failure MUST be classified as
`FormattingError` when input can be structurally read, but cannot be transformed
into canonical surface form deterministically.

`FormattingError` is distinct from schema or semantic error classes.

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

* canonical encoding and newline normalization (see `spec/0.1/surface-form/index.md`)
* deterministic indentation
* no trailing whitespace on lines
* no trailing blank lines at end of file
* exactly one blank line between sibling Concepts
* canonical spacing of Traits
* canonical Trait layout (1–2 Traits on one line; 3+ Traits on separate lines)
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
* Block annotations with `CODE:` or `MARKDOWN:` directives are byte-preserving: tools
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
* Change any bytes inside `CODE:` or `MARKDOWN:` block annotations
* Guess annotation attachment or reinterpret annotation kinds
* Invent, remove, or rename Concepts/Traits/Values

---

## 7. Normalization Failures (Normative)

A **canonicalization failure** occurs when:

* indentation is ambiguous
* annotation attachment is ambiguous
* whitespace cannot be normalized without changing meaning
* structural inconsistencies prevent a unique surface form

Canonicalization failures MUST be classified as `FormattingError` as defined by
the **Validation Error Taxonomy** (`spec/0.1/validation-errors/index.md`).

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
* Formatting failures are classified as `FormattingError` (see `spec/0.1/validation-errors/index.md`)
* No heuristic or best-effort formatting is permitted
* Formatting is separate from schema validation

---

**End of Codex Formatting and Canonicalization Specification v0.1**
