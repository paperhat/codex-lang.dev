Status: NORMATIVE
Lock State: UNLOCKED
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
* be mechanically canonicalizable
* support lossless round-tripping
* be unambiguous and mechanically parseable under the Codex language invariants
	(`spec/0.1/language/index.md`)

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

Indentation is a **canonical formatting requirement**.

In canonical surface form, indentation MUST use **tabs only**.

### 4.2 Indentation Depth

In canonical surface form, one tab character represents one level of nesting.

* Root Concept: no indentation (column 0)
* Direct children of root: one tab
* Their children: two tabs
* And so on

### 4.3 Formatter Enforcement

A conforming Codex formatter MUST normalize indentation before semantic
validation proceeds.

Indentation is part of the **canonical surface form**. Conforming tooling MUST
not treat author indentation as authoritative; it MUST be normalized by the
formatter prior to downstream processing.

If indentation cannot be normalized deterministically, the formatter MUST fail
with a FormattingError.

---

## 5. Blank Lines (Normative)

### 5.1 Between Sibling Concepts

Blank lines are a **canonical formatting requirement**.

In canonical surface form, there MUST be exactly **one blank line** between
sibling Concepts.

### 5.2 Elsewhere

In canonical surface form, blank lines are forbidden elsewhere in Children Mode:

* No blank lines between a Concept's opening marker and its first child
* No blank lines between a Concept's last child and its closing marker
* No blank lines within a Concept except between sibling children

### 5.3 Blank Line Definition

A blank line is a line containing **no characters** (empty after normalization).
Lines containing only whitespace are normalized to empty.

### 5.4 Exception: Annotations

Annotation blank-line rules are defined in § 8.

### 5.5 Exception: Content

Content is opaque to semantics and MAY contain blank lines.

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

## 7. Schema-Directed Content Mode (Normative)

The schema determines whether a Concept contains **child Concepts** or **Content**.

A tool performing **semantic validation** MUST consult the governing schema to
interpret a Concept’s body according to its declared content mode.

However, tools MAY perform **schema-less well-formed parsing** to check structural
readability and enable formatting/canonicalization without a governing schema.
In that mode, content-mode interpretation is deferred until semantic validation.

See the **Language Specification § Schema-First Parsing** for the architectural
rationale.

### 7.1 Parser Dispatch

When performing semantic validation and the parser encounters `<ConceptName ...>`:

1. Look up `ConceptName` in the active schema
2. If not found → the document is invalid under the schema
3. If found, retrieve the content mode from `ContentRules`
4. Interpret the body according to that mode
5. Match the closing marker `</ConceptName>`

This dispatch is deterministic. There is no ambiguity or backtracking.

### 7.2 Children Mode

When schema specifies a Concept contains children (`ForbidsContent`):

* The parser scans the body for child Concept markers and Annotations
* Only whitespace, Annotations, and child Concepts may appear in the body
* Any other non-whitespace text is a ParseError

### 7.3 Content Mode

When schema specifies a Concept contains Content (`AllowsContent`):

* The parser captures all text between the opening and closing markers as Content
* Content is **opaque to schema semantics** (it is not interpreted as Concepts,
	Traits, Values, or Annotations)
* Content is still read token-by-token and is subject to **content escaping**
	rules (see § 12)
* Because `<` is not permitted unescaped inside Content, the closing marker
	`</ConceptName>` is always unambiguous
* Content is preserved exactly (after required newline normalization and escape
	decoding)

### 7.4 Empty Mode

When schema specifies a Concept must be empty:

* The Concept MUST use self-closing form (`<Concept ... />`)
* Block form with any body content is a ParseError

### 7.5 Mutual Exclusivity

A Concept MUST NOT contain both child Concepts and Content.

This constraint is enforced structurally by the schema definition and parser
dispatch. A schema author declares one mode; the parser enforces it.

---

## 8. Annotations (Normative)

Annotations are **editorial metadata**, distinct from Values and Content.
Codex preserves them without interpretation.

### 8.1 Annotation Form

Codex defines two surface forms for annotations.

#### 8.1.1 Inline Annotation

An **inline annotation** uses `[` and `]` on the same line:

```cdx
[Short note]
<Thing />
```

Inline annotations are intended for short notes, `GROUP`/`END` markers, and
attached annotations.

#### 8.1.2 Block Annotation

A **block annotation** uses `[` and `]` on their own lines:

```cdx
[
	A longer note.
	It may include lists:

	- red
	- green
	- blue
]
```

Block annotations are intended for longer editorial notes.

Annotations:

* MAY appear at top-level or within children-mode bodies
* MUST NOT appear inside Concept markers
* MAY contain arbitrary text (including blank lines)
* MAY attach to a Concept (see § 8.6)
* MAY be standalone (see § 8.6)

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
* For an inline annotation, the closing `]` MUST appear on the same line
* For a block annotation:
	* the line containing `[` MUST contain no other non-whitespace characters
	* the closing `]` MUST appear as the first non-whitespace character on its
		own line and the line MUST contain no other non-whitespace characters

Whether an annotation attaches to a Concept (or is standalone) is determined by
the rules in § 8.6.

### 8.3 Escaping

Within an Annotation:

* `\]` → literal `]`
* `\\` → literal `\`

No other escape sequences are defined.

### 8.4 Canonical Form (Normative)

Canonicalization of annotations is **deterministic** and depends on the
annotation form.

#### 8.4.1 Inline Annotation Canonicalization

Inline annotations are canonicalized as follows:

* Leading and trailing whitespace inside the brackets is trimmed
* Internal runs of whitespace (spaces, tabs, newlines) are collapsed to a single space
* Escaped characters remain escaped

Canonical rendering uses no padding spaces just inside the brackets:

* `[text]` (not `[ text ]`)

#### 8.4.2 Block Annotation Canonicalization

Block annotations preserve their internal line structure.

Canonicalization of a block annotation MUST:

* normalize line endings to LF
* preserve the block annotation content according to its directive (see § 8.5)

For a block annotation with no directive (verbatim note), canonicalization MUST:

* remove trailing whitespace on each content line
* normalize indentation so that the content lines are indented exactly one tab
	deeper than the `[` / `]` lines

Block annotations MAY declare a directive (see § 8.5) that controls additional
canonicalization.

### 8.5 Block Annotation Directives (Normative)

In a **block annotation**, the first non-blank content line MAY be a directive
line.

The directive line MUST be exactly one of:

* `FLOW:`
* `CODE:`
* `MD:`

If present, the directive line MUST be preserved in canonical output.

Directive behavior:

* `CODE:` — preserve the block annotation bytes verbatim (except for global
	newline normalization). Tools MUST NOT reindent, trim, strip trailing
	whitespace, wrap, or interpret escapes within the block annotation.
* `MD:` — preserve the block annotation bytes verbatim (except for global
	newline normalization). Tools MUST NOT reindent, trim, strip trailing
	whitespace, wrap, or interpret escapes within the block annotation.
* `FLOW:` — treat the remaining content as flow text; tools MAY apply
	deterministic wrapping to a fixed width without changing the flow-text value

If no directive is present, the block annotation is treated as a verbatim note
and MUST be canonicalized as described in § 8.4.2.

For `FLOW:` blocks, the flow-text value is the remaining content with:

* leading and trailing whitespace trimmed
* internal runs of whitespace (spaces, tabs, newlines) collapsed to single spaces
* escapes interpreted per § 8.3

Canonical rendering for `FLOW:` blocks MUST:

* split the remaining content into paragraphs separated by one or more blank
	lines
* for each paragraph, wrap words to lines of at most 80 Unicode scalar
	characters using greedy packing (a word that would exceed 80 starts a new
	line)
* indent each wrapped line exactly one tab deeper than the `[` / `]` lines
* separate paragraphs by exactly one blank line

### 8.6 Annotation Kinds (Normative)

Codex defines three kinds of annotations:

1. **Attached annotations** — attach to a single Concept
2. **Grouping annotations** — `GROUP` / `END` markers that bracket a region
3. **General annotations** — standalone annotations (inline or block)

#### 8.6.1 Attached Annotations

An annotation is an **attached annotation** if and only if:

* it is an **inline annotation**, and
* it is not a grouping annotation, and
* it is immediately followed (on the next line) by a Concept opening marker, and
* there is **no blank line** between the annotation and that marker

Multiple attached annotations MAY stack; an attached-annotation stack attaches
to the next Concept opening marker.

Attached annotations MUST NOT have blank lines separating them from each other.
If a blank line appears, the annotations are not attached.

#### 8.6.2 Grouping Annotations

A grouping annotation is a **single-line** annotation whose **canonicalized**
annotation text matches one of the following forms:

* `GROUP: <label>`
* `END: <label>`

`<label>` is any non-empty string after trimming.

Whitespace between `[` and `GROUP` / `END`, and between the label and `]`, is
permitted. Grouping recognition is performed after applying the annotation
canonicalization rules in § 8.4.1 (trim + internal whitespace collapse).

Grouping annotations:

* do not attach to Concepts
* define a purely editorial grouping region
* MAY nest

Label comparison uses the canonical label form (trimmed, with internal
whitespace collapsed to single spaces).

#### 8.6.3 General Annotations

An annotation is a **general annotation** if and only if:

* it is surrounded by **exactly one blank line above and exactly one blank line
	below**, where file boundaries count as blank-line boundaries, and
* it is not a grouping annotation

General annotations MAY be inline or block.

General annotations do not attach to Concepts.

### 8.7 Group Nesting and Matching (Normative)

Grouping annotations form a properly nested stack.

* `[GROUP: X]` pushes label `X`
* `[END: X]` MUST match the most recent unmatched `[GROUP: X]`

If an `END` label does not match the most recent open group label, or if an
`END` appears with no open group, the document is invalid (ParseError).

### 8.8 Canonical Blank Line Requirements (Normative)

In canonical surface form:

* **Attached annotations** appear directly above the annotated Concept opening
  marker with no blank line
* **Grouping annotations** MUST be surrounded by exactly one blank line above
  and below (file boundaries count as blank-line boundaries)
* **General annotations** MUST be surrounded by exactly one blank line above and
  below (file boundaries count as blank-line boundaries)

Any annotation that is neither an attached annotation, a grouping annotation,
nor a general annotation is invalid.

---

## 9. Concept Markers (Normative)

### 9.1 Opening Marker

```
<ConceptName>
<ConceptName trait=value>
```

Rules:

* `ConceptName` MUST follow the **Naming and Value Specification**
	(`spec/0.1/naming-and-values/index.md`)
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
* Trait names MUST follow the **Naming and Value Specification**
	(`spec/0.1/naming-and-values/index.md`)

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

Content exists for Concepts that the schema designates as content-mode via
`AllowsContent` in `ContentRules`.

### 12.1 Example

```cdx
<Description>
	This is content. It is not parsed by Codex.
	Angle brackets like \<this> are literal text.
	So are [square brackets] and other characters.
</Description>
```

### 12.2 Rules

* Content is **not** a Value
* Content is **not** interpreted as Codex structure or Values
* In canonical surface form, Content lines are indented one level relative to
	their Concept (the formatter normalizes indentation)
* Content MAY contain any characters, but MUST escape `<` and `\` (see § 12.4)
* Content MAY contain blank lines
* Content MAY span multiple lines

### 12.3 Content Termination

The parser identifies the end of content by scanning for the closing marker
that matches the opening Concept name: `</ConceptName>`.

Because `<` is not permitted unescaped inside Content, `</ConceptName>` is
unambiguous.

### 12.4 Content Escaping (Normative)

Within Content:

* `\<` represents a literal `<`
* `\\` represents a literal `\`

All other uses of `\` are invalid (ParseError).

A raw `<` character MUST NOT appear in Content.
A raw `\` character MUST NOT appear in Content.

Example of content containing markup-like text:

```cdx
<Tutorial>
	<Section title="Writing Descriptions">
		To write a description, use the Description Concept:

		\<Description>Your text here.\</Description>

		The text inside is opaque content.
	</Section>
</Tutorial>
```

In this example:
* `<Section>` is a child Concept (Section is children-mode per schema)
* The lines inside Section including `\<Description>Your text here.\</Description>`
  are literal content text (if Section allows content per schema), or if Section
  is children-mode, then the inner Description is a nested Concept

The schema determines interpretation.

### 12.5 Indentation Normalization

Content is stored and processed without its canonical leading indentation.
In canonical form, Content lines are indented one level relative to their
Concept; the logical Content value removes that indentation based on structural
nesting depth.

Given:

```cdx
<Outer>
	<Inner>
		Line one.
		Line two.
	</Inner>
</Outer>
```

If `Inner` is content-mode, the content is:

```
Line one.
Line two.
```

The two leading tabs (one for Outer, one for Inner) are stripped.

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

## 18. Canonicalization (Normative)

Canonical form requirements and canonicalization rules are defined by the
**Formatting and Canonicalization Specification**
(`spec/0.1/formatting-and-canonicalization/index.md`).

This specification defines the surface structure, token spellings, and encoding
rules that canonicalization operates over.

---

## 19. Prohibited Behaviors (Normative)

Codex tools MUST NOT:

* Infer missing structure
* Silently rewrite Content
* Silently correct surface errors
* Accept multiple canonical forms
* Violate the Codex language invariants (e.g., use heuristics to disambiguate;
	see `spec/0.1/language/index.md`)

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
* Content is opaque to semantics; Content escapes `<` as `\<` and `\\` as `\`
* Annotations are `[...]`, multiline, whitespace-collapsed
* Empty blocks `<X></X>` are invalid; use `<X />`
* Strings `"..."`, characters `'...'`, backtick strings `` `...` ``
* 1-2 Traits single line, 3+ Traits multiline
* Formatter normalizes before parsing
* Canonicalization is mechanical or fails

---

**End of Codex Surface Form Specification v0.1**
