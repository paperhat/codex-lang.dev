Status: NORMATIVE  
Version: 0.1  
Editor: Charles F. Munat

# **Codex Surface Form Specification — Version 0.1 (FINAL, CORE)**

This specification defines the **surface form** of Codex documents: the concrete
spellings authors write and tools parse.

It governs:

* Concept markers (`<...>`, `</...>`, `/>`)
* Traits and their Values
* **Multiline Annotations**
* Content blocks (opaque narrative text)
* Whitespace significance for deterministic parsing
* String literal escaping
* Structural requirements necessary for canonicalization

This specification is **core language**.
It contains **no Module, Dialect, Gloss, Paperhat, or tooling concerns**.

---

# Codex Surface Form Specification — Version 0.1

## 1. Purpose

The Codex surface form exists to:

* read as structured, precise English
* be deterministic to parse
* be mechanically canonicalizable
* support lossless round-tripping
* avoid heuristic or best-effort interpretation

This specification defines **what is parseable Codex**.

---

## 2. Fundamental Constructs (Normative)

Codex documents are composed of **Concepts**.

A Concept MAY include:

* zero or more **Traits**
* zero or more **child Concepts**
* optional **Content**
* optional **Annotations**

---

## 3. Annotations (Normative)

Annotations are **editorial metadata**.
They are not Values, not Content, and not interpreted by Codex.

---

### 3.1 Annotation Form

An Annotation consists of all text from an opening `[` to a matching closing `]`.

Annotations:

* MAY span multiple lines
* MAY contain arbitrary text
* MUST attach to the **next Concept**
* MUST NOT be nested

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
* The closing `]` MUST terminate the annotation
* There MUST be no blank line between an Annotation and the Concept it annotates
* Annotations MAY contain blank lines internally

---

### 3.3 Escaping

Within an Annotation:

* `\]` represents a literal `]`
* `\\` represents a literal `\`

No other escape sequences are defined.

---

### 3.4 Annotation Whitespace

Annotations preserve their authored text for tooling purposes.

For canonical surface form:

* leading and trailing whitespace is trimmed
* internal runs of whitespace (spaces, tabs, newlines) are collapsed to a single space
* escaped characters remain escaped

If whitespace collapse would make attachment ambiguous, canonicalization MUST fail.

---

## 4. Concept Markers (Normative)

---

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

Rules:

* MUST match the most recent unclosed Concept
* No additional content is permitted on the line

---

### 4.3 Self-Closing Marker

```
<ConceptName />
<ConceptName trait=value />
```

Rules:

* Represents a Concept with no Content and no children
* MAY include Traits

---

## 5. Traits (Normative)

A Trait is written as:

```
traitName=value
```

Rules:

* No whitespace is permitted around `=`
* Traits are separated by whitespace
* Trait order is preserved
* Trait names are schema-authorized

---

## 6. Values (Normative)

Values are literal spellings defined by the **Naming and Value Specification**.

Rules:

* No leading or trailing whitespace
* Parsed mechanically
* Not evaluated or normalized by Codex

Balanced delimiters (`[]`, `{}`, `()`) MUST be respected during parsing.

---

## 7. Content Blocks (Normative)

Content is opaque narrative text between opening and closing Concept markers.

Example:

```cdx
<Description>
	This is text.
	It is opaque to Codex.
</Description>
```

Rules:

* Content is **not** a Value
* Content is **not** parsed
* Content MUST be indented relative to its Concept
* Content MAY contain blank lines and arbitrary characters

---

## 8. Whitespace Significance (Normative)

### 8.1 Insignificant Whitespace

* Multiple spaces between tokens are equivalent
* Line breaks between Traits act as separators

---

### 8.2 Significant Boundaries

The following delimiters are structurally significant:

* `<`, `</`, `>`, `/>`
* `[` as the first non-whitespace character of a line
* the matching `]` that closes an Annotation
* string literal delimiters `"`

---

## 9. Structural Grammar (Normative)

### 9.1 Document

```
Document ::= (Annotation | BlankLine)* RootConcept (BlankLine)*
```

A document MUST contain exactly one root Concept.

---

### 9.2 Concept Forms

```
Concept ::= BlockConcept | SelfClosingConcept
```

---

### 9.3 Block Concept

```
BlockConcept ::=
	OpeningMarker
	(Annotation | ChildConcept | ContentLine | BlankLine)*
	ClosingMarker
```

---

## 10. String Literal Escaping (Normative)

String Values are written as:

```
"..."
```

Rules:

* Single-line only
* Escapes:

  * `\"` → `"`
  * `\\` → `\`
  * `\uXXXX`, `\u{H...}` → Unicode scalar
* All other escapes are forbidden
* Raw line breaks are forbidden

---

## 11. Canonical Surface Requirements (Normative)

A valid Codex document MUST be transformable into **exactly one canonical surface form**.

Surface requirements include:

* deterministic indentation
* canonical Trait spacing
* canonical Annotation whitespace collapse
* canonical string escaping

If canonicalization cannot be performed mechanically, the document is invalid.

---

## 12. Prohibited Behaviors (Normative)

Codex tools MUST NOT:

* infer missing structure
* silently rewrite Content
* silently correct surface errors
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

* Codex surface form is deterministic and canonicalizable
* Annotations are multiline, escaped, and editorial
* Content is opaque and distinct from Values
* Canonicalization is mechanical or fails
* No heuristics, no guessing

---

**End of Codex Surface Form Specification v0.1**
