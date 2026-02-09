# Trait Values in Codex

This guide summarizes the value literal forms defined by the Codex specification. It is informative and intended to mirror the specification in plain English.

During schema validation, every trait value is parsed into its specific value kind from the value literal catalog. The schema then checks that parsed value against the allowed value types.

## Text Values

Text values are written with double quotes.

```cdx
name="Jane Doe"
summary="Single-line text"
```

Text values may be empty.

Text values are normalized after escapes are interpreted:

- Runs of whitespace (spaces, tabs, and line breaks) become single spaces.
- Leading and trailing spaces are removed.
- The resulting text is single-line.

Text escape sequences are defined by the grammar. The allowed escapes are:

- `\"` for a literal quote
- `\uXXXX` for a Unicode code point (4 hex digits)
- `\u{XXXXXX}` for a Unicode code point (1–6 hex digits)

Any backslash that does not introduce one of the escapes above is a literal backslash.

## Backtick Text

Backtick text is an alternate spelling for text values. It lets you write a long text value across multiple source lines while still producing a single-line text value after normalization.

Example (intended use):

```cdx
summary=`This is a long summary
that spans multiple lines
in the source file.`
```

Backtick text rules:

- The only escape is ``\` `` for a literal backtick.
- A backslash not followed by a backtick is a literal backslash.
- After escapes, the same whitespace normalization as quoted text is applied.
- The resulting text is single-line.

Canonical formatting uses quoted text when the normalized value fits on one line and does not contain a Unicode escape sequence. If it would exceed the 100-character line-length limit (tabs count as 2), or if it contains `\uXXXX` or `\u{...}`, the canonical form uses a backtick block with deterministic word-wrapping.

## Boolean Values

Boolean values are `true` and `false`.

```cdx
isPublished=true
isDraft=false
```

## Numeric Values

Numeric values are distinct value kinds determined by their surface spelling. Codex does not compute or normalize them; literal spelling is preserved exactly. During schema validation, tools classify numeric values by their spelling and validate them against the expected numeric value type.

Common rules:

- A leading `+` is not permitted.
- Leading zeros are not permitted in integer components, except for `0` itself.
- `-0` is not a valid integer literal.
- `NaN` is not permitted.
- `Infinity` and `-Infinity` are permitted. `+Infinity` is not permitted.

### Integer

Base-10 integer values.

```cdx
count=42
offset=-5
zero=0
```

Integer classifiers used in schema validation:

- `Zero`
- `PositiveInteger`
- `NegativeInteger`
- `NonNegativeInteger`
- `NonPositiveInteger`

### DecimalNumber

Decimals with a dot.

```cdx
price=19.99
delta=-0.25
```

### ExponentialNumber

Scientific notation using `e` or `E`.

```cdx
distance=1.5e11
tiny=2.5e-10
```

### Fraction

Integer numerator and integer denominator.

```cdx
ratio=3/4
half=1/2
```

### PrecisionNumber

A decimal number followed by `p`, with optional explicit precision.

```cdx
measurement=3.1415p
explicit=3.1415p6
```

Precision rules:

- If no explicit precision is provided, it is inferred from the number of digits after the decimal point, including trailing zeros.
- If an explicit precision is provided after `p`, it overrides the inferred precision.

### ImaginaryNumber

An integer or decimal followed by `i`.

```cdx
imaginary=2i
alsoImaginary=3.5i
```

### ComplexNumber

Real plus or minus imaginary, ending with `i`.

```cdx
complex=2+3i
another=1.5-2.5i
```

### Infinity

Literal spellings `Infinity` and `-Infinity`.

```cdx
maximum=Infinity
minimum=-Infinity
```

When compiled to XSD numeric forms, `Infinity` maps to `INF` and `-Infinity` maps to `-INF`.

The meaning of a numeric value beyond its literal spelling is defined by the governing schema or consuming system.

## Enumerated Token Values

Enumerated token values are schema-defined tokens written with `$` and PascalCase.

```cdx
status=$Draft
priority=$High
```

Enumerated tokens are not text values and are not evaluated.

## Temporal Values

Temporal values are written in braces and are parsed purely by syntax.

```cdx
publishedAt={2024-12-31}
updatedAt={2024-12-31T12:34:56Z}
duration={P3D}
```

Temporal rules:

- Temporal values must match the temporal grammar.
- Temporal keywords such as `{now}` and `{today}` remain symbolic unless a schema explicitly defines evaluation.
- Temporal values are not enumerated token values.
- Temporal kind is determined syntactically by the first matching grammar alternative.

## Color Values

Color values are not text values. They use dedicated color literal forms.

Supported color forms include:

- Hexadecimal colors: `#RGB`, `#RGBA`, `#RRGGBB`, `#RRGGBBAA`
- `rgb(...)` and legacy `rgba(...)`
- `hsl(...)` and legacy `hsla(...)`
- `hwb(...)`
- `lab(...)`
- `lch(...)`
- `oklab(...)`
- `oklch(...)`
- `color(...)`
- `color-mix(...)`
- Relative colors using `from <color>` within a color function
- `device-cmyk(...)`
- Named colors using `&name`

Canonicalization rules:

- Hex digits are lowercase in canonical form.
- Function names and color space tokens are lowercase in canonical form.

Named colors:

- Use a leading `&` and lowercase ASCII letters only.
- The name must match the named color list in Appendix B.

Color space tokens used by `color(...)` are restricted to:

- `srgb`
- `srgb-linear`
- `display-p3`
- `a98-rgb`
- `prophoto-rgb`
- `rec2020`
- `xyz`
- `xyz-d50`
- `xyz-d65`

Schema validation of colors is deterministic and uses the specific color value type requested by the schema. Values that cannot be converted to the expected color domain are schema errors.

## UUID Values

UUID values are unquoted 36-character tokens of the form:

```
xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

Rules:

- Hex digits are case-insensitive for parsing.
- Canonical form uses lowercase hex.
- Hyphens appear in the fixed UUID positions (8-4-4-4-12).
- No braces or prefixes are permitted.
- UUID values are not text values.

## IRI Reference Values

IRI reference values are unquoted tokens that include a `:` separating the scheme from the remainder.

Rules:

- Must contain `:` and must not end with `:`.
- Must not contain Unicode whitespace, control, bidirectional control, or private-use characters.
- Permit non-ASCII Unicode and percent-encoding.
- Are compared as opaque Unicode scalar sequences.
- Must not be dereferenced by Codex tools.
- Are not text values.

## Lookup Token Values

Lookup token values are document-scoped symbolic references written with `~` and camelCase.

```cdx
author=~janeDoe
```

Rules:

- They resolve by matching a `key` trait in the same document.
- They must not be dereferenced externally.
- They are not text values.

## Character Values

Character values represent exactly one Unicode scalar value and are written with single quotes.

```cdx
grade='A'
newline='\n'
emoji='\u{1F600}'
```

Character escape sequences follow the same escape set as text values (with `'` instead of `"`).

## List Values

List values are ordered sequences written with square brackets.

```cdx
numbers=[1, 2, 3]
mixed=["a", 2, true]
```

Rules:

- Lists may be empty.
- List order is significant.
- Lists may contain mixed value kinds.
- Lists allow nesting.

## Set Values

Set values are unordered collections written with `set[...]`.

```cdx
colors=set[$Red, $Green, $Blue]
```

Rules:

- Sets may be empty.
- Sets may contain mixed value kinds.
- Sets allow nesting.
- Sets must not contain duplicates.
- Duplicate detection uses the value equality rules in the specification.
- In canonical surface form, elements are serialized in the order they appear in the source spelling.

## Map Values

Map values are unordered key-value collections written with `map[...]`.

```cdx
scores=map[alice: 10, bob: 12]
```

Rules:

- Maps may be empty.
- Maps allow nesting.
- Keys must be unique (value equality rules apply).
- Map keys may be unquoted identifier keys, text values, character values, integer values, enumerated tokens, or IRI reference values.
- In canonical surface form, entries are serialized in the order they appear in the source spelling.

## Tuple Values

Tuple values are ordered sequences written with parentheses.

```cdx
point=(10, 20)
```

Rules:

- Tuples must contain at least one element.
- Tuples may contain mixed value kinds.
- Tuples allow nesting.
- Arity and position meaning must be defined by the schema.

## Range Values

Range values are declarative intervals written with `..`, with an optional step.

```cdx
span=1..10
stepSpan=1..10s2
```

Rules:

- Start and end endpoints are required.
- Endpoints are inclusive.
- Step is optional and at most one value.
- Endpoints must be ordered numeric types, temporal values, or character values.
- Start and end endpoints must be the same base value kind.
- Step values must be ordered numeric types or temporal values.
- Complex numbers, imaginary numbers, and infinity are not permitted as endpoints or step values.
- Range values must not be enumerated by tools.

## Record Values

Record values are fixed-structure field collections written with `record[...]`.

```cdx
person=record[name: "Ada", age: 36]
```

Rules:

- Records may be empty.
- Field names are unquoted identifiers using camelCase.
- Fields must be unique (value equality rules apply).
- Records allow nesting.
- In canonical surface form, entries are serialized in the order they appear in the source spelling.

## Collection Value Equality

Set, map, and record uniqueness checks use the specification value equality rules. Equality is defined over parsed values and is not based on raw source bytes.

Highlights:

- Text values compare by Unicode scalar sequence.
- Numeric, temporal, enumerated token, and lookup token values compare by exact literal spelling.
- Color values compare by spelling, with case-insensitive comparison of hex digits, function names, and color space tokens.
- UUID values compare case-insensitively for hex digits.
- Host name, email address, and URL values compare by their canonicalized forms.
- Lists and tuples compare by length and ordered element equality.
- Sets, maps, and records compare by contents regardless of entry order.

## Parameterized Value Types

Schemas may constrain collection contents using parameterized value types:

- `$List<T>`
- `$Set<T>`
- `$Map<K, V>`
- `$Tuple<T1, T2, ...>`
- `$Range<T>`
- `$Record<V>`

Type arguments may be simple value type tokens, parameterized types, or type unions. Type arguments do not include whitespace.

Unparameterized collection types such as `$List` or `$Map` allow any value types for their contents.

## Host Name Values

Host name values are written as `host("...")` and represent ASCII DNS hostnames.

Rules:

- The text must be ASCII only.
- The text must not contain Unicode whitespace, control, bidirectional control, or private-use characters.
- The canonical form lowercases the hostname.
- Hostnames must be valid DNS hostnames.
- Host name values are not text values.

## Email Address Values

Email address values are written as `email("...")` with a Unicode local part and an ASCII domain.

Rules:

- The value must contain exactly one `@`.
- The value must not contain Unicode whitespace, control, bidirectional control, or private-use characters.
- The local part is normalized with Unicode NFC.
- The domain is canonicalized as a host name.
- Email address values are not text values.

## URL Values

URL values are written as `url("...")` or `url("<base>", "<relative>")` and represent ASCII-only absolute URLs.

Rules:

- The parsed URL must include a scheme and be absolute.
- The URL text must not contain Unicode whitespace, control, bidirectional control, or private-use characters.
- The URL text must be ASCII only.
- The two-argument form resolves the second argument against the base.
- The base in the two-argument form must include an authority.
- Canonical form lowercases the scheme and authority, normalizes the path, and serializes as `url("<canonical>")`.
- URL values are not text values.

## See Also

- [Terminology: Data Documents and Schemas](/notes/terminology-data-documents/)
