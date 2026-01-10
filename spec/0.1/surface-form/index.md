Status: NORMATIVE  
Version: 0.1  
Editor: Charles F. Munat

# Codex Surface Form Specification

This specification defines the **surface form** of Codex documents: the concrete spellings authors write and tools parse.

It governs:

* Concept markers (`<...>`, `</...>`, `/>`)
* Traits and their Values
* Annotation lines (`[ ... ]`)
* Content blocks (opaque narrative content)
* Whitespace significance required for deterministic parsing
* String literal escaping

This document governs **surface form only**.
It does not define schemas or domain semantics.

---

## 1. Purpose

Codex surface form exists to:

* read like plain English structured markup
* avoid confusion with programming languages
* be deterministic to parse and round-trip
* support automatic formatting (gofmt-like) without ambiguity

---

## 2. Fundamental Constructs (Normative)

Codex documents are composed of **Concepts**.

A Concept may include:

* zero or more **Traits** (name/value pairs)
* zero or more **child Concepts**
* optional **Content** (opaque narrative text)

A Concept is written using angle-bracket markers similar to (but not the same as) XML.

Codex documents may also include **Annotations**.

---

## 3. Annotations (Normative)

An Annotation line is written as:

```
[Annotation text.]
```

Rules:

* An Annotation line MUST begin with `[` and end with `]` on the same line.
* Annotation lines are not nested and have no escape mechanism.
* Annotation lines attach to the **next** Concept in the document.
* There MUST be no blank line between an Annotation and the Concept it annotates.

Annotations are not Values and are not interpreted by Codex.

---

## 4. Concept Markers (Normative)

### 4.1 Opening marker

An opening marker begins a Concept:

```
<ConceptName>
```

A ConceptName MUST follow the naming rules defined by the Codex Naming and Value Specification.

An opening marker MAY include Traits:

```
<ConceptName trait=value>
```

### 4.2 Closing marker

A closing marker ends a non-self-closing Concept:

```
</ConceptName>
```

The closing marker ConceptName MUST match the most recent unclosed ConceptName.

### 4.3 Self-closing marker

A self-closing marker represents a Concept with no child Concepts and no Content:

```
<ConceptName />
```

A self-closing marker MAY include Traits:

```
<ConceptName trait=value />
```

Notes:

* A self-closing Concept has no Content block.
* A self-closing Concept has no child Concepts.

---

## 5. Traits (Normative)

A Trait is written as:

```
traitName=value
```

Rules:

* Trait names MUST follow the naming rules defined by the Codex Naming and Value Specification.
* Trait names are schema-authorized; syntax does not imply validity.
* A Concept MAY declare zero or more Traits.
* Trait order is preserved as written.

Whitespace rules:

* No whitespace is permitted around `=`.

  * `name="Bob"` ✅
  * `name = "Bob"` ❌
* Traits within an opening marker are separated by one or more whitespace characters (space or line break).

---

## 6. Values (Normative)

A Value is a literal datum spelling.

Codex Values are **not expressions** and are **not evaluated**.

The full set of Value spellings is defined by the Codex Naming and Value Specification.
This surface-form specification defines only how Values appear inline in Traits and how they nest structurally.

Values MUST be written without leading or trailing whitespace.

---

## 7. Content Blocks (Normative)

Content is opaque narrative data.

A Concept carries Content by placing text lines between its opening and closing markers:

```cdx
<Title>
	Some text.
</Title>
```

Rules:

* Content is not interpreted by Codex.
* Content MUST be indented relative to its containing Concept.
* Content MAY include any characters, including markup and code.
* Content MAY include blank lines.

Content is not a Value spelling. Content is distinct from string Values.

---

## 8. Whitespace Significance (Normative)

Codex is whitespace-tolerant in most places, but requires certain whitespace constraints for deterministic parsing.

### 8.1 Insignificant whitespace

Outside of string Values, whitespace is generally insignificant except where it separates tokens.

Examples:

* Multiple spaces between Traits are treated as a separator.
* Line breaks between Traits are treated as a separator.

### 8.2 Significant structural boundaries

The following boundaries are structural:

* `<` begins a Concept marker
* `</` begins a closing marker
* `/>` ends a self-closing Concept marker
* `>` ends an opening Concept marker
* `[` begins an Annotation line (only when it is the first non-whitespace character on the line)
* `]` ends an Annotation line (same line)

### 8.3 Annotation line recognition

A line is an Annotation line if and only if its first non-whitespace character is `[` and the line ends with `]`.

---

## 9. Surface Grammar (Normative)

This section defines the structural grammar of Codex surface form. It is intentionally simple and non-expressive.

### 9.1 Document

A document consists of exactly one root Concept, preceded and interleaved by optional Annotation lines:

```
Document ::= (AnnotationLine | BlankLine)* RootConcept (BlankLine)*
```

### 9.2 Concept forms

A Concept is either:

* a non-self-closing Concept with children and/or Content, or
* a self-closing Concept

```
Concept ::= BlockConcept | SelfClosingConcept
```

### 9.3 Block Concept

```
BlockConcept ::=
	OpeningMarker
	(InterleavedContentOrChildren)*
	ClosingMarker
```

Where:

* `OpeningMarker` and `ClosingMarker` ConceptName MUST match.
* `InterleavedContentOrChildren` is any sequence of:

  * Annotation lines
  * child Concepts
  * content lines
  * blank lines

Codex does not interpret Content; tools may still need to detect child Concept markers.

### 9.4 Self-closing Concept

```
SelfClosingConcept ::= "<" ConceptName (Whitespace Trait)* Whitespace? "/>"
```

### 9.5 Opening marker

```
OpeningMarker ::= "<" ConceptName (Whitespace Trait)* Whitespace? ">"
```

### 9.6 Closing marker

```
ClosingMarker ::= "</" ConceptName Whitespace? ">"
```

### 9.7 Trait

```
Trait ::= TraitName "=" Value
```

TraitName and Value spellings are defined elsewhere (Naming and Value Specification), but Values may contain nested structures:

* lists: `[...]`
* temporals: `{...}`
* color functional forms: `name(...)`

A parser MUST treat bracketed/parenthesized/braced forms as balanced nested structures when parsing list items and other composite Values.

---

## 10. String Value Escaping (Normative)

A string Value is delimited by double quotation marks:

```
"..."
```

Strings are Values and may appear only where schema authorizes string Values.

### 10.1 Permitted characters

Within a string literal, the following are forbidden unless escaped:

* the double quote character: `"`
* the reverse solidus (backslash): `\`

The following are forbidden in all cases inside a string literal:

* a line break (U+000A LF)
* a carriage return (U+000D CR)

Notes:

* Codex string Values are **single-line** spellings.
* Multi-line text belongs in **Content**, not in string Values.

### 10.2 Escape sequences

Codex recognizes the following escape sequences inside string literals.

Required escapes:

* `\"` represents a literal `"` character
* `\\` represents a literal `\` character

Unicode escapes:

* `\uXXXX` where `X` is a hexadecimal digit (`0-9`, `a-f`, `A-F`) and exactly 4 digits are provided
* `\u{H...}` where `H...` is 1 or more hexadecimal digits (`0-9`, `a-f`, `A-F`)

Rules:

* Unicode escapes represent a single Unicode scalar value.
* Codex does not normalize or re-encode the result.

### 10.3 Forbidden escapes

No escape sequences other than those listed in §10.2 are permitted.

In particular, the following are forbidden:

* `\n`
* `\r`
* `\t`
* `\0`
* `\x..`
* `\` followed by any other character

A consumer MUST report a validation error upon encountering an unrecognized escape.

### 10.4 Canonical emission

When a consumer emits (formats) a string literal, it MUST ensure:

* any literal `"` is emitted as `\"`
* any literal `\` is emitted as `\\`
* no raw line breaks (LF/CR) are emitted inside the string literal

Consumers MUST NOT introduce or remove Unicode escapes as a normalization step.
If a string was authored using Unicode escapes, a consumer MAY preserve them as authored.

Examples:

Valid:

* `"firebrick"`
* `"He said \"hello\"."`
* `"C:\\Recipes\\Pasta"`
* `"Spaghetti \u{1F35D}"`

Invalid:

* `"line1
  line2"` (line break inside string)
* `"tab\tseparated"` (`\t` escape not permitted)
* `"bad \q escape"` (unknown escape)

---

**End of Codex Surface Form Specification**
