Status: NORMATIVE  
Version: 0.1  
Editor: Charles F. Munat

# Codex Formatting Error Rules — Version 0.1

This document defines **how formatting-related errors are classified and handled**
in the Codex language.

Formatting error rules are part of the Codex language specification and are governed
by this document.

This document is **Normative**.

---

## 1. Purpose

This contract defines **formatting and normalization error handling** in Codex.

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

Formatting errors MAY arise during validation or normalization,
but MUST NOT alter phase ordering.

---

## 3. Parse Errors vs Formatting Errors (Normative)

### Parse Errors

Parse errors occur when the input cannot be read into a valid syntactic structure.

Examples include:

- malformed Concept markers
- invalid quoting
- broken indentation
- unterminated Concepts
- unterminated annotations

Parse errors halt processing immediately.

---

### Formatting Errors

Formatting errors occur when:

- input parses successfully
- but violates **canonical surface form rules**

Formatting errors are **distinct from semantic, schema, or validation errors**.

---

## 4. Canonical Form Requirement (Normative)

Every valid Codex document MUST normalize to **exactly one canonical textual form**.

If canonicalization is not possible, the document is invalid.

There is no “closest” or “best-effort” canonical form.

---

## 5. Classes of Formatting Errors

Formatting errors include (non-exhaustive):

- expanded empty Concepts
- non-canonical indentation
- invalid whitespace placement
- invalid casing of Concept or Trait names
- multiple blank lines where forbidden
- blank lines in invalid positions
- non-canonical Trait ordering
- invalid line continuations
- misplaced or malformed annotations

Each listed violation is a **formatting error**, not a schema error.

---

## 6. Annotation Formatting Errors (Normative)

The following are **formatting errors** related to annotations.

### 6.1 Structural Errors

Structural annotation errors include:

- unterminated editorial annotations (`[` without matching `]`)
- nested editorial annotations
- editorial annotations appearing inside Content
- editorial annotations appearing inside Concept markers
- editorial annotations appearing inside Trait names or values

Structural annotation errors are **fatal formatting errors**.

---

### 6.2 Canonicalization Errors

Canonicalization errors include:

- annotation placement that cannot be deterministically attached to a target Concept
- ambiguous attachment caused by invalid whitespace or structure
- editorial annotations that split a syntactic unit
  (e.g. between a marker name and its Traits)

If deterministic attachment cannot be established, normalization MUST fail.

---

### 6.3 Typed Annotation Errors

The following conditions apply:

- editorial annotations with malformed type prefixes (e.g. missing colon)
  are **formatting errors**
- unrecognized editorial prefixes are **not errors** and are treated as literal text
- `<Annotation>` Concepts with invalid structure or invalid `kind` Trait values
  are **schema errors**, not formatting errors

Error classification MUST follow this distinction.

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

Examples include:

- ambiguous indentation
- conflicting sectioning rules
- invalid but unfixable whitespace patterns
- annotation attachment ambiguity

---

## 9. Formatting vs Schema Errors

The following distinction is mandatory:

- Formatting errors concern **how** Codex is written
- Schema errors concern **what** Codex means

A document MAY contain both kinds of errors, but tools MUST classify them correctly.

Tools MUST NOT report schema errors when the true cause is a formatting error.

---

## 10. Error Reporting Requirements

Formatting error reports SHOULD include:

- error classification: `FormattingError`
- violated rule reference (surface form section)
- location (line number or Concept path)
- expected canonical form, when applicable

Exact wording and presentation are tool-defined.

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

---

End of Codex Formatting Error Rules v0.1.
