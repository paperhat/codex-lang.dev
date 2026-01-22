Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Codex Language Specification — Version 0.1

This document is the authoritative language specification for Codex 0.1.

The Codex 0.1 normative specification set includes this document, its normative annexes, and any additional documents under `spec/0.1/` that are explicitly marked `Status: NORMATIVE`.

All normative requirements for Codex 0.1 MUST appear exactly once across the normative specification set.

---

## 1. Front Matter

### 1.1 Scope

Codex 0.1 defines the Codex language.

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

Codex 0.1 does not define runtime behavior.

---

### 1.2 Non-Goals

Codex 0.1 does not define:

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

The authoritative model for schema authoring, schema-to-instance-graph interpretation, and deterministic projection to derived validation artifacts is defined in the normative annex [SCHEMAS.md](SCHEMAS.md).

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

The required semantics for schema-driven validation and any required derived artifacts are defined in [SCHEMAS.md](SCHEMAS.md).

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

The derived validation embedding mechanism is defined in [SCHEMAS.md](SCHEMAS.md).

#### 9.5.3 Explicit Path and Quantifier Rule Forms

Layer A MUST provide explicit rule forms that bind exactly one path to exactly one nested rule, so that path and quantifier semantics are total and deterministic.

The required rule forms and their semantics are defined in [SCHEMAS.md](SCHEMAS.md).

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

Layer B MUST be deterministic and canonical:

- Layer B MUST NOT contain RDF blank nodes.
- Any node that would otherwise be a blank node MUST be assigned a deterministic skolem IRI.
- Layer B MUST be treated as a set of RDF triples.
- Layer B MUST NOT contain duplicate triples.

Any algorithm that derives Layer B or derives SHACL shapes from Layer B MUST fail rather than guess when required semantics are not explicitly defined.

The canonicalization and projection rules for Layer B are defined in [SCHEMAS.md](SCHEMAS.md).

### 9.7 Codex→RDF Instance Graph Mapping

To support deterministic derived validation artifacts (including SHACL), Codex defines a canonical mapping from a parsed Codex document to an RDF instance graph.

The mapping MUST be deterministic and MUST NOT use RDF blank nodes.

The mapping requires an explicit `documentBaseIri` external input.

If `documentBaseIri` is missing, the mapping MUST fail.

#### 9.7.1 Document Node

The instance graph MUST include a single document node derived from `documentBaseIri`.

#### 9.7.2 Node Identity and Declared Identifiers

Each Concept instance in the Codex document MUST map to exactly one RDF node whose identity is a deterministic skolem IRI derived from its structural position within the document.

The RDF node IRI MUST NOT be derived from the Concept instance's declared `id` trait value.

If a Concept instance declares an `id` trait, that declared identifier MUST be represented as data via a dedicated predicate `codex:declaredId`.

#### 9.7.3 Entity Marker

If and only if a Concept instance is an Entity, the mapped RDF node MUST be marked as an Entity using a dedicated predicate `codex:isEntity`.

#### 9.7.4 Parent Link and Ordered Children

For each non-root Concept instance, the instance graph MUST include a parent link using a dedicated predicate `codex:parentNode`.

Where a Concept instance contains child Concepts, the instance graph MUST represent the ordered child sequence using explicit edge nodes that carry a stable numeric index.

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

Other aspects of the instance graph mapping not defined in this section (including the exact `nodeIri(...)` derivation) are defined in [SCHEMAS.md](SCHEMAS.md).

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

Codex permits derived validation artifacts expressed as SHACL.

If SHACL is used as a derived validation artifact format, the generated shapes MAY use SHACL-SPARQL.

The canonical projection algorithms and canonicalization rules for derived artifacts are defined in [SCHEMAS.md](SCHEMAS.md).

### 9.10 Failure Rules (No Guessing)

Schema processing, schema-driven validation, instance-graph mapping, and derived-artifact projection MUST fail rather than guess when required information is missing or ambiguous.

At minimum, processing MUST fail in any of the following cases:

- the schema authoring profile is missing, invalid, or mixed (see §9.4)
- a schema rule requires semantics not explicitly defined by this specification, the governing schema, or the schema-definition specification
- a required external input is missing
- an algorithm would require nondeterministic choice (including heuristic inference or “best effort”)
- a lookup token is required to resolve but does not have exactly one binding
- a derived validation artifact cannot be constructed without inventing missing definitions

---

## 10. Formatting and Canonicalization

### 10.1 Processing Phases

### 10.2 Canonical Form Requirement

### 10.3 Canonicalization Rules

### 10.4 Allowed vs Forbidden Transformations

### 10.5 Canonicalization Failures

---

## 11. Schema Definition Language

The schema definition language is defined by the Codex schema-definition model and its schema-to-validation projection.

The authoritative schema authoring profile rules and projection requirements are defined in [SCHEMAS.md](SCHEMAS.md).

---

## 12. Schema Loading and Bootstrapping

Schema loading and bootstrapping requirements are defined by the normative schema system described in [SCHEMAS.md](SCHEMAS.md).

---

## 13. Schema Versioning

Schema versioning requirements are defined by the normative schema system described in [SCHEMAS.md](SCHEMAS.md).

---

## 14. Validation Errors

### 14.1 Primary Error Class Requirement

### 14.2 Closed Set of Error Classes

### 14.3 Error Class Definitions

### 14.4 Fatality

### 14.5 Reporting Expectations

---

## Appendix A. Formal Grammar

### A.1 EBNF (Normative)

### A.2 PEG (Informative)

---

## Appendix B. CSS Named Colors (Informative)

The normative definition of CSS named color keywords is in the CSS Color Module specifications.

---

**End of Codex Language Specification v0.1**
