Status: NORMATIVE  
Lock State: UNLOCKED  
Version: 1.0.0 BETA  
Editor: Charles F. Munat

# Codex Language Specification — Version 1.0.0 BETA

This document is the authoritative language specification for Codex 1.0.0 BETA.

All normative requirements for Codex 1.0.0 BETA MUST appear exactly once in this document.

---

## 1. Front Matter

### 1.1 Scope

This specification normatively defines:

- the core language model (Concepts, Traits, Values, Content, and Entities)
- naming and identifier constraints
- literal value spellings
- surface form syntax and structural rules for `.cdx` documents
- formatting and canonicalization requirements
- schema-first parsing architecture
- schema definition, schema loading/bootstrapping, and schema versioning rules
- reference trait semantics
- well-formedness and schema validation error classification

Well-formedness checking does not require a schema; semantic validation does. See §2.5 for this distinction.

---

### 1.2 Non-Goals

Codex 1.0.0 BETA does not define:

- a programming, scripting, or templating language
- an execution model, runtime, or pipeline orchestration
- storage, querying, indexing, inference, or rendering behavior
- identifier base scoping, dereferencing, or external/base resolution mechanisms
- schema distribution, registry protocols, or migration mechanisms

Those concerns belong to consuming systems and tooling.

### 1.3 Normativity and Conformance

This document uses the capitalized keywords **MUST** and **MUST NOT** to indicate requirements.

Any statement that uses **MUST** or **MUST NOT** is normative.

Unless explicitly stated otherwise:

- Text labeled **Normative** defines required behavior.
- Text labeled **Informative** is explanatory and does not define requirements.
- Examples are illustrative and non-normative.

All statements that do not use **MUST** or **MUST NOT** are informative unless explicitly labeled **Normative**.

A conforming implementation satisfies every normative requirement in this specification. Given identical inputs, all conforming implementations MUST produce identical outputs.

#### 1.3.1 Consistency Guarantee

This specification contains no internal conflicts.

Appendix A.1 (EBNF) formalizes the syntactic rules described in the prose. The prose defines semantic meaning and processing obligations. These two forms address distinct concerns and do not conflict.

The bootstrap schemas (`bootstrap-schema/schema.cdx` and `bootstrap-schema/expanded/schema.cdx`) instantiate the schema-definition rules defined in this specification. They are derived artifacts, not independent sources of authority.

If an implementer discovers an apparent conflict between any parts of this specification or between this specification and the bootstrap schemas, that conflict is a defect. Implementers MUST NOT guess which source prevails. Implementers MUST report the defect.

---

## 2. Language Invariants

### 2.1 Declarative and Closed-World Model

Codex is a declarative language with closed-world semantics.

A conforming implementation MUST treat something not explicitly declared as not present.

An implementation MUST NOT infer meaning from omission, shape, or other non-specified cues.

An implementation MUST NOT assume defaults unless explicitly defined by this specification or by the governing schema.

Structural ordering (of Traits, children, and collection elements) carries no semantic meaning to Codex itself. Schemas define whether ordering is semantically significant for specific constructs. Implementations MUST preserve structural ordering both for round-trippability (see §2.6) and to support schema-defined ordering constraints.

### 2.2 Determinism and Explainability

Given the same inputs, a conforming implementation MUST produce the same results.

Required inputs are:

- document bytes
- governing schema (for validation; not required for well-formedness checking)
- document base IRI (for instance graph mapping; see §9.7)

In particular:

- Parsing MUST be deterministic.
- Well-formedness checking MUST be deterministic.
- Schema validation MUST be deterministic.
- Canonicalization MUST be deterministic.

An implementation MUST NOT exhibit non-deterministic or heuristic behavior.

For any well-formedness, schema validation, or canonicalization result, an implementation MUST be able to attribute the result to:

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
- Semantic validation MUST evaluate schema rules (including content-mode interpretation, constraints, value types, identity, and references) and MUST NOT be performed implicitly during parsing.

### 2.4 Target Agnosticism

Codex is target-agnostic. A Codex document can be transformed into other representations (RDF/SHACL, JSON, TOML, etc.).

Codex constructs and Codex-conforming tool behavior MUST NOT assume or require any particular target format, runtime, storage backend, inference system, rendering model, or execution semantics.

### 2.5 Well-Formedness and Validity

Codex distinguishes two independent questions:

* **Well-formedness**: whether a document is syntactically and structurally correct under this specification's surface-form grammar and structural rules.
* **Validity**: whether a well-formed document satisfies the semantic rules of a governing schema (including typing, authorization, value types, identity, references, and constraints).

Accordingly:

* A conforming implementation MUST be able to parse and check well-formedness without a governing schema.
* A conforming implementation MUST NOT perform schema validation without an explicit governing schema.

Well-formedness checking includes mechanically recognizing and classifying Value spellings into their Value kinds (and any grammar-defined subkinds) by applying this specification's surface-form grammar (§5 and Appendix A).

Expected types and type constraints for Trait values are schema-defined; checking a Trait value against its expected `ValueType` is part of schema validation and therefore requires an explicit governing schema.

The bootstrap schema-of-schemas provides a built-in governing schema only for schema documents (§12.4) and MUST NOT be used as a fallback governing schema for instance documents.

In this document, the term **schema validation** refers only to the schema-based semantic phase. When referring to the schema-free phase, this document uses **parse** and **check well-formedness**.

### 2.6 Round-Trippability

Round-trippability applies to the canonical form, not raw input. Raw input may use arbitrary whitespace or non-canonical formatting. Canonicalization (similar to `gofmt`) normalizes raw input to a single canonical surface form. Round-tripping preserves this canonical form.

A conforming implementation MUST support round-tripping: a canonicalized Codex document, after transformation to RDF triples, storage, retrieval via SPARQL, and reconstruction, MUST produce a byte-identical canonicalized document.

Formally: `canonicalize(original) = canonicalize(reconstruct(query(store(to_triples(validate(parse(canonicalize(original))))))))`

This invariant ensures that Codex serves as a lossless serialization format for RDF data. Structural ordering, annotations, and all surface-form details MUST survive the round-trip.

To guarantee round-trippability, a conforming implementation MUST include:

- canonicalization (raw bytes → canonical surface form)
- parsing (canonical surface form → AST)
- validation (AST + schema → IR)
- triple serialization (IR → RDF/SHACL triples)
- triple reconstruction (SPARQL query results → canonical Codex)

---

## 3. Core Model

### 3.1 Concept

A Concept is a named declarative construct and the primary structural unit of a Codex document.

A Concept instance MUST have exactly one Concept name.

A Concept instance MUST declare zero or more Traits.

A Concept instance MUST be in exactly one of two body modes:

- **children mode**: the Concept instance contains zero or more child Concepts and no Content.
- **content mode**: the Concept instance contains Content and no child Concepts.

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

A Concept instance is an Entity if and only if the governing schema declares `$MustBeEntity` for that Concept via its `entityEligibility` rule.

The governing schema MUST declare exactly one `entityEligibility` value for each Concept. The valid values are:

- `$MustBeEntity`: each instance of that Concept MUST declare an `id` Trait.
- `$MustNotBeEntity`: each instance of that Concept MUST NOT declare an `id` Trait.

If the governing schema does not declare `entityEligibility` for a Concept, schema validation MUST fail.

Codex-conforming formatting and canonicalization MUST NOT synthesize identity by adding an `id` Trait or inventing an identifier value.

### 3.6 Marker

A Marker is a syntactic delimiter for Concept instances in the surface form.

Markers MUST be one of:

- an opening marker,
- a closing marker, or
- a self-closing marker.

Markers MUST delimit Concept structure and nesting.

Each closing marker MUST match the most recent unclosed opening marker. If a closing marker does not match, or if any opening marker remains unclosed at end of input, the document MUST be rejected with a `ParseError` (§14).

A self-closing marker MUST represent a Concept with no children and no Content.

### 3.7 Annotation

An Annotation is author-supplied editorial metadata.

Annotations MUST NOT affect parsing, schema validation outcomes, or domain semantics.

Annotations MUST be preserved through Codex-conforming processing, subject only
to the surface-form normalization and canonicalization rules defined by this
specification.

---

## 4. Naming Rules

This section defines requirements for Concept names and Trait names.
Some requirements in this section are normative but not mechanically enforceable; such requirements bind schema authors and govern conformance, even where implementations cannot detect all violations.

### 4.1 Name Forms

For the purposes of Codex, this specification defines:

* **PascalCase**: a name composed only of ASCII letters and digits; the first character MUST be an ASCII uppercase letter.
* **camelCase**: a name composed only of ASCII letters and digits; the first character MUST be an ASCII lowercase letter.

A name MUST contain at least one character.

Concept names MUST use PascalCase.

Trait names MUST use camelCase.

No other casing is permitted.

### 4.2 Consecutive Uppercase Restriction

Concept names and Trait names MUST NOT contain three or more consecutive ASCII uppercase letters.

This restriction ensures that acronyms and initialisms are written as ordinary words with only the first letter capitalized (e.g., `AstNode`, not `ASTNode`). It also permits single-letter words in names (e.g., `ThisIsAThing` is valid because the transition from "A" to "Thing" produces only two consecutive uppercase letters).

### 4.3 Acronyms and Initialisms (Author Responsibility)

Authors MUST write acronyms and initialisms as single words with only the first letter capitalized.

This requirement binds schema authors. It is not fully mechanically enforceable because implementations cannot distinguish an incorrectly written acronym from a legitimate sequence of single-letter words.

| Correct | Incorrect | Mechanical rejection (§4.2) | Author intent |
|---------|-----------|----------------------------|---------------|
| `AstNode` | `ASTNode` | A-S-T-N = 4 consecutive | "AST" is one word |
| `HtmlParser` | `HTMLParser` | H-T-M-L-P = 5 consecutive | "HTML" is one word |
| `safeHtml` | `safeHTML` | H-T-M-L = 4 consecutive | "HTML" is one word |
| `ioStream` | `iOStream` | not rejected | "IO" is one word |

---

## 5. Value Literal Catalog

### 5.1 String Values

A String Value is a sequence of zero or more Unicode scalar values. An empty String Value (zero scalar values) is permitted.

In the Surface Form, String Values MUST be spelled as quoted string literals (see Appendix A) or backtick strings (see §5.2).

### 5.2 Backtick Strings

A Backtick String is a surface-form spelling of a String Value.

Within a Backtick String, `` \` `` represents a literal `` ` ``.

A backslash not immediately followed by a backtick is a literal backslash and has no special meaning.

After interpreting the Backtick String's escape sequences, the resulting character sequence MUST be transformed into the resulting String Value by applying the following whitespace normalization:

- Each maximal run of whitespace characters (spaces, tabs, and line breaks) MUST be replaced with a single U+0020 SPACE.
- Leading and trailing U+0020 SPACE MUST be removed.

The resulting String Value MUST be single-line.

### 5.3 Boolean Values

A Boolean Value is one of two values: true or false.

In the Surface Form, Boolean Values MUST be spelled as the tokens `true` and `false`.

No other spellings are permitted.

### 5.4 Numeric Values

Codex performs no arithmetic and no numeric normalization. Numeric spellings MUST be preserved exactly.

Integer components in Numeric Value spellings MUST NOT contain leading zeros, except that the single digit `0` is permitted. A sign character (if present) is not part of the integer component.

This requirement applies to:

- integer Numeric Values
- the integer component of Decimal Numbers
- the exponent digit sequence of Scientific Numbers
- the explicit precision suffix digit sequence (if present)
- fraction denominators

In the Surface Form, Numeric Values MUST be spelled using the numeric literal grammar defined by this specification.

Numeric Values MUST NOT include infinity, NaN, or other non-finite representations. Codex defines only finite numeric literals.

The literal spelling `-0` is permitted and MUST be preserved distinct from `0`.

The meaning of a Numeric Value beyond its literal spelling MUST be defined by the governing schema or consuming system.

#### 5.4.1 Precision-Significant Numbers

A precision-significant number is a Numeric Value spelled with a `p` suffix.

The declared precision (a count of decimal places) MUST be determined by one of the following mechanisms:

- Inferred precision: the count of decimal places in the literal spelling, including trailing zeros. A literal with no decimal point has 0 decimal places.
- Explicit precision: a non-negative integer following the `p` suffix, which overrides inferred precision.

Consuming systems MUST preserve the declared precision.

### 5.5 Enumerated Token Values

An Enumerated Token Value is a Value drawn from a schema-defined closed set.

In the Surface Form, Enumerated Token Values MUST be spelled with a leading `$` sigil followed by a token name. The token name MUST use PascalCase.

Enumerated Token Values MUST NOT be treated as String Values.

Enumerated Token Values MUST NOT be evaluated.

### 5.6 Temporal Values

A Temporal Value represents a declarative temporal literal.

In the Surface Form, Temporal Values MUST be spelled using `{...}`.

Temporal Values MUST conform to the Temporal Value grammar defined by this specification (see Appendix A.1.14 and Appendix A.2.15). The Temporal Value grammar defines the complete braced literal; the Temporal Body grammar defines the content within the braces.

Codex itself defines no temporal evaluation, normalization, ordering, time zone interpretation, or calendrical correctness requirements for Temporal Values. In canonical surface form, Temporal Values MUST be spelled exactly as parsed (no normalization).

Codex-conforming tools MUST NOT derive temporal meaning, perform evaluation, apply defaults, or check real-world correctness (for example, month length or leap seconds) except as explicitly defined by the governing schema or consuming system.

#### 5.6.1 Temporal Kind Determination (Normative)

To classify a Temporal Value as a specific temporal kind (for example, `ZonedDateTime` or `Date`), tools MUST parse the braced payload using the Temporal Body grammar in Appendix A.

This classification is purely syntactic and depends only on the braced payload; it does not imply temporal evaluation or interpretation.

The temporal kind MUST be determined by the first matching alternative in the following ordered list:

1. `ZonedDateTime`
2. `LocalDateTime`
3. `Date`
4. `YearMonth`
5. `MonthDay`
6. `Time`
7. `Duration`
8. `ReservedTemporal`

Temporal Values MUST NOT be treated as Enumerated Token Values, even when the braced payload is a reserved literal such as `now` or `today`.

### 5.7 Color Values

A Color Value MUST NOT be treated as a String Value.

Codex-conforming tools MUST NOT normalize, convert, or interpret Color Values beyond the well-formedness checks defined by this specification.

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

Hex digits in hexadecimal colors are case-insensitive for parsing. In canonical surface form, hexadecimal digits in Color Values MUST be lowercase.

Color function names are case-insensitive for parsing. In canonical surface form, color function names MUST be lowercase.

Color space tokens in `color(...)` are case-insensitive for parsing. In canonical surface form, color space tokens MUST be lowercase. The color space token MUST be one of:

- `srgb`
- `srgb-linear`
- `display-p3`
- `a98-rgb`
- `prophoto-rgb`
- `rec2020`
- `xyz`
- `xyz-d50`
- `xyz-d65`

#### 5.7.1 Named Color Values

In the Surface Form, a Named Color Value MUST be spelled as `&` followed immediately by a color name.

The color name MUST consist only of ASCII lowercase letters (`a` through `z`).

The color name MUST be one of the named color keywords defined in Appendix B.

### 5.8 UUID Values

A UUID Value is a 36-character unquoted token with the form:

`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

where each `x` is a hexadecimal digit.

A UUID Value MUST NOT be a String Value.

A UUID Value MUST NOT include braces, prefixes, or other delimiters.

Hyphens MUST appear at character positions 9, 14, 19, and 24 (1-indexed).

Hexadecimal digits in UUID Values are case-insensitive for parsing. In canonical surface form, UUID Values MUST be spelled using lowercase hexadecimal digits.

No UUID version is mandated.

### 5.9 IRI Reference Values

An IRI Reference Value is an unquoted token representing identity or reference.

An IRI Reference Value MUST contain a `:` character separating the scheme from the remainder.

In the Surface Form, IRI Reference Values MUST be spelled using the IRI reference grammar defined by this specification.

IRI Reference Values MUST permit non-ASCII Unicode characters directly and MUST permit percent-encoding, as defined for IRI-references by RFC 3987: https://www.rfc-editor.org/rfc/rfc3987.

IRI Reference Values MUST NOT contain Unicode whitespace characters.

IRI Reference Values MUST NOT contain Unicode control characters.

IRI Reference Values MUST NOT contain Unicode bidirectional control characters.

IRI Reference Values MUST NOT contain Unicode private-use characters.

An IRI Reference Value MUST NOT be a String Value.

IRI Reference Values MUST be compared as opaque strings.

Codex-conforming tools MUST NOT dereference IRI Reference Values.

Where this specification defines deterministic resolution (for example, lookup-token binding and reference-constraint resolution), tools MUST apply only the mechanisms defined by this specification and MUST NOT perform any external lookup, registry query, or network dereferencing.

### 5.10 Lookup Token Values

A Lookup Token Value is an unquoted token that binds to a schema-defined value.

In the Surface Form, Lookup Token Values MUST be spelled as `~` followed immediately by a token name.

The token name MUST use camelCase.

A Lookup Token Value MUST NOT be a String Value.

Codex-conforming tools MUST NOT dereference Lookup Token Values.

### 5.11 Character Values

A Character Value represents exactly one Unicode scalar value.

In the Surface Form, Character Values MUST be spelled as character literals delimited by single quotes (`'`). See Appendix A for the full grammar.

A Character Value MUST NOT be a String Value.

After interpreting the character literal's escape sequences, the resulting Character Value MUST contain exactly one Unicode scalar value.

### 5.12 List Values

A List Value is an ordered sequence of zero or more Value elements.

In the Surface Form, List Values MUST be spelled using square brackets (`[...]`). See Appendix A for the full grammar.

Each element of a List Value MUST be a Value.

A List Value MUST permit nesting.

A List Value MUST NOT require all elements to have the same Value kind.

A List Value MUST represent exactly the elements explicitly present in its literal spelling.

For schema-level type constraints on list contents, see §5.18.

### 5.13 Value Equality for Collection Uniqueness (Normative)

For purposes of detecting duplicates in Set Values and Map Values, Codex-conforming tools MUST use the following Value equality relation.

Equality is defined over parsed Values (after interpreting escape sequences, backtick-string whitespace normalization, and other value-specific decoding rules) and MUST NOT be defined over raw source bytes.

Two Values are equal if and only if they have the same Value kind and satisfy the following rules (recursively where applicable):

- String Values: equal if and only if they contain the same sequence of Unicode scalar values.
- Boolean Values: equal if and only if both are `true` or both are `false`.
- Numeric Values: equal if and only if their literal spellings are identical codepoint-for-codepoint.
- Enumerated Token Values: equal if and only if their literal spellings are identical codepoint-for-codepoint.
- Temporal Values: equal if and only if their literal spellings are identical codepoint-for-codepoint.
- Color Values: equal if and only if their literal spellings are identical, except that hexadecimal digits, color function names, and color space tokens are compared case-insensitively.
- UUID Values: equal if and only if they are identical after case-folding hexadecimal digits (i.e., hexadecimal digits are compared case-insensitively).
- IRI Reference Values: equal if and only if their spellings are identical codepoint-for-codepoint (see §5.9).
- Lookup Token Values: equal if and only if their literal spellings are identical codepoint-for-codepoint.
- Character Values: equal if and only if they contain the same Unicode scalar value.
- List Values and Tuple Values: equal if and only if they have the same length and corresponding elements are equal.
- Range Values: equal if and only if their start endpoints are equal, their end endpoints are equal, and either both omit a step or both include equal step Values.
- Set Values: equal if and only if they contain the same elements (under this equality relation), regardless of element order.
- Map Values: equal if and only if they contain the same bindings, where keys are equal and corresponding bound Values are equal, regardless of entry order.

### 5.14 Set Values

A Set Value is an unordered collection of zero or more Value elements. Set Values have no semantic ordering; however, in canonical surface form, elements MUST be serialized in the order they appear in the source spelling.

In the Surface Form, Set Values MUST be spelled using the `set` keyword followed by square brackets (`set[...]`). See Appendix A for the full grammar.

Each element of a Set Value MUST be a Value.

A Set Value MUST permit nesting.

A Set Value MUST NOT require all elements to have the same Value kind.

A Set Value MUST contain no duplicate elements.

Duplicate elements MUST be determined using the Value equality relation in §5.13.

If a set literal spelling contains duplicate elements, Codex-conforming tools MUST treat that spelling as an error.

For schema-level type constraints on set contents, see §5.18.

### 5.15 Map Values

A Map Value is a collection of key-value pairs. Map Values have no semantic ordering; however, in canonical surface form, entries MUST be serialized in the order they appear in the source spelling.

In the Surface Form, Map Values MUST be spelled using the `map` keyword followed by square brackets containing `key: value` entries (`map[key: value, ...]`). See Appendix A for the full grammar.

A Map Value MUST permit zero entries.

Each entry in a Map Value MUST bind exactly one key to exactly one Value.

A Map Value MUST permit nesting.

A Map Value MUST contain no duplicate keys.

Duplicate keys MUST be determined using the Value equality relation in §5.13.

If a map literal spelling contains duplicate keys, Codex-conforming tools MUST treat that spelling as an error.

For schema-level type constraints on map keys and values, see §5.18.

#### 5.15.1 Map Keys

In the Surface Form, a map key MUST be one of:

- an unquoted identifier key
- a String Value
- a Character Value
- an integer Numeric Value
- an Enumerated Token Value

An unquoted identifier key MUST use camelCase.

### 5.16 Tuple Values

A Tuple Value is an ordered sequence of one or more Value elements with positional semantics.

In the Surface Form, Tuple Values MUST be spelled using parentheses (`(...)`). See Appendix A for the full grammar.

A Tuple Value MUST contain at least one element.

Each element of a Tuple Value MUST be a Value.

A Tuple Value MUST permit nesting.

A Tuple Value MUST NOT require all elements to have the same Value kind.

For any Tuple Value used by a Trait, the governing schema MUST define the required arity and the meaning of each position.

For schema-level type constraints on tuple positions, see §5.18.

### 5.17 Range Values

A Range Value is a declarative interval.

In the Surface Form, Range Values MUST be spelled using `..` between endpoints, with an optional `s` suffix for step (`x..y` or `x..ysz` where `x` is the starting value, `y` is the ending value, and `z` is the step). See Appendix A for the full grammar.

A Range Value MUST contain a start endpoint and an end endpoint.

The start endpoint and end endpoint MUST be Values of the same base Value kind (e.g., both Integer, both String), independent of any parameterized type constraints.

A Range Value MUST contain either zero steps or one step.

If a step is present, the governing schema MUST define which Value kinds are valid for the step.

Range endpoints MUST be treated as inclusive.

Codex-conforming tools MUST NOT enumerate Range Values.

The semantics of a Range Value beyond these structural requirements MUST be defined by the governing schema or consuming system.

For schema-level type constraints on range bounds, see §5.18.

### 5.18 Parameterized Value Types

This section defines parameterized forms of collection value types, which constrain the types of their contents.

#### 5.18.1 Syntax

A parameterized value type consists of a base type token followed by type arguments in angle brackets.

The following collection types support parameterization:

* `$List<T>` — a list where each item conforms to `T`
* `$Set<T>` — a set where each item conforms to `T`
* `$Map<K, V>` — a map where keys conform to `K` and values conform to `V`
* `$Tuple<T1, T2, ...>` — a tuple where each position conforms to its corresponding type
* `$Range<T>` — a range where bounds conform to `T`

#### 5.18.2 Type Arguments

A type argument MUST be one of:

* A simple value type token (e.g., `$String`)
* A parameterized value type (e.g., `$List<$String>`)
* A type union (e.g., `[$String, $Integer]`)

A type union is a bracketed, comma-separated list of value type tokens. A value conforms to a type union if it conforms to any member type.

Type arguments MUST NOT contain whitespace.

#### 5.18.3 Unparameterized Collection Types

An unparameterized collection type (e.g., `$List` without `<...>`) permits items of any value type.

#### 5.18.4 Nesting

There is no limit on the nesting depth of parameterized types.

For example, `$List<$List<$String>>` specifies a list of lists of strings.

#### 5.18.5 Examples

| Type | Meaning |
|------|---------|
| `$List<$String>` | List of strings |
| `$List<[$String, $Boolean]>` | List where each item is a string or boolean |
| `$Set<$Integer>` | Set of integers |
| `$Map<$String, $List<$Integer>>` | Map from strings to lists of integers |
| `$Tuple<$String, $Integer, $Boolean>` | 3-tuple: (string, integer, boolean) |
| `$Range<$Integer>` | Range with integer bounds |
| `$List` | List of any values (unparameterized) |

---

## 6. Identity

### 6.1 Overview

Codex provides two mechanisms for referencing Concepts:

| Mechanism | Trait | Value Type | Scope |
|-----------|-------|------------|-------|
| Entity Identity | `id` | IRI Reference Value (§5.9) | Global |
| Concept Key | `key` | Lookup Token Value (§5.10) | Document |

### 6.2 Entity Identity

#### 6.2.1 The `id` Trait

Every Entity MUST have exactly one `id` trait.

Every non-Entity MUST NOT have an `id` trait.

The value of an `id` trait MUST be an IRI Reference Value (§5.9).

Codex-conforming tools MUST NOT synthesize an `id` trait.

#### 6.2.2 Uniqueness

Within a single document, each `id` value MUST be unique across all Entities.

Codex does not define a mechanism to enforce cross-document uniqueness; however, `id` values serve as RDF subject identifiers in triple stores and are expected to be globally unique in practice.

#### 6.2.3 Stability

Once an `id` value is assigned to an Entity, that `id` value MUST continue to refer to the same Entity.

Changing an Entity's `id` value MUST be treated as creating a new Entity.

### 6.3 Concept Keys

#### 6.3.1 The `key` Trait

A Concept MUST have zero or one `key` traits.

The value of a `key` trait MUST be a Lookup Token Value (§5.10).

Codex-conforming tools MUST NOT synthesize a `key` trait.

#### 6.3.2 Uniqueness

Within a single document, each `key` value MUST be unique across all Concepts.

Concept keys have document scope; cross-document key references are not defined by this specification.

#### 6.3.3 Resolution

When a Lookup Token Value appears as a reference trait value, resolution to an Entity `id` is performed via the binding mechanism defined in §9.8.

---

## 7. Reference Traits

### 7.1 Reference Traits Overview

Codex defines exactly three reference Traits:

- `reference`
- `target`
- `for`

Each reference Trait expresses a declarative relationship from a Concept instance to another Concept instance, identified by identity reference.

An identity reference is either an Entity `id` (an IRI Reference Value; §6.2) or a Concept `key` (a Lookup Token Value; §6.3) that is resolved as explicitly defined by this specification and the governing schema.

The value of each reference Trait MUST be either an IRI Reference Value (see §5.9) or a Lookup Token Value (see §5.10).

The value of a reference Trait MUST NOT be any other Value kind.

Reference Traits MUST be interpreted only as declarative relationships.

Reference Traits MUST NOT imply dereferencing, loading, execution, or transformation.

Reference Traits MUST NOT imply any automatic or external resolution beyond what is explicitly defined by this specification or the governing schema.

A Concept instance MUST NOT declare a reference Trait unless authorized by the governing schema.

Where reference Traits are authorized, the governing schema MUST define any additional semantics beyond the intent statements in this section.

The intent statements in §7.2–7.4 guide schema authors but are not normative requirements.

### 7.2 `reference`

The `reference` Trait expresses that a Concept instance mentions or depends on another Concept instance for meaning.

The `reference` Trait MUST NOT imply action, application, scope, execution, or transformation.

### 7.3 `target`

The `target` Trait expresses that a Concept instance is about, applied to, or oriented toward another Concept instance.

### 7.4 `for`

The `for` Trait expresses applicability, scope, specialization, or intended domain.

If a `for` reference is used to denote a Concept type, it MUST reference the `ConceptDefinition` Entity for that Concept by identity reference.

### 7.5 Singleton Rule

If a governing schema requires that at most one of `reference`, `target`, or `for` be present on a Concept instance, it MUST express that requirement using `ReferenceConstraint(type=ReferenceSingleton)`.

If a governing schema authorizes more than one reference Trait on the same Concept instance, it MUST document the permitted combinations and the intended interpretation.

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
<Bindings>
	<Bind key=~hobbit id=book:TheHobbit />
</Bindings>

<Book id=book:TheHobbit title="The Hobbit" />

<Tag id=tag:classicFantasy target=~hobbit name=$classicFantasy />
```

Example: using `for` to scope a rule/policy to a Concept type.

In this example, `LabelPolicy` is not about a particular `Book` instance; it is intended to apply to the `Book` Concept type.

```cdx
<Bindings>
	<Bind key=~book id=concept:Book />
</Bindings>

<ConceptDefinition id=concept:Book name="Book" />

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

Codex-conforming tools MUST treat bare CR (`\r`) as a parse error.

In canonical surface form, a Codex document MUST end with a trailing LF.

### 8.3 Indentation

Indentation is a canonical formatting requirement.

In canonical surface form, one tab character represents one level of nesting.

- A root Concept instance MUST have no indentation (column 0).
- Direct children of a root Concept instance MUST be indented by exactly one tab.
- Each additional nesting level MUST increase indentation by exactly one additional tab.

Codex-conforming formatters MUST normalize indentation before semantic validation proceeds.

Codex-conforming tools MUST NOT treat author indentation as authoritative.

In the Surface Form, indentation MUST use U+0009 TAB characters only.

Any U+0020 SPACE character that appears in the indentation prefix of any of the following lines MUST be treated as a `ParseError`:

- Concept marker lines
- Trait lines (including multi-line trait layout)
- non-blank content lines

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

An opening marker includes zero or more Traits.

If multiple Traits are present, their order MUST be preserved.

#### 8.5.2 Closing Marker

A closing marker MUST be spelled as:

```cdx
</ConceptName>
```

The closing marker MUST match the most recent unclosed opening marker (see §3.6).

The closing marker MUST appear on its own line after indentation.

Additional content MUST NOT appear on the closing marker line.

#### 8.5.3 Self-Closing Marker

A self-closing marker MUST be spelled as:

```cdx
<ConceptName />
<ConceptName trait=value />
```

A self-closing marker represents a Concept instance with no content and no child Concepts.

A self-closing marker includes zero or more Traits.

#### 8.5.4 Empty Block Concepts

Codex-conforming tools MUST treat the form `<ConceptName></ConceptName>` as a parse error.

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

When Traits are written on multiple lines, the closing `>` or `/>` MUST appear on its own line at the same indentation level as the opening `<`.

Example (canonical multiline opening marker):

```cdx
<Book
	id=book:TheHobbit
	title="The Hobbit"
	author="J.R.R. Tolkien"
>
	[children here]
</Book>
```

Example (canonical multiline self-closing marker):

```cdx
<Book
	id=book:TheHobbit
	title="The Hobbit"
	author="J.R.R. Tolkien"
/>
```

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

### 8.7.1 Multiline Value Literals

Codex-conforming tools MUST accept multiline spellings for Value literals that use balanced delimiters, including list (`[...]`), set (`set[...]`), map (`map[...]`), tuple (`(...)`), and range forms.

Within a balanced Value literal:

* Line breaks are treated as whitespace.
* Whitespace between elements, entries, or delimiters is not significant.
* Whitespace MUST NOT terminate the Value.

Outside of balanced delimiters, a Value literal MUST be fully contained on a single line.

Codex-conforming tools MUST determine Value boundaries solely by balanced delimiter matching and MUST NOT treat line boundaries as semantically significant within a Value literal.

### 8.8 Content Blocks

A Content Block is opaque text between an opening marker and a closing marker.

Content is not a Value.

Content MUST NOT be interpreted as Codex structure, Traits, or Values.

In canonical surface form, content lines MUST be indented one nesting level deeper than their enclosing Concept instance.

Content can contain blank lines and can span multiple lines.

#### 8.8.1 Content Termination

Codex-conforming tools MUST identify the end of content by scanning for the closing marker that matches the opening Concept name: `</ConceptName>`.

#### 8.8.2 Content Escaping

Within content:

- `\<` represents a literal `<`.
- `\[` represents a literal `[`.

A backslash not immediately followed by `<` or `[` is a literal backslash and has no special meaning.

A raw `<` character MUST NOT appear anywhere in content.

A raw `[` character MUST NOT appear as the first non-indentation character of a content line. This preserves schema-less determinism of content-versus-children body mode (see §10.2.1.1).

#### 8.8.3 Content Indentation Normalization

Codex-conforming tools MUST store and process content without its canonical leading indentation.

In canonical surface form, each non-blank content line MUST be indented exactly one nesting level deeper than its enclosing Concept instance.

For each non-blank content line, the canonical leading indentation is the exact leading indentation required to place that line at one nesting level deeper than its enclosing Concept instance.

Codex-conforming tools MUST remove exactly that canonical leading indentation from each non-blank content line when producing the logical content.

Codex-conforming tools MUST preserve all characters following the removed indentation, including any additional leading whitespace.

If a non-blank content line does not have the required canonical leading indentation after indentation normalization, Codex-conforming tools MUST fail with a formatting error.

Indentation normalization is schema-free and MUST be performed before schema-directed processing.

#### 8.8.4 Whitespace Mode Normalization

Whitespace mode normalization is schema-directed and MUST be performed during schema-directed processing.

The governing schema declares `whitespaceMode` on each Concept that allows content (see §11.4.2).

For `whitespaceMode=$Preformatted`:

* Codex-conforming tools MUST preserve all content whitespace exactly after indentation normalization.

For `whitespaceMode=$Flow`:

* Codex-conforming tools MUST collapse each run of whitespace characters (spaces, tabs, and line breaks) to a single U+0020 SPACE.
* Codex-conforming tools MUST trim leading and trailing whitespace from the resulting content.
* In canonical surface form, Codex-conforming tools MUST wrap content to lines of at most 100 Unicode scalar values, breaking at whitespace boundaries where possible.
* Each wrapped line MUST be indented exactly one nesting level deeper than the enclosing Concept instance.

Schema-less processing MUST treat all content as `$Preformatted` (preserve all whitespace after indentation normalization).

#### 8.8.5 Examples (Informative)

This section is informative.

Example: indentation stripping while preserving whitespace-sensitive content.

This example assumes `Verse` is defined with `whitespaceMode=$Preformatted`.

```cdx
<Verse>
	Buffalo Bill 's
	defunct
	        who used to
	        ride a watersmooth-silver
	                                  stallion
	and break onetwothreefourfive pigeonsjustlikethat
	                                                  Jesus

	he was a handsome man
	                      and what i want to know is
	how do you like your blueeyed boy
	Mister Death
</Verse>
```

The logical content is:

```
Buffalo Bill 's
defunct
        who used to
        ride a watersmooth-silver
                                  stallion
and break onetwothreefourfive pigeonsjustlikethat
                                                  Jesus

he was a handsome man
                      and what i want to know is
how do you like your blueeyed boy
Mister Death
```

(Poem: "Buffalo Bill 's" by e.e. cummings)

Example: escaping `<` inside content.

```cdx
<Tutorial>
	<Section title="Writing Descriptions">
		To write a description, use the Description Concept:

		\<Description>Your text here.\</Description>

		The text inside is opaque content.
	</Section>
</Tutorial>
```

Example: escaping `[` at the start of a content line.

```cdx
<Note>
	\[1] This footnote reference starts with a bracket.
	Normal [bracketed] text mid-line needs no escaping.
</Note>
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

Annotations can appear at top-level or within bodies interpreted as containing child Concepts.

Annotations MUST NOT appear inside Concept markers (that is, inside `<Concept …>`, `</Concept>`, or `<Concept />`).

Annotations can contain arbitrary text, including blank lines (block annotations only).

#### 8.9.2 Structural Rules

The opening `[` MUST be the first non-whitespace character on its line.

For an inline annotation, the closing `]` MUST appear on the same line.

For a block annotation:

* The line containing `[` MUST contain no other non-whitespace characters.
* The closing `]` MUST appear as the first non-whitespace character on its own line.
* The closing `]` line MUST contain no other non-whitespace characters.

#### 8.9.3 Escaping

Within an annotation:

* `\]` represents a literal `]`.

A backslash not immediately followed by `]` is a literal backslash and has no special meaning.

#### 8.9.4 Canonical Form

Canonicalization of annotations is deterministic and depends on the annotation form.

##### 8.9.4.1 Inline Annotation Canonicalization

Codex-conforming tools MUST canonicalize inline annotations as follows:

* Leading and trailing whitespace inside the brackets MUST be trimmed.
* Internal runs of whitespace (spaces, tabs, and newlines) MUST be collapsed to a single space.
* Escaped closing brackets MUST remain escaped (that is, `\]` MUST remain spelled as `\]`).

Canonical rendering MUST use no padding spaces just inside the brackets (for example, `[text]`, not `[ text ]`).

##### 8.9.4.2 Block Annotation Canonicalization

Block annotations MUST preserve their internal line structure.

Codex-conforming tools MUST normalize block-annotation line endings to LF.

A block annotation can include a directive (see §8.9.5) that controls additional canonicalization.

For a block annotation with no directive, Codex-conforming tools MUST:

* Remove trailing whitespace on each content line.
* Normalize indentation so that the content lines are indented exactly one tab deeper than the `[` / `]` lines.

#### 8.9.5 Block Annotation Directives

In a block annotation, the first non-blank content line can be a directive line.

If present, the directive line MUST be exactly one of:

* `FLOW:`
* `CODE:`
* `MARKDOWN:`

Directive recognition MUST be performed prior to any canonicalization other than newline normalization.

If present, the directive line MUST be preserved in canonical output.

Directive behavior:

* `CODE:` — Codex-conforming tools MUST preserve the block annotation bytes verbatim except for newline normalization.
* `MARKDOWN:` — Codex-conforming tools MUST preserve the block annotation bytes verbatim except for newline normalization.
* `FLOW:` — The flow-text value is the remaining content with leading and trailing whitespace trimmed, internal runs of whitespace collapsed to single spaces, and escapes interpreted per §8.9.3.

For `CODE:` and `MARKDOWN:` directives, Codex-conforming tools MUST NOT reindent, trim, strip trailing whitespace, wrap, or interpret escapes within the block annotation.

If no directive is present, the block annotation MUST be canonicalized as described in §8.9.4.2.

For `FLOW:` directives, Codex-conforming tools MUST render canonical output as follows:

* Split the remaining content into paragraphs separated by one or more blank lines.
* For each paragraph, wrap words to lines of at most 80 Unicode scalar characters using greedy packing.
* Indent each wrapped line exactly one tab deeper than the `[` / `]` lines.
* Separate paragraphs by exactly one blank line.

#### 8.9.6 Annotation Kinds

Codex defines three kinds of annotations:

1. Attached annotations — attach to a single Concept instance.
2. Grouping annotations — `GROUP` / `END` markers that bracket a region.
3. General annotations — standalone annotations (inline or block).

##### 8.9.6.1 Attached Annotations

An annotation is an attached annotation if and only if:

* It is not a grouping annotation.
* It appears immediately before a Concept opening marker.
* There is no blank line between the annotation and that marker.

An attached annotation can be either inline or block form.

Multiple attached annotations can stack.

Stacked attached annotations MUST be contiguous and MUST NOT be separated by blank lines.

An attached-annotation stack attaches to the next Concept opening marker.

##### 8.9.6.2 Grouping Annotations

A grouping annotation is a single-line annotation whose canonicalized annotation text matches one of the following forms:

* `GROUP: <label>`
* `END: <label>`

`<label>` MUST be a non-empty string after trimming.

Grouping recognition MUST be performed after applying the inline annotation canonicalization rules in §8.9.4.1.

Grouping annotations MUST NOT attach to Concept instances.

Grouping annotations define a purely editorial grouping region.

Grouping annotations can nest.

Label comparison MUST use the canonical label form (trimmed, with internal whitespace collapsed to single spaces).

Grouping annotations MUST conform to the canonical blank-line requirements in §8.9.8.

##### 8.9.6.3 General Annotations

An annotation is a general annotation if and only if:

* It is not an attached annotation.
* It is not a grouping annotation.
* It is surrounded by exactly one blank line above and exactly one blank line below, where file boundaries count as blank-line boundaries.

A general annotation can be either inline or block form.

General annotations MUST NOT attach to Concept instances.

#### 8.9.7 Group Nesting and Matching

Grouping annotations form a properly nested stack.

* `[GROUP: X]` pushes label `X`.
* `[END: X]` MUST match the most recent unmatched `[GROUP: X]`.

If an `END` label does not match the most recent open group label, or if an `END` appears with no open group, Codex-conforming tools MUST treat the document as invalid.

#### 8.9.8 Canonical Blank Line Requirements

In canonical surface form:

* Attached annotations MUST appear directly above the annotated Concept opening marker with no blank line.
* Grouping annotations MUST be surrounded by exactly one blank line above and below, where file boundaries count as blank-line boundaries.
* General annotations MUST be surrounded by exactly one blank line above and below, where file boundaries count as blank-line boundaries.

Codex-conforming tools MUST treat any annotation that is neither an attached annotation, a grouping annotation, nor a general annotation as invalid.

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

If an implementation performs schema-less checks, it MUST limit those checks to rules that are explicitly defined by this specification as independent of schema semantics.

Schema-less checks are limited to:

- determining whether the input bytes can be decoded as a permitted file encoding
- determining whether the input matches the surface-form grammar
- mechanically recognizing and classifying Value spellings into their Value kinds (and any grammar-defined subkinds) using the surface-form grammar
- enforcing surface-form structural well-formedness (including marker nesting/matching)
- enforcing surface-form canonicalization rules defined by this specification

Schema-less checks MUST NOT include any schema-driven semantic interpretation.

In particular, without a governing schema, an implementation MUST NOT:

- interpret content mode versus child mode for a concept beyond what is mechanically implied by the surface form
- interpret whether a concept instance is an Entity beyond the presence or absence of an `id` trait spelling
- evaluate trait meaning, trait authorization, expected `ValueType` constraints, value typing beyond surface-form Value recognition, or constraint logic
- resolve reference traits beyond their surface-form value type constraints

### 9.3 Schema-Required Semantic Validation

An implementation MUST NOT perform semantic validation without a governing schema.

Given a governing schema, an implementation MUST perform semantic validation as defined by that schema.

Schema-driven semantic validation MUST be explainable in terms of the specific schema rule(s) applied.

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

### 9.4 Authoring Modes (Guardrail)

A schema document MUST be validated under exactly one authoring mode.

Codex defines two authoring modes:

- **Simplified Authoring Mode**: Layer A schema authoring only
- **Canonical Authoring Mode**: Layer B schema authoring only

All conforming implementations MUST support the Simplified Authoring Mode.

All conforming implementations MUST support the Canonical Authoring Mode.

A schema document MUST NOT mix modes.

The authoring mode MUST be selected by an explicit declaration in the schema document.

The schema document's root `Schema` concept MUST have an `authoringMode` trait.

`authoringMode` MUST be exactly one of:

- `$SimplifiedMode`
- `$CanonicalMode`

If `authoringMode` is missing or has any other value, schema processing MUST fail.

Additional guardrails MUST hold:

- Simplified mode schemas MUST contain exactly one `ConceptDefinitions` and MUST NOT contain `RdfGraph`.
- Canonical mode schemas MUST contain exactly one `RdfGraph` and MUST NOT contain Layer A schema-definition concepts (including `ConceptDefinitions`, `TraitDefinitions`, `EnumeratedValueSets`, `ConstraintDefinitions`, `ValueTypeDefinitions`, and `ValidatorDefinitions`).
- Layer A expansion MUST generate a canonical Layer B graph; different Layer A spellings that are semantically identical MUST expand to byte-identical Layer B graphs.
- Layer B canonicalization MUST make semantically identical graphs byte-identical.

### 9.5 Layer A (Codex-Native Schema Authoring)

Layer A is the Codex-native schema authoring model defined by the schema-definition specification.

Layer A schema authoring MUST satisfy the Codex language invariants, including closed-world semantics, determinism, and prohibition of heuristics.

Layer A authoring is the required authoring form for the Simplified Authoring Mode.

To support a total, deterministic projection to derived validation artifacts, simplified-mode schema authoring MUST additionally support the following extensions.

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

`ValidatorDefinition` names MUST be unique within the Schema.

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

### 9.8 Lookup Token Bindings (Normative)

Lookup Token Values (`~name`) are symbolic references that require an explicit binding to a target identifier in order to be resolved.

A document MAY declare lookup token bindings using a document-level binding section.

#### 9.8.1 Binding Section Surface Form

A binding section is declared using a top-level `Bindings` Concept.

The `Bindings` Concept:

* MUST appear at the top level of the document
* MUST NOT be nested inside any other Concept
* MUST NOT contain Content
* MUST contain one or more `Bind` child Concepts

#### 9.8.2 `Bind`

A `Bind` Concept declares a single lookup binding.

##### Traits (Normative)

* `key` (required; Lookup Token Value; §5.10)
* `id` (required; IRI Reference Value; §5.9)

Each `Bind` Concept binds the specified lookup token (`key`) to the specified Entity identity (`id`).

##### Constraints

* Each lookup token key MUST be bound at most once within a document.
* If a lookup token is used in the document and is required to be resolved by the governing schema, a corresponding binding MUST be present.
* Lookup token bindings MUST NOT be inferred, synthesized, or imported implicitly.

#### 9.8.3 Resolution Semantics

When lookup token resolution is required by schema validation:

* The binding table MUST be constructed from the `Bindings` section.
* A lookup token MUST resolve to exactly one identifier.
* If no binding is found for a required lookup token, validation MUST fail with a `ReferenceError`.
* If duplicate bindings for the same lookup token are present, validation MUST fail with a `SchemaError`.

Lookup token bindings are declarative only and MUST NOT imply loading, dereferencing, or execution.

#### 9.8.4 Schema Interaction

A governing schema MUST specify, for each context where lookup token values are permitted, one of the following resolution requirements:

* The lookup token MUST be resolvable.
* The lookup token MUST NOT appear in the context.
* Resolution is not required.

These requirements are enforced during schema validation, not during parsing or formatting.

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
- For the `$k$`-th visited node (1-indexed), allocate a node-local suffix `$k$`.
- Any internal variable introduced while translating that node MUST append suffix `$k$` to a base name.
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

#### 9.9.6 Identity Constraints

If a derived SHACL artifact encodes an identity constraint requiring an entity, it MUST emit:

- Let `S` be the owning node shape for the constraint. The property shape IRI MUST be `PS = predicatePropertyShapeIri(S, codex:isEntity)`.
- `(PS, sh:path, codex:isEntity)`
- `(PS, sh:hasValue, "true"^^xsd:boolean)`

If a derived SHACL artifact encodes an identity constraint requiring a non-entity, it MUST emit:

- Let `S` be the owning node shape for the constraint. The property shape IRI MUST be `PS = predicatePropertyShapeIri(S, codex:isEntity)`.
- `(PS, sh:path, codex:isEntity)`
- `(PS, sh:hasValue, "false"^^xsd:boolean)`

Derived validation artifacts MUST support `IdentityConstraint(type=IdentifierUniqueness, scope=S)`.

The `scope` trait MUST be present. For derived artifact purposes, `IdentityConstraint(type=IdentifierUniqueness, scope=S)` MUST be treated as `UniqueConstraint(trait=id, scope=S)` and MUST follow §9.9.7.

Derived validation artifacts MUST support `IdentityConstraint(type=IdentifierForm, pattern=p, flags=f)`.

Because `codex:declaredId` is represented as an RDF IRI term (see §9.7.7), this constraint MUST be expressible using SHACL-SPARQL.
It MUST report a violation if the focus node is an Entity and either:

* it has no `codex:declaredId`, or
* `STR(codex:declaredId)` does not match `p` under SPARQL 1.1 `REGEX` semantics (using flags `f` if present).

One conforming boolean condition for the SHACL-SPARQL constraint is:

```
EXISTS {
	focusVar codex:declaredId ?idK .
	FILTER(
		REGEX(STR(?idK), p, f)
	)
}
```

where `p` is the required pattern and `f` is the flags string if present. If `flags` is absent, the generated constraint MUST use the 2-argument `REGEX(text, pattern)` form.

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

`ContextConstraint(type=OnlyValidUnderParent)` MUST be expressible in derived validation artifacts.

`OnlyValidUnderParent` requires that the focus node's immediate parent is of the type specified by `TargetContext` in the constraint's `Targets` block. The `contextSelector` trait MUST NOT be present.

If projected into a SHACL-derived artifact, it MUST map to SHACL-SPARQL and MUST report a violation when the focus node has no direct parent of the target context type.

One conforming boolean condition for the SHACL-SPARQL constraint is:

```
EXISTS {
	focusVar <codex:parentNode> ?pK .
	?pK rdf:type <conceptClassIri(TargetContext)> .
}
```

`ContextConstraint(type=OnlyValidUnderContext, contextSelector=A)` MUST be expressible in derived validation artifacts.

`OnlyValidUnderContext` requires that the focus node has an ancestor of type `A` somewhere in its parent chain. The `contextSelector` trait MUST be present and specifies the required ancestor type.

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

1. Check the derived `RdfGraph` against the derived-artifact structural rules.
2. Emit the triples in a chosen RDF concrete syntax (for example, Turtle).

The projection MUST NOT change the set of triples.

### 9.10 Failure Rules (No Guessing)

Schema processing, schema-driven validation, instance-graph mapping, and derived-artifact projection MUST fail rather than guess when required information is missing or ambiguous.

At minimum, processing MUST fail in any of the following cases:

- the schema authoring mode is missing, invalid, or mixed (see §9.4)
- a schema rule requires semantics not explicitly defined by this specification, the governing schema, or the schema-definition specification
- a required external input is missing
- an algorithm would require nondeterministic choice (including heuristic inference or “best effort”)
- a lookup token is required to resolve but does not have exactly one binding
- a derived validation artifact cannot be constructed without inventing missing definitions

### 9.11 Layer A → Layer B Expansion Algorithm (Total)

This section defines a deterministic, total expansion algorithm from the Simplified Authoring Mode (Layer A) schema authoring to canonical Layer B (`RdfGraph`) suitable for derived validation artifacts (including SHACL and SHACL-SPARQL).

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

###### 9.11.6.3.2 Quantifier Semantics (Revised — `OnPathCount`)

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

`OnPathCount(path, r, minCount=m?, maxCount=n?)` MUST translate to a COUNT-based boolean condition.

If both `minCount` and `maxCount` are absent, expansion MUST fail.

The expansion MUST introduce a subquery that binds a single variable `?countK` and MUST then apply all required comparisons to `?countK` using a `FILTER` expression.

A conforming translation MUST have the following canonical form:

```
{
	SELECT (COUNT(?xVar) AS ?countK)
	WHERE {
		B(path, focusVar, xVar)
		FILTER( H(r, ctxChild, xVar) )
	}
}
FILTER(
	(minCountPresent ? (?countK >= m) : true)
	&&
	(maxCountPresent ? (?countK <= n) : true)
)
```

Where:

* `?countK` MUST be deterministically allocated according to §9.11.6.2.2.
* The subquery MUST appear in the same `WHERE` block as the enclosing constraint.
* The `FILTER` expression applying the count comparisons MUST appear immediately after the subquery.
* No other bindings or filters MAY intervene between the subquery and its associated `FILTER`.

The resulting boolean condition MUST evaluate to true if and only if the count constraints hold.

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

### 10.2.1.1 Schema-less Content Mode Determination (Normative)

In schema-less formatting and canonicalization mode, the parser MUST determine a Concept instance’s body mode mechanically as follows:

* Let the body lines be the lines between the Concept instance's opening marker and its matching closing marker (or empty for a self-closing marker).
* Ignore blank lines.
* Consider only lines at exactly one nesting level deeper than the enclosing Concept instance after indentation normalization.

The body MUST be classified according to the following rules:

* If there are no non-blank body lines, the body MUST be treated as children mode.
* If any non-blank considered line begins with `<` (Concept marker) or `[` (annotation), the body MUST be treated as children mode.
* Otherwise, the body MUST be treated as content mode.

Lines beginning with the escape sequences `\<` or `\[` are content, not structural markers.

If the body is classified as children mode but contains any non-blank considered line that is neither a valid Concept marker line (§8.5) nor a valid annotation line (§8.9), the document MUST be rejected with a `ParseError`.

This determination is purely mechanical and MUST NOT depend on schema knowledge, heuristics, or inferred intent.

If subsequent schema-based validation determines that the mechanically determined body mode is not permitted for the Concept, validation MUST fail with a `SchemaError`.

#### 10.2.2 Full Validation Pipeline (Normative)

To validate a document under a schema, a conforming tool MUST follow this sequence:

1. Decode + newline normalization
2. Formatting + canonicalization (mandatory) — using the schema-less mode defined in §10.2.1
3. Schema resolution — obtain the governing schema for the document (§12)
4. Semantic validation — schema rule evaluation (constraints, value types, identity, references)

Schema resolution is required before semantic validation.

### 10.3 Parse Errors vs Formatting Errors (Normative)

#### 10.3.1 Parse Errors

During formatting + canonicalization, a failure MUST be classified as `ParseError` (§14) when input cannot be read into the syntactic structure required to produce a parsed document model (AST) as defined by the Codex surface form.

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

Canonicalization is divided into two phases:

**Phase 1 (schema-free)** applies to all documents:

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
- content indentation normalization (§8.8.3)

**Phase 2 (schema-directed)** applies during schema-directed processing:

- content whitespace mode normalization per `whitespaceMode` declaration (§8.8.4)

Schema-less processing MUST complete Phase 1 only. Schema-directed processing MUST complete both phases.

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
- Normalize UUID spelling to the canonical form required by §5.8

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

Formatting error reports MUST include at minimum:

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

This section normatively defines the schema definition language for Codex 1.0.0 BETA.

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

### 11.1 Purpose

This section normatively defines the **schema definition language for Codex**.

It specifies how **schemas themselves are authored in Codex**, using the same surface form, parsing rules, and language invariants as instance documents.

The purposes of the schema definition language are to:

* make schemas **first-class Codex data**
* define all schema semantics **declaratively**
* ensure schema validation satisfies the Codex language invariants, including closed-world semantics, determinism, and prohibition of heuristics
* enable schemas to validate other schemas (bootstrapping)
* support deterministic expansion to derived validation artifacts (including SHACL)

Schemas authored using this language are authoritative.

Derived representations (for example, SHACL or RDF graphs) MUST NOT introduce semantics not explicitly defined by the schema definition language and this specification.

The Codex language invariants governing schema-first processing, determinism, and failure rules are defined in §9.

The schema definition language is bootstrapped by a built-in **schema-of-schemas**, which itself is expressed using this language. See §12.4.

---

### 11.2 Core Principles

The schema definition language obeys the same language invariants as Codex instance documents.

The following principles are normative:

* Schemas are **declarative data**, not executable programs.
* All authorization is **explicit**; nothing is implied or inferred.
* All constraints are **mechanically enforceable**.
* Schema semantics MUST be **closed-world**, **deterministic**, and **free of heuristics**.
* Any schema rule whose semantics cannot be expressed deterministically under this specification MUST cause schema processing to fail.

Schema validation, schema expansion, and derived-artifact generation MUST satisfy the schema-first requirements defined in §9.

Schemas MUST NOT rely on tool-specific behavior, implicit defaults, or external interpretation beyond what is explicitly defined by this specification and the governing schema-of-schemas.

---

### 11.3 Schema

A `Schema` Concept defines a governing Codex schema.

A `Schema` document is the authoritative source of semantic meaning, authorization, and validation rules for Codex documents validated under it.

A schema itself is validated as Codex data under the schema-of-schemas.

#### Traits (Normative)

A `Schema` Concept MUST declare the following Traits:

* `id` (required; IRI Reference Value)
  The globally unique identifier for the schema. This value is used as `schemaIri` throughout schema processing, instance-graph mapping, and derived-artifact generation.

* `version` (required; String Value)

  A schema version identifier whose ordering is defined by `versionScheme`.

* `versionScheme` (required; Enumerated Token Value)

  Declares the version comparison scheme used to order schema versions within the schema lineage. Allowed values and comparison rules are defined in §13.4.

* `compatibilityClass` (required; Enumerated Token Value)
  One of:

  * `$BackwardCompatible`
  * `$ForwardCompatible`
  * `$Breaking`

The following Traits are optional:

* `title` (optional; String Value)
* `description` (optional; String Value)

The `Schema` Concept MUST declare exactly one authoring mode via the `authoringMode` Trait, as defined in §9.4.

If `authoringMode` is missing, invalid, or mixed, schema processing MUST fail.

All conforming implementations MUST support both the Simplified Authoring Mode and the Canonical Authoring Mode (see §9.4).

#### Children (Normative)

A `Schema` MUST satisfy the mode-conditional child-Concept rules defined in §9.4.

For `authoringMode=$SimplifiedMode`:

* A `Schema` MUST contain exactly one `ConceptDefinitions` child Concept.
* A `Schema` MAY contain the following child Concepts, in any order:

  * `TraitDefinitions`
  * `EnumeratedValueSets`
  * `ConstraintDefinitions`
  * `ValueTypeDefinitions`
  * `ValidatorDefinitions`

* A `Schema` MUST NOT contain `RdfGraph`.

For `authoringMode=$CanonicalMode`:

* A `Schema` MUST contain exactly one `RdfGraph` child Concept.
* A `Schema` MUST NOT contain any of the following child Concepts:

  * `ConceptDefinitions`
  * `TraitDefinitions`
  * `EnumeratedValueSets`
  * `ConstraintDefinitions`
  * `ValueTypeDefinitions`
  * `ValidatorDefinitions`

No other child Concepts are permitted.

Each container Concept listed above MUST obey the structural, identity, and content rules defined by this specification and the schema-of-schemas.

#### Semantic Requirements

* A `Schema` Concept is an Entity and therefore MUST declare an `id`.
* All Concept, Trait, ValueType, and Constraint identifiers used within the schema MUST be resolvable and unique where required.
* A schema MUST be self-contained except for explicitly declared external inputs permitted by this specification.
* A schema MUST be valid under exactly one authoring mode (see §9.4).
* Any schema whose structure or semantics cannot be interpreted deterministically under this specification MUST be rejected.

The `Schema` Concept defines the boundary within which schema-first parsing, validation, instance-graph mapping, and derived-artifact generation occur, as specified in §9.

---

### 11.4 Concept Definitions

This section defines how Codex Concepts are declared in schemas.

#### 11.4.1 `ConceptDefinition`

A `ConceptDefinition` declares a Concept class and its structural, semantic, and identity rules.

A `ConceptDefinition` is an Entity.

##### Traits (Normative)

* `id` (required; IRI Reference Value)
* `key` (optional; Lookup Token Value)
* `name` (required; Concept name string, per §4 Naming Rules)
* `conceptKind` (required; `$Semantic | $Structural | $ValueLike`)
* `entityEligibility` (required; `$MustBeEntity | $MustNotBeEntity`)

##### Children (Normative)

A `ConceptDefinition` MAY contain, in any order:

* `ContentRules` (optional)
* `TraitRules` (optional)
* `ChildRules` (optional)
* `CollectionRules` (optional)

No other children are permitted.

If a child section is omitted, its default behavior applies as defined below.

---

#### 11.4.2 `ContentRules`

`ContentRules` declares whether instances of the Concept are in content mode or children mode.

This declaration is schema-authoritative and MUST be consulted before parsing Concept bodies in schema-directed processing (§9).

##### Children (Normative)

Exactly one of:

* `AllowsContent` — instances are in content mode
* `ForbidsContent` — instances are in children mode

###### `AllowsContent`

Traits:

* `whitespaceMode` (required; Enumerated Token Value)

`whitespaceMode` MUST be one of:

* `$Preformatted` — content whitespace is significant and MUST be preserved exactly (e.g., source code, poetry)
* `$Flow` — content whitespace is not significant; Codex-conforming tools MUST collapse runs of whitespace to single spaces and trim leading/trailing whitespace

###### `ForbidsContent`

`ForbidsContent` has no traits.

##### Defaults

If `ContentRules` is omitted, `ForbidsContent` applies.

---

#### 11.4.3 `TraitRules`

`TraitRules` declares which Traits are permitted, required, or forbidden on instances of the Concept.

##### Children (Normative)

One or more of:

* `RequiresTrait`
* `AllowsTrait`
* `ForbidsTrait`

If no trait rules are needed, omit the `TraitRules` container entirely.

Each rule applies to exactly one trait name.

###### `RequiresTrait`

Traits:

* `name` (required; Trait name string, per §4)

###### `AllowsTrait`

Traits:

* `name` (required; Trait name string, per §4)

###### `ForbidsTrait`

Traits:

* `name` (required; Trait name string, per §4)

##### Defaults

* Traits not explicitly allowed or required are forbidden.
* If `TraitRules` is omitted, no Traits are permitted except:

  * `id`, when permitted or required by `entityEligibility`
  * `key`, when applicable by schema rules

---

#### 11.4.4 `ChildRules`

`ChildRules` declares which child Concepts are permitted, required, or forbidden beneath instances of the Concept.

##### Children (Normative)

One or more of:

* `AllowsChildConcept`
* `RequiresChildConcept`
* `ForbidsChildConcept`

If no child rules are needed, omit the `ChildRules` container entirely.

###### `AllowsChildConcept`

Traits:

* `conceptSelector` (required; Concept name string)
* `min` (optional; non-negative integer; default `0`)
* `max` (optional; positive integer; omitted means unbounded)

###### `RequiresChildConcept`

Traits:

* `conceptSelector` (required; Concept name string)
* `min` (optional; positive integer; default `1`)
* `max` (optional; positive integer; omitted means unbounded)

`RequiresChildConcept` is semantically equivalent to `AllowsChildConcept` with `min = 1`.

###### `ForbidsChildConcept`

Traits:

* `conceptSelector` (required; Concept name string)

##### Defaults

Child Concepts not explicitly allowed or required are forbidden.

---

#### 11.4.5 `CollectionRules`

`CollectionRules` declares collection semantics for Concepts whose children form a logical collection.

These semantics inform schema validation and deterministic graph mapping (§9).

##### Traits (Normative)

* `ordering` (required; `$Ordered | $Unordered`)
* `allowsDuplicates` (required; boolean)

##### Form

`CollectionRules` MUST be self-closing and MUST NOT have children.

##### Applicability

If `CollectionRules` is present:

* Child ordering and duplication semantics MUST be enforced as declared.
* Any schema rule that depends on collection semantics MUST refer to this declaration.

If `CollectionRules` is absent, no collection semantics are assumed.

##### Ordering Semantics (Normative)

The `ordering` trait on `CollectionRules` specifies whether the order of children in a collection is semantically significant.

Ordering MUST be exactly one of:

###### `$Ordered`

A collection with `ordering=$Ordered` has semantically significant order.

Source order MUST be preserved through all conforming processing.

Conforming implementations MUST NOT reorder children of an `$Ordered` collection.

Two `$Ordered` collections with identical children in different orders MUST be treated as semantically distinct.

Validation and comparison of `$Ordered` collections MUST be order-sensitive.

###### `$Unordered`

A collection with `ordering=$Unordered` has no semantically significant order.

Conforming implementations MUST preserve source order during parsing and general processing.

Validation of `$Unordered` collections MUST be order-insensitive.

Semantic comparison of `$Unordered` collections MUST be order-insensitive: two `$Unordered` collections with identical children in different orders MUST be treated as semantically equivalent.

In canonical surface form, children of an `$Unordered` collection MUST be sorted according to the deterministic ordering defined by the canonicalization rules in §8.

---

This section is normative.

---

### 11.5. Trait Definitions

#### 11.5.1 `TraitDefinition`

Defines a Trait independently of any Concept.

Trait definitions establish the value type and constraints for a Trait that may be used across multiple Concepts.

###### Traits (Normative)

* `id` (optional; IRI reference)
* `name` (required; Trait name string per §4 Naming Rules)
* `defaultValueType` (required unless `defaultValueTypes` is provided; value type token, optionally parameterized per §5.17)
* `defaultValueTypes` (required unless `defaultValueType` is provided; list of one or more value type tokens, optionally parameterized per §5.17)
* `isReferenceTrait` (optional; boolean)
* `priority` (optional; enumerated token; presentation hint)

`isReferenceTrait` is schema metadata only. It MUST NOT change the definition of reference Traits in §7, and it MUST NOT change the reference constraint semantics in §9.9.9–§9.9.12.

If both `defaultValueType` and `defaultValueTypes` are provided, the implementation MUST treat that as a schema error.

`priority` is a meta-schema concern. Implementations MUST NOT use `priority` to change validation or compilation semantics. Meta-schemas MAY constrain allowed `priority` values (e.g., `$Primary`, `$Secondary`).

##### Value Type Semantics (Normative)

When a trait is present on a Concept instance, its value MUST conform to the declared value type.

If `defaultValueType` specifies a single type, the value MUST conform to that type.

If `defaultValueTypes` specifies multiple types, the value MUST conform to exactly one of the listed types.

##### Collection Type Semantics (Normative)

If a trait's value type is a parameterized collection type (e.g., `$List<$String>`), each element of the collection MUST conform to the declared item type.

If a trait's value type is an unparameterized collection type (e.g., `$List`), elements MAY be of any type.

If a trait's value type is a union containing both scalar and collection types (e.g., `[$String, $List<$String>]`), the value MUST conform to exactly one member of the union.

##### Trait Presence

Whether a trait must, may, or must not appear on a Concept instance is governed by `TraitRules` (`RequiresTrait`, `AllowsTrait`, `ForbidsTrait`), not by its value type.

##### Children (Optional)

* `AllowedValues` — constrains the set of valid values

##### Example

```cdx
<TraitDefinition
	name="amount"
	defaultValueType=$Number
/>

<TraitDefinition
	name="unit"
	defaultValueType=$EnumeratedToken
>
	<AllowedValues>
		<ValueIsOneOf values=[$Grams, $Kilograms, $Milliliters, $Liters, $Units] />
	</AllowedValues>
</TraitDefinition>

<TraitDefinition
	name="tags"
	defaultValueType=$List<$String>
/>

<TraitDefinition
	name="role"
	defaultValueTypes=[$String, $List<$String>]
/>
```

---

#### 11.5.2 `AllowedValues`

Constrains the values a Trait may accept.

##### Children (Normative)

One or more value constraints:

* `ValueIsOneOf` — value must be in explicit list
* `EnumeratedConstraint` — value must be member of named enumeration

##### `ValueIsOneOf`

###### Traits

* `values` (required; list of allowed values)

##### `EnumeratedConstraint`

###### Traits

* `set` (required; name of an `EnumeratedValueSet`)

---

### 11.6 Value Types

This section defines how schemas constrain the **Value types** permitted for Trait values.

Value types in schemas are **classifiers**, not evaluators. They constrain which surface-form Value spellings (§5) are permitted and how those values may participate in schema-defined constraints.

#### 11.6.1 Built-In Value Type Tokens (Normative)

Schemas MAY reference the following built-in value type tokens.

Each token corresponds to a Value category defined in §5 (Value Literal Catalog).

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
* `$List`
* `$Set`
* `$Map`
* `$Tuple`
* `$Range`

A built-in value type token constrains only **surface-form validity and structural classification**.
It MUST NOT imply evaluation, normalization, or conversion beyond what is defined in §5.

See §2.5 and §9.2 for the distinction between schema-less Value-kind classification and schema validation of expected `ValueType` constraints.

If a schema constrains a value using a built-in value type token, and a Trait value does not match that Value type’s surface grammar, schema-driven validation MUST fail.

---

#### 11.6.2 `ValueTypeDefinition` (Optional)

A `ValueTypeDefinition` defines a **schema-specific named value type** with additional validation semantics.

Schema-defined value types are referenced using Enumerated Token Values whose name matches the `ValueTypeDefinition.name`.

##### Container

`ValueTypeDefinitions` is a container Concept holding one or more `ValueTypeDefinition` children.

##### Traits (Normative)

* `id` (optional; IRI Reference Value)
* `name` (required; Concept name string per §4 Naming Rules)
* `baseValueType` (required; built-in value type token)
* `validatorName` (optional; Enumerated Token Value identifying a `ValidatorDefinition`)

`ValueTypeDefinition` names MUST be unique within the Schema.

The `baseValueType` defines the surface-form Value category.

If `validatorName` is present, schema-driven validation MUST apply the referenced validator as specified in §9.5.2 and §9.11.6.6.

If `validatorName` cannot be resolved to exactly one `ValidatorDefinition`, schema processing MUST fail.

A `ValueTypeDefinition` MUST NOT change the surface grammar of its `baseValueType`.

---

#### 11.6.3 Enumerated Value Sets

Schemas MAY define named sets of Enumerated Token Values.

Enumerated value sets are used exclusively by constraints and Trait definitions; they do not introduce new Value types.

##### Container

`EnumeratedValueSets` is a container Concept holding one or more `EnumeratedValueSet` children.

##### `EnumeratedValueSet`

Defines a closed set of enumerated tokens.

###### Traits (Normative)

* `name` (required; Concept name string per §4 Naming Rules)

###### Children (Normative)

One or more `Member` children.

##### `Member`

Defines one member of an enumerated value set.

###### Traits (Normative)

* `value` (required; token name without `$`)
* `label` (optional; String Value)
* `description` (optional; String Value)

Each `value` MUST be unique within its `EnumeratedValueSet`.

---

#### 11.6.4 Built-In Enumerated Value Sets (Normative)

The following enumerated value sets are defined by the Codex language itself and MUST be recognized by all conforming implementations.

##### `ConceptKind`

* `$Semantic`
* `$Structural`
* `$ValueLike`

##### `EntityEligibility`

* `$MustBeEntity`
* `$MustNotBeEntity`

##### `CompatibilityClass`

* `$BackwardCompatible`
* `$ForwardCompatible`
* `$Breaking`

##### `Ordering`

* `$Ordered`
* `$Unordered`

##### `Cardinality`

* `$Single`
* `$List`

These enumerated sets are authoritative and MUST NOT be redefined by schemas.

---

### 11.7 Constraint Model

This section defines the **schema constraint model** used to express semantic validation rules.

Constraints are **declarative**, **closed-world**, and **deterministic**.
They describe conditions that MUST hold for a document to be valid under a governing schema.

Constraints:

* MUST NOT execute code
* MUST NOT depend on implicit inference
* MUST be mechanically translatable to the schema-first validation model defined in §9

---

#### 11.7.1 `ConstraintDefinitions`

`ConstraintDefinitions` is a container Concept that groups named, reusable constraints.

##### Children (Normative)

One or more `ConstraintDefinition` children.

The order of `ConstraintDefinition` children MUST be preserved but MUST NOT affect semantics.

---

#### 11.7.2 `ConstraintDefinition`

A `ConstraintDefinition` defines a single named constraint that may be applied to one or more targets.

A `ConstraintDefinition` is itself an Entity.

##### Traits (Normative)

* `id` (required; IRI Reference Value)
* `title` (optional; String Value)
* `description` (optional; String Value)

##### Children (Normative)

Exactly two children, in any order:

* `Targets` — declares what the constraint applies to
* `Rule` — declares the constraint logic

If either child is missing or appears more than once, schema processing MUST fail.

---

#### 11.7.3 `Targets`

`Targets` declares the focus set for a constraint.

A constraint MAY target multiple Concepts and/or contexts.

##### Children (Normative)

One or more of:

* `TargetConcept`
* `TargetContext`

If `Targets` contains no children, schema processing MUST fail.

---

##### 11.7.3.1 `TargetConcept`

Applies the constraint to instances of a specific Concept.

###### Traits (Normative)

* `conceptSelector` (required; Concept name string)

The selector MUST resolve to exactly one `ConceptDefinition`.
Otherwise, schema processing MUST fail.

---

##### 11.7.3.2 `TargetContext`

Applies the constraint relative to a context.

###### Traits (Normative)

* `contextSelector` (required; Concept name string or the literal string `"Document"`)

If `contextSelector` is not `"Document"`, it MUST resolve to exactly one `ConceptDefinition`.
Otherwise, schema processing MUST fail.

---

#### 11.7.4 `Rule`

`Rule` contains the constraint logic.

##### Children (Normative)

Exactly one child, which MUST be one of:

* a **composition rule** (§11.8)
* an **atomic constraint** (§11.10)
* a **path-scoped rule** (§11.9 with quantifier)

If `Rule` contains zero or more than one child, schema processing MUST fail.

`Rule` nodes are purely structural and MUST NOT carry Traits.

---

### 11.8 Rule Algebra (Normative)

This section defines the **rule algebra** used to compose constraints.

Rule algebra nodes are **purely declarative**, **structural**, and **deterministic**.
They define how atomic constraints are combined, without introducing new semantics.

Rule algebra MUST be interpreted according to the schema-first validation model defined in §9.
Rule algebra MUST be translatable to a total, deterministic validation form (for example, SHACL-SPARQL).

---

#### 11.8.1 General Rules

* Rule algebra nodes MUST NOT carry Traits.
* Rule algebra nodes MUST contain only other `Rule` nodes as children.
* Rule algebra MUST NOT introduce side effects, inference, or execution semantics.
* Any rule tree MUST be finite and acyclic.

If a rule algebra structure cannot be translated deterministically, schema processing MUST fail.

---

#### 11.8.2 `AllOf`

`AllOf` requires that **all** child rules hold.

##### Children (Normative)

Two or more `Rule` children.

##### Semantics

The rule holds if and only if **every** child rule holds for the same focus node.

---

#### 11.8.3 `AnyOf`

`AnyOf` requires that **at least one** child rule holds.

##### Children (Normative)

Two or more `Rule` children.

##### Semantics

The rule holds if and only if **one or more** child rules hold for the same focus node.

---

#### 11.8.4 `Not`

`Not` negates a rule.

##### Children (Normative)

Exactly one `Rule` child.

##### Semantics

The rule holds if and only if the child rule does **not** hold for the same focus node.

---

#### 11.8.5 `ConditionalConstraint`

`ConditionalConstraint` expresses implication: *if a condition holds, then a consequent must hold*.

##### Children (Normative)

Exactly two children:

* `When` — contains exactly one `Rule` child (the condition)
* `Then` — contains exactly one `Rule` child (the consequent)

##### Semantics

The rule holds if and only if:

* the condition does **not** hold, **or**
* the condition holds and the consequent holds

This is logically equivalent to:
`¬When ∨ Then`.

---

#### 11.8.6 Determinism Requirement

Rule algebra evaluation MUST be:

* order-independent (except where explicitly scoped by paths or quantifiers)
* free of heuristic interpretation
* reducible to a single boolean outcome per focus node

If rule algebra composition would require guessing, short-circuit heuristics, or undefined evaluation order, schema processing MUST fail.

---

### 11.9 Paths and Quantifiers (Normative)

This section defines **paths** and **quantifiers** used to scope constraint evaluation over structured data.

Paths and quantifiers are **structural selectors**, not semantic operators.
They MUST be interpreted deterministically and MUST NOT introduce inference or implicit traversal rules.

All path and quantifier semantics MUST be compatible with the instance-graph mapping defined in §9.7 and the rule-to-SPARQL translation defined in §9.11.

---

#### 11.9.1 Paths

A path selects zero or more elements relative to a focus node.

Paths MUST be explicit and MUST NOT depend on implicit defaults, ordering assumptions, or heuristic traversal.

Codex defines the following path types:

* `TraitPath`
* `ChildPath`
* `DescendantPath`
* `ContentPath`

Each path node MUST declare exactly the traits required for its form.

##### `TraitPath`

Selects values of a Trait on the focus Concept instance.

###### Traits (Normative)

* `traitName` (required; Trait name string per the Naming Rules in §4)

##### Semantics

Selects each value bound to the named Trait on the focus node.

---

##### `ChildPath`

Selects direct child Concept instances of a given Concept type.

###### Traits (Normative)

* `conceptSelector` (required; Concept name string)

##### Semantics

Selects each direct child of the focus node whose Concept type matches `conceptSelector`.

---

##### `DescendantPath`

Selects descendant Concept instances at any depth of a given Concept type.

###### Traits (Normative)

* `conceptSelector` (required; Concept name string)

##### Semantics

Selects each descendant (via one or more parent links) of the focus node whose Concept type matches `conceptSelector`.

---

##### `ContentPath`

Selects the content of the focus Concept instance.

###### Traits

None.

##### Semantics

Selects the content string if and only if the focus Concept instance is in content mode.

---

#### 11.9.2 Quantifiers

Quantifiers scope a nested rule over the set of elements selected by a Path.

Quantifiers MUST be explicit and MUST NOT introduce implicit cardinality assumptions.

Codex defines the following quantifiers:

* `Exists`
* `ForAll`
* `Count`

Quantifiers MUST appear only in rule nodes that explicitly bind a Path to a nested Rule (see §9.5.3).

---

##### `Exists`

At least one selected element MUST satisfy the nested rule.

###### Semantics

The rule holds if and only if there exists at least one path-selected element for which the nested rule holds.

---

##### `ForAll`

All selected elements MUST satisfy the nested rule.

###### Semantics

The rule holds if and only if no path-selected element violates the nested rule.

---

##### `Count`

Constrains the number of selected elements that satisfy the nested rule.

###### Traits (Normative)

* `minCount` (optional; non-negative integer)
* `maxCount` (optional; positive integer)

At least one of `minCount` or `maxCount` MUST be present.

###### Semantics

The rule holds if and only if the number of path-selected elements that satisfy the nested rule is within the specified bounds.

---

#### 11.9.3 Determinism and Totality

* Paths MUST select a well-defined set of elements.
* Quantifiers MUST evaluate to a single boolean outcome.
* If a path selector cannot be resolved uniquely, schema processing MUST fail.
* If a quantifier cannot be evaluated without guessing, schema processing MUST fail.

Paths and quantifiers MUST NOT be evaluated outside the schema-driven validation pipeline defined in §9.

---

### 11.10 Atomic Constraints (Normative)

Atomic constraints are the **leaves** of the rule algebra.
Each atomic constraint defines a single, declarative validation predicate with no internal composition.

Atomic constraints:

* MUST be deterministic
* MUST be mechanically enforceable
* MUST be evaluable without inference or heuristics
* MUST be translatable to the schema-driven validation model defined in §9

If an atomic constraint cannot be expressed under the instance-graph mapping (§9.7) and the constraint-to-artifact rules (§9.9–§9.11), schema processing MUST fail.

---

#### 11.10.1 Trait Constraints

Trait constraints apply to Traits declared on the focus Concept instance.

##### `TraitExists`

The named Trait MUST be present.

###### Traits (Normative)

* `trait` (required; Trait name string per §4)

---

##### `TraitMissing`

The named Trait MUST be absent.

###### Traits (Normative)

* `trait` (required; Trait name string per §4)

---

##### `TraitEquals`

The named Trait MUST have at least one value equal to the specified value.

###### Traits (Normative)

* `trait` (required; Trait name string per §4)
* `value` (required; Value)

---

##### `TraitCardinality`

Constrains the number of values bound to a Trait.

###### Traits (Normative)

* `trait` (required; Trait name string per §4)
* `min` (optional; non-negative integer)
* `max` (optional; positive integer)

At least one of `min` or `max` MUST be present.

---

##### `TraitValueType`

Constrains the value type of a Trait.

###### Traits (Normative)

* `trait` (required; Trait name string per §4)
* `valueType` (required; value type token)

---

#### 11.10.2 Value Constraints

Value constraints apply to values selected by paths or Traits.

##### `ValueIsOneOf`

The value MUST be one of the explicitly listed values.

###### Traits (Normative)

* `values` (required; list of Values)

---

##### `ValueMatchesPattern`

The value MUST match a regular expression.

###### Traits (Normative)

* `pattern` (required; regex string)
* `flags` (optional; string; SPARQL 1.1 `REGEX` flags)

---

##### `PatternConstraint`

Constrains a specific Trait value to match a regular expression.

###### Traits (Normative)

* `trait` (required; Trait name string per §4)
* `pattern` (required; regex string)
* `flags` (optional; string; SPARQL 1.1 `REGEX` flags)

---

##### `ValueLength`

Constrains the length of a string value.

###### Traits (Normative)

* `min` (optional; non-negative integer)
* `max` (optional; positive integer)

At least one of `min` or `max` MUST be present.

---

##### `ValueInNumericRange`

Constrains a numeric value to an inclusive range.

###### Traits (Normative)

* `min` (optional; number)
* `max` (optional; number)

At least one of `min` or `max` MUST be present.

This constraint MUST apply only to numeric value types that support ordered comparison.
If comparison semantics are not explicitly defined for the active value type, schema processing MUST fail.

---

##### `ValueIsNonEmpty`

The value MUST be present and non-empty.

This constraint applies to string-like values only.
If applied to an incompatible value type, schema processing MUST fail.

---

##### `ValueIsValid`

The value MUST satisfy a named validator.

###### Traits (Normative)

* `validatorName` (required; enumerated token)

The validator MUST resolve to exactly one `ValidatorDefinition` in the governing schema.
If resolution fails, schema processing MUST fail.

---

#### 11.10.3 Child Constraints

Child constraints apply to child Concept instances.

##### `ChildConstraint`

Generic child constraint using explicit type dispatch.

###### Traits (Normative)

* `type` (required; one of `RequiresChildConcept | AllowsChildConcept | ForbidsChildConcept`)
* `conceptSelector` (required; Concept name string)

This form is provided for compatibility and normalization.
Its semantics MUST be equivalent to the corresponding explicit child-rule form defined in §11.4.4.

---

##### `ChildSatisfies`

Constrains child Concept instances using a nested rule.

###### Traits (Normative)

* `conceptSelector` (required; Concept name string)

###### Children (Normative)

* Exactly one `Rule` child

The rule MUST be evaluated for each matching child Concept instance.

---

#### 11.10.4 Collection Constraints

Collection constraints apply only where a Concept’s children form a logical collection.

##### `CollectionOrdering`

Constrains the ordering semantics of a collection.

###### Traits (Normative)

* `ordering` (required; `$Ordered | $Unordered`)

###### Children (Normative)

* Exactly one of `ChildPath` or `DescendantPath` (see §9.5.4)

---

##### `CollectionAllowsEmpty`

Constrains whether a collection may be empty.

###### Traits (Normative)

* `allowed` (required; boolean)

###### Children (Normative)

* Exactly one of `ChildPath` or `DescendantPath` (see §9.5.4)

---

##### `CollectionAllowsDuplicates`

Constrains whether a collection may contain duplicate members.

###### Traits (Normative)

* `allowed` (required; boolean)
* `keyTrait` (conditional; required when `allowed=false`)

###### Children (Normative)

* Exactly one of `ChildPath` or `DescendantPath` (see §9.5.4)

---

##### `MemberCount`

Constrains the number of collection members.

###### Traits (Normative)

* `min` (optional; non-negative integer)
* `max` (optional; positive integer)

At least one of `min` or `max` MUST be present.

###### Children (Normative)

* Exactly one of `ChildPath` or `DescendantPath` (see §9.5.4)

---

##### `EachMemberSatisfies`

Each collection member MUST satisfy a nested rule.

###### Children (Normative)

* Exactly one of `ChildPath` or `DescendantPath` (see §9.5.4)
* Exactly one `Rule` child

The rule MUST be evaluated for each matching collection member.

---

#### 11.10.5 Uniqueness Constraints

##### `UniqueConstraint`

Constrains Trait values to be unique within a scope.

###### Traits (Normative)

* `trait` (required; Trait name string per §4)
* `scope` (required; Concept name string defining the uniqueness scope)

Uniqueness semantics MUST follow the deterministic scope rules defined in §9.9.7.

---

#### 11.10.6 Order Constraints

##### `OrderConstraint`

Constrains the ordering of collection elements by a trait value.

###### Traits (Normative)

* `type` (required; one of the order constraint types defined below)
* `byTrait` (required; Trait name string per §4)

###### Types (Normative)

* `Ascending`: Elements must be in ascending order by the specified trait value.
* `Descending`: Elements must be in descending order by the specified trait value.

###### Children (Normative)

* Exactly one of `ChildPath` or `DescendantPath` (see §9.5.4)

Order constraint semantics apply to ordered collections. If the collection is unordered, the constraint has no effect.
If a rule cannot be translated deterministically, schema processing MUST fail.

---

#### 11.10.7 Reference Constraints

##### `ReferenceConstraint`

Constrains usage of reference Traits.

###### Traits (Normative)

* `type` (required; one of the reference constraint types defined below)

###### Types (Normative)

* `ReferenceTargetsEntity`: Target must be an entity. The `conceptSelector` and `traitName` traits MUST NOT be present.
* `ReferenceMustResolve`: Reference must resolve. The `conceptSelector` and `traitName` traits MUST NOT be present.
* `ReferenceSingleton`: At most one reference trait may be present. The `conceptSelector` and `traitName` traits MUST NOT be present.
* `ReferenceTargetsConcept`: Target must be a specific concept type. The `conceptSelector` trait MUST be present.
* `ReferenceTraitAllowed`: A specific reference trait is allowed. The `traitName` trait MUST be present.

Reference constraint semantics MUST follow §9.9.9–§9.9.12 exactly.

---

#### 11.10.8 Identity Constraints

##### `IdentityConstraint`

Constrains entity and identifier semantics.

###### Traits (Normative)

* `type` (required; one of the identity constraint types defined below)
* `scope` (optional; Concept name string defining an identity uniqueness scope)
* `pattern` (optional; regex string)
* `flags` (optional; string; SPARQL 1.1 `REGEX` flags)

###### Types (Normative)

* `MustBeEntity`: Instance must be an entity. The `scope`, `pattern`, and `flags` traits MUST NOT be present.
* `MustNotBeEntity`: Instance must not be an entity. The `scope`, `pattern`, and `flags` traits MUST NOT be present.
* `IdentifierUniqueness`: Identifiers must be unique within scope. The `scope` trait MUST be present. The `pattern` and `flags` traits MUST NOT be present.
* `IdentifierForm`: Identifier must match pattern. The `pattern` trait MUST be present. The `scope` trait MUST NOT be present.

Identity constraint semantics MUST follow the entity and identity model defined in §§3.5 and 6.

`IdentityConstraint(type=MustBeEntity)` MUST report an `IdentityError` unless the focus Concept instance is an Entity under §3.5.

`IdentityConstraint(type=MustNotBeEntity)` MUST report an `IdentityError` if the focus Concept instance declares an `id` Trait.

For `MustBeEntity` and `MustNotBeEntity`, `scope`, `pattern`, and `flags` MUST NOT be present.

`IdentityConstraint(type=IdentifierUniqueness, scope=S)` constrains identifiers to be unique within the nearest enclosing scope `S`.
Its semantics MUST be identical to `UniqueConstraint(trait=id, scope=S)` as defined in §9.9.7 (where `id` refers to `codex:declaredId`).

For `IdentifierUniqueness`, the `scope` trait MUST be present. The `pattern` and `flags` traits MUST NOT be present.

`IdentityConstraint(type=IdentifierForm, pattern=p, flags=f)` constrains the spelling of declared identifiers.
When the focus Concept instance is an Entity, its declared `id` value MUST match the regular expression `p` under SPARQL 1.1 `REGEX` semantics (see §9.5.1).

`IdentityConstraint(type=IdentifierForm)` MUST be treated as a schema error unless `pattern` is provided.

For `IdentifierForm`, `scope` MUST NOT be present.

---

#### 11.10.9 Context Constraints

##### `ContextConstraint`

Constrains the structural context in which a Concept instance may appear.

###### Traits (Normative)

* `type` (required; one of the context constraint types defined below)
* `contextSelector` (Concept name string; see type-specific requirements below)

###### Types (Normative)

* `OnlyValidUnderParent`: Requires the immediate parent is of the type specified by `TargetContext`. The `contextSelector` trait MUST NOT be present.
* `OnlyValidUnderContext`: Requires an ancestor of the specified type exists in the parent chain. The `contextSelector` trait MUST be present.

Context constraint semantics MUST follow §9.9.8.

---

#### 11.10.10 Content Constraints

##### `ContentConstraint`

Constrains content presence or structure.

###### Traits (Normative)

* `type` (required; one of the content constraint types defined below)

###### Types (Normative)

* `ContentForbiddenUnlessAllowed`: Requires content is absent. The `pattern` and `flags` traits MUST NOT be present.
* `ContentRequired`: Requires content exists. The `pattern` and `flags` traits MUST NOT be present.
* `ContentMatchesPattern`: Requires content matches a pattern. The `pattern` trait MUST be present. The `flags` trait MAY be present.

Content constraint semantics MUST follow the content model defined in §3.4 and the validation rules defined in §9.9.5.

---

#### 11.10.11 Failure Rules

If any atomic constraint:

* lacks required traits
* references an unresolved selector
* applies to an incompatible value or structure
* requires semantics not explicitly defined

schema processing MUST fail rather than guess.

---

### 11.11 Complete Constraint Example (Informative)

This section provides illustrative examples of constraint definitions authored using the schema definition language.

Examples in this section are **informative** and do not introduce additional normative requirements.

---

```cdx
<ConstraintDefinition
	id=example:constraint:recipe-requires-title
	title="Recipe requires Title"
>
	<Targets>
		<TargetConcept conceptSelector="Recipe" />
	</Targets>
	<Rule>
		<ChildConstraint
			type="RequiresChildConcept"
			conceptSelector="Title"
		/>
	</Rule>
</ConstraintDefinition>
```

---

```cdx
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
				<ChildConstraint
					type="RequiresChildConcept"
					conceptSelector="Parameters"
				/>
			</Then>
		</ConditionalConstraint>
	</Rule>
</ConstraintDefinition>
```

---

These examples demonstrate:

* targeting constraints to specific Concepts
* use of rule algebra (`Not`, `ConditionalConstraint`)
* reuse of atomic constraints
* deterministic, schema-first validation intent

---

### 11.12 Relationship to External Systems (Normative)

Codex schemas are **authoritative** with respect to meaning and validation.

External representations MAY be derived from Codex schemas, subject to the following constraints:

* Any derived representation (including SHACL, SHACL-SPARQL, or OWL) MUST be a pure, deterministic projection of the Codex schema.
* Derived artifacts MUST NOT introduce semantics, defaults, inference rules, or interpretation not explicitly defined by:

  * this specification, and
  * the governing Codex schema.
* Derived artifacts MUST NOT override, weaken, or contradict Codex validation semantics.
* If a Codex constraint or rule cannot be expressed faithfully in the chosen external system, derivation MUST fail rather than approximate.

Codex does not defer to external systems for meaning.

External systems are consumers or validation backends only; they are not normative authorities.

---

### 11.13 Summary

* The schema definition language is itself Codex.
* Schemas are declarative, closed-world, and deterministic.
* All authorization, structure, and constraints are explicit.
* Content mode, traits, children, collections, and references are schema-defined.
* Constraint logic is compositional and total.
* Schemas may validate other schemas via the bootstrap schema-of-schemas.
* External validation artifacts are optional, derived, and non-authoritative.

All schema semantics are governed by this specification and by the schema-first architecture defined in §9.

---







## 12. Schema Loading and Bootstrapping

This section defines how schemas are associated with documents for schema-first parsing and validation.

### 12.1 Purpose

Codex is a schema-first language.

A Codex document MUST NOT be semantically validated without an explicit governing schema.

Codex permits schema-less formatting and well-formedness checks that do not require a governing schema, but such checks MUST NOT perform semantic interpretation or validation (see §9.2 and §10.2.1).

This section normatively defines how a conforming implementation obtains the governing schema for a document.

Its goals are to:

* ensure that every semantic validation operation has an explicit governing schema
* define a clear and deterministic schema resolution order
* support bootstrapping of the schema language itself via a built-in schema-of-schemas
* ensure failures are reported clearly and classified correctly when a schema is unavailable or invalid
### 12.2 Schema Provision Mechanisms (Normative)

A conforming implementation MUST support explicit provision of a governing schema.

A conforming implementation MAY support additional schema provision mechanisms, provided they do not override or weaken explicit provision.

Schema provision mechanisms determine **which schema is supplied** to the schema-first processing pipeline; they MUST NOT alter parsing, validation, or canonicalization semantics.

#### 12.2.1 Explicit Provision (Required)

The governing schema is provided directly by the caller as an explicit input.

```
parse(documentBytes, governingSchema) → parsedDocument
```

This is the baseline mechanism.

All conforming implementations MUST support explicit schema provision.

If an explicit schema is provided, the implementation MUST use that schema and MUST NOT attempt to substitute, infer, or override it.

#### 12.2.2 Registry-Based Resolution (Optional)

An implementation MAY support resolving a governing schema via a schema registry.

Registry lookup mechanisms, identifiers, transport protocols, caching behavior, and trust models are outside the scope of this specification.

If supported, registry-based resolution MUST be explicit, deterministic, and fail-fast.

Registry-based resolution MUST NOT be attempted unless explicit provision did not occur.

### 12.3 Schema Resolution Order (Normative)

If an implementation supports more than one schema provision mechanism, it MUST resolve the governing schema using the following strict precedence order:

1. **Explicit provision** — if a governing schema is provided directly by the caller, it MUST be used.
2. **Registry-based resolution** — if supported and no explicit schema was provided, the implementation MAY attempt registry lookup.
3. **Failure** — if no governing schema is obtained, processing MUST fail.

Explicit provision always takes precedence over all other mechanisms.

An implementation MUST NOT infer, guess, or substitute a governing schema.

### 12.4 Bootstrap Schema-of-Schemas (Normative)

Codex defines a built-in **bootstrap schema-of-schemas** used to parse and validate schema documents authored in Codex.

The bootstrap schema-of-schemas exists to eliminate circular dependency during schema loading and to make the schema definition language self-hosting.

The bootstrap schema-of-schemas is distinct from domain schemas and from ecosystem meta-schemas.
It governs **only** documents whose root Concept is `Schema`.

The bootstrap schema-of-schemas MUST NOT be substituted for a missing governing schema when processing an instance document.

#### 12.4.1 Requirements

Every conforming implementation MUST:

* include the complete bootstrap schema-of-schemas as built-in, immutable data
* use the bootstrap schema-of-schemas to parse and validate schema documents
* ensure the bootstrap schema-of-schemas is applied deterministically and without extension unless an explicit governing schema is provided

An explicitly provided governing schema for a schema document MUST either be the bootstrap schema-of-schemas itself or a schema that is valid under the bootstrap schema-of-schemas. Partial extension, modification, or augmentation of the bootstrap schema-of-schemas is forbidden.

The bootstrap schema-of-schemas MUST itself conform to the Codex language invariants (§2) and the schema-first architecture (§9).

#### 12.4.2 Schema Document Detection

A document is a schema document if and only if its root Concept is `Schema`.

A document whose root Concept is `Schema` MUST be treated as a schema document and MUST NOT be parsed as an instance document under any schema other than the bootstrap schema-of-schemas or an explicitly provided governing schema.

When a parser encounters a root `Schema` Concept:

1. If an explicit governing schema was provided by the caller, that schema MUST be used.
2. Otherwise, the built-in bootstrap schema-of-schemas MUST be used.

No other detection, inference, or fallback mechanisms are permitted.

#### 12.4.3 Validation and Error Classification

When processing a schema document:

* If the document cannot be decoded, tokenized, or structurally parsed, the failure MUST be classified as `ParseError`.
* If the document is structurally readable but violates the bootstrap schema-of-schemas or an explicitly provided governing schema, the failure MUST be classified as `SchemaError`.

Implementations MUST NOT attempt partial validation, recovery, or best-effort interpretation.

#### 12.4.4 Canonical Authority

All schema-language constructs that appear in schema documents are defined **exactly once**:

* in the schema definition language specified in §11 of this document

The bootstrap schema-of-schemas MUST accept exactly those schema documents that conform to §11, and MUST reject all others.

The bootstrap schema-of-schemas MUST NOT introduce additional constructs, defaults, or semantics beyond those defined in §11.

### 12.5 Schema Caching (Informative)

Schemas are immutable within a declared version.

Implementations MAY cache parsed and validated schemas to avoid redundant processing.

Caching behavior, eviction policy, persistence, and invalidation strategies are implementation-defined.

Caching MUST NOT change observable parsing, validation, or error-reporting behavior.

### 12.6 Error Handling (Normative)

#### 12.6.1 Schema Unavailable

If no schema can be obtained through any supported mechanism:

* Error class: `ParseError`
* The report MUST indicate that the governing schema was unavailable
* Parsing MUST NOT proceed

#### 12.6.2 Schema Load Failure

If schema resolution succeeds but loading the schema fails (for example, network error or file not found):

* Error class: `ParseError`
* The report MUST indicate that the schema could not be loaded
* The report MUST include the schema identifier

#### 12.6.3 Invalid Schema

If a loaded schema is not valid Codex or is not a valid schema under the bootstrap schema-of-schemas:

* Error class: `SchemaError`
* The report MUST indicate that schema validation failed
* Underlying schema validation errors MUST be reported

### 12.7 Relationship to Other Specifications

* This specification defines schema-first processing semantics (§9).
* This section defines how governing schemas are obtained and bootstrapped (§12).
* The schema definition language itself is defined normatively in §11.
* Formatting and canonicalization rules apply uniformly to both schema documents and non-schema documents (§10).

No other specification may override or weaken these rules.

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

### 13.3 Schema Identity (Normative)

Every Codex schema MUST declare its identity and version explicitly.

Schema identity and versioning are defined exclusively by the root `Schema` Concept as specified in §11.

Accordingly:

* The `id` Trait of the root `Schema` Concept defines the **stable schema identifier**.
* The `version` Trait of the root `Schema` Concept defines the **schema version**.
* The `versionScheme` Trait of the root `Schema` Concept defines the **version ordering scheme**.

The schema identifier (`Schema id`) identifies the schema lineage.
All versions of the same schema MUST share the same schema identifier.

The schema version (`Schema version`) identifies the specific set of rules that apply.

A schema document that omits any of the `id`, `version`, or `versionScheme` Traits on the root `Schema` Concept is invalid.

A schema document MUST NOT declare more than one schema identifier.

A schema document MUST NOT redefine or alias the schema identifier across versions.

Schema identity and version information MUST be treated as authoritative and MUST NOT be inferred, synthesized, or substituted by tooling.

### 13.4 Version Semantics (Normative)

Schemas MUST use monotonic versioning within a schema lineage.

Within a schema lineage, all schema versions MUST use the same `versionScheme` value.

Regardless of scheme, schema versions MUST form a **total, unambiguous ordering**.

If two schema versions cannot be ordered deterministically, the schema is invalid.

A schema whose version ordering is ambiguous or non-comparable MUST be rejected with a `SchemaError`.

Tools MUST compare schema versions mechanically according to the comparison rules defined in this section for the declared `versionScheme`, and MUST NOT apply heuristics, coercion, or fallback rules.

#### 13.4.1 Version Schemes (Normative)

The root `Schema` Concept’s `versionScheme` Trait MUST be one of the following Enumerated Token Values:

* `$Semver`
* `$DateYYYYMM`
* `$DateYYYYMMDD`
* `$Lexical`

If `versionScheme` is not one of these values, schema processing MUST fail with a `SchemaError`.

#### 13.4.2 Version Comparison Rules (Normative)

For all schemes below, if a `version` string does not conform to the required scheme-specific syntax, schema processing MUST fail with a `SchemaError`.

`$Semver`

* Syntax: `MAJOR.MINOR.PATCH` where `MAJOR`, `MINOR`, and `PATCH` are base-10 non-negative integers with no leading zeros (except that `0` is permitted).
* Comparison: compare by numeric tuple `(MAJOR, MINOR, PATCH)`.

`$DateYYYYMM`

* Syntax: `YYYY-MM` where `YYYY` is four base-10 digits and `MM` is `01` through `12`.
* Comparison: compare by numeric tuple `(YYYY, MM)`.

`$DateYYYYMMDD`

* Syntax: `YYYY-MM-DD` where `YYYY` is four base-10 digits, `MM` is `01` through `12`, and `DD` is `01` through `31`.
* Comparison: compare by numeric tuple `(YYYY, MM, DD)`.

`$Lexical`

* Syntax: any String Value.
* Comparison: compare the `version` String Values by Unicode scalar value codepoint order, left-to-right; if all compared codepoints are equal, the shorter string is less than the longer string.

### 13.5 Compatibility Classes (Normative)

Each schema version MUST declare exactly one compatibility class relative to the immediately preceding version in the same schema lineage.

The compatibility class is declared via the `compatibilityClass` Trait on the root `Schema` Concept as defined in §11.

The declared compatibility class is **normative and enforceable**.

If a schema version’s declared compatibility class is contradicted by its actual effects on validation semantics, the schema is invalid and MUST be rejected with a `SchemaError`.

Exactly one of the following compatibility classes MUST be specified.

#### 13.5.1 Backward-Compatible

A backward-compatible schema version guarantees that:

* all Codex data that passed schema validation under the immediately preceding version MUST also pass schema validation under this version
* the meaning of existing Concepts and Traits MUST be preserved
* new Concepts or Traits MAY be added
* new constraints MAY be added only if they do not invalidate any data that was valid under the preceding version

If any previously valid data becomes invalid under a schema version declared as backward-compatible, the schema is invalid.

#### 13.5.2 Forward-Compatible

A forward-compatible schema version guarantees that:

* Codex data authored for this version MAY pass schema validation under the immediately preceding version
* newly introduced constructs are optional and additive
* existing Concepts, Traits, and constraints remain unchanged in meaning

Forward compatibility is intended for extension-oriented evolution where older tools can safely ignore newer constructs.

If data authored for a forward-compatible version cannot pass schema validation under the preceding version without loss of meaning, the schema is invalid.

#### 13.5.3 Breaking

A breaking schema version declares that:

* Codex data valid under the preceding version MAY become invalid
* the meaning or constraints of existing Concepts or Traits MAY change
* explicit migration is required

Breaking schema versions MUST be explicitly declared.

Any schema version that introduces a breaking change MUST be marked as breaking.

### 13.6 What Constitutes a Breaking Change (Normative)

A schema version introduces a breaking change if and only if it violates any guarantee required by the `BackwardCompatible` or `ForwardCompatible` compatibility classes with respect to the immediately preceding version.

The following changes are breaking and MUST require `compatibilityClass=$Breaking`:

* removing a `ConceptDefinition`
* renaming a Concept
* removing a `TraitDefinition`
* renaming a Trait
* changing the value type or reference semantics of an existing Trait
* changing `entityEligibility` for any Concept
* changing collection semantics, including ordering or duplicate allowance
* changing identity, reference, or uniqueness semantics
* tightening constraints in a way that causes any previously valid data to become invalid
* changing the meaning or interpretation of any existing Concept or Trait

A schema version that introduces any breaking change without declaring `compatibilityClass=$Breaking` is invalid and MUST be rejected with a `SchemaError`.

Documentation-only changes, comments, or purely presentational metadata that do not affect validation or meaning do not constitute breaking changes.

### 13.7 Non-Breaking Changes (Normative)

A schema version MAY be declared as non-breaking only if it preserves all validation and semantic guarantees required by its declared compatibility class.

The following changes are non-breaking **only when they do not invalidate any data that was valid under the immediately preceding version**:

* adding new `ConceptDefinition` entries
* adding new `TraitDefinition` entries
* adding optional Traits to existing Concepts
* adding new Structural Concepts that do not alter existing structure
* adding new constraints that apply **only** to newly introduced Concepts or Traits
* adding documentation, labels, or descriptive metadata with no semantic effect

Non-breaking changes MUST NOT:

* alter the interpretation of any existing Concept, Trait, or Value Type
* restrict previously allowed structures, values, or relationships
* introduce new required Traits, Children, or Content on existing Concepts

If any change classified as non-breaking would cause previously valid data to fail validation, the schema version MUST instead be declared as `compatibilityClass=$Breaking`.

### 13.8 Schema Validation Behavior (Normative)

When validating a Codex document, the governing schema version MUST be explicitly known.

Validation MUST be performed strictly according to the rules of that schema version.

A conforming implementation MUST:

* use exactly the rules defined by the declared schema version
* treat schema identifier and version as part of the validation input
* fail validation if the schema version is missing, ambiguous, or cannot be resolved
* fail validation if the declared compatibility class does not permit validation in the requested context

A conforming implementation MUST NOT:

* infer schema version intent
* substitute a different schema version
* relax or tighten validation rules across versions
* silently reinterpret data authored under a different schema version

If schema version resolution fails for any reason, validation MUST fail.

### 13.9 Relationship to Data Migration (Normative)

This specification defines schema evolution semantics, not data migration mechanisms.

A breaking schema version declaration MUST be treated as a statement that migration is required for existing data to validate under the new schema version.

Codex schemas MUST:

* explicitly declare when a version is breaking
* define what semantic rules have changed between versions
* NOT imply or embed migration behavior

Codex tooling MUST:

* NOT perform implicit or heuristic data migration
* NOT alter data to make it validate under a different schema version
* treat migration as an explicit, external process

Any migrated data MUST validate cleanly under the target schema version using ordinary schema validation rules.

Migration tooling, if provided, is outside the scope of this specification and MUST be explicit, deterministic, and non-heuristic.

### 13.10 Tooling Responsibilities (Normative)

Codex tooling MUST:

* surface the governing schema identifier and version as explicit inputs to validation
* surface the declared compatibility class for the schema version
* refuse to validate data against a schema version whose compatibility class does not permit such validation
* refuse to validate data when schema identifier, version, or compatibility class is missing or ambiguous
* treat schema identifier, version, and compatibility class as part of the validation contract

Codex tooling MUST NOT:

* silently reinterpret data across schema versions
* infer compatibility or intent beyond what is explicitly declared
* downgrade or upgrade schema versions implicitly
* validate data against an incompatible schema version

All version handling MUST be explicit, deterministic, and free of heuristics.

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

- violation of a governing schema's `ReferenceConstraint(type=ReferenceSingleton)` requirement
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

### 14.6 Reporting Requirements (Normative)

Tools MUST report validation failures with:

* the primary error class
* the Concept name
* the Trait name (if applicable)
* a reference to the violated rule or constraint
* a precise location (line number or Concept path)

If any of the above information is not applicable, the tool MUST omit it explicitly rather than infer or guess.

Error wording, formatting, and presentation are tool-defined, but classification and attribution MUST be precise and deterministic.

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

* EBNF (Normative) — ISO/IEC 14977 Extended Backus-Naur Form
* PEG (Informative) — Parsing Expression Grammar for implementation

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
* `-` exception
* `;` end of production

Character classes use the following extensions:

* `#x0000` Unicode code point
* `[a-z]` character range
* `\t` tab (U+0009)
* `\n` line feed (U+000A)

---

#### A.1.2 Document Structure

```ebnf
(* A Codex document contains exactly one root Concept. *)

Document
	= OptionalLeadingAnnotations, RootConcept, OptionalTrailingBlankLines
	;

OptionalLeadingAnnotations
	= { GeneralOrGroupingAnnotationBlock }
	;

OptionalTrailingBlankLines
	= { BlankLine }
	;

RootConcept
	= ConceptAtColumn0
	;

ConceptAtColumn0
	= ConceptLineStart0, Concept, [ ConceptLineEnd ]
	;

ConceptLineStart0
	= (* beginning of file or immediately after Newline *)
	  [ Newline ]
	;

ConceptLineEnd
	= (* a structural line ends with a newline *)
	  Newline
	;

(* A general or grouping annotation block may appear before the root concept.
	This grammar admits them structurally; their kind/attachment rules are checked
	by the surface-form rules. *)
GeneralOrGroupingAnnotationBlock
	= { BlankLine }, Annotation, { BlankLine }
	;

Concept
	= BlockConcept | SelfClosingConcept
	;
```

---

#### A.1.3 Block Concepts

```ebnf
(* Block concepts contain either children or content.
	The parser consults the governing schema (ContentRules) to select the Body production.
	This is schema-directed dispatch, not syntactic ambiguity. *)

BlockConcept
	= OpeningMarkerLine, Body, ClosingMarkerLine
	;

OpeningMarkerLine
	= Indentation, OpeningMarker, Newline
	;

ClosingMarkerLine
	= Indentation, ClosingMarker, Newline
	;

OpeningMarker
	= "<", ConceptName, [ Traits ], ">"
	;

ClosingMarker
	= "</", ConceptName, ">"
	;

(* Body is selected by schema lookup on ConceptName:
	- If schema indicates children mode (ForbidsContent): ChildrenBody
	- If schema indicates content mode (AllowsContent): ContentBody *)
Body
	= ChildrenBody | ContentBody
	;

ChildrenBody
	= { ChildItem }
	;

(* A ChildItem is either:
	- an annotation line/block, or
	- a child concept (block or self-closing), each on its own structural line.
	Blank-line legality is enforced by surface-form rules; the grammar admits both. *)
ChildItem
	= ( BlankLine
	  | AnnotationLine
	  | AnnotationBlock
	  | ConceptLine
	  )
	;

ConceptLine
	= Indentation, ConceptMarkerOrConcept, Newline
	;

(* Within a children body, a child concept begins on a line and is either:
	- a self-closing marker, or
	- an opening marker line followed by its body and closing marker line. *)
ConceptMarkerOrConcept
	= SelfClosingMarker
	| OpeningMarker (* followed by Body and ClosingMarkerLine in BlockConcept *)
	;

ContentBody
	= { ContentLine }
	;

ContentLine
	= Indentation, ContentText, Newline
	;

ContentText
	= { ContentChar }
	;

ContentChar
	= ContentEscape | ContentSafeChar
	;

ContentEscape
	= "\\", ( "<" | "[" )
	;

(* Raw '<' is forbidden anywhere in content. Raw '[' is forbidden at line start only. *)
ContentSafeChar
	= AnyCharExceptNewline - "<"
	;
```

---

#### A.1.4 Self-Closing Concepts

```ebnf
SelfClosingConcept
	= SelfClosingMarker
	;

SelfClosingMarker
	= "<", ConceptName, [ Traits ], "/>"
	;
```

---

#### A.1.5 Concept Names

```ebnf
(* Naming rule details beyond basic lexical form (e.g., no runs of uppercase)
	are enforced by surface-form validation. *)

ConceptName
	= UppercaseLetter, { Letter | Digit }
	;

UppercaseLetter
	= "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J"
	| "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T"
	| "U" | "V" | "W" | "X" | "Y" | "Z"
	;

LowercaseLetter
	= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j"
	| "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t"
	| "u" | "v" | "w" | "x" | "y" | "z"
	;

Letter
	= UppercaseLetter | LowercaseLetter
	;

Digit
	= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
	;
```

---

#### A.1.6 Traits

```ebnf
Traits
	= WhitespaceNoNewline, Trait, { Whitespace, Trait }
	;

Trait
	= TraitName, "=", Value
	;

(* Naming rule details beyond basic lexical form are enforced by surface-form validation. *)
TraitName
	= LowercaseLetter, { Letter | Digit }
	;
```

---

#### A.1.7 Values

```ebnf
Value
	= StringValue
	| CharValue
	| BacktickString
	| BooleanValue
	| NumericValue
	| EnumeratedToken
	| TemporalValue
	| ColorValue
	| UuidValue
	| LookupToken
	| IriReference
	| ListValue
	| SetValue
	| MapValue
	| TupleValue
	| RangeValue
	;
```

---

#### A.1.8 String Values

```ebnf
StringValue
	= '"', { StringChar }, '"'
	;

StringChar
	= UnescapedStringChar | EscapeSequence
	;

UnescapedStringChar
	= AnyCharExceptQuoteBackslashNewline
	;

EscapeSequence
	= "\\", ( '"' | "\\" | "n" | "r" | "t" | UnicodeEscape )
	;

UnicodeEscape
	= "u", HexDigit, HexDigit, HexDigit, HexDigit
	| "u{", HexDigit, { HexDigit }, "}"
	;

HexDigit
	= Digit
	| "a" | "b" | "c" | "d" | "e" | "f"
	| "A" | "B" | "C" | "D" | "E" | "F"
	;
```

---

#### A.1.9 Character Values

```ebnf
CharValue
	= "'", CharContent, "'"
	;

CharContent
	= UnescapedChar | CharEscapeSequence
	;

UnescapedChar
	= AnyCharExceptApostropheBackslashNewline
	;

CharEscapeSequence
	= "\\", ( "'" | "\\" | "n" | "r" | "t" | UnicodeEscape )
	;
```

---

#### A.1.10 Backtick Strings

```ebnf
BacktickString
	= "`", { BacktickChar }, "`"
	;

BacktickChar
	= UnescapedBacktickChar | BacktickEscape
	;

UnescapedBacktickChar
	= AnyCharExceptBacktick
	;

BacktickEscape
	= "\\", "`"
	;
```

---

#### A.1.11 Boolean Values

```ebnf
BooleanValue
	= "true" | "false"
	;
```

---

#### A.1.12 Numeric Values

```ebnf
NumericValue
	= ComplexNumber
	| ImaginaryNumber
	| Fraction
	| Infinity
	| PrecisionNumber
	| ScientificNumber
	| DecimalNumber
	| Integer
	;

Sign
	= "+" | "-"
	;

Integer
	= [ Sign ], IntegerDigits
	;

DecimalNumber
	= [ Sign ], IntegerDigits, ".", DigitSequence
	;

ScientificNumber
	= ( Integer | DecimalNumber ), ( "e" | "E" ), [ Sign ], IntegerDigits
	;

PrecisionNumber
	= DecimalNumber, "p", [ IntegerDigits ]
	;

Infinity
	= [ Sign ], "Infinity"
	;

Fraction
	= Integer, "/", IntegerDigits
	;

ImaginaryNumber
	= ( Integer | DecimalNumber ), "i"
	;

ComplexNumber
	= ( Integer | DecimalNumber ), ( "+" | "-" ), ( Integer | DecimalNumber ), "i"
	;

DigitSequence
	= Digit, { Digit }
	;

NonZeroDigit
	= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
	;

IntegerDigits
	= "0" | NonZeroDigit, { Digit }
	;
```

---

#### A.1.13 Enumerated Tokens

```ebnf
EnumeratedToken
	= "$", UppercaseLetter, { Letter | Digit }, [ TypeParameters ]
	;

TypeParameters
	= "<", TypeArgument, { ",", TypeArgument }, ">"
	;

TypeArgument
	= EnumeratedToken
	| TypeUnion
	;

TypeUnion
	= "[", EnumeratedToken, { ",", EnumeratedToken }, "]"
	;
```

---

#### A.1.14 Temporal Values

```ebnf
TemporalValue
	= "{", TemporalBody, "}"
	;

TemporalBody
	= ZonedDateTime
	| LocalDateTime
	| Date
	| YearMonth
	| MonthDay
	| Time
	| Duration
	| ReservedTemporal
	;

Date
	= Year, "-", Month, "-", Day
	;

YearMonth
	= Year, "-", Month
	;

MonthDay
	= Month, "-", Day
	;

LocalDateTime
	= Date, "T", Time
	;

ZonedDateTime
	= LocalDateTime, TimeZoneOffset, [ TimeZoneId ]
	;

TimeZoneOffset
	= "Z" | ( ( "+" | "-" ), Hour, ":", Minute )
	;

TimeZoneId
	= "[", TimeZoneIdChar, { TimeZoneIdChar }, "]"
	;

TimeZoneIdChar
	= Letter | Digit | "/" | "_" | "-"
	;

Time
	= Hour, ":", Minute, [ ":", Second, [ ".", Milliseconds ] ]
	;

Duration
	= "P", { DurationComponent }, [ "T", { TimeDurationComponent } ]
	;

DurationComponent
	= DigitSequence, ( "Y" | "M" | "W" | "D" )
	;

TimeDurationComponent
	= DigitSequence, [ ".", DigitSequence ], ( "H" | "M" | "S" )
	;

ReservedTemporal
	= "now" | "today"
	;

Year
	= Digit, Digit, Digit, Digit
	;

Month
	= Digit, Digit
	;

Day
	= Digit, Digit
	;

Hour
	= Digit, Digit
	;

Minute
	= Digit, Digit
	;

Second
	= Digit, Digit
	;

Milliseconds
	= Digit, { Digit }
	;
```

---

#### A.1.15 Color Values

```ebnf
(* Color values are accepted as declarative spellings; tools MUST NOT normalize,
	convert, or interpret them. This grammar admits the permitted surface spellings. *)

ColorValue
	= HexColor
	| FunctionColor
	| NamedColor
	;

HexColor
	= "#", HexDigit, HexDigit, HexDigit, [ HexDigit ]
	| "#", HexDigit, HexDigit, HexDigit, HexDigit, HexDigit, HexDigit, [ HexDigit, HexDigit ]
	;

NamedColor
	= "&", LowercaseLetter, { LowercaseLetter }
	;

FunctionColor
	= RgbFunc
	| HslFunc
	| HwbFunc
	| LabFunc
	| LchFunc
	| OklabFunc
	| OklchFunc
	| ColorFunc
	| ColorMixFunc
	| RelativeColorFunc
	| DeviceCmykFunc
	;

RgbFunc
	= ( "rgb" | "rgba" ), "(", ColorFuncPayload, ")"
	;

HslFunc
	= ( "hsl" | "hsla" ), "(", ColorFuncPayload, ")"
	;

HwbFunc
	= "hwb", "(", ColorFuncPayload, ")"
	;

LabFunc
	= "lab", "(", ColorFuncPayload, ")"
	;

LchFunc
	= "lch", "(", ColorFuncPayload, ")"
	;

OklabFunc
	= "oklab", "(", ColorFuncPayload, ")"
	;

OklchFunc
	= "oklch", "(", ColorFuncPayload, ")"
	;

ColorFunc
	= "color", "(", ColorSpace, WhitespaceNoNewline, ColorFuncPayload, ")"
	;

ColorMixFunc
	= "color-mix", "(", ColorFuncPayload, ")"
	;

RelativeColorFunc
	= ( "rgb" | "rgba" | "hsl" | "hsla" | "hwb" | "lab" | "lch" | "oklab" | "oklch" | "color" ),
	  "(", "from", WhitespaceNoNewline, ColorValue, ColorFuncTail, ")"
	;

DeviceCmykFunc
	= "device-cmyk", "(", ColorFuncPayload, ")"
	;

ColorSpace
	= "srgb"
	| "srgb-linear"
	| "display-p3"
	| "a98-rgb"
	| "prophoto-rgb"
	| "rec2020"
	| "xyz"
	| "xyz-d50"
	| "xyz-d65"
	;

(* The payload is accepted as an uninterpreted balanced-parentheses token sequence,
	subject only to Value termination rules (see A.1.27). *)
ColorFuncPayload
	= { ColorPayloadChar }
	;

ColorFuncTail
	= { ColorPayloadChar }
	;

ColorPayloadChar
	= AnyCharExceptRightParenNewline
	;
```

---

#### A.1.16 UUID Values

```ebnf
UuidValue
	= HexOctet, HexOctet, HexOctet, HexOctet, "-",
	  HexOctet, HexOctet, "-",
	  HexOctet, HexOctet, "-",
	  HexOctet, HexOctet, "-",
	  HexOctet, HexOctet, HexOctet, HexOctet, HexOctet, HexOctet
	;

HexOctet
	= HexDigit, HexDigit
	;
```

---

#### A.1.17 IRI Reference Values

```ebnf
(* IRI references are unquoted tokens containing a ':'.
	They terminate at Value termination (see A.1.27). *)

IriReference
	= IriScheme, ":", IriTokenBody
	;

IriScheme
	= Letter, { Letter | Digit | "+" | "-" | "." }
	;

IriTokenBody
	= { IriTokenChar }
	;

(* This is a token-level placeholder: the exact admissible character set is RFC 3987
	profiled by this specification. Surface-form validation enforces the disallowed
	Unicode categories; the grammar enforces only token termination exclusions. *)
IriTokenChar
	= AnyCharExceptValueTerminator
	;
```

---

#### A.1.18 Lookup Token Values

```ebnf
LookupToken
	= "~", LowercaseLetter, { Letter | Digit }
	;
```

---

#### A.1.19 List Values

```ebnf
ListValue
	= "[", { Whitespace }, [ ListItems ], { Whitespace }, "]"
	;

ListItems
	= Value, { { Whitespace }, ",", { Whitespace }, Value }
	;
```

---

#### A.1.20 Set Values

```ebnf
SetValue
	= "set", "[", { Whitespace }, [ SetItems ], { Whitespace }, "]"
	;

SetItems
	= Value, { { Whitespace }, ",", { Whitespace }, Value }
	;
```

---

#### A.1.21 Map Values

```ebnf
MapValue
	= "map", "[", { Whitespace }, [ MapItems ], { Whitespace }, "]"
	;

MapItems
	= MapEntry, { { Whitespace }, ",", { Whitespace }, MapEntry }
	;

MapEntry
	= MapKey, { Whitespace }, ":", { Whitespace }, Value
	;

MapKey
	= MapIdentifier
	| StringValue
	| CharValue
	| Integer
	| EnumeratedToken
	;

MapIdentifier
	= LowercaseLetter, { Letter | Digit }
	;
```

---

#### A.1.22 Tuple Values

```ebnf
TupleValue
	= "(", { Whitespace }, TupleItems, { Whitespace }, ")"
	;

TupleItems
	= Value, { { Whitespace }, ",", { Whitespace }, Value }
	;
```

---

#### A.1.23 Range Values

```ebnf
RangeValue
	= RangeStart, "..", RangeEnd, [ "s", StepValue ]
	;

RangeStart
	= NumericValue | TemporalValue | CharValue
	;

RangeEnd
	= NumericValue | TemporalValue | CharValue
	;

StepValue
	= NumericValue | TemporalValue
	;
```

---

#### A.1.24 Annotations

```ebnf
(* Codex defines two surface forms for annotations:
	- Inline: '[' ... ']' on a single line
	- Block: '[' on its own line, then content lines, then ']' on its own line
	The attachment/grouping/general-kind rules are surface-form validation rules. *)

Annotation
	= AnnotationLine | AnnotationBlock
	;

AnnotationLine
	= Indentation, "[", { AnnotationChar }, "]", Newline
	;

AnnotationBlock
	= Indentation, "[", Newline,
	  { AnnotationBlockLine },
	  Indentation, "]", Newline
	;

AnnotationBlockLine
	= Indentation, { AnnotationBlockChar }, Newline
	;

AnnotationChar
	= UnescapedAnnotationChar | AnnotationEscape
	;

UnescapedAnnotationChar
	= AnyCharExceptRightBracketNewline
	;

AnnotationEscape
	= "\\", "]"
	;

(* Inside block annotations, the only escape defined is the same as inline: '\]'. *)
AnnotationBlockChar
	= UnescapedAnnotationBlockChar | AnnotationEscape
	;

UnescapedAnnotationBlockChar
	= AnyCharExceptNewline
	;
```

---

#### A.1.25 Whitespace and Structural Elements

```ebnf
Whitespace
	= WhitespaceChar, { WhitespaceChar }
	;

WhitespaceNoNewline
	= WhitespaceNoNewlineChar, { WhitespaceNoNewlineChar }
	;

WhitespaceChar
	= " " | "\t" | Newline
	;

WhitespaceNoNewlineChar
	= " " | "\t"
	;

Newline
	= "\n"
	;

(* A blank line is a line that contains no characters after normalization.
	This grammar admits optional spaces/tabs on an otherwise empty line. *)
BlankLine
	= { " " | "\t" }, Newline
	;

Indentation
	= { "\t" }
	;
```

---

#### A.1.26 Character Classes (Informative)

The following character classes are used but not fully enumerated:

* `AnyCharExceptNewline` — any Unicode scalar except U+000A
* `AnyCharExceptQuoteBackslashNewline` — any Unicode scalar except `"`, `\\`, U+000A
* `AnyCharExceptApostropheBackslashNewline` — any Unicode scalar except `'`, `\\`, U+000A
* `AnyCharExceptBacktick` — any Unicode scalar except `` ` ``
* `AnyCharExceptBacktickBackslash` — any Unicode scalar except `` ` ``, `\\`
* `AnyCharExceptRightParenNewline` — any Unicode scalar except `)`, U+000A
* `AnyCharExceptRightBracketNewline` — any Unicode scalar except `]`, U+000A
* `AnyCharExceptRightBracketBackslashNewline` — any Unicode scalar except `]`, `\\`, U+000A
* `AnyCharExceptBackslashNewline` — any Unicode scalar except `\\`, U+000A
* `AnyCharExceptValueTerminator` — any Unicode scalar except a Value terminator (defined in §A.1.27)

---

#### A.1.27 Value Termination and Disambiguation (Normative)

```ebnf
(* Value termination is token-level, not type-level.

	In a Concept marker, an unquoted Value token MUST terminate at the first of:
	- whitespace (space, tab, or newline)
	- ">" or "/>" (end of marker)

	While scanning for termination, parsers MUST respect balanced delimiters for
	delimited value spellings and composite literals, including:
	[], {}, (), '', "", and backticks.

	This appendix provides type grammars for each Value form, but conformance requires
	the termination behavior above.

	Value disambiguation is performed by deterministic precedence, applied to the
	maximal token recognized under the termination rule.

	Precedence (highest first):

	1. Delimited: StringValue, CharValue, BacktickString
	2. BooleanValue ("true" | "false")
	3. EnumeratedToken ($...)
	4. LookupToken (~...)
	5. TemporalValue ({...})
	6. SetValue (set[...])
	7. MapValue (map[...])
	8. ListValue ([...])
	9. TupleValue ((...))
	10. ColorValue (all permitted color literal spellings, including functions and named colors)
	11. UuidValue (8-4-4-4-12 with hex digits)
	12. RangeValue (contains ".." with valid endpoints)
	13. NumericValue (Complex/Imaginary/Fraction/Infinity/Precision/Scientific/Decimal/Integer per §A.1.12)
	14. IriReference (fallback: token contains ":" and matches IriReference)

	If a token matches multiple forms at the same precedence level, parsing MUST fail
	rather than guess. *)
```
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
# A Codex document contains exactly one root Concept.
# Surface-form rules constrain root count, blank-line placement, and annotation kinds.

Document <- LeadingAnnotationBlocks? RootConcept TrailingBlankLines EOF

LeadingAnnotationBlocks <- (BlankLine* Annotation BlankLine*)*

TrailingBlankLines <- BlankLine*

RootConcept <- ConceptAtColumn0

ConceptAtColumn0 <- (BOL ConceptLine0)

ConceptLine0 <- Concept Newline?

BOL <- &(StartOfFile / Newline)
StartOfFile <- !.

Concept <- BlockConcept / SelfClosingConcept
```

---

#### A.2.3 Block Concepts

```peg
# Block concepts contain either children or content.
# The parser consults the governing schema (ContentRules) to decide which Body to parse.
# This is schema-directed dispatch, not syntactic ambiguity.

BlockConcept <- OpeningMarkerLine Body ClosingMarkerLine

OpeningMarkerLine <- Indentation OpeningMarker Newline
ClosingMarkerLine <- Indentation ClosingMarker Newline

OpeningMarker <- '<' ConceptName Traits? '>'
ClosingMarker <- '</' ConceptName '>'

# Body is selected by schema lookup on ConceptName:
# - children mode (ForbidsContent): ChildrenBody
# - content mode (AllowsContent): ContentBody
Body <- ChildrenBody / ContentBody

# ChildrenBody admits BlankLine and Annotation; their legality and attachment kinds
# are checked by surface-form rules and canonicalization rules.
ChildrenBody <- ChildItem*

ChildItem <- BlankLine / AnnotationLine / AnnotationBlock / ConceptLine

ConceptLine <- Indentation (SelfClosingMarker / OpeningMarker) Newline
# Note: A full BlockConcept begins with OpeningMarkerLine and ends at its ClosingMarkerLine.
# This line-level production is used for child-start recognition only.

ContentBody <- ContentLine*

ContentLine <- Indentation ContentText Newline

ContentText <- ContentChar*
ContentChar <- ContentEscape / ContentSafeChar
ContentEscape <- '\\' ('<' / '[')
ContentSafeChar <- !Newline !'<' .
```

---

#### A.2.4 Self-Closing Concepts

```peg
SelfClosingConcept <- SelfClosingMarker

SelfClosingMarker <- '<' ConceptName Traits? '/>'
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
# Traits are whitespace-separated tokens in the opening marker.
# Newline is permitted in Whitespace, enabling multi-line trait layout;
# formatting rules define canonical layout.

Traits <- (WhitespaceNoNewline Trait (Whitespace Trait)*) / (Whitespace Trait (Whitespace Trait)*)

Trait <- TraitName '=' Value

TraitName <- LowercaseLetter (Letter / Digit)*
```

---

#### A.2.7 Values

```peg
# Values are tried in deterministic precedence order.
# Token termination in markers is governed by the surface rules (see A.1.27);
# this PEG uses explicit constructs for balanced literals.

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
      / ColorValue
      / UuidValue
      / RangeValue
      / NumericValue
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
CharEscapeSequence <- '\\' ( ["'\\nrt] / UnicodeEscape )
```

---

#### A.2.10 Backtick Strings

```peg
BacktickString <- '`' BacktickChar* '`'
BacktickChar <- BacktickEscape / (!'`' .)
BacktickEscape <- '\\' '`'
```

---

#### A.2.11 Boolean Values

```peg
BooleanValue <- 'true' / 'false'
```

---

#### A.2.12 Numeric Values

```peg
NumericValue <- ComplexNumber
             / ImaginaryNumber
             / Fraction
             / Infinity
             / PrecisionNumber
             / ScientificNumber
             / DecimalNumber
             / Integer

ComplexNumber <- (Integer / DecimalNumber) ([+-]) (Integer / DecimalNumber) 'i'
ImaginaryNumber <- (Integer / DecimalNumber) 'i'
Fraction <- Integer '/' IntDigits
Infinity <- Sign? 'Infinity'
PrecisionNumber <- DecimalNumber 'p' IntDigits?
ScientificNumber <- (Integer / DecimalNumber) [eE] Sign? IntDigits
DecimalNumber <- Sign? IntDigits '.' Digits
Integer <- Sign? IntDigits

Sign <- [+-]
Digits <- Digit+
IntDigits <- '0' / [1-9] Digit*
```

---

#### A.2.13 Enumerated Tokens

```peg
EnumeratedToken <- '$' UppercaseLetter (Letter / Digit)* TypeParameters?

TypeParameters <- '<' TypeArgument (',' TypeArgument)* '>'

TypeArgument <- EnumeratedToken / TypeUnion

TypeUnion <- '[' EnumeratedToken (',' EnumeratedToken)* ']'
```

---

#### A.2.14 Lookup Tokens

```peg
LookupToken <- '~' LowercaseLetter (Letter / Digit)*
```

---

#### A.2.15 Temporal Values

```peg
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
DurationComponent <- Digits [YMWD]
TimeDurationComponent <- Digits ('.' Digits)? [HMS]

ReservedTemporal <- 'now' / 'today'

Year <- Digit Digit Digit Digit
Month <- Digit Digit
Day <- Digit Digit
Hour <- Digit Digit
Minute <- Digit Digit
Second <- Digit Digit
Milliseconds <- Digit+
```

---

#### A.2.16 List Values

```peg
# Lists MAY contain arbitrary whitespace (including newlines) between tokens.

ListValue <- '[' WS* ListItems? WS* ']'
ListItems <- Value (WS* ',' WS* Value)*
```

---

#### A.2.17 Set Values

```peg
SetValue <- 'set' '[' WS* SetItems? WS* ']'
SetItems <- Value (WS* ',' WS* Value)*
```

---

#### A.2.18 Map Values

```peg
MapValue <- 'map' '[' WS* MapItems? WS* ']'
MapItems <- MapEntry (WS* ',' WS* MapEntry)*
MapEntry <- MapKey WS* ':' WS* Value
MapKey <- MapIdentifier / StringValue / CharValue / Integer / EnumeratedToken
MapIdentifier <- LowercaseLetter (Letter / Digit)*
```

---

#### A.2.19 Tuple Values

```peg
TupleValue <- '(' WS* TupleItems WS* ')'
TupleItems <- Value (WS* ',' WS* Value)*
```

---

#### A.2.20 Range Values

```peg
RangeValue <- RangeStart '..' RangeEnd ('s' StepValue)?
RangeStart <- TemporalValue / CharValue / NumericValue
RangeEnd <- TemporalValue / CharValue / NumericValue
StepValue <- TemporalValue / NumericValue
```

---

#### A.2.21 UUID Values

```peg
UuidValue <- Hex8 '-' Hex4 '-' Hex4 '-' Hex4 '-' Hex12
Hex8 <- HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit
Hex4 <- HexDigit HexDigit HexDigit HexDigit
Hex12 <- HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit
```

---

#### A.2.22 Color Values

```peg
# Color spellings are accepted as declarative literals; no semantic evaluation occurs.
# For function spellings, we accept any balanced-parentheses payload up to ')'.

ColorValue <- HexColor / NamedColor / ColorFunction

HexColor <- '#' (Hex3 / Hex4 / Hex6 / Hex8)
Hex3 <- HexDigit HexDigit HexDigit
Hex4 <- HexDigit HexDigit HexDigit HexDigit
Hex6 <- HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit
Hex8 <- HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit

NamedColor <- '&' [a-z]+

ColorFunction <- ColorFuncName '(' ColorPayload ')'
ColorFuncName <- 'rgb' / 'rgba' / 'hsl' / 'hsla' / 'hwb' / 'lab' / 'lch' / 'oklab' / 'oklch' / 'color'
              / 'color-mix' / 'device-cmyk'

# Accept payload as any chars except ')' and '\n' (conservative, still token-terminated by marker rules).
ColorPayload <- (!(')' / '\n') .)*
```

---

#### A.2.23 IRI References

```peg
# IRI references are fallback unquoted values that contain ':'.
# Exact RFC 3987 profiling is enforced by surface-form validation, not this PEG.

IriReference <- IriScheme ':' IriBody
IriScheme <- Letter (Letter / Digit / [+\-\.])*
IriBody <- IriTokenChar*
IriTokenChar <- !ValueTerminator .
```

---

#### A.2.24 Annotations

```peg
Annotation <- AnnotationLine / AnnotationBlock

AnnotationLine <- Indentation '[' AnnotationChar* ']' Newline

AnnotationBlock <- Indentation '[' Newline AnnotationBlockLine* Indentation ']' Newline

AnnotationBlockLine <- Indentation AnnotationBlockChar* Newline

AnnotationChar <- AnnotationEscape / (!(']' / '\n') .)
AnnotationEscape <- '\\' ']'

AnnotationBlockChar <- AnnotationEscape / (!'\n' .)
```

---

#### A.2.25 Whitespace and Structural Elements

```peg
Newline <- '\n'

WhitespaceChar <- [ \t\n]
Whitespace <- WhitespaceChar+

WhitespaceNoNewline <- [ \t]+

WS <- [ \t\n]

BlankLine <- [ \t]* Newline

Indentation <- '\t'*

# Conservative terminators for unquoted tokens in markers:
ValueTerminator <- [ \t\n] / '>' / '/'
```

---

#### A.2.26 End of File

```peg
EOF <- !.
```

---

## Appendix B. Codex Named Colors (Normative)

This appendix defines the complete set of named color keywords accepted in Codex Named Color Values (§5.7.1).

Codex-conforming tools MUST treat Color Values as opaque and MUST NOT infer, compute, normalize, or transform Color Values based on the keyword tables in this appendix.

The sRGB hex values shown are descriptive references only.

Aliases and duplicates (for example, `gray`/`grey`, `cyan`/`aqua`) are intentional and are part of the Codex named color set.

### B.1 Named Color Keyword Table

Each entry defines an accepted Codex Named Color Value (`&name`).

The sRGB hex column is informative and does not define Codex color semantics.

| Named color             |  sRGB hex |
| ----------------------- | --------: |
| `&aliceblue`            | `#f0f8ff` |
| `&antiquewhite`         | `#faebd7` |
| `&aqua`                 | `#00ffff` |
| `&aquamarine`           | `#7fffd4` |
| `&azure`                | `#f0ffff` |
| `&beige`                | `#f5f5dc` |
| `&bisque`               | `#ffe4c4` |
| `&black`                | `#000000` |
| `&blanchedalmond`       | `#ffebcd` |
| `&blue`                 | `#0000ff` |
| `&blueviolet`           | `#8a2be2` |
| `&brown`                | `#a52a2a` |
| `&burlywood`            | `#deb887` |
| `&cadetblue`            | `#5f9ea0` |
| `&chartreuse`           | `#7fff00` |
| `&chocolate`            | `#d2691e` |
| `&coral`                | `#ff7f50` |
| `&cornflowerblue`       | `#6495ed` |
| `&cornsilk`             | `#fff8dc` |
| `&crimson`              | `#dc143c` |
| `&cyan`                 | `#00ffff` |
| `&darkblue`             | `#00008b` |
| `&darkcyan`             | `#008b8b` |
| `&darkgoldenrod`        | `#b8860b` |
| `&darkgray`             | `#a9a9a9` |
| `&darkgrey`             | `#a9a9a9` |
| `&darkgreen`            | `#006400` |
| `&darkkhaki`            | `#bdb76b` |
| `&darkmagenta`          | `#8b008b` |
| `&darkolivegreen`       | `#556b2f` |
| `&darkorange`           | `#ff8c00` |
| `&darkorchid`           | `#9932cc` |
| `&darkred`              | `#8b0000` |
| `&darksalmon`           | `#e9967a` |
| `&darkseagreen`         | `#8fbc8f` |
| `&darkslateblue`        | `#483d8b` |
| `&darkslategray`        | `#2f4f4f` |
| `&darkslategrey`        | `#2f4f4f` |
| `&darkturquoise`        | `#00ced1` |
| `&darkviolet`           | `#9400d3` |
| `&deeppink`             | `#ff1493` |
| `&deepskyblue`          | `#00bfff` |
| `&dimgray`              | `#696969` |
| `&dimgrey`              | `#696969` |
| `&dodgerblue`           | `#1e90ff` |
| `&firebrick`            | `#b22222` |
| `&floralwhite`          | `#fffaf0` |
| `&forestgreen`          | `#228b22` |
| `&fuchsia`              | `#ff00ff` |
| `&gainsboro`            | `#dcdcdc` |
| `&ghostwhite`           | `#f8f8ff` |
| `&gold`                 | `#ffd700` |
| `&goldenrod`            | `#daa520` |
| `&gray`                 | `#808080` |
| `&grey`                 | `#808080` |
| `&green`                | `#008000` |
| `&greenyellow`          | `#adff2f` |
| `&honeydew`             | `#f0fff0` |
| `&hotpink`              | `#ff69b4` |
| `&indianred`            | `#cd5c5c` |
| `&indigo`               | `#4b0082` |
| `&ivory`                | `#fffff0` |
| `&khaki`                | `#f0e68c` |
| `&lavender`             | `#e6e6fa` |
| `&lavenderblush`        | `#fff0f5` |
| `&lawngreen`            | `#7cfc00` |
| `&lemonchiffon`         | `#fffacd` |
| `&lightblue`            | `#add8e6` |
| `&lightcoral`           | `#f08080` |
| `&lightcyan`            | `#e0ffff` |
| `&lightgoldenrodyellow` | `#fafad2` |
| `&lightgray`            | `#d3d3d3` |
| `&lightgrey`            | `#d3d3d3` |
| `&lightgreen`           | `#90ee90` |
| `&lightpink`            | `#ffb6c1` |
| `&lightsalmon`          | `#ffa07a` |
| `&lightseagreen`        | `#20b2aa` |
| `&lightskyblue`         | `#87cefa` |
| `&lightslategray`       | `#778899` |
| `&lightslategrey`       | `#778899` |
| `&lightsteelblue`       | `#b0c4de` |
| `&lightyellow`          | `#ffffe0` |
| `&lime`                 | `#00ff00` |
| `&limegreen`            | `#32cd32` |
| `&linen`                | `#faf0e6` |
| `&magenta`              | `#ff00ff` |
| `&maroon`               | `#800000` |
| `&mediumaquamarine`     | `#66cdaa` |
| `&mediumblue`           | `#0000cd` |
| `&mediumorchid`         | `#ba55d3` |
| `&mediumpurple`         | `#9370db` |
| `&mediumseagreen`       | `#3cb371` |
| `&mediumslateblue`      | `#7b68ee` |
| `&mediumspringgreen`    | `#00fa9a` |
| `&mediumturquoise`      | `#48d1cc` |
| `&mediumvioletred`      | `#c71585` |
| `&midnightblue`         | `#191970` |
| `&mintcream`            | `#f5fffa` |
| `&mistyrose`            | `#ffe4e1` |
| `&moccasin`             | `#ffe4b5` |
| `&navajowhite`          | `#ffdead` |
| `&navy`                 | `#000080` |
| `&oldlace`              | `#fdf5e6` |
| `&olive`                | `#808000` |
| `&olivedrab`            | `#6b8e23` |
| `&orange`               | `#ffa500` |
| `&orangered`            | `#ff4500` |
| `&orchid`               | `#da70d6` |
| `&palegoldenrod`        | `#eee8aa` |
| `&palegreen`            | `#98fb98` |
| `&paleturquoise`        | `#afeeee` |
| `&palevioletred`        | `#db7093` |
| `&papayawhip`           | `#ffefd5` |
| `&peachpuff`            | `#ffdab9` |
| `&peru`                 | `#cd853f` |
| `&pink`                 | `#ffc0cb` |
| `&plum`                 | `#dda0dd` |
| `&powderblue`           | `#b0e0e6` |
| `&purple`               | `#800080` |
| `&rebeccapurple`        | `#663399` |
| `&red`                  | `#ff0000` |
| `&rosybrown`            | `#bc8f8f` |
| `&royalblue`            | `#4169e1` |
| `&saddlebrown`          | `#8b4513` |
| `&salmon`               | `#fa8072` |
| `&sandybrown`           | `#f4a460` |
| `&seagreen`             | `#2e8b57` |
| `&seashell`             | `#fff5ee` |
| `&sienna`               | `#a0522d` |
| `&silver`               | `#c0c0c0` |
| `&skyblue`              | `#87ceeb` |
| `&slateblue`            | `#6a5acd` |
| `&slategray`            | `#708090` |
| `&slategrey`            | `#708090` |
| `&snow`                 | `#fffafa` |
| `&springgreen`          | `#00ff7f` |
| `&steelblue`            | `#4682b4` |
| `&tan`                  | `#d2b48c` |
| `&teal`                 | `#008080` |
| `&thistle`              | `#d8bfd8` |
| `&tomato`               | `#ff6347` |
| `&turquoise`            | `#40e0d0` |
| `&violet`               | `#ee82ee` |
| `&wheat`                | `#f5deb3` |
| `&white`                | `#ffffff` |
| `&whitesmoke`           | `#f5f5f5` |
| `&yellow`               | `#ffff00` |
| `&yellowgreen`          | `#9acd32` |

### B.2 Context-Dependent Keywords

The following keywords are accepted as Codex named colors but do not have a single fixed sRGB value in all contexts.

These values are valid Codex Color Values, but Codex does not define any fixed expansion or interpretation for them.

Codex-conforming tools MUST treat these values as opaque Color Values and MUST NOT attempt to resolve them.

| Named color     | Notes                                                                                       |
| --------------- | ------------------------------------------------------------------------------------------- |
| `&transparent`  | Context-dependent; informative reference sRGB form: `#00000000`.                            |
| `&currentcolor` | Context-dependent.                                                                          |

---

**End of Codex Language Specification v1.0.0 BETA**
