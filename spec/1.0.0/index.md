Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 1.0.0 BETA  
Editor: Charles F. Munat

# Codex Language Specification — Version 1.0.0 BETA

This document is the authoritative language specification for Codex 1.0.0 BETA.

All normative requirements for Codex 1.0.0 MUST appear exactly once in this document.

---

## 1. Front Matter

### 1.1 Scope

Codex 1.0.0 defines the Codex language.

This specification governs:

- the core language model (Concepts, Traits, Values, Content, and Entities)
- naming and identifier constraints
- literal value spellings
- surface form syntax and structural rules for `.cdx` documents
- formatting and canonicalization requirements
- schema-first parsing architecture
- schema definition, schema loading/bootstrapping, and schema versioning rules
- reference trait semantics
- validation error classification

Codex 1.0.0 does not define runtime behavior.

---

### 1.2 Non-Goals

Codex 1.0.0 does not define:

- a programming, scripting, or templating language
- an execution model, runtime, or pipeline orchestration
- storage, querying, indexing, inference, or rendering behavior
- identifier base scoping or base resolution mechanisms
- schema distribution, registry protocols, or migration mechanisms

Those concerns belong to consuming systems and tooling.

### 1.3 Normativity and Precedence

This document uses the capitalized keywords **MUST**, **MUST NOT**, and **MAY**
to indicate requirements.

Any statement that uses **MUST**, **MUST NOT**, or **MAY** is normative.

**MAY** defines an explicitly optional capability. If an implementation supports
that capability, it MUST implement it exactly as specified.

Unless explicitly stated otherwise:

- Text labeled **Normative** defines required behavior.
- Text labeled **Informative** is explanatory and does not define requirements.
- Examples are illustrative and non-normative.

All statements that do not use **MUST**, **MUST NOT**, or **MAY** are
informative unless explicitly labeled **Normative**.

If two statements in this document conflict, a conforming implementation MUST
follow this precedence order:

1. Statements explicitly marked **Normative**
2. Unmarked requirement statements using MUST/MUST NOT/MAY
3. Appendix A.1 **EBNF (Normative)** for syntactic precision (what parses)
4. Appendix A.2 **PEG (Informative)** and all other informative material

Where Appendix A.1 (EBNF) defines syntax and the prose defines semantic intent:

- For syntactic recognition (what sequences of characters are valid tokens): EBNF prevails.
- For semantic meaning and processing obligations: prose prevails.

---

## 2. Language Invariants

### 2.1 Declarative and Closed-World Model

Codex is a declarative language.

A conforming implementation MUST treat the meaning of a Codex document as the result of its explicit declarations only.

Codex has closed-world semantics:

- Meaning MUST be explicitly declared.
- An implementation MUST NOT infer additional meaning from omission, shape, ordering, or other non-specified cues.
- An implementation MUST NOT assume defaults unless they are explicitly defined by this specification or by the governing schema.

If something is not declared, it MUST be treated as not present.

### 2.2 Determinism and Explainability

Given the same inputs (document bytes, governing schema, and any other required external inputs explicitly defined by this specification), a conforming implementation MUST produce the same results.

In particular:

- Parsing MUST be deterministic.
- Validation MUST be deterministic.
- Canonicalization MUST be deterministic.

Non-deterministic or heuristic behavior is forbidden.

For any validation or canonicalization result, an implementation MUST be able to attribute the result to:

- the rule applied, and
- the specific declaration(s) or input construct(s) that caused the result.

### 2.3 Separation of Responsibility

Codex enforces separation between:

- language and surface form rules,
- schema-defined meaning and constraints,
- formatting/canonicalization,
- semantic validation, and
- consuming-system behavior (storage, querying, inference, rendering, execution).

Accordingly:

- Parsing MUST determine only the syntactic structure of the document.
- Formatting and canonicalization MUST be mechanical and MUST NOT perform schema evaluation.
- Semantic validation MUST evaluate schema rules (including content-mode interpretation, constraints, cardinality, identity, and references) and MUST NOT be performed implicitly during parsing.

Codex and Codex-conforming tools MUST NOT define, assume, or require any particular storage backend, inference system, rendering model, or execution semantics.

### 2.4 Target Agnosticism

Codex is target-agnostic.

A Codex document MAY be transformed into other representations.

No Codex construct, and no Codex-conforming tool behavior defined by this specification, MUST assume a specific target, runtime, storage backend, or rendering model.

---

## 3. Core Model

### 3.1 Concept

A Concept is a named declarative construct and the primary structural unit of a Codex document.

A Concept instance MUST have exactly one Concept name.

A Concept instance MAY declare zero or more Traits.

A Concept instance MAY contain either:

- zero or more child Concepts, or
- Content,

but it MUST NOT contain both child Concepts and Content.

### 3.2 Trait

A Trait binds a Trait name to a Value.

A Trait instance MUST be declared on exactly one containing Concept instance.

A Trait instance MUST NOT have independent identity.

Trait meaning and permissibility MUST be defined by the governing schema.

### 3.3 Value

A Value is a literal datum.

A Value instance MUST be expressed using one of the literal spellings defined by this specification.

A Value instance MUST be treated as declarative and immutable.

Codex-conforming tools MUST parse Value spellings mechanically and MUST NOT evaluate Values as expressions.

The meaning of a Value beyond its literal form MUST be defined by the governing schema or consuming system.

### 3.4 Content

Content is opaque narrative text carried by a Concept.

Content MUST NOT be treated as a Value.

Content MUST NOT be typed, evaluated, or interpreted as Concepts, Traits, Values, or Annotations.

Content MUST be preserved through Codex-conforming processing, subject only to the surface-form normalization and canonicalization rules defined by this specification.

### 3.5 Entity

An Entity is a Concept instance with explicit identity.

A Concept instance is an Entity if and only if:

- the governing schema permits or requires identity for that Concept via its `entityEligibility` rule, and
- the Concept instance declares an `id` Trait.

If the governing schema declares `$MustBeEntity` for a Concept, each instance of that Concept MUST declare an `id` Trait.

If the governing schema declares `$MustNotBeEntity` for a Concept, each instance of that Concept MUST NOT declare an `id` Trait.

Codex-conforming tools MUST NOT treat a Concept instance as an Entity unless it declares an `id` Trait.

Codex-conforming formatting and canonicalization MUST NOT synthesize identity by adding an `id` Trait or inventing an identifier value.

### 3.6 Marker

A Marker is a syntactic delimiter for Concept instances in the surface form.

Markers MUST be one of:

- an opening marker,
- a closing marker, or
- a self-closing marker.

Markers MUST delimit Concept structure and nesting.

Each closing marker MUST match the most recent unclosed opening marker.

A self-closing marker MUST represent a Concept with no children and no Content.

### 3.7 Annotation

An Annotation is author-supplied editorial metadata.

Annotations MUST NOT affect parsing, validation outcomes, or domain semantics.

Annotations MUST be preserved through Codex-conforming processing, subject only
to the surface-form normalization and canonicalization rules defined by this
specification.

---

## 4. Naming Rules

### 4.1 Casing

For the purposes of Codex, this specification defines:

- PascalCase: a name composed only of ASCII letters and digits, with no separators; the first character MUST be an ASCII uppercase letter; each subsequent ASCII letter that begins a new word segment MUST be an ASCII uppercase letter.
- camelCase: a name composed only of ASCII letters and digits, with no separators; the first character MUST be an ASCII lowercase letter; each subsequent ASCII letter that begins a new word segment MUST be an ASCII uppercase letter.

Concept names MUST use PascalCase.

Trait names MUST use camelCase.

No other casing is permitted.

### 4.2 Initialisms and Acronyms

For the purposes of Codex, this specification defines:

- Abbreviation: a shortened form of a word or phrase.
- Initialism: an abbreviation formed from the initial letters of words in a phrase.
- Acronym: an initialism designed to be pronounceable as a word.

Initialisms and acronyms are permitted in names.

An initialism or acronym MUST be written as an ordinary word segment: only the first letter of the segment is uppercase and all remaining letters in the segment are lowercase.

A name MUST NOT contain a run of two or more uppercase letters.

### 4.3 General Abbreviations

General abbreviations are forbidden in Codex names.

Names MUST NOT contain periods.

A schema MAY whitelist specific general abbreviations for its domain. Such
exceptions apply only within that schema.

---

## 5. Value Literal Catalog

### 5.1 String Values

A String Value is a sequence of Unicode scalar values.

In the Surface Form, String Values are spelled as string literals and backtick strings.

### 5.2 Backtick Strings

A Backtick String is a surface-form spelling of a String Value.

Backtick strings are intended for multiline authoring convenience.

After interpreting the Backtick String's escape sequences, the resulting character sequence MUST be transformed into the resulting String Value by applying the following whitespace normalization:

- Each maximal run of whitespace characters (spaces, tabs, and line breaks) MUST be replaced with a single U+0020 SPACE.
- Leading and trailing U+0020 SPACE MUST be removed.

The resulting String Value MUST be single-line.

### 5.3 Boolean Values

A Boolean Value is one of two values: true or false.

In the Surface Form, Boolean Values MUST be spelled as the tokens `true` and `false`.

No other spellings are permitted.

### 5.4 Numeric Values

Numeric Values are declarative spellings.

Codex performs no arithmetic and no numeric normalization. Numeric spellings MUST be preserved exactly.

In the Surface Form, Numeric Values MUST be spelled using the numeric literal grammar defined by this specification.

Numeric Values include:

- integers
- decimals
- scientific notation
- infinities
- fractions
- imaginary numbers
- complex numbers
- precision-significant numbers

The meaning of a Numeric Value beyond its literal spelling MUST be defined by the governing schema or consuming system.

#### 5.4.1 Precision-Significant Numbers

Precision-significant numbers are marked with a `p` suffix.

The precision (number of significant decimal places) MUST be determined by one of the following mechanisms:

- Inferred precision: the count of decimal places in the literal spelling, including trailing zeros.
- Explicit precision: an integer following the `p` suffix.

The `p` suffix indicates that precision is semantically significant.

Consuming systems MUST preserve the declared precision.

### 5.5 Enumerated Token Values

An Enumerated Token Value is a Value drawn from a schema-defined closed set.

In the Surface Form, Enumerated Token Values MUST be spelled with a leading `$` sigil.

Enumerated Token Values MUST NOT be treated as String Values.

Enumerated Token Values MUST NOT be evaluated.

### 5.6 Temporal Values

In the Surface Form, Temporal Values MUST be spelled using `{...}`.

Temporal Values MUST NOT be treated as Enumerated Token Values, even when the braced payload is a reserved literal such as `now` or `today`.

### 5.7 Color Values

Color Values are first-class values, not String Values.

Codex-conforming tools MUST NOT validate, normalize, or convert Color Values.

In the Surface Form, Color Values MUST be spelled using one of the following literal forms:

- hexadecimal colors (`#RGB`, `#RGBA`, `#RRGGBB`, `#RRGGBBAA`)
- `rgb(...)` (with legacy alias `rgba(...)`)
- `hsl(...)` (with legacy alias `hsla(...)`)
- `hwb(...)`
- `lab(...)`
- `lch(...)`
- `oklab(...)`
- `oklch(...)`
- `color(...)`
- `color-mix(...)`
- relative colors using `from <color>` within a color function
- `device-cmyk(...)`
- named colors using a leading `&` sigil

Hex digits in hexadecimal colors are case-insensitive.

#### 5.7.1 Named Color Values

In the Surface Form, a Named Color Value MUST be spelled as `&` followed immediately by a color name.

The color name MUST consist only of ASCII lowercase letters (`a` through `z`).

The color name MUST be a CSS named color keyword as defined by the CSS Color Module specifications.

Appendix B provides an informative list.

The following context-dependent CSS keywords are included as named colors:

- `transparent`
- `currentcolor`

In `color(...)`, the color space token MUST be one of:

- `srgb`
- `srgb-linear`
- `display-p3`
- `a98-rgb`
- `prophoto-rgb`
- `rec2020`
- `xyz`
- `xyz-d50`
- `xyz-d65`

### 5.8 UUID Values

A UUID Value is a 36-character unquoted token with the form:

`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

where each `x` is a hexadecimal digit.

A UUID Value MUST NOT be a String Value.

A UUID Value MUST NOT include braces, prefixes, or other delimiters.

Hyphens MUST appear at positions 9, 14, 19, and 24.

Hexadecimal digits in UUID Values are case-insensitive.

No UUID version is mandated.

### 5.9 IRI Reference Values

An IRI Reference Value is an unquoted token representing identity or reference.

An IRI Reference Value MUST contain a `:` character separating the scheme from the remainder.

In the Surface Form, IRI Reference Values MUST be spelled using the IRI reference grammar defined by this specification.

IRI Reference Values MUST permit non-ASCII Unicode characters directly (RFC 3987 IRI-reference).

IRI Reference Values MUST permit percent-encoding (RFC 3987): https://www.rfc-editor.org/rfc/rfc3987.

IRI Reference Values MUST NOT contain Unicode whitespace characters.

IRI Reference Values MUST NOT contain Unicode control characters.

IRI Reference Values MUST NOT contain Unicode bidirectional control characters.

IRI Reference Values MUST NOT contain Unicode private-use characters.

An IRI Reference Value MUST NOT be a String Value.

IRI Reference Values MUST be compared as opaque strings.

Codex-conforming tools MUST NOT resolve or dereference IRI Reference Values.

### 5.10 Lookup Token Values

A Lookup Token Value is an unquoted token representing a shorthand reference.

In the Surface Form, Lookup Token Values MUST be spelled as `~` followed immediately by a token name.

The token name MUST use camelCase.

Therefore, the token name MUST start with an ASCII lowercase letter.

The token name MAY contain ASCII letters and digits.

The token name MUST NOT contain whitespace, punctuation, hyphens, or underscores.

A Lookup Token Value MUST NOT be a String Value.

Codex-conforming tools MUST NOT resolve or dereference Lookup Token Values.

### 5.11 Character Values

A Character Value represents exactly one Unicode scalar value.

In the Surface Form, Character Values MUST be spelled as character literals.

A Character Value MUST NOT be a String Value.

After interpreting the character literal's escape sequences, the resulting Character Value MUST contain exactly one Unicode scalar value.

### 5.12 List Values

A List Value is an ordered sequence of zero or more Value elements.

In the Surface Form, List Values MUST be spelled using the list literal grammar defined by this specification.

A List Value MUST preserve element order.

A List Value MUST permit zero elements.

Each element of a List Value MUST be a Value.

A List Value MUST permit nesting.

A List Value MUST NOT require all elements to have the same Value type.

A List Value MUST represent exactly the elements explicitly present in its literal spelling.

### 5.13 Set Values

A Set Value is an unordered collection of zero or more Value elements.

In the Surface Form, Set Values MUST be spelled using the set literal grammar defined by this specification.

A Set Value MUST permit zero elements.

Each element of a Set Value MUST be a Value.

A Set Value MUST permit nesting.

A Set Value MUST NOT require all elements to have the same Value type.

A Set Value MUST contain no duplicate elements.

If a set literal spelling contains duplicate elements, Codex-conforming tools MUST ignore duplicates.

### 5.14 Map Values

A Map Value is a collection of key-value pairs.

In the Surface Form, Map Values MUST be spelled using the map literal grammar defined by this specification.

A Map Value MUST permit zero entries.

Each entry in a Map Value MUST bind exactly one key to exactly one Value.

A Map Value MUST permit nesting.

A Map Value MUST contain no duplicate keys.

If a map literal spelling contains duplicate keys, Codex-conforming tools MUST treat that spelling as an error.

#### 5.14.1 Map Keys

In the Surface Form, a map key MUST be one of:

- an unquoted identifier key
- a String Value
- a Character Value
- an integer Numeric Value
- an Enumerated Token Value

An unquoted identifier key MUST start with an ASCII lowercase letter.

An unquoted identifier key MAY contain ASCII letters and digits.

An unquoted identifier key MUST NOT contain whitespace, punctuation, hyphens, or underscores.

### 5.15 Tuple Values

A Tuple Value is an ordered sequence of one or more Value elements with positional semantics.

In the Surface Form, Tuple Values MUST be spelled using the tuple literal grammar defined by this specification.

A Tuple Value MUST preserve element order.

A Tuple Value MUST contain at least one element.

Each element of a Tuple Value MUST be a Value.

A Tuple Value MUST permit nesting.

A Tuple Value MUST NOT require all elements to have the same Value type.

For any Tuple Value used by a Trait, the governing schema MUST define the required arity and the meaning of each position.

### 5.16 Range Values

A Range Value is a declarative interval.

In the Surface Form, Range Values MUST be spelled using the range literal grammar defined by this specification.

A Range Value MUST contain a start endpoint and an end endpoint.

The start endpoint and end endpoint MUST be Values of the same Value type.

An optional step MAY be present.

If a step is present, the step MUST be a Value appropriate to the endpoint Value type.

Range endpoints MUST be treated as inclusive.

Codex-conforming tools MUST NOT enumerate Range Values.

The semantics of a Range Value beyond these structural requirements MUST be defined by the governing schema or consuming system.

---

## 6. Identity

### 6.1 Identifiers and the `id` Trait

An identifier is a stable, globally unique name for an Entity.

Identifiers MUST be declared, not inferred.

Identifiers MUST be expressed exclusively via the `id` Trait.

Codex-conforming tools MUST NOT synthesize an `id` Trait.

### 6.2 Identifiers Are IRIs

All identifiers MUST be IRIs as defined by RFC 3987 (Internationalized Resource Identifiers): https://www.rfc-editor.org/rfc/rfc3987.

Identifiers MUST be comparable as opaque strings.

Codex-conforming tools MUST NOT require identifiers to be dereferenceable.

### 6.3 IRI Surface Profile Restrictions

In the Surface Form, identifiers MUST be spelled as IRI Reference Values (RFC 3987 IRI-reference): https://www.rfc-editor.org/rfc/rfc3987.

Identifier surface spellings MUST NOT contain Unicode whitespace characters.

Identifier surface spellings MUST NOT contain Unicode control characters.

Identifier surface spellings MUST NOT contain Unicode bidirectional control characters.

Identifier surface spellings MUST NOT contain Unicode private-use characters.

Identifier surface spellings MUST permit percent-encoding.

### 6.4 Stability and Immutability

Once assigned, an identifier MUST continue to refer to the same Entity.

Identifiers MUST NOT be reused for different Entities.

Changing an identifier MUST be treated as creating a new Entity.

### 6.5 Opaqueness and Normalization

Codex-conforming tools MUST treat identifiers as opaque values.

Codex-conforming tools MUST NOT reinterpret identifier spellings based on document structure or implicit context.

---

## 7. Reference Traits

### 7.1 Reference Traits Overview

Codex defines exactly three reference Traits:

- `reference`
- `target`
- `for`

Each reference Trait binds a Concept instance to another Concept instance by identifier.

The value of each reference Trait MUST be either an IRI Reference Value (see §5.9) or a Lookup Token Value (see §5.10).

The value of a reference Trait MUST NOT be any other Value type.

Reference Traits MUST be interpreted only as declarative relationships.

Reference Traits MUST NOT imply resolution, dereferencing, loading, execution, or transformation.

Reference Traits are valid only where authorized by the governing schema.

Where reference Traits are authorized, the governing schema MUST define any additional semantics beyond the intent statements in this section.

### 7.2 `reference`

The `reference` Trait expresses that a Concept instance mentions or depends on another Concept instance for meaning.

The `reference` Trait MUST NOT imply action, application, scope, execution, or transformation.

### 7.3 `target`

The `target` Trait expresses that a Concept instance is about, applied to, or oriented toward another Concept instance.

The `target` Trait MUST NOT imply execution or transformation.

### 7.4 `for`

The `for` Trait expresses applicability, scope, specialization, or intended domain.

The `for` Trait MUST NOT imply execution or transformation.

If a `for` reference is used to denote a Concept type, it MUST reference the `ConceptDefinition` Entity for that Concept.

### 7.5 Singleton Rule

By default, a Concept instance MUST NOT declare more than one of the following Traits:

- `reference`
- `target`
- `for`

A schema MAY explicitly authorize an exception.

Any exception MUST be explicit and documented.

If a Concept instance declares more than one of these Traits without a schema-authorized exception, Codex-conforming tools MUST treat that instance as invalid.

If a schema authorizes an exception, the schema MUST document the permitted combinations and the intended interpretation.

### 7.6 Examples (Informative)

This section is informative.

Example: using `reference` for a citation-like relationship.

In this example, `Footnote` mentions (and depends on) `Source` for meaning, but does not apply to it.

```cdx
<Source id=source:HobbitFirstEdition title="The Hobbit" />

<Footnote
	id=note:fn1
	reference=source:HobbitFirstEdition
	text="First published in 1937."
/>
```

Example: using `target` for an about/applied-to relationship.

In this example, `Tag` is applied to (is about) the `Book` Concept instance.

```cdx
<Book id=book:TheHobbit key=~hobbit title="The Hobbit" />

<Tag id=tag:classicFantasy target=~hobbit name=$classicFantasy />
```

Example: using `for` to scope a rule/policy to a Concept type.

In this example, `LabelPolicy` is not about a particular `Book` instance; it is intended to apply to the `Book` Concept type.

```cdx
<ConceptDefinition id=concept:Book key=~book name="Book" />

<LabelPolicy id=policy:BookLabels for=concept:Book />
<LabelPolicy id=policy:BookLabelsAlt for=~book />
```

Example (invalid unless explicitly authorized by schema): a single Concept instance declares both `reference` and `target`.

```cdx
<Link id=link:1 reference=source:HobbitFirstEdition target=book:TheHobbit />
```

---

## 8. Surface Form

### 8.1 File Encoding

Codex documents MUST be encoded in UTF-8 or UTF-16.

UTF-8 is the default encoding.

UTF-8 encoded files MUST NOT include a Byte Order Mark (BOM).

UTF-16 encoding MUST be indicated by a BOM at the start of the file:

- `FE FF` (2 bytes) indicates UTF-16 Big Endian.
- `FF FE` (2 bytes) indicates UTF-16 Little Endian.

Codex-conforming tools MUST determine the file encoding as follows:

- If the file starts with `FE FF`, interpret the file as UTF-16 Big Endian.
- If the file starts with `FF FE`, interpret the file as UTF-16 Little Endian.
- Otherwise, interpret the file as UTF-8 with no BOM.

Codex-conforming tools MUST treat any other encoding as an error.

### 8.2 Line Endings

The canonical line ending is LF (`\n`, U+000A).

Codex-conforming tools MUST normalize CRLF (`\r\n`) sequences to LF on input.

Bare CR (`\r`) is forbidden.

Codex-conforming tools MUST treat bare CR (`\r`) as a parse error.

In canonical surface form, a Codex document MUST end with a trailing LF.

### 8.3 Indentation

Indentation is a canonical formatting requirement.

In canonical surface form, indentation MUST use tabs only.

In canonical surface form, one tab character represents one level of nesting.

- A root Concept instance MUST have no indentation (column 0).
- Direct children of a root Concept instance MUST be indented by exactly one tab.
- Each additional nesting level MUST increase indentation by exactly one additional tab.

Codex-conforming formatters MUST normalize indentation before semantic validation proceeds.

Codex-conforming tools MUST NOT treat author indentation as authoritative.

If indentation cannot be normalized deterministically, Codex-conforming tools MUST fail with a formatting error.

### 8.4 Blank Lines

Blank lines are a canonical formatting requirement.

In canonical surface form, a Codex document MUST NOT start with a blank line.

Outside of content blocks (see §8.8) and annotations (see §8.9), Codex-conforming tools MUST NOT produce two consecutive blank lines in canonical surface form.

In canonical surface form, if no grouping or general annotations appear between two sibling Concept instances, there MUST be exactly one blank line between them.

For the purposes of this rule, an attached-annotation stack (see §8.9.6.1) MUST be treated as part of the Concept instance it attaches to.

If grouping or general annotations appear between two sibling Concept instances, blank line requirements are governed by the annotation rules (see §8.9.8).

In canonical surface form, blank line restrictions apply only to structure parsed as child Concepts.

Outside of annotations (see §8.9) and content, a blank line MUST NOT appear in any other location within a Concept instance body interpreted as containing child Concepts.

In canonical surface form, Codex-conforming tools MUST treat the following as errors:

- A blank line between a Concept instance's opening marker and its first child.
- A blank line between a Concept instance's last child and its closing marker.
- A blank line within a Concept instance body except between sibling children.

A blank line is a line containing no characters after normalization.

Codex-conforming tools MUST treat a line containing only whitespace as empty after normalization.

Annotation blank-line rules MUST be defined by the rules for annotations (see §8.9).

Content is opaque to semantics and MAY contain blank lines.

Blank line restrictions in this section MUST NOT be applied to content.

### 8.5 Concept Markers

A Concept instance MUST be delimited by a Concept marker.

Codex defines three Concept marker forms:

- Opening marker
- Closing marker
- Self-closing marker

#### 8.5.1 Opening Marker

An opening marker MUST be spelled as:

```cdx
<ConceptName>
<ConceptName trait=value>
```

`ConceptName` MUST follow the naming rules defined by this specification.

Traits MAY appear inline in the opening marker.

If multiple Traits are present, their order MUST be preserved.

#### 8.5.2 Closing Marker

A closing marker MUST be spelled as:

```cdx
</ConceptName>
```

The closing marker MUST match the most recent unclosed Concept instance.

The closing marker MUST appear on its own line after indentation.

No additional content is permitted on the closing marker line.

#### 8.5.3 Self-Closing Marker

A self-closing marker MUST be spelled as:

```cdx
<ConceptName />
<ConceptName trait=value />
```

A self-closing marker represents a Concept instance with no content and no child Concepts.

A self-closing marker MAY include Traits.

#### 8.5.4 Empty Block Concepts

The form `<ConceptName></ConceptName>` is invalid.

Codex-conforming tools MUST treat that form as a parse error.

To represent a deliberately empty Concept instance, authors MUST use self-closing form.

### 8.6 Traits

A Trait MUST be spelled as:

```cdx
traitName=value
```

The `traitName` MUST follow the naming rules defined by this specification.

The `value` MUST be a Value as defined by this specification.

No whitespace is permitted around `=`.

Traits MUST be separated by whitespace (space or newline).

If multiple Traits are present, their order MUST be preserved.

#### 8.6.1 Canonical Trait Formatting

Canonical surface form for Traits depends on the number of Traits present in a Concept opening marker.

If a Concept opening marker has one or two Traits, the Traits MUST appear on a single line.

If a Concept opening marker has three or more Traits, each Trait MUST appear on its own line.

When Traits are written on multiple lines, each Trait line MUST be indented exactly one nesting level deeper than the Concept marker.

### 8.7 Values (Surface Parsing Notes)

In the Surface Form, Trait values are literal spellings of Value types defined by this specification (see §5).

Codex-conforming tools MUST parse Values mechanically.

Codex-conforming tools MUST NOT evaluate, interpret, or normalize Values beyond recognizing their Value type and literal structure.

A Trait value spelling MUST match exactly one Value spelling defined by this specification (see §5).

If a Trait value spelling does not match any Value spelling defined by this specification, Codex-conforming tools MUST treat it as a parse error.

Codex-conforming tools MUST NOT infer a Value type.

Codex-conforming tools MUST NOT coerce one Value type into another.

Within a Concept marker, a Value MUST terminate at the first of the following:

- unbalanced whitespace (space, tab, or newline)
- `>` or `/>` (end of Concept marker)

While scanning for Value termination, Codex-conforming tools MUST respect balanced delimiters as required by the Value spellings and the grammar, including `[]`, `{}`, `()`, `''`, and `""`.

Except where permitted by a Value spelling (for example, within string and character literals), leading and trailing whitespace MUST NOT be treated as part of a Value.

### 8.8 Content Blocks

A Content Block is opaque text between an opening marker and a closing marker.

Content is not a Value.

Content MUST NOT be interpreted as Codex structure, Traits, or Values.

In canonical surface form, content lines MUST be indented one nesting level deeper than their enclosing Concept instance.

Content MAY contain blank lines.

Content MAY span multiple lines.

#### 8.8.1 Content Termination

Codex-conforming tools MUST identify the end of content by scanning for the closing marker that matches the opening Concept name: `</ConceptName>`.

#### 8.8.2 Content Escaping

Within content:

- `\<` represents a literal `<`.
- `\\` represents a literal `\`.

Codex-conforming tools MUST treat any other use of `\` within content as a parse error.

A raw `<` character MUST NOT appear in content.

A raw `\` character MUST NOT appear in content.

#### 8.8.3 Content Indentation Normalization

Codex-conforming tools MUST store and process content without its canonical leading indentation.

In canonical surface form, each non-blank content line MUST be indented exactly one nesting level deeper than its enclosing Concept instance.

For each non-blank content line, the canonical leading indentation is the exact leading indentation required to place that line at one nesting level deeper than its enclosing Concept instance.

Codex-conforming tools MUST remove exactly that canonical leading indentation from each non-blank content line when producing the logical content.

Codex-conforming tools MUST preserve all characters following the removed indentation, including any additional leading whitespace.

If a non-blank content line does not have the required canonical leading indentation after indentation normalization, Codex-conforming tools MUST fail with a formatting error.

#### 8.8.4 Examples (Informative)

This section is informative.

Example: indentation stripping while preserving whitespace-sensitive content.

```cdx
<Code>
	def add(a, b):
	    return a + b
</Code>
```

The logical content is:

```
def add(a, b):
    return a + b
```

Example: escaping `<` and `\` inside content.

```cdx
<Tutorial>
	<Section title="Writing Descriptions">
		To write a description, use the Description Concept:

		\<Description>Your text here.\</Description>

		The text inside is opaque content.
	</Section>
</Tutorial>
```

### 8.9 Annotations

Annotations are editorial metadata, distinct from Values and content.

Codex-conforming tools MUST preserve annotations without interpretation.

#### 8.9.1 Annotation Forms

Codex defines two surface forms for annotations.

##### 8.9.1.1 Inline Annotation

An inline annotation MUST use `[` and `]` on the same line.

```cdx
[Short note]
<Thing />
```

##### 8.9.1.2 Block Annotation

A block annotation MUST use `[` and `]` on their own lines.

```cdx
[
	A longer note.
	It may include lists:

	- red
	- green
	- blue
]
```

Annotations MAY appear at top-level or within bodies interpreted as containing child Concepts.

Annotations MUST NOT appear inside Concept markers.

Annotations MAY contain arbitrary text, including blank lines.

#### 8.9.2 Structural Rules

The opening `[` MUST be the first non-whitespace character on its line.

For an inline annotation, the closing `]` MUST appear on the same line.

For a block annotation:

- The line containing `[` MUST contain no other non-whitespace characters.
- The closing `]` MUST appear as the first non-whitespace character on its own line.
- The closing `]` line MUST contain no other non-whitespace characters.

#### 8.9.3 Escaping

Within an annotation:

- `\]` represents a literal `]`.
- `\\` represents a literal `\`.

No other escape sequences are defined.

Codex-conforming tools MUST treat any other use of `\` within an annotation as a parse error.

#### 8.9.4 Canonical Form

Canonicalization of annotations is deterministic and depends on the annotation form.

##### 8.9.4.1 Inline Annotation Canonicalization

Codex-conforming tools MUST canonicalize inline annotations as follows:

- Leading and trailing whitespace inside the brackets MUST be trimmed.
- Internal runs of whitespace (spaces, tabs, and newlines) MUST be collapsed to a single space.
- Escaped characters MUST remain escaped.

Canonical rendering MUST use no padding spaces just inside the brackets (for example, `[text]`, not `[ text ]`).

##### 8.9.4.2 Block Annotation Canonicalization

Block annotations MUST preserve their internal line structure.

Codex-conforming tools MUST normalize block-annotation line endings to LF.

Block annotations MAY declare a directive (see §8.9.5) that controls additional canonicalization.

For a block annotation with no directive, Codex-conforming tools MUST:

- Remove trailing whitespace on each content line.
- Normalize indentation so that the content lines are indented exactly one tab deeper than the `[` / `]` lines.

#### 8.9.5 Block Annotation Directives

In a block annotation, the first non-blank content line MAY be a directive line.

If present, the directive line MUST be exactly one of:

- `FLOW:`
- `CODE:`
- `MARKDOWN:`

If present, the directive line MUST be preserved in canonical output.

Directive behavior:

- `CODE:` — Codex-conforming tools MUST preserve the block annotation bytes verbatim except for newline normalization.
- `MARKDOWN:` — Codex-conforming tools MUST preserve the block annotation bytes verbatim except for newline normalization.
- `FLOW:` — The flow-text value is the remaining content with leading and trailing whitespace trimmed, internal runs of whitespace collapsed to single spaces, and escapes interpreted per §8.9.3.

For `CODE:` and `MARKDOWN:` directives, Codex-conforming tools MUST NOT reindent, trim, strip trailing whitespace, wrap, or interpret escapes within the block annotation.

If no directive is present, the block annotation MUST be canonicalized as described in §8.9.4.2.

For `FLOW:` directives, Codex-conforming tools MUST render canonical output as follows:

- Split the remaining content into paragraphs separated by one or more blank lines.
- For each paragraph, wrap words to lines of at most 80 Unicode scalar characters using greedy packing.
- Indent each wrapped line exactly one tab deeper than the `[` / `]` lines.
- Separate paragraphs by exactly one blank line.

#### 8.9.6 Annotation Kinds

Codex defines three kinds of annotations:

1. Attached annotations — attach to a single Concept instance.
2. Grouping annotations — `GROUP` / `END` markers that bracket a region.
3. General annotations — standalone annotations (inline or block).

##### 8.9.6.1 Attached Annotations

An annotation is an attached annotation if and only if:

- It is an inline annotation.
- It is not a grouping annotation.
- It is immediately followed (on the next line) by a Concept opening marker.
- There is no blank line between the annotation and that marker.

Multiple attached annotations MAY stack.

An attached-annotation stack attaches to the next Concept opening marker.

Attached annotations MUST NOT have blank lines separating them from each other.

If a blank line appears between stacked annotations, the annotations MUST NOT be treated as attached.

##### 8.9.6.2 Grouping Annotations

A grouping annotation is a single-line annotation whose canonicalized annotation text matches one of the following forms:

- `GROUP: <label>`
- `END: <label>`

`<label>` MUST be a non-empty string after trimming.

Grouping recognition MUST be performed after applying the inline annotation canonicalization rules in §8.9.4.1.

Grouping annotations MUST NOT attach to Concept instances.

Grouping annotations define a purely editorial grouping region.

Grouping annotations MAY nest.

Label comparison MUST use the canonical label form (trimmed, with internal whitespace collapsed to single spaces).

##### 8.9.6.3 General Annotations

An annotation is a general annotation if and only if:

- It is surrounded by exactly one blank line above and exactly one blank line below, where file boundaries count as blank-line boundaries.
- It is not a grouping annotation.

General annotations MAY be inline or block.

General annotations MUST NOT attach to Concept instances.

#### 8.9.7 Group Nesting and Matching

Grouping annotations form a properly nested stack.

- `[GROUP: X]` pushes label `X`.
- `[END: X]` MUST match the most recent unmatched `[GROUP: X]`.

If an `END` label does not match the most recent open group label, or if an `END` appears with no open group, Codex-conforming tools MUST treat the document as invalid.

#### 8.9.8 Canonical Blank Line Requirements

In canonical surface form:

- Attached annotations MUST appear directly above the annotated Concept opening marker with no blank line.
- Grouping annotations MUST be surrounded by exactly one blank line above and below, where file boundaries count as blank-line boundaries.
- General annotations MUST be surrounded by exactly one blank line above and below, where file boundaries count as blank-line boundaries.

Any annotation that is neither an attached annotation, a grouping annotation, nor a general annotation is invalid.

---

## 9. Schema-First Architecture

Codex is schema-first.

A conforming implementation MUST provide schema-directed parsing and validation.

This specification defines the authoritative model for schema authoring, schema-to-instance-graph interpretation, and deterministic projection to derived validation artifacts.

### 9.1 Scope and Inputs

Schema-first means that semantic meaning and semantic validation are defined by a governing schema.

Given the same required inputs, a conforming implementation MUST produce the same parsing, validation, and canonicalization results.

The required inputs for schema-directed processing are:

- the Codex document bytes
- the governing schema
- any other external inputs explicitly required by this specification or by the governing schema

If any required input is missing, schema-directed processing MUST fail.

Given a Codex document and a governing schema, a conforming implementation MUST dispatch parsing and validation according to that schema.

### 9.2 Schema-Less Formatting / Well-Formedness Checks

An implementation MAY perform purely syntactic parsing and formatting checks without a governing schema.

If an implementation performs schema-less checks, it MUST limit those checks to rules that are explicitly defined by this specification as independent of schema semantics.

Schema-less checks MAY include:

- determining whether the input bytes can be decoded as a permitted file encoding
- determining whether the input matches the surface-form grammar
- enforcing surface-form structural well-formedness (including marker nesting/matching)
- enforcing surface-form canonicalization rules defined by this specification

Schema-less checks MUST NOT include any schema-driven semantic interpretation.

In particular, without a governing schema, an implementation MUST NOT:

- interpret content mode versus child mode for a concept beyond what is mechanically implied by the surface form
- interpret whether a concept instance is an Entity beyond the presence or absence of an `id` trait spelling
- evaluate trait meaning, trait authorization, value typing beyond surface-form Value recognition, or constraint logic
- resolve or validate reference traits beyond their surface-form value type constraints

### 9.3 Schema-Required Semantic Validation

An implementation MUST NOT perform semantic validation without a governing schema.

Given a governing schema, an implementation MUST perform semantic validation as defined by that schema.

Schema-driven semantic validation MUST be deterministic and MUST be explainable in terms of the specific schema rule(s) applied.

Schema-driven semantic validation MUST include evaluation of all schema-defined authorizations and constraints, including at least:

- concept authorization and required/forbidden structure
- content mode versus child mode requirements
- trait authorization and required/forbidden traits
- value type constraints beyond surface-form recognition
- entity eligibility and any schema-defined identity constraints
- schema-defined constraints over children, descendants, and collections
- schema-defined reference semantics and any schema-defined resolution requirements

If the governing schema requires any external inputs (for example, inputs needed to interpret lookup token bindings or to construct derived validation artifacts), those inputs MUST be explicit and machine-checkable.

The required semantics for schema-driven validation and any required derived artifacts are defined by this specification (notably §9.5–§9.11) and by the schema-definition specification.

### 9.4 Authoring Profiles (Guardrail)

A schema document MUST be validated under exactly one authoring profile.

Codex defines two authoring profiles:

- **Profile A**: Layer A schema authoring only
- **Profile B**: Layer B schema authoring only

A schema document MUST NOT mix profiles.

The authoring profile MUST be selected by an explicit declaration in the schema document.

The schema document's root `Schema` concept MUST have an `authoringProfile` trait.

`authoringProfile` MUST be exactly one of:

- `$ProfileA`
- `$ProfileB`

If `authoringProfile` is missing or has any other value, schema processing MUST fail.

Additional guardrails MUST hold:

- Profile A schemas MUST NOT contain `RdfGraph`.
- Profile B schemas MUST contain exactly one `RdfGraph` and MUST NOT contain Layer A schema-definition concepts.
- Layer A expansion MUST generate a canonical Layer B graph; different Layer A spellings that are semantically identical MUST expand to byte-identical Layer B graphs.
- Layer B canonicalization MUST make semantically identical graphs byte-identical.

### 9.5 Layer A (Codex-Native Schema Authoring)

Layer A is the Codex-native schema authoring model defined by the schema-definition specification.

Layer A schema authoring MUST satisfy the Codex language invariants, including closed-world semantics, determinism, and prohibition of heuristics.

Layer A authoring is the required authoring form for Profile A.

To support a total, deterministic projection to derived validation artifacts, Profile A schema authoring MUST additionally support the following extensions.

#### 9.5.1 Pattern Flags

The following atomic constraints MUST support an optional `flags` trait whose value is a string:

- `ValueMatchesPattern`
- `PatternConstraint`
- `ContentMatchesPattern`

If `flags` is omitted, it MUST be treated as the empty string.

The `pattern` and `flags` semantics MUST be SPARQL 1.1 `REGEX` semantics.

#### 9.5.2 Explicit Validator Definitions

Layer A MUST support explicit validator definitions that make `ValueIsValid` deterministic.

`ValidatorDefinitions` is a container concept.

`ValidatorDefinition` defines one validator.

Each `ValidatorDefinition` MUST have these traits:

- `name` (required; Enumerated Token Value)
- `message` (optional; String Value)

Each `ValidatorDefinition` MUST be in content mode.

The content of `ValidatorDefinition` MUST be a SPARQL `SELECT` query string.

The `SELECT` results MUST follow the SHACL-SPARQL convention (returning one row per violation with `?this` bound to the focus node).

If a derived validation artifact is expressed using SHACL-SPARQL, the embedding contract for `ValueIsValid validatorName=$X` MUST be:

1. Resolve `$X` to exactly one `ValidatorDefinition` in the governing schema.
2. Emit a SHACL-SPARQL constraint whose `sh:select` string is exactly the `ValidatorDefinition` content.

If `$X` cannot be resolved to exactly one `ValidatorDefinition`, schema processing MUST fail.

#### 9.5.3 Explicit Path and Quantifier Rule Forms

Layer A MUST provide explicit rule forms that bind exactly one path to exactly one nested rule, so that path and quantifier semantics are total and deterministic.

The schema-definition specification defines paths (`TraitPath`, `ChildPath`, `DescendantPath`, `ContentPath`) and quantifiers (`Exists`, `ForAll`, `Count`) but does not, by itself, define a concrete rule-node form that composes them with rules.

To produce a total, deterministic mapping, Layer A MUST include explicit rule-node forms that bind a path and scope a nested rule.

Layer A MUST provide the following rule nodes:

- `OnPathExists`
- `OnPathForAll`
- `OnPathCount`

Each of these MUST have exactly one `Path` child and exactly one `Rule` child.

`OnPathCount` MUST additionally have:

- `minCount` (optional; non-negative integer)
- `maxCount` (optional; positive integer)

The `Path` child MUST be exactly one of:

- `TraitPath`
- `ChildPath`
- `DescendantPath`
- `ContentPath`

For schema rules that express the common “every direct child of type X satisfies R” pattern, `ChildSatisfies(conceptSelector=X, Rule=R)` MUST be interpreted as equivalent to `OnPathForAll(Path=ChildPath(X), Rule=R)`.

#### 9.5.4 Collection and Order Constraint Scoping

For each of the following constraint nodes:

- `CollectionOrdering`
- `CollectionAllowsEmpty`
- `CollectionAllowsDuplicates`
- `MemberCount`
- `EachMemberSatisfies`
- `OrderConstraint`

the constraint node MUST have exactly one `Path` child that selects the collection members the constraint applies to.

That member-selection path MUST be either `ChildPath` or `DescendantPath`.

If the member-selection path is not one of these, expansion MUST fail.

For `CollectionAllowsDuplicates` with `allowed=false`, the constraint node MUST include a required `keyTrait` trait whose value is a trait name string.

If `keyTrait` is `id`, it MUST refer to the declared identifier as specified by the instance-graph identity rules.

### 9.6 Layer B (RDF / SHACL Representation)

Layer B is the canonical, fully general schema representation used to derive validation artifacts.

Layer B MUST be representable as an RDF 1.1 graph.

Layer B MAY be further expressed as SHACL shapes.

Layer B MUST be able to represent any SHACL graph, including SHACL-SPARQL constraints.

This specification does not define namespace prefixes; Layer B uses IRIs directly.

Layer B MUST be deterministic and canonical:

- Layer B MUST NOT contain RDF blank nodes.
- All RDF nodes in Layer B MUST be IRIs.
- Where SHACL commonly uses blank nodes (for example, `sh:property` values and RDF lists), Layer B MUST use deterministically derived skolem IRIs instead.
- Layer B MUST be treated as a set of RDF triples.
- Layer B MUST NOT contain duplicate triples.

#### 9.6.1 Canonical Triple Form

When Layer B is authored as a Codex graph form, it MUST use:

- `RdfGraph` — container for triples
- `RdfTriple` — a single RDF triple

`RdfGraph` MUST be in children mode.

`RdfGraph` children MUST be one or more `RdfTriple`.

Each `RdfTriple` MUST have these traits:

- `s` (required; IRI Reference Value) — subject
- `p` (required; IRI Reference Value) — predicate

And exactly one of:

- `o` (required; IRI Reference Value) — object IRI
- `lex` (required; String Value) — object literal lexical form

If `lex` is present, `RdfTriple` MAY have:

- `datatype` (optional; IRI Reference Value) — RDF datatype IRI
- `language` (optional; String Value) — RDF language tag

If `language` is present, `datatype` MUST be absent.

If `datatype` is absent and `language` is absent, the literal datatype MUST be `xsd:string`.

#### 9.6.2 Canonical Ordering and Duplicate Removal

In canonical Layer B, `RdfTriple` children MUST be sorted in ascending lexicographic order of `(s, p, oKey)`.

`oKey` MUST be:

- `o` when the object is an IRI, and
- the pair `(datatypeOrDefault, lex)` when the object is a literal.

If two triples are identical after this normalization, duplicates MUST be removed.

Any algorithm that derives Layer B or derives SHACL shapes from Layer B MUST fail rather than guess when required semantics are not explicitly defined.

#### 9.6.3 RDF List Encoding (No Blank Nodes)

If Layer B includes an RDF list (for example, as the object of `sh:in`), it MUST be encoded using the standard RDF list vocabulary (`rdf:first`, `rdf:rest`, `rdf:nil`).

All RDF list nodes MUST be IRIs.

Where the RDF list encoding would otherwise use blank nodes, Layer B MUST use deterministically derived skolem IRIs instead.

#### 9.6.4 Deterministic Derived IRIs (One Way To Say It)

To preserve “one way to say it”, every derived IRI used by schema processing, instance graph mapping, and derived validation artifact generation MUST be computed by a single deterministic algorithm.

If a derivation is underspecified such that multiple incompatible algorithms could conform, processing MUST fail rather than guess.

#### 9.6.5 Node Shape IRIs

If derived validation artifacts use node shapes (for example, SHACL `sh:NodeShape` resources), the node shape IRI for a concept class IRI `K` MUST be deterministically derived as:

- `nodeShapeIri(K) = K + "#shape"`

#### 9.6.6 Property Shape IRIs

If derived validation artifacts use property shapes (for example, SHACL `sh:PropertyShape` resources), each property shape MUST have a deterministic IRI.

For a node shape IRI `S` and a trait name `t`:

- `propertyShapeIri(S,t) = S + "/property/trait/" + t`

For a node shape IRI `S` and a child class IRI `Q`:

- `propertyShapeIri(S,Q) = S + "/property/child/" + percentEncode(Q)`

`percentEncode` MUST be RFC 3987 percent-encoding over the Unicode string form.

For a node shape IRI `S` and an RDF predicate IRI `p` used as a SHACL path (for example, `codex:content` or `codex:isEntity`):

- `predicatePropertyShapeIri(S,p) = S + "/property/predicate/" + percentEncode(p)`

#### 9.6.7 Document Node Shape IRI

If derived validation artifacts include a node shape targeting the document node, its node shape IRI MUST be deterministically derived as:

- `documentNodeShapeIri = schemaIri + "#shape/Document"`

All canonicalization and projection rules for Layer B required by this specification are defined in this section.

### 9.7 Codex→RDF Instance Graph Mapping

To support deterministic derived validation artifacts (including SHACL), Codex defines a canonical mapping from a parsed Codex document to an RDF instance graph.

The mapping MUST be deterministic and MUST NOT use RDF blank nodes.

The mapping requires an explicit `documentBaseIri` external input.

If `documentBaseIri` is missing, the mapping MUST fail.

#### 9.7.1 Document Node

The instance graph MUST include a single document node.

The RDF node IRI for the Document context MUST be exactly `documentBaseIri`.

#### 9.7.2 Node Identity and Declared Identifiers

Each Concept instance in the Codex document MUST map to exactly one RDF node whose identity is a deterministic skolem IRI derived from its structural position within the document.

##### 9.7.2.1 Skolem IRI Derivation (`nodeIri`)

This section defines a conforming deterministic skolem IRI derivation for concept instance nodes.

Let `C` be a Concept instance.

Let `C.name` be the concept name of `C`.

Let `parent(C)` be the direct parent Concept instance of `C`, or the Document context if `C` is a root Concept instance.

Let `siblings(C)` be:

- the ordered list of all top-level Concept instances in the document (in source order) if `parent(C)` is the Document context, or
- the ordered list of all direct child Concept instances of `parent(C)` (in source order) otherwise.

Let `ordinalIndex(C)` be the unique integer `i` such that `siblings(C)[i]` is `C`.

`ordinalIndex(C)` MUST be zero-based.

`ordinalIndex(C)` MUST be expressed in base-10 with no leading zeros (except that `0` is permitted).

Let `percentEncode` be RFC 3987 percent-encoding over the Unicode string form.

Define `addressSegments(C)` as the ordered list of segments obtained by walking from the document root to `C` (inclusive), where each segment for a visited node `X` is:

- `percentEncode(X.name) + "/" + ordinalIndex(X)`

Define `nodeIri(C)` as:

- `documentBaseIri + "/__node/" + join("/", addressSegments(C))`

`nodeIri(C)` MUST be stable and injective within a document.

The RDF node IRI MUST NOT be derived from the Concept instance's declared `id` trait value.

If a Concept instance declares an `id` trait, that declared identifier MUST be represented as data via a dedicated predicate `codex:declaredId`.

If a concept instance `C` declares an `id` trait with value `v`, the mapping MUST emit:

- `(nodeIri(C), codex:declaredId, valueTerm(v))`

#### 9.7.3 Entity Marker

If and only if a Concept instance is an Entity, the mapped RDF node MUST be marked as an Entity using a dedicated predicate `codex:isEntity`.

To support identity constraints without guessing, the mapping MUST emit an entity marker for every Concept instance node:

- If the concept instance is an Entity, emit `(nodeIri(C), codex:isEntity, "true"^^xsd:boolean)`.
- Otherwise, emit `(nodeIri(C), codex:isEntity, "false"^^xsd:boolean)`.

#### 9.7.4 Parent Link and Ordered Children

For each non-root Concept instance, the instance graph MUST include a parent link using a dedicated predicate `codex:parentNode`.

For each parent Concept instance `C` and each direct child Concept instance `D`, the instance graph MUST emit:

- `(nodeIri(D), codex:parentNode, nodeIri(C))`

For each child Concept instance `D` of parent Concept instance `C`, the instance graph MUST emit the structural child triple:

- `(nodeIri(C), childPredicateIri(C,D), nodeIri(D))`

If an ordered view is required, the instance graph MUST additionally represent the ordered child sequence using explicit edge nodes that carry a stable numeric index (see §9.7.6).

#### 9.7.5 Reserved Predicates

For the purposes of this section, let `schemaIri` be the governing schema's `Schema.id` value.

The following reserved predicates are used by the instance graph mapping:

- `codex:parent`
- `codex:child`
- `codex:index`
- `codex:parentNode`
- `codex:isEntity`
- `codex:declaredId`
- `codex:lookupToken`
- `codex:lookupIri`
- `codex:content`

Their IRIs MUST be deterministically derived from `schemaIri` as follows:

- `codex:parent` MUST be `schemaIri + "#codex/parent"`
- `codex:child` MUST be `schemaIri + "#codex/child"`
- `codex:index` MUST be `schemaIri + "#codex/index"`
- `codex:parentNode` MUST be `schemaIri + "#codex/parentNode"`
- `codex:isEntity` MUST be `schemaIri + "#codex/isEntity"`
- `codex:declaredId` MUST be `schemaIri + "#codex/declaredId"`
- `codex:lookupToken` MUST be `schemaIri + "#codex/lookupToken"`
- `codex:lookupIri` MUST be `schemaIri + "#codex/lookupIri"`
- `codex:content` MUST be `schemaIri + "#codex/content"`

#### 9.7.6 Ordered Children Encoding

This section defines the canonical ordered-children encoding used when an ordered view is required.

For each parent Concept instance `C` and each direct child Concept instance `D` in children order, let:

- `p = nodeIri(C)`
- `d = nodeIri(D)`
- `i = 0..n-1` be the ordinal position of `D` among the direct children of `C`, in source order

When an ordered view is required, the mapping MUST emit an edge node `e` and three triples:

- `(e, codex:parent, p)`
- `(e, codex:child, d)`
- `(e, codex:index, "i"^^xsd:integer)`

The edge node IRI MUST be deterministic and injective.

One conforming derivation is:

- `e = p + "/__childEdge/" + i`

`codex:parentNode` is distinct from `codex:parent`:

- `codex:parentNode` links a concept instance node to its parent concept instance node.
- `codex:parent` links an ordered-child edge node to the parent concept instance node.

#### 9.7.7 Traits and Value Terms

For each trait `t=v` on a concept instance `C`, the instance graph MUST emit exactly one triple:

- `(nodeIri(C), traitPredicateIri(t), valueTerm(v))`

Exception:

- If `t` is `id`, the mapping MUST NOT emit a `traitPredicateIri("id")` triple.
- Instead, `id` MUST be represented only by `codex:declaredId`.

`valueTerm(v)` MUST be:

- an IRI when `v` is an IRI Reference Value
- otherwise a typed literal

In this section, `xsd:*` refers to the XML Schema datatypes namespace.

For typed literals, the datatype IRI MUST be computed by `valueDatatypeIri(v)` and the lexical form MUST be computed by `valueLex(v)`.

Both `valueDatatypeIri(v)` and `valueLex(v)` MUST be derived by parsing `v` according to the Codex value catalog.

`valueDatatypeIri(v)` MUST be:

- `xsd:string` for String Values
- `xsd:string` for Character Values
- `xsd:boolean` for Boolean Values
- `xsd:integer` for Integer Values

For all other value types, `valueDatatypeIri(v)` MUST be the deterministic URN:

- `urn:cdx:value-type:<T>`

where `<T>` is the Codex value type token name (for example, `Uuid`, `Color`, `Temporal`, `List`, `Map`).

`valueLex(v)` MUST be:

- the decoded Unicode string value for String Values
- the single Unicode scalar value as a Unicode string for Character Values
- `"true"` or `"false"` for Boolean Values
- a base-10 integer string for Integer Values

For all other value types, `valueLex(v)` MUST be the canonical surface spelling of `v`.

Lookup Token Values MUST be represented as typed literals with:

- datatype: `urn:cdx:value-type:LookupToken`
- lexical form: the canonical surface spelling (for example, `~myToken`)

If a schema constraint requires an interpreted value (for example, numeric comparisons or string length), schema processing MUST either provide the interpreted value in a deterministic RDF representation or fail.

#### 9.7.8 Content

If a concept instance is in content mode, the mapping MUST emit:

- `(nodeIri(C), codex:content, contentString)`

`contentString` MUST be an `xsd:string` literal containing the concept's content after applying the Codex content escaping rules.

#### 9.7.9 Deterministic Predicate IRIs

For the purposes of this section, let `schemaIri` be the governing schema's `Schema.id` value.

Trait predicate IRIs MUST be derived as follows.

For a trait name `t`:

- If the governing schema contains exactly one `TraitDefinition` for `t` and that `TraitDefinition` has an `id`, `traitPredicateIri(t)` MUST be that `id`.
- Otherwise, `traitPredicateIri(t)` MUST be `schemaIri + "#trait/" + t`.

Child predicate IRIs MUST be derived as follows.

Let the governing schema's `ConceptDefinition.id` for the parent concept name be `P` and for the child concept name be `Q`.

- `childPredicateIri(P,Q)` MUST be `P + "#child/" + percentEncode(Q)`.

`percentEncode` MUST be RFC 3987 percent-encoding over the Unicode string form.

#### 9.7.10 RDF Types

Each Concept instance MUST emit an RDF type triple:

- `(nodeIri(C), rdf:type, conceptClassIri(C.name))`

`conceptClassIri(X)` MUST be the `ConceptDefinition.id` for concept name `X` in the governing schema.

If `conceptClassIri(X)` cannot be resolved to exactly one `ConceptDefinition`, schema-driven validation MUST fail.

All aspects of the instance graph mapping required by this specification are defined in this section.

### 9.8 Lookup Binding Table

Lookup Token Values (see §5.10) are never resolved implicitly.

If a governing schema requires lookup tokens to be resolved for any validation rule, the schema-driven validation process MUST construct and use an explicit lookup binding table.

Each lookup binding MUST map exactly one lookup token name to exactly one IRI.

If a lookup token is required to be resolved and the binding table does not contain exactly one binding for that token, schema-driven validation MUST fail.

#### 9.8.1 Representation in the Instance Graph

The schema-driven validation process MAY incorporate a lookup binding table.

Each binding entry associates one Lookup Token Value with one IRI.

Lookup Token Values MUST be represented as typed literals with:

- datatype: `urn:cdx:value-type:LookupToken`
- lexical form: the canonical surface spelling (for example, `~myToken`)

Binding entries MUST be represented in the instance graph using the reserved predicates:

- `codex:lookupToken` (object MUST be a Lookup Token typed literal)
- `codex:lookupIri` (object MUST be an IRI)

The mapping MUST accept bindings from any source that is explicit and deterministic.

One conforming source is: a document-level section that is parsed into a list of bindings in source order.

For each binding entry at ordinal position `i`, the mapping MUST emit a binding node `b` and two triples:

- `(b, codex:lookupToken, tokenLiteral)`
- `(b, codex:lookupIri, targetIri)`

The binding node IRI MUST be deterministic and injective within a document.

One conforming derivation is:

- `b = documentBaseIri + "/__lookupBinding/" + i`

#### 9.8.2 Binding Table Well-Formedness

Additional binding table well-formedness rules:

- If two binding entries have the same `tokenLiteral`, schema-driven validation MUST fail.
- If any binding entry lacks either `tokenLiteral` or `targetIri`, schema-driven validation MUST fail.
- If any binding entry provides multiple `targetIri` values for the same `tokenLiteral`, schema-driven validation MUST fail.

### 9.9 Deterministic Projection to Derived Validation Artifacts

A conforming implementation MAY derive validation artifacts from a governing schema.

If an implementation derives validation artifacts, it MUST do so deterministically.

Any derived validation artifact MUST be a pure function of:

- the governing schema
- the explicitly required external inputs, if any

Derived validation artifact generation MUST fail rather than guess if any required semantic rule is not explicitly defined.

Derived validation artifact generation MUST fail if any of the following hold:

- the governing schema is not valid under the schema-of-schemas
- any `ConceptDefinition` lacks an `id`
- any required selector (concept name, trait name) cannot be resolved to a unique definition
- any schema rule produces a semantic constraint that cannot be expressed under the chosen Codex→RDF instance graph mapping

Codex permits derived validation artifacts expressed as SHACL.

If SHACL is used as a derived validation artifact format, the generated shapes MAY use SHACL-SPARQL.

If the governing schema includes constraint definitions with explicit targets, a derived SHACL artifact MUST apply each constraint to the target node shape(s) determined as follows:

- For `TargetConcept conceptSelector="X"`, the constraint MUST be applied to the node shape derived from the `ConceptDefinition` whose `name` is `X`.
- For `TargetContext contextSelector="Document"`, the constraint MUST be applied to a special node shape with IRI `schemaIri + "#shape/Document"` and MUST include at least:
	- `(schemaIri + "#shape/Document", rdf:type, sh:NodeShape)`
	- `(schemaIri + "#shape/Document", sh:targetNode, documentBaseIri)`
	If `documentBaseIri` is not available as an external input, derived validation artifact generation MUST fail.
- If `contextSelector` is a concept name (not `Document`), the constraint MUST be applied to the node shape for that concept.

If a derived validation artifact is produced as a SHACL graph, it MUST be canonical and MUST include the following structural shape triples:

- For each `ConceptDefinition` in the governing schema with concept name `X`, let `K = conceptClassIri(X)` and let `S = nodeShapeIri(K)`. The derived artifact MUST include:
	- `(S, rdf:type, sh:NodeShape)`
	- `(S, sh:targetClass, K)`
- If the derived artifact includes any constraint expressed on a property shape `PS`, it MUST include:
	- `(S, sh:property, PS)` where `S` is the owning node shape
	- `(PS, rdf:type, sh:PropertyShape)`
	and `PS` MUST be deterministically derived as follows:
	- for a trait name `t`: `PS = propertyShapeIri(S,t)` and the artifact MUST include `(PS, sh:path, traitPredicateIri(t))`
	- for a child class IRI `Q`: `PS = propertyShapeIri(S,Q)` and the artifact MUST include `(PS, sh:path, childPredicateIri(K,Q))`
	- for a predicate IRI `p`: `PS = predicatePropertyShapeIri(S,p)` and the artifact MUST include `(PS, sh:path, p)`

If a derived validation artifact expresses any constraint using SHACL-SPARQL, the `sh:select` string MUST be a SPARQL 1.1 `SELECT` query that returns one row per violating focus node using the SHACL-SPARQL convention:

- the focus node variable MUST be `?this`
- a row returned by the query MUST indicate a violation

To keep derived artifacts canonical and avoid accidental variable capture, internal SPARQL variables introduced during constraint translation MUST be allocated deterministically.

One conforming approach is:

- Walk the constraint's rule tree in pre-order.
- For the $k$-th visited node (1-indexed), allocate a node-local suffix $k$.
- Any internal variable introduced while translating that node MUST append suffix $k$ to a base name.
- Variables introduced for one rule node MUST NOT be referenced outside the `EXISTS { ... }` block created for that node.

#### 9.9.1 Enumerated Value Sets (`sh:in`)

If a derived SHACL artifact encodes an enumerated value-set constraint using `sh:in` on a property shape `PS`, it MUST emit a triple `(PS, sh:in, listHead)`.

This rule applies whenever the governing schema constrains a value to a fixed enumerated set and that constraint is projected into SHACL.

`listHead` MUST be an IRI and MUST be a deterministically derived skolem IRI (no blank nodes).

The list structure MUST be encoded as an RDF list as specified in §9.6.3.

#### 9.9.2 Pattern Constraints (`sh:pattern`, `sh:flags`)

If a derived SHACL artifact encodes a pattern constraint using `sh:pattern` on a property shape `PS`, it MUST emit a triple `(PS, sh:pattern, p)`.

If `flags` is present and non-empty, it MUST emit a triple `(PS, sh:flags, f)`.

This rule applies to derived SHACL constraints corresponding to schema constraints such as `ValueMatchesPattern` and `PatternConstraint`.

The `pattern` and `flags` semantics MUST be SPARQL 1.1 `REGEX` semantics (see §9.5.1).

#### 9.9.3 SHACL Core Value Constraints

If a derived SHACL artifact encodes a value-length constraint on a property shape `PS`, it MUST emit:

- `(PS, sh:minLength, "a"^^xsd:integer)` when a minimum length `a` is present
- `(PS, sh:maxLength, "b"^^xsd:integer)` when a maximum length `b` is present

If a derived SHACL artifact encodes a non-empty constraint on a property shape `PS`, it MUST emit:

- `(PS, sh:minLength, "1"^^xsd:integer)`

If a derived SHACL artifact encodes a numeric-range constraint on a property shape `PS`, it MUST use SHACL Core numeric bounds only when the active value datatype is `xsd:integer`.

If the active datatype is not `xsd:integer`, derived validation artifact generation MUST fail.

When permitted, it MUST emit:

- `(PS, sh:minInclusive, "u"^^xsd:integer)` when a minimum value `u` is present
- `(PS, sh:maxInclusive, "v"^^xsd:integer)` when a maximum value `v` is present

#### 9.9.4 Child Constraints

For child constraints projected onto a property shape `PS`, let `P` be the concept class IRI (RDF class) targeted by the owning node shape.

If a derived SHACL artifact encodes a required-child constraint for a child concept selector `X` on a property shape `PS`, it MUST emit:

- `(PS, sh:path, childPredicateIri(P, conceptClassIri(X)))`
- `(PS, sh:minCount, "1"^^xsd:integer)`
- `(PS, sh:class, conceptClassIri(X))`

If a derived SHACL artifact encodes a forbidden-child constraint for a child concept selector `X` on a property shape `PS`, it MUST emit:

- `(PS, sh:path, childPredicateIri(P, conceptClassIri(X)))`
- `(PS, sh:maxCount, "0"^^xsd:integer)`

If a schema rule permits a child relationship (allows without requiring), the derived SHACL artifact MUST NOT emit a constraint.

#### 9.9.5 Content Constraints

If a derived SHACL artifact encodes a content-required constraint on a property shape `PS`, it MUST emit:

- Let `S` be the owning node shape for the constraint. The property shape IRI MUST be `PS = predicatePropertyShapeIri(S, codex:content)`.
- `(PS, sh:path, codex:content)`
- `(PS, sh:minLength, "1"^^xsd:integer)`

If a derived SHACL artifact encodes a content pattern constraint on a property shape `PS`, it MUST emit:

- Let `S` be the owning node shape for the constraint. The property shape IRI MUST be `PS = predicatePropertyShapeIri(S, codex:content)`.
- `(PS, sh:path, codex:content)`
- `(PS, sh:pattern, p)`

If `flags` is present and non-empty, it MUST emit:

- `(PS, sh:flags, f)`

The `pattern` and `flags` semantics MUST be SPARQL 1.1 `REGEX` semantics (see §9.5.1).

#### 9.9.6 Identity Constraints (`codex:isEntity`)

If a derived SHACL artifact encodes an identity constraint requiring an entity, it MUST emit:

- Let `S` be the owning node shape for the constraint. The property shape IRI MUST be `PS = predicatePropertyShapeIri(S, codex:isEntity)`.
- `(PS, sh:path, codex:isEntity)`
- `(PS, sh:hasValue, "true"^^xsd:boolean)`

If a derived SHACL artifact encodes an identity constraint requiring a non-entity, it MUST emit:

- Let `S` be the owning node shape for the constraint. The property shape IRI MUST be `PS = predicatePropertyShapeIri(S, codex:isEntity)`.
- `(PS, sh:path, codex:isEntity)`
- `(PS, sh:hasValue, "false"^^xsd:boolean)`

#### 9.9.7 Uniqueness Constraints

Derived validation artifacts MUST support the following uniqueness constraints.

For both constraints, the identity of a trait is determined by the instance-graph trait mapping (see §9.7.7).

If a uniqueness constraint refers to `t = id`, it MUST refer to the declared identifier as represented by `codex:declaredId`.

For nearest-scope uniqueness, `UniqueConstraint(trait=t, scope=S)` MUST mean:

- within the nearest ancestor (including self) of concept type `S`, no two nodes may share the same value for trait `t`.

For purposes of this constraint, the nearest scope node is the unique node `scopeK` such that:

- `focusVar <codex:parentNode>* scopeK`
- `scopeK rdf:type <conceptClassIri(S)>`
- and there is no other node `midK` where:
	- `focusVar <codex:parentNode>* midK`
	- `midK rdf:type <conceptClassIri(S)>`
	- `midK <codex:parentNode>+ scopeK`
	- `midK != scopeK`

Derived validation artifact generation MUST fail if no nearest scope node exists.

For document-wide uniqueness, `UniqueInDocument(trait=t)` MUST mean:

- no two nodes in the Document may share the same value for trait `t`.

#### 9.9.8 Context Constraints

Context constraints are expressible using the deterministic parent links in the instance graph (see §9.7.4).

`ContextConstraint(type=OnlyValidUnderParent, contextSelector=P)` MUST be expressible in derived validation artifacts.

If projected into a SHACL-derived artifact, it MUST map to SHACL-SPARQL and MUST report a violation when the focus node has no direct parent of type `P`.

One conforming boolean condition for the SHACL-SPARQL constraint is:

```
EXISTS {
	focusVar <codex:parentNode> ?pK .
	?pK rdf:type <conceptClassIri(P)> .
}
```

`ContextConstraint(type=OnlyValidUnderContext, contextSelector=A)` MUST be expressible in derived validation artifacts.

If projected into a SHACL-derived artifact, it MUST map to SHACL-SPARQL and MUST report a violation when the focus node has no ancestor (via one or more parent links) of type `A`.

One conforming boolean condition for the SHACL-SPARQL constraint is:

```
EXISTS {
	focusVar <codex:parentNode>+ ?aK .
	?aK rdf:type <conceptClassIri(A)> .
}
```

#### 9.9.9 Reference Constraints (Reference Trait Predicates)

Reference constraints are expressible without external resolution if identifiers are represented by `codex:declaredId` and lookup tokens are resolvable via the lookup binding table (see §9.8).

For the purposes of reference constraints, the set of reference-trait predicates MUST be exactly:

- `traitPredicateIri("reference")`
- `traitPredicateIri("target")`
- `traitPredicateIri("for")`

If a governing schema uses different reference trait names, derived validation artifact generation MUST fail.

`ReferenceConstraint(type=ReferenceSingleton)` MUST be expressible in derived validation artifacts.

If projected into a SHACL-derived artifact, it MUST be expressible (for example, via SHACL-SPARQL or equivalent core constraints) and MUST report a violation when more than one reference-trait predicate is present on the same focus node.

`ReferenceConstraint(type=ReferenceTraitAllowed)` is underspecified unless the constraint specifies which reference trait is allowed.

Therefore, derived validation artifact generation MUST fail for `ReferenceTraitAllowed` unless the constraint provides an additional trait `traitName` whose value is one of `reference`, `target`, or `for`.

#### 9.9.10 Reference Constraints (Deterministic Resolution and Targets)

Some reference constraints require deterministically resolving reference values to an IRI.

For the purposes of reference constraints, a reference value `v` MUST be one of:

- an IRI (RDF IRI term), or
- a Lookup Token typed literal with datatype `urn:cdx:value-type:LookupToken`.

Given a reference value `v`, its resolved IRI `r` MUST be computed as follows:

- If `v` is an IRI, then `r = v`.
- If `v` is a Lookup Token typed literal, then:
	- If there exists exactly one binding entry in the lookup binding table such that the binding entry's `tokenLiteral` is `v`, and the binding entry's `targetIri` is `r`, then `r` is that bound `targetIri`.
	- Otherwise, `v` MUST be treated as unresolved.
- Otherwise, `v` MUST be treated as unresolved.

Derived validation artifacts MUST NOT guess a resolution for an unresolved reference value.

Derived validation artifacts MUST support `ReferenceConstraint(type=ReferenceTargetsEntity)`.

`ReferenceTargetsEntity` MUST mean:

- For each reference-trait predicate `p` in the reference-trait predicate set and for each value `v` on the focus node where `(focusVar, p, v)` holds, compute the resolved IRI `r`.
- A violation MUST be reported if `v` is treated as unresolved.
- A violation MUST be reported unless there exists a node `n` in the same Document such that:
	- `(n, codex:declaredId, r)` holds, and
	- `(n, codex:isEntity, "true"^^xsd:boolean)` holds.

#### 9.9.11 Reference Constraints (Targets a Concept)

Derived validation artifacts MUST support `ReferenceConstraint(type=ReferenceTargetsConcept, conceptSelector=X)`.

`ReferenceTargetsConcept` MUST mean:

- For each reference-trait predicate `p` in the reference-trait predicate set and for each value `v` on the focus node where `(focusVar, p, v)` holds, compute the resolved IRI `r`.
- A violation MUST be reported if `v` is treated as unresolved.
- A violation MUST be reported unless there exists a node `n` in the same Document such that:
	- `(n, codex:declaredId, r)` holds, and
	- `(n, rdf:type, conceptClassIri(X))` holds.

#### 9.9.12 Reference Constraints (Must Resolve)

Derived validation artifacts MUST support `ReferenceConstraint(type=ReferenceMustResolve)`.

`ReferenceMustResolve` MUST mean:

- For each reference-trait predicate `p` in the reference-trait predicate set and for each value `v` on the focus node where `(focusVar, p, v)` holds, compute the resolved IRI `r`.
- A violation MUST be reported if `v` is treated as unresolved.
- A violation MUST be reported unless there exists a node `n` in the same Document such that `(n, codex:declaredId, r)` holds.

If a derived validation artifact is produced as an RDF graph (including a SHACL graph), the projection to a concrete RDF syntax MUST be exactly:

1. Validate the derived `RdfGraph` against the derived-artifact structural rules.
2. Emit the triples in a chosen RDF concrete syntax (for example, Turtle).

The projection MUST NOT change the set of triples.

### 9.10 Failure Rules (No Guessing)

Schema processing, schema-driven validation, instance-graph mapping, and derived-artifact projection MUST fail rather than guess when required information is missing or ambiguous.

At minimum, processing MUST fail in any of the following cases:

- the schema authoring profile is missing, invalid, or mixed (see §9.4)
- a schema rule requires semantics not explicitly defined by this specification, the governing schema, or the schema-definition specification
- a required external input is missing
- an algorithm would require nondeterministic choice (including heuristic inference or “best effort”)
- a lookup token is required to resolve but does not have exactly one binding
- a derived validation artifact cannot be constructed without inventing missing definitions

### 9.11 Layer A → Layer B Expansion Algorithm (Total)

This section defines a deterministic, total expansion algorithm from Profile A (Layer A) schema authoring to canonical Layer B (`RdfGraph`) suitable for derived validation artifacts (including SHACL and SHACL-SPARQL).

The expansion algorithm is normative.

#### 9.11.1 Inputs and Output

Input: a Layer A schema document `S`.

Output: a Layer B `RdfGraph` containing a SHACL graph.

#### 9.11.2 Preconditions

The expansion MUST fail if any of the following hold:

- The schema is not valid under the schema-of-schemas.
- Any `ConceptDefinition` lacks an `id`.
- Any required selector (concept name, trait name, validator name) cannot be resolved to a unique definition.
- Any rule produces a semantic constraint that cannot be expressed under the instance graph mapping defined in §9.7.

#### 9.11.3 Expansion Steps

1. Compute `schemaIri` as the governing schema's `Schema.id` value.
2. For each `ConceptDefinition` in `S`, compute:
	- `K = conceptClassIri(X)` where `X` is the concept name
	- `NS = nodeShapeIri(K)`
3. Emit SHACL node shape triples for each concept definition:
	- `(NS, rdf:type, sh:NodeShape)`
	- `(NS, sh:targetClass, K)`
4. Expand TraitRules into property shapes (§9.11.4).
5. Expand ChildRules into property shapes (§9.11.5).
6. Expand ConstraintDefinitions into SHACL constraints (§9.11.6).
7. Canonicalize the resulting `RdfGraph` (§9.6).

#### 9.11.4 TraitRules → SHACL Property Shapes

For each trait rule attached to a concept definition with node shape IRI `NS`, let `t` be the trait name string.

The expansion MUST emit one SHACL property shape node `PS` with:

- `(NS, sh:property, PS)`
- `(PS, rdf:type, sh:PropertyShape)`
- `(PS, sh:path, traitPredicateIri(t))`

`PS` MUST be `propertyShapeIri(NS, t)`.

Cardinality mapping:

- `RequiresTrait` MUST emit `(PS, sh:minCount, "1"^^xsd:integer)`.
- `ForbidsTrait` MUST emit `(PS, sh:maxCount, "0"^^xsd:integer)`.

Value type mapping:

- If Layer A declares a value type token that maps to an RDF datatype IRI, the expansion MUST emit `(PS, sh:datatype, datatypeIri)`.
- If Layer A constrains by enumerated set, the expansion MUST emit `(PS, sh:in, listNodeIri)` and MUST emit the RDF list structure using deterministic skolem IRIs (see §9.6.3).

Any value-type token without a defined mapping MUST cause expansion failure.

#### 9.11.5 ChildRules → SHACL Property Shapes

For each allowed/required/forbidden child relationship declared on a concept definition with node shape IRI `NS` and concept class IRI `K`, let `Q = conceptClassIri(X)` for the selected child concept name `X`.

The expansion MUST emit one SHACL property shape node `PS` with:

- `(NS, sh:property, PS)`
- `(PS, rdf:type, sh:PropertyShape)`
- `(PS, sh:path, childPredicateIri(K, Q))`

`PS` MUST be `propertyShapeIri(NS, Q)`.

Child presence mapping:

- `RequiresChildConcept` MUST emit `(PS, sh:minCount, "1"^^xsd:integer)`.
- `ForbidsChildConcept` MUST emit `(PS, sh:maxCount, "0"^^xsd:integer)`.

If Layer A restricts child type, the expansion MUST emit `(PS, sh:class, Q)`.

#### 9.11.6 ConstraintDefinitions → SHACL Constraints

ConstraintDefinitions MUST expand to SHACL constraints.

##### 9.11.6.1 General Rule

Each Codex constraint type permitted by the schema-definition specification MUST map to either:

- a SHACL Core constraint expression, or
- a SHACL-SPARQL constraint (`sh:sparql`).

If a constraint type cannot be expressed without inventing semantics not defined by this specification and the schema-definition specification, expansion MUST fail.

Atomic constraint mappings that are defined by this specification MUST follow §9.9.

##### 9.11.6.2 Rule Algebra → SHACL-SPARQL (Total)

This section defines a total mapping for the rule algebra elements:

- `AllOf`
- `AnyOf`
- `Not`
- `ConditionalConstraint` (`When` / `Then`)

This mapping is total in the sense that it provides a deterministic SHACL-SPARQL construction for any rule algebra tree.

If the rule algebra tree contains an atomic constraint whose required mapping is undefined, expansion MUST fail.

###### 9.11.6.2.1 Canonical SPARQL Form

For any `ConstraintDefinition`, expansion MUST emit exactly one SHACL-SPARQL constraint query per target shape.

The query MUST be a `SELECT` query that returns one row per violating focus node using the SHACL-SPARQL convention:

- The focus node variable MUST be `?this`.
- A row returned by the query MUST indicate a violation.

The query MUST have the following canonical structure:

```
SELECT DISTINCT ?this
WHERE {
	<TARGET_BINDING>
	FILTER( !( <HOLD_EXPR> ) )
}
```

`<TARGET_BINDING>` MUST bind `?this` to the set of focus nodes implied by the constraint's targets.

One conforming target binding is:

- For a concept target with concept name `X`: `?this rdf:type <conceptClassIri(X)> .`
- For `TargetContext contextSelector="Document"`: `FILTER( ?this = <documentBaseIri> ) .`

`<documentBaseIri>` denotes the IRI term whose value is the required external input `documentBaseIri`.

If target binding cannot be expressed without ambiguity (for example, the target selector is not resolvable), expansion MUST fail.

`<HOLD_EXPR>` MUST be computed by the function `H(rule, ctx, focusVar)` defined below, with `focusVar` set to `?this`.

###### 9.11.6.2.2 Deterministic Variable Allocation

Atomic constraints and path/quantifier expressions often require internal SPARQL variables.

To avoid accidental capture and to make the output canonical, expansion MUST allocate internal variable names deterministically.

Expansion MUST walk the rule tree in pre-order.

For the k-th node visited (1-indexed), the expansion context `ctx` MUST define a node-local suffix `k`.

Any internal variable introduced while translating that node MUST be named by appending `k` to a base name.

Examples:

- `?v1`, `?v2`, ... for values
- `?c1`, `?c2`, ... for child nodes

Variables introduced for one rule node MUST NOT be referenced outside the `EXISTS { ... }` block created for that node.

###### 9.11.6.2.3 The `H(rule, ctx, focusVar)` Function

`H(rule, ctx, focusVar)` returns a SPARQL boolean expression that evaluates to true exactly when the rule holds for the current focus node.

If `focusVar` is omitted, it MUST be `?this`.

`H(rule, ctx, focusVar)` MUST be computed as follows.

**AllOf**

If `rule` is `AllOf` with child rules `r1..rn`, then:

- `H(rule, ctx, focusVar) = H(r1, ctx1, focusVar) && H(r2, ctx2, focusVar) && ... && H(rn, ctxn, focusVar)`

where `ctxi` are derived by continuing the deterministic pre-order traversal.

**AnyOf**

If `rule` is `AnyOf` with child rules `r1..rn`, then:

- `H(rule, ctx, focusVar) = H(r1, ctx1, focusVar) || H(r2, ctx2, focusVar) || ... || H(rn, ctxn, focusVar)`

**Not**

If `rule` is `Not` with exactly one child rule `r`, then:

- `H(rule, ctx, focusVar) = !H(r, ctx1, focusVar)`

**ConditionalConstraint**

If `rule` is `ConditionalConstraint` with condition rule `w` (under `When`) and consequent rule `t` (under `Then`), then:

- `H(rule, ctx, focusVar) = (!H(w, ctxW, focusVar)) || H(t, ctxT, focusVar)`

This is logically equivalent to: if the condition holds, the consequent must hold.

###### 9.11.6.2.4 Atomic Rules as `EXISTS` Blocks

If `rule` is atomic, `H(rule, ctx, focusVar)` MUST be a SPARQL `EXISTS { ... }` form or an `EXISTS`-free boolean constant.

For atomic rules whose SHACL Core mapping is defined in §9.9, expansion MUST ALSO define `H(rule, ctx, focusVar)` using only SPARQL 1.1 constructs.

If an atomic rule cannot be expressed as a SPARQL boolean expression without inventing additional semantics, expansion MUST fail.

For atomic rules mapped in §9.9, a conforming `H` translation includes at minimum:

- `TraitExists(trait=t)`: `EXISTS { focusVar <traitPredicateIri(t)> ?vK }`
- `TraitMissing(trait=t)`: `!EXISTS { focusVar <traitPredicateIri(t)> ?vK }`
- `TraitEquals(trait=t, value=v)`: `EXISTS { focusVar <traitPredicateIri(t)> <valueTerm(v)> }`

Here `?vK` MUST follow the deterministic variable allocation rule in §9.11.6.2.2.

###### 9.11.6.2.5 One-Way Representation Rule

When a `ConstraintDefinition` uses rule algebra (i.e., contains `AllOf`, `AnyOf`, `Not`, or `ConditionalConstraint` anywhere in its rule tree), expansion MUST express that constraint definition using SHACL-SPARQL only.

Expansion MUST NOT additionally emit independent SHACL Core constraints for the same `ConstraintDefinition`.

Rationale: emitting both creates multiple ways to say the same thing and risks divergence between engines.

##### 9.11.6.3 Paths and Quantifiers → SHACL-SPARQL (Total)

This section defines a total mapping for:

- `TraitPath`, `ChildPath`, `DescendantPath`, `ContentPath`
- `OnPathExists`, `OnPathForAll`, `OnPathCount`

These operators MUST be expressed using SHACL-SPARQL.

###### 9.11.6.3.1 Path Binding Function

Define a function `B(path, focusVar, outVar)` that emits a SPARQL graph pattern which binds `outVar` to each element selected by `path` from `focusVar`.

`B` MUST be computed as follows.

**TraitPath**

For `TraitPath traitName=t`:

```
focusVar <traitPredicateIri(t)> outVar .
```

**ChildPath**

For `ChildPath conceptSelector=X`:

```
outVar <codex:parentNode> focusVar .
outVar rdf:type <conceptClassIri(X)> .
```

**DescendantPath**

For `DescendantPath conceptSelector=X`:

```
outVar <codex:parentNode>+ focusVar .
outVar rdf:type <conceptClassIri(X)> .
```

**ContentPath**

For `ContentPath`:

```
focusVar <codex:content> outVar .
```

If `conceptSelector` cannot be resolved to a unique `ConceptDefinition`, expansion MUST fail.

###### 9.11.6.3.2 Quantifier Semantics

Each `OnPath*` node scopes a nested rule over the set of elements produced by `B`.

Let `path` be its `Path` child.

Let `r` be its nested `Rule` child.

Let `xVar` be the deterministically allocated variable for the bound element.

The nested rule MUST be evaluated with `focusVar` set to `xVar`.

**OnPathExists**

`OnPathExists(path, r)` MUST translate to:

```
EXISTS {
	B(path, focusVar, xVar)
	FILTER( H(r, ctxChild, xVar) )
}
```

**OnPathForAll**

`OnPathForAll(path, r)` MUST translate to:

```
!EXISTS {
	B(path, focusVar, xVar)
	FILTER( !H(r, ctxChild, xVar) )
}
```

**OnPathCount**

`OnPathCount(path, r, minCount=m?, maxCount=n?)` MUST translate to a COUNT aggregate over elements that satisfy `r`.

If both `minCount` and `maxCount` are absent, expansion MUST fail.

It MUST translate to a boolean expression of the form:

```
(
	SELECT (COUNT(?xVar) AS ?countK)
	WHERE {
		B(path, focusVar, xVar)
		FILTER( H(r, ctxChild, xVar) )
	}
)
```

combined with comparisons:

- if `minCount` is present: `?countK >= m`
- if `maxCount` is present: `?countK <= n`

`?countK` MUST follow the deterministic variable allocation rule in §9.11.6.2.2.

##### 9.11.6.4 SPARQL Constraint Shape

When a constraint is expressed using SHACL-SPARQL, the expansion MUST emit:

Let `targetShapeIri` be the node shape IRI the constraint is applied to (for example, `nodeShapeIri(conceptClassIri(X))` for a concept target or `documentNodeShapeIri` for the Document context).

- `(targetShapeIri, sh:sparql, sparqlConstraintIri)`
- `(sparqlConstraintIri, sh:select, selectTextLiteral)`

If the source constraint has a `title` or `description`, the expansion MAY emit `sh:message`.

The SPARQL query MUST be deterministic given the source constraint.

##### 9.11.6.5 Pattern Constraints (SPARQL 1.1 REGEX)

For the pattern-bearing constraints (`ValueMatchesPattern`, `PatternConstraint`, `ContentMatchesPattern`), the expansion MUST use SPARQL 1.1 `REGEX` semantics.

If `flags` is present, it MUST be projected to `sh:flags` when using `sh:pattern`, and it MUST be passed as the third argument to `REGEX` when using `sh:sparql`.

##### 9.11.6.6 `ValueIsValid` via Explicit `ValidatorDefinition`

For `ValueIsValid validatorName=$X`, expansion MUST:

1. Resolve `$X` to exactly one `ValidatorDefinition` in the schema.
2. Embed the `ValidatorDefinition` content into a SHACL-SPARQL constraint.

If the validator cannot be resolved uniquely, expansion MUST fail.

The embedding contract MUST be purely textual and deterministic.

One conforming contract is:

- The validator content MUST be a SPARQL `SELECT` query string whose results follow the SHACL-SPARQL convention (returning a row per violation with `?this`).

The derived `sh:select` string MUST be exactly the validator content.

---

## 10. Formatting and Canonicalization

### 10.1 Purpose

This section defines how Codex documents are:

- formatted
- canonicalized
- rejected when canonicalization is not possible

Its goals are to:

- ensure exactly one canonical surface form
- ensure formatting/canonicalization conforms to the language invariants (§2), including the prohibition of heuristics
- enable mechanical, explainable normalization
- support lossless round-tripping

This section governs formatting and canonicalization only.

### 10.2 Processing Phases (Normative)

Codex supports two related pipelines:

1. Schema-less formatting / well-formedness check (no schema required)
2. Semantic validation (schema required)

Formatting and canonicalization are not optional in the full pipeline.
However, schema availability is required only for semantic validation.

#### 10.2.1 Schema-Less Formatting Mode (Required) (Normative)

An implementation MUST provide a schema-less formatting / canonicalization mode that can be run without a governing schema.

This mode exists to support well-formedness and formatting checks (gofmt-like), independent of semantic validation.

If provided, a schema-less formatter:

- MUST NOT claim that its output is valid under any schema
- MUST NOT report schema/semantic error classes (e.g., `SchemaError`, `IdentityError`, `ReferenceError`, `ConstraintError`)
- MUST normalize encoding and line endings as defined by the surface form requirements (§8)
- MUST apply the canonical form requirement defined in §10.4
- MAY normalize whitespace, blank-line layout, trait layout, and annotation whitespace

Schema-less formatting is not validation. It exists to produce a consistent surface form without consulting schema meaning.

#### 10.2.2 Full Validation Pipeline (Normative)

To validate a document under a schema, a conforming tool MUST follow this sequence:

1. Decode + newline normalization
2. Formatting + canonicalization (mandatory) — using the schema-less mode defined in §10.2.1
3. Schema resolution — obtain the governing schema for the document (§12)
4. Semantic validation — schema rule evaluation (constraints, cardinality, identity, references)

Schema resolution is required before semantic validation.

### 10.3 Parse Errors vs Formatting Errors (Normative)

#### 10.3.1 Parse Errors

During formatting + canonicalization, a failure MUST be classified as `ParseError` (§14) when input cannot be read into the syntactic structure required to produce a parsed document model (AST) under the governing schema.

#### 10.3.2 Formatting Errors

During formatting + canonicalization, a failure MUST be classified as `FormattingError` (§14) when input can be structurally read, but cannot be transformed into canonical surface form deterministically.

`FormattingError` is distinct from schema or semantic error classes.

### 10.4 Canonical Form Requirement (Normative)

Every valid Codex document MUST normalize to exactly one canonical textual form.

Canonicalization:

- is deterministic
- is mechanical
- preserves meaning and Content
- never guesses author intent

If canonicalization cannot be performed unambiguously, the document is invalid.

### 10.5 Canonicalization Rules (Normative)

Canonicalization includes, at minimum:

- canonical encoding and newline normalization (§8)
- deterministic indentation
- no trailing whitespace on lines
- no trailing blank lines at end of file
- exactly one blank line between sibling Concepts
- canonical spacing of Traits
- canonical Trait layout (1–2 Traits on one line; 3+ Traits on separate lines)
- canonical placement of self-closing markers
- canonical inline-annotation whitespace collapse
- canonical string escaping
- preservation of Concept, Trait, and Content order

Canonicalization MUST NOT:

- reorder Concepts
- reorder Traits
- invent or remove Concepts, Traits, or Content
- infer missing structure

### 10.6 Annotation Canonicalization (Normative)

Annotation canonicalization MUST follow the surface form requirements (§8).

In particular:

- Inline annotations collapse internal whitespace to single spaces and trim leading/trailing whitespace (as described in §8)
- Block annotations preserve internal line structure
- Block annotations with `CODE:` or `MARKDOWN:` directives are byte-preserving: tools MUST NOT reindent, trim, strip trailing whitespace, wrap, or interpret escapes within those blocks

If attachment cannot be determined deterministically, canonicalization MUST fail.

### 10.7 Allowed vs Forbidden Changes (Normative)

The formatter/canonicalizer exists to produce a single canonical surface form without changing meaning.

Allowed changes (examples):

- Normalize newlines to LF and ensure a trailing newline
- Normalize structural indentation (tabs) for Concept markers and children bodies
- Canonicalize trait layout/spacing without reordering traits
- Canonicalize inline annotation whitespace (trim + internal collapse)
- Canonicalize grouping-annotation labels by whitespace normalization
- Normalize UUID spelling (e.g., hex lowercase) where explicitly specified

Forbidden changes (examples):

- Reorder Concepts or Traits
- Change Content bytes
- Change any bytes inside `CODE:` or `MARKDOWN:` block annotations
- Guess annotation attachment or reinterpret annotation kinds
- Invent, remove, or rename Concepts/Traits/Values

### 10.8 Normalization Failures (Normative)

A canonicalization failure occurs when:

- indentation is ambiguous
- annotation attachment is ambiguous
- whitespace cannot be normalized without changing meaning
- structural inconsistencies prevent a unique surface form

Canonicalization failures MUST be classified as `FormattingError` (§14).

### 10.9 Formatting vs Schema Errors (Normative)

Mandatory distinction:

- Formatting errors concern how Codex is written
- Schema errors concern what Codex means

Tools MUST NOT report schema errors when the root cause is a formatting failure.

### 10.10 Error Classification (Normative)

Formatting and canonicalization failures MUST be classified as:

```
FormattingError
```

They MUST NOT be downgraded to warnings.

### 10.11 Prohibited Behaviors (Normative)

Codex tools MUST NOT:

- silently normalize invalid input
- auto-correct formatting errors without reporting them
- accept multiple canonical forms
- discard or rewrite Content
- depend on source offsets or editor state

### 10.12 Reporting Requirements

Formatting error reports SHOULD include:

- error class (`FormattingError`)
- violated rule
- location (line number or Concept path)
- explanation of canonicalization failure

Exact wording is tool-defined.

### 10.13 Non-Goals

This section does not:

- define editor behavior
- prescribe auto-format-on-save policies
- define diff or patch semantics
- define schema validation rules
- define rendering or execution behavior

### 10.14 Summary

- Canonical surface form is mandatory
- Canonicalization is mechanical and deterministic
- Formatting failures are classified as `FormattingError` (§14)
- No heuristic or best-effort formatting is permitted
- Formatting is separate from schema validation

---

## 11. Schema Definition Language

This section normatively defines the schema definition language for Codex 1.0.0.

It specifies how **schemas themselves are authored in Codex**, including:

* Concept definitions
* Trait definitions
* Content, child, trait, and collection rules
* Enumerated value sets
* Entity eligibility
* Declarative constraints
* Schema versioning and compatibility

This content is **Normative**.

---

#### 1. Purpose

This specification defines the **authoritative ontology for Codex schemas**.

Its goals are to:

* make schemas **first-class Codex data**
* enable validation consistent with the Codex language invariants
* allow schemas to validate other schemas (bootstrapping)
* ensure interoperability across tools and implementations
* support compilation to external validation systems (e.g., SHACL)

The Codex language invariants governing meaning, closed-world semantics,
determinism, and prohibition of heuristics are defined by this specification (see §9).

The schema-language itself is bootstrapped by a built-in **bootstrap schema-of-schemas**.
See §12.4.

---

#### 2. Core Principles (Normative)

* Schemas are **declarative data**, not executable programs
* All authorization is **explicit**
* All constraints are **mechanically enforceable**
* Schema validation semantics MUST satisfy the Codex language invariants (see §9)

---

#### 3. Schema

##### 3.1 `Schema`

A `Schema` Concept defines a schema.

###### Traits (Normative)

* `id` (required; IRI reference)
* `version` (required; string)
* `compatibilityClass` (required; `$BackwardCompatible | $ForwardCompatible | $Breaking`)
* `title` (optional; string)
* `description` (optional; string)

###### Children (Normative)

A `Schema` MAY contain, in any order:

* `ConceptDefinitions`
* `TraitDefinitions`
* `EnumeratedValueSets`
* `ConstraintDefinitions`
* `ValueTypeDefinitions` (optional)

---

#### 4. Concept Definitions

##### 4.1 `ConceptDefinition`

Defines a Codex Concept.

A `ConceptDefinition` is itself an Entity.

###### Traits (Normative)

* `id` (required; IRI reference)
* `key` (optional; lookup token)
* `name` (required; Concept name string per the Naming and Value Specification (`spec/0.1/naming-and-values/index.md`))
* `conceptKind` (required; `$Semantic | $Structural | $ValueLike`)
* `entityEligibility` (required; `$MustBeEntity | $MayBeEntity | $MustNotBeEntity`)

###### Children (Normative)

* `ContentRules` (optional)
* `TraitRules` (optional)
* `ChildRules` (optional)
* `CollectionRules` (optional)

---

##### 4.2 `ContentRules`

Declares whether a Concept allows content.

A Concept's content mode determines how the parser handles its body. This is essential for schema-first parsing.

###### Children (Normative)

Exactly one of:

* `AllowsContent` — Concept body is opaque content (content mode)
* `ForbidsContent` — Concept body contains children or is empty (children mode)

###### Defaults

If `ContentRules` is omitted, `ForbidsContent` is assumed.

###### Parser Implication

The parser MUST consult `ContentRules` to determine content mode before parsing
the Concept body. See §12.

###### Example

```cdx
<ConceptDefinition
	id=example:concept:Description
	name="Description"
	conceptKind=$Semantic
	entityEligibility=$MustNotBeEntity
>
	<ContentRules>
		<AllowsContent />
	</ContentRules>
</ConceptDefinition>
```

---

##### 4.3 `TraitRules`

Declares which Traits a Concept allows, requires, or forbids.

###### Children (Normative)

Zero or more of:

* `RequiresTrait` — Trait MUST be present
* `AllowsTrait` — Trait MAY be present
* `ForbidsTrait` — Trait MUST NOT be present

###### `RequiresTrait`

####### Traits

* `name` (required; Trait name string per the Naming and Value Specification (`spec/0.1/naming-and-values/index.md`))

###### `AllowsTrait`

####### Traits

* `name` (required; Trait name string per the Naming and Value Specification (`spec/0.1/naming-and-values/index.md`))

###### `ForbidsTrait`

####### Traits

* `name` (required; Trait name string per the Naming and Value Specification (`spec/0.1/naming-and-values/index.md`))

###### Defaults

Traits not listed are forbidden by default. A Concept with no `TraitRules` allows no Traits (except `id` and `key` which are governed by `entityEligibility`).

###### Example

```cdx
<TraitRules>
	<RequiresTrait name="amount" />
	<AllowsTrait name="unit" />
	<AllowsTrait name="optional" />
</TraitRules>
```

---

##### 4.4 `ChildRules`

Declares which child Concepts are allowed under a Concept.

###### Children (Normative)

Zero or more of:

* `AllowsChildConcept` — child Concept MAY appear
* `RequiresChildConcept` — child Concept MUST appear (alias for min=1)
* `ForbidsChildConcept` — child Concept MUST NOT appear

###### `AllowsChildConcept`

####### Traits

* `conceptSelector` (required; Concept name as string)
* `min` (optional; non-negative integer, default 0)
* `max` (optional; positive integer, omit for unbounded)

###### `RequiresChildConcept`

####### Traits

* `conceptSelector` (required; Concept name as string)
* `min` (optional; positive integer, default 1)
* `max` (optional; positive integer, omit for unbounded)

Note: `RequiresChildConcept` is semantically equivalent to `AllowsChildConcept` with `min=1`. It exists for clarity.

###### `ForbidsChildConcept`

####### Traits

* `conceptSelector` (required; Concept name as string)

###### Defaults

Child Concepts not listed are forbidden by default.

###### Example

```cdx
<ChildRules>
	<AllowsChildConcept conceptSelector="Title" />
	<AllowsChildConcept conceptSelector="Description" />
	<RequiresChildConcept conceptSelector="Ingredients" />
	<AllowsChildConcept conceptSelector="Instructions" min=1 />
</ChildRules>
```

---

##### 4.5 `CollectionRules`

Declares collection semantics for a Concept that acts as a container.

`CollectionRules` is used when a Concept's children represent a logical collection (e.g., a list of ingredients, a set of tags). The semantics inform validation and graph compilation.

###### Traits (Normative)

* `ordering` (required; `$Ordered | $Unordered`)
* `allowsDuplicates` (required; boolean)

###### Form

`CollectionRules` is self-closing (no children).

###### Example

```cdx
<ConceptDefinition
	id=example:concept:Ingredients
	name="Ingredients"
	conceptKind=$Structural
	entityEligibility=$MustNotBeEntity
>
	<ContentRules>
		<ForbidsContent />
	</ContentRules>
	<ChildRules>
		<AllowsChildConcept conceptSelector="Ingredient" />
	</ChildRules>
	<CollectionRules ordering=$Unordered allowsDuplicates=true />
</ConceptDefinition>
```

---

#### 5. Trait Definitions

##### 5.1 `TraitDefinition`

Defines a Trait independently of any Concept.

Trait definitions establish the value type, cardinality, and constraints for a Trait that may be used across multiple Concepts.

###### Traits (Normative)

* `id` (optional; IRI reference)
* `name` (required; Trait name string per the Naming and Value Specification (`spec/0.1/naming-and-values/index.md`))
* `defaultValueType` (required unless `defaultValueTypes` is provided; value type token)
* `defaultValueTypes` (required unless `defaultValueType` is provided; list of one or more value type tokens)
* `cardinality` (required; `$Single | $List`)
* `itemValueType` (required if `cardinality=$List`; value type token)
* `isReferenceTrait` (optional; boolean)
* `priority` (optional; enumerated token; presentation hint)

If both `defaultValueType` and `defaultValueTypes` are provided, the implementation MUST treat that as a schema error.

`priority` is a meta-schema concern. Implementations MUST NOT use `priority` to change validation or compilation semantics. Meta-schemas MAY constrain allowed `priority` values (e.g., `$Primary`, `$Secondary`).

###### Children (Optional)

* `AllowedValues` — constrains the set of valid values

###### Example

```cdx
<TraitDefinition
	name="amount"
	defaultValueType=$Number
	cardinality=$Single
/>

<TraitDefinition
	name="unit"
	defaultValueType=$EnumeratedToken
	cardinality=$Single
>
	<AllowedValues>
		<ValueIsOneOf values=[$Grams, $Kilograms, $Milliliters, $Liters, $Units] />
	</AllowedValues>
</TraitDefinition>
```

---

##### 5.2 `AllowedValues`

Constrains the values a Trait may accept.

###### Children (Normative)

One or more value constraints:

* `ValueIsOneOf` — value must be in explicit list
* `EnumeratedConstraint` — value must be member of named enumeration

###### `ValueIsOneOf`

####### Traits

* `values` (required; list of allowed values)

###### `EnumeratedConstraint`

####### Traits

* `set` (required; name of an `EnumeratedValueSet`)

---

#### 6. Value Types

##### 6.1 Built-in Value Type Tokens (Normative)

Schemas MAY reference the following built-in value types:

* `$String`
* `$Char`
* `$Boolean`
* `$Number`
* `$Integer`
* `$EnumeratedToken`
* `$IriReference`
* `$LookupToken`
* `$Uuid`
* `$Color`
* `$Temporal`
* `$Date`
* `$YearMonth`
* `$MonthDay`
* `$LocalDateTime`
* `$ZonedDateTime`
* `$Duration`
* `$List`
* `$Set`
* `$Map`
* `$Tuple`
* `$Range`

Schemas MAY also define additional value type tokens via `ValueTypeDefinition` (see §6.2). These schema-defined value type tokens are referenced as enumerated tokens using the `name` (e.g., a `ValueTypeDefinition name="NumericRange" ...` is referenced as `$NumericRange`).

---

##### 6.2 `ValueTypeDefinition` (Optional)

Defines a named value type with custom validation.

###### Container

`ValueTypeDefinitions` is a container Concept holding one or more `ValueTypeDefinition` children.

###### Traits

* `id` (optional; IRI reference)
* `name` (required; Concept name string per the Naming and Value Specification (`spec/0.1/naming-and-values/index.md`))
* `baseValueType` (required; built-in value type token)
* `validatorName` (optional; enumerated token identifying a validator)

---

##### 6.3 Enumerated Value Sets

Schemas MAY define named sets of enumerated values.

###### Container

`EnumeratedValueSets` is a container Concept holding one or more `EnumeratedValueSet` children.

###### `EnumeratedValueSet`

Defines a named set of valid enumerated tokens.

####### Traits

* `name` (required; Concept name string per the Naming and Value Specification (`spec/0.1/naming-and-values/index.md`))

####### Children

One or more `Member` children.

###### `Member`

Defines a single member of an enumerated value set.

####### Traits

* `value` (required; string matching the token name without `$` prefix)
* `label` (optional; human-readable display string)
* `description` (optional; explanatory string)

###### Example

```cdx
<EnumeratedValueSets>
	<EnumeratedValueSet name="MeasurementUnit">
		<Member value="Grams" label="Grams" />
		<Member value="Kilograms" label="Kilograms" />
		<Member value="Milliliters" label="Milliliters" />
		<Member value="Liters" label="Liters" />
		<Member value="Units" label="Units" description="Countable items" />
	</EnumeratedValueSet>
</EnumeratedValueSets>
```

Usage:

```cdx
<TraitDefinition name="unit" defaultValueType=$EnumeratedToken cardinality=$Single>
	<AllowedValues>
		<EnumeratedConstraint set="MeasurementUnit" />
	</AllowedValues>
</TraitDefinition>
```

---

##### 6.4 Built-in Enumerated Value Sets (Normative)

The following enumerated value sets are defined by the language and MUST be recognized by all implementations.

###### ConceptKind

Describes the semantic role of a Concept.

* `$Semantic` — carries domain meaning; may become graph nodes
* `$Structural` — organizes or groups other Concepts; typically not graph nodes
* `$ValueLike` — represents a value-like construct

###### EntityEligibility

Governs whether Concept instances may or must have identity.

* `$MustBeEntity` — instances MUST declare an `id` Trait
* `$MayBeEntity` — instances MAY declare an `id` Trait
* `$MustNotBeEntity` — instances MUST NOT declare an `id` Trait

###### CompatibilityClass

Declares schema version compatibility.

* `$BackwardCompatible` — existing valid data remains valid
* `$ForwardCompatible` — data authored for new version may validate under older
* `$Breaking` — migration required; existing data may become invalid

###### Ordering

Declares collection ordering semantics.

* `$Ordered` — child order is significant and preserved
* `$Unordered` — child order is not significant

###### Cardinality

Declares Trait value cardinality.

* `$Single` — exactly one value
* `$List` — zero or more values

---

### 11.7. Constraint Model

#### 11.7.1 `ConstraintDefinitions`

Container for constraint definitions within a schema.

##### Children

One or more `ConstraintDefinition` children.

---

#### 11.7.2 `ConstraintDefinition`

Defines a reusable, named constraint.

##### Traits (Normative)

* `id` (required; IRI reference)
* `title` (optional; string)
* `description` (optional; string)

##### Children (Normative)

* `Targets` (required) — what the constraint applies to
* `Rule` (required) — the constraint logic

---

#### 11.7.3 `Targets`

Declares what a constraint applies to.

##### Children (Normative)

One or more of:

* `TargetConcept` — constraint applies to instances of a Concept
* `TargetContext` — constraint applies within a context

##### `TargetConcept`

###### Traits

* `conceptSelector` (required; Concept name as string)

##### `TargetContext`

###### Traits

* `contextSelector` (required; Concept name or `"Document"`)

---

#### 11.7.4 `Rule`

Contains the constraint logic.

A `Rule` MUST contain exactly one constraint or composition element.

---

### 11.8. Rule Algebra (Normative)

#### 11.8.1 Composition Rules

Composition rules combine other rules.

##### `AllOf`

All child rules must hold.

###### Children

Two or more `Rule` children.

##### `AnyOf`

At least one child rule must hold.

####### Children

Two or more `Rule` children.

###### `Not`

The child rule must not hold.

###### Children

Exactly one `Rule` child.

###### `ConditionalConstraint`

If a condition holds, a consequent must hold.

###### Children

* `When` — contains the condition (one `Rule` child)
* `Then` — contains the consequent (one `Rule` child)

---

### 11.9. Paths and Quantifiers

#### 11.9.1 Paths

Constraints MAY reference data using paths:

* `TraitPath` — references a Trait value
	* `traitName` (required; Trait name string per the Naming and Value Specification (`spec/0.1/naming-and-values/index.md`))
* `ChildPath` — references direct children
  * `conceptSelector` (required; Concept name)
* `DescendantPath` — references descendants at any depth
  * `conceptSelector` (required; Concept name)
* `ContentPath` — references Content (no traits)

---

#### 11.9.2 Quantifiers

Quantifiers scope constraints over collections.

* `Exists` — at least one element satisfies the rule
* `ForAll` — all elements satisfy the rule
* `Count` — count of elements satisfies bounds
  * `minCount` (optional; non-negative integer)
  * `maxCount` (optional; positive integer)

Quantifiers are structural and deterministic.

---

### 11.10. Atomic Constraints (Normative)

Atomic constraints are the leaves of the rule algebra.

#### 11.10.1 Trait Constraints

##### `TraitExists`

Trait is present on the Concept.

###### Traits

* `trait` (required; Trait name string per the Naming and Value Specification (`spec/0.1/naming-and-values/index.md`))

##### `TraitMissing`

Trait is absent from the Concept.

###### Traits

* `trait` (required; Trait name string per the Naming and Value Specification (`spec/0.1/naming-and-values/index.md`))

##### `TraitEquals`

Trait has a specific value.

###### Traits

* `trait` (required; Trait name string per the Naming and Value Specification (`spec/0.1/naming-and-values/index.md`))
* `value` (required; the expected value)

##### `TraitCardinality`

Trait value count is within bounds.

###### Traits

* `trait` (required; Trait name string per the Naming and Value Specification (`spec/0.1/naming-and-values/index.md`))
* `min` (optional; non-negative integer)
* `max` (optional; positive integer)

##### `TraitValueType`

Trait value matches expected type.

###### Traits

* `trait` (required; Trait name string per the Naming and Value Specification (`spec/0.1/naming-and-values/index.md`))
* `valueType` (required; value type token)

---

#### 11.10.2 Value Constraints

##### `ValueIsOneOf`

Value is in an explicit list.

###### Traits

* `values` (required; list of allowed values)

##### `ValueMatchesPattern`

Value matches a regular expression.

###### Traits

* `pattern` (required; regex string)

##### `PatternConstraint`

Trait value matches a regular expression.

###### Traits

* `trait` (required; Trait name string per the Naming and Value Specification (`spec/0.1/naming-and-values/index.md`))
* `pattern` (required; regex string)

##### `ValueLength`

String value length is within bounds.

###### Traits

* `min` (optional; non-negative integer)
* `max` (optional; positive integer)

##### `ValueInNumericRange`

Numeric value is within bounds.

###### Traits

* `min` (optional; number, inclusive)
* `max` (optional; number, inclusive)

##### `ValueIsNonEmpty`

Value is present and non-empty.

No traits.

##### `ValueIsValid`

Value passes custom validation.

###### Traits

* `validatorName` (required; enumerated token)

---

#### 11.10.3 Child Constraints

##### `ChildConstraint`

Generic child constraint using type dispatch.

###### Traits

* `type` (required; `RequiresChildConcept | AllowsChildConcept | ForbidsChildConcept`)
* `conceptSelector` (required; Concept name)

##### `ChildSatisfies`

Child Concepts satisfy a nested rule.

###### Traits

* `conceptSelector` (required; Concept name)

###### Children

One `Rule` child.

---

#### 11.10.4 Collection Constraints

##### `CollectionOrdering`

Declares expected ordering.

###### Traits

* `ordering` (required; `$Ordered | $Unordered`)

##### `CollectionAllowsEmpty`

Collection may be empty.

###### Traits

* `allowed` (required; boolean)

##### `CollectionAllowsDuplicates`

Collection may contain duplicates.

###### Traits

* `allowed` (required; boolean)

##### `MemberCount`

Collection member count is within bounds.

###### Traits

* `min` (optional; non-negative integer)
* `max` (optional; positive integer)

##### `EachMemberSatisfies`

Each collection member satisfies a nested rule.

###### Children

One `Rule` child.

##### `CollectionConstraint`

Generic collection constraint using type dispatch.

###### Traits

* `type` (required; one of the following)

###### Types

* `CollectionOrderingDeclared` — the applicable collection ordering MUST be explicitly declared in schema definitions (typically via `CollectionRules ordering=...`).

---

#### 11.10.5 Uniqueness Constraints

##### `UniqueConstraint`

Trait values must be unique within a scope.

###### Traits

* `trait` (required; Trait name string per the Naming and Value Specification (`spec/0.1/naming-and-values/index.md`))
* `scope` (required; Concept name defining the uniqueness scope)

---

#### 11.10.6 Order Constraints

##### `OrderConstraint`

Positional rules for ordered collections.

###### Traits

* `type` (required; e.g., `VariadicMustBeLast`)

---

#### 11.10.7 Reference Constraints

##### `ReferenceConstraint`

Validates reference Trait usage.

###### Traits

* `type` (required; one of the following)

###### Types

* `ReferenceTargetsEntity` — referenced Concept must be an Entity
* `ReferenceMustResolve` — reference must resolve to existing Concept
* `ReferenceTargetsConcept` — reference must target specified Concept type
  * `conceptSelector` (additional trait; Concept name)
* `ReferenceSingleton` — only one reference Trait may be present
* `ReferenceTraitAllowed` — specific reference Trait is permitted

---

#### 11.10.8 Identity Constraints

##### `IdentityConstraint`

Validates Entity identity rules.

###### Traits

* `type` (required; one of the following)

###### Types

* `MustBeEntity` — Concept instance must have `id`
* `MustNotBeEntity` — Concept instance must not have `id`
* `IdentifierUniqueness` — identifier must be unique within scope
* `IdentifierForm` — identifier must match pattern

---

#### 11.10.9 Context Constraints

##### `ContextConstraint`

Validates parent or context rules.

##### Traits

* `type` (required; one of the following)
* `contextSelector` (required for most types; Concept name)

###### Types

* `OnlyValidUnderParent` — Concept may only appear as direct child of specified parent
* `OnlyValidUnderContext` — Concept may only appear within specified ancestor

---

#### 11.10.10 Content Constraints

##### `ContentConstraint`

Validates content rules.

###### Traits

* `type` (required; one of the following)

###### Types

* `ContentForbiddenUnlessAllowed` — content forbidden unless explicitly allowed
* `ContentRequired` — content must be present and non-empty
* `ContentMatchesPattern` — content matches regex pattern
  * `pattern` (additional trait; regex string)

---

### 11.11. Complete Constraint Example

```cdx
<ConstraintDefinition
	id=example:constraint:recipe-requires-title
	title="Recipe requires Title"
>
	<Targets>
		<TargetConcept conceptSelector="Recipe" />
	</Targets>
	<Rule>
		<ChildConstraint type="RequiresChildConcept" conceptSelector="Title" />
	</Rule>
</ConstraintDefinition>

<ConstraintDefinition
	id=example:constraint:non-nullary-requires-parameters
	title="Non-nullary operators require parameters"
>
	<Targets>
		<TargetConcept conceptSelector="OperatorDefinition" />
	</Targets>
	<Rule>
		<ConditionalConstraint>
			<When>
				<Not>
					<TraitEquals trait="arity" value=$Nullary />
				</Not>
			</When>
			<Then>
				<ChildConstraint type="RequiresChildConcept" conceptSelector="Parameters" />
			</Then>
		</ConditionalConstraint>
	</Rule>
</ConstraintDefinition>
```

---

### 11.12. Relationship to External Systems (Normative)

* Codex schemas are **authoritative**
* SHACL or OWL representations MAY be derived
* Derived artifacts MUST NOT override Codex validation semantics

---

### 11.13. Summary

* Schemas are first-class Codex data
* Content mode is declared via `ContentRules`
* Trait, child, and collection rules are explicit
* Constraints are declarative and compositional
* Enumerated value sets may be defined per-schema or built-in
* This ontology enables self-hosting schema validation

Validation semantics, including closed-world behavior and determinism, are governed by this specification (see §9).

---

**End of Codex Schema Definition Specification v0.1**

---

## 12. Schema Loading and Bootstrapping

This section defines how schemas are associated with documents for schema-first parsing and validation.

### 12.1 Purpose

Codex is a schema-first language. A document cannot be semantically validated without its governing schema.

Codex permits schema-less formatting and well-formedness checks that do not require a governing schema (see §9.2).

This section defines how parsers obtain the governing schema for a document.

Its goals are to:

- ensure every validation operation has a schema
- support multiple schema provision mechanisms
- enable schema-document bootstrapping via a built-in bootstrap schema-of-schemas
- provide clear errors when schema is unavailable

### 12.2 Schema Provision Mechanisms (Normative)

A conforming parser MUST support explicit schema provision.

A conforming parser MAY support additional mechanisms.

#### 12.2.1 Explicit Provision (Required)

The caller provides the schema directly to the parser.

`parse(document, schema) → AST`

This is the baseline mechanism. All conforming implementations MUST support it.

#### 12.2.2 Schema Registry (Optional)

The parser MAY consult a registry to resolve schema identifiers.

Registry implementation details are outside this specification.

### 12.3 Resolution Order (Normative)

When a parser supports multiple provision mechanisms, it MUST follow this order:

1. Explicit provision — if caller provides schema, use it.
2. Registry lookup — if implementation supports registry, consult it.
3. Failure — if no schema is obtained, fail with `ParseError`.

Explicit provision always takes precedence.

### 12.4 Bootstrap Schema-of-Schemas (Normative)

The bootstrap schema-of-schemas is the built-in schema language required to parse and validate schema documents (root `Schema`) without circular dependency.

This is distinct from ecosystem meta-schemas (for example, a domain meta-schema), which are ordinary schema documents authored in Codex and validated under the bootstrap schema-of-schemas.

#### 12.4.1 Requirements

Every conforming implementation MUST:

- include the complete bootstrap schema-of-schemas as built-in, hard-coded data
- use the bootstrap schema-of-schemas when parsing and validating schema documents

#### 12.4.2 Detection

A document is a schema document if its root Concept is `Schema`.

When the parser encounters a root `Schema` Concept:

1. If explicit schema was provided, use it (it MAY be a meta-schema or an extension).
2. Otherwise, use the built-in bootstrap schema-of-schemas.

#### 12.4.3 Error Classification (Normative)

- If a schema document is not structurally readable (for example, malformed markers), the failure is a `ParseError`.
- If a schema document is structurally readable but violates the bootstrap schema-of-schemas rules, the failure is a `SchemaError`.

#### 12.4.4 Canonical Schema-Language Definition (Normative)

All schema-language constructs that appear inside schema documents are defined normatively in exactly one place:

- the schema definition language defined by §11 of this specification

The bootstrap schema-of-schemas MUST accept exactly the schema documents that conform to §11.

### 12.5 Schema Caching (Informative)

Schemas are immutable within a version. Implementations SHOULD cache parsed schemas to avoid redundant parsing.

Cache invalidation strategies are implementation-defined.

### 12.6 Error Handling (Normative)

#### 12.6.1 Schema Unavailable

If no schema can be obtained through any supported mechanism:

- Error class: `ParseError`
- Message SHOULD indicate schema was unavailable.
- Parsing MUST NOT proceed.

#### 12.6.2 Schema Load Failure

If schema resolution succeeds but loading fails (network error, file not found):

- Error class: `ParseError`
- Message SHOULD indicate schema could not be loaded.
- Message SHOULD include the schema identifier.

#### 12.6.3 Invalid Schema

If the loaded schema is not valid Codex or not a valid schema:

- Error class: `SchemaError`
- Message SHOULD indicate schema validation failed.
- Underlying schema errors SHOULD be reported.

### 12.7 Relationship to Other Specifications

- This specification defines schema-first processing (§9) and schema provision and bootstrapping (§12).
- The schema definition language is defined in §11.

---

## 13. Schema Versioning

This section defines how schemas are versioned and evolved.

Schema versioning rules are part of the Codex language and are governed by this section.

### 13.1 Purpose

This section defines how Codex schemas are versioned and evolved.

Its goals are to:

- allow schemas to change without breaking existing data
- make compatibility explicit and inspectable
- prevent silent semantic drift
- support long-lived data and tooling stability

This section governs schema evolution semantics, not data migration mechanisms.

### 13.2 Core Principles

Codex schema versioning is governed by the following principles:

1. Schemas evolve; data persists.
2. Compatibility is explicit, not inferred.
3. Breaking changes are deliberate.
4. Validation is version-aware and conforms to the determinism invariant.

Schemas MUST make their versioning intent explicit.

### 13.3 Schema Identity

Every Codex schema MUST declare:

- a stable schema identifier
- an explicit version designation

The schema identifier defines what schema this is.

The version defines which rules apply.

Schemas without explicit version information are invalid.

### 13.4 Version Semantics

Schemas MUST use monotonic versioning.

Versions MAY be expressed as:

- semantic versions (for example, `1.2.0`)
- date-based versions (for example, `2026-01`)
- another documented, totally ordered scheme

The specific format is schema-defined, but ordering MUST be unambiguous.

### 13.5 Compatibility Classes (Normative)

Each schema version MUST declare its compatibility class relative to the previous version.

Exactly one of the following MUST be specified.

#### 13.5.1 Backward-Compatible

A backward-compatible version guarantees:

- existing valid Codex data remains valid
- meaning of existing Concepts and Traits is preserved
- new Concepts or Traits MAY be added
- new constraints MAY be added only if they do not invalidate existing data

#### 13.5.2 Forward-Compatible

A forward-compatible version guarantees:

- Codex data authored for the new version MAY validate under older versions
- older tools can safely ignore newer constructs
- new constructs are optional and additive

Forward compatibility is typically used for extension-oriented evolution.

#### 13.5.3 Breaking

A breaking version declares that:

- existing valid Codex data MAY become invalid
- semantics of existing Concepts or Traits MAY change
- migration is required

Breaking versions MUST be explicitly marked.

### 13.6 What Constitutes a Breaking Change

The following changes are breaking:

- removing a Concept
- removing a Trait
- changing Entity eligibility
- changing reference semantics
- changing collection semantics
- tightening constraints that invalidate existing data
- changing the meaning of a Concept or Trait

Breaking changes MUST NOT be introduced silently.

### 13.7 Non-Breaking Changes

The following changes are non-breaking when properly declared:

- adding new Concepts
- adding optional Traits
- adding new Structural Concepts
- clarifying documentation
- adding new constraints that apply only to newly introduced Concepts

### 13.8 Schema Validation Behavior

When validating Codex data:

- the applicable schema version MUST be known
- validation MUST use that version's rules
- tools MUST NOT infer or guess schema intent

If schema version information is missing, ambiguous, or incompatible, validation MUST fail.

### 13.9 Relationship to Data Migration

This section does not define migration mechanisms.

However:

- breaking schema changes imply migration is required
- migration tooling MUST be explicit and MUST NOT rely on heuristics
- migrated data MUST validate cleanly under the target schema version

Schemas define what changed, not how to migrate.

### 13.10 Tooling Responsibilities

Codex tooling SHOULD:

- surface schema identifiers and versions clearly
- surface declared compatibility classes
- warn when data targets a newer schema version
- refuse to validate data against incompatible schema versions

Tooling MUST NOT silently reinterpret data across schema versions.

---

## 14. Validation Errors

### 14.1 Purpose

This section defines a canonical taxonomy of validation errors in Codex.

Its goals are to:

- make failures precise and predictable
- ensure consistent classification across tools
- avoid vague reporting and classification approaches that violate the language invariants (§2)
- separate parsing, surface form, formatting/canonicalization, and schema failures cleanly

This section governs error classification only, not wording, UI presentation, or recovery behavior.

### 14.2 Primary Error Class Requirement (Normative)

Every Codex failure MUST belong to exactly one primary error class.

Secondary information MAY be attached, but the primary class MUST be unambiguous.

### 14.3 Closed Set of Error Classes (Top Level) (Normative)

Codex defines the following closed set of top-level error classes:

1. ParseError
2. SurfaceFormError
3. FormattingError
4. SchemaError
5. IdentityError
6. ReferenceError
7. CollectionError
8. ContextError
9. ConstraintError

No other top-level error classes are permitted.

### 14.4 Error Class Definitions

#### 14.4.1 ParseError

Definition: a `.cdx` file cannot be parsed into a syntactic structure.

Characteristics:

- input is not structurally readable
- parsing cannot continue
- parsing MAY be performed without a governing schema for well-formedness checks

Examples (illustrative):

- unbalanced Concept markers
- invalid string literal escaping
- malformed Traits
- unterminated Annotation (missing closing `]`)
- structurally invalid nesting of markers

`ParseError` is fatal.

#### 14.4.2 SurfaceFormError

Definition: a file parses successfully but violates the surface form requirements (§8).

Characteristics:

- syntax is readable
- surface requirements are violated
- schema is available, but this class concerns schema-independent surface rules

Examples (illustrative):

- invalid casing in Concept or Trait names
- multiple root Concepts in a file
- forbidden whitespace around `=`
- annotation opening `[` not at first non-whitespace position
- annotation escape misuse (e.g., `\q` in an Annotation)

`SurfaceFormError` is fatal.

#### 14.4.3 FormattingError

Definition: input parses and passes surface-form requirements but cannot be transformed into canonical surface form.

See §10 for canonicalization rules.

Characteristics:

- canonicalization is deterministic or must fail
- tools MUST NOT guess or “best-effort” normalize

Examples (illustrative):

- ambiguous annotation attachment
- non-deterministic blank-line/whitespace normalization that would change annotation kind
- whitespace patterns that cannot be normalized without changing structure
- any other canonicalization failure

`FormattingError` is fatal.

#### 14.4.4 SchemaError

Definition: parsed Codex violates schema-defined rules.

Characteristics:

- schema is consulted
- Concepts or Traits are invalid under the active schema
- meaning cannot be assigned

Examples (illustrative):

- unauthorized Trait on a Concept
- missing required Trait
- invalid Trait value type

`SchemaError` is fatal.

#### 14.4.5 IdentityError

Definition: identity rules are violated.

See §6 for identifier rules.

Characteristics:

- concerns Entity eligibility and identifier use
- compromises stable identity or uniqueness

Examples (illustrative):

- `id` declared on a Concept that MUST NOT be an Entity
- missing required `id` where schema requires an Entity
- duplicate identifiers within a schema-defined scope
- identifier form invalid under schema constraints

`IdentityError` is fatal.

#### 14.4.6 ReferenceError

Definition: reference Traits are invalid or inconsistent.

See §7 for reference trait semantics.

Characteristics:

- involves `reference`, `target`, or `for`
- relates to graph linkage and intent

Examples (illustrative):

- violation of the reference singleton rule (unless schema permits)
- reference to a non-existent Entity (where resolution is required)
- reference to an Entity of an unauthorized Concept type

`ReferenceError` is fatal.

#### 14.4.7 CollectionError

Definition: schema-defined collection rules are violated.

Characteristics:

- concerns domain collection Concepts
- membership and ordering semantics are incorrect

Examples (illustrative):

- mixed member Concept types in a collection
- missing required members
- duplicate membership where forbidden
- member count outside required bounds

`CollectionError` is fatal.

#### 14.4.8 ContextError

Definition: a Concept or Trait is used outside its schema-defined context.

Characteristics:

- the name may be valid
- but it is misapplied due to containment or scope rules

Examples (illustrative):

- Concept permitted only under a specific parent appears elsewhere
- Trait permitted only in a particular context appears outside it

`ContextError` is fatal.

#### 14.4.9 ConstraintError

Definition: schema-defined declarative constraints are violated beyond basic structure and authorization.

Characteristics:

- logical or semantic invariants fail
- constraints are schema-defined and mechanically enforceable

Examples (illustrative):

- mutually exclusive Traits both present
- invalid combinations of Traits
- value range violations
- domain-specific invariant failures

`ConstraintError` is fatal.

### 14.5 Error Severity (Normative)

Codex errors are not warnings.

- any failure halts compilation or processing
- no best-effort recovery is permitted
- tools MUST NOT silently reinterpret invalid data

### 14.6 Reporting Requirements

Tools SHOULD report failures with:

- primary error class
- Concept name
- Trait name (if applicable)
- violated rule reference
- precise location (line number or Concept path)

Classification is mandatory. Wording and presentation are tool-defined.

### 14.7 Non-Goals

This section does not:

- define message wording
- mandate UX
- define recovery strategies
- prescribe exception hierarchies
- define logging formats

It defines what kind of error occurred, not how it is presented.

### 14.8 Summary

- every failure has exactly one primary error class
- error classes are finite and closed
- parsing, surface form, formatting/canonicalization, and schema are separated
- failures are fatal within their primary error class

---

## Appendix A. Formal Grammar

This appendix defines the formal grammar of the Codex surface form.

Two grammar notations are provided:

- EBNF (Normative) — ISO/IEC 14977 Extended Backus-Naur Form
- PEG (Informative) — Parsing Expression Grammar for implementation

### A.1 EBNF (Normative)

#### A.1.1 Notation

This grammar uses ISO/IEC 14977 EBNF notation:

* `=` defines a production
* `,` concatenation
* `|` alternation
* `[ ... ]` optional (zero or one)
* `{ ... }` repetition (zero or more)
* `( ... )` grouping
* `" ... "` terminal string
* `' ... '` terminal string (alternative)
* `(* ... *)` comment
* `- ` exception
* `;` end of production

Character classes use the following extensions:

* `#x0000` Unicode code point
* `[a-z]` character range
* `\t` tab (U+0009)
* `\n` line feed (U+000A)

---

#### A.1.2 Document Structure

```ebnf
(* A Codex document contains exactly one root Concept *)

(* Annotations may appear with intervening blank lines; formatter normalizes. *)
Document = { BlankLine }, { Annotation, { BlankLine } }, RootConcept, { BlankLine } ;

RootConcept = Concept ;

Concept = BlockConcept | SelfClosingConcept ;
```

---

#### A.1.3 Block Concepts

```ebnf
(* Block concepts contain either children or content.
	The parser consults the schema to determine which.
	This is schema-directed dispatch, not syntactic ambiguity. *)

BlockConcept = OpeningMarker, Body, ClosingMarker ;

OpeningMarker = "<", ConceptName, [ Traits ], [ Whitespace ], ">" ;

ClosingMarker = "</", ConceptName, ">" ;

(* Body production is selected by schema lookup on ConceptName:
	- If schema indicates children mode (ForbidsContent): ChildrenBody
	- If schema indicates content mode (AllowsContent): ContentBody *)

Body = ChildrenBody | ContentBody ;

ChildrenBody = { ChildEntry } ;

ChildEntry = Newline, Indentation, { Annotation, Newline, Indentation }, Concept, [ BlankLine ] ;

ContentBody = { ContentLine } ;

ContentLine = Newline, Indentation, ContentText ;

ContentText = { ContentChar } ;

ContentChar = ContentEscape | ContentSafeChar ;

ContentEscape = "\\", ( "<" | "\\" ) ;

(* Raw '<' and '\\' are not permitted in content.
	They MUST be written as '\\<' and '\\\\' respectively. *)
ContentSafeChar = AnyCharExceptNewline - "<" - "\\" ;
```

---

#### A.1.4 Self-Closing Concepts

```ebnf
SelfClosingConcept = "<", ConceptName, [ Traits ], [ Whitespace ], "/>" ;
```

---

#### A.1.5 Concept Names

```ebnf
ConceptName = UppercaseLetter, { Letter | Digit } ;

UppercaseLetter = "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J"
					 | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T"
					 | "U" | "V" | "W" | "X" | "Y" | "Z" ;

LowercaseLetter = "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j"
					 | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t"
					 | "u" | "v" | "w" | "x" | "y" | "z" ;

Letter = UppercaseLetter | LowercaseLetter ;

Digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
```

---

#### A.1.6 Traits

```ebnf
Traits = Whitespace, Trait, { Whitespace, Trait } ;

Trait = TraitName, "=", Value ;

TraitName = LowercaseLetter, { Letter | Digit } ;
```

---

#### A.1.7 Values

```ebnf
Value = StringValue
		| CharValue
		| BacktickString
		| BooleanValue
		| NumericValue
		| EnumeratedToken
		| IriReference
		| LookupToken
		| UuidValue
		| ColorValue
		| TemporalValue
		| ListValue
		| SetValue
		| MapValue
		| TupleValue
		| RangeValue ;
```

---

#### A.1.8 String Values

```ebnf
StringValue = '"', { StringChar }, '"' ;

StringChar = UnescapedStringChar | EscapeSequence ;

UnescapedStringChar = AnyCharExceptQuoteBackslashNewline ;

EscapeSequence = "\\", ( '"' | "\\" | "n" | "r" | "t" | UnicodeEscape ) ;

UnicodeEscape = "u", HexDigit, HexDigit, HexDigit, HexDigit
				  | "u{", HexDigit, { HexDigit }, "}" ;

HexDigit = Digit | "a" | "b" | "c" | "d" | "e" | "f"
					  | "A" | "B" | "C" | "D" | "E" | "F" ;
```

---

#### A.1.9 Character Values

```ebnf
CharValue = "'", CharContent, "'" ;

CharContent = UnescapedChar | CharEscapeSequence ;

UnescapedChar = AnyCharExceptApostropheBackslashNewline ;

CharEscapeSequence = "\\", ( "'" | "\\" | "n" | "r" | "t" | UnicodeEscape ) ;
```

---

#### A.1.10 Backtick Strings

```ebnf
(* Backtick strings collapse whitespace to single spaces *)

BacktickString = "`", { BacktickChar }, "`" ;

BacktickChar = UnescapedBacktickChar | BacktickEscape ;

UnescapedBacktickChar = AnyCharExceptBacktickBackslash ;

BacktickEscape = "\\", ( "`" | "\\" ) ;
```

---

#### A.1.11 Boolean Values

```ebnf
BooleanValue = "true" | "false" ;
```

---

#### A.1.12 Numeric Values

```ebnf
NumericValue = ComplexNumber
				 | ImaginaryNumber
				 | Fraction
				 | Infinity
				 | PrecisionNumber
				 | ScientificNumber
				 | DecimalNumber
				 | Integer ;

Sign = "+" | "-" ;

Integer = [ Sign ], DigitSequence ;

DecimalNumber = [ Sign ], DigitSequence, ".", DigitSequence ;

ScientificNumber = ( Integer | DecimalNumber ), ( "e" | "E" ), [ Sign ], DigitSequence ;

PrecisionNumber = DecimalNumber, "p", [ DigitSequence ] ;

Infinity = [ Sign ], "Infinity" ;

Fraction = Integer, "/", DigitSequence ;

ImaginaryNumber = ( Integer | DecimalNumber ), "i" ;

ComplexNumber = ( Integer | DecimalNumber ), ( "+" | "-" ), ( Integer | DecimalNumber ), "i" ;

DigitSequence = Digit, { Digit } ;
```

---

#### A.1.13 Enumerated Tokens

```ebnf
EnumeratedToken = "$", UppercaseLetter, { Letter | Digit } ;
```

---

#### A.1.14 IRI References

```ebnf
(* Codex IRI references allow RFC 3987 IRI-reference characters directly.
		Unicode characters MAY appear directly; percent-encoding remains valid.
	Codex further forbids Unicode whitespace, control, bidi-control, and private-use characters.
	These profile restrictions are enforced by surface-form validation; they are not fully
	encoded in the UcsChar placeholder production below. *)

IriReference = IriScheme, ":", IriBody ;

IriScheme = Letter, { Letter | Digit | "+" | "-" | "." } ;

IriBody = { IriChar } ;

IriChar = IriAsciiChar | UcsChar ;

IriAsciiChar = Letter | Digit | "-" | "." | "_" | "~" | ":" | "/" | "?" | "#"
			 | "[" | "]" | "@" | "!" | "$" | "&" | "'" | "(" | ")"
			 | "*" | "+" | "," | ";" | "=" | "%" ;

(* RFC 3987 character classes (descriptive):
	UcsChar  = %xA0-D7FF / %xF900-FDCF / %xFDF0-FFEF / %x10000-1FFFD
			 / %x20000-2FFFD / %x30000-3FFFD / %x40000-4FFFD / %x50000-5FFFD
			 / %x60000-6FFFD / %x70000-7FFFD / %x80000-8FFFD / %x90000-9FFFD
			 / %xA0000-AFFFD / %xB0000-BFFFD / %xC0000-CFFFD / %xD0000-DFFFD
			 / %xE1000-EFFFD
*)
UcsChar = ? any Unicode scalar value in the RFC 3987 ucschar ranges ? ;
```

---

#### A.1.15 Lookup Tokens

```ebnf
LookupToken = "~", LowercaseLetter, { Letter | Digit } ;
```

---

#### A.1.16 UUID Values

```ebnf
UuidValue = HexOctet, HexOctet, HexOctet, HexOctet, "-",
				HexOctet, HexOctet, "-",
				HexOctet, HexOctet, "-",
				HexOctet, HexOctet, "-",
				HexOctet, HexOctet, HexOctet, HexOctet, HexOctet, HexOctet ;

HexOctet = HexDigit, HexDigit ;
```

---

#### A.1.17 Color Values

```ebnf
ColorValue = HexColor | RgbColor | HslColor | LabColor | LchColor
			  | OklabColor | OklchColor | ColorFunction | NamedColor ;

HexColor = "#", HexDigit, HexDigit, HexDigit, [ HexDigit ]
			| "#", HexDigit, HexDigit, HexDigit, HexDigit, HexDigit, HexDigit, [ HexDigit, HexDigit ] ;

RgbColor = ( "rgb" | "rgba" ), "(", ColorArgs, ")" ;

HslColor = ( "hsl" | "hsla" ), "(", ColorArgs, ")" ;

LabColor = "lab", "(", ColorArgs, ")" ;

LchColor = "lch", "(", ColorArgs, ")" ;

OklabColor = "oklab", "(", ColorArgs, ")" ;

OklchColor = "oklch", "(", ColorArgs, ")" ;

ColorFunction = "color", "(", ColorSpace, Whitespace, ColorArgs, ")" ;

ColorSpace = "srgb" | "srgb-linear" | "display-p3" | "a98-rgb"
			  | "prophoto-rgb" | "rec2020" | "xyz" | "xyz-d50" | "xyz-d65" ;

ColorArgs = ColorArg, { ( Whitespace | "," ), ColorArg }, [ ( Whitespace, "/" | "," ), AlphaArg ] ;

ColorArg = NumericValue | Percentage ;

AlphaArg = NumericValue | Percentage ;

Percentage = NumericValue, "%" ;

NamedColor = "&", LowercaseLetter, { LowercaseLetter } ;
```

---

#### A.1.18 Temporal Values

```ebnf
TemporalValue = "{", TemporalBody, "}" ;

TemporalBody = ZonedDateTime | LocalDateTime | Date | YearMonth | MonthDay | Time | Duration | ReservedTemporal ;

Date = Year, "-", Month, "-", Day ;

YearMonth = Year, "-", Month ;

MonthDay = Month, "-", Day ;

LocalDateTime = Date, "T", Time ;

ZonedDateTime = LocalDateTime, TimeZoneOffset, [ TimeZoneId ] ;

TimeZoneOffset = "Z" | ( ( "+" | "-" ), Hour, ":", Minute ) ;

TimeZoneId = "[", TimeZoneIdChar, { TimeZoneIdChar }, "]" ;

TimeZoneIdChar = Letter | Digit | "/" | "_" | "-" ;

Time = Hour, ":", Minute, [ ":", Second, [ ".", Milliseconds ] ] ;

Duration = "P", { DurationComponent }, [ "T", { TimeDurationComponent } ] ;

DurationComponent = DigitSequence, ( "Y" | "M" | "W" | "D" ) ;

TimeDurationComponent = DigitSequence, [ ".", DigitSequence ], ( "H" | "M" | "S" ) ;

ReservedTemporal = "now" | "today" ;

Year = Digit, Digit, Digit, Digit ;
Month = Digit, Digit ;
Day = Digit, Digit ;
Hour = Digit, Digit ;
Minute = Digit, Digit ;
Second = Digit, Digit ;
Milliseconds = Digit, { Digit } ;
```

---

#### A.1.19 List Values

```ebnf
ListValue = "[", [ Whitespace ], [ ListItems ], [ Whitespace ], "]" ;

ListItems = Value, { ",", [ Whitespace ], Value } ;
```

---

#### A.1.20 Set Values

```ebnf
SetValue = "set[", [ Whitespace ], [ SetItems ], [ Whitespace ], "]" ;

SetItems = Value, { ",", [ Whitespace ], Value } ;
```

---

#### A.1.21 Map Values

```ebnf
MapValue = "map[", [ Whitespace ], [ MapItems ], [ Whitespace ], "]" ;

MapItems = MapEntry, { ",", [ Whitespace ], MapEntry } ;

MapEntry = MapKey, ":", [ Whitespace ], Value ;

MapKey = MapIdentifier | StringValue | CharValue | Integer | EnumeratedToken ;

MapIdentifier = LowercaseLetter, { Letter | Digit } ;
```

---

#### A.1.22 Tuple Values

```ebnf
TupleValue = "(", [ Whitespace ], TupleItems, [ Whitespace ], ")" ;

TupleItems = Value, { ",", [ Whitespace ], Value } ;
```

---

#### A.1.23 Range Values

```ebnf
RangeValue = RangeStart, "..", RangeEnd, [ "s", StepValue ] ;

RangeStart = NumericValue | TemporalValue | CharValue ;

RangeEnd = NumericValue | TemporalValue | CharValue ;

StepValue = NumericValue | TemporalValue ;
```

---

#### A.1.24 Annotations

```ebnf
Annotation = "[", { AnnotationChar }, "]" ;

AnnotationChar = UnescapedAnnotationChar | AnnotationEscape ;

UnescapedAnnotationChar = AnyCharExceptBracketBackslash ;

AnnotationEscape = "\\", ( "]" | "\\" ) ;
```

---

#### A.1.25 Whitespace and Structural Elements

```ebnf
Whitespace = WhitespaceChar, { WhitespaceChar } ;

WhitespaceChar = " " | "\t" | Newline ;

Newline = "\n" ;

BlankLine = Newline, { " " | "\t" }, Newline ;

Indentation = { "\t" } ;

Tab = "\t" ;
```

---

#### A.1.26 Character Classes (Informative)

The following character classes are used but not fully enumerated:

* `AnyCharExceptNewline` — any Unicode scalar except U+000A
* `AnyCharExceptQuoteBackslashNewline` — any Unicode scalar except `"`, `\\`, U+000A
* `AnyCharExceptApostropheBackslashNewline` — any Unicode scalar except `'`, `\\`, U+000A
* `AnyCharExceptBacktickBackslash` — any Unicode scalar except `` ` ``, `\\`
* `AnyCharExceptBracketBackslash` — any Unicode scalar except `]`, `\\`

---

#### A.1.27 Precedence and Disambiguation

When parsing Values, the following precedence applies (highest first):

1. String, Character, Backtick (delimited)
2. Boolean keywords (`true`, `false`)
3. Enumerated tokens (`$...`)
4. Lookup tokens (`~...`)
5. Temporal values (`{...}`)
6. Set values (`set[...]`)
7. Map values (`map[...]`)
8. List values (`[...]`)
9. Tuple values (`(...)`)
10. Color functions (`rgb(...)`, etc.)
11. Hex colors (`#...`)
12. UUID (pattern match: 8-4-4-4-12)
13. Range (contains `..`)
14. Complex/Imaginary (contains `i`)
15. Fraction (contains `/`)
16. Precision (contains `p`)
17. Scientific (contains `e` or `E`)
18. Decimal (contains `.`)
19. Integer
20. IRI reference (fallback)

---

### A.2 PEG (Informative)

The PEG grammar is informative. It provides an implementation-ready, unambiguous grammar.

In case of discrepancy between EBNF and PEG, the EBNF grammar in §A.1 takes precedence.

#### A.2.1 Notation

This grammar uses standard PEG notation:

* `<-` defines a rule
* `/` ordered choice (try left first)
* `*` zero or more
* `+` one or more
* `?` optional (zero or one)
* `&` positive lookahead
* `!` negative lookahead
* `( ... )` grouping
* `" ... "` literal string
* `' ... '` literal string (alternative)
* `[ ... ]` character class
* `.` any character
* `#` comment to end of line

---

#### A.2.2 Document Structure

```peg
# A Codex document contains exactly one root Concept

Document <- BlankLine* (Annotation BlankLine*)* RootConcept BlankLine* EOF

RootConcept <- Concept

Concept <- BlockConcept / SelfClosingConcept
```

---

#### A.2.3 Block Concepts

```peg
# Block concepts contain either children or content.
# The parser consults the schema to determine which.
# This is schema-directed dispatch, not syntactic ambiguity.

BlockConcept <- OpeningMarker Body ClosingMarker

OpeningMarker <- '<' ConceptName Traits? Whitespace? '>'

ClosingMarker <- '</' ConceptName '>'

# Body parsing is schema-directed:
# - Children mode (ForbidsContent): parse as ChildrenBody
# - Content mode (AllowsContent): parse as ContentBody
# Implementation selects the appropriate production at runtime.

ChildrenBody <- (Newline Indentation ChildEntry)*

ChildEntry <- (Annotation Newline Indentation)* Concept

ContentBody <- ContentLine*

ContentLine <- Newline Indentation ContentText

ContentText <- ContentChar*

ContentChar <- ContentEscape / ContentSafeChar

ContentEscape <- '\\' ('<' / '\\')

ContentSafeChar <- !Newline !('<' / '\\') .

# Content termination is unambiguous because '<' is not permitted unescaped
# inside content.
```

---

#### A.2.4 Self-Closing Concepts

```peg
SelfClosingConcept <- '<' ConceptName Traits? Whitespace? '/>'
```

---

#### A.2.5 Concept Names

```peg
ConceptName <- UppercaseLetter (Letter / Digit)*

UppercaseLetter <- [A-Z]
LowercaseLetter <- [a-z]
Letter <- [A-Za-z]
Digit <- [0-9]
```

---

#### A.2.6 Traits

```peg
Traits <- (Whitespace Trait)+

Trait <- TraitName '=' Value

TraitName <- LowercaseLetter (Letter / Digit)*
```

---

#### A.2.7 Values

```peg
# Values are tried in precedence order
# Delimited values first, then keywords, then pattern-matched

Value <- StringValue
		 / CharValue
		 / BacktickString
		 / BooleanValue
		 / EnumeratedToken
		 / LookupToken
		 / TemporalValue
		 / SetValue
		 / MapValue
		 / ListValue
		 / TupleValue
		 / ColorFunction
		 / HexColor
		 / NamedColor
		 / UuidValue
		 / RangeValue
		 / ComplexNumber
		 / ImaginaryNumber
		 / Fraction
		 / Infinity
		 / PrecisionNumber
		 / ScientificNumber
		 / DecimalNumber
		 / Integer
		 / IriReference
```

---

#### A.2.8 String Values

```peg
StringValue <- '"' StringChar* '"'

StringChar <- EscapeSequence / (!["\\\n] .)

EscapeSequence <- '\\' ( ["\\nrt] / UnicodeEscape )

UnicodeEscape <- 'u' HexDigit HexDigit HexDigit HexDigit
					/ 'u{' HexDigit+ '}'

HexDigit <- [0-9A-Fa-f]
```

---

#### A.2.9 Character Values

```peg
CharValue <- "'" CharContent "'"

CharContent <- CharEscapeSequence / (!['\\\n] .)

CharEscapeSequence <- '\\' ( ['\\/nrt] / UnicodeEscape )
```

---

#### A.2.10 Backtick Strings

```peg
# Backtick strings span multiple lines; whitespace collapses to single space

BacktickString <- '`' BacktickChar* '`'

BacktickChar <- BacktickEscape / (![`\\] .)

BacktickEscape <- '\\' [`\\]
```

---

#### A.2.11 Boolean Values

```peg
BooleanValue <- 'true' / 'false'
```

---

#### A.2.12 Numeric Values

```peg
# Ordered by specificity: complex before imaginary, precision before decimal

ComplexNumber <- Sign? Digits ('.' Digits)? Sign Digits ('.' Digits)? 'i'

ImaginaryNumber <- Sign? Digits ('.' Digits)? 'i'

Fraction <- Sign? Digits '/' Digits

Infinity <- Sign? 'Infinity'

PrecisionNumber <- Sign? Digits '.' Digits 'p' Digits?

ScientificNumber <- Sign? Digits ('.' Digits)? [eE] Sign? Digits

DecimalNumber <- Sign? Digits '.' Digits

Integer <- Sign? Digits

Sign <- [+-]
Digits <- Digit+
```

---

#### A.2.13 Enumerated Tokens

```peg
EnumeratedToken <- '$' UppercaseLetter (Letter / Digit)*
```

---

#### A.2.14 IRI References

```peg
IriReference <- IriScheme ':' IriBody

IriScheme <- Letter (Letter / Digit / [+.-])*

IriBody <- IriChar*

# In surface form, unquoted values are delimited by structural characters
# (whitespace, '>', '/>', etc.). This PEG defines a conservative tokenization:
IriChar <- !WhitespaceChar !'>' .

# ---

LookupToken <- '~' LowercaseLetter (Letter / Digit)*

# ---

TemporalValue <- '{' TemporalBody '}'

TemporalBody <- ZonedDateTime / LocalDateTime / Date / YearMonth / MonthDay / Time / Duration / ReservedTemporal

Date <- Year '-' Month '-' Day
YearMonth <- Year '-' Month
MonthDay <- Month '-' Day

LocalDateTime <- Date 'T' Time
ZonedDateTime <- LocalDateTime TimeZoneOffset TimeZoneId?

TimeZoneOffset <- 'Z' / ([+-] Hour ':' Minute)
TimeZoneId <- '[' TimeZoneIdChar+ ']'
TimeZoneIdChar <- Letter / Digit / '/' / '_' / '-'

Time <- Hour ':' Minute (':' Second ('.' Milliseconds)?)?

Duration <- 'P' DurationComponent* ('T' TimeDurationComponent*)?
DurationComponent <- Digits ([YMWD])
TimeDurationComponent <- Digits ('.' Digits)? ([HMS])

ReservedTemporal <- 'now' / 'today'

Year <- Digit Digit Digit Digit
Month <- Digit Digit
Day <- Digit Digit
Hour <- Digit Digit
Minute <- Digit Digit
Second <- Digit Digit
Milliseconds <- Digit+

# ---

ListValue <- '[' Whitespace? ListItems? Whitespace? ']'
ListItems <- Value (',' Whitespace? Value)*

SetValue <- 'set[' Whitespace? SetItems? Whitespace? ']'
SetItems <- Value (',' Whitespace? Value)*

MapValue <- 'map[' Whitespace? MapItems? Whitespace? ']'
MapItems <- MapEntry (',' Whitespace? MapEntry)*
MapEntry <- MapKey ':' Whitespace? Value
MapKey <- MapIdentifier / StringValue / CharValue / Integer / EnumeratedToken
MapIdentifier <- LowercaseLetter (Letter / Digit)*

TupleValue <- '(' Whitespace? TupleItems Whitespace? ')'
TupleItems <- Value (',' Whitespace? Value)*

# ---

UuidValue <- Hex8 '-' Hex4 '-' Hex4 '-' Hex4 '-' Hex12
Hex8 <- HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit
Hex4 <- HexDigit HexDigit HexDigit HexDigit
Hex12 <- HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit

# ---

RangeValue <- RangeStart '..' RangeEnd ('s' StepValue)?
RangeStart <- TemporalValue / CharValue / NumericAtom
RangeEnd <- TemporalValue / CharValue / NumericAtom
StepValue <- TemporalValue / NumericAtom

NumericAtom <- ComplexNumber / ImaginaryNumber / Fraction / Infinity / PrecisionNumber / ScientificNumber / DecimalNumber / Integer

# ---

HexColor <- '#' (Hex3 / Hex4 / Hex6 / Hex8Color)
Hex3 <- HexDigit HexDigit HexDigit
Hex4 <- HexDigit HexDigit HexDigit HexDigit
Hex6 <- HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit
Hex8Color <- HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit

NamedColor <- '&' [a-z]+

ColorFunction <- RgbFunc / HslFunc / LabFunc / LchFunc / OklabFunc / OklchFunc / ColorSpaceFunc

RgbFunc <- ('rgb' / 'rgba') '(' ColorArgs ')'
HslFunc <- ('hsl' / 'hsla') '(' ColorArgs ')'
LabFunc <- 'lab' '(' ColorArgs ')'
LchFunc <- 'lch' '(' ColorArgs ')'
OklabFunc <- 'oklab' '(' ColorArgs ')'
OklchFunc <- 'oklch' '(' ColorArgs ')'
ColorSpaceFunc <- 'color' '(' ColorSpace Whitespace ColorArgs ')'

ColorSpace <- 'srgb' / 'srgb-linear' / 'display-p3' / 'a98-rgb'
		   / 'prophoto-rgb' / 'rec2020' / 'xyz' / 'xyz-d50' / 'xyz-d65'

ColorArgs <- ColorArg ((Whitespace / ',') ColorArg)* (Whitespace? ('/' / ',') Whitespace? AlphaArg)?
ColorArg <- Percentage / NumericAtom
AlphaArg <- Percentage / NumericAtom
Percentage <- NumericAtom '%'

# ---

Annotation <- '[' AnnotationChar* ']'
AnnotationChar <- AnnotationEscape / (!(']' / '\\') .)
AnnotationEscape <- '\\' (']' / '\\')

Newline <- '\n'

WhitespaceChar <- [ \t\n]
Whitespace <- WhitespaceChar+

BlankLine <- Newline [ \t]* Newline

Indentation <- '\t'*

EOF <- !.
```

---

## Appendix B. CSS Named Colors (Informative)

This appendix provides an informative list of CSS named color keywords and their sRGB hex values.

This list exists for convenience only.

- The normative definition of CSS color keywords is in the CSS Color Module specifications.
- Codex-conforming tools MUST NOT validate, normalize, or convert Color Values (see §5.7).
- Named colors in Codex are written with a leading `&` sigil and an ASCII-lowercase keyword (see §5.7.1).

### B.1 Named Color Keyword Table

Each entry maps a Codex Named Color Value (`&name`) to its sRGB hex form.

| Named color | sRGB hex |
|---|---:|
| `&aliceblue` | `#f0f8ff` |
| `&antiquewhite` | `#faebd7` |
| `&aqua` | `#00ffff` |
| `&aquamarine` | `#7fffd4` |
| `&azure` | `#f0ffff` |
| `&beige` | `#f5f5dc` |
| `&bisque` | `#ffe4c4` |
| `&black` | `#000000` |
| `&blanchedalmond` | `#ffebcd` |
| `&blue` | `#0000ff` |
| `&blueviolet` | `#8a2be2` |
| `&brown` | `#a52a2a` |
| `&burlywood` | `#deb887` |
| `&cadetblue` | `#5f9ea0` |
| `&chartreuse` | `#7fff00` |
| `&chocolate` | `#d2691e` |
| `&coral` | `#ff7f50` |
| `&cornflowerblue` | `#6495ed` |
| `&cornsilk` | `#fff8dc` |
| `&crimson` | `#dc143c` |
| `&cyan` | `#00ffff` |
| `&darkblue` | `#00008b` |
| `&darkcyan` | `#008b8b` |
| `&darkgoldenrod` | `#b8860b` |
| `&darkgray` | `#a9a9a9` |
| `&darkgrey` | `#a9a9a9` |
| `&darkgreen` | `#006400` |
| `&darkkhaki` | `#bdb76b` |
| `&darkmagenta` | `#8b008b` |
| `&darkolivegreen` | `#556b2f` |
| `&darkorange` | `#ff8c00` |
| `&darkorchid` | `#9932cc` |
| `&darkred` | `#8b0000` |
| `&darksalmon` | `#e9967a` |
| `&darkseagreen` | `#8fbc8f` |
| `&darkslateblue` | `#483d8b` |
| `&darkslategray` | `#2f4f4f` |
| `&darkslategrey` | `#2f4f4f` |
| `&darkturquoise` | `#00ced1` |
| `&darkviolet` | `#9400d3` |
| `&deeppink` | `#ff1493` |
| `&deepskyblue` | `#00bfff` |
| `&dimgray` | `#696969` |
| `&dimgrey` | `#696969` |
| `&dodgerblue` | `#1e90ff` |
| `&firebrick` | `#b22222` |
| `&floralwhite` | `#fffaf0` |
| `&forestgreen` | `#228b22` |
| `&fuchsia` | `#ff00ff` |
| `&gainsboro` | `#dcdcdc` |
| `&ghostwhite` | `#f8f8ff` |
| `&gold` | `#ffd700` |
| `&goldenrod` | `#daa520` |
| `&gray` | `#808080` |
| `&grey` | `#808080` |
| `&green` | `#008000` |
| `&greenyellow` | `#adff2f` |
| `&honeydew` | `#f0fff0` |
| `&hotpink` | `#ff69b4` |
| `&indianred` | `#cd5c5c` |
| `&indigo` | `#4b0082` |
| `&ivory` | `#fffff0` |
| `&khaki` | `#f0e68c` |
| `&lavender` | `#e6e6fa` |
| `&lavenderblush` | `#fff0f5` |
| `&lawngreen` | `#7cfc00` |
| `&lemonchiffon` | `#fffacd` |
| `&lightblue` | `#add8e6` |
| `&lightcoral` | `#f08080` |
| `&lightcyan` | `#e0ffff` |
| `&lightgoldenrodyellow` | `#fafad2` |
| `&lightgray` | `#d3d3d3` |
| `&lightgrey` | `#d3d3d3` |
| `&lightgreen` | `#90ee90` |
| `&lightpink` | `#ffb6c1` |
| `&lightsalmon` | `#ffa07a` |
| `&lightseagreen` | `#20b2aa` |
| `&lightskyblue` | `#87cefa` |
| `&lightslategray` | `#778899` |
| `&lightslategrey` | `#778899` |
| `&lightsteelblue` | `#b0c4de` |
| `&lightyellow` | `#ffffe0` |
| `&lime` | `#00ff00` |
| `&limegreen` | `#32cd32` |
| `&linen` | `#faf0e6` |
| `&magenta` | `#ff00ff` |
| `&maroon` | `#800000` |
| `&mediumaquamarine` | `#66cdaa` |
| `&mediumblue` | `#0000cd` |
| `&mediumorchid` | `#ba55d3` |
| `&mediumpurple` | `#9370db` |
| `&mediumseagreen` | `#3cb371` |
| `&mediumslateblue` | `#7b68ee` |
| `&mediumspringgreen` | `#00fa9a` |
| `&mediumturquoise` | `#48d1cc` |
| `&mediumvioletred` | `#c71585` |
| `&midnightblue` | `#191970` |
| `&mintcream` | `#f5fffa` |
| `&mistyrose` | `#ffe4e1` |
| `&moccasin` | `#ffe4b5` |
| `&navajowhite` | `#ffdead` |
| `&navy` | `#000080` |
| `&oldlace` | `#fdf5e6` |
| `&olive` | `#808000` |
| `&olivedrab` | `#6b8e23` |
| `&orange` | `#ffa500` |
| `&orangered` | `#ff4500` |
| `&orchid` | `#da70d6` |
| `&palegoldenrod` | `#eee8aa` |
| `&palegreen` | `#98fb98` |
| `&paleturquoise` | `#afeeee` |
| `&palevioletred` | `#db7093` |
| `&papayawhip` | `#ffefd5` |
| `&peachpuff` | `#ffdab9` |
| `&peru` | `#cd853f` |
| `&pink` | `#ffc0cb` |
| `&plum` | `#dda0dd` |
| `&powderblue` | `#b0e0e6` |
| `&purple` | `#800080` |
| `&rebeccapurple` | `#663399` |
| `&red` | `#ff0000` |
| `&rosybrown` | `#bc8f8f` |
| `&royalblue` | `#4169e1` |
| `&saddlebrown` | `#8b4513` |
| `&salmon` | `#fa8072` |
| `&sandybrown` | `#f4a460` |
| `&seagreen` | `#2e8b57` |
| `&seashell` | `#fff5ee` |
| `&sienna` | `#a0522d` |
| `&silver` | `#c0c0c0` |
| `&skyblue` | `#87ceeb` |
| `&slateblue` | `#6a5acd` |
| `&slategray` | `#708090` |
| `&slategrey` | `#708090` |
| `&snow` | `#fffafa` |
| `&springgreen` | `#00ff7f` |
| `&steelblue` | `#4682b4` |
| `&tan` | `#d2b48c` |
| `&teal` | `#008080` |
| `&thistle` | `#d8bfd8` |
| `&tomato` | `#ff6347` |
| `&turquoise` | `#40e0d0` |
| `&violet` | `#ee82ee` |
| `&wheat` | `#f5deb3` |
| `&white` | `#ffffff` |
| `&whitesmoke` | `#f5f5f5` |
| `&yellow` | `#ffff00` |
| `&yellowgreen` | `#9acd32` |

### B.2 Context-Dependent Keywords

The following keywords are accepted as Codex named colors, but do not have a single fixed sRGB value in all contexts:

| Named color | Notes |
|---|---|
| `&transparent` | Equivalent to fully transparent black in CSS; informative sRGB hex form: `#00000000`. |
| `&currentcolor` | Context-dependent; resolves to the current text color in CSS. |

---

**End of Codex Language Specification v0.1**
