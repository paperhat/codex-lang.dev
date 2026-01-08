# Codex Formatting Error Rules (DRAFT)

## Status

- **DRAFT**  
- Normative once locked  
- Applies to all Codex formatters, validators, and normalization tooling

---

## 1. Purpose

This contract defines **how formatting-related errors are classified and handled** in Codex.

Its goals are to:

- draw a hard boundary between parsing, formatting, and semantics
- make canonicalization deterministic and enforceable
- eliminate heuristic or “best-effort” formatting behavior
- ensure round-tripping without reliance on source offsets

This contract governs **formatting and normalization errors only**.

---

## 2. Formatting Phases

Codex processing follows this strict sequence:

1. **Parse**
2. **Validate**
3. **Normalize (canonicalize)**
4. _(Optional)_ Re-parse canonical form

Formatting errors may arise in phases 2 or 3, but **never** alter phase ordering.

---

## 3. Parse vs Formatting Errors (Normative)

### Parse Errors

Parse Errors occur when the input cannot be read into a syntactic structure.

Examples:

- malformed Concept markers
- invalid quoting
- broken indentation
- unterminated Concepts
- unterminated annotations

Parse Errors halt processing immediately.

---

### Formatting Errors

Formatting Errors occur when:

- input parses successfully
- but violates **canonical surface form rules**

Formatting Errors are **distinct from semantic or schema errors**.

---

## 4. Canonical Form Requirement (Normative)

Every valid Codex document MUST normalize to **exactly one canonical textual form**.

If canonicalization is not possible, the document is invalid.

There is no “closest” or “best-effort” canonical form.

---

## 5. Classes of Formatting Errors

Formatting Errors include (non-exhaustive):

- expanded empty Concepts
- non-canonical indentation
- invalid whitespace placement
- invalid casing of Concept or Trait names
- multiple blank lines where forbidden
- blank lines in invalid positions
- non-canonical Trait ordering
- invalid line continuations
- **misplaced or malformed annotations**

Each violation is a **formatting error**, not a schema error.

---

## 6. Annotation Formatting Errors (Normative)

The following are **formatting errors** related to annotations:

### 6.1 Structural Errors

- Unterminated editorial annotation (`[` without matching `]`)
- Nested editorial annotations
- Editorial annotation appearing inside Content
- Editorial annotation appearing inside a Concept marker
- Editorial annotation appearing inside a Trait name or value

These are **fatal errors**.

---

### 6.2 Canonicalization Errors

- Annotation placement that cannot be deterministically attached to a target Concept
- Ambiguous attachment caused by invalid whitespace or structure
- Editorial annotation that splits a syntactic unit (e.g. between a marker name and its Traits)

If deterministic attachment cannot be established, normalization MUST fail.

---

### 6.3 Typed Annotation Errors

- Editorial annotation with a malformed type prefix (e.g. missing colon)
- `<Annotation>` Concept with an invalid or non-canonical `kind` Trait value
- `<Annotation>` Concept missing required structure defined by schema

Unrecognized editorial prefixes are **not errors**; they are treated as plain text.
Invalid `<Annotation>` Concepts are schema errors, not formatting errors.

---

## 7. Formatter Behavior (Normative)

Codex formatters:

- MUST produce canonical output
- MUST preserve all annotations
- MUST preserve annotation attachment targets
- MUST NOT reorder Concepts or collections
- MUST NOT invent or remove Concepts, Traits, or annotations
- MUST NOT infer missing structure
- MUST NOT depend on source offsets

Formatting is purely mechanical.

---

## 8. Normalization Failures

A **normalization failure** occurs when:

- input parses and validates
- but cannot be transformed into canonical form

Normalization failures are **fatal formatting errors**.

Examples:

- ambiguous indentation
- conflicting sectioning rules
- invalid but unfixable whitespace patterns
- annotation attachment ambiguity

---

## 9. Formatting vs Schema Errors

The following distinctions are mandatory:

- Formatting Errors concern **how** Codex is written
- Schema Errors concern **what** Codex means

A document MAY have both, but errors MUST be classified correctly.

Tools MUST NOT report schema errors when the true cause is formatting.

---

## 10. Error Reporting Requirements

Formatting error reports SHOULD include:

- error classification: `FormattingError`
- violated rule reference (surface form section)
- location (line number or Concept path)
- expected canonical form (if applicable)

Exact wording and UI presentation are tool-defined.

---

## 11. Prohibited Behaviors (Normative)

Codex tools MUST NOT:

- silently normalize invalid input
- auto-correct formatting errors without reporting them
- accept multiple canonical forms
- treat formatting errors as warnings
- discard annotations during formatting

If formatting is wrong, the document is invalid.

---

## 12. Non-Goals

This contract does **not**:

- define editor integrations
- prescribe auto-format-on-save behavior
- define diff or patch semantics
- define pretty-printing options
- replace the Surface Form Contract

It strictly defines **error classification and enforcement**.

---

## 13. Summary

- Canonical formatting is mandatory
- Formatting errors are distinct from parse and schema errors
- Annotations are formatting-relevant and must be preserved
- Normalization must be deterministic or fail
- No heuristic or silent correction is permitted
- Codex formatting is mechanical and enforceable
