Status: NORMATIVE
Lock State: LOCKED
Version: 0.1
Editor: Charles F. Munat

# Codex Surface Form Specification — Version 0.1

This specification defines the **surface form** of Codex documents: the concrete
spellings authors write and tools parse.

It governs:

* File encoding and line endings
* Indentation and blank lines
* Concept markers (`<...>`, `</...>`, `/>`)
* Traits and their Values
* Annotations
* Content blocks (opaque narrative text)
* String and character literal escaping
* Structural requirements necessary for canonicalization

This specification is **core language**.
It defines syntax only. Semantics are schema responsibilities.

---

## 1. Purpose

The Codex surface form exists to:

* read as structured, precise English
* be deterministic to parse
* be mechanically canonicalizable
* support lossless round-tripping
* avoid heuristic or best-effort interpretation

This specification defines **what is parseable Codex**.

---

## 2. File Encoding (Normative)

Codex documents MUST be encoded in **UTF-8** or **UTF-16**.

### 2.1 Default Encoding

UTF-8 is the default encoding. UTF-8 encoded files MUST NOT include a BOM.

### 2.2 UTF-16 Encoding

UTF-16 encoding is indicated by a Byte Order Mark (BOM) at the start of the file:

* `FE FF` (2 bytes) → UTF-16 Big Endian
* `FF FE` (2 bytes) → UTF-16 Little Endian

### 2.3 Detection Rule

* File starts with `FE FF` → UTF-16 BE
* File starts with `FF FE` → UTF-16 LE
* Otherwise → UTF-8 (no BOM)

No other encodings are supported.

---

## 3. Line Endings (Normative)

### 3.1 Canonical Form

The canonical line ending is **LF** (`\n`, U+000A).

### 3.2 Input Normalization

CRLF (`\r\n`) sequences MUST be normalized to LF on input.

Bare CR (`\r`) is forbidden and MUST cause a parse error.

---

## 4. Indentation (Normative)

### 4.1 Indentation Character

Indentation MUST use **tabs only**. Spaces are forbidden for indentation.

### 4.2 Indentation Depth

One tab character represents one level of nesting.

* Root Concept: no indentation (column 0)
* Direct children of root: one tab
* Their children: two tabs
* And so on

### 4.3 Formatter Enforcement

A conforming formatter MUST normalize indentation before parsing.
Incorrect indentation is a formatting error.

---

## 5. Blank Lines (Normative)

### 5.1 Between Sibling Concepts

There MUST be exactly **one blank line** between sibling Concepts.

### 5.2 Elsewhere

Blank lines are forbidden elsewhere in Children Mode:

* No blank lines between a Concept's opening marker and its first child
* No blank lines between a Concept's last child and its closing marker
* No blank lines within a Concept except between sibling children

### 5.3 Blank Line Definition

A blank line is a line containing **no characters** (empty after normalization).
Lines containing only whitespace are normalized to empty.

### 5.4 Exception: Annotations

There MUST NOT be a blank line between an Annotation and the Concept it annotates.
Annotations MAY contain blank lines internally.

### 5.5 Exception: Content

Content is opaque and MAY contain blank lines.

Blank line restrictions in § 5.2 apply only to Children Mode structure.
Content is not parsed or interpreted by Codex.

---

## 6. Fundamental Constructs (Normative)

Codex documents are composed of **Concepts**.

A Concept MAY include:

* zero or more **Traits**
* zero or more **child Concepts** OR **Content** (never both)
* optional **Annotations**

---

## 7. Schema-Determined Content Mode (Normative)

The schema determines whether a Concept contains **child Concepts** or **Content**.

### 7.1 Children Mode

When schema specifies a Concept contains children:

* Only whitespace, `<` (child Concept), or `[` (Annotation) may appear inside
* Any other content is a SchemaError (content mode is schema-determined, not parser-determined)

### 7.2 Content Mode

When schema specifies a Concept contains Content:

* Everything between the opening and closing markers is opaque text
* Content is opaque to Codex
* Content may contain anything: prose, code, markup, even literal `<` or `[` characters
* Content is preserved exactly (after indentation normalization)

### 7.3 Mutual Exclusivity

A Concept MUST NOT contain both child Concepts and Content.
This is enforced by schema, not by the parser.

---

## 8. Annotations (Normative)

Annotations are **editorial metadata**, distinct from Values and Content.
Codex preserves them without interpretation.

### 8.1 Annotation Form

An Annotation consists of all text from an opening `[` to a matching closing `]`.

Annotations:

* MAY span multiple lines
* MAY contain arbitrary text (including blank lines)
* MUST attach to the **next Concept**
* MAY stack (multiple Annotations may attach to the same Concept)
* MUST NOT be nested
* MUST NOT appear inside Concept markers

Example (single annotation):

```cdx
[This is a
multiline annotation.]
<Recipe id=~pasta>
```

Example (stacked annotations):

```cdx
[First annotation]
[Second annotation]
<Recipe id=~pasta>
```

Both annotations attach to the Recipe Concept.

### 8.2 Structural Rules

* The opening `[` MUST be the first non-whitespace character on its line
* The closing `]` MUST terminate the annotation
* There MUST NOT be a blank line between an Annotation and the Concept it annotates

### 8.3 Escaping

Within an Annotation:

* `\]` → literal `]`
* `\\` → literal `\`

No other escape sequences are defined.

### 8.4 Canonical Form

For canonical surface form:

* Leading and trailing whitespace is trimmed
* Internal runs of whitespace (spaces, tabs, newlines) are collapsed to a single space
* Escaped characters remain escaped

---

## 9. Concept Markers (Normative)

### 9.1 Opening Marker

```
<ConceptName>
<ConceptName trait=value>
```

Rules:

* `ConceptName` MUST be PascalCase
* Traits MAY appear inline
* Trait order is preserved

### 9.2 Closing Marker

```
</ConceptName>
```

Rules:

* MUST match the most recent unclosed Concept
* MUST be on its own line (after indentation)
* No additional content is permitted on the line

### 9.3 Self-Closing Marker

```
<ConceptName />
<ConceptName trait=value />
```

Rules:

* Represents a Concept with no Content and no children
* MAY include Traits
* Indicates **deliberate emptiness**

### 9.4 Empty Block Concepts Are Invalid

The form `<ConceptName></ConceptName>` (opening and closing with nothing between) is **invalid**.

Authors MUST use either:

* Self-closing form `<ConceptName />` for deliberately empty Concepts
* Block form with Content or children

This prevents incomplete templates from passing validation.

---

## 10. Traits (Normative)

A Trait is written as:

```
traitName=value
```

Rules:

* No whitespace is permitted around `=`
* Traits are separated by whitespace (space or newline)
* Trait order is preserved
* Trait names MUST be camelCase

### 10.1 Trait Formatting (Canonical)

The canonical form for Traits depends on count:

**1-2 Traits**: Single line

```cdx
<Recipe id=~pasta title="Pasta" />
```

**3 or more Traits**: One Trait per line, indented

```cdx
<Recipe
	id=~pasta
	title="Pasta"
	author=~chas
	difficulty=$Medium
/>
```

When multiline, Traits are indented one level deeper than the Concept marker.

---

## 11. Values (Normative)

Values are literal spellings defined by the **Naming and Value Specification**.

Rules:

* No leading or trailing whitespace (except inside string/character literals)
* Parsed mechanically
* Not evaluated or normalized by Codex

### 11.1 Value Termination

Values terminate at:

* Unbalanced whitespace (space, tab, newline)
* `>` or `/>` (end of Concept marker)

Balanced delimiters (`[]`, `{}`, `()`, `''`, `""`) MUST be respected during parsing.

---

## 12. Content Blocks (Normative)

Content is opaque narrative text between opening and closing Concept markers.

Example:

```cdx
<Description>
	This is text.
	It is opaque to Codex.
</Description>
```

### 12.1 Rules

* Content is **not** a Value
* Content is **not** parsed by Codex
* Content MUST be indented one level relative to its Concept
* Content MAY contain any characters

### 12.2 Content Escaping

If Content contains a literal closing marker that matches the current Concept, it MUST be escaped.

Escape `</` as `\</` to prevent the parser from closing the block prematurely.

Example:

```cdx
<Description>
	Use the description concept like this:
	<Description>Some text here.\</Description>
</Description>
```

Rules:

* `\</` → literal `</` (not a closing marker)
* `\\` → literal `\`

This escaping is only needed when the literal `</ConceptName>` matches the current Concept's closing marker.

---

## 13. String Literals (Normative)

String Values are written with double quotes:

```
"..."
```

### 13.1 Rules

* Single-line only
* Delimited by `"`

### 13.2 Escape Sequences

* `\"` → `"`
* `\\` → `\`
* `\n` → newline (U+000A)
* `\r` → carriage return (U+000D)
* `\t` → tab (U+0009)
* `\uXXXX` → Unicode scalar (4 hex digits)
* `\u{H...}` → Unicode scalar (1-6 hex digits)

All other escape sequences are forbidden.
Raw line breaks inside strings are forbidden.

---

## 14. Backtick Strings (Normative)

Backtick strings allow multiline text with whitespace collapse.

```
`...`
```

### 14.1 Rules

* Delimited by single backtick
* MAY span multiple lines
* Whitespace (spaces, tabs, newlines) is collapsed to single spaces
* Leading and trailing whitespace is trimmed
* Result is a single-line string

### 14.2 Escape Sequences

* `` \` `` → literal backtick
* `\\` → literal `\`

### 14.3 Example

```cdx
<Article summary=`This is a long summary
	that spans multiple lines in the source
	but collapses to a single line.` />
```

Becomes equivalent to:

```cdx
<Article summary="This is a long summary that spans multiple lines in the source but collapses to a single line." />
```

### 14.4 Usage Guidance

Backtick strings should be used sparingly. If a Trait value requires significant text,
consider whether it should be Content instead.

---

## 15. Character Literals (Normative)

Character Values are written with single quotes:

```
'X'
```

### 15.1 Rules

* MUST contain exactly one character (or escape sequence)
* Delimited by `'`
* Distinct from string values

### 15.2 Escape Sequences

* `\'` → `'`
* `\\` → `\`
* `\n` → newline (U+000A)
* `\r` → carriage return (U+000D)
* `\t` → tab (U+0009)
* `\uXXXX` → Unicode scalar (4 hex digits)
* `\u{H...}` → Unicode scalar (1-6 hex digits)

---

## 16. Whitespace Significance (Normative)

### 16.1 Insignificant Whitespace

* Multiple spaces between tokens on a line are equivalent to one space
* Line breaks between Traits act as separators (equivalent to space)

### 16.2 Significant Whitespace

* Indentation (tabs at start of line)
* Blank lines (exactly one between siblings)
* Whitespace inside string/character literals

### 16.3 Significant Boundaries

The following delimiters are structurally significant:

* `<`, `</`, `>`, `/>`
* `[` as the first non-whitespace character of a line (Annotation start)
* `]` that closes an Annotation
* `"` (string delimiter)
* `'` (character delimiter)
* `` ` `` (backtick string delimiter)

---

## 17. Structural Grammar (Normative)

### 17.1 Document

```
Document ::= BlankLine* Annotation* RootConcept
```

A document MUST contain exactly one root Concept.
Trailing blank lines are normalized away.

### 17.2 Concept Forms

```
Concept ::= BlockConcept | SelfClosingConcept
```

### 17.3 Block Concept (Children Mode)

```
BlockConcept ::=
	OpeningMarker
	Annotation* ChildConcept (BlankLine Annotation* ChildConcept)*
	ClosingMarker
```

### 17.4 Block Concept (Content Mode)

```
BlockConcept ::=
	OpeningMarker
	ContentLines
	ClosingMarker
```

### 17.5 Self-Closing Concept

```
SelfClosingConcept ::= '<' ConceptName Traits? Whitespace? '/>'
```

---

## 18. Canonical Surface Requirements (Normative)

A valid Codex document MUST be transformable into **exactly one canonical surface form**.

### 18.1 Canonical Requirements

* UTF-8 encoding (unless UTF-16 required)
* LF line endings
* Tab indentation, one per level
* Exactly one blank line between sibling Concepts
* No trailing whitespace on lines
* No trailing blank lines at end of file
* Traits: 1-2 on single line, 3+ on separate lines
* Annotations: whitespace collapsed
* Strings: minimal escaping

### 18.2 Formatter Requirement

A conforming Codex formatter MUST:

* Normalize encoding
* Normalize line endings
* Normalize indentation
* Normalize blank lines
* Normalize Trait layout
* Normalize Annotation whitespace

The formatter runs before the parser. Invalid formatting is an error.

---

## 19. Prohibited Behaviors (Normative)

Codex tools MUST NOT:

* Infer missing structure
* Silently rewrite Content
* Silently correct surface errors
* Accept multiple canonical forms
* Use heuristics to disambiguate

---

## 20. Non-Goals

This specification does **not**:

* Define schemas or validation rules
* Define inline text markup
* Define semantics beyond parsing
* Define rendering or execution semantics

---

## 21. Summary

* UTF-8 default, UTF-16 via BOM
* LF line endings (CRLF normalized)
* Tabs only for indentation, one per level
* Exactly one blank line between siblings
* Concepts contain children OR content, never both (schema-defined)
* Content is opaque; `\</` escapes closing markers
* Annotations are `[...]`, multiline, whitespace-collapsed
* Empty blocks `<X></X>` are invalid; use `<X />`
* Strings `"..."`, characters `'...'`, backtick strings `` `...` ``
* 1-2 Traits single line, 3+ Traits multiline
* Formatter normalizes before parsing
* Canonicalization is mechanical or fails

---

**End of Codex Surface Form Specification v0.1**
