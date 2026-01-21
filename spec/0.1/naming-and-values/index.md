Status: NORMATIVE  
Lock State: UNLOCKED    
Version: 0.1  
Editor: Charles F. Munat

# Codex Naming and Value Specification — Version 0.1

This specification defines the **core surface vocabulary**, **naming rules**, and
**literal value spellings** of the Codex language.

It is **language-level and core**.
It defines vocabulary and literal forms. Semantics are schema responsibilities.

---

## 1. Purpose

This specification defines **how things are named** and **how literal data is written**
in Codex.

Its goals are to:

* make Codex read as structured, precise English
* prevent ambiguity for humans and machines
* support ontology authoring, configuration, and data interchange
* provide **first-class data values**, not string encodings
* keep naming and value rules consistent with the Codex language invariants
	(`spec/0.1/language/index.md`)

This document governs **naming and literal values only**.

---

## 2. Core Surface Vocabulary (Normative)

### 2.1 Concept

A **Concept** is the primary surface construct in Codex.

A Concept:

* has a name
* may declare Traits
* may contain Content
* may contain child Concepts
* is purely declarative

A Concept is **not** an element, component, tag, node, class, or object.

---

### 2.2 Trait

A **Trait** binds a name to a Value.

Traits:

* are declared inline on Concepts
* are schema-authorized
* have no independent identity
* are immutable once declared

Traits are **not properties, props, attributes, fields, or parameters**.

---

### 2.3 Value

A **Value** is a literal datum.

Values are:

* declarative
* immutable
* not expressions
* not evaluated by Codex
* parsed mechanically

Codex defines a rich set of **first-class literal value spellings**.

---

### 2.4 Content

**Content** is opaque narrative material.

Content:

* is opaque to Codex
* may contain prose, markup, code, or other text
* exists only inside Concepts
* is preserved verbatim (after indentation normalization)

Content is distinct from Values. This distinction prevents conflating **data** with **text**.

---

### 2.5 Entity

A Concept instance is an **Entity if and only if it declares an `id` Trait and the active schema permits or requires Entity identity via `entityEligibility`**.

The schema controls Entity eligibility; the `id` Trait is the mechanism. See the **Schema Definition Specification § 4.1** for `entityEligibility` rules.

Entities:

* represent **high semantic density**
* participate in ontologies and graphs
* may be referenced by other Concepts

---

### 2.6 Marker

A **Marker** is a syntactic delimiter for Concept instances in the surface form.

Markers include:

* opening markers (e.g., `<Recipe>`)
* closing markers (e.g., `</Recipe>`)
* self-closing markers (e.g., `<Ingredient />`)

Markers are **not** tags, start tags, end tags, open tags, or close tags.

---

### 2.7 Annotation

An **Annotation** is a non-normative, author-supplied note preserved through the Codex pipeline.

Annotations:

* do not affect validation
* do not alter domain semantics
* are preserved for round-tripping and tooling

Annotations are **not** comments, code comments, inline comments, XML comments, or HTML comments.

---

## 3. Naming Rules (Normative)

### 3.1 Casing

* **Concept names** MUST use **PascalCase**
* **Trait names** MUST use **camelCase**

Forbidden everywhere:

* kebab-case
* snake_case
* SCREAMING_CASE
* mixed or inconsistent casing
* any other casing (sentence, title, Train-Case, etc.)

---

### 3.2 Abbreviation Categories

Three categories of shortened forms exist:

**Abbreviation**: A shortened form of a word or phrase.
Example: "etc." for "et cetera."

**Initialism**: An abbreviation formed from the initial letters of words in a phrase.
Examples: "FBI", "CIA", "NASA", "IRS."

**Acronym**: An initialism designed to be pronounceable as a word, sometimes incorporating letters beyond strict initials.
Examples: "RADAR" (Radio Detection And Ranging), "COMSUBPAC" (Commander Submarines Pacific), "MADD" (Mothers Against Drunk Driving).

The hierarchy is: Abbreviation ⊃ Initialism ⊃ Acronym.

---

### 3.3 Initialisms and Acronyms (Permitted)

Initialisms and acronyms are **always permitted** in Codex names.

Capitalization rule: Treat them as ordinary words. Capitalize only the first letter.

Valid examples:

* `Url` — not `URL`
* `Iri` — not `IRI`
* `Isbn` — not `ISBN`
* `HttpRequest` — not `HTTPRequest`
* `AstNode` — not `ASTNode`
* `JsonParser` — not `JSONParser`

Invalid examples:

* `ASTNode` — should be `AstNode`
* `HTMLParser` — should be `HtmlParser`
* `plainHTML` — should be `plainHtml`

---

### 3.4 General Abbreviations (Forbidden)

General abbreviations are **forbidden** in Codex names. Write the full word.

Examples:

* `definition` — not `def`
* `reference` — not `ref`
* `configuration` — not `cfg` or `config`
* `identifier` — not `ident`
* `specification` — not `spec`

Periods are never permitted in names.

**Schema-level exceptions**: Schemas MAY whitelist specific general abbreviations for their domain. Such exceptions are schema-scoped and do not affect core Codex naming rules.

---

## 4. Literal Value Spellings (Normative)

Codex defines the following **literal value forms**.

Codex **parses** these values but **does not evaluate or interpret them**.
Typing and semantics are schema responsibilities.

**Clarification on normalization:**

* Codex does **not** normalize numeric spellings (`1.0` stays `1.0`, not `1`)
* Codex does **not** perform arithmetic or type conversion
* Codex **does** enforce structural constraints (set uniqueness, map key uniqueness)
* Codex **does** canonicalize certain forms (UUID case, backtick whitespace)

---

### 4.1 String Values

A **String Value** is a sequence of Unicode scalar values.

Syntax: See **Surface Form Specification § 13** for literal syntax and escape sequences.

---

### 4.2 Backtick Strings

A **Backtick String** is a multiline authoring convenience that collapses to a single-line string.

Syntax: See **Surface Form Specification § 14** for literal syntax, whitespace handling, and escape sequences.

Backtick strings are for authoring convenience. If a Trait value requires significant text, consider whether it should be Content instead.

---

### 4.3 Boolean Values

```text
true
false
```

---

### 4.4 Numeric Values

Numeric literals are declarative spellings.

Supported:

* integers (`7`, `-42`)
* decimals (`3.14`)
* scientific notation (`1.2e6`)
* infinities (`Infinity`, `-Infinity`)
* fractions (`3/4`)
* imaginary numbers (`2i`, `3.5i`)
* complex numbers (`2+3i`, `1.5-2.5i`)
* precision-significant numbers (see below)

Codex performs **no arithmetic and no numeric normalization** (spellings are preserved exactly).

#### 4.4.1 Precision-Significant Numbers

Precision-significant numbers are marked with a `p` suffix.

The precision (number of significant decimal places) is determined by:

1. **Inferred precision**: Count of decimal places in the literal, including trailing zeros
2. **Explicit precision**: An integer following the `p` suffix

Examples:

* `3.1415p` — precision 4 (inferred from 4 decimal places)
* `3.141500p` — precision 6 (trailing zeros count)
* `3.1415p6` — precision 6 (explicit override)
* `2.0p` — precision 1
* `2.00p` — precision 2

The `p` suffix indicates that precision is semantically significant.
Consuming systems MUST preserve the declared precision.

---

### 4.5 Enumerated Token Values

```text
$Identifier
```

* drawn from schema-defined closed sets
* not strings
* not evaluated

---

### 4.6 List Values

```text
[ value, value, ... ]
```

Rules:

* ordered
* may be empty
* may be nested
* may mix value types
* no implicit expansion

---

### 4.7 Set Values

```text
set[ value, value, ... ]
```

Rules:

* unordered
* unique values (duplicates are ignored)
* may be empty
* may be nested
* may mix value types
* values can be any value type

Examples:

* `set[$Featured, $Sale, $New]` — enumerated tokens
* `set["red", "green", "blue"]` — strings
* `set[1, 2, 3]` — integers
* `set[map[a: 1], map[b: 2]]` — nested maps

---

### 4.8 Map Values

```text
map[ key: value, key: value, ... ]
```

Rules:

* key-value pairs
* keys are unique (duplicate keys are errors)
* may be empty
* may be nested
* values can be any value type

#### 4.8.1 Map Keys

Keys may be:

* unquoted identifiers: `name`, `red`, `foo42`
* strings: `"hello world"`
* characters: `'A'`
* integers: `42`
* enumerated tokens: `$Red`

Unquoted identifiers:

* MUST start with a lowercase letter
* MAY contain letters (a-z, A-Z) and digits (0-9)
* MUST NOT contain whitespace, punctuation, hyphens, or underscores

Examples:

* `map[name: "John", age: 30]` — unquoted identifier keys
* `map["first name": "John", "last name": "Doe"]` — string keys with spaces
* `map[$Red: "#ff0000", $Green: "#00ff00"]` — enumerated token keys
* `map[en: "Hello", es: "Hola", fr: "Bonjour"]` — localization

---

### 4.9 Tuple Values

```text
( value, value, ... )
```

Rules:

* ordered
* fixed length (schema-defined)
* positional semantics (position determines meaning)
* may mix value types (heterogeneous)
* values can be any value type
* MUST contain at least one value

Tuples differ from lists:

* Lists have iteration semantics; tuples have positional semantics
* Lists are typically homogeneous; tuples are typically heterogeneous
* List length is variable; tuple length is fixed by schema

Examples:

* `(10, 20)` — 2D coordinates (x, y)
* `(10, 20, 30)` — 3D coordinates (x, y, z)
* `("John", "Doe", 30)` — person record (first, last, age)
* `((0, 0), (100, 100))` — nested tuples (bounding box)

---

### 4.10 Range Values

```text
start..end
start..endsStep
```

Where:

* `start` and `end` are values of the same type
* `..` separates the endpoints (no surrounding spaces)
* `s` is a keyword meaning "step" (no surrounding spaces)
* `step` is a value appropriate to the range type

Ranges are **declarative intervals**.

* inclusive endpoints
* not enumerated by Codex
* semantics are schema-defined

#### 4.10.1 Numeric Ranges

Start and end are numeric values. Step is a numeric value.

Examples:

* `1..10` — range from 1 to 10
* `1..100s5` — range from 1 to 100, step 5
* `0.0..1.0s0.1` — range from 0.0 to 1.0, step 0.1
* `-10..10s2` — range from -10 to 10, step 2

#### 4.10.2 Temporal Ranges

Start and end are temporal values. Step is a duration.

Examples:

* `{2024-01-01}..{2024-12-31}` — date range
* `{2024-01-01}..{2024-12-31}s{P1D}` — date range, step 1 day
* `{2024-01}..{2024-12}s{P1M}` — year-month range, step 1 month
* `{09:00}..{17:00}s{PT1H}` — time range, step 1 hour

#### 4.10.3 Character Ranges

Start and end are single-character values. Step is a numeric value (code point increment).

Examples:

* `'A'..'Z'` — uppercase letters
* `'A'..'Z's2` — A, C, E, G, ...
* `'a'..'z's1` — lowercase letters
* `'0'..'9'` — digits

---

### 4.11 Temporal Values

Temporal literals are written in `{}`.

Supported spellings:

* `{YYYY-MM}` — Year-Month
* `{MM-DD}` — Month-Day
* `{YYYY-MM-DD}` — Date
* `{hh:mm}` or `{hh:mm:ss(.sss)?}` — Time
* `{YYYY-MM-DDThh:mm(:ss(.sss)?)?}` — Local Date-Time
* `{YYYY-MM-DDThh:mm(:ss(.sss)?)?Z}` — Zoned Date-Time (UTC)
* `{YYYY-MM-DDThh:mm(:ss(.sss)?)?±hh:mm}` — Zoned Date-Time (offset)
* `{YYYY-MM-DDThh:mm(:ss(.sss)?)?±hh:mm[TimeZone]}` — Zoned Date-Time (offset with IANA timezone)
* `{P...}` — Duration
* `{now}`, `{today}` — Reserved literals

#### 4.11.1 Zoned Date-Time

Zoned date-time values include timezone information via offset and optional IANA timezone identifier.

Forms:

* UTC: `{2024-01-15T09:30:00Z}`
* Offset: `{2024-01-15T09:30:00+05:30}`
* Offset with timezone: `{2024-01-15T09:30:00+05:30[Asia/Kolkata]}`

The timezone identifier uses IANA Time Zone Database names (e.g., `America/New_York`, `Europe/London`, `Asia/Kolkata`).

Codex parses zoned date-time values but does **not** perform timezone conversion or validation.

---

### 4.12 Color Values

Colors are **first-class values**, not strings.

Codex parses color literals but does not validate, normalize, or convert them.

#### 4.12.1 Hexadecimal Colors

```text
#RGB
#RGBA
#RRGGBB
#RRGGBBAA
```

Examples:

* `#f80` — 3-digit (RGB)
* `#f80a` — 4-digit (RGBA)
* `#ff8800` — 6-digit (RRGGBB)
* `#ff8800aa` — 8-digit (RRGGBBAA)

Hex digits are case-insensitive. Canonical form is lowercase.

#### 4.12.2 RGB Colors

Legacy (comma-separated):

```text
rgb(red, green, blue)
rgba(red, green, blue, alpha)
```

Modern (space-separated):

```text
rgb(red green blue)
rgb(red green blue / alpha)
```

Examples:

* `rgb(255, 128, 0)` — legacy
* `rgba(255, 128, 0, 0.5)` — legacy with alpha
* `rgb(255 128 0)` — modern
* `rgb(255 128 0 / 50%)` — modern with alpha

#### 4.12.3 HSL Colors

Legacy (comma-separated):

```text
hsl(hue, saturation, lightness)
hsla(hue, saturation, lightness, alpha)
```

Modern (space-separated):

```text
hsl(hue saturation lightness)
hsl(hue saturation lightness / alpha)
```

Examples:

* `hsl(30, 100%, 50%)` — legacy
* `hsla(30, 100%, 50%, 0.5)` — legacy with alpha
* `hsl(30 100% 50%)` — modern
* `hsl(30 100% 50% / 50%)` — modern with alpha

#### 4.12.4 Lab and LCH Colors

```text
lab(lightness a b)
lab(lightness a b / alpha)
lch(lightness chroma hue)
lch(lightness chroma hue / alpha)
```

Examples:

* `lab(70% 20 -30)`
* `lch(70% 45 30)`
* `lch(70% 45 30 / 50%)`

#### 4.12.5 OKLab and OKLCH Colors

```text
oklab(lightness a b)
oklab(lightness a b / alpha)
oklch(lightness chroma hue)
oklch(lightness chroma hue / alpha)
```

Examples:

* `oklab(0.7 -0.1 0.1)`
* `oklch(0.7 0.15 180)`
* `oklch(0.7 0.15 180 / 50%)`

#### 4.12.6 Color Function (Wide Gamut)

```text
color(colorspace c1 c2 c3)
color(colorspace c1 c2 c3 / alpha)
```

Supported color spaces include:

* `srgb`
* `srgb-linear`
* `display-p3`
* `a98-rgb`
* `prophoto-rgb`
* `rec2020`
* `xyz`, `xyz-d50`, `xyz-d65`

Examples:

* `color(display-p3 1 0.5 0)`
* `color(srgb 1 0.5 0 / 50%)`
* `color(rec2020 0.7 0.2 0.1)`

#### 4.12.7 Named Colors

Named colors MUST be written as string values:

```text
"red"
"rebeccapurple"
"transparent"
```

Named colors are **not** unquoted tokens.

---

### 4.13 UUID Values

UUID literals are written in standard 8-4-4-4-12 hexadecimal format:

```text
xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

Example:

```text
550e8400-e29b-41d4-a716-446655440000
```

Rules:

* UUIDs are **not** strings (no quotes)
* UUIDs contain **no** braces or prefixes
* UUIDs are case-insensitive
* Canonical form is **lowercase**
* Hyphens are **required** at positions 9, 14, 19, 24
* No UUID version is mandated

Valid:

* `550e8400-e29b-41d4-a716-446655440000` — canonical
* `550E8400-E29B-41D4-A716-446655440000` — valid, normalizes to lowercase

Invalid:

* `"550e8400-e29b-41d4-a716-446655440000"` — this is a string, not a UUID
* `{550e8400-e29b-41d4-a716-446655440000}` — braces forbidden
* `550e840029b41d4a716446655440000` — hyphens required

---

### 4.14 IRI Reference Values

IRI reference values are **unquoted tokens** representing identity or reference.

Used by the following Traits:

* `id` — entity identity
* `reference` — explicit reference to another entity
* `target` — explicit target of a relationship

The `for` trait accepts either IRI references or Lookup Tokens (see § 4.15).

IRI references:

* MUST be valid IRIs
* MUST contain a ':' separating the scheme from the remainder
* MAY contain non-ASCII Unicode characters directly (RFC 3987 IRI-reference)
* Percent-encoding MAY be used, but is not required at the Codex surface layer
* MUST NOT contain Unicode whitespace characters
* MUST NOT contain Unicode control characters
* MUST NOT contain Unicode bidirectional control characters
* MUST NOT contain Unicode private-use characters
* are **not** strings (no quotes)
* are compared as opaque strings
* are **not** resolved or dereferenced by Codex

Examples:

* `recipe:spaghetti`
* `book:the-hobbit`
* `https://example.org/resource/123`

---

### 4.15 Lookup Token Values

Lookup token values are **shorthand references** to Concepts.

Surface form:

```text
~token
```

Usage:

* The `key` trait declares a Concept's lookup token
* Reference Traits MAY accept lookup tokens to reference Concepts by key

Rules:

* MUST start with `~` sigil
* Token MUST use camelCase (lowerCamelCase)
* Therefore, Token MUST start with a lowercase letter
* Token MAY contain letters (a-z, A-Z) and digits (0-9)
* Token MUST NOT contain whitespace, punctuation, hyphens, or underscores

Examples:

* `~hobbit`
* `~theHobbit`
* `~spaghettiBolognese`
* `~recipe42`

Invalid:

* `~Hobbit` — starts with uppercase
* `~the-hobbit` — kebab-case forbidden
* `~the_hobbit` — snake_case forbidden
* `hobbit` — missing `~` sigil

#### 4.15.1 Resolution

Lookup tokens are resolved by finding a Concept whose `key` Trait matches.

Resolution rules:

1. Find all Concepts where `key=~token`
2. If exactly one match: resolved
3. If zero matches: resolution error (unresolved lookup token)
4. If multiple matches: resolution error (ambiguous lookup token)

Resolution is performed by consuming systems, not by Codex itself.

---

### 4.16 Character Values

A **Character Value** represents a single Unicode scalar value.

Syntax: See **Surface Form Specification § 15** for literal syntax and escape sequences.

Rules:

* MUST contain exactly one character (or escape sequence)
* Distinct from string values

Examples:

* `'A'`
* `'z'`
* `'\n'`
* `'\u0041'` — equivalent to `'A'`
* `'\u{1F600}'` — emoji

Invalid:

* `'AB'` — more than one character
* `''` — empty
* `"A"` — this is a string, not a character

---

## 5. Schema Authority (Normative)

Schemas MUST define:

* which Traits are allowed
* which Value types are valid
* cardinality rules
* semantic meaning

Codex syntax alone carries **no semantics**.

---

## 6. Non-Goals

This specification does **not**:

* define schema syntax
* define inference rules
* define validation logic
* define semantics beyond parsing
* define inline text markup

---

## 7. Summary

* Codex distinguishes Concepts, Traits, Values, and Content
* Values are rich, first-class, and declarative
* Content is opaque and non-semantic
* Naming is explicit and English-readable
* Semantics come exclusively from schemas

---

**End of Codex Naming and Value Specification v0.1**
