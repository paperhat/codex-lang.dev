Status: NORMATIVE
Version: 0.1
Editor: Charles F. Munat

# Codex Formatting and Canonicalization Specification — Version 0.1

This document defines **canonical formatting and normalization rules** for Codex
documents.

It specifies:

* what it means for a Codex document to be **canonical**
* how canonical form is produced
* which formatting conditions are errors
* when normalization MUST fail

This document governs **formatting and normalization only**.
It does **not** define parsing, schemas, identity, or semantic meaning.

This document is **Normative**.

---

## 1. Purpose

This specification exists to:

* ensure every valid Codex document has **exactly one canonical textual form**
* make formatting **deterministic, mechanical, and enforceable**
* eliminate heuristic or best-effort normalization
* support stable diffs, round-tripping, and reproducible builds
* ensure tools and humans agree on document equivalence

Formatting is a **pure function** over valid Codex syntax.

---

## 2. Processing Phases (Normative)

Codex processing occurs in the following strict order:

1. **Parse**
2. **Validate**
3. **Canonicalize**
4. *(Optional)* Re-parse canonical form

Canonicalization MUST NOT alter this ordering.

Formatting errors MAY be detected during validation or canonicalization, but
canonicalization MUST NOT attempt to repair invalid input.

---

## 3. Definition of Canonical Form (Normative)

A Codex document is in **canonical form** if and only if:

* it conforms to the Codex Surface Form Specification
* it satisfies all schema and validation rules
* it obeys all formatting rules defined in this document
* no further canonicalization step would change its textual representation

For every valid Codex document, there MUST exist **exactly one** canonical textual
representation.

If no such representation exists, the document is invalid.

---

## 4. Canonicalization Is Mechanical (Normative)

Canonicalization:

* MUST be deterministic
* MUST be total over valid input
* MUST NOT depend on source offsets, editor state, or tool configuration
* MUST NOT consult schemas for formatting decisions
* MUST NOT infer missing structure
* MUST NOT invent, remove, or reorder semantic content

Canonicalization operates **only on surface structure and whitespace**.

---

## 5. Canonicalization Outputs (Normative)

Canonicalization MUST:

* preserve all Concepts, Traits, Values, Content, and annotations
* preserve Concept nesting and document structure
* preserve semantic order where order is meaningful
* preserve author-authored literal spellings (Values)

Canonicalization MUST NOT:

* reorder Concepts
* reorder child Concepts
* reorder lists
* reorder Traits
* normalize numeric, temporal, or color literals
* rewrite Content text
* discard annotations

---

## 6. Canonical Whitespace Rules (Normative)

### 6.1 Line Endings

* Canonical documents MUST use LF (`\n`) line endings.

---

### 6.2 Indentation

* Indentation MUST be performed using **tabs**.
* One indentation level corresponds to **one tab character**.
* Spaces MUST NOT be used for indentation.

---

### 6.3 Blank Lines

* No more than **one consecutive blank line** is permitted anywhere.
* Blank lines at the start of the document are forbidden.
* Blank lines at the end of the document are forbidden.

---

### 6.4 Trailing Whitespace

* Trailing whitespace on any line is forbidden.

---

## 7. Canonical Concept Formatting (Normative)

### 7.1 Opening Markers

* Opening markers MUST appear on their own line.
* Traits MAY appear on the same line or on subsequent lines.
* If Traits span multiple lines:

  * each Trait MUST appear on its own line
  * Trait lines MUST be indented one level deeper than the Concept marker

Example (canonical):

```cdx
<Recipe
	id=recipe:spaghetti
	servings=4
>
```

---

### 7.2 Self-Closing Concepts

* Self-closing Concepts MUST appear on a single line.
* Traits MUST appear inline unless line length exceeds tool-defined limits.
* If line wrapping occurs, the same multi-line Trait rules as §7.1 apply.

---

### 7.3 Closing Markers

* Closing markers MUST appear on their own line.
* Closing markers MUST align with their opening marker.

---

## 8. Canonical Trait Formatting (Normative)

* Trait order is **preserved as authored**.
* No whitespace is permitted around `=`.
* Exactly one space or line break separates adjacent Traits.

Canonicalization MUST NOT reorder Traits.

---

## 9. Canonical Annotation Formatting (Normative)

### 9.1 Placement

* An annotation MUST immediately precede the Concept it annotates.
* No blank line is permitted between an annotation and its target Concept.

---

### 9.2 Whitespace Normalization

Annotation text MUST be normalized as follows:

* leading and trailing whitespace removed
* all internal runs of whitespace collapsed to a single space

The canonical annotation MUST be emitted on a **single line**.

Example:

```cdx
[This is an annotation.]
```

---

### 9.3 Escaping

* Literal `]` MUST be emitted as `\]`
* Literal `\` MUST be emitted as `\\`

---

## 10. Canonical Content Formatting (Normative)

* Content text MUST be preserved exactly as authored.
* Content lines MUST be indented one level deeper than their enclosing Concept.
* Canonicalization MUST NOT:

  * trim Content
  * reflow Content
  * normalize whitespace inside Content
  * alter line breaks inside Content

Content is opaque.

---

## 11. Canonical Document Structure (Normative)

* A document MUST contain exactly one root Concept.
* Annotations MAY appear before the root Concept but MUST attach to it.
* Canonicalization MUST remove any redundant blank lines.

---

## 12. Canonicalization Failures (Normative)

Canonicalization MUST fail if:

* indentation is ambiguous
* tabs and spaces are mixed for indentation
* annotation attachment is ambiguous
* annotation spans are unterminated
* annotation normalization would change attachment semantics
* surface form violations cannot be normalized mechanically

A canonicalization failure is a **fatal formatting error**.

---

## 13. Formatting Errors (Normative)

A **Formatting Error** occurs when:

* input parses successfully
* validation succeeds
* but canonical form cannot be produced

Formatting Errors are **fatal**.

Formatting Errors MUST NOT be downgraded to warnings.

---

## 14. Error Classification

Formatting Errors MUST be reported as a single primary error class.

They MUST NOT be misclassified as:

* parse errors
* schema errors
* identity errors
* reference errors

---

## 15. Non-Goals

This specification does **not**:

* define editor behavior
* prescribe auto-format-on-save
* define pretty-printing options
* define diff or patch semantics
* define schema-dependent formatting rules

It defines **one canonical form**, not multiple styles.

---

## 16. Summary

* Every valid Codex document has exactly one canonical form
* Canonicalization is deterministic and mechanical
* Formatting is not semantic
* No heuristic correction is permitted
* Ambiguity causes failure, not guesswork
* Canonical form is the foundation for stable tooling

---

**End of Codex Formatting and Canonicalization Specification v0.1**
