Status: INFORMATIVE
Lock State: LOCKED
Version: 0.1
Editor: Charles F. Munat

# Codex Formal Grammar — PEG (Informative)

This document defines the **formal grammar** of the Codex surface form using Parsing Expression Grammar (PEG) notation.

This grammar is **informative**. It provides an unambiguous, implementation-ready grammar that may be used for parser construction. The normative EBNF grammar takes precedence in case of discrepancy.

---

## 1. Notation

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

## 2. Document Structure

```peg
# A Codex document contains exactly one root Concept

Document <- BlankLine* Annotation* RootConcept BlankLine* EOF

RootConcept <- Concept

Concept <- BlockConcept / SelfClosingConcept
```

---

## 3. Block Concepts

```peg
# Block concepts contain either children or content (schema-determined)
# Parser treats body as opaque; schema validates content mode

BlockConcept <- OpeningMarker Body ClosingMarker

OpeningMarker <- '<' ConceptName Traits? Whitespace? '>'

ClosingMarker <- '</' ConceptName '>'

Body <- (Newline Indentation BodyLine)*

BodyLine <- (Annotation Newline Indentation)* Concept
          / ContentText

ContentText <- (!ClosingMarkerLookahead ContentChar)*

ContentChar <- EscapedClosingMarker / (!Newline .)

EscapedClosingMarker <- '\\</'

ClosingMarkerLookahead <- Newline Indentation '</' ConceptName '>'
```

---

## 4. Self-Closing Concepts

```peg
SelfClosingConcept <- '<' ConceptName Traits? Whitespace? '/>'
```

---

## 5. Concept Names

```peg
# Concept names are PascalCase

ConceptName <- UppercaseLetter (Letter / Digit)*

UppercaseLetter <- [A-Z]
LowercaseLetter <- [a-z]
Letter <- [A-Za-z]
Digit <- [0-9]
```

---

## 6. Traits

```peg
# Traits are name=value pairs, separated by whitespace

Traits <- (Whitespace Trait)+

Trait <- TraitName '=' Value

TraitName <- LowercaseLetter (Letter / Digit)*
```

---

## 7. Values

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

## 8. String Values

```peg
StringValue <- '"' StringChar* '"'

StringChar <- EscapeSequence / (!["\\\n] .)

EscapeSequence <- '\\' ( ["\\nrt] / UnicodeEscape )

UnicodeEscape <- 'u' HexDigit HexDigit HexDigit HexDigit
               / 'u{' HexDigit+ '}'

HexDigit <- [0-9A-Fa-f]
```

---

## 9. Character Values

```peg
CharValue <- "'" CharContent "'"

CharContent <- CharEscapeSequence / (!['\\\n] .)

CharEscapeSequence <- '\\' ( ['\\/nrt] / UnicodeEscape )
```

---

## 10. Backtick Strings

```peg
# Backtick strings span multiple lines; whitespace collapses to single space

BacktickString <- '`' BacktickChar* '`'

BacktickChar <- BacktickEscape / (![`\\] .)

BacktickEscape <- '\\' [`\\]
```

---

## 11. Boolean Values

```peg
BooleanValue <- 'true' / 'false'
```

---

## 12. Numeric Values

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

## 13. Enumerated Tokens

```peg
EnumeratedToken <- '$' UppercaseLetter (Letter / Digit)*
```

---

## 14. IRI References

```peg
# Codex IRI references allow RFC 3987 IRI-reference characters directly.
# Unicode characters MAY appear directly; percent-encoding remains valid.
# Codex further forbids Unicode whitespace, control, bidi-control, and private-use characters.

IriReference <- IriScheme ':' IriBody

IriScheme <- Letter (Letter / Digit / [+.-])*

IriBody <- IriChar*

IriChar <- IriAsciiChar / UcsChar

IriAsciiChar <- [A-Za-z0-9_.~:/?#\[\]@!$&'()*+,;=%-]

# RFC 3987 character classes. PEG dialects vary in Unicode-range support;
# treat these as normative character-range definitions.
UcsChar <- [\u00A0-\uD7FF]
         / [\uF900-\uFDCF]
         / [\uFDF0-\uFFEF]
         / [\U00010000-\U0001FFFD]
         / [\U00020000-\U0002FFFD]
         / [\U00030000-\U0003FFFD]
         / [\U00040000-\U0004FFFD]
         / [\U00050000-\U0005FFFD]
         / [\U00060000-\U0006FFFD]
         / [\U00070000-\U0007FFFD]
         / [\U00080000-\U0008FFFD]
         / [\U00090000-\U0009FFFD]
         / [\U000A0000-\U000AFFFD]
         / [\U000B0000-\U000BFFFD]
         / [\U000C0000-\U000CFFFD]
         / [\U000D0000-\U000DFFFD]
         / [\U000E1000-\U000EFFFD]

```

---

## 15. Lookup Tokens

```peg
LookupToken <- '~' LowercaseLetter (Letter / Digit)*
```

---

## 16. UUID Values

```peg
# 8-4-4-4-12 format

UuidValue <- HexOctet HexOctet HexOctet HexOctet '-'
             HexOctet HexOctet '-'
             HexOctet HexOctet '-'
             HexOctet HexOctet '-'
             HexOctet HexOctet HexOctet HexOctet HexOctet HexOctet

HexOctet <- HexDigit HexDigit
```

---

## 17. Color Values

```peg
# Color functions first (more specific), then hex

ColorFunction <- RgbColor / HslColor / LabColor / LchColor
               / OklabColor / OklchColor / ColorSpaceFunction

RgbColor <- 'rgba' '(' ColorArgs ')'
          / 'rgb' '(' ColorArgs ')'

HslColor <- 'hsla' '(' ColorArgs ')'
          / 'hsl' '(' ColorArgs ')'

LabColor <- 'lab' '(' ColorArgs ')'

LchColor <- 'lch' '(' ColorArgs ')'

OklabColor <- 'oklab' '(' ColorArgs ')'

OklchColor <- 'oklch' '(' ColorArgs ')'

ColorSpaceFunction <- 'color' '(' ColorSpace Separator ColorArgs ')'

ColorSpace <- 'srgb-linear' / 'srgb' / 'display-p3' / 'a98-rgb'
            / 'prophoto-rgb' / 'rec2020' / 'xyz-d50' / 'xyz-d65' / 'xyz'

ColorArgs <- ColorArg (Separator ColorArg)* (Separator? '/' Separator? AlphaArg)?

ColorArg <- Percentage / NumericValue

AlphaArg <- Percentage / NumericValue

Percentage <- NumericValue '%'

Separator <- Whitespace / ','

HexColor <- '#' HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit
          / '#' HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit
          / '#' HexDigit HexDigit HexDigit HexDigit
          / '#' HexDigit HexDigit HexDigit

# Note: 8-digit, 6-digit, 4-digit, 3-digit hex in decreasing specificity
```

---

## 18. Temporal Values

```peg
TemporalValue <- '{' TemporalBody '}'

TemporalBody <- ZonedDateTime / LocalDateTime / Date / YearMonth / MonthDay / Time / Duration / ReservedTemporal

LocalDateTime <- Date 'T' Time

ZonedDateTime <- LocalDateTime TimeZoneOffset TimeZoneId?

TimeZoneOffset <- 'Z' / [+-] Hour ':' Minute

TimeZoneId <- '[' TimeZoneIdChar+ ']'

TimeZoneIdChar <- [A-Za-z0-9/_-]

Date <- Year '-' Month '-' Day

YearMonth <- Year '-' Month

MonthDay <- Month '-' Day

Time <- Hour ':' Minute (':' Second ('.' Milliseconds)?)?

Duration <- 'P' DurationComponent* ('T' TimeDurationComponent+)?

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

## 19. List Values

```peg
ListValue <- '[' ListItems? ']'

ListItems <- Value (',' Whitespace? Value)*
```

---

## 20. Set Values

```peg
SetValue <- 'set[' SetItems? ']'

SetItems <- Value (',' Whitespace? Value)*
```

---

## 21. Map Values

```peg
MapValue <- 'map[' MapItems? ']'

MapItems <- MapEntry (',' Whitespace? MapEntry)*

MapEntry <- MapKey ':' Whitespace? Value

MapKey <- MapIdentifier / StringValue / CharValue / Integer / EnumeratedToken

MapIdentifier <- [a-z] [A-Za-z0-9]*
```

---

## 22. Tuple Values

```peg
TupleValue <- '(' TupleItems ')'

TupleItems <- Value (',' Whitespace? Value)*
```

---

## 23. Range Values

```peg
# Range endpoints must be same type (enforced by schema, not parser)

RangeValue <- RangeEndpoint '..' RangeEndpoint ('s' StepValue)?

RangeEndpoint <- TemporalValue / CharValue / NumericValue

StepValue <- TemporalValue / NumericValue

NumericValue <- ComplexNumber / ImaginaryNumber / Fraction / Infinity
              / PrecisionNumber / ScientificNumber / DecimalNumber / Integer
```

---

## 24. Annotations

```peg
Annotation <- '[' AnnotationChar* ']'

AnnotationChar <- AnnotationEscape / (![\\]] .)

AnnotationEscape <- '\\' [\]\\]
```

---

## 25. Whitespace and Structural Elements

```peg
Whitespace <- WhitespaceChar+

WhitespaceChar <- ' ' / '\t' / Newline

Newline <- '\n'

BlankLine <- Newline Whitespace* Newline

Indentation <- '\t'*

EOF <- !.
```

---

## 26. Implementation Notes

### 26.1 Value Termination

Values terminate at:

* Unescaped whitespace (space, tab, newline)
* `>` or `/>` (end of Concept marker)

Balanced delimiters (`[]`, `{}`, `()`, `''`, `""`, ``` `` ```) are respected during parsing.

### 26.2 Content Mode Detection

The parser cannot distinguish Children Mode from Content Mode syntactically. The schema determines which mode applies. Implementations should:

1. Parse body as raw text
2. Consult schema for content mode
3. Re-parse as children if schema indicates Children Mode

### 26.3 Indentation Handling

Indentation is significant. Before parsing:

1. Normalize CRLF to LF
2. Reject bare CR
3. Count leading tabs per line
4. Validate indentation depth matches nesting

### 26.4 Canonical Form

A conforming formatter produces canonical form:

* UTF-8 encoding (no BOM)
* LF line endings
* Tab indentation (one per level)
* One blank line between siblings
* No trailing whitespace
* No trailing blank lines
* 1-2 Traits: single line
* 3+ Traits: one per line, indented

---

## 27. Example Parse

Input:

```cdx
<Recipe id=recipe:pasta title="Spaghetti">
	<Ingredients>
		<Ingredient name="pasta" amount=500 unit=$Grams />
		<Ingredient name="sauce" amount=400 unit=$Milliliters />
	</Ingredients>

	<Instructions>
		Boil the pasta. Add the sauce.
	</Instructions>
</Recipe>
```

Parse tree (simplified):

```
Document
└── Concept (Block)
    ├── ConceptName: "Recipe"
    ├── Traits
    │   ├── Trait: id = IriReference("recipe:pasta")
    │   └── Trait: title = StringValue("Spaghetti")
    └── Body
        ├── Concept (Block): Ingredients
        │   ├── Concept (SelfClosing): Ingredient
        │   │   └── Traits: name, amount, unit
        │   └── Concept (SelfClosing): Ingredient
        │       └── Traits: name, amount, unit
        └── Concept (Block): Instructions
            └── Content: "Boil the pasta. Add the sauce."
```

---

**End of Codex Formal Grammar — PEG v0.1**
