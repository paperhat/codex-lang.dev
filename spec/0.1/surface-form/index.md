Proceeding.

## **Codex Surface Form Specification — Version 0.1 (REVISED, CORE-ONLY)**

**Status:** NORMATIVE
**Version:** 0.1
**Editor:** Charles F. Munat

This specification defines the **surface form** of Codex documents: the concrete spellings authors write and tools parse.

It governs:

* Concept markers (`<...>`, `</...>`, `/>`)
* Traits and their Values
* **Multiline Annotations**
* Content blocks (opaque narrative text)
* Whitespace significance required for deterministic parsing
* String literal escaping
* **Canonicalization rules for surface form**

This document governs **surface form and canonicalization only**.
It does **not** define schemas, semantics, modules, dialects, or inline text markup.

---

## 1. Purpose

The Codex surface form exists to:

* read as plain-English structured markup
* be deterministic to parse
* support lossless round-tripping
* admit exactly **one canonical textual form**
* avoid heuristic or best-effort interpretation

---

## 2. Fundamental Constructs (Normative)

Codex documents are composed of **Concepts**.

A Concept may include:

* zero or more **Traits**
* zero or more **child Concepts**
* optional **Content**
* optional **Annotations** (editorial)

---

## 3. Annotations (Normative)

Annotations are **editorial metadata**, not Values and not Content.

### 3.1 Annotation Form

An Annotation consists of everything from an opening `[` to a matching closing `]`.

Annotations:

* MAY span multiple lines
* MAY contain arbitrary text
* attach to the **next Concept**
* are not nested
* are not interpreted by Codex

Example:

```cdx
[This
 is a
 multiline annotation.]
<Recipe>
```

---

### 3.2 Structural Rules

* The opening `[` MUST be the **first non-whitespace character** on its line
* The closing `]` MUST terminate the annotation (may appear on any line)
* There MUST be no blank line between an Annotation and the Concept it annotates
* Annotations MAY contain blank lines internally

---

### 3.3 Escaping

Within an Annotation:

* `\]` represents a literal `]`
* `\\` represents a literal `\`

No other escapes are defined.

---

### 3.4 Canonicalization of Annotations

For canonical form:

* Leading and trailing whitespace inside the annotation is trimmed
* Internal runs of whitespace (spaces, tabs, newlines) are collapsed to a single space
* Escaped characters are preserved as written

If whitespace collapse would make attachment ambiguous, canonicalization MUST fail.

---

## 4. Concept Markers (Normative)

### 4.1 Opening Marker

```
<ConceptName>
<ConceptName trait=value>
```

Rules:

* `ConceptName` MUST follow naming rules
* Traits MAY appear inline
* Trait order is preserved

---

### 4.2 Closing Marker

```
</ConceptName>
```

* MUST match the most recent unclosed Concept

---

### 4.3 Self-Closing Marker

```
<ConceptName />
<ConceptName trait=value />
```

* Represents a Concept with no Content and no children

---

## 5. Traits (Normative)

A Trait is written as:

```
traitName=value
```

Rules:

* No whitespace around `=`
* Traits separated by whitespace
* Trait names are schema-authorized
* Trait order is preserved

---

## 6. Values (Normative)

Values are literal spellings defined by the **Naming and Value Specification**.

Rules:

* No leading or trailing whitespace
* Parsed mechanically
* Not evaluated or normalized

Balanced delimiters (`[]`, `{}`, `()`) MUST be respected during parsing.

---

## 7. Content Blocks (Normative)

Content is opaque narrative text between opening and closing markers.

Example:

```cdx
<Description>
	This is text.
	It is opaque to Codex.
</Description>
```

Rules:

* Content is not a Value
* Content is not parsed
* Content MUST be indented relative to its Concept
* Content MAY contain blank lines and arbitrary characters

---

## 8. Whitespace Significance (Normative)

### 8.1 Insignificant Whitespace

* Multiple spaces between tokens are equivalent
* Line breaks between Traits are separators

---

### 8.2 Significant Boundaries

The following are structural delimiters:

* `<`, `</`, `>`, `/>`
* `[` as first non-whitespace character
* matching `]` ending an Annotation
* string literal delimiters `"`

---

## 9. Structural Grammar (Normative)

### 9.1 Document

```
Document ::= (Annotation | BlankLine)* RootConcept (BlankLine)*
```

Exactly one root Concept is required.

---

### 9.2 Concept Forms

```
Concept ::= BlockConcept | SelfClosingConcept
```

---

### 9.3 Block Concept

```
<BlockConcept> ::= OpeningMarker
                   (Annotation | ChildConcept | ContentLine | BlankLine)*
                   ClosingMarker
```

---

## 10. String Literals (Normative)

String Values:

```
"..."
```

Rules:

* Single-line only
* Escapes:

  * `\"` → `"`
  * `\\` → `\`
  * `\uXXXX`, `\u{H...}` → Unicode scalar
* No other escapes permitted
* No raw line breaks allowed

---

## 11. Canonical Surface Form (Normative)

A valid Codex document MUST normalize to **exactly one canonical textual form**.

Canonicalization rules:

* Deterministic indentation
* Canonical Trait spacing
* Canonical Annotation whitespace collapse
* Canonical string escaping
* No reordering of Concepts, Traits, or Content

If canonicalization cannot be performed mechanically, the document is invalid.

---

## 12. Prohibited Behaviors (Normative)

Tools MUST NOT:

* infer missing structure
* silently rewrite Content
* silently correct formatting errors
* accept multiple canonical forms

---

## 13. Non-Goals

This specification does **not**:

* define schemas or validation rules
* define inline text markup
* define modules or dialects
* define rendering or execution semantics

---

## 14. Summary

* Codex surface form is deterministic and canonical
* Annotations are multiline, escaped, and editorial
* Content is opaque and distinct from Values
* Canonicalization is mechanical or fails
* No heuristics, no guessing

---

**End of Codex Surface Form Specification v0.1**

---

Next (unless redirected):
**Codex Identifier Specification — Revised (semantic density explicit, no resolution)**
