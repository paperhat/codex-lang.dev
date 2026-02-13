Status: NORMATIVE  
Lock State: LOCKED  
Version: 1.0.0  
Editor: Charles F. Munat

**This specification is locked. No modifications—including clarifications, corrections, or improvements—are permitted without explicit approval from the editor.**

# Codex Language Specification — Version 1.0.0

This document is the authoritative language specification for Codex 1.0.0.

All normative requirements for Codex 1.0.0 MUST appear exactly once in this document.

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

Codex 1.0.0 does not define:

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

- All sections are normative unless explicitly labeled **Informative**.
- Text labeled **Informative** is explanatory and does not define requirements.
- Examples are illustrative and non-normative.

All statements that do not use **MUST** or **MUST NOT** are informative.

A conforming implementation satisfies every normative requirement in this specification.

#### 1.3.1 Consistency Guarantee

This specification contains no internal conflicts.

The prose sections of this specification are the sole source of authority for all syntactic and semantic rules. Appendix A provides informative grammar projections (EBNF and PEG) that illustrate the prose rules in a formal notation. In case of discrepancy between prose and grammar, the prose is authoritative.

The bootstrap schemas (`bootstrap-schema/schema.cdx` and `bootstrap-schema/simplified/schema.cdx`) instantiate the schema-definition rules defined in this specification. They are derived artifacts, not independent sources of authority.

If an implementer discovers an apparent conflict between any parts of this specification or between this specification and the bootstrap schemas, that conflict is a defect. Implementers MUST NOT guess which source prevails. Implementers MUST report the defect.

---

## 2. Language Invariants

### 2.1 Declarative and Closed-World Model

Codex is a declarative language with closed-world semantics.

A conforming implementation MUST treat something not explicitly declared as not present.

An implementation MUST NOT infer meaning from omission, shape, or other non-specified cues.

An implementation MUST NOT assume defaults unless explicitly defined by this specification or by the governing schema.

Structural ordering carries no semantic meaning to Codex itself. Trait order in canonical form is alphabetical by Trait name (§10.4); implementations MUST NOT treat Trait order as semantically significant. For children and collection elements, schemas define whether ordering is semantically significant (§11.3). Implementations MUST preserve the ordering of children and collection elements both for round-trippability (see §2.6) and to support schema-defined ordering constraints.

### 2.2 Determinism and Explainability

Given the same inputs, all conforming implementations MUST produce identical results.

Required inputs are:

- document bytes
- governing schema (for validation; not required for well-formedness checking)
- imported schemas (for validation of documents with schema imports; see §11.2.1)
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
- Formatting and canonicalization MUST be mechanical and MUST NOT perform schema validation.
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

Well-formedness checking includes mechanically recognizing and classifying Value spellings into their Value kinds (and any grammar-defined value types) by applying the spelling rules defined in §5 and §8.

Expected types and type constraints for Trait values are schema-defined; checking a Trait value against its expected `ValueType` is part of schema validation and therefore requires an explicit governing schema.

The bootstrap schema-of-schemas provides a built-in governing schema only for schema documents (§12.3) and MUST NOT be used as a fallback governing schema for instance documents.

In this document, the term **schema validation** refers only to the schema-based semantic phase. When referring to the schema-free phase, this document uses **parse** and **check well-formedness**.

### 2.6 Round-Trippability

Round-trippability applies to the canonical form, not raw input. Raw input may use arbitrary whitespace or non-canonical formatting. Canonicalization (similar to `gofmt`) normalizes raw input to a single canonical surface form. Round-tripping preserves this canonical form.

A conforming implementation MUST support round-tripping: a canonicalized Codex document, after transformation to RDF triples, storage, retrieval via SPARQL, and reconstruction, MUST produce a byte-identical canonicalized document.

This invariant ensures that Codex serves as a lossless serialization format for RDF data. Structural ordering, annotations, and all surface-form details MUST survive the round-trip. The round-trip guarantee is achieved through the triple store projection alone, with no sidecar artifacts required.

To guarantee round-trippability, a conforming implementation MUST provide the following capabilities:

- canonicalization (raw bytes → canonical surface form)
- parsing (canonical surface form → AST)
- validation (AST + schema → IR)
- triple serialization (IR → RDF/SHACL triples)
- triple reconstruction (SPARQL query results → canonical Codex)

These capabilities MUST compose such that: for any valid input, canonicalizing the reconstructed output produces a byte-identical result to canonicalizing the original input.

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

A Concept instance MUST NOT declare two or more Traits with the same Trait name. A violation MUST be rejected with a `SurfaceFormError` (§14).

Trait meaning and permissibility MUST be defined by the governing schema, except for language-level traits whose meaning is defined by this specification (§6, §7).

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

If the governing schema does not declare `entityEligibility` for a Concept, schema validation MUST fail with a `SchemaError` (§14).

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

#### 4.1.1 Qualified Names

A **qualified name** combines a namespace prefix with a Concept name or Trait name, separated by a colon (`:`) with no surrounding whitespace.

A **namespace prefix** MUST be a camelCase name (same form as a Trait name per §4.1).

The two qualified name forms are:

* **Qualified Concept name**: `namespacePrefix:ConceptName` — a namespace prefix followed by `:` followed by a PascalCase Concept name.
* **Qualified Trait name**: `namespacePrefix:traitName` — a namespace prefix followed by `:` followed by a camelCase Trait name.

The namespace prefix and the local name MUST each satisfy the naming rules of §4.1 and §4.2 independently.

Qualified names MUST only appear in contexts where schema imports are in effect (§11.2.1). The namespace prefix MUST resolve to an imported schema via the document's `SchemaImports` declarations.

Language-level Trait names (`id`, `key`, `reference`, `target`, `for`) MUST NOT be namespace-qualified. These Traits are defined by this specification (§6–§7), not by any schema.

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

### 5.1 Text Values

A Text Value is a sequence of zero or more Unicode scalar values as defined by Unicode 16.0.0. An empty Text Value (zero scalar values) is permitted.

In the Surface Form, Text Values MUST be spelled as quoted text literals or backtick text (see §5.2). Appendix A.1.8 and A.2.8 provide informative grammar projections of these rules.

A quoted text literal is delimited by double-quote characters (`"..."`) and MUST NOT contain raw newlines (U+000A). Within the quotes, any Unicode scalar value other than `"` (U+0022), `\` (U+005C), or newline (U+000A) may appear literally. The `\` character introduces an escape sequence. The permitted escape sequences are:

- `\"` — literal double quote
- `\\` — literal backslash
- `\uXXXX` — Unicode scalar value specified by exactly four hexadecimal digits
- `\u{X...}` — Unicode scalar value specified by one or more hexadecimal digits enclosed in braces

Hexadecimal digits in escape sequences are case-insensitive for parsing. A Unicode escape MUST identify a Unicode scalar value (U+0000 to U+D7FF or U+E000 to U+10FFFF).

After interpreting escape sequences, the resulting character sequence MUST be transformed into the resulting Text Value by applying the following whitespace normalization:

- Each maximal run of characters with the Unicode `White_Space` property (as defined by Unicode 16.0.0) MUST be replaced with a single U+0020 SPACE.
- Leading and trailing U+0020 SPACE MUST be removed.

This normalization applies to all Text Value spellings (quoted text and backtick text). The resulting Text Value MUST be single-line.

### 5.2 Backtick Text

A Backtick Text is a surface-form spelling of a Text Value, delimited by backtick characters (`` ` ``).

Backtick text MUST allow authors to write Text Values that span multiple source lines.

Within a Backtick Text, `` \` `` represents a literal `` ` ``.

A backslash not immediately followed by a backtick is a literal backslash and has no special meaning.
The Text Value normalization defined in §5.1 applies after escape interpretation.

### 5.3 Boolean Values

A Boolean Value is one of two values: true or false.

In the Surface Form, Boolean Values MUST be spelled as the tokens `true` and `false`.

No other spellings are permitted.

### 5.4 Numeric Values

Each type defined in §5.4.1–§5.4.9 is an independent standalone value type, determined by lexical form at parse time during well-formedness checking (§2.5). No schema is required for type determination. `$Number` (§11.5) is a union type token that accepts any of these types. It is not a parent type.

When the surface spelling could match multiple type grammars, the type MUST be the first match in this order: ComplexNumber, ImaginaryNumber, PrecisionNumber, ExponentialNumber, Fraction, PositiveInfinity, NegativeInfinity, DecimalNumber, Integer.

Codex performs no arithmetic and no numeric normalization. Spellings MUST be preserved exactly. Value-level `+` signs MUST NOT appear; absence of a sign indicates a positive value. Exponent signs in ExponentialNumber (§5.4.3) and complex-number signs in ComplexNumber (§5.4.9) are not value-level signs.

Integer digit sequences MUST NOT have leading zeros, except that the single digit `0` is permitted. A sign character (if present) is not part of the integer component. This applies to: Integer values, the integer part of DecimalNumber, the exponent digits of ExponentialNumber, the precision suffix digits of PrecisionNumber, and Fraction denominators.

NaN MUST NOT appear.

When mapped to XSD datatypes for the RDF canonical representation (§9), `Infinity` MUST be translated to `INF` and `-Infinity` MUST be translated to `-INF`.

#### 5.4.1 Integer

An Integer value represents a whole number.

The literal `0`, or an optional `-` sign followed by a non-zero ASCII digit (`1`–`9`) followed by zero or more ASCII digits (`0`–`9`).

The spelling `-0` MUST NOT appear. A conforming implementation MUST reject it as a `SurfaceFormError` (§14).

Integer constraint tokens for schema validation (§11.5): `$Zero` (spelling `0`), `$PositiveInteger` (no `-`, digits not `0`), `$NegativeInteger` (`-` present, digits not `0`), `$NonNegativeInteger` (`$Zero` or `$PositiveInteger`), `$NonPositiveInteger` (`$Zero` or `$NegativeInteger`). These are schema-level constraint tokens, not separate types.

#### 5.4.2 DecimalNumber

A DecimalNumber value represents a number with a decimal point.

An optional `-` sign, followed by an integer digit sequence (satisfying the no-leading-zeros rule), followed by a `.` (U+002E), followed by one or more ASCII digits (`0`–`9`).

`-0.0` is permitted. The Integer `-0` prohibition does not apply to DecimalNumber. Trailing zeros after the decimal point are significant (spelling is preserved).

#### 5.4.3 ExponentialNumber

An ExponentialNumber value represents a number in scientific notation.

An Integer or DecimalNumber base, followed by `e` or `E`, followed by an optional sign (`+` or `-`), followed by an integer digit sequence (satisfying the no-leading-zeros rule).

The `+` or `-` after `e`/`E` is the exponent sign, not a value-level sign. The value-level `+` prohibition does not apply here. Case of `e`/`E` is preserved (spelling preservation).

#### 5.4.4 PrecisionNumber

A PrecisionNumber value represents a number with declared measurement precision.

A DecimalNumber followed by `p`, optionally followed by an integer digit sequence (satisfying the no-leading-zeros rule).

Declared precision is a count of decimal places, determined by:

- Inferred: the count of digits after the decimal point in the DecimalNumber base, including trailing zeros.
- Explicit: the integer after `p`, which overrides inferred precision.

Consuming systems MUST preserve the declared precision.

#### 5.4.5 Fraction

A Fraction value represents a rational number as a numerator/denominator pair.

An Integer (numerator) followed by `/` (U+002F) followed by an integer digit sequence (denominator, satisfying the no-leading-zeros rule).

The denominator MUST NOT be `0`. A conforming implementation MUST reject a zero denominator as a `SurfaceFormError` (§14).

Fractions MUST NOT be reduced or normalized. The spelling is preserved exactly.

#### 5.4.6 PositiveInfinity

A PositiveInfinity value represents positive infinity.

The literal spelling `Infinity`.

#### 5.4.7 NegativeInfinity

A NegativeInfinity value represents negative infinity.

The literal spelling `-Infinity`.

`+Infinity` MUST NOT appear. `$Infinity` (§11.5) is a union type token accepting either PositiveInfinity or NegativeInfinity. It is not a parent type.

#### 5.4.8 ImaginaryNumber

An ImaginaryNumber value represents a pure imaginary number.

An Integer or DecimalNumber followed immediately by `i` (U+0069).

#### 5.4.9 ComplexNumber

A ComplexNumber value represents a complex number with real and imaginary parts.

An Integer or DecimalNumber (real part), followed by `+` or `-`, followed by an Integer or DecimalNumber (imaginary coefficient), followed immediately by `i` (U+0069).

The `+` or `-` between the real and imaginary parts is the complex-number sign, not a value-level sign. The value-level `+` prohibition does not apply here.

The meaning of any value of these types beyond its literal spelling MUST be defined by the governing schema or consuming system.

`$RealNumber` (§11.5) is a union type token accepting Integer, DecimalNumber, ExponentialNumber, PrecisionNumber, Fraction, PositiveInfinity, or NegativeInfinity. It is not a parent type.

`$FiniteNumber` (§11.5) is a union type token accepting Integer, DecimalNumber, ExponentialNumber, PrecisionNumber, Fraction, ImaginaryNumber, or ComplexNumber. It is not a parent type.

`$FiniteRealNumber` (§11.5) is a union type token accepting Integer, DecimalNumber, ExponentialNumber, PrecisionNumber, or Fraction. It is not a parent type. The membership of `$FiniteRealNumber` is the same as the `OrderedNumericValue` grammar rule (Appendix A).

`$ExactNumber` (§11.5) is a union type token accepting Integer or Fraction. It is not a parent type.

### 5.5 Enumerated Token Values

An Enumerated Token Value is a Value drawn from a schema-defined closed set.

In the Surface Form, Enumerated Token Values MUST be spelled with a leading `$` sigil followed by a token name. The token name MUST use PascalCase. An Enumerated Token Value spelling may include type parameters as defined in §5.18.

Enumerated Token Values MUST NOT be treated as Text Values.

Enumerated Token Values MUST NOT be evaluated.

### 5.6 Temporal Values

A Temporal Value represents a declarative temporal literal.

In the Surface Form, Temporal Values MUST be spelled as `{` followed by a Temporal Body followed by `}`.

Well-formedness checking and temporal kind determination are purely syntactic.

During semantic validation, when a schema declares an expected temporal value type (for example, `$PlainDate`), tools MUST parse the braced payload into that temporal type and MUST reject values that are semantically invalid for that type (for example, an impossible date).

Temporal Keywords (`{now}` and `{today}`) MUST remain symbolic during semantic validation unless the governing schema explicitly defines otherwise; they MUST NOT be evaluated implicitly.

#### 5.6.1 Temporal Kind Determination

To classify a Temporal Value as a specific temporal kind, tools MUST parse the Temporal Body using the spelling rules defined in §5.6.2.

This classification is purely syntactic and depends only on the braced payload; it does not imply temporal evaluation or interpretation.

The temporal kind MUST be determined by the first matching alternative in the following ordered list:

1. `ZonedDateTime`
2. `Instant`
3. `PlainDateTime`
4. `PlainDate`
5. `YearWeek`
6. `PlainYearMonth`
7. `PlainMonthDay`
8. `PlainTime`
9. `Duration`
10. `TemporalKeyword`

Temporal Values MUST NOT be treated as Enumerated Token Values, even when the braced payload is a reserved literal such as `now` or `today`.

#### 5.6.2 Temporal Spelling Rules

This subsection defines the complete spelling rules for each temporal kind. Appendix A.1.14 and A.2.15 provide informative grammar projections of these rules.

**Common components**

The following common components are used by the temporal kinds below:

- A `Year` MUST be spelled as exactly four decimal digits (`0`–`9`).
- A `Month` MUST be spelled as exactly two decimal digits.
- A `Day` MUST be spelled as exactly two decimal digits.
- An `Hour` MUST be spelled as exactly two decimal digits.
- A `Minute` MUST be spelled as exactly two decimal digits.
- A `Second` MUST be spelled as exactly two decimal digits.
- `FractionalSeconds` MUST be spelled as one or more decimal digits.
- A `WeekNumber` MUST be spelled as exactly two decimal digits.

**PlainDate**

A `PlainDate` MUST be spelled as `Year`, `-`, `Month`, `-`, `Day` (for example, `2024-03-15`).

**YearWeek**

A `YearWeek` MUST be spelled as `Year`, `-`, `W` or `w`, `WeekNumber` (for example, `2024-W12`).

**PlainYearMonth**

A `PlainYearMonth` MUST be spelled as `Year`, `-`, `Month` (for example, `2024-03`).

**PlainMonthDay**

A `PlainMonthDay` MUST be spelled as `Month`, `-`, `Day` (for example, `03-15`).

**PlainTime**

A `PlainTime` MUST be spelled as `Hour`, `:`, `Minute`, optionally followed by `:`, `Second`, which itself is optionally followed by `.`, `FractionalSeconds` (for example, `14:30`, `14:30:00`, `14:30:00.123`).

**PlainDateTime**

A `PlainDateTime` MUST be spelled as a `PlainDate`, followed by `T`, followed by a `PlainTime` (for example, `2024-03-15T14:30:00`).

**Timezone offset**

A timezone offset MUST be spelled as either `Z` or as `+` or `-` followed by `Hour`, `:`, `Minute` (for example, `Z`, `+05:30`, `-08:00`).

**Timezone identifier**

A timezone identifier MUST be spelled as `[`, followed by one or more timezone identifier characters, followed by `]`. A timezone identifier character MUST be an ASCII letter, an ASCII digit, `/`, `_`, or `-` (for example, `[America/New_York]`).

**Instant**

An `Instant` MUST be spelled as a `PlainDateTime` followed by a timezone offset (for example, `2024-03-15T14:30:00Z`).

**ZonedDateTime**

A `ZonedDateTime` MUST be spelled as a `PlainDateTime`, followed by a timezone offset, followed by a timezone identifier (for example, `2024-03-15T14:30:00-05:00[America/New_York]`).

**Duration**

A `Duration` MUST be spelled in one of two forms:

- `P` followed by one or more date duration components, optionally followed by `T` and one or more time duration components.
- `PT` followed by one or more time duration components.

A date duration component MUST be spelled as one or more decimal digits followed by one of `Y`, `M`, `W`, or `D`.

A time duration component MUST be spelled as one or more decimal digits, optionally followed by `.` and one or more decimal digits, followed by one of `H`, `M`, or `S`.

For example: `P1Y2M3D`, `PT1H30M`, `P1Y2M3DT4H5M6S`, `PT0.5S`.

**TemporalKeyword**

A `TemporalKeyword` MUST be exactly `now` or `today`.

`$TemporalPoint` (§11.5) is a union type token accepting PlainDate, PlainTime, PlainDateTime, PlainYearMonth, PlainMonthDay, YearWeek, Instant, or ZonedDateTime. It is not a parent type.

### 5.7 Color Values

A Color Value MUST NOT be treated as a Text Value.

Well-formedness checking for Color Values is lexical and does not require a schema.

During semantic validation, when a schema declares an expected color value type (for example, `$Color` or a more specific built-in color type), tools MUST interpret the lexical spelling into a semantic color value of the expected type and MUST reject values that cannot be converted into a valid color in that type.

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

#### 5.7.1 Color Kind Determination

To classify a Color Value as a specific color kind, tools MUST identify the surface spelling and apply the first matching rule in the following ordered list:

1. `HexColor` — spelling begins with `#`
2. `NamedColor` — spelling begins with `&`
3. `RgbColor` — function name is `rgb` or `rgba`
4. `HslColor` — function name is `hsl` or `hsla`
5. `HwbColor` — function name is `hwb`
6. `LabColor` — function name is `lab`
7. `LchColor` — function name is `lch`
8. `OklabColor` — function name is `oklab`
9. `OklchColor` — function name is `oklch`
10. `ColorMix` — function name is `color-mix`
11. `DeviceCmyk` — function name is `device-cmyk`
12. `ColorSpaceColor` — function name is `color`

This classification is purely syntactic and depends only on the surface spelling; it does not imply color evaluation or interpretation.

Function name matching for color kind determination is case-insensitive (see §5.7 for canonical case rules).

A relative color form (containing `from` after the function name) retains the color kind determined by its enclosing function name.

#### 5.7.2 Named Color Values

In the Surface Form, a Named Color Value MUST be spelled as `&` followed immediately by a color name.

The color name MUST consist only of ASCII lowercase letters (`a` through `z`).

The color name MUST be one of the named color keywords defined in Appendix B; an unrecognized color name is a ParseError (§14).

During semantic validation, a recognized named color MUST be interpreted as the sRGB RGBA value defined for that keyword in Appendix B.

#### 5.7.3 Deterministic Conversion-Based Validity (Lab/LCH, OKLab/OKLCH)

For `lab(...)`, `lch(...)`, `oklab(...)`, and `oklch(...)`, this specification defines semantic validity by **deterministic conversion** to *linear sRGB* (D65).

This subsection exists because these perceptual color spaces do not admit simple per-component bounds that are both non-arbitrary and interoperable.

During semantic validation, when a schema expects any of:

- `$LabColor` / `$LchColor` / `$OklabColor` / `$OklchColor`, or
- `$Color` in a position where these color functions are permitted,

tools MUST:

1. Parse the function arguments per the color function argument spelling rules of §5.7.4, producing numeric components.
2. Convert the parsed components to linear sRGB (D65) using the algorithm and constants defined in this subsection.
3. Reject the value with a `SchemaError` (§14) if the conversion produces any non-finite intermediate value, or if the resulting linear sRGB components are not all within the closed interval `[0,1]`.

Tools MUST NOT clamp, normalize, wrap hues, or apply gamut mapping.

For `lch(...)` and `oklch(...)`, hue MUST satisfy the Hue rule defined in §5.7.4.

**Numeric requirements**

The conversion MUST be computed using a deterministic binary floating-point arithmetic model with precision `p = 256` bits, using round-to-nearest ties-to-even.

Every non-dot-product arithmetic operation used by this subsection (addition, subtraction, multiplication, division, comparisons, and the cube computations used by the `lab(...)` transfer) MUST compute its result in this `p = 256` model, rounding to `p = 256` before any subsequent operation.

All matrix-vector multiplications in this subsection MUST be evaluated using the following single mandated dot-product procedure.

Given a row vector `(a0, a1, a2)` and a column vector `(b0, b1, b2)`, compute:

1. Compute the three products `p_i = a_i * b_i` using precision `p' = 768` bits, round-to-nearest ties-to-even.
2. Compute the sum `s = p_0 + p_1 + p_2` using precision `p' = 768` bits, round-to-nearest ties-to-even.
3. Round `s` once to precision `p = 256` bits, round-to-nearest ties-to-even, yielding the dot-product result.

Each matrix-vector product component MUST be computed by applying the above procedure to the corresponding matrix row and input vector.

No additional intermediate rounding to `p = 256` is permitted except the single rounding in step (3) above.

The trigonometric functions `sin` and `cos` used by `lch(...)` and `oklch(...)` MUST be computed as correctly-rounded results in precision `p = 256`.

The functions `sqrt`, `cbrt`, and `atan2` used by §5.7 MUST be computed as correctly-rounded results in precision `p = 256`.

The real-exponent power computations required by §5.7 (for example, raising a channel to `2.4`, `1/2.4`, `563/256`, `256/563`, `1.8`, `1/1.8`, `0.45`, and `1/0.45`) MUST be computed as correctly-rounded results in precision `p = 256`.

Tools MUST NOT use lower-precision arithmetic for any intermediate step, and MUST NOT approximate this procedure using binary64 or binary128.

**Constants**

Define:

- `ε = 216/24389`
- `κ = 24389/27`
- `π`: the correctly-rounded value of the mathematical constant π in precision `p = 256`, round-to-nearest ties-to-even

Define reference whites (XYZ, scaled so `Y=1`) from chromaticity coordinates as:

- D50: `x=0.3457`, `y=0.3585`; `X=x/y`, `Y=1`, `Z=(1-x-y)/y`
- D65: `x=0.3127`, `y=0.3290`; `X=x/y`, `Y=1`, `Z=(1-x-y)/y`

Define the Bradford chromatic adaptation matrix (D50 → D65):

$$
M_{D50\to D65} =
\begin{bmatrix}
0.955473421488075 & -0.02309845494876471 & 0.06325924320057072\\
-0.0283697093338637 & 1.0099953980813041 & 0.021041441191917323\\
0.012314014864481998 & -0.020507649298898964 & 1.330365926242124
\end{bmatrix}
$$

Define the XYZ (D65) → linear sRGB matrix:

$$
M_{XYZ\to lin\_sRGB} =
\begin{bmatrix}
3.2409699419045226 & -1.537383177570094 & -0.4986107602930034\\
-0.9692436362808796 & 1.8759675015077202 & 0.04155505740717559\\
0.05563007969699366 & -0.20397695888897652 & 1.0569715142428786
\end{bmatrix}
$$

Define OKLab conversion matrices (OKLab → XYZ D65) as follows.

First define the OKLab-to-LMS mixing matrix:

$$
M_{OKLab\to LMS} =
\begin{bmatrix}
1 & 0.3963377773761749 & 0.2158037573099136\\
1 & -0.1055613458156586 & -0.0638541728258133\\
1 & -0.0894841775298119 & -1.2914855480194092
\end{bmatrix}
$$

Then define the LMS-to-XYZ matrix:

$$
M_{LMS\to XYZ} =
\begin{bmatrix}
1.2268798758459243 & -0.5578149944602171 & 0.2813910456659647\\
-0.0405757452148008 & 1.1122868032803170 & -0.0717110580655164\\
-0.0763729366746601 & -0.4214933324022432 & 1.5869240198367816
\end{bmatrix}
$$

**Algorithms**

All matrix multiplications below are standard `3x3` by `3x1` products.

1) `lab(...)` → XYZ D50

Given `(L, a, b)` and a D50 white `(X_n, Y_n, Z_n)`:

- `f1 = (L + 16) / 116`
- `f0 = a / 500 + f1`
- `f2 = f1 - b / 200`

Then:

- `x = (f0^3 > ε) ? f0^3 : (116*f0 - 16) / κ`
- `y = (L > κ*ε) ? ((L + 16) / 116)^3 : L / κ`
- `z = (f2^3 > ε) ? f2^3 : (116*f2 - 16) / κ`

Return `XYZ_D50 = (x*X_n, y*Y_n, z*Z_n)`.

2) `lch(...)` → `lab(...)`

Given `(L, C, h)` where `h` is degrees:

- `h_r = h * (π/180)`
- `a = C * cos(h_r)`
- `b = C * sin(h_r)`

Then proceed as for `lab(...)`.

3) XYZ D50 → XYZ D65

`XYZ_D65 = M_D50_to_D65 * XYZ_D50`

4) `oklab(...)` → XYZ D65

Given `(L, a, b)` (OKLab uses D65):

- `(l', m', s') = M_OKLab_to_LMS * (L, a, b)`
- `(l, m, s) = (l'^3, m'^3, s'^3)`
- `XYZ_D65 = M_LMS_to_XYZ * (l, m, s)`

5) `oklch(...)` → `oklab(...)`

Given `(L, C, h)` where `h` is degrees:

- `h_r = h * (π/180)`
- `a = C * cos(h_r)`
- `b = C * sin(h_r)`

Then proceed as for `oklab(...)`.

6) XYZ D65 → linear sRGB

`lin_sRGB = M_XYZ_to_lin_sRGB * XYZ_D65`

The value is semantically valid iff all three components of `lin_sRGB` are finite and each is in `[0,1]`.

#### 5.7.4 Schema-Directed Semantic Color IR

This subsection defines the complete color function argument spelling rules and semantic color value domains used by schema validation for the built-in color `ValueType` tokens listed in §11.5.1. Appendix A.1.15 and A.2.23 provide informative grammar projections of these rules.

These rules apply only during schema-driven semantic validation. They MUST NOT rewrite or normalize the canonical surface spelling.

**Deterministic numeric interpretation**

All arithmetic required by this subsection (including percent conversion, normalization by division, and range comparisons) MUST be performed using the deterministic binary floating-point model defined by §5.7.3 (precision `p=256`, round-to-nearest ties-to-even).

All component inputs and computed intermediates used by this subsection MUST be finite, per the non-finite rejection rule in §5.7.3.

Percent values are interpreted by dividing by 100 in the mandated numeric model.

**Color function argument spelling**

Color function spellings obey the following structural rules.

A color function is written as `functionName(arguments)`. The function name is case-insensitive for parsing; lowercase is canonical (§5.7).

Newlines MUST NOT appear inside color function parentheses. Whitespace inside color function parentheses consists of spaces (U+0020) and tabs (U+0009) only.

Numeric arguments in color functions use the real-number subset of the Numeric Value form (§5.4): integers, decimal numbers, exponential numbers, precision-annotated numbers, rational fractions, and `Infinity`/`-Infinity`. Complex and imaginary numbers MUST NOT appear in color function arguments.

A percentage argument is a real number immediately followed by `%` with no intervening whitespace.

Color functions accept arguments in one of two separator styles:

- **Modern syntax**: components are separated by whitespace; if an alpha component is present, it follows a `/` separator with optional surrounding whitespace.
- **Legacy syntax**: components are separated by commas with optional surrounding whitespace; if an alpha component is present, it follows a comma.

`rgb(...)`/`rgba(...)` and `hsl(...)`/`hsla(...)` MUST accept both modern and legacy syntax. All other color functions MUST use modern syntax only.

The `color(...)` function is written as `color(ColorSpace c1 c2 c3)` with an optional alpha. `ColorSpace` is one of the RGB color space tokens (`srgb`, `srgb-linear`, `display-p3`, `a98-rgb`, `prophoto-rgb`, `rec2020`) or XYZ color space tokens (`xyz`, `xyz-d50`, `xyz-d65`). For RGB color spaces, each component is a percentage or a number. For XYZ color spaces, each component is a number.

The `color-mix(...)` function is written as `color-mix(in ColorSpace, stop, stop, ...)` where at least two stops are required and stops are comma-separated. Each stop is a Color Value optionally followed by a percentage weight.

A relative color function is written as `functionName(from originColor c1 c2 c3)` with an optional alpha, where `originColor` is any Color Value. Each channel position accepts either a literal value of the type normally expected for that position, or a single-letter channel keyword referencing the corresponding channel of the origin color after decomposition into the target function's color space. The alpha position accepts the keyword `a` to reference the origin color's alpha. Channel keywords by function:

- `rgb`/`rgba`: `r`, `g`, `b`
- `hsl`/`hsla`: `h`, `s`, `l`
- `hwb`: `h`, `w`, `b`
- `lab`: `l`, `a`, `b`
- `lch`: `l`, `c`, `h`
- `oklab`: `l`, `a`, `b`
- `oklch`: `l`, `c`, `h`
- `color(ColorSpace ...)`: `r`, `g`, `b`, `x`, `y`, `z`

**Alpha**

Where an alpha component is permitted:

- If alpha is spelled as a percentage, it MUST be in `[0%,100%]` and is interpreted as `alpha` in `[0,1]`.
- If alpha is spelled as a number, it MUST be in `[0,1]` and is interpreted as `alpha` in `[0,1]`.

If alpha is omitted, `alpha = 1`.

**Hue**

Where a hue component is permitted (in `hsl(...)`, `hwb(...)`, `lch(...)`, and `oklch(...)`), hue is a bare numeric angle in degrees. A hue component MUST NOT be spelled as a percentage. Hue values MUST be finite and MUST satisfy `0 <= h < 360`. See §5.7.3 for the general prohibition on clamping, normalization, hue wrapping, and gamut mapping.

**Semantic domains by built-in ValueType**

When a schema expects:

- `$HexColor`: tools MUST decode the hex spelling into a semantic RGBA value with 8-bit components.
	- `#RGB` expands each nibble to a byte (`#abc` → `#aabbcc`) and uses `alpha=255`.
	- `#RGBA` expands each nibble to a byte and decodes alpha similarly.
	- `#RRGGBB` and `#RRGGBBAA` decode each pair as a byte.

- `$NamedColor`: tools MUST validate that the name is a keyword in Appendix B and compile the semantic value as the corresponding sRGB RGBA value defined by Appendix B.

- `$RgbColor`: tools MUST parse `rgb(...)`/`rgba(...)` — three RGB components (red, green, blue) and an optional alpha, in modern or legacy syntax — and compile a semantic sRGB value `(r,g,b,alpha)` where each component is in `[0,1]`.
	- For each `RgbComponent`:
		- If spelled as a percentage, it MUST be in `[0%,100%]` and is interpreted by dividing by 100.
		- If spelled as a number, it MUST be in `[0,255]` and is interpreted by dividing by 255.

- `$HslColor`: tools MUST parse `hsl(...)`/`hsla(...)` — a hue, two percentages, and an optional alpha, in modern or legacy syntax — and compile a semantic HSL value `(h,s,l,alpha)` where:
	- `h` is degrees and satisfies the Hue rule above.
	- `s` and `l` are percentages in `[0%,100%]` interpreted as fractions in `[0,1]`.

- `$HwbColor`: tools MUST parse `hwb(...)` — a hue, two percentages, and an optional alpha, in modern syntax — and compile a semantic HWB value `(h,w,b,alpha)` where:
	- `h` is degrees and satisfies the Hue rule above.
	- `w` and `b` are percentages in `[0%,100%]` interpreted as fractions in `[0,1]`.
	- Additionally, `w + b` MUST satisfy `<= 1`.

- `$LabColor`: tools MUST parse `lab(...)` — a percentage, two numbers, and an optional alpha, in modern syntax — and compile a semantic Lab value `(L,a,b,alpha)` where:
	- `L` is a percentage in `[0%,100%]` interpreted as `L` in `[0,100]`.
	- `a` and `b` are finite real numbers.
	- The value MUST additionally satisfy the deterministic conversion validity rule in §5.7.3.

- `$LchColor`: tools MUST parse `lch(...)` — a percentage, two numbers, and an optional alpha, in modern syntax — and compile a semantic LCH value `(L,C,h,alpha)` where:
	- `L` is a percentage in `[0%,100%]` interpreted as `L` in `[0,100]`.
	- `C` MUST be finite and MUST satisfy `C >= 0`.
	- `h` satisfies the Hue rule above.
	- The value MUST additionally satisfy the deterministic conversion validity rule in §5.7.3.

- `$OklabColor`: tools MUST parse `oklab(...)` — three numbers and an optional alpha, in modern syntax — and compile a semantic OKLab value `(L,a,b,alpha)` where:
	- `L` MUST be in `[0,1]`.
	- `a` and `b` are finite real numbers.
	- The value MUST additionally satisfy the deterministic conversion validity rule in §5.7.3.

- `$OklchColor`: tools MUST parse `oklch(...)` — three numbers and an optional alpha, in modern syntax — and compile a semantic OKLCH value `(L,C,h,alpha)` where:
	- `L` MUST be in `[0,1]`.
	- `C` MUST be finite and MUST satisfy `C >= 0`.
	- `h` satisfies the Hue rule above.
	- The value MUST additionally satisfy the deterministic conversion validity rule in §5.7.3.


- `$ColorSpaceColor`: tools MUST parse `color(...)` — a `ColorSpace` token followed by three numeric components and an optional alpha, in modern syntax — and compile a semantic color-space value `(space, c1, c2, c3, alpha)` where:
	- `space` is the `ColorSpace` token.
	- For RGB color spaces (`srgb`, `srgb-linear`, `display-p3`, `a98-rgb`, `prophoto-rgb`, `rec2020`), each component is a percentage or a number.
	- For XYZ color spaces (`xyz`, `xyz-d50`, `xyz-d65`), each component is a number.

- `$DeviceCmyk`: tools MUST parse `device-cmyk(...)` — four CMYK components (each a percentage or number) and an optional alpha, in modern syntax — and compile a semantic device-CMYK value `(c,m,y,k,alpha)` where each of `c,m,y,k,alpha` is in `[0,1]`.
	- If a CMYK component is spelled as a percentage, it MUST be in `[0%,100%]` and is interpreted as a fraction in `[0,1]`.
	- If a CMYK component is spelled as a number, it MUST be in `[0,1]`.

- `$ColorMix`: tools MUST parse `color-mix(...)` per the argument spelling rules above and compile a semantic color-mix value `(space, stops)`.
	- `space` is the `ColorSpace` token.
	- `stops` is an ordered list of at least two stops.
	- Each stop is `(color, weight?)` where `weight`, if present, is a percentage in `[0%,100%]`.
	- The nested `color` value in each stop MUST be semantically valid as `$Color`.
	- When a schema expects `$Color` and the spelling is `color-mix(...)`, tools MUST additionally evaluate the mix deterministically as specified by §5.7.7.


- `$ColorSpaceColorFunction`: tools MUST accept any function-based Color Value spelling and compile the corresponding semantic function-domain value (including `rgb(...)`, `hsl(...)`, `hwb(...)`, `lab(...)`, `lch(...)`, `oklab(...)`, `oklch(...)`, `color(...)`, `color-mix(...)`, relative-color forms, and `device-cmyk(...)`).
	- If the spelling is a relative color form, tools MUST interpret `from <color>` deterministically as specified by §5.7.8.
	- If the spelling is `color-mix(...)`, tools MUST interpret the stop list deterministically as specified by §5.7.7.

- `$Color`: tools MUST accept any Color Value spelling and compile a semantic color value as follows.
	- For `device-cmyk(...)`, the semantic value is the device-CMYK domain value `(c,m,y,k,alpha)`.
	- For all other Color Value spellings, the semantic value is the `XYZ_D65` interchange form `(X,Y,Z,alpha)` computed deterministically by §5.7.5.

If a schema expects a specific built-in color ValueType token and the Trait value uses a different Color Value form, schema validation MUST fail with a `SchemaError` (§14).

#### 5.7.5 Deterministic Conversions for `color(...)` Spaces (`XYZ_D65` Interchange)

This subsection defines a single deterministic conversion graph for all `ColorSpace` tokens used by `color(...)`, `color-mix(...)`, and `color(from <color> ...)`.

The mandated interchange form for convertible colors is `XYZ_D65` with alpha.

- `XYZ_D65` is a triple `(X,Y,Z)` using the D65 reference white and the scaling convention `Y=1` for the reference white.
- `alpha` is a fraction in `[0,1]`.

All arithmetic required by this subsection MUST use the deterministic numeric model of §5.7.3.

All matrix-vector multiplications required by §5.7.5–§5.7.8 MUST use the single mandated dot-product procedure defined by §5.7.3.

The non-finite rejection and no-clamp/no-wrap/no-gamut-mapping rules of §5.7.3 apply to all conversions in this subsection.

##### 5.7.5.1 Transfer Functions

For RGB spaces that use a transfer function, each channel value is represented as an encoded fraction in `[0,1]`.

Define the sRGB transfer functions (used by `srgb` and `display-p3`) as:

- `srgb_decode(v)` (encoded → linear):
	- Require `0 <= v <= 1`.
	- If `v <= 0.04045`, return `v / 12.92`.
	- Otherwise return `((v + 0.055) / 1.055) ^ 2.4`.

- `srgb_encode(L)` (linear → encoded):
	- Require `0 <= L <= 1`.
	- If `L <= 0.0031308`, return `12.92 * L`.
	- Otherwise return `1.055 * (L ^ (1/2.4)) - 0.055`.

Define the Adobe RGB (1998) transfer functions (used by `a98-rgb`) as:

- `a98_decode(v)` (encoded → linear): Require `0 <= v <= 1`; return `v ^ (563/256)`.
- `a98_encode(L)` (linear → encoded): Require `0 <= L <= 1`; return `L ^ (256/563)`.

Define the ProPhoto RGB transfer functions (used by `prophoto-rgb`) as:

- `prophoto_decode(v)` (encoded → linear):
	- Require `0 <= v <= 1`.
	- If `v < 16/512`, return `v / 16`.
	- Otherwise return `v ^ 1.8`.

- `prophoto_encode(L)` (linear → encoded):
	- Require `0 <= L <= 1`.
	- If `L < 1/512`, return `16 * L`.
	- Otherwise return `L ^ (1/1.8)`.

Define the Rec. 2020 transfer functions (used by `rec2020`) as:

- `rec2020_decode(v)` (encoded → linear):
	- Require `0 <= v <= 1`.
	- If `v < 0.08145`, return `v / 4.5`.
	- Otherwise return `((v + 0.0993) / 1.0993) ^ (1/0.45)`.

- `rec2020_encode(L)` (linear → encoded):
	- Require `0 <= L <= 1`.
	- If `L < 0.0181`, return `4.5 * L`.
	- Otherwise return `1.0993 * (L ^ 0.45) - 0.0993`.

##### 5.7.5.2 Matrices and Chromatic Adaptation

Define the linear sRGB (D65) matrix (linear sRGB → `XYZ_D65`):

```text
M_lin_sRGB_to_XYZ_D65 =
[ 0.41239079926595934  0.35758433938387796  0.18048078840183430 ]
[ 0.21263900587151027  0.71516867876775593  0.07219231536073371 ]
[ 0.01933081871559182  0.11919477979462598  0.95053215224966069 ]
```

Define the inverse matrix (`XYZ_D65` → linear sRGB): this is `M_XYZ_to_lin_sRGB` as defined in §5.7.3.

Define the Display P3 (D65) matrices:

```text
M_lin_display_p3_to_XYZ_D65 =
[ 0.48657094864821620  0.26566769316909306  0.19821728523436250 ]
[ 0.22897456406974880  0.69173852183650640  0.07928691409374500 ]
[ 0.00000000000000000  0.04511338185890264  1.04394436890097600 ]

M_XYZ_D65_to_lin_display_p3 =
[ 2.49349691194142500 -0.93138361791912390 -0.40271078445071684 ]
[-0.82948896956157470  1.76266406031834630  0.02362468584194358 ]
[ 0.03584583024378447 -0.07617238926804182  0.95688452400768720 ]
```

Define the Adobe RGB (1998) (D65) matrices:

```text
M_lin_a98_rgb_to_XYZ_D65 =
[ 0.57673090000000000  0.18555400000000000  0.18818520000000000 ]
[ 0.29737690000000000  0.62734910000000000  0.07527410000000000 ]
[ 0.02703430000000000  0.07068720000000000  0.99110850000000000 ]

M_XYZ_D65_to_lin_a98_rgb =
[ 2.04136900000000000 -0.56494640000000000 -0.34469440000000000 ]
[-0.96926600000000000  1.87601080000000000  0.04155600000000000 ]
[ 0.01344740000000000 -0.11838970000000000  1.01540960000000000 ]
```

Define the ProPhoto RGB matrices relative to `XYZ_D50`:

```text
M_lin_prophoto_rgb_to_XYZ_D50 =
[ 0.79767490000000000  0.13519170000000000  0.03135340000000000 ]
[ 0.28804020000000000  0.71187410000000000  0.00008570000000000 ]
[ 0.00000000000000000  0.00000000000000000  0.82521000000000000 ]

M_XYZ_D50_to_lin_prophoto_rgb =
[ 1.34594330000000000 -0.25560750000000000 -0.05111180000000000 ]
[-0.54459890000000000  1.50816730000000000  0.02053510000000000 ]
[ 0.00000000000000000  0.00000000000000000  1.21181280000000000 ]
```

Define the Rec. 2020 (D65) matrices:

```text
M_lin_rec2020_to_XYZ_D65 =
[ 0.63695804830129140  0.14461690358620832  0.16888097516417210 ]
[ 0.26270021201126710  0.67799807151887080  0.05930171646986196 ]
[ 0.00000000000000000  0.02807269304908743  1.06098505771079100 ]

M_XYZ_D65_to_lin_rec2020 =
[ 1.71665118797126800 -0.35567078377639200 -0.25336628137366000 ]
[-0.66668435183248900  1.61648123663493900  0.01576854581391110 ]
[ 0.01763985744531100 -0.04277061325780800  0.94210312123547400 ]
```

Define the Bradford chromatic adaptation matrix (D50 → D65) as `M_D50_to_D65` from §5.7.3.

Define the inverse adaptation matrix (D65 → D50):

```text
M_D65_to_D50 =
[ 1.04792982084054880  0.02294679334101909 -0.05019222954313557 ]
[ 0.02962781568815934  0.99043448457324900 -0.01707382502938514 ]
[-0.00924305815259118  0.01505514489657790  0.75187428995800080 ]
```

##### 5.7.5.3 Converting Between a `ColorSpace` and `XYZ_D65`

For a `ColorSpace` token `S` and components `(c1,c2,c3,alpha)`:

- If `S` is `xyz`, interpret it as `xyz-d65`.

To convert `color(S ...)` to `XYZ_D65`:

- For `srgb`:
	- Interpret `(c1,c2,c3)` as encoded sRGB fractions.
	- Compute linear channels `(r,g,b) = (srgb_decode(c1), srgb_decode(c2), srgb_decode(c3))`.
	- Compute `XYZ_D65 = M_lin_sRGB_to_XYZ_D65 * (r,g,b)`.

- For `srgb-linear`:
	- Interpret `(c1,c2,c3)` as linear sRGB fractions.
	- Compute `XYZ_D65 = M_lin_sRGB_to_XYZ_D65 * (c1,c2,c3)`.

- For `display-p3`:
	- Interpret `(c1,c2,c3)` as encoded Display P3 fractions.
	- Compute linear channels `(r,g,b) = (srgb_decode(c1), srgb_decode(c2), srgb_decode(c3))`.
	- Compute `XYZ_D65 = M_lin_display_p3_to_XYZ_D65 * (r,g,b)`.

- For `a98-rgb`:
	- Interpret `(c1,c2,c3)` as encoded Adobe RGB fractions.
	- Compute linear channels `(r,g,b) = (a98_decode(c1), a98_decode(c2), a98_decode(c3))`.
	- Compute `XYZ_D65 = M_lin_a98_rgb_to_XYZ_D65 * (r,g,b)`.

- For `prophoto-rgb`:
	- Interpret `(c1,c2,c3)` as encoded ProPhoto fractions.
	- Compute linear channels `(r,g,b) = (prophoto_decode(c1), prophoto_decode(c2), prophoto_decode(c3))`.
	- Compute `XYZ_D50 = M_lin_prophoto_rgb_to_XYZ_D50 * (r,g,b)`.
	- Compute `XYZ_D65 = M_D50_to_D65 * XYZ_D50`.

- For `rec2020`:
	- Interpret `(c1,c2,c3)` as encoded Rec. 2020 fractions.
	- Compute linear channels `(r,g,b) = (rec2020_decode(c1), rec2020_decode(c2), rec2020_decode(c3))`.
	- Compute `XYZ_D65 = M_lin_rec2020_to_XYZ_D65 * (r,g,b)`.

- For `xyz-d65`:
	- Interpret `(c1,c2,c3)` as `XYZ_D65 = (c1,c2,c3)`.

- For `xyz-d50`:
	- Interpret `(c1,c2,c3)` as `XYZ_D50 = (c1,c2,c3)`.
	- Compute `XYZ_D65 = M_D50_to_D65 * XYZ_D50`.

To convert from `XYZ_D65` to a `ColorSpace` token `S` (used by relative colors and by `color-mix(in S, ...)`):

- For `srgb`:
	- Compute `(r,g,b) = M_XYZ_to_lin_sRGB * XYZ_D65`.
	- Require each of `r,g,b` to be in `[0,1]`.
	- Return encoded channels `(srgb_encode(r), srgb_encode(g), srgb_encode(b))`.

- For `srgb-linear`:
	- Compute `(r,g,b) = M_XYZ_to_lin_sRGB * XYZ_D65`.
	- Require each of `r,g,b` to be in `[0,1]`.
	- Return `(r,g,b)`.

- For `display-p3`:
	- Compute `(r,g,b) = M_XYZ_D65_to_lin_display_p3 * XYZ_D65`.
	- Require each of `r,g,b` to be in `[0,1]`.
	- Return encoded channels `(srgb_encode(r), srgb_encode(g), srgb_encode(b))`.

- For `a98-rgb`:
	- Compute `(r,g,b) = M_XYZ_D65_to_lin_a98_rgb * XYZ_D65`.
	- Require each of `r,g,b` to be in `[0,1]`.
	- Return encoded channels `(a98_encode(r), a98_encode(g), a98_encode(b))`.

- For `prophoto-rgb`:
	- Compute `XYZ_D50 = M_D65_to_D50 * XYZ_D65`.
	- Compute `(r,g,b) = M_XYZ_D50_to_lin_prophoto_rgb * XYZ_D50`.
	- Require each of `r,g,b` to be in `[0,1]`.
	- Return encoded channels `(prophoto_encode(r), prophoto_encode(g), prophoto_encode(b))`.

- For `rec2020`:
	- Compute `(r,g,b) = M_XYZ_D65_to_lin_rec2020 * XYZ_D65`.
	- Require each of `r,g,b` to be in `[0,1]`.
	- Return encoded channels `(rec2020_encode(r), rec2020_encode(g), rec2020_encode(b))`.

- For `xyz` and `xyz-d65`:
	- Return `(X,Y,Z) = XYZ_D65`.

- For `xyz-d50`:
	- Return `XYZ_D50 = M_D65_to_D50 * XYZ_D65`.

##### 5.7.5.4 Converting Any Convertible Color Value to `XYZ_D65`

This subsection defines the conversion to interchange for all Color Value spellings except `device-cmyk(...)`.

The non-finite rejection rule of §5.7.3 applies to all conversions in this subsection.

**Hexadecimal and Named colors**

- For a Hex Color spelling, decode the bytes as specified by §5.7.4 (`#RGB`, `#RGBA`, `#RRGGBB`, `#RRGGBBAA`).
	- Let encoded sRGB channels be `r = R/255`, `g = G/255`, `b = B/255`.
	- Let alpha be `alpha = A/255` (with `A=255` when alpha is absent).
	- Compute `XYZ_D65` from encoded sRGB using the `srgb` conversion in §5.7.5.3.

- For a Named Color spelling `&name`, obtain its hex value from Appendix B and interpret it exactly as if that hex spelling had appeared.

**`rgb(...)` / `rgba(...)`**

- Interpret each `RgbComponent` as specified by §5.7.4 for `$RgbColor`.
	- Percent form yields an encoded fraction in `[0,1]` by dividing by 100.
	- Number form yields an encoded fraction in `[0,1]` by dividing by 255.
- Interpret alpha per §5.7.4.
- Compute `XYZ_D65` from encoded sRGB using the `srgb` conversion in §5.7.5.3.

**`hsl(...)` / `hsla(...)`**

- Interpret `h` (degrees), `s` (fraction), `l` (fraction), and alpha per §5.7.4.
- Convert HSL to encoded sRGB as follows.

Let `h` be degrees satisfying the Hue rule of §5.7.4. Let `s` and `l` be fractions in `[0,1]`.

1. Compute `c = (1 - abs(2*l - 1)) * s`.
2. Compute `h' = h / 60`.
3. Compute the remainder of `h'` modulo 2 without using a `mod` operator:
	- If `0 <= h' < 2`, let `h2 = h'`.
	- If `2 <= h' < 4`, let `h2 = h' - 2`.
	- If `4 <= h' < 6`, let `h2 = h' - 4`.
4. Compute `x = c * (1 - abs(h2 - 1))`.

5. Determine `(r1,g1,b1)` by the interval containing `h'`:
	- If `0 <= h' < 1`: `(c, x, 0)`
	- If `1 <= h' < 2`: `(x, c, 0)`
	- If `2 <= h' < 3`: `(0, c, x)`
	- If `3 <= h' < 4`: `(0, x, c)`
	- If `4 <= h' < 5`: `(x, 0, c)`
	- If `5 <= h' < 6`: `(c, 0, x)`

6. Compute `m = l - c/2`.
7. The encoded sRGB channels are `(r,g,b) = (r1+m, g1+m, b1+m)`.
- Require each of `r,g,b` to be in `[0,1]` (reject-only semantics).
- Compute `XYZ_D65` from encoded sRGB using the `srgb` conversion in §5.7.5.3.

**`hwb(...)`**

- Interpret `h` (degrees), `w` (fraction), `b` (fraction), and alpha per §5.7.4.
- The `w + b <= 1` constraint from §5.7.4 applies.

To convert HWB to encoded sRGB:

1. Compute the base pure hue color as encoded sRGB with saturation 1 and lightness 0.5: let `(rh,gh,bh)` be the result of converting `hsl(h, 100%, 50%)` using the HSL algorithm above.
2. Compute the scale factor `t = 1 - w - b`.
3. The encoded sRGB channels are `(r,g,b) = (rh*t + w, gh*t + w, bh*t + w)`.
- Require each of `r,g,b` to be in `[0,1]`.
- Compute `XYZ_D65` from encoded sRGB using the `srgb` conversion in §5.7.5.3.

**`lab(...)` / `lch(...)` / `oklab(...)` / `oklch(...)`**

- For `lab(...)` and `lch(...)`, compute `XYZ_D65` by applying steps (1)–(3) of §5.7.3.
- For `oklab(...)` and `oklch(...)`, compute `XYZ_D65` by applying step (4) of §5.7.3.

##### 5.7.5.5 Inverse Conversions Needed by Relative Colors

Relative color forms require extracting base-channel values from a base interchange color.

**Encoded sRGB → HSL/HWB**

Given encoded sRGB `(r,g,b)` in `[0,1]`:

1. Let `max = max(r,g,b)`, `min = min(r,g,b)`, `delta = max - min`.
2. Compute lightness fraction `l = (max + min) / 2`.
3. If `delta = 0`, set hue degrees `h = 0` and saturation fraction `s = 0`.
4. Otherwise:
	- Compute saturation fraction `s = delta / (1 - abs(2*l - 1))`.
	- Compute hue fraction `h6` as:
		- If `max = r`: `h6 = ((g - b) / delta)`.
		- If `max = g`: `h6 = ((b - r) / delta) + 2`.
		- If `max = b`: `h6 = ((r - g) / delta) + 4`.
	- Compute hue degrees `h = 60 * h6`.
	- If `h < 0`, set `h = h + 360`.
	- If `h = 360`, set `h = 0`.

The base HSL channel tokens used by relative colors are:

- `h` is degrees `h`.
- `s` is percentage `100*s`.
- `l` is percentage `100*l`.

The base HWB channel tokens used by relative colors are:

- `h` is the same degrees `h`.
- `w` is percentage `100 * min`.
- `b` is percentage `100 * (1 - max)`.

**`XYZ_D50` → Lab (D50)**

Let D50 white be `(X_n, Y_n, Z_n)` as defined in §5.7.3. Given `XYZ_D50 = (X,Y,Z)`:

1. Compute `x = X / X_n`, `y = Y / Y_n`, `z = Z / Z_n`.
2. Define the helper `f(t)`:
	- If `t > ε`, return `t ^ (1/3)`.
	- Otherwise return `(κ*t + 16) / 116`.
3. Compute `fx = f(x)`, `fy = f(y)`, `fz = f(z)`.
4. Compute Lab:
	- `L = 116*fy - 16`
	- `a = 500*(fx - fy)`
	- `b = 200*(fy - fz)`

Relative channel tokens use:

- `l` as the percentage `L` (in `[0,100]`).
- `a` and `b` as the Lab components.
- `c = sqrt(a^2 + b^2)`.
- `h` as degrees computed from `atan2(b,a)` as follows:
	- Compute `theta = atan2(b,a)` in radians.
	- Compute `h = theta * (180/π)`.
	- If `h < 0`, set `h = h + 360`.
	- If `h = 360`, set `h = 0`.

**`XYZ_D65` → OKLab (D65)**

Given `XYZ_D65 = (X,Y,Z)`, compute OKLab as follows.

Define:

```text
M_XYZ_D65_to_LMS =
[ 0.8189330101  0.3618667424 -0.1288597137 ]
[ 0.0329845436  0.9293118715  0.0361456387 ]
[ 0.0482003018  0.2643662691  0.6338517070 ]

M_LMS_to_OKLab =
[ 0.2104542553  0.7936177850 -0.0040720468 ]
[ 1.9779984951 -2.4285922050  0.4505937099 ]
[ 0.0259040371  0.7827717662 -0.8086757660 ]
```

1. Compute `(l',m',s') = M_XYZ_D65_to_LMS * (X,Y,Z)`.
2. Compute `(l,m,s) = (cbrt(l'), cbrt(m'), cbrt(s'))`.
3. Compute `(L,a,b) = M_LMS_to_OKLab * (l,m,s)`.

Relative channel tokens use:

- `l` as `L` (in `[0,1]`).
- `a` and `b` as the OKLab components.
- `c = sqrt(a^2 + b^2)`.
- `h` as degrees computed from `atan2(b,a)` using the same rule as Lab above.

#### 5.7.6 Semantic Interpretation of `color(...)`

When a schema expects a `color(...)` spelling as `$Color` or `$ColorSpaceColorFunction`, tools MUST interpret the components and alpha as follows.

For `color(S c1 c2 c3 / alpha?)` where `S` is an RGB `ColorSpace` (`srgb`, `srgb-linear`, `display-p3`, `a98-rgb`, `prophoto-rgb`, `rec2020`):

- If a component is spelled as a percentage, it MUST be in `[0%,100%]` and is interpreted by dividing by 100.
- If a component is spelled as a number, it MUST be in `[0,1]` and is interpreted as-is.

For `color(S x y z / alpha?)` where `S` is an XYZ `ColorSpace` (`xyz`, `xyz-d50`, `xyz-d65`):

- Each of `x`, `y`, and `z` MUST be finite and MUST satisfy `>= 0`.

Alpha is interpreted per §5.7.4 (percentage in `[0%,100%]` or number in `[0,1]`; default `alpha=1`).

#### 5.7.7 Deterministic Semantic Evaluation of `color-mix(...)`

When a schema expects `$Color` and the Trait value is `color-mix(in S, stop1, stop2, ...)`, tools MUST evaluate the mix deterministically.

1. Let `S` be the interpolation `ColorSpace` token.
2. Each stop MUST be `(color, weight?)` where `color` is a Color Value.
	- At least two stops are required.
	- If no stop provides a weight, each stop has equal weight.
	- If any stop provides a weight, then every stop MUST provide a weight; otherwise it is a `SchemaError`.
	- Each provided weight MUST be in `[0%,100%]`.
3. Evaluate each stop color as `$Color`.
	- If the stop is `device-cmyk(...)`, evaluation fails with `SchemaError` (device-CMYK is not convertible for mixing).
	- Otherwise, obtain its interchange value `(XYZ_D65, alpha)`.
4. Convert each stop to interpolation space `S` using §5.7.5.3:
	- If `S` is an RGB space, convert `XYZ_D65` to the *linear* channels for `S` and require each linear channel in `[0,1]`.
	- If `S` is `xyz`/`xyz-d65`, use `XYZ_D65`.
	- If `S` is `xyz-d50`, use `XYZ_D50 = M_D65_to_D50 * XYZ_D65`.
5. Interpolate using premultiplied alpha in the interpolation space:
	- Let each stop have components vector `v_i` (either linear RGB or XYZ) and alpha `a_i`.
	- Let weights be normalized to fractions `w_i` summing to 1.
	- Compute `a_out = sum_i (w_i * a_i)`.
	- Compute `v_out_premul = sum_i (w_i * v_i * a_i)`.
	- If `a_out = 0`, set `v_out` to the zero vector.
	- Otherwise set `v_out = v_out_premul / a_out`.
6. Convert the mixed result back to interchange `XYZ_D65`:
	- If `S` is `xyz`/`xyz-d65`, the mixed XYZ is already `XYZ_D65`.
	- If `S` is `xyz-d50`, compute `XYZ_D65 = M_D50_to_D65 * XYZ_D50`.
	- If `S` is an RGB space, treat `v_out` as *linear* channels for `S` and compute `XYZ_D65` as follows:
		- For `srgb` or `srgb-linear`: `XYZ_D65 = M_lin_sRGB_to_XYZ_D65 * v_out`.
		- For `display-p3`: `XYZ_D65 = M_lin_display_p3_to_XYZ_D65 * v_out`.
		- For `a98-rgb`: `XYZ_D65 = M_lin_a98_rgb_to_XYZ_D65 * v_out`.
		- For `rec2020`: `XYZ_D65 = M_lin_rec2020_to_XYZ_D65 * v_out`.
		- For `prophoto-rgb`: compute `XYZ_D50 = M_lin_prophoto_rgb_to_XYZ_D50 * v_out`, then `XYZ_D65 = M_D50_to_D65 * XYZ_D50`.
7. The semantic `$Color` value is `(XYZ_D65, a_out)`.

#### 5.7.8 Deterministic Semantic Evaluation of Relative Colors (`from <color>`)

When a schema expects `$Color` or `$ColorSpaceColorFunction` and the Trait value is a relative color form, tools MUST evaluate `from <color>` deterministically as follows.

Common requirements:

1. Evaluate the base Color Value after `from` as `$Color`.
	- If the base is `device-cmyk(...)`, evaluation fails with `SchemaError` (device-CMYK is not convertible for relative colors).
	- Otherwise, obtain base interchange `(XYZ_D65_base, alpha_base)`.
2. Convert the base interchange value to the function's source domain:
	- For `rgb(from ...)`, convert `XYZ_D65_base` to `srgb` encoded channels `(r,g,b)` using §5.7.5.3.
	- For `hsl(from ...)` and `hwb(from ...)`, convert `XYZ_D65_base` to `srgb` encoded channels and then compute base HSL/HWB using §5.7.5.5.
	- For `lab(from ...)` and `lch(from ...)`, convert `XYZ_D65_base` to `xyz-d50`, then compute base Lab (D50) using §5.7.5.5.
	- For `oklab(from ...)` and `oklch(from ...)`, compute base OKLab (D65) using §5.7.5.5.
	- For `color(from ... S ...)`, convert `XYZ_D65_base` to `S` using §5.7.5.3.
3. For each component position in the relative argument list:
	- If it is a literal numeric/percentage component, interpret it as if it appeared in the corresponding non-relative function form.
	- If it is a channel token (such as `r`, `g`, `b`, `x`, `y`, `z`, `l`, `a`, `c`, `h`, or `a` for alpha), substitute the base channel value in the same unit system defined below.
4. Interpret alpha:
	- If alpha is omitted, use `alpha_base`.
	- If alpha is spelled as `a`, use `alpha_base`.
	- If alpha is spelled as a literal, interpret it per the Alpha rule in §5.7.4.
5. After substitution, the resulting non-relative color spelling MUST satisfy the semantic rules for that function/value type (including hue and range rules). Otherwise it is a `SchemaError`.

Units for channel substitution:

- `rgb(from ...)` / `rgba(from ...)`:
	- Base `r`, `g`, `b` channel tokens substitute the base sRGB encoded channel in the number-form unit: `255 * channel`.

- `hsl(from ...)` / `hsla(from ...)` and `hwb(from ...)`:
	- Base hue token `h` substitutes the base hue in degrees in `[0,360)`.
	- Base `s`, `l`, `w`, `b` tokens substitute the base percentage in `[0,100]` (not the fraction).

- `lab(from ...)` / `lch(from ...)`:
	- Base `l` substitutes the base Lab `L` in the percent unit (a number in `[0,100]`).
	- Base `a` and `b` substitute the base Lab `a`/`b` components.
	- Base `c` substitutes chroma `C = sqrt(a^2 + b^2)`.
	- Base `h` substitutes hue degrees computed from `atan2(b,a)` using the rule in §5.7.5.5.

- `oklab(from ...)` / `oklch(from ...)`:
	- Base `l` substitutes the base OKLab `L` component in `[0,1]`.
	- Base `a` and `b` substitute the base OKLab `a`/`b` components.
	- Base `c` substitutes chroma `C = sqrt(a^2 + b^2)`.
	- Base `h` substitutes hue degrees computed from `atan2(b,a)` using the rule in §5.7.5.5.

- `color(from ... S ...)`:
	- If `S` is an RGB space, base `r`, `g`, `b` substitute the encoded channel fractions in `[0,1]`.
	- If `S` is an XYZ space, base `x`, `y`, `z` substitute the XYZ components.

### 5.8 UUID Values

A UUID Value is a 36-character unquoted token with the form:

`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

where each `x` is a hexadecimal digit.

A UUID Value MUST NOT be a Text Value.

A UUID Value MUST NOT include braces, prefixes, or other delimiters.

Hyphens MUST appear at character positions 9, 14, 19, and 24 (1-indexed).

Hexadecimal digits in UUID Values are case-insensitive for parsing. In canonical surface form, UUID Values MUST be spelled using lowercase hexadecimal digits.

No UUID version is mandated.

### 5.9 IRI Reference Values

An IRI Reference Value is an unquoted token representing identity or reference.

An IRI Reference Value MUST contain a `:` character separating the scheme from the remainder.

In the Surface Form, IRI Reference Values MUST be spelled using the IRI reference grammar defined by this specification.

IRI Reference Values MUST permit non-ASCII Unicode characters directly and MUST permit percent-encoding, as defined for IRI-references by RFC 3987: https://www.rfc-editor.org/rfc/rfc3987.

For all Unicode character classifications referenced by this section (whitespace, control, bidirectional control, and private-use), tools MUST use the Unicode 16.0.0 character property tables.

IRI Reference Values MUST NOT contain Unicode whitespace characters.

IRI Reference Values MUST NOT contain Unicode control characters.

IRI Reference Values MUST NOT contain Unicode bidirectional control characters.

IRI Reference Values MUST NOT contain Unicode private-use characters.

An IRI Reference Value MUST NOT end with a `:` character.

An IRI Reference Value MUST NOT be a Text Value.

IRI Reference Values MUST be compared as opaque sequences of Unicode scalar values (Unicode 16.0.0).

Codex-conforming tools MUST NOT dereference IRI Reference Values.

Where this specification defines deterministic resolution (for example, lookup-token resolution and reference-constraint resolution), tools MUST apply only the mechanisms defined by this specification and MUST NOT perform any external lookup, registry query, or network dereferencing.

### 5.10 Lookup Token Values

A Lookup Token Value is a document-scoped symbolic reference that identifies a Concept by its `key` trait (§6.3).

In the Surface Form, Lookup Token Values MUST be spelled as `~` followed immediately by a token name.

The token name MUST use camelCase.

A Lookup Token Value MUST NOT be a Text Value.

Codex-conforming tools MUST NOT dereference Lookup Token Values.

### 5.11 Character Values

A Character Value represents exactly one Unicode scalar value.

In the Surface Form, Character Values MUST be spelled as character literals delimited by single quotes (`'...'`). A character literal MUST NOT contain raw newlines (U+000A). Within the quotes, any Unicode scalar value other than `'` (U+0027), `\` (U+005C), or newline (U+000A) may appear literally. The `\` character introduces an escape sequence. The permitted escape sequences are:

- `\'` — literal single quote
- `\\` — literal backslash
- `\n` — newline (U+000A)
- `\r` — carriage return (U+000D)
- `\t` — tab (U+0009)
- `\uXXXX` — Unicode scalar value specified by exactly four hexadecimal digits
- `\u{X...}` — Unicode scalar value specified by one or more hexadecimal digits enclosed in braces

Hexadecimal digits in escape sequences are case-insensitive for parsing. A Unicode escape MUST identify a Unicode scalar value (U+0000 to U+D7FF or U+E000 to U+10FFFF).

A Character Value MUST NOT be a Text Value.

After interpreting the character literal's escape sequences, the resulting Character Value MUST contain exactly one Unicode scalar value.

### 5.12 List Values

A List Value is an ordered sequence of zero or more Value elements.

In the Surface Form, a List Value is delimited by square brackets (`[...]`). Elements are separated by commas, with optional whitespace (including newlines) permitted between brackets, around commas, and between elements.

Each element of a List Value MUST be a Value.

A List Value MUST permit nesting.

A List Value MUST NOT require all elements to have the same Value kind.

A List Value MUST represent exactly the elements explicitly present in its literal spelling.

For schema-level type constraints on list contents, see §5.18.

### 5.13 Value Equality for Collection Uniqueness
For purposes of detecting duplicates in Set Values, Map Values, and Record Values, Codex-conforming tools MUST use the following Value equality relation.

Equality is defined over parsed Values (after interpreting escape sequences, Text whitespace normalization, and other value-specific decoding rules) and MUST NOT be defined over raw source bytes.

Two Values are equal if and only if they have the same Value kind and satisfy the following rules (recursively where applicable):

- Text Values: equal if and only if they contain the same sequence of Unicode scalar values.
- Boolean Values: equal if and only if both are `true` or both are `false`.
- Numeric Values: equal if and only if their literal spellings are identical codepoint-for-codepoint.
- Enumerated Token Values: equal if and only if their literal spellings are identical codepoint-for-codepoint.
- Temporal Values: equal if and only if their literal spellings are identical codepoint-for-codepoint.
- Color Values: equal if and only if their literal spellings are identical, except that hexadecimal digits, color function names, and color space tokens are compared case-insensitively.
- UUID Values: equal if and only if they are identical after case-folding hexadecimal digits (i.e., hexadecimal digits are compared case-insensitively).
- IRI Reference Values: equal if and only if their spellings are identical codepoint-for-codepoint (see §5.9).
- Host Name Values: equal if and only if their canonical hostnames are identical codepoint-for-codepoint.
- Email Address Values: equal if and only if their canonical email addresses are identical codepoint-for-codepoint.
- URL Values: equal if and only if their canonical URL strings are identical codepoint-for-codepoint.
- Lookup Token Values: equal if and only if their literal spellings are identical codepoint-for-codepoint.
- Character Values: equal if and only if they contain the same Unicode scalar value.
- List Values and Tuple Values: equal if and only if they have the same length and corresponding elements are equal.
- Range Values: equal if and only if their start endpoints are equal, their end endpoints are equal, and either both omit a step or both include equal step Values.
- Set Values: equal if and only if they contain the same elements (under this equality relation), regardless of element order.
- Map Values: equal if and only if they contain the same bindings, where keys are equal and corresponding bound Values are equal, regardless of entry order.
- Record Values: equal if and only if they contain the same bindings, where field names are equal and corresponding bound Values are equal, regardless of entry order.

### 5.14 Set Values

A Set Value is an unordered collection of zero or more Value elements. Set Values have no semantic ordering; however, in canonical surface form, elements MUST be serialized in the order they appear in the source spelling.

In the Surface Form, a Set Value is spelled as the keyword `set` followed immediately (no whitespace) by square brackets (`set[...]`). Elements are separated by commas, with optional whitespace (including newlines) permitted between brackets, around commas, and between elements.

Each element of a Set Value MUST be a Value.

A Set Value MUST permit nesting.

A Set Value MUST NOT require all elements to have the same Value kind.

A Set Value MUST contain no duplicate elements.

Duplicate elements MUST be determined using the Value equality relation in §5.13.

If a set literal spelling contains duplicate elements, Codex-conforming tools MUST reject that spelling with a `ParseError` (§14).

For schema-level type constraints on set contents, see §5.18.

### 5.15 Map Values

A Map Value is a collection of key-value pairs. Map Values have no semantic ordering; however, in canonical surface form, entries MUST be serialized in the order they appear in the source spelling.

In the Surface Form, a Map Value is spelled as the keyword `map` followed immediately (no whitespace) by square brackets (`map[...]`). Each entry is written as a key, optional whitespace, a colon (`:`), optional whitespace, and a Value. Entries are separated by commas, with optional whitespace (including newlines) permitted between brackets, around commas, and between entries.

A Map Value MUST permit zero entries.

Each entry in a Map Value MUST bind exactly one key to exactly one Value.

A Map Value MUST permit nesting.

A Map Value MUST NOT require all bound Values to have the same Value kind.

A Map Value MUST contain no duplicate keys.

Duplicate keys MUST be determined using the Value equality relation in §5.13.

If a map literal spelling contains duplicate keys, Codex-conforming tools MUST reject that spelling with a `ParseError` (§14).

For schema-level type constraints on map keys and values, see §5.18.

#### 5.15.1 Map Keys

In the Surface Form, a map key MUST be one of:

- an unquoted identifier key
- a Text Value
- a Character Value
- an Integer value
- an Enumerated Token Value
- an IRI Reference Value

An unquoted identifier key MUST use camelCase.

### 5.16 Tuple Values

A Tuple Value is an ordered sequence of one or more Value elements with positional semantics.

In the Surface Form, a Tuple Value is delimited by parentheses (`(...)`). Elements are separated by commas, with optional whitespace (including newlines) permitted between parentheses, around commas, and between elements.

A Tuple Value MUST contain at least one element.

Each element of a Tuple Value MUST be a Value.

A Tuple Value MUST permit nesting.

A Tuple Value MUST NOT require all elements to have the same Value kind.

For any Tuple Value used by a Trait, the governing schema MUST define the required arity and the meaning of each position.

For schema-level type constraints on tuple positions, see §5.18.

### 5.17 Range Values

A Range Value is a declarative interval.

In the Surface Form, a Range Value is spelled as a start endpoint, the `..` operator, and an end endpoint. An optional step is introduced by the letter `s` followed by the step value. Optional whitespace is permitted around the `..` operator and around the `s` step separator (e.g., `x..y` or `x .. y s z`).

Range endpoints and step values MUST be `$FiniteRealNumber` types (Integer, DecimalNumber, ExponentialNumber, PrecisionNumber, or Fraction), Temporal Values, or Character Values (Character Values are permitted as endpoints only, not as step values). ComplexNumber, ImaginaryNumber, and Infinity MUST NOT appear as range endpoints or step values.

A Range Value MUST contain a start endpoint and an end endpoint.

The start endpoint and end endpoint MUST be Values of the same base Value kind (e.g., both Integer, both PlainDate), independent of any parameterized type constraints.

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
* `$Record<V>` — a record where all field values conform to `V`

#### 5.18.2 Type Arguments

A type argument MUST be one of:

* A simple value type token (e.g., `$Text`)
* A parameterized value type (e.g., `$List<$Text>`)
* A type union (e.g., `[$Text, $Integer]`)

A type union is a bracketed, comma-separated list of value type tokens. A value conforms to a type union if it conforms to any member type.

When a parameterized type has multiple type arguments, the arguments MUST be separated by a comma followed by exactly one space (`, `). Within a type union, members MUST be separated by a comma followed by exactly one space (`, `).

Type arguments MUST NOT contain whitespace. No whitespace is permitted immediately after `<`, immediately before `>`, immediately after `[`, or immediately before `]`.

#### 5.18.3 Unparameterized Collection Types

An unparameterized collection type (e.g., `$List` without `<...>`) permits items of any value type.

#### 5.18.4 Nesting

There is no limit on the nesting depth of parameterized types.

For example, `$List<$List<$Text>>` specifies a list of lists of text values.

#### 5.18.5 Examples

| Type | Meaning |
|------|---------|
| `$List<$Text>` | List of text values |
| `$List<[$Text, $Boolean]>` | List where each item is a text value or boolean |
| `$Set<$Integer>` | Set of integers |
| `$Map<$Text, $List<$Integer>>` | Map from text values to lists of integers |
| `$Tuple<$Text, $Integer, $Boolean>` | 3-tuple: (text value, integer, boolean) |
| `$Range<$Integer>` | Range with integer bounds |
| `$List` | List of any values (unparameterized) |
| `$Record<$Text>` | Record where all fields have text values |

### 5.19 Record Values

A Record Value is a fixed-structure aggregate of named fields. Unlike Map Values, which permit arbitrary keys, Record Values have field names that are schema-defined identifiers.

In the Surface Form, a Record Value is spelled as the keyword `record` followed immediately (no whitespace) by square brackets (`record[...]`). Each entry is written as a field name, optional whitespace, a colon (`:`), optional whitespace, and a Value. Entries are separated by commas, with optional whitespace (including newlines) permitted between brackets, around commas, and between entries.

A Record Value MUST permit zero fields.

Each entry in a Record Value MUST bind exactly one field name to exactly one Value.

A Record Value MUST permit nesting.

A Record Value MUST NOT require all bound Values to have the same Value kind.

A Record Value MUST contain no duplicate field names.

Duplicate field names MUST be determined using the Value equality relation in §5.13.

If a record literal spelling contains duplicate field names, Codex-conforming tools MUST reject that spelling with a `ParseError` (§14).

For schema-level type constraints on record fields, see §5.18.

#### 5.19.1 Record Field Names

In the Surface Form, a record field name MUST be an unquoted identifier using camelCase.

### 5.20 Host Name Values

A Host Name Value represents a DNS hostname in **ASCII form**.

Host Name Values are defined to avoid reliance on external internationalization profiles. Implementations MUST treat Host Name Values as already being in ASCII (for example, A-label form for internationalized names).

In the Surface Form, Host Name Values MUST be spelled as the keyword `host` followed by a parenthesized Text Value. Optional whitespace is permitted after `(` and before `)`:

- `host("<hostname>")`

The keyword `host` MUST be spelled using ASCII lowercase letters.

After interpreting the Text Value's escape sequences, the decoded `hostname` text MUST NOT contain Unicode whitespace characters.

The decoded `hostname` text MUST NOT contain Unicode control characters.

The decoded `hostname` text MUST NOT contain Unicode bidirectional control characters.

The decoded `hostname` text MUST NOT contain Unicode private-use characters.

For all Unicode character classifications referenced by this section (whitespace, control, bidirectional control, and private-use), tools MUST use the Unicode 16.0.0 character property tables.

Host Name Values MUST be canonicalized as follows:

1. Require that the decoded `hostname` text contains only ASCII characters.
2. Lowercase ASCII letters (`A`–`Z`) in the decoded hostname.
3. Check the lowercase hostname for well-formedness as a DNS host name using these rules:
	- The hostname MUST NOT be empty.
	- The hostname MUST NOT start or end with `.`.
	- The hostname MUST be at most 253 characters.
	- The hostname MUST consist of one or more labels separated by `.`.
	- Each label MUST be 1–63 characters.
	- Each label MUST contain only ASCII letters `a`–`z`, digits `0`–`9`, and hyphen `-`.
	- Each label MUST NOT start with `-` and MUST NOT end with `-`.

If any step fails, Codex-conforming tools MUST reject the Host Name Value spelling with a `SchemaError` (§14).

In canonical surface form, Host Name Values MUST be spelled as `host("<hostname>")`, where `<hostname>` is the lowercase ASCII hostname produced by the canonicalization procedure above.

A Host Name Value MUST NOT be treated as a Text Value.

### 5.21 Email Address Values

An Email Address Value represents an email address with a Unicode local part and an ASCII domain.

In the Surface Form, Email Address Values MUST be spelled as the keyword `email` followed by a parenthesized Text Value. Optional whitespace is permitted after `(` and before `)`:

- `email("<address>")`

The keyword `email` MUST be spelled using ASCII lowercase letters.

After interpreting the Text Value's escape sequences, the decoded `address` text MUST contain exactly one `@` character.

Let `local` be the substring before `@` and `domain` be the substring after `@`.

The decoded `address` text MUST NOT contain Unicode whitespace characters.

The decoded `address` text MUST NOT contain Unicode control characters.

The decoded `address` text MUST NOT contain Unicode bidirectional control characters.

The decoded `address` text MUST NOT contain Unicode private-use characters.

For all Unicode character classifications referenced by this section (whitespace, control, bidirectional control, and private-use), tools MUST use the Unicode 16.0.0 character property tables.

The `local` part MUST be non-empty.

The `domain` part MUST be non-empty.

Email Address Values MUST be canonicalized as follows:

1. Apply Unicode Normalization Form C (NFC) to `local` using Unicode 16.0.0.
2. Canonicalize `domain` using the Host Name Value canonicalization procedure in §5.20.
3. Preserve the NFC-normalized `local` part codepoint-for-codepoint (no case folding).

If any step fails, Codex-conforming tools MUST reject the Email Address Value spelling with a `SchemaError` (§14).

In canonical surface form, Email Address Values MUST be spelled as `email("<local>@<ascii-domain>")`, where `<local>` is the NFC-normalized local part and `<ascii-domain>` is the canonicalized lowercase ASCII domain.

An Email Address Value MUST NOT be treated as a Text Value.

### 5.22 URL Values

A URL Value represents a **URI** in absolute form.

URL Values are defined to avoid reliance on living URL standards. This specification defines a deterministic parsing, resolution, and canonicalization procedure for a restricted, ASCII-only URI form.

In the Surface Form, URL Values MUST be spelled using one of the following two forms:

- `url("<absolute-url>")`
- `url("<base-url>", "<relative-reference>")`

The keyword `url` MUST be spelled using ASCII lowercase letters.

Both arguments MUST be Text Values. Optional whitespace is permitted after `(`, before `)`, and around the comma in the two-argument form.

For all Unicode character classifications referenced by this section (whitespace, control, bidirectional control, and private-use), tools MUST use the Unicode 16.0.0 character property tables.

After interpreting Text Value escape sequences, the decoded URL text MUST NOT contain Unicode whitespace characters, Unicode control characters, Unicode bidirectional control characters, or Unicode private-use characters.

The decoded URL text MUST contain only ASCII characters.

#### 5.22.1 URL Parsing Model

Codex URL parsing operates on an ASCII string and produces the components `(scheme, authority?, path, query?, fragment?)`.

- The `scheme` is the substring before the first `:`.
- The remainder after `:` is parsed as:
	- If it begins with `//`, it has an `authority` ending at the next `/`, `?`, or `#` (or end of string).
	- The `path` is the substring from the start of the path to before `?` or `#` (or end of string). If no path is present after an authority, the path is the empty string.
	- If a `?` is present, `query` is the substring after `?` up to before `#` (or end of string).
	- If a `#` is present, `fragment` is the substring after `#` to end of string.

Parsing requirements:

1. The decoded URL text MUST contain a `:` character.
2. The `scheme` MUST be non-empty.
3. The first character of `scheme` MUST be an ASCII letter (`A`–`Z` or `a`–`z`).
4. The remaining characters of `scheme` MUST be ASCII letters, digits, `+`, `-`, or `.`.
5. If an `authority` is present, it MUST be non-empty.

#### 5.22.2 URL Resolution (two-argument form)

For the two-argument form `url("<base-url>", "<relative-reference>")`:

1. Parse `base-url` using §5.22.1.
2. Require that `base-url` is absolute (it contains a scheme) and that it has an `authority`.
3. Resolve `relative-reference` against `base-url` using this deterministic procedure:
	- If `relative-reference` contains a `:` before any `/`, `?`, or `#`, it is treated as an absolute URL text and is parsed directly (the base is ignored).
	- Otherwise, construct a target by inheriting `scheme` and `authority` from the base and computing the target path/query/fragment:
		- If `relative-reference` starts with `//`, inherit `scheme` from base and use the `authority` and following components from `relative-reference`.
		- Else if `relative-reference` starts with `/`, use the base `scheme`/`authority` and set `path` to the relative-reference path.
		- Else, use the base `scheme`/`authority` and set `path` to the base path with its final segment removed, then append the relative-reference path.
		- If `relative-reference` includes `?`, use its `query`; otherwise inherit the base `query`.
		- If `relative-reference` includes `#`, use its `fragment`; otherwise omit `fragment`.
4. After resolution, apply dot-segment removal to the target `path` using this procedure:
	- Split the path on `/` into segments.
	- Process segments left-to-right:
		- Skip segments equal to `.`.
		- For a segment equal to `..`, remove the most recent retained non-empty segment if any; otherwise retain nothing.
		- Otherwise retain the segment.
	- Re-join with `/`, preserving a leading `/` if the input path had a leading `/`.

If parsing or resolution fails, tools MUST reject with a `SchemaError` (§14).

#### 5.22.3 URL Canonicalization

After obtaining the resolved URL components (one-argument form parses directly; two-argument form resolves then parses), tools MUST canonicalize as follows:

1. Lowercase ASCII letters in `scheme`.
2. If an `authority` is present:
	- Lowercase ASCII letters in the `authority` substring.
	- If the `path` is the empty string, replace it with `/`.
3. Apply dot-segment removal to `path` as defined in §5.22.2.
4. Serialize the canonical URL string as:
	- `scheme`, then `:`, then:
		- if `authority` is present: `//` + `authority`
		- then `path`
		- then, if `query` is present: `?` + `query`
		- then, if `fragment` is present: `#` + `fragment`

If canonicalization fails at any step, tools MUST reject with a `SchemaError` (§14).

In canonical surface form, URL Values MUST be spelled using the single-argument form `url("<canonical-url>")` where `<canonical-url>` is the canonical serialized URL string.

A URL Value MUST NOT be treated as a Text Value.

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

Every Entity MUST have exactly one `id` trait. If an Entity lacks an `id` trait, Codex-conforming tools MUST reject that document with an `IdentityError` (§14).

Every non-Entity MUST NOT have an `id` trait. If a non-Entity declares an `id` trait, Codex-conforming tools MUST reject that document with an `IdentityError` (§14).

The value of an `id` trait MUST be an IRI Reference Value (§5.9). If the value of an `id` trait is not an IRI Reference Value, Codex-conforming tools MUST reject that document with an `IdentityError` (§14).

Codex-conforming tools MUST NOT synthesize an `id` trait.

#### 6.2.2 Uniqueness

Within a single document, each `id` value MUST be unique across all Entities. If a document contains duplicate `id` values, Codex-conforming tools MUST reject that document with an `IdentityError` (§14).

Codex does not define a mechanism to enforce cross-document uniqueness; however, `id` values serve as RDF subject identifiers in triple stores and are expected to be globally unique in practice.

#### 6.2.3 Stability

Once an `id` value is assigned to an Entity, that `id` value MUST continue to refer to the same Entity.

Changing an Entity's `id` value MUST be treated as creating a new Entity.

### 6.3 Concept Keys

#### 6.3.1 The `key` Trait

A Concept MUST NOT declare more than one `key` trait (see §3 for the general duplicate trait name prohibition).

The value of a `key` trait MUST be a Lookup Token Value (§5.10). If the value of a `key` trait is not a Lookup Token Value, Codex-conforming tools MUST reject that document with an `IdentityError` (§14).

Codex-conforming tools MUST NOT synthesize a `key` trait.

#### 6.3.2 Uniqueness

Within a single document, each `key` value MUST be unique across all Concepts. If a document contains duplicate `key` values, Codex-conforming tools MUST reject that document with an `IdentityError` (§14).

Concept keys have document scope; cross-document key references are not defined by this specification.

#### 6.3.3 Resolution

When a Lookup Token Value appears as a reference trait value, the token resolves to the `id` of the Concept in the same document that declares that token as its `key` value. Full resolution semantics are defined in §9.8.

---

## 7. Reference Traits

### 7.1 Reference Traits Overview

Codex defines exactly three reference Traits:

- `reference`
- `target`
- `for`

Each reference Trait expresses a declarative relationship from a Concept instance to another Concept instance, identified by identity reference.

An identity reference is either an Entity `id` (an IRI Reference Value; §6.2) or a Concept `key` (a Lookup Token Value; §6.3) that is resolved as explicitly defined by this specification and the governing schema.

The value of each reference Trait MUST be either an IRI Reference Value (see §5.9) or a Lookup Token Value (see §5.10). The value of a reference Trait MUST NOT be any other Value kind. If the value of a reference Trait is not an IRI Reference Value or a Lookup Token Value, Codex-conforming tools MUST reject that document with a `ReferenceError` (§14).

Reference Traits MUST be interpreted only as declarative relationships.

Reference Traits MUST NOT imply dereferencing, loading, execution, or transformation.

Reference Traits MUST NOT imply any automatic or external resolution beyond what is explicitly defined by this specification or the governing schema.

A Concept instance MUST NOT declare a reference Trait unless authorized by the governing schema. If a Concept instance declares an unauthorized reference Trait, Codex-conforming tools MUST reject that document with a `SchemaError` (§14).

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

A Codex document MUST contain exactly one root Concept instance.

### 8.1 File Encoding

Codex documents MUST be encoded in UTF-8 or UTF-16.

The canonical encoding is UTF-8 with no Byte Order Mark (BOM). Canonicalization MUST normalize UTF-16 encoded input to UTF-8, removing the BOM.

UTF-8 encoded files MUST NOT include a Byte Order Mark (BOM).

UTF-16 encoding MUST be indicated by a BOM at the start of the file:

- `FE FF` (2 bytes) indicates UTF-16 Big Endian.
- `FF FE` (2 bytes) indicates UTF-16 Little Endian.

Codex-conforming tools MUST determine the file encoding as follows:

- If the file starts with `FE FF`, interpret the file as UTF-16 Big Endian.
- If the file starts with `FF FE`, interpret the file as UTF-16 Little Endian.
- Otherwise, interpret the file as UTF-8 with no BOM.

Codex-conforming tools MUST reject any other encoding with a `ParseError` (§14).

### 8.2 Line Endings

The canonical line ending is LF (`\n`, U+000A).

Codex-conforming tools MUST normalize CRLF (`\r\n`) sequences to LF on input.

Codex-conforming tools MUST reject bare CR (`\r`) with a `ParseError` (§14).

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

Codex-conforming tools MUST reject any U+0020 SPACE character that appears in the indentation prefix of any of the following lines with a `ParseError` (§14):

- Concept marker lines
- Trait lines (including multi-line trait layout)
- non-blank content lines

If indentation cannot be normalized deterministically, Codex-conforming tools MUST fail with a `FormattingError` (§14).

### 8.4 Blank Lines

Blank lines are a canonical formatting requirement.

In canonical surface form, a Codex document MUST NOT start with a blank line.

Outside of content blocks (see §8.8) and annotations (see §8.9), Codex-conforming tools MUST NOT produce two consecutive blank lines in canonical surface form.

In canonical surface form, if no grouping or general annotations appear between two sibling Concept instances, there MUST be exactly one blank line between them.

For the purposes of this rule, an attached-annotation stack (see §8.9.6.1) MUST be treated as part of the Concept instance it attaches to.

If grouping or general annotations appear between two sibling Concept instances, blank line requirements are governed by the annotation rules (see §8.9.8).

In canonical surface form, Codex-conforming tools MUST reject documents containing any of the following with a `FormattingError` (§14):

- A blank line between a Concept instance's opening marker and its first child.
- A blank line between a Concept instance's last child and its closing marker.
- A blank line within a Concept instance body except between sibling children.

A blank line is a line containing no characters after normalization.

Codex-conforming tools MUST treat a line containing only whitespace as empty after normalization. This is a canonicalization rule: trailing whitespace on a line is stripped during Phase 1 canonicalization (§10.4). In canonical form, a blank line contains no characters before its newline.

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

or, when referencing a Concept from an imported schema (§11.2.1):

```cdx
<namespace:ConceptName>
<namespace:ConceptName trait=value>
```

The Concept name (or qualified Concept name) MUST follow the naming rules defined by this specification (§4.1). If the name does not conform to §4.1, Codex-conforming tools MUST reject the document with a `ParseError` (§14).

An opening marker includes zero or more Traits.

If multiple Traits are present, they MUST be ordered per §8.6.

#### 8.5.2 Closing Marker

A closing marker MUST be spelled as:

```cdx
</ConceptName>
```

or, when referencing a Concept from an imported schema (§11.2.1):

```cdx
</namespace:ConceptName>
```

The closing marker MUST match the most recent unclosed opening marker (see §3.6). A qualified closing marker MUST match a qualified opening marker exactly, including the namespace prefix.

The closing marker MUST appear on its own line after indentation. If the closing marker does not appear on its own line, Codex-conforming tools MUST reject the document with a `SurfaceFormError` (§14).

Additional content MUST NOT appear on the closing marker line. If additional content appears on the closing marker line, Codex-conforming tools MUST reject the document with a `SurfaceFormError` (§14).

#### 8.5.3 Self-Closing Marker

A self-closing marker MUST be spelled as:

```cdx
<ConceptName />
<ConceptName trait=value />
```

or, when referencing a Concept from an imported schema (§11.2.1):

```cdx
<namespace:ConceptName />
<namespace:ConceptName trait=value />
```

A self-closing marker represents a Concept instance with no content and no child Concepts.

Whitespace MUST appear immediately before `/>` in a self-closing marker.

A self-closing marker includes zero or more Traits.

If multiple Traits are present, they MUST be ordered per §8.6.

#### 8.5.4 Empty Block Concepts

Codex-conforming tools MUST reject the form `<ConceptName></ConceptName>` with a `ParseError` (§14).

### 8.6 Traits

A Trait MUST be spelled as:

```cdx
traitName=value
```

The `traitName` MUST follow the naming rules defined by this specification (§4.1). If the name does not conform to §4.1, Codex-conforming tools MUST reject the document with a `ParseError` (§14).

Whitespace MUST NOT appear around the `=` separator. If whitespace appears around `=`, Codex-conforming tools MUST reject the document with a `SurfaceFormError` (§14).

Traits MUST be separated by whitespace (space or newline).

If multiple Traits are present, canonical form MUST order them alphabetically by Trait name.

#### 8.6.1 Canonical Trait Formatting

Canonical surface form for Traits depends on whether the complete Concept marker fits within the 100-character line limit.

To determine layout, Codex-conforming tools MUST compute the total length of the Concept marker as if all Traits appeared on a single line: leading indentation, the `<` character, the Concept name, a space before each Trait, each `name=value` pair, and the closing `>` or ` />`. For this computation, each tab character (U+0009) MUST be counted as 2 characters.

If the computed length is 100 characters or fewer, all Traits MUST appear on the same line as the Concept marker.

If the computed length exceeds 100 characters, all Traits MUST be stacked: each Trait MUST appear on its own line, indented exactly one nesting level deeper than the Concept marker. The closing `>` or `/>` MUST appear on its own line at the same indentation level as the opening `<`.

A single `name=value` pair MUST NOT be wrapped across lines, even if it exceeds 100 characters.

A Backtick Text Value MUST NOT appear as an inline Trait value. If a Trait value is expressed as a Backtick Text Value, it MUST use its multiline form, which forces the Concept marker into stacked layout. Alternatively, the value MUST be converted to a Quoted Text Value.

If a document violates any formatting rule in this section, Codex-conforming tools MUST reject the document with a `FormattingError` (§14).

Example (canonical inline — total length under 100 characters):

```cdx
<Color id=urn:x:c1 name="Red" hex="#FF0000" />
```

Example (canonical stacked — total length exceeds 100 characters):

```cdx
<Book
	id=urn:isbn:978-0-618-26030-2
	title="The Hobbit, or There and Back Again"
	author="John Ronald Reuel Tolkien"
>
	[children here]
</Book>
```

Example (canonical stacked self-closing):

```cdx
<Book
	id=urn:isbn:978-0-618-26030-2
	title="The Hobbit, or There and Back Again"
	author="John Ronald Reuel Tolkien"
/>
```

### 8.7 Values (Surface Parsing Notes)

In the Surface Form, Trait values are literal spellings of Value types defined by this specification (see §5).

Codex-conforming tools MUST NOT evaluate, interpret, or normalize Values beyond recognizing their Value type and literal structure.

A Trait value spelling MUST match exactly one Value spelling defined by this specification (see §5).

If a Trait value spelling does not match any Value spelling defined by this specification, Codex-conforming tools MUST reject it with a `ParseError` (§14).

Within a Concept marker, a Value MUST terminate at the first of the following:

- whitespace outside balanced delimiters (space, tab, or newline)
- `>` or `/>` (end of Concept marker)

While scanning for Value termination, Codex-conforming tools MUST respect balanced delimiters as required by the Value spellings defined in §5, including `[]`, `{}`, `()`, `''`, and `""`.

Except where permitted by a Value spelling (for example, within text and character literals), leading and trailing whitespace MUST NOT be treated as part of a Value.

#### 8.7.1 Value Type Disambiguation

When a maximal Value token (recognized under the termination rules above) could match the spelling rules of more than one Value type, tools MUST resolve the type by deterministic precedence. The Value type MUST be the first match in the following order:

1. Delimited values: Text Value (`"..."`, `'...'`), Character Value, Backtick Text, Host Name Value (`host(...)`), Email Address Value (`email(...)`), URL Value (`url(...)`)
2. Boolean Value (`true` or `false`)
3. Enumerated Token Value (`$...`)
4. Lookup Token Value (`~...`)
5. Temporal Value (`{...}`)
6. Set Value (`set[...]`)
7. Map Value (`map[...]`)
8. Record Value (`record[...]`)
9. List Value (`[...]`)
10. Tuple Value (`(...)`)
11. Color Value (all permitted color literal spellings, including function-based and named colors)
12. UUID Value (8-4-4-4-12 hexadecimal pattern)
13. Range Value (contains `..` with valid endpoints)
14. Numeric Value (ComplexNumber, ImaginaryNumber, PrecisionNumber, ExponentialNumber, Fraction, PositiveInfinity, NegativeInfinity, DecimalNumber, Integer per §5.4)
15. IRI Reference Value (fallback: token contains `:` and matches the IRI Reference spelling per §5.9)

If a token matches multiple Value type spellings at the same precedence level, tools MUST reject it with a `ParseError` (§14).

#### 8.7.2 Multiline Value Literals

Codex-conforming tools MUST accept multiline spellings for Value literals that use balanced delimiters, including list (`[...]`), set (`set[...]`), map (`map[...]`), record (`record[...]`), and tuple (`(...)`).

Within a balanced Value literal:

* Line breaks within a balanced Value literal MUST be treated as whitespace.
* Whitespace between elements, entries, or delimiters MUST NOT be treated as significant.
* Whitespace MUST NOT terminate the Value.

In canonical surface form, exactly one space MUST follow each comma separator within a balanced Value literal. All other optional whitespace within balanced Value literals MUST be removed. Mandatory whitespace required by a specific production MUST be preserved.

Outside of balanced delimiters, a Value literal MUST be fully contained on a single line.

Codex-conforming tools MUST determine Value boundaries solely by balanced delimiter matching and MUST NOT treat line boundaries as semantically significant within a Value literal.

### 8.8 Content Blocks

A Content Block is opaque text between an opening marker and a closing marker.

Content MUST NOT be interpreted as Codex structure, Traits, or Values.

#### 8.8.1 Content Termination

Codex-conforming tools MUST identify the end of content by scanning for the closing marker that matches the opening Concept name: `</ConceptName>`.

#### 8.8.2 Content Escaping

Within content:

- `\\` represents a literal `\`.
- `\<` represents a literal `<`.
- `\[` represents a literal `[`.

A backslash not immediately followed by `\`, `<`, or `[` is a literal backslash and has no special meaning.

A raw `<` character MUST NOT appear anywhere in content.

A raw `[` character MUST NOT appear as the first non-indentation character of a content line. This preserves schema-less determinism of content-versus-children body mode (see §10.1.1.1).

Codex-conforming tools MUST reject violations of these content escaping rules with a `ParseError` (§14).

#### 8.8.3 Content Indentation Normalization

Codex-conforming tools MUST store and process content without its canonical leading indentation.

In canonical surface form, each non-blank content line MUST be indented exactly one nesting level deeper than its enclosing Concept instance.

For each non-blank content line, the canonical leading indentation is the exact leading indentation required to place that line at one nesting level deeper than its enclosing Concept instance.

Codex-conforming tools MUST remove exactly that canonical leading indentation from each non-blank content line when producing the logical content.

Codex-conforming tools MUST preserve all characters following the removed indentation, including any additional leading whitespace.

If a non-blank content line does not have the required canonical leading indentation after indentation normalization, Codex-conforming tools MUST fail with a `FormattingError` (§14).

Indentation normalization is schema-free and MUST be performed before schema-directed processing.

#### 8.8.4 Whitespace Mode Normalization

Whitespace mode normalization is schema-directed and MUST be performed during schema-directed processing.

The governing schema declares `whitespaceMode` on each Concept that allows content (see §11.3.2).

For `whitespaceMode=$Preformatted`:

* Codex-conforming tools MUST preserve all content whitespace exactly after indentation normalization.

For `whitespaceMode=$Flow`:

* Codex-conforming tools MUST collapse each run of whitespace characters (spaces, tabs, and line breaks) to a single U+0020 SPACE.
* Codex-conforming tools MUST trim leading and trailing whitespace from the resulting content.
* In canonical surface form, Codex-conforming tools MUST wrap content to lines of at most 100 characters, including canonical indentation, breaking at whitespace boundaries. For this computation, each tab character (U+0009) MUST be counted as 2 characters. If a non-breakable sequence plus its canonical indentation exceeds 100 characters, it MUST appear on its own line without wrapping.
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

Annotations MUST be permitted at top-level and within bodies interpreted as containing child Concepts.

Annotations MUST NOT appear inside Concept markers (that is, inside `<Concept …>`, `</Concept>`, or `<Concept />`).

#### 8.9.2 Structural Rules

The opening `[` MUST be the first non-whitespace character on its line.

For an inline annotation, the closing `]` MUST appear on the same line.

For a block annotation:

* The line containing `[` MUST contain no other non-whitespace characters.
* The closing `]` MUST appear as the first non-whitespace character on its own line.
* The closing `]` line MUST contain no other non-whitespace characters.

If a document violates any structural rule in this section, Codex-conforming tools MUST reject the document with a `SurfaceFormError` (§14).

#### 8.9.3 Escaping

Within an annotation:

* `\\` represents a literal `\`.
* `\]` represents a literal `]`.

A backslash not immediately followed by `\` or `]` is a literal backslash and has no special meaning.

#### 8.9.4 Canonical Form

Canonicalization of annotations is deterministic and depends on the annotation form.

##### 8.9.4.1 Inline Annotation Canonicalization

Codex-conforming tools MUST canonicalize inline annotations as follows:

* Leading and trailing whitespace inside the brackets MUST be trimmed.
* Internal runs of whitespace (spaces and tabs) MUST be collapsed to a single space.
* Escaped closing brackets MUST remain escaped (that is, `\]` MUST remain spelled as `\]`).

##### 8.9.4.2 Block Annotation Canonicalization

Block annotations MUST preserve their internal line structure.

Codex-conforming tools MUST normalize block-annotation line endings to LF.

For a block annotation with no directive, Codex-conforming tools MUST:

* Remove trailing whitespace on each content line.
* Normalize indentation so that the content lines are indented exactly one tab deeper than the `[` / `]` lines.

#### 8.9.5 Block Annotation Directives

In a block annotation, the first non-blank content line is a directive line if it matches one of the directive forms defined below.

If present, the directive line MUST be exactly one of:

* `FLOW:`
* `CODE:`
* `MARKDOWN:`

Directive recognition MUST be performed prior to any canonicalization other than newline normalization.

If present, the directive line MUST be preserved in canonical output.

Directive behavior:

* `CODE:` — Codex-conforming tools MUST preserve the block annotation bytes verbatim except for newline normalization.
* `MARKDOWN:` — Codex-conforming tools MUST preserve the block annotation bytes verbatim except for newline normalization.
* `FLOW:` — Codex-conforming tools MUST trim leading and trailing whitespace from the remaining content, MUST collapse internal runs of whitespace to single spaces, and MUST interpret escapes per §8.9.3.

If no directive is present, the block annotation MUST be canonicalized as described in §8.9.4.2.

For `FLOW:` directives, Codex-conforming tools MUST render canonical output as follows:

* Split the remaining content into paragraphs separated by one or more blank lines.
* For each paragraph, wrap words to lines using the 100-character line limit defined in §8.8.4, including canonical indentation and counting tabs as 2 characters. If a non-breakable sequence plus its canonical indentation exceeds 100 characters, it MUST appear on its own line without wrapping.
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

Stacked attached annotations MUST be contiguous and MUST NOT be separated by blank lines.

An attached-annotation stack attaches to the next Concept opening marker.

##### 8.9.6.2 Grouping Annotations

A grouping annotation is a single-line annotation whose canonicalized annotation text matches one of the following forms:

* `GROUP: <label>`
* `END: <label>`

`<label>` MUST be non-empty text after trimming.

Grouping recognition MUST be performed after applying the inline annotation canonicalization rules in §8.9.4.1.

Label comparison MUST use the canonical label form (trimmed, with internal whitespace collapsed to single spaces).

Grouping annotations MUST conform to the canonical blank-line requirements in §8.9.8.

##### 8.9.6.3 General Annotations

An annotation is a general annotation if and only if:

* It is not an attached annotation.
* It is not a grouping annotation.
* It is surrounded by exactly one blank line above and exactly one blank line below, where file boundaries count as blank-line boundaries.

#### 8.9.7 Group Nesting and Matching

Grouping annotations form a properly nested stack.

* `[GROUP: X]` pushes label `X`.
* `[END: X]` MUST match the most recent unmatched `[GROUP: X]`.

If an `END` label does not match the most recent open group label, or if an `END` appears with no open group, Codex-conforming tools MUST reject the document with a `ParseError` (§14).

#### 8.9.8 Canonical Blank Line Requirements

In canonical surface form:

* Attached annotations MUST appear directly above the annotated Concept opening marker with no blank line.
* Grouping and general annotations MUST be surrounded by exactly one blank line above and below, where file boundaries count as blank-line boundaries.

If an annotation does not qualify as an attached annotation, a grouping annotation, or a general annotation, Codex-conforming tools MUST reject the document with a `ParseError` (§14).

---

## 9. Schema-First Architecture

A conforming implementation MUST provide schema-directed validation.

This specification defines the authoritative model for schema authoring, schema-to-instance-graph interpretation, and deterministic projection to derived validation artifacts.

Canonical Authoring Mode permits authors to write the canonical RDF representation directly. Simplified Authoring Mode permits authors to write a Codex-native surface form that has no independent semantics and exists only as a deterministic, lossless authoring convenience; documents written in Simplified Authoring Mode MUST expand to a byte-identical canonical RDF representation.

No other semantic layers, representations, or interpretive stages exist in Codex, and implementations MUST treat the canonical RDF representation as the sole source of truth.

### 9.1 Scope and Inputs

Given the same required inputs, a conforming implementation MUST produce the same validation and canonicalization results.

The required inputs for schema-directed processing are:

- the Codex document bytes
- the governing schema
- imported schemas, if the document or governing schema declares schema imports (see §11.2.1)
- `documentBaseIri` (for instance graph mapping; see §9.7)

Other external inputs—including environment state, configuration, registries, network access, clocks, or randomness—MUST NOT influence processing.

If any required input is missing, schema-directed processing MUST fail with a `SchemaError` (§14).

Given a Codex document and a governing schema, a conforming implementation MUST dispatch validation according to that schema.

### 9.2 Schema-Less Formatting / Well-Formedness Checks

Schema-less checks MUST be limited to rules that are explicitly defined by this specification as independent of schema semantics.

Schema-less checks are limited to:

- determining whether the input bytes can be decoded as a permitted file encoding
- determining whether the input matches the surface-form grammar
- mechanically recognizing and classifying Value spellings into their Value kinds (and any grammar-defined value types) using only surface-form grammar rules, without reference to schema-defined value types
- enforcing surface-form structural well-formedness (including marker nesting/matching)
- enforcing surface-form canonicalization rules defined by this specification

Without a governing schema, an implementation MUST NOT:

- interpret content mode versus child mode for a concept beyond the surface-form rule defined in §8.8
- determine Entity eligibility; a parser observes the presence or absence of an `id` trait spelling, but Entity status (`$MustBeEntity` / `$MustNotBeEntity`) is schema-directed (§11)
- evaluate trait meaning, trait authorization, expected `ValueType` constraints, value typing beyond surface-form Value recognition, or constraint logic
- resolve reference traits beyond their surface-form value type constraints

### 9.3 Schema-Required Semantic Validation

An implementation MUST NOT perform semantic validation without a governing schema.

Given a governing schema, an implementation MUST perform semantic validation as defined by that schema.

Schema-driven semantic validation MUST be traceable to the specific schema rule(s) applied.

Schema-driven semantic validation MUST include evaluation of all schema-defined authorizations and constraints:

- concept authorization and required/forbidden structure
- content mode versus child mode requirements
- trait authorization and required/forbidden traits
- value type constraints beyond surface-form recognition
- entity eligibility and any schema-defined identity constraints
- schema-defined constraints over children, descendants, and collections
- schema-defined reference semantics and any schema-defined resolution requirements

The required semantics for schema-driven validation and the instance graph are defined by §9.5–§9.11 and by the schema definition language (§11).

### 9.4 Authoring Modes

A schema document MUST be validated under exactly one authoring mode.

Codex defines two authoring modes:

- **Simplified Authoring Mode**: Codex-native schema-definition authoring surface only (§9.5, §11)
- **Canonical Authoring Mode**: Canonical Representation authoring only via `RdfGraph` (§9.6)

All conforming implementations MUST support both authoring modes.

The schema document's root `Schema` concept MUST have an `authoringMode` trait.

`authoringMode` MUST be exactly one of `$SimplifiedMode` or `$CanonicalMode`; any other value or a missing `authoringMode` trait is a `SchemaError` (§14).

The following mode-specific constraints MUST hold:

- Simplified mode schemas MUST contain exactly one `ConceptDefinitions` and MUST NOT contain `RdfGraph`.
- Canonical mode schemas MUST contain exactly one `RdfGraph` and MUST NOT contain Codex-native schema-definition concepts (including `ConceptDefinitions`, `TraitDefinitions`, `EnumeratedValueSets`, `ConstraintDefinitions`, `ValueTypeDefinitions`, and `ValidatorDefinitions`).
- Simplified-mode expansion MUST generate the Canonical Representation as a canonical RDF graph; different simplified spellings that are semantically identical MUST expand to byte-identical canonical RDF graphs.
- Canonicalization of the Canonical Representation MUST make semantically identical graphs byte-identical.

### 9.5 Simplified Authoring Mode (Codex-Native Schema Authoring Surface)

Simplified Authoring Mode is the Codex-native schema-definition authoring surface defined by the schema definition language (§11).

To support a total, deterministic projection to derived validation artifacts, simplified-mode schema authoring MUST support the following extensions.

#### 9.5.1 Pattern Flags

The following atomic constraints MUST support an optional `flags` trait whose value is text:

- `ValueMatchesPattern`
- `PatternConstraint`
- `ContentMatchesPattern`

If `flags` is omitted, it MUST be treated as empty text.

The `pattern` and `flags` semantics MUST be SPARQL 1.1 `REGEX` semantics.

#### 9.5.2 Explicit Validator Definitions

Simplified Authoring Mode MUST support explicit validator definitions that make `ValueIsValid` deterministic.

`ValidatorDefinitions` is a container concept.

`ValidatorDefinition` defines one validator.

A `ValidatorDefinition` is an Entity.

Each `ValidatorDefinition` MUST have these traits:

- `id` (required; IRI Reference Value)
- `name` (required; Concept name per §4 Naming Rules)
- `message` (required; Text Value)

`ValidatorDefinition` names MUST be unique within the Schema.

Each `ValidatorDefinition` MUST be in content mode.

The content of `ValidatorDefinition` MUST be a SPARQL `SELECT` query text.

The `SELECT` results MUST follow the SHACL-SPARQL convention (returning one row per violation with `?this` bound to the focus node).

If a derived validation artifact is expressed using SHACL-SPARQL, the embedding contract for `ValueIsValid validatorName=$X` MUST be:

1. Resolve `$X` to exactly one `ValidatorDefinition` in the governing schema.
2. Emit a SHACL-SPARQL constraint whose `sh:select` text is exactly the `ValidatorDefinition` content.

If `$X` cannot be resolved to exactly one `ValidatorDefinition`, schema processing MUST fail with a `SchemaError` (§14).

#### 9.5.3 Explicit Path and Quantifier Rule Forms

The schema definition language (§11) defines paths (`TraitPath`, `ChildPath`, `DescendantPath`, `ContentPath`) and quantifiers (`Exists`, `ForAll`, `Count`) but does not define a concrete rule-node form that composes them with rules.

To produce a total, deterministic mapping, Simplified Authoring Mode MUST provide explicit rule-node forms that bind exactly one path to exactly one nested rule.

Simplified Authoring Mode MUST provide the following rule nodes:

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

`ChildSatisfies(conceptSelector=X, Rule=R)` MUST be interpreted as equivalent to `OnPathForAll(Path=ChildPath(X), Rule=R)`.

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

If the member-selection path is not one of these, expansion MUST fail with a `SchemaError` (§14).

For `CollectionAllowsDuplicates` with `allowed=false`, the constraint node MUST include a required `keyTrait` trait whose value is a Trait name.

If `keyTrait` is `id`, it MUST refer to the declared identifier as specified by the instance-graph identity rules.

### 9.6 Canonical Representation (RDF / SHACL)

The Canonical Representation of Codex schemas is an RDF 1.1 graph.

The Canonical Representation MUST be deterministic and canonical:

- The Canonical Representation MUST NOT contain RDF blank nodes.
- All RDF nodes in the Canonical Representation MUST be IRIs.
- Where SHACL commonly uses blank nodes (for example, `sh:property` values and RDF lists), the Canonical Representation MUST use deterministically derived skolem IRIs instead.
- The Canonical Representation MUST be treated as a set of RDF triples.
- The Canonical Representation MUST NOT contain duplicate triples.

#### 9.6.1 Canonical Triple Form

When the Canonical Representation is authored as a Codex graph form, it MUST use:

- `RdfGraph` — container for triples
- `RdfTriple` — a single RDF triple

`RdfGraph` MUST be in children mode.

`RdfGraph` children MUST include one or more `RdfTriple`. `RdfGraph` children MUST be `RdfTriple` children and annotations only; no other Concept children are allowed.

Each `RdfTriple` MUST have these traits:

- `subject` (required; IRI Reference Value)
- `predicate` (required; IRI Reference Value)

And exactly one of:

- `object` (required; IRI Reference Value) — object IRI
- `lexical` (required; Text Value) — object literal lexical form

When `lexical` is present, the following additional traits are permitted:

- `datatype` (IRI Reference Value) — RDF datatype IRI
- `language` (Text Value) — RDF language tag

If `language` is present, `datatype` MUST be absent.

If `datatype` is absent and `language` is absent, the literal datatype MUST be `xsd:string`.

#### 9.6.2 Canonical Ordering and Duplicate Removal

The sort key for an `RdfTriple` is the tuple `(subject, predicate, objectKey)`, compared in ascending lexicographic order.

`objectKey` MUST be:

- `object` when the object is an IRI, and
- the tuple `(datatypeOrDefault, languageOrEmpty, lexical)` when the object is a literal.

`datatypeOrDefault` MUST be: `datatype` if present; otherwise `rdf:langString` if `language` is present; otherwise `xsd:string`.

`languageOrEmpty` MUST be: `language` if present; otherwise the empty string.

If two triples have identical sort keys, the duplicate MUST be removed.

When an `RdfGraph` contains no grouping annotations (§8.9.7), all `RdfTriple` children MUST be sorted by sort key.

When an `RdfGraph` contains grouping annotations, the following rules apply:

1. Within each group, `RdfTriple` children MUST be sorted by sort key.
2. Groups at the same nesting level MUST be sorted in ascending lexicographic order of their canonical group label.
3. `RdfTriple` children not enclosed in any group MUST be sorted by sort key and MUST appear before all groups at the same nesting level.
4. An attached annotation (§8.9.6.1) on an `RdfTriple` MUST move with that triple during sorting.

#### 9.6.3 RDF List Encoding (No Blank Nodes)

If the Canonical Representation includes an RDF list (for example, as the object of `sh:in`), it MUST be encoded using the standard RDF list vocabulary (`rdf:first`, `rdf:rest`, `rdf:nil`).

All RDF list nodes MUST be IRIs.

Where the RDF list encoding would otherwise use blank nodes, the Canonical Representation MUST use deterministically derived skolem IRIs instead.

At most one RDF list MUST be attached as the object of triples sharing a given `(subject, predicate)` pair.

For an RDF list attached as the object of a triple `(subject, predicate, _)`, list node IRIs MUST be derived as follows:

- Let `listAnchor = subject + "/list/" + iriHash(predicate)`.
- For the list node at position `i` (0-indexed): `listNodeIri(listAnchor, i) = listAnchor + "/" + i`.
- The list head is the node at position 0.
- The final list node's `rdf:rest` MUST be `rdf:nil`.

#### 9.6.4 Deterministic IRI Hashing

When a derived IRI embeds another IRI or name as a path component, the embedded value MUST be hashed to produce fixed-length, path-safe text.

`iriHash(value)` MUST be computed as:

1. Encode the value as a UTF-8 byte sequence.
2. Compute the SHA-256 hash of that byte sequence.
3. Encode the hash as lowercase hexadecimal (64 characters).

#### 9.6.5 Deterministic Derived IRIs (One Way To Say It)

To preserve "one way to say it", every derived IRI used by schema processing, instance graph mapping, and derived validation artifact generation MUST be computed by a single deterministic algorithm.

This requirement applies to:

- derived node IRIs (skolem IRIs)
- derived shape IRIs (node shapes, property shapes)
- derived SPARQL variable names
- derived graph structures (RDF lists, edge nodes)

#### 9.6.6 Node Shape IRIs

The node shape IRI for a concept class IRI `K` MUST be deterministically derived as:

- `nodeShapeIri(K) = K + "#shape"`

#### 9.6.7 Property Shape IRIs

Each property shape MUST have a deterministic IRI.

For a node shape IRI `S` and a trait name `t`:

- `propertyShapeIri(S,t) = S + "/property/trait/" + iriHash(t)`

For a node shape IRI `S` and a child class IRI `Q`:

- `propertyShapeIri(S,Q) = S + "/property/child/" + iriHash(Q)`

For a node shape IRI `S` and an RDF predicate IRI `p` used as a SHACL path (for example, `codex:content` or `codex:isEntity`):

- `predicatePropertyShapeIri(S,p) = S + "/property/predicate/" + iriHash(p)`

#### 9.6.8 Document Node Shape IRI

The document node shape IRI MUST be deterministically derived as:

- `documentNodeShapeIri = schemaIri + "#shape/Document"`

#### 9.6.9 SPARQL Constraint IRIs

Each SHACL-SPARQL constraint node emitted for a `ConstraintDefinition` MUST have a deterministic IRI.

For a target node shape IRI `S` and a `ConstraintDefinition` with `id` value `C`:

- `sparqlConstraintIri(S, C) = S + "/constraint/" + iriHash(C)`

### 9.7 Codex→RDF Instance Graph Mapping

Codex defines a canonical mapping from a parsed Codex document to an RDF instance graph.

The mapping MUST be deterministic and MUST NOT use RDF blank nodes.

The mapping requires an explicit `documentBaseIri` external input.

If `documentBaseIri` is missing, the mapping MUST fail with a `SchemaError` (§14).

#### 9.7.1 Document Node

The instance graph MUST include a single document node.

The RDF node IRI for the Document context MUST be exactly `documentBaseIri`.

#### 9.7.2 Node Identity and Declared Identifiers

Each Concept instance in the Codex document MUST map to exactly one RDF node whose identity is a deterministic skolem IRI derived from its structural position within the document. The `codex:` prefix used in this section is shorthand; full IRI derivations are defined in §9.7.5.

##### 9.7.2.1 Skolem IRI Derivation (`nodeIri`)

Let `C` be a Concept instance.

Let `C.name` be the concept name of `C`.

Let `parent(C)` be the direct parent Concept instance of `C`, or the Document context if `C` is a root Concept instance.

Let `siblings(C)` be:

- the ordered list of all top-level Concept instances in the document (in canonical order) if `parent(C)` is the Document context, or
- the ordered list of all direct child Concept instances of `parent(C)` (in canonical order) otherwise.

Let `ordinalIndex(C)` be the unique integer `i` such that `siblings(C)[i]` is `C`.

`ordinalIndex(C)` MUST be zero-based.

`ordinalIndex(C)` MUST be expressed in base-10 with no leading zeros (except that `0` is permitted).

Define `addressSegments(C)` as the ordered list of segments obtained by walking from the document root to `C` (inclusive), where each segment for a visited node `X` is:

- `iriHash(X.name) + "/" + ordinalIndex(X)`

Define `nodeIri(C)` as:

- `documentBaseIri + "/__node/" + join("/", addressSegments(C))`

The RDF node IRI MUST NOT be derived from the Concept instance's declared `id` trait value.

If a Concept instance declares an `id` trait, that declared identifier MUST be represented as data via a dedicated predicate `codex:declaredId`.

If a concept instance `C` declares an `id` trait with value `v`, the mapping MUST emit:

- `(nodeIri(C), codex:declaredId, valueTerm(v))`

#### 9.7.3 Entity Marker

If and only if a Concept instance is an Entity, the mapped RDF node MUST be marked as an Entity using a dedicated predicate `codex:isEntity`.

The mapping MUST emit an entity marker for every Concept instance node:

- If the concept instance is an Entity, emit `(nodeIri(C), codex:isEntity, "true"^^xsd:boolean)`.
- Otherwise, emit `(nodeIri(C), codex:isEntity, "false"^^xsd:boolean)`.

#### 9.7.4 Parent Link and Ordered Children

For each non-root Concept instance, the instance graph MUST include a parent link using a dedicated predicate `codex:parentNode`.

For each parent Concept instance `C` and each direct child Concept instance `D`, the instance graph MUST emit:

- `(nodeIri(D), codex:parentNode, nodeIri(C))`

For each child Concept instance `D` of parent Concept instance `C`, the instance graph MUST emit the structural child triple:

- `(nodeIri(C), childPredicateIri(C,D), nodeIri(D))`

The instance graph MUST additionally represent the ordered child sequence using explicit edge nodes that carry a stable numeric index (see §9.7.6).

#### 9.7.5 Reserved Predicates

For the purposes of this section, let `schemaIri` be the governing schema's `Schema.id` value.

The following reserved predicates are used by the instance graph mapping:

- `codex:parent`
- `codex:child`
- `codex:index`
- `codex:parentNode`
- `codex:isEntity`
- `codex:declaredId`
- `codex:content`
- `codex:annotationParent`
- `codex:annotationIndex`
- `codex:annotationText`
- `codex:annotationForm`
- `codex:annotationKind`
- `codex:annotationDirective`
- `codex:annotationTarget`
- `codex:mapKey`
- `codex:mapValue`
- `codex:rangeStart`
- `codex:rangeEnd`
- `codex:rangeStep`

Their IRIs MUST be deterministically derived from `schemaIri` as follows:

- `codex:parent` MUST be `schemaIri + "#codex/parent"`
- `codex:child` MUST be `schemaIri + "#codex/child"`
- `codex:index` MUST be `schemaIri + "#codex/index"`
- `codex:parentNode` MUST be `schemaIri + "#codex/parentNode"`
- `codex:isEntity` MUST be `schemaIri + "#codex/isEntity"`
- `codex:declaredId` MUST be `schemaIri + "#codex/declaredId"`
- `codex:content` MUST be `schemaIri + "#codex/content"`
- `codex:annotationParent` MUST be `schemaIri + "#codex/annotationParent"`
- `codex:annotationIndex` MUST be `schemaIri + "#codex/annotationIndex"`
- `codex:annotationText` MUST be `schemaIri + "#codex/annotationText"`
- `codex:annotationForm` MUST be `schemaIri + "#codex/annotationForm"`
- `codex:annotationKind` MUST be `schemaIri + "#codex/annotationKind"`
- `codex:annotationDirective` MUST be `schemaIri + "#codex/annotationDirective"`
- `codex:annotationTarget` MUST be `schemaIri + "#codex/annotationTarget"`
- `codex:mapKey` MUST be `schemaIri + "#codex/mapKey"`
- `codex:mapValue` MUST be `schemaIri + "#codex/mapValue"`
- `codex:rangeStart` MUST be `schemaIri + "#codex/rangeStart"`
- `codex:rangeEnd` MUST be `schemaIri + "#codex/rangeEnd"`
- `codex:rangeStep` MUST be `schemaIri + "#codex/rangeStep"`

#### 9.7.6 Ordered Children Encoding

For each Concept instance `D`, let:

- `p = nodeIri(C)` if `D` is a direct child of parent Concept instance `C`; `p = documentBaseIri` if `D` is a root Concept instance
- `d = nodeIri(D)`
- `i` be the ordinal position of `D` among all sibling items (Concept instances and annotations) at the same nesting level, in canonical order, starting from 0

The mapping MUST emit an edge node `e` and three triples:

- `(e, codex:parent, p)`
- `(e, codex:child, d)`
- `(e, codex:index, "i"^^xsd:integer)`

The edge node IRI MUST be:

- `e = p + "/__childEdge/" + i`

#### 9.7.7 Annotation Nodes

For each annotation `A` at a given nesting level, let:

- `p = nodeIri(C)` if the nesting level is the children context of parent Concept instance `C`; `p = documentBaseIri` if the annotation is at document top level
- `i` be the ordinal position of `A` in the unified sibling index (§9.7.6), starting from 0

The mapping MUST emit an annotation edge node `e` with the following triples:

- `(e, codex:annotationParent, p)`
- `(e, codex:annotationIndex, "i"^^xsd:integer)`
- `(e, codex:annotationText, "text"^^xsd:string)` where `text` is the canonical annotation text after canonicalization (§8.9.4)
- `(e, codex:annotationForm, "form"^^xsd:string)` where `form` is `inline` or `block` (§8.9.1)
- `(e, codex:annotationKind, "kind"^^xsd:string)` where `kind` is `attached`, `grouping`, or `general` (§8.9.6)

The annotation edge node IRI MUST be:

- `e = p + "/__annotationEdge/" + i`

If the annotation has a block directive (§8.9.5), the mapping MUST additionally emit:

- `(e, codex:annotationDirective, "directive"^^xsd:string)` where `directive` is `CODE`, `MARKDOWN`, or `FLOW`

If no block directive is present, no `codex:annotationDirective` triple is emitted.

If the annotation is an attached annotation (§8.9.6.1), the mapping MUST additionally emit:

- `(e, codex:annotationTarget, nodeIri(D))` where `D` is the Concept instance to which the annotation is attached

#### 9.7.8 Traits and Value Terms

For each trait `t=v` on a concept instance `C`, the instance graph MUST emit exactly one triple:

- `(nodeIri(C), traitPredicateIri(t), valueTerm(v))`

Exception:

- If `t` is `id`, the mapping MUST NOT emit a `traitPredicateIri("id")` triple.
- Instead, `id` MUST be represented only by `codex:declaredId`, with the `id` value as an IRI (not a literal).

Because `id` has no `traitPredicateIri` representation in the instance graph, schema definitions MUST NOT target `id` through generic trait mechanisms (`TraitRules`, `TraitPath`, `TraitExists`, `TraitMissing`, `TraitEquals`). The `id` trait is governed by `entityEligibility` (§6.1) and identity constraints (§9.9.6, §9.9.7). If a generic trait mechanism references `id`, derived validation artifact generation MUST fail with a `SchemaError` (§14).

`valueTerm(v)` MUST be:

- an IRI when `v` is an IRI Reference Value
- an IRI when `v` is an Enumerated Token Value and the governing trait is constrained by an `EnumeratedValueSet` (see below)
- the collection head IRI of the collection graph (§9.7.8.1) when `v` is a collection value (List, Set, Map, Record, Tuple, or Range)
- otherwise a typed literal

For typed literals, the datatype IRI MUST be computed by `valueDatatypeIri(v)` and the lexical form MUST be computed by `valueLex(v)`.

Both `valueDatatypeIri(v)` and `valueLex(v)` MUST be derived by parsing `v` according to the Codex value catalog.

`valueDatatypeIri(v)` MUST be:

- `xsd:string` for Text Values
- `xsd:string` for Character Values
- `xsd:boolean` for Boolean Values
- `xsd:integer` for Integer Values

For all other scalar value types, `valueDatatypeIri(v)` MUST be the deterministic URN:

- `urn:cdx:value-type:<T>`

where `<T>` is the Codex value type token name (for example, `Uuid`, `HexColor`, `PlainDate`).

Collection value types (List, Set, Map, Record, Tuple, and Range) do not produce typed literals. Their RDF mapping is defined in §9.7.8.1.

`valueLex(v)` MUST be:

- the decoded Unicode text value for Text Values
- the single Unicode scalar value as Unicode text for Character Values
- `"true"` or `"false"` for Boolean Values
- base-10 integer text for Integer Values

For all other scalar value types, `valueLex(v)` MUST be the canonical surface spelling of `v`.

Lookup Token Values MUST be represented as typed literals with:

- datatype: `urn:cdx:value-type:LookupToken`
- lexical form: the canonical surface spelling (for example, `~myToken`)

When an Enumerated Token Value `v` appears on a trait that is constrained by an `EnumeratedValueSet` `E` (via `AllowedValues` containing an `EnumeratedConstraint` referencing `E`), `valueTerm(v)` MUST be the IRI:

- `E.id + "#" + tokenName(v)`

where `tokenName(v)` is the token name without the `$` sigil.

This rule applies to scalar trait values. For Enumerated Token Values within collections, see §9.7.8.1.

If the trait is constrained only by `ValueIsOneOf` (not by an `EnumeratedConstraint` referencing an `EnumeratedValueSet`), Enumerated Token Values fall through to the typed literal case above. `ValueIsOneOf` does not provide an `EnumeratedValueSet` from which to derive an IRI base.

If the trait is not constrained by any `EnumeratedValueSet`, the Enumerated Token Value falls through to the typed literal case above.

If a schema constraint requires an interpreted value (for example, numeric comparisons or text length), schema processing MUST provide the interpreted value in a deterministic RDF representation.

##### 9.7.8.1 Collection Value Graphs

When a trait value `v` is a collection (List, Set, Map, Record, Tuple, or Range), `valueTerm(v)` MUST NOT be a typed literal. Instead, the value MUST be represented as a structured collection graph using the standard RDF list vocabulary (`rdf:first`, `rdf:rest`, `rdf:nil`) and reserved Codex predicates.

All collection graph nodes MUST be IRIs. No blank nodes are permitted (§9.6.1).

**List anchor and node IRIs.**

For a trait `t=v` on concept instance `C`, let:

- `traitPredIri = traitPredicateIri(t)`
- `collectionAnchor = nodeIri(C) + "/list/" + iriHash(traitPredIri)`

List node IRIs MUST follow the same pattern as §9.6.3:

- `listNodeIri(collectionAnchor, i) = collectionAnchor + "/" + i`

The list head node is at position 0. `valueTerm(v)` for the trait MUST be `listNodeIri(collectionAnchor, 0)`.

If the collection is empty (zero elements), `valueTerm(v)` MUST be `rdf:nil`.

**Ordered collections (List, Tuple).**

For a List or Tuple with elements `e_0, e_1, ..., e_(n-1)`:

For each position `i` from 0 to n-1, the mapping MUST emit:

- `(listNodeIri(collectionAnchor, i), rdf:first, elementTerm(e_i))`
- `(listNodeIri(collectionAnchor, i), rdf:rest, listNodeIri(collectionAnchor, i+1))` — or `rdf:nil` when `i = n-1`

**Unordered collections (Set).**

Sets use the same RDF list encoding as Lists. Element order in the RDF list MUST match canonical source order (§5.14).

**Keyed collections (Map, Record).**

For a Map or Record with entries `(k_0:v_0), (k_1:v_1), ..., (k_(n-1):v_(n-1))`:

For each position `i` from 0 to n-1, let `entryIri = listNodeIri(collectionAnchor, i) + "/__entry"`. The mapping MUST emit:

- `(listNodeIri(collectionAnchor, i), rdf:first, entryIri)`
- `(listNodeIri(collectionAnchor, i), rdf:rest, listNodeIri(collectionAnchor, i+1))` — or `rdf:nil` when `i = n-1`
- `(entryIri, codex:mapKey, elementTerm(k_i))`
- `(entryIri, codex:mapValue, elementTerm(v_i))`

Entry order in the RDF list MUST match canonical source order.

**Range.**

For a Range `start..end` (with optional step), let the components be `start`, `end`, and (if present) `step`. A Range MUST be encoded as a single RDF resource (not a list). Let `rangeIri = nodeIri(C) + "/range/" + iriHash(traitPredIri)`. The mapping MUST emit:

- `(rangeIri, codex:rangeStart, elementTerm(start))`
- `(rangeIri, codex:rangeEnd, elementTerm(end))`
- If a step is present: `(rangeIri, codex:rangeStep, elementTerm(step))`

`valueTerm(v)` for a Range MUST be `rangeIri`.

**`elementTerm(e)`.**

Each element `e` within a collection MUST be mapped to an RDF term as follows:

- If `e` is an IRI Reference Value, `elementTerm(e)` MUST be the IRI.
- If `e` is an Enumerated Token Value and the governing trait is constrained by an `EnumeratedValueSet` `E`, `elementTerm(e)` MUST be the IRI `E.id + "#" + tokenName(e)`.
- If `e` is a nested collection (List, Set, Map, Record, Tuple, or Range), `elementTerm(e)` MUST be the head IRI of the nested collection's graph. Let `nestedAnchor = listNodeIri(collectionAnchor, i) + "/__value"`, where `i` is the position of the element in the parent collection. For nested List, Set, Map, Record, or Tuple collections, the nested collection anchor is `nestedAnchor` and the list head IRI is `nestedAnchor + "/0"`. For a nested Range, the range IRI is `nestedAnchor` directly. The nested collection graph MUST be emitted following the same rules defined in this section.
- Otherwise, `elementTerm(e)` MUST be the typed literal `valueLex(e)^^valueDatatypeIri(e)`, using the scalar rules defined in §9.7.8.

This rule replaces the typed-literal representation for collection values. A collection value on a trait MUST always produce a collection graph; it MUST NOT produce a typed literal.

#### 9.7.9 Content

If a concept instance is in content mode, the mapping MUST emit:

- `(nodeIri(C), codex:content, contentText)`

`contentText` MUST be an `xsd:string` literal containing the concept's content after applying the Codex content escaping rules.

#### 9.7.10 Deterministic Predicate IRIs

Trait predicate IRIs MUST be derived as follows.

For a trait name `t`:

- If the governing schema contains exactly one `TraitDefinition` for `t`, `traitPredicateIri(t)` MUST be that `TraitDefinition`'s `id`.
- If an imported schema contains the `TraitDefinition` for `t` (resolved via a qualified Trait name in the governing schema's `ConceptDefinition`), `traitPredicateIri(t)` MUST be the imported schema's `TraitDefinition.id` for `t`.
- If the governing schema contains zero `TraitDefinition` entries for `t` (including imported schemas), validation MUST fail with a `SchemaError` (§14).
- If the governing schema contains more than one `TraitDefinition` for `t`, validation MUST fail with a `SchemaError` (§14).

Child predicate IRIs MUST be derived as follows.

Let the governing schema's `ConceptDefinition.id` for the parent concept name be `P` and for the child concept name be `Q`.

- `childPredicateIri(P,Q)` MUST be `P + "#child/" + iriHash(Q)`.

When the child Concept `Q` is from an imported schema (referenced via a qualified Concept name per §4.1.1), `Q` MUST be the `ConceptDefinition.id` from the imported schema. The child predicate IRI derivation MUST use the imported schema's `ConceptDefinition.id`.

#### 9.7.11 RDF Types

Each Concept instance MUST emit an RDF type triple:

- `(nodeIri(C), rdf:type, conceptClassIri(C.name))`

`conceptClassIri(X)` MUST be the `ConceptDefinition.id` for concept name `X` in the governing schema, or in the imported schema if `X` is a qualified Concept name (§4.1.1).

If `conceptClassIri(X)` cannot be resolved to exactly one `ConceptDefinition`, schema-driven validation MUST fail with a `SchemaError` (§14).

#### 9.7.12 Conformance Graph (`G₁`)

For a Codex instance document processed under a governing schema and an explicit `documentBaseIri`, let `G₁` be the RDF instance graph produced by the Codex→RDF instance graph mapping defined in §9.7.

A conforming implementation MUST emit `G₁` in the Codex `RdfGraph` form defined in §9.6.1 and MUST apply the canonical ordering and duplicate-removal rules defined in §9.6.2.

### 9.8 Lookup Token Resolution

#### 9.8.1 Resolution Table

Each Concept in the document that declares both a `key` trait (§6.3) and an `id` trait (§6.2) contributes one entry to the resolution table. Each entry consists of a `tokenLiteral` (the `key` lookup token value) and a `targetIri` (the `id` IRI value).

The resolution table MUST be constructed solely from explicit `key` and `id` trait declarations. Resolution entries MUST NOT be inferred, synthesized, or imported implicitly.

#### 9.8.2 Resolution Semantics

When lookup token resolution is required by schema validation:

* A lookup token MUST resolve to exactly one identifier in the resolution table.
* If no matching entry is found for a required lookup token, validation MUST fail with a `ReferenceError` (§14).

Lookup token resolution is declarative only and MUST NOT imply loading, dereferencing, or execution.

#### 9.8.3 Schema Interaction

A governing schema MUST specify, for each context where lookup token values are permitted, one of the following resolution requirements:

* The lookup token MUST be resolvable.
* The lookup token MUST NOT appear in the context.
* The lookup token MUST pass through without resolution.

### 9.9 Deterministic Projection to Derived Validation Artifacts

Derived validation artifacts MUST be generated deterministically.

Any derived validation artifact MUST be a pure function of:

- the governing schema
- the explicitly required external inputs (§9.1)

Derived validation artifact generation MUST fail with a `SchemaError` (§14) if any of the following hold:

- the governing schema is not valid under the schema-of-schemas
- any `ConceptDefinition` lacks an `id`
- any required selector (concept name, trait name) cannot be resolved to a unique definition
- any schema rule produces a semantic constraint that cannot be expressed under the chosen Codex→RDF instance graph mapping
- any generic trait mechanism (`TraitRules`, `TraitPath`, `TraitExists`, `TraitMissing`, `TraitEquals`) targets the `id` trait (see §9.7.8)

Derived validation artifacts MUST be expressed as SHACL, including SHACL-SPARQL constraints.

A derived SHACL artifact MUST apply each constraint to the target node shape(s) determined as follows:

- For `TargetConcept conceptSelector="X"`, the constraint MUST be applied to the node shape derived from the `ConceptDefinition` whose `name` is `X`.
- For `TargetContext contextSelector="Document"`, the constraint MUST be applied to a special node shape with IRI `schemaIri + "#shape/Document"` and MUST include at least:
	- `(schemaIri + "#shape/Document", rdf:type, sh:NodeShape)`
	- `(schemaIri + "#shape/Document", sh:targetNode, documentBaseIri)`
	If `documentBaseIri` is not available as an external input, derived validation artifact generation MUST fail with a `SchemaError` (§14).
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

If a derived validation artifact expresses any constraint using SHACL-SPARQL, the `sh:select` text MUST be a SPARQL 1.1 `SELECT` query that returns one row per violating focus node using the SHACL-SPARQL convention:

- the focus node variable MUST be `?this`
- a row returned by the query MUST indicate a violation

SPARQL text in derived artifacts MUST be canonically formatted. Internal SPARQL variables introduced during constraint translation MUST be allocated as follows:

- Walk the constraint's rule tree in pre-order.
- For the `$k$`-th visited node (1-indexed), allocate a node-local suffix `$k$`.
- Any internal variable introduced while translating that node MUST append suffix `$k$` to a base name.
- Variables introduced for one rule node MUST NOT be referenced outside the `EXISTS { ... }` block created for that node.

#### 9.9.1 Enumerated Value Sets (`sh:in`)

A derived SHACL artifact encoding an enumerated value-set constraint MUST emit a triple `(PS, sh:in, listHead)` on the property shape `PS`.

The list encoding MUST conform to §9.6.3.

#### 9.9.2 Pattern Constraints (`sh:pattern`, `sh:flags`)

A derived SHACL artifact encoding a pattern constraint MUST emit a triple `(PS, sh:pattern, p)` on the property shape `PS`.

When `flags` is present and non-empty, the artifact MUST also emit a triple `(PS, sh:flags, f)`.

The `pattern` and `flags` semantics MUST be SPARQL 1.1 `REGEX` semantics (see §9.5.1).

#### 9.9.3 SHACL Core Value Constraints

A derived SHACL artifact encoding a value-length constraint on a property shape `PS` MUST emit:

- `(PS, sh:minLength, "a"^^xsd:integer)` when a minimum length `a` is present
- `(PS, sh:maxLength, "b"^^xsd:integer)` when a maximum length `b` is present

A derived SHACL artifact encoding a non-empty constraint on a property shape `PS` MUST emit:

- `(PS, sh:minLength, "1"^^xsd:integer)`

A derived SHACL artifact encoding a numeric-range constraint on a property shape `PS` MUST use SHACL Core numeric bounds. The active value datatype MUST be `xsd:integer`; any other active datatype is a `SchemaError` (§14).

The artifact MUST emit:

- `(PS, sh:minInclusive, "u"^^xsd:integer)` when a minimum value `u` is present
- `(PS, sh:maxInclusive, "v"^^xsd:integer)` when a maximum value `v` is present

#### 9.9.4 Child Constraints

For child constraints projected onto a property shape `PS`, let `P` be the concept class IRI (RDF class) targeted by the owning node shape.

A derived SHACL artifact encoding a required-child constraint for a child concept selector `X` on a property shape `PS` MUST emit:

- `(PS, sh:path, childPredicateIri(P, conceptClassIri(X)))`
- `(PS, sh:minCount, "1"^^xsd:integer)`
- `(PS, sh:class, conceptClassIri(X))`

A derived SHACL artifact encoding a forbidden-child constraint for a child concept selector `X` on a property shape `PS` MUST emit:

- `(PS, sh:path, childPredicateIri(P, conceptClassIri(X)))`
- `(PS, sh:maxCount, "0"^^xsd:integer)`

An allowed-without-required child relationship MUST NOT produce a constraint in the derived SHACL artifact.

#### 9.9.5 Content Constraints

For content constraints, let `S` be the owning node shape. The property shape IRI MUST be `PS = predicatePropertyShapeIri(S, codex:content)`.

A derived SHACL artifact encoding a content-required constraint MUST emit:

- `(PS, sh:path, codex:content)`
- `(PS, sh:minLength, "1"^^xsd:integer)`

A derived SHACL artifact encoding a content pattern constraint MUST emit:

- `(PS, sh:path, codex:content)`
- `(PS, sh:pattern, p)`

When `flags` is present and non-empty, the artifact MUST also emit `(PS, sh:flags, f)`.

The `pattern` and `flags` semantics MUST be SPARQL 1.1 `REGEX` semantics (see §9.5.1).

#### 9.9.6 Identity Constraints

For identity constraints, let `S` be the owning node shape. The property shape IRI MUST be `PS = predicatePropertyShapeIri(S, codex:isEntity)`.

A derived SHACL artifact encoding an identity constraint requiring an entity MUST emit:

- `(PS, sh:path, codex:isEntity)`
- `(PS, sh:hasValue, "true"^^xsd:boolean)`

A derived SHACL artifact encoding an identity constraint requiring a non-entity MUST emit:

- `(PS, sh:path, codex:isEntity)`
- `(PS, sh:hasValue, "false"^^xsd:boolean)`

Derived validation artifacts MUST support `IdentityConstraint(type=IdentifierUniqueness, scope=S)`.

The `scope` trait MUST be present. For derived artifact purposes, `IdentityConstraint(type=IdentifierUniqueness, scope=S)` MUST be treated as `UniqueConstraint(trait=id, scope=S)` and MUST follow §9.9.7.

Derived validation artifacts MUST support `IdentityConstraint(type=IdentifierForm, pattern=p, flags=f)`.

This constraint MUST be expressed using SHACL-SPARQL.
It MUST report a violation if the focus node is an Entity and either:

* it has no `codex:declaredId`, or
* `STR(codex:declaredId)` does not match `p` under SPARQL 1.1 `REGEX` semantics (using flags `f` if present).

The SHACL-SPARQL constraint MUST use the following boolean condition:

```
EXISTS {
	focusVar codex:declaredId ?idK .
	FILTER(
		REGEX(STR(?idK), p, f)
	)
}
```

where `p` is the required pattern and `f` is the flags text if present. When `flags` is absent, the generated constraint MUST use the 2-argument `REGEX(text, pattern)` form.

#### 9.9.7 Uniqueness Constraints

Derived validation artifacts MUST support the `UniqueConstraint` constraint (§11.9.4).

When a uniqueness constraint refers to `t = id`, it MUST refer to the declared identifier as represented by `codex:declaredId`.

For nearest-scope uniqueness, `UniqueConstraint(trait=t, scope=S)` MUST mean:

- within the nearest ancestor (including self) of concept type `S`, no two nodes share the same value for trait `t`.

For purposes of this constraint, the nearest scope node is the unique node `scopeK` such that:

- `focusVar <codex:parentNode>* scopeK`
- `scopeK rdf:type <conceptClassIri(S)>`
- and there is no other node `midK` where:
	- `focusVar <codex:parentNode>* midK`
	- `midK rdf:type <conceptClassIri(S)>`
	- `midK <codex:parentNode>+ scopeK`
	- `midK != scopeK`

Derived validation artifact generation MUST fail with a `SchemaError` (§14) if no nearest scope node exists.

Derived validation artifacts MUST also enforce the document-wide uniqueness invariants for `id` (§6.2.2) and `key` (§6.3.2). Within a single document, two nodes MUST NOT share the same value for `codex:declaredId`, and two nodes MUST NOT share the same `key` trait value.

#### 9.9.8 Context Constraints

Derived validation artifacts MUST express `ContextConstraint(type=OnlyValidUnderParent)`.

The `contextSelector` trait MUST NOT be present. The SHACL-SPARQL constraint MUST use the following boolean condition:

```
EXISTS {
	focusVar <codex:parentNode> ?pK .
	?pK rdf:type <conceptClassIri(TargetContext)> .
}
```

Derived validation artifacts MUST express `ContextConstraint(type=OnlyValidUnderContext, contextSelector=A)`.

The `contextSelector` trait MUST be present. The SHACL-SPARQL constraint MUST use the following boolean condition:

```
EXISTS {
	focusVar <codex:parentNode>+ ?aK .
	?aK rdf:type <conceptClassIri(A)> .
}
```

#### 9.9.9 Reference Constraints (Reference Trait Predicates)

The set of reference-trait predicates MUST be exactly:

- `traitPredicateIri("reference")`
- `traitPredicateIri("target")`
- `traitPredicateIri("for")`

Derived validation artifacts MUST support `ReferenceConstraint(type=ReferenceSingleton)`. The constraint MUST report a violation when more than one reference-trait predicate is present on the same focus node.

Derived validation artifacts MUST support `ReferenceConstraint(type=ReferenceTraitAllowed)`. The constraint MUST provide a `traitName` trait whose value is one of `reference`, `target`, or `for`; a missing or invalid `traitName` is a `SchemaError` (§14).

#### 9.9.10 Reference Constraints (Deterministic Resolution and Targets)

For the purposes of reference constraints, a reference value `v` MUST be one of:

- an IRI (RDF IRI term), or
- a Lookup Token typed literal with datatype `urn:cdx:value-type:LookupToken`.

Given a reference value `v`, its resolved IRI `r` MUST be computed as follows:

- If `v` is an IRI, then `r = v`.
- If `v` is a Lookup Token typed literal, then:
	- If there exists exactly one entry in the resolution table (§9.8) such that the entry's `tokenLiteral` is `v`, and the entry's `targetIri` is `r`, then `r` is that `targetIri`.
	- Otherwise, `v` MUST be treated as unresolved.
- Otherwise, `v` MUST be treated as unresolved.

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

The projection of a derived validation artifact to a concrete RDF syntax MUST be exactly:

1. Check the derived `RdfGraph` against the derived-artifact structural rules.
2. Emit the triples in the chosen RDF concrete syntax.

### 9.10 Failure Rules (No Guessing)

Schema processing, schema-driven validation, instance-graph mapping, and derived-artifact projection MUST fail with an appropriate error rather than guess when required information is missing or ambiguous.

Processing MUST fail in any of the following cases:

- the schema authoring mode is missing, invalid, or mixed (see §9.4) — `SchemaError`
- a schema rule requires semantics not explicitly defined by this specification, the governing schema, or the schema-definition specification — `SchemaError`
- a required external input is missing — `SchemaError`
- an algorithm would require nondeterministic choice (including heuristic inference or "best effort") — `SchemaError`
- a lookup token is required to resolve but no Concept with a matching `key` is found — `ReferenceError`
- a derived validation artifact cannot be constructed without inventing missing definitions — `SchemaError`

### 9.11 Simplified Authoring Mode → Canonical Representation Expansion Algorithm (Total)

#### 9.11.1 Inputs and Output

Input: a Simplified Authoring Mode schema document `S`.

Output: a Canonical Representation `RdfGraph` containing a SHACL graph.

#### 9.11.2 Preconditions

The expansion MUST fail with a `SchemaError` (§14) if any precondition defined in §9.9 is violated.

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

For each trait rule attached to a concept definition with node shape IRI `NS`, let `t` be the trait name.

The expansion MUST emit one SHACL property shape node `PS` with:

- `(NS, sh:property, PS)`
- `(PS, rdf:type, sh:PropertyShape)`
- `(PS, sh:path, traitPredicateIri(t))`

`PS` MUST be `propertyShapeIri(NS, t)`.

Cardinality mapping:

- `RequiresTrait` MUST emit `(PS, sh:minCount, "1"^^xsd:integer)`.
- `ForbidsTrait` MUST emit `(PS, sh:maxCount, "0"^^xsd:integer)`.

Value type mapping:

- When a value type token maps to an RDF datatype IRI, the expansion MUST emit `(PS, sh:datatype, datatypeIri)`.
- When a value type token constrains by enumerated set, the expansion MUST emit `(PS, sh:in, listNodeIri)` and MUST emit the RDF list structure using deterministic skolem IRIs (see §9.6.3).

Any value-type token without a defined mapping MUST cause expansion failure with a `SchemaError` (§14).

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

When the child relationship restricts child type, the expansion MUST emit `(PS, sh:class, Q)`.

#### 9.11.6 ConstraintDefinitions → SHACL Constraints

ConstraintDefinitions MUST expand to SHACL constraints.

##### 9.11.6.1 General Rule

Each Codex constraint type defined by the schema-definition specification MUST map to either:

- a SHACL Core constraint expression, or
- a SHACL-SPARQL constraint (`sh:sparql`).

If a constraint type cannot be expressed without inventing semantics not defined by this specification and the schema-definition specification, expansion MUST fail with a `SchemaError` (§14).

Atomic constraint mappings that are defined by this specification MUST follow §9.9.

##### 9.11.6.2 Rule Algebra → SHACL-SPARQL (Total)

The rule algebra elements are `AllOf`, `AnyOf`, `Not`, and `ConditionalConstraint` (`When` / `Then`).

If the rule algebra tree contains an atomic constraint whose required mapping is undefined, expansion MUST fail with a `SchemaError` (§14).

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

The target binding MUST be:

- For a concept target with concept name `X`: `?this rdf:type <conceptClassIri(X)> .`
- For `TargetContext contextSelector="Document"`: `FILTER( ?this = <documentBaseIri> ) .`

`<documentBaseIri>` denotes the IRI term whose value is the required external input `documentBaseIri`.

If target binding cannot be expressed without ambiguity (for example, the target selector is not resolvable), expansion MUST fail with a `SchemaError` (§14).

`<HOLD_EXPR>` MUST be computed by the function `H(rule, ctx, focusVar)` defined below, with `focusVar` set to `?this`.

###### 9.11.6.2.2 Deterministic Variable Allocation

Expansion MUST allocate internal variable names deterministically.

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

###### 9.11.6.2.4 Atomic Rules as `EXISTS` Blocks

If `rule` is atomic, `H(rule, ctx, focusVar)` MUST be a SPARQL `EXISTS { ... }` form or an `EXISTS`-free boolean constant.

For atomic rules whose SHACL Core mapping is defined in §9.9, expansion MUST define `H(rule, ctx, focusVar)` using only SPARQL 1.1 constructs.

If an atomic rule cannot be expressed as a SPARQL boolean expression without inventing additional semantics, expansion MUST fail with a `SchemaError` (§14).

For atomic rules mapped in §9.9, the `H` translation MUST be:

- `TraitExists(trait=t)`: `EXISTS { focusVar <traitPredicateIri(t)> ?vK }`
- `TraitMissing(trait=t)`: `!EXISTS { focusVar <traitPredicateIri(t)> ?vK }`
- `TraitEquals(trait=t, value=v)`: `EXISTS { focusVar <traitPredicateIri(t)> <valueTerm(v)> }`

Here `?vK` MUST follow the deterministic variable allocation rule in §9.11.6.2.2.

If `value` in a `TraitEquals` rule is a collection value (List, Set, Map, Record, Tuple, or Range), derived validation artifact generation MUST fail with a `SchemaError` (§14). Collection equality is not expressible as a single-triple SPARQL pattern.

###### 9.11.6.2.5 One-Way Representation Rule

When a `ConstraintDefinition` uses rule algebra (i.e., contains `AllOf`, `AnyOf`, `Not`, or `ConditionalConstraint` anywhere in its rule tree), expansion MUST express that constraint definition using SHACL-SPARQL only.

Expansion MUST NOT additionally emit independent SHACL Core constraints for the same `ConstraintDefinition`.

##### 9.11.6.3 Paths and Quantifiers → SHACL-SPARQL (Total)

The path operators (`TraitPath`, `ChildPath`, `DescendantPath`, `ContentPath`) and quantifier operators (`OnPathExists`, `OnPathForAll`, `OnPathCount`) MUST be expressed using SHACL-SPARQL.

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

If `conceptSelector` cannot be resolved to a unique `ConceptDefinition`, expansion MUST fail with a `SchemaError` (§14).

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

If both `minCount` and `maxCount` are absent, expansion MUST fail with a `SchemaError` (§14).

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
* Other bindings or filters MUST NOT intervene between the subquery and its associated `FILTER`.

##### 9.11.6.4 SPARQL Constraint Shape

When a constraint is expressed using SHACL-SPARQL, the expansion MUST emit:

Let `targetShapeIri` be the node shape IRI the constraint is applied to. Let `C` be the `ConstraintDefinition`'s `id` value.

- `(targetShapeIri, sh:sparql, sparqlConstraintIri(targetShapeIri, C))`
- `(sparqlConstraintIri(targetShapeIri, C), sh:select, selectTextLiteral)`

`sparqlConstraintIri` MUST be computed according to §9.6.9.

When the source constraint has a `title` or `description`, the expansion MUST emit `sh:message`.

The SPARQL query MUST be deterministic given the source constraint.

##### 9.11.6.5 Pattern Constraints (SPARQL 1.1 REGEX)

For the pattern-bearing constraints (`ValueMatchesPattern`, `PatternConstraint`, `ContentMatchesPattern`), the expansion MUST use SPARQL 1.1 `REGEX` semantics.

If `flags` is present, it MUST be projected to `sh:flags` when using `sh:pattern`, and it MUST be passed as the third argument to `REGEX` when using `sh:sparql`.

##### 9.11.6.6 `ValueIsValid` via Explicit `ValidatorDefinition`

For `ValueIsValid validatorName=$X`, expansion MUST:

1. Resolve `$X` to exactly one `ValidatorDefinition` in the schema.
2. Embed the `ValidatorDefinition` content into a SHACL-SPARQL constraint.

The embedding contract MUST be:

- The validator content MUST be a SPARQL `SELECT` query text whose results follow the SHACL-SPARQL convention (returning a row per violation with `?this`).

The derived `sh:select` text MUST be exactly the validator content.

---

## 10. Formatting and Canonicalization

### 10.1 Processing Phases

Conforming implementations MUST support two pipelines:

1. Schema-less formatting / well-formedness check (§2.5) (no schema required)
2. Semantic validation (§2.5) (schema required)

Formatting and canonicalization MUST be performed in the full pipeline.

#### 10.1.1 Schema-Less Formatting Mode (Required)
An implementation MUST provide a schema-less formatting / canonicalization mode that can be run without a governing schema.

A schema-less formatter:

- MUST NOT claim that its output is valid under any schema
- MUST NOT report schema/semantic error classes (e.g., `SchemaError`, `IdentityError`, `ReferenceError`, `ConstraintError`)
- MUST normalize encoding and line endings as defined by the surface form requirements (§8)
- MUST apply the canonical form requirement defined in §10.3
- MUST normalize whitespace, blank-line layout, trait layout, and annotation whitespace

##### 10.1.1.1 Schema-less Content Mode Determination
In schema-less formatting and canonicalization mode, the parser MUST determine a Concept instance’s body mode mechanically as follows:

* Let the body lines be the lines between the Concept instance's opening marker and its matching closing marker (or empty for a self-closing marker).
* Ignore blank lines.
* Consider only lines at exactly one nesting level deeper than the enclosing Concept instance after indentation normalization.

The body MUST be classified according to the following rules:

* If there are no non-blank body lines, the body MUST be treated as children mode.
* If any non-blank considered line begins with `<` (Concept marker) or `[` (annotation), the body MUST be treated as children mode.
* Otherwise, the body MUST be treated as content mode.

Lines beginning with the escape sequences `\<` or `\[` are content, not structural markers.

If the body is classified as children mode but contains any non-blank considered line that is neither a valid Concept marker line (§8.5) nor a valid annotation line (§8.9), the document MUST be rejected with a `ParseError` (§14).

When subsequent schema-based validation determines that the mechanically determined body mode is not authorized for the Concept, validation MUST fail with a `SchemaError` (§14).

#### 10.1.2 Full Validation Pipeline
To validate a document under a schema, a conforming tool MUST follow this sequence:

1. Decode + newline normalization
2. Formatting + canonicalization (mandatory) — using the schema-less mode defined in §10.1.1
3. Schema resolution — obtain the governing schema for the document (§12)
4. Semantic validation — schema rule evaluation (constraints, value types, identity, references)

### 10.2 Parse Errors vs Formatting Errors
#### 10.2.1 Parse Errors

During formatting + canonicalization, a failure MUST be classified as `ParseError` (§14) when input cannot be read into the syntactic structure required to produce a parsed document model (AST) as defined by the Codex surface form.

#### 10.2.2 Formatting Errors

During formatting + canonicalization, a failure MUST be classified as `FormattingError` (§14) when input can be structurally read, but cannot be transformed into canonical surface form deterministically.

### 10.3 Canonical Form Requirement
Every valid Codex document MUST normalize to exactly one canonical textual form.

When canonicalization cannot be performed unambiguously, the document MUST be rejected with a `FormattingError` (§14). Formatting errors MUST NOT be downgraded to warnings.

### 10.4 Canonicalization Rules
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
- canonical grouping-annotation label whitespace normalization
- canonical Text Value escaping and formatting (§10.4.2)
- canonical Value literal formatting (exactly one space MUST follow each comma separator; all other optional whitespace MUST be removed; mandatory whitespace required by a specific production MUST be preserved; case-insensitive components MUST be normalized to their canonical case as defined by each value type in §5)
- alphabetical ordering of Traits by Trait name
- preservation of Concept and Content order
- canonical `RdfTriple` ordering within `RdfGraph` (§9.6.2)
- content indentation normalization (§8.8.3)

**Phase 2 (schema-directed)** applies during schema-directed processing:

- content whitespace mode normalization per `whitespaceMode` declaration (§8.8.4)
- deterministic sorting of children in `$Unordered` collections (§10.4.1)
- namespace label normalization: the `namespace` trait on each `SchemaImport` MUST be normalized to the imported schema's declared `namespace` value (§11.2.1)
- `SchemaImport` ordering: within a `SchemaImports` block, `SchemaImport` children MUST be sorted alphabetically by their canonical `namespace` value (lexicographic ascending)

Schema-less processing MUST complete Phase 1 only. Schema-directed processing MUST complete both phases.

Canonicalization MUST NOT:

- reorder Concepts (except children of `$Unordered` collections during Phase 2, and `RdfTriple` children within `RdfGraph` per §9.6.2)
- invent or remove Concepts, Traits, or Content

#### 10.4.1 Deterministic Ordering for Unordered Collections

In canonical surface form, children of an `$Unordered` collection MUST be sorted according to the following deterministic algorithm:

1. Sort by Concept name (lexicographic, case-sensitive, ascending).
2. If Concept names are equal, sort by `id` trait value (lexicographic, ascending) if present.
3. If Concept names are equal and neither child has an `id` trait, sort by `key` trait value (lexicographic, ascending) if present.
4. If still tied, preserve source order.

#### 10.4.2 Canonical Text Value Formatting
Text Values have a single semantic value after whitespace normalization (§5.1). Canonical surface form MUST be chosen deterministically as follows.

Let `t` be the normalized Text Value (after escape interpretation and whitespace normalization).

1. Form the canonical quoted spelling `q` for `t` by escaping `\` as `\\` and `"` as `\"`. No other escapes are permitted in quoted Text Values.
2. If rendering the trait as `<trait>=q` on a single line would result in a line length of at most 100 columns, the Text Value MUST be rendered using the quoted spelling `q`.
3. Otherwise, the Text Value MUST be rendered as a backtick block:

Line length for this decision is measured after applying canonical indentation; a tab counts as 2 columns.

Canonical backtick blocks are always multi-line: the opening and closing backticks MUST appear on their own lines.

- The trait MUST appear on its own line.
- The opening backtick appears immediately after `=` on the trait line, and the line ends there.
- The closing backtick appears on its own line at the trait indentation level.
- The normalized text `t` MUST be wrapped into lines by breaking at spaces. Each line (including indentation) MUST be at most 100 columns, counting tabs as 2 columns. If a single word exceeds 100 columns, it MUST appear on its own line without splitting.
- Each content line is indented one tab deeper than the trait line.
- Within backtick blocks, a literal backtick in `t` MUST be escaped as `` \` ``. No other escapes are permitted.

Line breaks introduced by backtick block wrapping are surface-form only; they are not part of the Text Value.

### 10.5 Annotation Canonicalization
Annotation canonicalization MUST follow the surface form requirements (§8).

- Inline annotations collapse internal whitespace to single spaces and trim leading/trailing whitespace (§8)
- Block annotations preserve internal line structure
- Block annotations with `CODE:` or `MARKDOWN:` directives are byte-preserving: tools MUST NOT reindent, trim, strip trailing whitespace, wrap, or interpret escapes within those blocks

When attachment cannot be determined deterministically, canonicalization MUST fail with a `FormattingError` (§14).

### 10.6 Allowed vs Forbidden Changes

Allowed changes:

- Normalize newlines to LF and ensure a trailing newline
- Normalize structural indentation (tabs) for Concept markers and children bodies
- Canonicalize trait layout/spacing and alphabetical ordering
- Canonicalize inline annotation whitespace (trim + internal collapse)
- Canonicalize grouping-annotation labels by whitespace normalization
- Normalize UUID spelling to the canonical form required by §5.8

Forbidden changes:

- Reorder Concepts (except children of `$Unordered` collections during Phase 2, and `RdfTriple` children within `RdfGraph` per §9.6.2)
- Change Content bytes (except content whitespace mode normalization during Phase 2, per §8.8.4)
- Change any bytes inside `CODE:` or `MARKDOWN:` block annotations

### 10.7 Prohibited Behaviors
Codex tools MUST NOT:

- silently normalize invalid input
- auto-correct formatting errors without reporting them
- accept multiple canonical forms
- discard or rewrite Content
- depend on source offsets or editor state

### 10.8 Reporting Requirements

Formatting error reports MUST include:

- error class (`FormattingError`)
- violated rule
- location (line number or Concept path)
- explanation of canonicalization failure

---

## 11. Schema Definition Language

### 11.1 Core Principles

* Schemas are **declarative data**, not executable programs.
* All authorization is **explicit**; nothing is implied or inferred.
* All constraints are **mechanically enforceable**.
* Schema semantics MUST be **closed-world**, **deterministic**, and **free of heuristics**.

Schema validation, schema expansion, and derived-artifact generation MUST satisfy the schema-first requirements defined in §9.

---

### 11.2 Schema

A `Schema` Concept defines a governing Codex schema.

#### Traits
A `Schema` Concept MUST declare the following Traits:

* `id` (required; IRI Reference Value)
  The globally unique identifier for the schema. This value is used as `schemaIri` throughout schema processing, instance-graph mapping, and derived-artifact generation.

* `version` (required; Text Value)

  A schema version identifier whose ordering is defined by `versionScheme`.

* `versionScheme` (required; Enumerated Token Value)

  Declares the version comparison scheme used to order schema versions within the schema lineage. Allowed values and comparison rules are defined in §13.4.

* `authoringMode` (required; Enumerated Token Value)

  Declares the authoring mode for the schema. See §9.4.

* `compatibilityClass` (required; Enumerated Token Value)
  One of:

  * `$Initial`
  * `$BackwardCompatible`
  * `$ForwardCompatible`
  * `$Breaking`

* `namespace` (required; Text Value)

  The canonical namespace label for this schema. The value MUST be a camelCase name (§4.1). This label is used by importing documents to construct qualified names (§4.1.1) that reference Concept and Trait definitions from this schema. Each schema's `namespace` value MUST be unique among all schemas loaded together (governing schema plus imported schemas); if two schemas declare the same `namespace` value, processing MUST fail with a `SchemaError` (§14).

A `Schema` Concept is allowed to declare the following Traits:

* `key` (Lookup Token Value)
* `title` (Text Value)
* `description` (Text Value)

#### Children
A `Schema` MUST satisfy the mode-conditional child-Concept rules defined in §9.4.

For `authoringMode=$SimplifiedMode`:

* A `Schema` MUST contain exactly one `ConceptDefinitions` child Concept.
* The following child Concepts are allowed, in any order:

  * `TraitDefinitions`
  * `EnumeratedValueSets`
  * `ConstraintDefinitions`
  * `ValueTypeDefinitions`
  * `ValidatorDefinitions`
  * `SchemaImports` (see §11.2.1)

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

* A `Schema` in `$CanonicalMode` is allowed to contain a `SchemaImports` child Concept. The parser MUST merge imported SHACL shapes at the RDF level.

No other child Concepts are allowed.

#### Semantic Requirements

* Any schema whose structure or semantics cannot be interpreted deterministically under this specification MUST be rejected with a `SchemaError` (§14).

---

### 11.2.1 Schema Imports

#### `SchemaImports`

`SchemaImports` is a language-level child Concept allowed on any root Concept in children mode, regardless of the governing schema's child rules.

`SchemaImports` MUST only appear as a direct child of a root Concept.

A root Concept MUST NOT contain more than one `SchemaImports` child.

If `SchemaImports` appears on a non-root Concept, the document MUST be rejected with a `ParseError` (§14).

`SchemaImports` contains one or more `SchemaImport` children.

`SchemaImports` has no Traits.

##### Canonical Ordering

Within a `SchemaImports` block, `SchemaImport` children MUST be sorted alphabetically by their canonical `namespace` value (lexicographic ascending) in canonical form.

#### `SchemaImport`

##### Traits

* `reference` (required; IRI Reference Value)

  The IRI of the imported schema. This MUST be the `Schema.id` of an imported schema provided via the `importedSchemas` input (§12.2). The value MUST be an IRI Reference Value.

* `namespace` (required; Text Value)

  The namespace label used in qualified names (§4.1.1) to reference Concepts and Traits from this imported schema. The value MUST be a camelCase name (§4.1). In canonical form, this value MUST be normalized to the imported schema's declared `namespace` Trait value (§10.4).

##### Semantic Requirements

* The `reference` IRI MUST appear as a key in the `importedSchemas` map provided to `validate()` (§12.2). If the IRI is not present in `importedSchemas`, processing MUST fail with a `SchemaError` (§14).
* After namespace label normalization, all `SchemaImport` entries within a `SchemaImports` block MUST have distinct canonical `namespace` values. If two entries produce the same canonical namespace label, processing MUST fail with a `SchemaError` (§14).
* A qualified name using a namespace label MUST resolve to a Concept or Trait definition within the corresponding imported schema. If the qualified name references a Concept or Trait not defined in the imported schema, processing MUST fail with a `SchemaError` (§14).

#### Governing Schema as Default Namespace

In data documents, the governing schema's Concept and Trait definitions are referenced without namespace qualification. Only Concepts from imported schemas require qualification via `namespace:ConceptName` (§4.1.1).

Trait names on Concept instances in data documents MUST be unqualified. The Concept definition (from the governing schema or the imported schema that defines the Concept) determines which `TraitDefinition` each Trait name refers to.

Enumerated Tokens (`$Value`) and Lookup Tokens (`~key`) MUST NOT be namespace-qualified. The Trait's constraint determines the `EnumeratedValueSet`; the document's resolution table (§9.8) resolves Lookup Tokens.

#### Namespace Qualification in Schema Documents

In schema documents, references to Concepts and Traits from imported schemas in meta-language constructs (`RequiresTrait`, `AllowsTrait`, `AllowsChildConcept`, `RequiresChildConcept`, `ForbidsChildConcept`, `ForbidsTrait`, `conceptSelector`, etc.) MUST use qualified names (`namespace:name`). Local definitions MUST be unqualified.

#### Data Documents with Imports

Data documents are allowed to declare `SchemaImports` as a child of their root Concept.

The `SchemaImports` in a data document MUST be consistent with the governing schema: any schema imported by the data document MUST also be imported by the governing schema (or be the governing schema itself).

---

### 11.3 Concept Definitions

#### 11.3.1 `ConceptDefinition`

A `ConceptDefinition` is an Entity.

##### Required Traits
* `id` (IRI Reference Value)
* `name` (Concept name, per §4 Naming Rules)
* `conceptKind` (`$Semantic | $Structural | $ValueLike`)
* `entityEligibility` (`$MustBeEntity | $MustNotBeEntity`)

##### Allowed Traits
* `key` (Lookup Token Value)
* `description` (Text Value)
* `role` (Text Value)

##### Children
A `ConceptDefinition` is allowed to contain, in any order:

* `ContentRules`
* `TraitRules`
* `ChildRules`
* `CollectionRules`

No other children are allowed.

When a child section is omitted, its default behavior applies as defined below.

---

#### 11.3.2 `ContentRules`

`ContentRules` declares whether instances of the Concept are in content mode or children mode.

##### Children
Exactly one of:

* `AllowsContent` — instances are in content mode
* `ForbidsContent` — instances are in children mode

###### `AllowsContent`

Traits:

* `whitespaceMode` (required; Enumerated Token Value)

`whitespaceMode` MUST be one of:

* `$Preformatted` — content whitespace is significant and MUST be preserved exactly
* `$Flow` — content whitespace is not significant; Codex-conforming tools MUST collapse runs of whitespace to single spaces and trim leading/trailing whitespace

###### `ForbidsContent`

`ForbidsContent` has no traits.

##### Defaults

When `ContentRules` is omitted, `ForbidsContent` applies.

---

#### 11.3.3 `TraitRules`

`TraitRules` declares which Traits are allowed, required, or forbidden on instances of the Concept.

##### Children
One or more of:

* `RequiresTrait`
* `AllowsTrait`
* `ForbidsTrait`

Each rule applies to exactly one trait name.

###### `RequiresTrait`

Traits:

* `name` (required; Trait name or qualified Trait name, per §4 and §4.1.1)

Children (allowed):

* `AllowedValues` — narrows the set of valid values for this trait on this concept (see below)

###### `AllowsTrait`

Traits:

* `name` (required; Trait name or qualified Trait name, per §4 and §4.1.1)

Children (allowed):

* `AllowedValues` — narrows the set of valid values for this trait on this concept (see below)

###### `ForbidsTrait`

Traits:

* `name` (required; Trait name or qualified Trait name, per §4 and §4.1.1)

###### Concept-Level `AllowedValues` Narrowing

When `AllowedValues` appears as a child of `RequiresTrait` or `AllowsTrait`, it further narrows the `AllowedValues` declared on the referenced `TraitDefinition`. The concept-level allowed values MUST be a subset of the `TraitDefinition`-level allowed values. If both exist, the concept-level constraint governs.

In the Canonical Representation, concept-level `AllowedValues` translates to an additional `sh:property` shape on the concept's NodeShape with `sh:path` equal to the trait's predicate IRI and `sh:in` equal to the concept-level allowed values list.

##### Defaults

When `TraitRules` is omitted, no Traits are allowed except:

* `id`, when allowed or required by `entityEligibility`
* `key`, when applicable by schema rules

---

#### 11.3.4 `ChildRules`

`ChildRules` declares which child Concepts are allowed, required, or forbidden beneath instances of the Concept.

##### Children
One or more of:

* `AllowsChildConcept`
* `RequiresChildConcept`
* `ForbidsChildConcept`
* `ExactlyOneChildOf`

###### `AllowsChildConcept`

Traits:

* `conceptSelector` (required; Concept name or qualified Concept name per §4.1.1)
* `min` (allowed; non-negative integer; default `0`)
* `max` (allowed; positive integer; omitted means unbounded)

###### `RequiresChildConcept`

Traits:

* `conceptSelector` (required; Concept name or qualified Concept name per §4.1.1)
* `min` (allowed; positive integer; default `1`)
* `max` (allowed; positive integer; omitted means unbounded)

###### `ForbidsChildConcept`

Traits:

* `conceptSelector` (required; Concept name or qualified Concept name per §4.1.1)

###### `ExactlyOneChildOf`

Declares that exactly one of the listed Concept types MUST appear as a child of the governed instance.

Children:

* `ConceptOption` (required; minimum 2)

No traits.

###### `ConceptOption`

Declares one option within an `ExactlyOneChildOf` group.

Traits:

* `conceptSelector` (required; Concept name or qualified Concept name per §4.1.1)

##### Defaults

When `ChildRules` is omitted, no child Concepts are allowed.

---

#### 11.3.5 `CollectionRules`

`CollectionRules` declares collection semantics for Concepts whose children form a logical collection.

##### Traits
* `ordering` (required; `$Ordered | $Unordered`)
* `allowsDuplicates` (required; boolean)

##### Form

`CollectionRules` MUST be self-closing and MUST NOT have children.

##### Applicability

When `CollectionRules` is present, child ordering and duplication semantics MUST be enforced as declared.

When `CollectionRules` is absent, no collection semantics are assumed.

##### Ordering Semantics

Ordering MUST be exactly one of:

###### `$Ordered`

A collection with `ordering=$Ordered` has semantically significant order.

Source order MUST be preserved through all conforming processing.

Two `$Ordered` collections with identical children in different orders MUST be treated as semantically distinct.

Validation and comparison of `$Ordered` collections MUST be order-sensitive.

###### `$Unordered`

A collection with `ordering=$Unordered` has no semantically significant order.

Conforming implementations MUST preserve source order during parsing and general processing.

Validation of `$Unordered` collections MUST be order-insensitive.

Semantic comparison of `$Unordered` collections MUST be order-insensitive: two `$Unordered` collections with identical children in different orders MUST be treated as semantically equivalent.

In canonical surface form, children of an `$Unordered` collection MUST be sorted according to the deterministic ordering defined in §10.4.1.

---

### 11.4. Trait Definitions

#### 11.4.1 `TraitDefinition`

A `TraitDefinition` is an Entity.

##### Required Traits
* `id` (IRI Reference Value)
* `name` (Trait name per §4 Naming Rules)
* `defaultValueType` (value type token, optionally parameterized per §5.18; required unless `defaultValueTypes` is provided)
* `defaultValueTypes` (list of one or more value type tokens, optionally parameterized per §5.18; required unless `defaultValueType` is provided)

##### Allowed Traits
* `description` (Text Value)
* `isReferenceTrait` (boolean)
* `priority` (enumerated token)

When both `defaultValueType` and `defaultValueTypes` are provided, schema processing MUST fail with a `SchemaError` (§14).

`priority` is a meta-schema concern. Implementations MUST NOT use `priority` to change validation or compilation semantics. Meta-schemas are allowed to constrain `priority` values.

##### Value Type Semantics
When a trait is present on a Concept instance, its value MUST conform to the declared value type.

When `defaultValueTypes` specifies multiple types, the value MUST conform to exactly one of the listed types.

##### Collection Type Semantics
When a trait's value type is a parameterized collection type, each element of the collection MUST conform to the declared item type.

When a trait's value type is an unparameterized collection type, elements are allowed to be of any type.

When a trait's value type is a union containing both scalar and collection types, the value MUST conform to exactly one member of the union.

##### Allowed Children

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
		<ValueIsOneOf values=[$Grams,$Kilograms,$Milliliters,$Liters,$Units] />
	</AllowedValues>
</TraitDefinition>

<TraitDefinition
	name="tags"
	defaultValueType=$List<$Text>
/>

<TraitDefinition
	name="role"
	defaultValueTypes=[$Text,$List<$Text>]
/>
```

---

#### 11.4.2 `AllowedValues`

Constrains the values a Trait accepts.

##### Children
Exactly one of:

* `ValueIsOneOf`
* `EnumeratedConstraint`

##### `ValueIsOneOf`

###### Traits

* `values` (required; list of allowed values)

##### `EnumeratedConstraint`

###### Traits

* `set` (required; name of an `EnumeratedValueSet`)

---

### 11.5 Value Types

Value type checking MUST be deterministic and MUST NOT perform implicit evaluation.

#### 11.5.1 Built-In Value Type Tokens
Schemas are allowed to reference the following built-in value type tokens.

* `$Text`
* `$Character`
* `$Boolean`
* `$Number`
* `$Integer`
* `$Zero`
* `$NegativeInteger`
* `$NonPositiveInteger`
* `$DecimalNumber`
* `$ExponentialNumber`
* `$PrecisionNumber`
* `$Fraction`
* `$ImaginaryNumber`
* `$ComplexNumber`
* `$NonNegativeInteger`
* `$PositiveInteger`
* `$PositiveInfinity`
* `$NegativeInfinity`
* `$Infinity`
* `$RealNumber`
* `$FiniteNumber`
* `$FiniteRealNumber`
* `$ExactNumber`
* `$EnumeratedToken`
* `$IriReference`
* `$LookupToken`
* `$Uuid`
* `$HostName`
* `$EmailAddress`
* `$Url`
* `$HexColor`
* `$NamedColor`
* `$RgbColor`
* `$HslColor`
* `$HwbColor`
* `$LabColor`
* `$LchColor`
* `$OklabColor`
* `$OklchColor`
* `$ColorSpaceColor`
* `$ColorSpaceColorFunction`
* `$ColorMix`
* `$DeviceCmyk`
* `$Color`
* `$PlainDate`
* `$PlainTime`
* `$PlainDateTime`
* `$PlainYearMonth`
* `$PlainMonthDay`
* `$YearWeek`
* `$Instant`
* `$ZonedDateTime`
* `$Duration`
* `$TemporalKeyword`
* `$TemporalPoint`
* `$List`
* `$Set`
* `$Map`
* `$Record`
* `$Tuple`
* `$Range`

When a schema constrains a Trait value using a built-in value type token, semantic validation MUST convert that value into the corresponding typed IR value and MUST reject values that are syntactically well-formed but semantically invalid for the expected type.

---

#### 11.5.2 `ValueTypeDefinition`

A `ValueTypeDefinition` is an Entity.

##### Container

`ValueTypeDefinitions` is a container Concept holding one or more `ValueTypeDefinition` children.

##### Required Traits
* `id` (IRI Reference Value)
* `name` (Concept name per §4 Naming Rules)
* `baseValueType` (built-in value type token)

##### Allowed Traits
* `validatorName` (Enumerated Token Value identifying a `ValidatorDefinition`)

`ValueTypeDefinition` names MUST be unique within the Schema.

When `validatorName` is present, schema-driven validation MUST apply the referenced validator as specified in §9.5.2 and §9.11.6.6.

When `validatorName` cannot be resolved to exactly one `ValidatorDefinition`, schema processing MUST fail with a `SchemaError` (§14).

A `ValueTypeDefinition` MUST NOT change the surface grammar of its `baseValueType`.

---

#### 11.5.3 Enumerated Value Sets

Schemas are allowed to define named sets of Enumerated Token Values.

##### Container

`EnumeratedValueSets` is a container Concept holding one or more `EnumeratedValueSet` children.

##### `EnumeratedValueSet`

An `EnumeratedValueSet` is an Entity.

###### Required Traits
* `id` (IRI Reference Value)
* `name` (Concept name per §4 Naming Rules)

###### Allowed Traits
* `key` (Lookup Token Value)
* `description` (Text Value)

###### Children
One or more `Member` children.

##### `Member`

###### Required Traits
* `value` (token name without `$`)

###### Allowed Traits
* `label` (Text Value)
* `description` (Text Value)

Each `value` MUST be unique within its `EnumeratedValueSet`.

---

#### 11.5.4 Built-In Enumerated Value Sets
The following enumerated value sets are defined by the Codex language itself and MUST be recognized by all conforming implementations.

##### `ConceptKind`

* `$Semantic`
* `$Structural`
* `$ValueLike`

##### `EntityEligibility`

* `$MustBeEntity`
* `$MustNotBeEntity`

##### `CompatibilityClass`

* `$Initial`
* `$BackwardCompatible`
* `$ForwardCompatible`
* `$Breaking`

##### `Ordering`

* `$Ordered`
* `$Unordered`

##### `Cardinality`

* `$Single`
* `$List`

These enumerated sets MUST NOT be redefined by schemas.

---

### 11.6 Constraint Model

#### 11.6.1 `ConstraintDefinitions`

##### Children
One or more `ConstraintDefinition` children.

The order of `ConstraintDefinition` children MUST be preserved but MUST NOT affect semantics.

---

#### 11.6.2 `ConstraintDefinition`

A `ConstraintDefinition` is itself an Entity.

##### Required Traits
* `id` (IRI Reference Value)

##### Allowed Traits
* `title` (Text Value)
* `description` (Text Value)

##### Children
Exactly two children, in any order:

* `Targets`
* `Rule`

When either child is missing or appears more than once, schema processing MUST fail with a `SchemaError` (§14).

---

#### 11.6.3 `Targets`

##### Children
One or more of:

* `TargetConcept`
* `TargetContext`

When `Targets` contains no children, schema processing MUST fail with a `SchemaError` (§14).

---

##### 11.6.3.1 `TargetConcept`

###### Traits
* `conceptSelector` (required; Concept name)

The selector MUST resolve to exactly one `ConceptDefinition`.
Otherwise, schema processing MUST fail with a `SchemaError` (§14).

---

##### 11.6.3.2 `TargetContext`

###### Traits
* `contextSelector` (required; Concept name or the literal text `"Document"`)

When `contextSelector` is not `"Document"`, it MUST resolve to exactly one `ConceptDefinition`.
Otherwise, schema processing MUST fail with a `SchemaError` (§14).

---

#### 11.6.4 `Rule`

##### Children
Exactly one child, which MUST be one of:

* a **composition rule** (§11.7)
* an **atomic constraint** (§11.9)
* a **path-scoped rule** (§11.8 with quantifier)

When `Rule` contains zero or more than one child, schema processing MUST fail with a `SchemaError` (§14).

`Rule` nodes are purely structural and MUST NOT carry Traits.

---

### 11.7 Rule Algebra

Rule algebra MUST be translatable to a total, deterministic validation form.

---

#### 11.7.1 General Rules

* Rule algebra nodes MUST NOT carry Traits.
* `AllOf`, `AnyOf`, and `Not` MUST contain only `Rule` nodes as children.
* Any rule tree MUST be finite and acyclic.

When a rule algebra structure cannot be translated deterministically, schema processing MUST fail with a `SchemaError` (§14).

---

#### 11.7.2 `AllOf`

##### Children
Two or more `Rule` children.

##### Semantics

The rule holds if and only if **every** child rule holds for the same focus node.

---

#### 11.7.3 `AnyOf`

##### Children
Two or more `Rule` children.

##### Semantics

The rule holds if and only if **one or more** child rules hold for the same focus node.

---

#### 11.7.4 `Not`

##### Children
Exactly one `Rule` child.

##### Semantics

The rule holds if and only if the child rule does **not** hold for the same focus node.

---

#### 11.7.5 `ConditionalConstraint`

##### Children
Exactly two children:

* `When` — contains exactly one `Rule` child (the condition)
* `Then` — contains exactly one `Rule` child (the consequent)

##### Semantics

The rule holds if and only if:

* the condition does **not** hold, **or**
* the condition holds and the consequent holds

---

#### 11.7.6 Determinism Requirement

Rule algebra evaluation MUST be:

* order-independent
* reducible to a single boolean outcome per focus node

When rule algebra composition cannot be evaluated deterministically, schema processing MUST fail with a `SchemaError` (§14).

---

### 11.8 Paths and Quantifiers

All path and quantifier semantics MUST be compatible with the instance-graph mapping defined in §9.7 and the rule-to-SPARQL translation defined in §9.11.

---

#### 11.8.1 Paths

Each path node MUST declare exactly the traits required for its form.

##### `TraitPath`

###### Traits
* `traitName` (required; Trait name per the Naming Rules in §4)

##### Semantics

Selects each value bound to the named Trait on the focus node.

---

##### `ChildPath`

###### Traits
* `conceptSelector` (required; Concept name)

##### Semantics

Selects each direct child of the focus node whose Concept type matches `conceptSelector`.

---

##### `DescendantPath`

###### Traits
* `conceptSelector` (required; Concept name)

##### Semantics

Selects each descendant (via one or more parent links) of the focus node whose Concept type matches `conceptSelector`.

---

##### `ContentPath`

###### Traits

None.

##### Semantics

Selects the content text if and only if the focus Concept instance is in content mode.

---

#### 11.8.2 Quantifiers

Quantifiers MUST appear only in rule nodes that explicitly bind a Path to a nested Rule (see §9.5.3).

---

##### `Exists`

###### Semantics

The rule holds if and only if there exists at least one path-selected element for which the nested rule holds.

---

##### `ForAll`

###### Semantics

The rule holds if and only if no path-selected element violates the nested rule.

---

##### `Count`

###### Allowed Traits
* `minCount` (non-negative integer)
* `maxCount` (positive integer)

At least one of `minCount` or `maxCount` MUST be present.

###### Semantics

The rule holds if and only if the number of path-selected elements that satisfy the nested rule is within the specified bounds.

---

#### 11.8.3 Determinism and Totality

* Paths MUST select a well-defined set of elements.
* Quantifiers MUST evaluate to a single boolean outcome.
* When a path selector cannot be resolved uniquely, schema processing MUST fail with a `SchemaError` (§14).
* When a quantifier cannot be evaluated without guessing, schema processing MUST fail with a `SchemaError` (§14).

Paths and quantifiers MUST NOT be evaluated outside the schema-driven validation pipeline defined in §9.

---

### 11.9 Atomic Constraints

When an atomic constraint cannot be expressed under the instance-graph mapping (§9.7) and the constraint-to-artifact rules (§9.9–§9.11), schema processing MUST fail with a `SchemaError` (§14).

---

#### 11.9.1 Trait Constraints

##### `TraitExists`

The named Trait MUST be present.

###### Traits
* `trait` (required; Trait name per §4)

---

##### `TraitMissing`

The named Trait MUST be absent.

###### Traits
* `trait` (required; Trait name per §4)

---

##### `TraitEquals`

The named Trait MUST have at least one value equal to the specified value.

###### Traits
* `trait` (required; Trait name per §4)
* `value` (required; Value)

---

##### `TraitCardinality`

###### Required Traits
* `trait` (Trait name per §4)

###### Allowed Traits
* `min` (non-negative integer)
* `max` (positive integer)

At least one of `min` or `max` MUST be present.

---

##### `TraitValueType`

###### Traits
* `trait` (required; Trait name per §4)
* `valueType` (required; value type token)

---

##### `TraitLessOrEqual`

The constraint is vacuously satisfied if either Trait is absent from the focus node.

###### Traits
* `leftTrait` (required; Trait name per §4)
* `rightTrait` (required; Trait name per §4)

###### SHACL Expansion

Produces a SHACL-SPARQL constraint that selects the focus node when the left value exceeds the right value:

```sparql
SELECT DISTINCT ?this WHERE {
  ?this <traitPredicateIri(leftTrait)> ?left .
  ?this <traitPredicateIri(rightTrait)> ?right .
  FILTER(?left > ?right)
}
```

---

#### 11.9.1 Value Constraints

##### `ValueIsOneOf`

The value MUST be one of the explicitly listed values.

###### Traits
* `values` (required; list of Values)

---

##### `ValueMatchesPattern`

The value MUST match a regular expression.

###### Traits
* `pattern` (required; regex text)

###### Allowed Traits
* `flags` (text; SPARQL 1.1 `REGEX` flags)

---

##### `PatternConstraint`

###### Required Traits
* `trait` (Trait name per §4)
* `pattern` (regex text)

###### Allowed Traits
* `flags` (text; SPARQL 1.1 `REGEX` flags)

---

##### `ValueLength`

###### Allowed Traits
* `min` (non-negative integer)
* `max` (positive integer)

At least one of `min` or `max` MUST be present.

---

##### `ValueInNumericRange`

###### Allowed Traits
* `min` (number)
* `max` (number)

At least one of `min` or `max` MUST be present.

This constraint MUST apply only to numeric value types that support ordered comparison.
When comparison semantics are not explicitly defined for the active value type, schema processing MUST fail with a `SchemaError` (§14).

---

##### `ValueIsNonEmpty`

The value MUST be present and non-empty.

This constraint applies to text-like values only.
If applied to an incompatible value type, schema processing MUST fail with a `SchemaError` (§14).

---

##### `ValueIsValid`

The value MUST satisfy a named validator.

###### Traits
* `validatorName` (required; enumerated token)

The validator MUST resolve to exactly one `ValidatorDefinition` in the governing schema.
If resolution fails, schema processing MUST fail with a `SchemaError` (§14).

---

#### 11.9.2 Child Constraints

##### `ChildConstraint`

###### Traits
* `type` (required; one of `RequiresChildConcept | AllowsChildConcept | ForbidsChildConcept`)
* `conceptSelector` (required; Concept name)

Its semantics MUST be equivalent to the corresponding explicit child-rule form defined in §11.3.4.

---

##### `ChildSatisfies`

###### Traits
* `conceptSelector` (required; Concept name)

###### Children
* Exactly one `Rule` child

The rule MUST be evaluated for each matching child Concept instance.

---

#### 11.9.3 Collection Constraints

##### `CollectionOrdering`

###### Traits
* `ordering` (required; `$Ordered | $Unordered`)

###### Children
* Exactly one of `ChildPath` or `DescendantPath` (see §9.5.4)

---

##### `CollectionAllowsEmpty`

###### Traits
* `allowed` (required; boolean)

###### Children
* Exactly one of `ChildPath` or `DescendantPath` (see §9.5.4)

---

##### `CollectionAllowsDuplicates`

###### Required Traits
* `allowed` (boolean)

###### Allowed Traits
* `keyTrait` (Trait name per §4)

When `allowed` is `false`, `keyTrait` MUST be present.

###### Children
* Exactly one of `ChildPath` or `DescendantPath` (see §9.5.4)

---

##### `MemberCount`

###### Allowed Traits
* `min` (non-negative integer)
* `max` (positive integer)

At least one of `min` or `max` MUST be present.

###### Children
* Exactly one of `ChildPath` or `DescendantPath` (see §9.5.4)

---

##### `EachMemberSatisfies`

Each collection member MUST satisfy a nested rule.

###### Children
* Exactly one of `ChildPath` or `DescendantPath` (see §9.5.4)
* Exactly one `Rule` child

The rule MUST be evaluated for each matching collection member.

---

#### 11.9.4 Uniqueness Constraints

##### `UniqueConstraint`

###### Traits
* `trait` (required; Trait name per §4)
* `scope` (required; Concept name defining the uniqueness scope)

Uniqueness semantics MUST follow the deterministic scope rules defined in §9.9.7.

---

#### 11.9.5 Order Constraints

##### `OrderConstraint`

###### Traits
* `type` (required; one of the order constraint types defined below)
* `byTrait` (required; Trait name per §4)

###### Types
* `Ascending`: Elements MUST be in ascending order by the specified trait value.
* `Descending`: Elements MUST be in descending order by the specified trait value.

###### Children
* Exactly one of `ChildPath` or `DescendantPath` (see §9.5.4)

Order constraint semantics apply to `$Ordered` collections only. When an `OrderConstraint` is applied to an `$Unordered` collection, schema processing MUST fail with a `SchemaError` (§14).

---

#### 11.9.6 Reference Constraints

##### `ReferenceConstraint`

###### Traits
* `type` (required; one of the reference constraint types defined below)

###### Types
* `ReferenceTargetsEntity`: Target MUST be an Entity. The `conceptSelector` and `traitName` traits MUST NOT be present.
* `ReferenceMustResolve`: Reference MUST resolve. The `conceptSelector` and `traitName` traits MUST NOT be present.
* `ReferenceSingleton`: At most one reference Trait MUST be present. The `conceptSelector` and `traitName` traits MUST NOT be present.
* `ReferenceTargetsConcept`: Target MUST be a specific Concept type. The `conceptSelector` trait MUST be present.
* `ReferenceTraitAllowed`: A specific reference Trait is allowed. The `traitName` trait MUST be present.

Reference constraint semantics MUST follow §9.9.9–§9.9.12 exactly.

---

#### 11.9.7 Identity Constraints

##### `IdentityConstraint`

###### Required Traits
* `type` (one of the identity constraint types defined below)

###### Types
* `MustBeEntity`: Instance MUST be an Entity. The `scope`, `pattern`, and `flags` traits MUST NOT be present.
* `MustNotBeEntity`: Instance MUST NOT be an Entity. The `scope`, `pattern`, and `flags` traits MUST NOT be present.
* `IdentifierUniqueness`: Identifiers MUST be unique within scope. The `scope` trait MUST be present. The `pattern` and `flags` traits MUST NOT be present.
* `IdentifierForm`: Identifier MUST match pattern. The `pattern` trait MUST be present. The `scope` trait MUST NOT be present.

Identity constraint semantics MUST follow the entity and identity model defined in §§3.5 and 6.

`IdentityConstraint(type=MustBeEntity)` MUST report an `IdentityError` (§14) unless the focus Concept instance is an Entity under §3.5.

`IdentityConstraint(type=MustNotBeEntity)` MUST report an `IdentityError` (§14) if the focus Concept instance declares an `id` Trait.

`IdentityConstraint(type=IdentifierUniqueness, scope=S)` constrains identifiers to be unique within the nearest enclosing scope `S`.
Its semantics MUST be identical to `UniqueConstraint(trait=id, scope=S)` as defined in §9.9.7 (where `id` refers to `codex:declaredId`).

`IdentityConstraint(type=IdentifierForm, pattern=p, flags=f)` constrains the spelling of declared identifiers.
When the focus Concept instance is an Entity, its declared `id` value MUST match the regular expression `p` under SPARQL 1.1 `REGEX` semantics (see §9.5.1).

When `pattern` is not provided for `IdentityConstraint(type=IdentifierForm)`, schema processing MUST fail with a `SchemaError` (§14).

---

#### 11.9.8 Context Constraints

##### `ContextConstraint`

###### Traits
* `type` (required; one of the context constraint types defined below)
* `contextSelector` (Concept name; see type-specific requirements below)

###### Types
* `OnlyValidUnderParent`: Requires the immediate parent is of the type specified by the `TargetContext` in this constraint's `Targets` block. The `ContextConstraint` itself MUST NOT have a `contextSelector` trait.
* `OnlyValidUnderContext`: Requires an ancestor of the specified type exists in the parent chain. The `contextSelector` trait MUST be present.

Context constraint semantics MUST follow §9.9.8.

---

#### 11.9.10 Content Constraints

##### `ContentConstraint`

###### Traits
* `type` (required; one of the content constraint types defined below)

###### Types
* `ForbidsContent`: Requires content is absent. The `pattern` and `flags` traits MUST NOT be present.
* `ContentRequired`: Requires content exists. The `pattern` and `flags` traits MUST NOT be present.
* `ContentMatchesPattern`: Requires content matches a pattern. The `pattern` trait MUST be present. The `flags` trait is allowed.

Content constraint semantics MUST follow the content model defined in §3.4 and the validation rules defined in §9.9.5.

---

### 11.10 Complete Constraint Example (Informative)

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
			type=$RequiresChildConcept
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
					type=$RequiresChildConcept
					conceptSelector="Parameters"
				/>
			</Then>
		</ConditionalConstraint>
	</Rule>
</ConstraintDefinition>
```

---

### 11.11 Relationship to External Systems

External representations are allowed to be derived from Codex schemas, subject to the following constraints:

* Any derived representation (including SHACL, SHACL-SPARQL, or OWL) MUST be a pure, deterministic projection of the Codex schema.
* Derived artifacts MUST NOT introduce semantics, defaults, inference rules, or interpretation not explicitly defined by:

  * this specification, and
  * the governing Codex schema.
* Derived artifacts MUST NOT override, weaken, or contradict Codex validation semantics.
* When a Codex constraint or rule cannot be expressed faithfully in the chosen external system, derivation MUST fail with a `SchemaError` (§14) rather than approximate.

---

## 12. Schema Loading and Bootstrapping

This section defines how schemas are associated with documents for schema-first parsing and validation.

### 12.1 Purpose

Codex is a schema-first language.

A Codex document MUST NOT be semantically validated without an explicit governing schema.

Codex permits schema-less formatting and well-formedness checks that do not require a governing schema, but such checks MUST NOT perform semantic interpretation or validation (see §9.2 and §10.1.1).

This section normatively defines how a conforming implementation obtains the governing schema for a document.

Its goals are to:

* ensure that every semantic validation operation has an explicit governing schema
* define a clear and deterministic schema resolution order
* support bootstrapping of the schema language itself via a built-in schema-of-schemas
* ensure failures are reported clearly and classified correctly when a schema is unavailable or invalid

### 12.2 Schema Provision

A conforming implementation MUST require explicit provision of a governing schema for semantic validation.

Schema-less formatting and well-formedness checks (§9.2, §10.1.1) do not require a governing schema and MUST NOT be blocked by the absence of one.

For semantic validation, the governing schema is provided directly by the caller as an explicit input:

```
validate(documentBytes, governingSchema, importedSchemas, documentBaseIri) → validatedDocument
```

`importedSchemas` is a map from schema IRIs to schema bytes. The document's `SchemaImports` declarations (§11.2.1) bind namespace labels to IRIs in this map. If a document or its governing schema declares no imports, `importedSchemas` is permitted to be empty.

`documentBaseIri` is the base IRI for instance graph mapping (§9.7). It MUST be an IRI. If `documentBaseIri` is missing, semantic validation MUST fail with a `SchemaError` (§14).

The implementation MUST use the provided schema and MUST NOT attempt to substitute, infer, or override it.

If no governing schema is provided and semantic validation is requested, the implementation MUST fail with a `SchemaError` (§14).

If the document or governing schema declares a `SchemaImport` whose `reference` IRI is not present in `importedSchemas`, the implementation MUST fail with a `SchemaError` (§14).

External systems for schema storage, discovery, or distribution do not affect the parsing, validation, or canonicalization of Codex documents and are outside the scope of this specification.

### 12.3 Bootstrap Schema-of-Schemas
Codex defines a built-in **bootstrap schema-of-schemas** used to parse and validate schema documents authored in Codex.

The bootstrap schema-of-schemas exists to eliminate circular dependency during schema loading and to make the schema definition language self-hosting.

The bootstrap schema-of-schemas is distinct from domain schemas and from ecosystem meta-schemas.
It governs **only** documents whose root Concept is `Schema`.

The bootstrap schema-of-schemas MUST NOT be substituted for a missing governing schema when processing an instance document.

#### 12.3.1 Requirements

Every conforming implementation MUST:

* include the complete bootstrap schema-of-schemas as built-in, immutable data
* use the bootstrap schema-of-schemas to parse and validate schema documents
* ensure the bootstrap schema-of-schemas is applied deterministically and without extension when no explicit governing schema is provided

An explicitly provided governing schema for a schema document MUST either be the bootstrap schema-of-schemas itself or a schema that is valid under the bootstrap schema-of-schemas. An implementation MUST NOT partially extend, modify, or augment the bootstrap schema-of-schemas.

The bootstrap schema-of-schemas MUST itself conform to the Codex language invariants (§2) and the schema-first architecture (§9).

#### 12.3.2 Schema Document Detection

A document is a schema document if and only if its root Concept is `Schema`.

A document whose root Concept is `Schema` MUST be treated as a schema document and MUST NOT be parsed as an instance document under any schema other than the bootstrap schema-of-schemas or an explicitly provided governing schema.

When a parser encounters a root `Schema` Concept:

1. If an explicit governing schema was provided by the caller, that schema MUST be used.
2. Otherwise, the built-in bootstrap schema-of-schemas MUST be used.

An implementation MUST NOT use any other detection, inference, or fallback mechanisms.

#### 12.3.3 Validation and Error Classification

When processing a schema document:

* If the document cannot be decoded, tokenized, or structurally parsed, the failure MUST be classified as `ParseError` (§14).
* If the document is structurally readable but violates the bootstrap schema-of-schemas or an explicitly provided governing schema, the failure MUST be classified as `SchemaError` (§14).

Implementations MUST NOT attempt partial validation, recovery, or best-effort interpretation.

#### 12.3.4 Canonical Authority

All schema-language constructs that appear in schema documents are defined **exactly once**:

* in the schema definition language specified in §11 of this document

The bootstrap schema-of-schemas MUST accept exactly those schema documents that conform to §11, and MUST reject all others with a `SchemaError` (§14).

The bootstrap schema-of-schemas MUST NOT introduce additional constructs, defaults, or semantics beyond those defined in §11.

### 12.4 Schema Caching

Caching behavior, eviction policy, persistence, and invalidation strategies are implementation-defined.

Caching MUST NOT change observable parsing, validation, or error-reporting behavior.

### 12.5 Error Handling
#### 12.5.1 Schema Unavailable

If no schema can be obtained through any supported mechanism:

* Error class: `SchemaError` (§14)
* The report MUST indicate that the governing schema was unavailable
* Validation MUST NOT proceed

#### 12.5.2 Schema Load Failure

If schema resolution succeeds but loading the schema fails (for example, network error or file not found):

* Error class: `SchemaError` (§14)
* The report MUST indicate that the schema could not be loaded
* The report MUST include the schema identifier

#### 12.5.3 Invalid Schema

If a loaded schema is not valid Codex or is not a valid schema under the bootstrap schema-of-schemas:

* Error class: `SchemaError` (§14)
* The report MUST indicate that schema validation failed
* Underlying schema validation errors MUST be reported

#### 12.5.4 Imported Schema Unavailable

If a `SchemaImport` (§11.2.1) declares a `reference` IRI that is not present in the `importedSchemas` map:

* Error class: `SchemaError` (§14)
* The report MUST indicate which imported schema IRI was unavailable
* Validation MUST NOT proceed

#### 12.5.5 Duplicate Namespace Label

If two or more imported schemas (after namespace label normalization per §10.4) produce the same canonical `namespace` value:

* Error class: `SchemaError` (§14)
* The report MUST indicate the duplicate namespace label and the conflicting schema IRIs
* Validation MUST NOT proceed

#### 12.5.6 Unresolved Qualified Name

If a qualified name (§4.1.1) references a Concept or Trait not defined in the imported schema identified by its namespace prefix:

* Error class: `SchemaError` (§14)
* The report MUST indicate the unresolved qualified name and the imported schema IRI

### 12.6 Relationship to Other Specifications

* This specification defines schema-first processing semantics (§9).
* This section defines how governing schemas are obtained and bootstrapped (§12).
* The schema definition language itself is defined normatively in §11.
* Formatting and canonicalization rules apply uniformly to both schema documents and non-schema documents (§10).

No other specification overrides or weakens these rules.

---

## 13. Schema Versioning

This section normatively defines how schemas are versioned and evolved.

### 13.1 Purpose

The goals of this section are to:

- allow schemas to change without breaking existing data
- make compatibility explicit and inspectable
- prevent silent semantic drift
- support long-lived data and tooling stability

### 13.2 Core Principles

Codex schema versioning is governed by the following principles:

1. Schemas evolve; data persists.
2. Compatibility is explicit, not inferred.
3. Breaking changes are deliberate.
4. Validation is version-aware and conforms to the determinism invariant (§2).

Schemas MUST make their versioning intent explicit.

### 13.3 Schema Identity
Every Codex schema MUST declare its identity and version explicitly.

Schema identity and versioning are defined exclusively by the root `Schema` Concept as specified in §11.

Accordingly:

* The `id` Trait of the root `Schema` Concept defines the **stable schema identifier**.
* The `version` Trait of the root `Schema` Concept defines the **schema version**.
* The `versionScheme` Trait of the root `Schema` Concept defines the **version ordering scheme**.

The schema identifier (`Schema id`) identifies the schema lineage.
All versions of the same schema MUST share the same schema identifier.

The schema version (`Schema version`) identifies the specific set of rules that apply.

A schema document that omits any of the `id`, `version`, or `versionScheme` Traits on the root `Schema` Concept MUST be rejected with a `SchemaError` (§14).

A schema document MUST NOT declare more than one schema identifier.

Within a schema lineage, the schema identifier MUST NOT be redefined or aliased.

Schema identity and version information MUST be treated as authoritative and MUST NOT be inferred, synthesized, or substituted by tooling.

### 13.4 Version Semantics
Schemas MUST use monotonic versioning within a schema lineage.

Within a schema lineage, all schema versions MUST use the same `versionScheme` value; a schema that changes the `versionScheme` within a lineage MUST be rejected with a `SchemaError` (§14).

Regardless of scheme, schema versions MUST form a **total, unambiguous ordering**. A schema whose version ordering is ambiguous or non-comparable MUST be rejected with a `SchemaError` (§14).

Tools MUST compare schema versions mechanically according to the comparison rules defined in this section for the declared `versionScheme`, and MUST NOT apply heuristics, coercion, or fallback rules.

#### 13.4.1 Version Schemes
The root `Schema` Concept’s `versionScheme` Trait MUST be one of the following Enumerated Token Values:

* `$Semver`
* `$DateYYYYMM`
* `$DateYYYYMMDD`
* `$Lexical`

If `versionScheme` is not one of these values, schema processing MUST fail with a `SchemaError` (§14).

#### 13.4.2 Version Comparison Rules
For all schemes below, if a `version` text does not conform to the required scheme-specific syntax, schema processing MUST fail with a `SchemaError` (§14).

`$Semver`

* Syntax: `MAJOR.MINOR.PATCH` where `MAJOR`, `MINOR`, and `PATCH` are base-10 non-negative integers with no leading zeros (the value zero is represented as a single `0` digit).
* Comparison: compare by numeric tuple `(MAJOR, MINOR, PATCH)`.

`$DateYYYYMM`

* Syntax: `YYYY-MM` where `YYYY` is four base-10 digits and `MM` is `01` through `12`.
* Comparison: compare by numeric tuple `(YYYY, MM)`.

`$DateYYYYMMDD`

* Syntax: `YYYY-MM-DD` where `YYYY` is four base-10 digits, `MM` is `01` through `12`, and `DD` is `01` through `31`.
* Comparison: compare by numeric tuple `(YYYY, MM, DD)`.

`$Lexical`

* Syntax: any Text Value.
* Comparison: compare the `version` Text Values by Unicode scalar value codepoint order, left-to-right; if all compared codepoints are equal, the shorter text is less than the longer text.

### 13.5 Compatibility Classes
Each schema version MUST declare exactly one compatibility class. For all versions except the first, the compatibility class declares the relationship to the immediately preceding version in the same schema lineage.

The compatibility class is declared via the `compatibilityClass` Trait on the root `Schema` Concept as defined in §11.

The `compatibilityClass` Trait MUST be one of the following Enumerated Token Values:

* `$Initial`
* `$BackwardCompatible`
* `$ForwardCompatible`
* `$Breaking`

If `compatibilityClass` is not one of these values, schema processing MUST fail with a `SchemaError` (§14).

The declared compatibility class is **normative and enforceable**.

If a schema version's declared compatibility class is contradicted by its actual effects on validation semantics, the schema MUST be rejected with a `SchemaError` (§14).

#### 13.5.1 Initial

The first version in a schema lineage MUST declare `compatibilityClass=$Initial`.

A schema version that declares `$Initial` MUST be the first version in its lineage; if a non-first version declares `$Initial`, schema processing MUST fail with a `SchemaError` (§14).

#### 13.5.2 BackwardCompatible

A backward-compatible schema version guarantees that:

* all Codex data that passed schema validation under the immediately preceding version MUST also pass schema validation under this version
* the meaning of existing Concepts and Traits MUST be preserved
* new Concepts or Traits are permitted to be added
* new constraints are permitted to be added only if they do not invalidate any data that was valid under the preceding version

If any previously valid data becomes invalid under a schema version declared as backward-compatible, the schema MUST be rejected with a `SchemaError` (§14).

#### 13.5.3 ForwardCompatible

A forward-compatible schema version guarantees that:

* Codex data authored for this version is permitted to pass schema validation under the immediately preceding version
* newly introduced constructs are optional and additive
* existing Concepts, Traits, and constraints remain unchanged in meaning

Forward compatibility is intended for extension-oriented evolution where older tools can safely ignore newer constructs.

If data authored for a forward-compatible version cannot pass schema validation under the preceding version without loss of meaning, the schema MUST be rejected with a `SchemaError` (§14).

#### 13.5.4 Breaking

A breaking schema version declares that:

* Codex data valid under the preceding version is permitted to become invalid
* the meaning or constraints of existing Concepts or Traits are permitted to change
* explicit migration is required

Any schema version that introduces a breaking change MUST be declared as breaking.

### 13.6 What Constitutes a Breaking Change
A schema version introduces a breaking change if and only if it violates any guarantee required by the `$BackwardCompatible` or `$ForwardCompatible` compatibility classes with respect to the immediately preceding version.

The following changes are breaking and MUST require `compatibilityClass=$Breaking`:

* removing a `ConceptDefinition`
* renaming a Concept
* removing a `TraitDefinition`
* renaming a Trait
* changing the value type or reference semantics of an existing Trait
* changing `entityEligibility` for any Concept
* changing collection semantics, including ordering or duplicate allowance
* changing identity, reference, or uniqueness semantics
* changing the `namespace` trait value on the root `Schema` Concept (downstream importers use this label to construct qualified names)
* tightening constraints in a way that causes any previously valid data to become invalid
* changing the meaning or interpretation of any existing Concept or Trait

A schema version that introduces any breaking change without declaring `compatibilityClass=$Breaking` is invalid and MUST be rejected with a `SchemaError` (§14).

Documentation-only changes, comments, or purely presentational metadata that do not affect validation or meaning do not constitute breaking changes.

### 13.7 Non-Breaking Changes
A schema version is permitted to be declared as non-breaking only if it preserves all validation and semantic guarantees required by its declared compatibility class.

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

### 13.8 Schema Validation Behavior
When validating a Codex document, the governing schema version MUST be explicitly known.

Validation MUST be performed strictly according to the rules of that schema version.

A conforming implementation MUST:

* use exactly the rules defined by the declared schema version
* treat schema identifier and version as part of the validation input
* fail validation with a `SchemaError` (§14) if the schema version is missing, ambiguous, or cannot be resolved
* fail validation with a `SchemaError` (§14) if the declared compatibility class is violated by the schema's actual effects

A conforming implementation MUST NOT:

* infer schema version intent
* substitute a different schema version
* relax or tighten validation rules across versions
* silently reinterpret data authored under a different schema version

If schema version resolution fails for any reason, validation MUST fail with a `SchemaError` (§14).

### 13.9 Relationship to Data Migration
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

### 13.10 Tooling Responsibilities
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

This section defines the closed set of validation error classes in Codex.

Its goals are to:

- make failures precise and predictable
- ensure consistent classification across tools
- avoid vague reporting and classification approaches that violate the language invariants (§2)
- separate parsing, surface form, formatting/canonicalization, and schema failures cleanly

This section governs error classification only, not wording, UI presentation, or recovery behavior.

### 14.2 Primary Error Class Requirement
Every Codex failure MUST belong to exactly one primary error class.

Tools MUST report exactly one primary error class; additional diagnostic details MUST NOT obscure or replace the primary classification.

### 14.3 Closed Set of Error Classes (Top Level)
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

An implementation MUST NOT define additional top-level error classes.

Validation MUST proceed in the following order:

1. Parsing (ParseError)
2. Surface form validation (SurfaceFormError)
3. Canonicalization (FormattingError)
4. Schema validation (SchemaError, IdentityError, ReferenceError, CollectionError, ContextError, ConstraintError)

Processing MUST halt at the first failure. A failure in an earlier phase MUST NOT be reported as a later-phase error class.

When a violation matches multiple schema-level error classes (4–9), the implementation MUST classify it as the earliest matching class in the enumerated order.

### 14.4 Error Class Definitions

#### 14.4.1 ParseError

Definition: a `.cdx` file cannot be parsed into a syntactic structure.

Characteristics:

- input is not structurally readable
- parsing cannot continue
- well-formedness checks MUST NOT require a governing schema

Examples (illustrative):

- unbalanced Concept markers
- invalid text literal escaping
- malformed Traits
- unterminated Annotation (missing closing `]`)
- structurally invalid nesting of markers
- `SchemaImports` on a non-root Concept (§11.2.1)

#### 14.4.2 SurfaceFormError

Definition: a file parses successfully but violates the surface form requirements (§8).

Characteristics:

- syntax is readable
- surface requirements are violated
- this class concerns schema-independent surface rules defined in §8

Examples (illustrative):

- invalid casing in Concept or Trait names
- multiple root Concepts in a file
- forbidden whitespace around `=`
- annotation opening `[` not at first non-whitespace position

#### 14.4.3 FormattingError

Definition: input parses and passes surface-form requirements but cannot be transformed into canonical surface form.

See §10 for canonicalization rules.

Characteristics:

- canonicalization MUST be deterministic or MUST fail
- tools MUST NOT guess or “best-effort” normalize

Examples (illustrative):

- ambiguous annotation attachment
- non-deterministic blank-line/whitespace normalization that would change annotation kind
- whitespace patterns that cannot be normalized without changing structure
- any other canonicalization failure

#### 14.4.4 SchemaError

Definition: parsed Codex violates schema-defined rules.

Characteristics:

- the governing schema is consulted
- Concepts or Traits are invalid under the governing schema

Examples (illustrative):

- unauthorized Trait on a Concept
- missing required Trait
- invalid Trait value type
- imported schema IRI not found in `importedSchemas` (§12.5.4)
- duplicate canonical namespace labels across imported schemas (§12.5.5)
- qualified name references undefined Concept or Trait in imported schema (§12.5.6)

See §9 and §11 for schema rules.

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

#### 14.4.6 ReferenceError

Definition: reference Traits are invalid or inconsistent.

See §7 for reference trait semantics.

Characteristics:

- involves `reference`, `target`, or `for` Traits
- concerns relationships between Concepts

Examples (illustrative):

- violation of a governing schema's `ReferenceConstraint(type=ReferenceSingleton)` requirement
- reference to a non-existent Entity (where resolution is required)
- reference to an Entity of an unauthorized Concept type

#### 14.4.7 CollectionError

Definition: schema-defined collection rules are violated.

Characteristics:

- concerns schema-defined collection Concepts
- membership, ordering, or cardinality rules are violated

See §11 for collection constraint definitions.

Examples (illustrative):

- mixed member Concept types in a collection
- missing required members
- duplicate membership where forbidden
- member count outside required bounds

#### 14.4.8 ContextError

Definition: a Concept or Trait is used outside its schema-defined context.

Characteristics:

- the Concept or Trait name is valid
- the usage violates containment or scope rules

See §11 for context constraint definitions.

Examples (illustrative):

- Concept allowed only under a specific parent appears elsewhere
- Trait allowed only in a particular context appears outside it

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

See §11 for constraint definitions.

### 14.5 Reporting Requirements
Tools MUST report validation failures with:

* the primary error class
* the Concept name
* the Trait name (if applicable)
* a reference to the violated rule or constraint
* a precise location (line number or Concept path)

If any of the above information is not applicable, the tool MUST omit it explicitly rather than infer or guess.

Error wording, formatting, and presentation are tool-defined, but classification and attribution MUST be precise and deterministic.

#### 14.5.1 Error Payload Shape (Recommended)

This specification does not mandate a serialization format (JSON, CBOR, exceptions, etc.).
However, cross-tool interoperability and stable automated testing benefit from structured error payloads with stable fields.

When a tool exposes a structured error payload, the following fields are recommended:

* `primaryClass` (required): one of the top-level error classes in §14.3.
* `code` (required): a stable machine identifier for the specific rule violation (for example, `parse.unterminated-annotation` or `schema.value-type-mismatch`).
	- `code` values MUST be stable across patch releases.
	- A `code` MUST NOT depend on message text.
* `message` (required): a human-readable description.
* `notes` (optional): a list of additional human-readable strings.
* `span` (recommended when a precise location is available): a source location with:
	- `startByteOffset` and `endByteOffset` in the UTF-8 encoded source file, and
	- `startLine`/`startColumn` and `endLine`/`endColumn` (1-based), where line breaks are LF (U+000A).
* `conceptPath` (optional): a deterministic Concept path identifying the closest relevant Concept instance.
* `traitName` (optional): the relevant Trait name, when applicable.
* `ruleRef` (optional): a stable reference identifying the violated rule or constraint.
* `causes` (optional): a list of nested errors (each with the same shape), ordered from most-direct to least-direct cause.

This list does not prohibit additional fields.
When an error payload includes both a `span` and a `conceptPath`, the `span` MUST identify the precise surface-form location for the same failing construct.

### 14.6 Non-Goals

This section does not:

- define message wording
- mandate UX
- define recovery strategies
- prescribe exception hierarchies
- define logging formats

It defines what kind of error occurred, not how it is presented.

### 14.7 Summary

- every failure has exactly one primary error class
- error classes are finite and closed
- parsing, surface form, formatting/canonicalization, and schema are separated
- failures are fatal within their primary error class

---

## Appendix A. Formal Grammar

This appendix defines the formal grammar of the Codex surface form (§8).

Two grammar notations are provided:

* EBNF (Normative) — ISO/IEC 14977 Extended Backus-Naur Form
* PEG (Informative) — Parsing Expression Grammar for implementation

### A.1 EBNF
#### A.1.1 Notation

This grammar is based on ISO/IEC 14977 EBNF notation with extensions:

* `=` defines a production
* `,` concatenation
* `|` alternation
* `[ ... ]` optional (zero or one)
* `{ ... }` repetition (zero or more)
* `( ... )` grouping
* " ... " terminal literal
* ' ... ' terminal literal (alternative)
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

> This grammar is an informative projection of the document-level rules defined in §8 (one root Concept), §8.2 (trailing LF), §8.4 (blank lines), and §8.9 (annotations). In case of discrepancy, those sections are authoritative.

```ebnf
(* A Codex document contains exactly one root Concept and MUST end with
   a trailing newline followed by EOF (§8.2). *)

Document
	= OptionalLeadingAnnotations, RootConcept, OptionalTrailingBlankLines, EOF
	;

OptionalLeadingAnnotations
	= { GeneralOrGroupingAnnotationBlock }
	;

OptionalTrailingBlankLines
	= { BlankLine }
	;

EOF
	= (* end of input; no further characters *)
	;

RootConcept
	= ConceptAtColumn0
	;

ConceptAtColumn0
	= ConceptLineStart0, BlockConcept
	| ConceptLineStart0, SelfClosingConcept, Newline
	;

ConceptLineStart0
	= (* beginning of file or immediately after Newline *)
	  [ Newline ]
	;

(* A general or grouping annotation block may appear before the root concept.
	This grammar admits them structurally; their kind/attachment rules are checked
	by the surface-form rules (§8.9). *)
GeneralOrGroupingAnnotationBlock
	= { BlankLine }, Annotation, { BlankLine }
	;

Concept
	= BlockConcept | SelfClosingConcept
	;
```

---

#### A.1.3 Block Concepts

> This grammar is an informative projection of the Concept marker rules defined in §8.5 and the content rules defined in §8.8. In case of discrepancy, those sections are authoritative.

```ebnf
(* Block concepts contain either children or content.
	The parser consults the governing schema (§11) to select the Body production.
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
	= "<", ConceptNameOrQualified, [ Traits ], { WhitespaceChar }, ">"
	;

ClosingMarker
	= "</", ConceptNameOrQualified, ">"
	;

(* Body is selected by schema lookup on ConceptName (§11):
	- If schema indicates children mode: ChildrenBody
	- If schema indicates content mode: ContentBody *)
Body
	= ChildrenBody | ContentBody
	;

ChildrenBody
	= { ChildItem }
	;

(* A ChildItem is either:
	- an annotation line/block, or
	- a child concept (block or self-closing), each on its own structural line.
	Blank-line legality is enforced by surface-form rules (§8); the grammar admits both. *)
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

(* Within a children body, a child concept is either a self-closing marker
	or a nested block concept (handled by the Concept production). *)
ConceptMarkerOrConcept
	= SelfClosingMarker
	| Concept
	;

ContentBody
	= { ContentLine }
	;

ContentLine
	= Indentation, ContentText, Newline
	;

ContentText
	= { ContentCharacter }
	;

ContentCharacter
	= ContentEscape | ContentSafeChar
	;

ContentEscape
	= "\\", ( "\\" | "<" | "[" )
	;

(* Raw '<' is forbidden anywhere in content; raw '[' at line start is
	checked by surface-form rules (§8.8). *)
ContentSafeChar
	= AnyCharExceptNewline - "<"
	;
```

---

#### A.1.4 Self-Closing Concepts

> This grammar is an informative projection of the self-closing marker rules defined in §8.5.3. In case of discrepancy, §8.5.3 is authoritative.

```ebnf
SelfClosingConcept
	= SelfClosingMarker
	;

SelfClosingMarker
	= "<", ConceptNameOrQualified, [ Traits ], Whitespace, "/>"
	;
```

---

#### A.1.5 Concept Names

> This grammar is an informative projection of the naming rules defined in §4.1 and §4.1.1. In case of discrepancy, those sections are authoritative.

```ebnf
(* Naming rule details beyond basic lexical form (e.g., no runs of uppercase)
	are enforced by surface-form validation (§4). *)

ConceptName
	= UppercaseLetter, { Letter | Digit }
	;

(* A qualified concept name combines a namespace prefix with a concept name,
	separated by a colon. See §4.1.1. *)
QualifiedConceptName
	= NamespacePrefix, ":", ConceptName
	;

(* A concept name reference is either a bare concept name or a qualified one. *)
ConceptNameOrQualified
	= QualifiedConceptName | ConceptName
	;

(* A namespace prefix follows the same lexical form as a trait name (camelCase). *)
NamespacePrefix
	= LowercaseLetter, { Letter | Digit }
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

> This grammar is an informative projection of the Trait spelling rules defined in §8.6. In case of discrepancy, §8.6 is authoritative.

```ebnf
Traits
	= Whitespace, Trait, { Whitespace, Trait }
	;

Trait
	= TraitName, "=", Value
	;

(* Naming rule details beyond basic lexical form are enforced by surface-form validation (§4). *)
TraitName
	= LowercaseLetter, { Letter | Digit }
	;
```

---

#### A.1.7 Values

> The inline productions for `HostNameValue`, `EmailAddressValue`, and `UrlValue` below are informative projections of §5.20, §5.21, and §5.22 respectively. In case of discrepancy, those sections are authoritative.

```ebnf
Value
	= TextValue
	| CharValue
	| BacktickText
	| BooleanValue
	| NumericValue
	| EnumeratedToken
	| TemporalValue
	| ColorValue
	| UuidValue
	| HostNameValue
	| EmailAddressValue
	| UrlValue
	| LookupToken
	| IriReference
	| ListValue
	| SetValue
	| MapValue
	| RecordValue
	| TupleValue
	| RangeValue
	;

HostNameValue
	= "host", "(", { Whitespace }, TextValue, { Whitespace }, ")"
	;

EmailAddressValue
	= "email", "(", { Whitespace }, TextValue, { Whitespace }, ")"
	;

UrlValue
	= "url", "(", { Whitespace }, TextValue, { Whitespace }, [ ",", { Whitespace }, TextValue, { Whitespace } ], ")"
	;
```

---

#### A.1.8 Text Values

> This grammar is an informative projection of the quoted text spelling rules defined in §5.1. In case of discrepancy, §5.1 is authoritative.

```ebnf
TextValue
	= '"', { TextCharacter }, '"'
	;

TextCharacter
	= UnescapedTextCharacter | EscapeSequence
	;

UnescapedTextCharacter
	= AnyCharExceptQuoteNewline
	;

EscapeSequence
	= "\\", ( '"' | "\\" | UnicodeEscape )
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

> This grammar is an informative projection of the character literal spelling rules defined in §5.11. In case of discrepancy, §5.11 is authoritative.

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

#### A.1.10 Backtick Text

> This grammar is an informative projection of the backtick text spelling rules defined in §5.2. In case of discrepancy, §5.2 is authoritative.

```ebnf
BacktickText
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

> This grammar is an informative projection of the Boolean Value spelling rules defined in §5.3. In case of discrepancy, §5.3 is authoritative.

```ebnf
BooleanValue
	= "true" | "false"
	;
```

---

#### A.1.12 Numeric Values

> This grammar is an informative projection of the numeric value spelling rules defined in §5.4. In case of discrepancy, §5.4 is authoritative.

```ebnf
NumericValue
	= ComplexNumber
	| ImaginaryNumber
	| Fraction
	| Infinity
	| PrecisionNumber
	| ExponentialNumber
	| DecimalNumber
	| Integer
	;

Sign
	= "+" | "-"
	;

Integer
	= "0" | [ "-" ], NonZeroDigit, { Digit }
	;

DecimalNumber
	= [ "-" ], IntegerDigits, ".", DigitSequence
	;

ExponentialNumber
	= ( Integer | DecimalNumber ), ( "e" | "E" ), [ Sign ], IntegerDigits
	;

PrecisionNumber
	= DecimalNumber, "p", [ IntegerDigits ]
	;

(* Infinity and -Infinity are permitted; +Infinity is not (§5.4).
	Compiles to XSD INF and -INF respectively. *)
Infinity
	= PositiveInfinity | NegativeInfinity
	;

PositiveInfinity
	= "Infinity"
	;

NegativeInfinity
	= "-", "Infinity"
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

> This grammar is an informative projection of the Enumerated Token spelling rules defined in §5.5 and the parameterized type syntax defined in §5.18. In case of discrepancy, §5.5 and §5.18 are authoritative.

```ebnf
EnumeratedToken
	= "$", UppercaseLetter, { Letter | Digit }, [ TypeParameters ]
	;

TypeParameters
	= "<", TypeArgument, { ",", " ", TypeArgument }, ">"
	;

TypeArgument
	= EnumeratedToken
	| TypeUnion
	;

TypeUnion
	= "[", EnumeratedToken, { ",", " ", EnumeratedToken }, "]"
	;
```

---

#### A.1.14 Temporal Values

> This grammar is an informative projection of the spelling rules defined in §5.6.2. In case of discrepancy, §5.6.2 is authoritative.

```ebnf
TemporalValue
	= "{", TemporalBody, "}"
	;

(* Temporal kind is determined by the first matching alternative
   in the order listed below (§5.6.1). *)
TemporalBody
	= ZonedDateTime
	| Instant
	| PlainDateTime
	| PlainDate
	| YearWeek
	| PlainYearMonth
	| PlainMonthDay
	| PlainTime
	| Duration
	| TemporalKeyword
	;

PlainDate
	= Year, "-", Month, "-", Day
	;

YearWeek
	= Year, "-", ( "W" | "w" ), WeekNumber
	;

WeekNumber
	= Digit, Digit
	;

PlainYearMonth
	= Year, "-", Month
	;

PlainMonthDay
	= Month, "-", Day
	;

PlainDateTime
	= PlainDate, "T", PlainTime
	;

Instant
	= PlainDateTime, TimeZoneOffset
	;

ZonedDateTime
	= PlainDateTime, TimeZoneOffset, TimeZoneId
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

PlainTime
	= Hour, ":", Minute, [ ":", Second, [ ".", FractionalSeconds ] ]
	;

Duration
	= "P", DurationComponent, { DurationComponent }, [ "T", TimeDurationComponent, { TimeDurationComponent } ]
	| "P", "T", TimeDurationComponent, { TimeDurationComponent }
	;

DurationComponent
	= DigitSequence, ( "Y" | "M" | "W" | "D" )
	;

TimeDurationComponent
	= DigitSequence, [ ".", DigitSequence ], ( "H" | "M" | "S" )
	;

TemporalKeyword
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

FractionalSeconds
	= Digit, { Digit }
	;
```

---

#### A.1.15 Color Values

> This grammar is an informative projection of the color function argument spelling rules and semantic domains defined in §5.7.4. In case of discrepancy, §5.7.4 is authoritative.

```ebnf
(* Color values are accepted as declarative spellings; tools MUST NOT normalize,
	rewrite, or "best-effort" correct them (§5.7). During semantic validation,
	tools MUST interpret and convert a color value to a semantic color type for the
	purposes of schema validation and evaluation, but this MUST NOT change the
	canonical surface spelling. Hex digits, function names, and color space tokens
	are case-insensitive for parsing; lowercase is canonical. *)

ColorValue
	= HexColor
	| FunctionColor
	| NamedColor
	;

HexColor
	= "#", HexDigit, HexDigit, HexDigit, [ HexDigit ]
	| "#", HexDigit, HexDigit, HexDigit, HexDigit, HexDigit, HexDigit, [ HexDigit, HexDigit ]
	;

(* §5.7.2, Appendix B: Name MUST be a named color keyword; unrecognized names are a ParseError (§14). *)
NamedColor
	= "&", LowercaseLetter, { LowercaseLetter }
	;

FunctionColor
	= RgbFunction
	| HslFunction
	| HwbFunction
	| LabFunction
	| LchFunction
	| OklabFunction
	| OklchFunction
	| ColorSpaceColorFunction
	| ColorMixFunction
	| RelativeColorFunction
	| DeviceCmykFunction
	;

RgbFunction
	= ( "rgb" | "rgba" ), "(", ColorWhitespaceOptional, RgbArguments, ColorWhitespaceOptional, ")"
	;

HslFunction
	= ( "hsl" | "hsla" ), "(", ColorWhitespaceOptional, HslArguments, ColorWhitespaceOptional, ")"
	;

HwbFunction
	= "hwb", "(", ColorWhitespaceOptional, HwbArguments, ColorWhitespaceOptional, ")"
	;

LabFunction
	= "lab", "(", ColorWhitespaceOptional, LabArguments, ColorWhitespaceOptional, ")"
	;

LchFunction
	= "lch", "(", ColorWhitespaceOptional, LchArguments, ColorWhitespaceOptional, ")"
	;

OklabFunction
	= "oklab", "(", ColorWhitespaceOptional, OklabArguments, ColorWhitespaceOptional, ")"
	;

OklchFunction
	= "oklch", "(", ColorWhitespaceOptional, OklchArguments, ColorWhitespaceOptional, ")"
	;

ColorSpaceColorFunction
	= "color", "(", ColorWhitespaceOptional, ( RgbColorSpace, ColorWhitespace, ColorRgbArguments | XyzColorSpace, ColorWhitespace, ColorXyzArguments ), ColorWhitespaceOptional, ")"
	;

ColorMixFunction
	= "color-mix", "(", ColorWhitespaceOptional, "in", ColorWhitespace, ColorSpace, ColorComma, ColorMixStop,
	  ColorComma, ColorMixStop, { ColorComma, ColorMixStop }, ColorWhitespaceOptional, ")"
	;

RelativeColorFunction
	= RelativeRgbFunction
	| RelativeHslFunction
	| RelativeHwbFunction
	| RelativeLabFunction
	| RelativeLchFunction
	| RelativeOklabFunction
	| RelativeOklchFunction
	| RelativeColorSpaceColorFunction
	;

DeviceCmykFunction
	= "device-cmyk", "(", ColorWhitespaceOptional, DeviceCmykArguments, ColorWhitespaceOptional, ")"
	;

ColorSpace
	= RgbColorSpace | XyzColorSpace
	;

RgbColorSpace
	= "srgb"
	| "srgb-linear"
	| "display-p3"
	| "a98-rgb"
	| "prophoto-rgb"
	| "rec2020"
	;

XyzColorSpace
	= "xyz"
	| "xyz-d50"
	| "xyz-d65"
	;

(* All supported color function spellings have explicit argument grammar.
	Newlines are not permitted in any function spelling.

	Numeric forms in color functions are a restricted subset of NumericValue:
	ColorRealNumber excludes complex and imaginary numbers.
*)

ColorWhitespace
	= WhitespaceNoNewline
	;

ColorWhitespaceOptional
	= { WhitespaceNoNewlineChar }
	;

ColorRealNumber
	= Fraction
	| Infinity
	| PrecisionNumber
	| ExponentialNumber
	| DecimalNumber
	| Integer
	;

ColorPercentage
	= ColorRealNumber, "%"
	;

ColorAlpha
	= ColorPercentage
	| ColorRealNumber
	;

ColorComma
	= ColorWhitespaceOptional, ",", ColorWhitespaceOptional
	;

RgbComponent
	= ColorPercentage
	| ColorRealNumber
	;

CmykComponent
	= ColorPercentage
	| ColorRealNumber
	;

HueComponent
	= ColorRealNumber
	;

RgbArguments
	= RgbLegacyArguments
	| RgbModernArguments
	;

RgbLegacyArguments
	= RgbComponent, ColorComma, RgbComponent, ColorComma, RgbComponent,
	  [ ColorComma, ColorAlpha ]
	;

RgbModernArguments
	= RgbComponent, ColorWhitespace, RgbComponent, ColorWhitespace, RgbComponent,
	  [ ColorWhitespaceOptional, "/", ColorWhitespaceOptional, ColorAlpha ]
	;

HslArguments
	= HslLegacyArguments
	| HslModernArguments
	;

HslLegacyArguments
	= HueComponent, ColorComma, ColorPercentage, ColorComma, ColorPercentage,
	  [ ColorComma, ColorAlpha ]
	;

HslModernArguments
	= HueComponent, ColorWhitespace, ColorPercentage, ColorWhitespace, ColorPercentage,
	  [ ColorWhitespaceOptional, "/", ColorWhitespaceOptional, ColorAlpha ]
	;

HwbArguments
	= HueComponent, ColorWhitespace, ColorPercentage, ColorWhitespace, ColorPercentage,
	  [ ColorWhitespaceOptional, "/", ColorWhitespaceOptional, ColorAlpha ]
	;

ColorRgbArguments
	= RgbComponent, ColorWhitespace, RgbComponent, ColorWhitespace, RgbComponent,
	  [ ColorWhitespaceOptional, "/", ColorWhitespaceOptional, ColorAlpha ]
	;

ColorXyzArguments
	= ColorRealNumber, ColorWhitespace, ColorRealNumber, ColorWhitespace, ColorRealNumber,
	  [ ColorWhitespaceOptional, "/", ColorWhitespaceOptional, ColorAlpha ]
	;

DeviceCmykArguments
	= CmykComponent, ColorWhitespace, CmykComponent, ColorWhitespace, CmykComponent, ColorWhitespace, CmykComponent,
	  [ ColorWhitespaceOptional, "/", ColorWhitespaceOptional, ColorAlpha ]
	;

LabArguments
	= ColorPercentage, ColorWhitespace, ColorRealNumber, ColorWhitespace, ColorRealNumber,
	  [ ColorWhitespaceOptional, "/", ColorWhitespaceOptional, ColorAlpha ]
	;

LchArguments
	= ColorPercentage, ColorWhitespace, ColorRealNumber, ColorWhitespace, ColorRealNumber,
	  [ ColorWhitespaceOptional, "/", ColorWhitespaceOptional, ColorAlpha ]
	;

OklabArguments
	= ColorRealNumber, ColorWhitespace, ColorRealNumber, ColorWhitespace, ColorRealNumber,
	  [ ColorWhitespaceOptional, "/", ColorWhitespaceOptional, ColorAlpha ]
	;

OklchArguments
	= ColorRealNumber, ColorWhitespace, ColorRealNumber, ColorWhitespace, ColorRealNumber,
	  [ ColorWhitespaceOptional, "/", ColorWhitespaceOptional, ColorAlpha ]
	;

ColorMixStop
	= ColorValue, [ ColorWhitespace, ColorPercentage ]
	;

RelativeRgbFunction
	= ( "rgb" | "rgba" ), "(", ColorWhitespaceOptional, "from", ColorWhitespace, ColorValue, ColorWhitespace, RelativeRgbArguments, ColorWhitespaceOptional, ")"
	;

RelativeHslFunction
	= ( "hsl" | "hsla" ), "(", ColorWhitespaceOptional, "from", ColorWhitespace, ColorValue, ColorWhitespace, RelativeHslArguments, ColorWhitespaceOptional, ")"
	;

RelativeHwbFunction
	= "hwb", "(", ColorWhitespaceOptional, "from", ColorWhitespace, ColorValue, ColorWhitespace, RelativeHwbArguments, ColorWhitespaceOptional, ")"
	;

RelativeLabFunction
	= "lab", "(", ColorWhitespaceOptional, "from", ColorWhitespace, ColorValue, ColorWhitespace, RelativeLabArguments, ColorWhitespaceOptional, ")"
	;

RelativeLchFunction
	= "lch", "(", ColorWhitespaceOptional, "from", ColorWhitespace, ColorValue, ColorWhitespace, RelativeLchArguments, ColorWhitespaceOptional, ")"
	;

RelativeOklabFunction
	= "oklab", "(", ColorWhitespaceOptional, "from", ColorWhitespace, ColorValue, ColorWhitespace, RelativeOklabArguments, ColorWhitespaceOptional, ")"
	;

RelativeOklchFunction
	= "oklch", "(", ColorWhitespaceOptional, "from", ColorWhitespace, ColorValue, ColorWhitespace, RelativeOklchArguments, ColorWhitespaceOptional, ")"
	;

RelativeColorSpaceColorFunction
	= "color", "(", ColorWhitespaceOptional, "from", ColorWhitespace, ColorValue, ColorWhitespace, ColorSpace, ColorWhitespace, RelativeColorArguments, ColorWhitespaceOptional, ")"
	;

RelativeRgbChannel
	= "r" | "g" | "b"
	;

RelativeHslChannel
	= "h" | "s" | "l"
	;

RelativeHwbChannel
	= "h" | "w" | "b"
	;

RelativeLabChannel
	= "l" | "a" | "b"
	;

RelativeLchChannel
	= "l" | "c" | "h"
	;

RelativeOklabChannel
	= "l" | "a" | "b"
	;

RelativeOklchChannel
	= "l" | "c" | "h"
	;

RelativeAlphaComponent
	= ColorAlpha
	| "a"
	;

RelativeRgbComponent
	= RgbComponent
	| RelativeRgbChannel
	;

RelativeRgbArguments
	= RelativeRgbComponent, ColorWhitespace, RelativeRgbComponent, ColorWhitespace, RelativeRgbComponent,
	  [ ColorWhitespaceOptional, "/", ColorWhitespaceOptional, RelativeAlphaComponent ]
	;

RelativeHslArguments
	= ( HueComponent | RelativeHslChannel ), ColorWhitespace, ( ColorPercentage | "s" ), ColorWhitespace, ( ColorPercentage | "l" ),
	  [ ColorWhitespaceOptional, "/", ColorWhitespaceOptional, RelativeAlphaComponent ]
	;

RelativeHwbArguments
	= ( HueComponent | "h" ), ColorWhitespace, ( ColorPercentage | "w" ), ColorWhitespace, ( ColorPercentage | "b" ),
	  [ ColorWhitespaceOptional, "/", ColorWhitespaceOptional, RelativeAlphaComponent ]
	;

RelativeLabArguments
	= ( ColorPercentage | "l" ), ColorWhitespace, ( ColorRealNumber | "a" ), ColorWhitespace, ( ColorRealNumber | "b" ),
	  [ ColorWhitespaceOptional, "/", ColorWhitespaceOptional, RelativeAlphaComponent ]
	;

RelativeLchArguments
	= ( ColorPercentage | "l" ), ColorWhitespace, ( ColorRealNumber | "c" ), ColorWhitespace, ( ColorRealNumber | "h" ),
	  [ ColorWhitespaceOptional, "/", ColorWhitespaceOptional, RelativeAlphaComponent ]
	;

RelativeOklabArguments
	= ( ColorRealNumber | "l" ), ColorWhitespace, ( ColorRealNumber | "a" ), ColorWhitespace, ( ColorRealNumber | "b" ),
	  [ ColorWhitespaceOptional, "/", ColorWhitespaceOptional, RelativeAlphaComponent ]
	;

RelativeOklchArguments
	= ( ColorRealNumber | "l" ), ColorWhitespace, ( ColorRealNumber | "c" ), ColorWhitespace, ( ColorRealNumber | "h" ),
	  [ ColorWhitespaceOptional, "/", ColorWhitespaceOptional, RelativeAlphaComponent ]
	;

RelativeColorChannel
	= "r" | "g" | "b" | "x" | "y" | "z"
	;

RelativeColorComponent
	= ColorRealNumber
	| ColorPercentage
	| RelativeColorChannel
	;

RelativeColorArguments
	= RelativeColorComponent, ColorWhitespace, RelativeColorComponent, ColorWhitespace, RelativeColorComponent,
	  [ ColorWhitespaceOptional, "/", ColorWhitespaceOptional, RelativeAlphaComponent ]
	;
```

---

#### A.1.16 UUID Values

> This grammar is an informative projection of the UUID spelling rules defined in §5.8. In case of discrepancy, §5.8 is authoritative.

```ebnf
(* UUID format: 8-4-4-4-12 hex digits (§5.8).
	Hex digits are case-insensitive for parsing; lowercase is canonical. *)
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

> This grammar is an informative projection of the IRI reference spelling rules defined in §5.9. In case of discrepancy, §5.9 is authoritative.

```ebnf
(* IRI references are unquoted tokens containing a ':' (§5.9).
	They terminate at Value termination (§A.1.28). *)

IriReference
	= IriScheme, ":", IriTokenBody
	;

IriScheme
	= Letter, { Letter | Digit | "+" | "-" | "." }
	;

IriTokenBody
	= { IriTokenChar }
	;

(* Token-level placeholder: the exact admissible character set is RFC 3987
	profiled by §5.9. Surface-form validation (§8) enforces disallowed Unicode
	categories; the grammar enforces only token termination exclusions. *)
IriTokenChar
	= AnyCharExceptValueTerminator
	;
```

---

#### A.1.18 Lookup Token Values

> This grammar is an informative projection of the Lookup Token spelling rules defined in §5.10. In case of discrepancy, §5.10 is authoritative.

```ebnf
(* Lookup tokens reference document-scoped keys (§5.10). *)
LookupToken
	= "~", LowercaseLetter, { Letter | Digit }
	;
```

---

#### A.1.19 List Values

> This grammar is an informative projection of the List Value spelling rules defined in §5.12. In case of discrepancy, §5.12 is authoritative.

```ebnf
(* List Values are ordered sequences of zero or more elements (§5.12). *)
ListValue
	= "[", { Whitespace }, [ ListItems ], { Whitespace }, "]"
	;

ListItems
	= Value, { { Whitespace }, ",", { Whitespace }, Value }
	;
```

---

#### A.1.20 Set Values

> This grammar is an informative projection of the Set Value spelling rules defined in §5.14. In case of discrepancy, §5.14 is authoritative.

```ebnf
(* Set Values are unordered collections; duplicate elements are a ParseError (§5.14, §14). *)
SetValue
	= "set", "[", { Whitespace }, [ SetItems ], { Whitespace }, "]"
	;

SetItems
	= Value, { { Whitespace }, ",", { Whitespace }, Value }
	;
```

---

#### A.1.21 Map Values

> This grammar is an informative projection of the Map Value spelling rules defined in §5.15. In case of discrepancy, §5.15 is authoritative.

```ebnf
(* Map Values are key-value collections; duplicate keys are a ParseError (§5.15, §14). *)
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
	| TextValue
	| CharValue
	| Integer
	| EnumeratedToken
	| IriReference
	;

MapIdentifier
	= LowercaseLetter, { Letter | Digit }
	;
```

---

#### A.1.22 Record Values

> This grammar is an informative projection of the Record Value spelling rules defined in §5.19. In case of discrepancy, §5.19 is authoritative.

```ebnf
(* Record Values have schema-defined field names; duplicate fields are a ParseError (§5.19, §14). *)
RecordValue
	= "record", "[", { Whitespace }, [ RecordItems ], { Whitespace }, "]"
	;

RecordItems
	= RecordEntry, { { Whitespace }, ",", { Whitespace }, RecordEntry }
	;

RecordEntry
	= RecordFieldName, { Whitespace }, ":", { Whitespace }, Value
	;

RecordFieldName
	= LowercaseLetter, { Letter | Digit }
	;
```

---

#### A.1.23 Tuple Values

> This grammar is an informative projection of the Tuple Value spelling rules defined in §5.16. In case of discrepancy, §5.16 is authoritative.

```ebnf
(* Tuple Values require at least one element (§5.16). *)
TupleValue
	= "(", { Whitespace }, TupleItems, { Whitespace }, ")"
	;

TupleItems
	= Value, { { Whitespace }, ",", { Whitespace }, Value }
	;
```

---

#### A.1.24 Range Values

> This grammar is an informative projection of the Range Value spelling rules defined in §5.17. In case of discrepancy, §5.17 is authoritative.

```ebnf
(* Range Values are declarative intervals with optional step (§5.17).
   Range endpoints and steps use OrderedNumericValue, which excludes
   ComplexNumber, ImaginaryNumber, and Infinity. *)
RangeValue
	= RangeStart, { WhitespaceChar }, "..", { WhitespaceChar }, RangeEnd,
	  [ { WhitespaceChar }, "s", { WhitespaceChar }, StepValue ]
	;

RangeStart
	= OrderedNumericValue | TemporalValue | CharValue
	;

RangeEnd
	= OrderedNumericValue | TemporalValue | CharValue
	;

StepValue
	= OrderedNumericValue | TemporalValue
	;

(* Numeric types with a total ordering, suitable for range intervals.
   Excludes ComplexNumber, ImaginaryNumber, and Infinity. *)
OrderedNumericValue
	= PrecisionNumber
	| ExponentialNumber
	| Fraction
	| DecimalNumber
	| Integer
	;
```

---

#### A.1.25 Annotations

> This grammar is an informative projection of the annotation rules defined in §8.9. In case of discrepancy, §8.9 is authoritative.

```ebnf
(* Codex defines two surface forms for annotations (§8.9):
	- Inline: '[' ... ']' on a single line
	- Block: '[' on its own line, then content lines, then ']' on its own line
	The attachment/grouping/general-kind rules are surface-form validation rules (§8.9). *)

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

(* A line consisting solely of Indentation + "]" + Newline terminates the
	block annotation; such a line MUST NOT be consumed as an AnnotationBlockLine.
	In EBNF this constraint is not directly expressible; implementations must
	check for the closing "]" before trying AnnotationBlockLine. *)
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
	= "\\", ( "\\" | "]" )
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

#### A.1.26 Whitespace and Structural Elements

> This grammar is an informative projection of the whitespace and structural rules defined in §8.2 (line endings), §8.3 (indentation), and §8.4 (blank lines). In case of discrepancy, those sections are authoritative.

```ebnf
(* Indentation uses tabs only; spaces in indentation are errors (§8.3). *)
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

(* A blank line contains only a newline; no spaces or tabs are permitted. *)
BlankLine
	= Newline
	;

Indentation
	= { "\t" }
	;
```

---

#### A.1.27 Character Classes (Informative)

The following character classes are used but not fully enumerated:

* `AnyCharExceptNewline` — any Unicode scalar except U+000A
* `AnyCharExceptQuoteNewline` — any Unicode scalar except `"`, U+000A
* `AnyCharExceptApostropheBackslashNewline` — any Unicode scalar except `'`, `\\`, U+000A
* `AnyCharExceptBacktick` — any Unicode scalar except `` ` ``
* `AnyCharExceptRightParenNewline` — any Unicode scalar except `)`, U+000A
* `AnyCharExceptParensNewline` — any Unicode scalar except `(`, `)`, U+000A
* `AnyCharExceptRightBracketNewline` — any Unicode scalar except `]`, U+000A
* `AnyCharExceptBackslashNewline` — any Unicode scalar except `\\`, U+000A
* `AnyCharExceptValueTerminator` — any Unicode scalar except a Value terminator (defined in §A.1.28)

---

#### A.1.28 Value Termination and Disambiguation

> This grammar is an informative projection of the Value termination and disambiguation rules defined in §8.7 and §8.7.1. In case of discrepancy, those sections are authoritative.
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
* " ... " literal
* ' ... ' literal (alternative)
* `[ ... ]` character class
* `.` any character
* `#` comment to end of line

---

#### A.2.2 Document Structure

> This grammar is an informative projection of the document-level rules defined in §8 (one root Concept), §8.2 (trailing LF), §8.4 (blank lines), and §8.9 (annotations). In case of discrepancy, those sections are authoritative.

```peg
# A Codex document contains exactly one root Concept.
# Surface-form rules constrain root count, blank-line placement, and annotation kinds.

Document <- OptionalLeadingAnnotations? RootConcept OptionalTrailingBlankLines EOF

OptionalLeadingAnnotations <- GeneralOrGroupingAnnotationBlock*
GeneralOrGroupingAnnotationBlock <- BlankLine* Annotation BlankLine*

OptionalTrailingBlankLines <- BlankLine*

RootConcept <- ConceptAtColumn0

ConceptAtColumn0 <- ConceptLineStart0 BlockConcept
                 / ConceptLineStart0 SelfClosingConcept Newline

ConceptLineStart0 <- &(!. / Newline)

Concept <- BlockConcept / SelfClosingConcept
```

---

#### A.2.3 Block Concepts

> This grammar is an informative projection of the Concept marker rules defined in §8.5 and the content rules defined in §8.8. In case of discrepancy, those sections are authoritative.

```peg
# Block concepts contain either children or content.
# The parser consults the governing schema (ContentRules) to decide which Body to parse.
# This is schema-directed dispatch, not syntactic ambiguity.

BlockConcept <- OpeningMarkerLine Body ClosingMarkerLine

OpeningMarkerLine <- Indentation OpeningMarker Newline
ClosingMarkerLine <- Indentation ClosingMarker Newline

OpeningMarker <- '<' ConceptNameOrQualified Traits? WhitespaceChar* '>'
ClosingMarker <- '</' ConceptNameOrQualified '>'

# Body is selected by schema lookup on ConceptName (§11):
# - children mode: ChildrenBody
# - content mode: ContentBody
Body <- ChildrenBody / ContentBody

# ChildrenBody admits BlankLine and Annotation; their legality and attachment kinds
# are checked by surface-form rules and canonicalization rules.
ChildrenBody <- ChildItem*

ChildItem <- BlankLine / AnnotationLine / AnnotationBlock / ConceptLine

ConceptLine <- Indentation ConceptMarkerOrConcept Newline
ConceptMarkerOrConcept <- SelfClosingMarker / Concept

ContentBody <- ContentLine*

ContentLine <- Indentation ContentText Newline

ContentText <- ContentCharacter*
ContentCharacter <- ContentEscape / ContentSafeChar
ContentEscape <- '\\' ('\\' / '<' / '[')
ContentSafeChar <- !Newline !'<' .
```

---

#### A.2.4 Self-Closing Concepts

> This grammar is an informative projection of the self-closing marker rules defined in §8.5.3. In case of discrepancy, §8.5.3 is authoritative.

```peg
SelfClosingConcept <- SelfClosingMarker

SelfClosingMarker <- '<' ConceptNameOrQualified Traits? Whitespace '/>'
```

---

#### A.2.5 Concept Names

> This grammar is an informative projection of the naming rules defined in §4.1 and §4.1.1. In case of discrepancy, those sections are authoritative.

```peg
ConceptName <- UppercaseLetter (Letter / Digit)*

# A qualified concept name: namespace prefix, colon, concept name (§4.1.1)
QualifiedConceptName <- NamespacePrefix ':' ConceptName

# A concept name reference: qualified or bare
ConceptNameOrQualified <- QualifiedConceptName / ConceptName

# A namespace prefix has the same lexical form as a trait name (camelCase)
NamespacePrefix <- LowercaseLetter (Letter / Digit)*

UppercaseLetter <- [A-Z]
LowercaseLetter <- [a-z]
Letter <- [A-Za-z]
Digit <- [0-9]
```

---

#### A.2.6 Traits

> This grammar is an informative projection of the Trait spelling rules defined in §8.6. In case of discrepancy, §8.6 is authoritative.

```peg
# Traits are whitespace-separated tokens in the opening marker.
# Newline is permitted in Whitespace, enabling multi-line trait layout;
# formatting rules define canonical layout.

Traits <- Whitespace Trait (Whitespace Trait)*

Trait <- TraitName '=' Value

TraitName <- LowercaseLetter (Letter / Digit)*
```

---

#### A.2.7 Values

> The inline productions for `HostNameValue`, `EmailAddressValue`, and `UrlValue` below are informative projections of §5.20, §5.21, and §5.22 respectively. In case of discrepancy, those sections are authoritative.

```peg
# Values are tried in deterministic precedence order.
# Token termination in markers is governed by the surface rules (see A.1.28);
# this PEG uses explicit constructs for balanced literals.

Value <- TextValue
      / CharValue
	/ BacktickText
	/ HostNameValue
	/ EmailAddressValue
	/ UrlValue
      / BooleanValue
      / EnumeratedToken
      / LookupToken
      / TemporalValue
      / SetValue
      / MapValue
      / RecordValue
      / ListValue
      / TupleValue
      / ColorValue
      / UuidValue
      / RangeValue
      / NumericValue
      / IriReference

HostNameValue <- 'host' '(' WhitespaceChar* TextValue WhitespaceChar* ')'
EmailAddressValue <- 'email' '(' WhitespaceChar* TextValue WhitespaceChar* ')'
UrlValue <- 'url' '(' WhitespaceChar* TextValue WhitespaceChar* (',' WhitespaceChar* TextValue WhitespaceChar*)? ')'
```

---

#### A.2.8 Text Values

> This grammar is an informative projection of the quoted text spelling rules defined in §5.1. In case of discrepancy, §5.1 is authoritative.

```peg
TextValue <- '"' TextCharacter* '"'
TextCharacter <- EscapeSequence / UnescapedTextCharacter
UnescapedTextCharacter <- !["\n] .
EscapeSequence <- '\\' ( '"' / '\\' / UnicodeEscape )
UnicodeEscape <- 'u' HexDigit HexDigit HexDigit HexDigit
             / 'u{' HexDigit+ '}'
HexDigit <- [0-9A-Fa-f]
```

---

#### A.2.9 Character Values

> This grammar is an informative projection of the character literal spelling rules defined in §5.11. In case of discrepancy, §5.11 is authoritative.

```peg
CharValue <- "'" CharContent "'"
CharContent <- CharEscapeSequence / UnescapedChar
UnescapedChar <- !['\\\n] .
CharEscapeSequence <- '\\' ( ['\\nrt] / UnicodeEscape )
```

---

#### A.2.10 Backtick Text

> This grammar is an informative projection of the backtick text spelling rules defined in §5.2. In case of discrepancy, §5.2 is authoritative.

```peg
BacktickText <- '`' BacktickChar* '`'
BacktickChar <- BacktickEscape / (!'`' .)
BacktickEscape <- '\\' '`'
```

---

#### A.2.11 Boolean Values

> This grammar is an informative projection of the Boolean Value spelling rules defined in §5.3. In case of discrepancy, §5.3 is authoritative.

```peg
BooleanValue <- 'true' / 'false'
```

---

#### A.2.12 Numeric Values

> This grammar is an informative projection of the numeric value spelling rules defined in §5.4. In case of discrepancy, §5.4 is authoritative.

```peg
NumericValue <- ComplexNumber
             / ImaginaryNumber
             / Fraction
             / Infinity
             / PrecisionNumber
             / ExponentialNumber
             / DecimalNumber
             / Integer

ComplexNumber <- (Integer / DecimalNumber) ([+-]) (Integer / DecimalNumber) 'i'
ImaginaryNumber <- (Integer / DecimalNumber) 'i'
Fraction <- Integer '/' IntegerDigits
PrecisionNumber <- DecimalNumber 'p' IntegerDigits?
ExponentialNumber <- (Integer / DecimalNumber) [eE] Sign? IntegerDigits
DecimalNumber <- '-'? IntegerDigits '.' DigitSequence
Infinity <- PositiveInfinity / NegativeInfinity
PositiveInfinity <- 'Infinity'
NegativeInfinity <- '-' 'Infinity'

Integer <- '0' / '-'? NonZeroDigit Digit*

Sign <- [+-]
NonZeroDigit <- [1-9]
DigitSequence <- Digit+
IntegerDigits <- '0' / NonZeroDigit Digit*
```

---

#### A.2.13 Enumerated Tokens

> This grammar is an informative projection of the Enumerated Token spelling rules defined in §5.5 and the parameterized type syntax defined in §5.18. In case of discrepancy, §5.5 and §5.18 are authoritative.

```peg
EnumeratedToken <- '$' UppercaseLetter (Letter / Digit)* TypeParameters?

TypeParameters <- '<' TypeArgument (',' ' ' TypeArgument)* '>'

TypeArgument <- EnumeratedToken / TypeUnion

TypeUnion <- '[' EnumeratedToken (',' ' ' EnumeratedToken)* ']'
```

---

#### A.2.14 Lookup Tokens

> This grammar is an informative projection of the Lookup Token spelling rules defined in §5.10. In case of discrepancy, §5.10 is authoritative.

```peg
LookupToken <- '~' LowercaseLetter (Letter / Digit)*
```

---

#### A.2.15 Temporal Values

> This grammar is an informative projection of the spelling rules defined in §5.6.2. In case of discrepancy, §5.6.2 is authoritative.

```peg
TemporalValue <- '{' TemporalBody '}'

TemporalBody <- ZonedDateTime / Instant / PlainDateTime / PlainDate / YearWeek / PlainYearMonth / PlainMonthDay / PlainTime / Duration / TemporalKeyword

PlainDate <- Year '-' Month '-' Day
YearWeek <- Year '-' [Ww] WeekNumber
WeekNumber <- Digit Digit
PlainYearMonth <- Year '-' Month
PlainMonthDay <- Month '-' Day

PlainDateTime <- PlainDate 'T' PlainTime
Instant <- PlainDateTime TimeZoneOffset
ZonedDateTime <- PlainDateTime TimeZoneOffset TimeZoneId

TimeZoneOffset <- 'Z' / ([+-] Hour ':' Minute)
TimeZoneId <- '[' TimeZoneIdChar+ ']'
TimeZoneIdChar <- Letter / Digit / '/' / '_' / '-'

PlainTime <- Hour ':' Minute (':' Second ('.' FractionalSeconds)?)?

Duration <- 'P' DurationComponent+ ('T' TimeDurationComponent+)?
          / 'P' 'T' TimeDurationComponent+
DurationComponent <- DigitSequence [YMWD]
TimeDurationComponent <- DigitSequence ('.' DigitSequence)? [HMS]

TemporalKeyword <- 'now' / 'today'

Year <- Digit Digit Digit Digit
Month <- Digit Digit
Day <- Digit Digit
Hour <- Digit Digit
Minute <- Digit Digit
Second <- Digit Digit
FractionalSeconds <- Digit+
```

---

#### A.2.16 List Values

> This grammar is an informative projection of the List Value spelling rules defined in §5.12. In case of discrepancy, §5.12 is authoritative.

```peg
# Lists permit arbitrary whitespace (including newlines) between tokens.

ListValue <- '[' WhitespaceChar* ListItems? WhitespaceChar* ']'
ListItems <- Value (WhitespaceChar* ',' WhitespaceChar* Value)*
```

---

#### A.2.17 Set Values

> This grammar is an informative projection of the Set Value spelling rules defined in §5.14. In case of discrepancy, §5.14 is authoritative.

```peg
SetValue <- 'set' '[' WhitespaceChar* SetItems? WhitespaceChar* ']'
SetItems <- Value (WhitespaceChar* ',' WhitespaceChar* Value)*
```

---

#### A.2.18 Map Values

> This grammar is an informative projection of the Map Value spelling rules defined in §5.15. In case of discrepancy, §5.15 is authoritative.

```peg
MapValue <- 'map' '[' WhitespaceChar* MapItems? WhitespaceChar* ']'
MapItems <- MapEntry (WhitespaceChar* ',' WhitespaceChar* MapEntry)*
MapEntry <- MapKey WhitespaceChar* ':' WhitespaceChar* Value
MapKey <- MapIdentifier / TextValue / CharValue / Integer / EnumeratedToken / IriReference
MapIdentifier <- LowercaseLetter (Letter / Digit)*
```

---

#### A.2.19 Record Values

> This grammar is an informative projection of the Record Value spelling rules defined in §5.19. In case of discrepancy, §5.19 is authoritative.

```peg
RecordValue <- 'record' '[' WhitespaceChar* RecordItems? WhitespaceChar* ']'
RecordItems <- RecordEntry (WhitespaceChar* ',' WhitespaceChar* RecordEntry)*
RecordEntry <- RecordFieldName WhitespaceChar* ':' WhitespaceChar* Value
RecordFieldName <- LowercaseLetter (Letter / Digit)*
```

---

#### A.2.20 Tuple Values

> This grammar is an informative projection of the Tuple Value spelling rules defined in §5.16. In case of discrepancy, §5.16 is authoritative.

```peg
TupleValue <- '(' WhitespaceChar* TupleItems WhitespaceChar* ')'
TupleItems <- Value (WhitespaceChar* ',' WhitespaceChar* Value)*
```

---

#### A.2.21 Range Values

> This grammar is an informative projection of the Range Value spelling rules defined in §5.17. In case of discrepancy, §5.17 is authoritative.

```peg
RangeValue <- RangeStart WhitespaceChar* '..' WhitespaceChar* RangeEnd (WhitespaceChar* 's' WhitespaceChar* StepValue)?
RangeStart <- TemporalValue / CharValue / OrderedNumericValue
RangeEnd <- TemporalValue / CharValue / OrderedNumericValue
StepValue <- TemporalValue / OrderedNumericValue
OrderedNumericValue <- PrecisionNumber / ExponentialNumber / Fraction / DecimalNumber / Integer
```

---

#### A.2.22 UUID Values

> This grammar is an informative projection of the UUID spelling rules defined in §5.8. In case of discrepancy, §5.8 is authoritative.

```peg
UuidValue <- HexOctet HexOctet HexOctet HexOctet '-' HexOctet HexOctet '-' HexOctet HexOctet '-' HexOctet HexOctet '-' HexOctet HexOctet HexOctet HexOctet HexOctet HexOctet
HexOctet <- HexDigit HexDigit
```

---

#### A.2.23 Color Values

> This grammar is an informative projection of the color function argument spelling rules and semantic domains defined in §5.7.4. In case of discrepancy, §5.7.4 is authoritative.

```peg
# Color spellings are accepted as declarative literals; semantic validity is checked
# during schema-driven semantic validation (§5.7).

ColorValue <- HexColor / FunctionColor / NamedColor

FunctionColor <- RgbFunction / HslFunction / HwbFunction / LabFunction / LchFunction / OklabFunction / OklchFunction / ColorSpaceColorFunction / ColorMixFunction / DeviceCmykFunction / RelativeColorFunction

HexColor <- '#' (HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit
              / HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit
              / HexDigit HexDigit HexDigit HexDigit
              / HexDigit HexDigit HexDigit)

NamedColor <- '&' [a-z]+

ColorWhitespaceOptional <- [ \t]*
ColorWhitespace <- [ \t]+

# Real-number subset of NumericValue used in color function arguments.
ColorRealNumber <- Fraction / Infinity / PrecisionNumber / ExponentialNumber / DecimalNumber / Integer
ColorPercentage <- ColorRealNumber '%'
ColorAlpha <- ColorPercentage / ColorRealNumber

ColorComma <- ColorWhitespaceOptional ',' ColorWhitespaceOptional

RgbComponent <- ColorPercentage / ColorRealNumber
HueComponent <- ColorRealNumber

RgbColorSpace <- 'srgb-linear' / 'srgb' / 'display-p3' / 'a98-rgb' / 'prophoto-rgb' / 'rec2020'
XyzColorSpace <- 'xyz-d50' / 'xyz-d65' / 'xyz'
ColorSpace <- RgbColorSpace / XyzColorSpace

ColorRgbArguments <- RgbComponent ColorWhitespace RgbComponent ColorWhitespace RgbComponent (ColorWhitespaceOptional '/' ColorWhitespaceOptional ColorAlpha)?
ColorXyzArguments <- ColorRealNumber ColorWhitespace ColorRealNumber ColorWhitespace ColorRealNumber (ColorWhitespaceOptional '/' ColorWhitespaceOptional ColorAlpha)?

ColorSpaceColorFunction <- 'color' '(' ColorWhitespaceOptional (RgbColorSpace ColorWhitespace ColorRgbArguments / XyzColorSpace ColorWhitespace ColorXyzArguments) ColorWhitespaceOptional ')'

RgbFunction <- ('rgb' / 'rgba') '(' ColorWhitespaceOptional RgbArguments ColorWhitespaceOptional ')'
RgbArguments <- RgbLegacyArguments / RgbModernArguments
RgbLegacyArguments <- RgbComponent ColorComma RgbComponent ColorComma RgbComponent (ColorComma ColorAlpha)?
RgbModernArguments <- RgbComponent ColorWhitespace RgbComponent ColorWhitespace RgbComponent (ColorWhitespaceOptional '/' ColorWhitespaceOptional ColorAlpha)?

HslFunction <- ('hsl' / 'hsla') '(' ColorWhitespaceOptional HslArguments ColorWhitespaceOptional ')'
HslArguments <- HslLegacyArguments / HslModernArguments
HslLegacyArguments <- HueComponent ColorComma ColorPercentage ColorComma ColorPercentage (ColorComma ColorAlpha)?
HslModernArguments <- HueComponent ColorWhitespace ColorPercentage ColorWhitespace ColorPercentage (ColorWhitespaceOptional '/' ColorWhitespaceOptional ColorAlpha)?

HwbFunction <- 'hwb' '(' ColorWhitespaceOptional HwbArguments ColorWhitespaceOptional ')'
HwbArguments <- HueComponent ColorWhitespace ColorPercentage ColorWhitespace ColorPercentage (ColorWhitespaceOptional '/' ColorWhitespaceOptional ColorAlpha)?

LabFunction <- 'lab' '(' ColorWhitespaceOptional LabArguments ColorWhitespaceOptional ')'
LabArguments <- ColorPercentage ColorWhitespace ColorRealNumber ColorWhitespace ColorRealNumber (ColorWhitespaceOptional '/' ColorWhitespaceOptional ColorAlpha)?

LchFunction <- 'lch' '(' ColorWhitespaceOptional LchArguments ColorWhitespaceOptional ')'
LchArguments <- ColorPercentage ColorWhitespace ColorRealNumber ColorWhitespace ColorRealNumber (ColorWhitespaceOptional '/' ColorWhitespaceOptional ColorAlpha)?

OklabFunction <- 'oklab' '(' ColorWhitespaceOptional OklabArguments ColorWhitespaceOptional ')'
OklabArguments <- ColorRealNumber ColorWhitespace ColorRealNumber ColorWhitespace ColorRealNumber (ColorWhitespaceOptional '/' ColorWhitespaceOptional ColorAlpha)?

OklchFunction <- 'oklch' '(' ColorWhitespaceOptional OklchArguments ColorWhitespaceOptional ')'
OklchArguments <- ColorRealNumber ColorWhitespace ColorRealNumber ColorWhitespace ColorRealNumber (ColorWhitespaceOptional '/' ColorWhitespaceOptional ColorAlpha)?

CmykComponent <- ColorPercentage / ColorRealNumber

DeviceCmykFunction <- 'device-cmyk' '(' ColorWhitespaceOptional DeviceCmykArguments ColorWhitespaceOptional ')'
DeviceCmykArguments <- CmykComponent ColorWhitespace CmykComponent ColorWhitespace CmykComponent ColorWhitespace CmykComponent (ColorWhitespaceOptional '/' ColorWhitespaceOptional ColorAlpha)?

ColorMixFunction <- 'color-mix' '(' ColorWhitespaceOptional 'in' ColorWhitespace ColorSpace ColorComma ColorMixStop (ColorComma ColorMixStop)+ ColorWhitespaceOptional ')'
ColorMixStop <- ColorValue (ColorWhitespace ColorPercentage)?

RelativeColorFunction <- RelativeRgbFunction / RelativeHslFunction / RelativeHwbFunction / RelativeLabFunction / RelativeLchFunction / RelativeOklabFunction / RelativeOklchFunction / RelativeColorSpaceColorFunction

RelativeAlphaComponent <- ColorAlpha / 'a'

RelativeRgbChannel <- 'r' / 'g' / 'b'
RelativeRgbComponent <- RgbComponent / RelativeRgbChannel
RelativeRgbArguments <- RelativeRgbComponent ColorWhitespace RelativeRgbComponent ColorWhitespace RelativeRgbComponent (ColorWhitespaceOptional '/' ColorWhitespaceOptional RelativeAlphaComponent)?
RelativeRgbFunction <- ('rgb' / 'rgba') '(' ColorWhitespaceOptional 'from' ColorWhitespace ColorValue ColorWhitespace RelativeRgbArguments ColorWhitespaceOptional ')'

RelativeHslArguments <- (HueComponent / 'h') ColorWhitespace (ColorPercentage / 's') ColorWhitespace (ColorPercentage / 'l') (ColorWhitespaceOptional '/' ColorWhitespaceOptional RelativeAlphaComponent)?
RelativeHslFunction <- ('hsl' / 'hsla') '(' ColorWhitespaceOptional 'from' ColorWhitespace ColorValue ColorWhitespace RelativeHslArguments ColorWhitespaceOptional ')'

RelativeHwbArguments <- (HueComponent / 'h') ColorWhitespace (ColorPercentage / 'w') ColorWhitespace (ColorPercentage / 'b') (ColorWhitespaceOptional '/' ColorWhitespaceOptional RelativeAlphaComponent)?
RelativeHwbFunction <- 'hwb' '(' ColorWhitespaceOptional 'from' ColorWhitespace ColorValue ColorWhitespace RelativeHwbArguments ColorWhitespaceOptional ')'

RelativeLabArguments <- (ColorPercentage / 'l') ColorWhitespace (ColorRealNumber / 'a') ColorWhitespace (ColorRealNumber / 'b') (ColorWhitespaceOptional '/' ColorWhitespaceOptional RelativeAlphaComponent)?
RelativeLabFunction <- 'lab' '(' ColorWhitespaceOptional 'from' ColorWhitespace ColorValue ColorWhitespace RelativeLabArguments ColorWhitespaceOptional ')'

RelativeLchArguments <- (ColorPercentage / 'l') ColorWhitespace (ColorRealNumber / 'c') ColorWhitespace (ColorRealNumber / 'h') (ColorWhitespaceOptional '/' ColorWhitespaceOptional RelativeAlphaComponent)?
RelativeLchFunction <- 'lch' '(' ColorWhitespaceOptional 'from' ColorWhitespace ColorValue ColorWhitespace RelativeLchArguments ColorWhitespaceOptional ')'

RelativeOklabArguments <- (ColorRealNumber / 'l') ColorWhitespace (ColorRealNumber / 'a') ColorWhitespace (ColorRealNumber / 'b') (ColorWhitespaceOptional '/' ColorWhitespaceOptional RelativeAlphaComponent)?
RelativeOklabFunction <- 'oklab' '(' ColorWhitespaceOptional 'from' ColorWhitespace ColorValue ColorWhitespace RelativeOklabArguments ColorWhitespaceOptional ')'

RelativeOklchArguments <- (ColorRealNumber / 'l') ColorWhitespace (ColorRealNumber / 'c') ColorWhitespace (ColorRealNumber / 'h') (ColorWhitespaceOptional '/' ColorWhitespaceOptional RelativeAlphaComponent)?
RelativeOklchFunction <- 'oklch' '(' ColorWhitespaceOptional 'from' ColorWhitespace ColorValue ColorWhitespace RelativeOklchArguments ColorWhitespaceOptional ')'

RelativeColorChannel <- 'r' / 'g' / 'b' / 'x' / 'y' / 'z'
RelativeColorComponent <- ColorPercentage / ColorRealNumber / RelativeColorChannel
RelativeColorArguments <- RelativeColorComponent ColorWhitespace RelativeColorComponent ColorWhitespace RelativeColorComponent (ColorWhitespaceOptional '/' ColorWhitespaceOptional RelativeAlphaComponent)?
RelativeColorSpaceColorFunction <- 'color' '(' ColorWhitespaceOptional 'from' ColorWhitespace ColorValue ColorWhitespace ColorSpace ColorWhitespace RelativeColorArguments ColorWhitespaceOptional ')'
```

---

#### A.2.24 IRI References

> This grammar is an informative projection of the IRI reference spelling rules defined in §5.9. In case of discrepancy, §5.9 is authoritative.

```peg
# IRI references are fallback unquoted values that contain ':'.
# Exact RFC 3987 profiling is enforced by surface-form validation, not this PEG.

IriReference <- IriScheme ':' IriTokenBody
IriScheme <- Letter (Letter / Digit / [+\-\.])*
IriTokenBody <- IriTokenChar*
IriTokenChar <- !ValueTerminator .
```

---

#### A.2.25 Annotations

> This grammar is an informative projection of the annotation rules defined in §8.9. In case of discrepancy, §8.9 is authoritative.

```peg
Annotation <- AnnotationLine / AnnotationBlock

AnnotationLine <- Indentation '[' AnnotationChar* ']' Newline

AnnotationBlock <- Indentation '[' Newline AnnotationBlockLine* Indentation ']' Newline

AnnotationBlockLine <- !(Indentation ']' Newline) Indentation AnnotationBlockChar* Newline

AnnotationChar <- AnnotationEscape / UnescapedAnnotationChar
UnescapedAnnotationChar <- !(']' / '\n') .
AnnotationEscape <- '\\' ('\\' / ']')

AnnotationBlockChar <- AnnotationEscape / UnescapedAnnotationBlockChar
UnescapedAnnotationBlockChar <- !'\n' .
```

---

#### A.2.26 Whitespace and Structural Elements

> This grammar is an informative projection of the whitespace and structural rules defined in §8.2 (line endings), §8.3 (indentation), and §8.4 (blank lines). In case of discrepancy, those sections are authoritative.

```peg
Newline <- '\n'

WhitespaceChar <- [ \t\n]
Whitespace <- WhitespaceChar+

WhitespaceNoNewlineChar <- [ \t]
WhitespaceNoNewline <- WhitespaceNoNewlineChar+

BlankLine <- Newline

Indentation <- '\t'*

# Conservative terminators for unquoted tokens in markers:
ValueTerminator <- [ \t\n] / '/>' / '>'
```

---

#### A.2.27 End of File

```peg
EOF <- !.
```

---

## Appendix B. Codex Named Colors
This appendix defines the exhaustive set of named color keywords permitted in Codex Named Color Values (§5.7). A color name is valid if and only if it appears in this appendix.

Aliases and duplicates (for example, `gray`/`grey`, `cyan`/`aqua`) are intentional and are part of the Codex named color set.

### B.1 Named Color Keyword Table

Each entry defines a valid Codex Named Color Value (`&name`).

During schema-driven semantic validation (§5.7), a Named Color Value MUST be interpreted as the sRGB color given by its `sRGB hex` value in this table:

- A 6-digit hex form `#RRGGBB` is interpreted as the corresponding sRGB color with `alpha=1`.
- An 8-digit hex form `#RRGGBBAA` is interpreted as the corresponding sRGB color with the given alpha byte.

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
| `&transparent`          | `#00000000` |
| `&turquoise`            | `#40e0d0` |
| `&violet`               | `#ee82ee` |
| `&wheat`                | `#f5deb3` |
| `&white`                | `#ffffff` |
| `&whitesmoke`           | `#f5f5f5` |
| `&yellow`               | `#ffff00` |
| `&yellowgreen`          | `#9acd32` |

---

**End of Codex Language Specification v1.0.0**
