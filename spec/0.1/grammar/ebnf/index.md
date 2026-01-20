Status: NORMATIVE
Lock State: UNLOCKED
Version: 0.1
Editor: Charles F. Munat

# Codex Formal Grammar — EBNF (Normative)

This document defines the **formal grammar** of the Codex surface form using Extended Backus-Naur Form (EBNF).

This grammar is **normative**. A conforming parser MUST accept all documents that match this grammar and MUST reject all documents that do not.

---

## 1. Notation

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

## 2. Document Structure

```ebnf
(* A Codex document contains exactly one root Concept *)

Document = { BlankLine }, { Annotation }, RootConcept, { BlankLine } ;

RootConcept = Concept ;

Concept = BlockConcept | SelfClosingConcept ;
```

---

## 3. Block Concepts

```ebnf
(* Block concepts contain either children or content.
   The parser consults the schema to determine which.
   This is schema-directed dispatch, not syntactic ambiguity.
   See Formal Grammar Specification § 6 for details. *)

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

ContentText = { AnyCharExceptNewline } ;

(* Note: No escape sequences are required in content mode.
   The parser knows it is in content mode from the schema
   and scans for the closing marker by Concept name match
   at the correct indentation level. *)
```

---

## 4. Self-Closing Concepts

```ebnf
SelfClosingConcept = "<", ConceptName, [ Traits ], [ Whitespace ], "/>" ;
```

---

## 5. Concept Names

```ebnf
(* Concept names are PascalCase *)

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

## 6. Traits

```ebnf
(* Traits are name=value pairs, separated by whitespace *)

Traits = Whitespace, Trait, { Whitespace, Trait } ;

Trait = TraitName, "=", Value ;

TraitName = LowercaseLetter, { Letter | Digit } ;
```

---

## 7. Values

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

## 8. String Values

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

## 9. Character Values

```ebnf
CharValue = "'", CharContent, "'" ;

CharContent = UnescapedChar | CharEscapeSequence ;

UnescapedChar = AnyCharExceptApostropheBackslashNewline ;

CharEscapeSequence = "\\", ( "'" | "\\" | "n" | "r" | "t" | UnicodeEscape ) ;
```

---

## 10. Backtick Strings

```ebnf
(* Backtick strings collapse whitespace to single spaces *)

BacktickString = "`", { BacktickChar }, "`" ;

BacktickChar = UnescapedBacktickChar | BacktickEscape ;

UnescapedBacktickChar = AnyCharExceptBacktickBackslash ;

BacktickEscape = "\\", ( "`" | "\\" ) ;
```

---

## 11. Boolean Values

```ebnf
BooleanValue = "true" | "false" ;
```

---

## 12. Numeric Values

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

## 13. Enumerated Tokens

```ebnf
EnumeratedToken = "$", UppercaseLetter, { Letter | Digit } ;
```

---

## 14. IRI References

```ebnf
(* Codex IRI references allow RFC 3987 IRI-reference characters directly.
      Unicode characters MAY appear directly; percent-encoding remains valid.
      Codex further forbids Unicode whitespace, control, bidi-control, and private-use characters. *)

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

## 15. Lookup Tokens

```ebnf
LookupToken = "~", LowercaseLetter, { Letter | Digit } ;
```

---

## 16. UUID Values

```ebnf
UuidValue = HexOctet, HexOctet, HexOctet, HexOctet, "-",
            HexOctet, HexOctet, "-",
            HexOctet, HexOctet, "-",
            HexOctet, HexOctet, "-",
            HexOctet, HexOctet, HexOctet, HexOctet, HexOctet, HexOctet ;

HexOctet = HexDigit, HexDigit ;
```

---

## 17. Color Values

```ebnf
ColorValue = HexColor | RgbColor | HslColor | LabColor | LchColor
           | OklabColor | OklchColor | ColorFunction ;

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
```

---

## 18. Temporal Values

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

## 19. List Values

```ebnf
ListValue = "[", [ ListItems ], "]" ;

ListItems = Value, { ",", [ Whitespace ], Value } ;
```

---

## 20. Set Values

```ebnf
SetValue = "set[", [ SetItems ], "]" ;

SetItems = Value, { ",", [ Whitespace ], Value } ;
```

---

## 21. Map Values

```ebnf
MapValue = "map[", [ MapItems ], "]" ;

MapItems = MapEntry, { ",", [ Whitespace ], MapEntry } ;

MapEntry = MapKey, ":", [ Whitespace ], Value ;

MapKey = MapIdentifier | StringValue | CharValue | Integer | EnumeratedToken ;

MapIdentifier = LowercaseLetter, { Letter | Digit } ;
```

---

## 22. Tuple Values

```ebnf
TupleValue = "(", TupleItems, ")" ;

TupleItems = Value, { ",", [ Whitespace ], Value } ;
```

---

## 23. Range Values

```ebnf
RangeValue = RangeStart, "..", RangeEnd, [ "s", StepValue ] ;

RangeStart = NumericValue | TemporalValue | CharValue ;

RangeEnd = NumericValue | TemporalValue | CharValue ;

StepValue = NumericValue | TemporalValue ;
```

---

## 24. Annotations

```ebnf
Annotation = "[", { AnnotationChar }, "]" ;

AnnotationChar = UnescapedAnnotationChar | AnnotationEscape ;

UnescapedAnnotationChar = AnyCharExceptBracketBackslash ;

AnnotationEscape = "\\", ( "]" | "\\" ) ;
```

---

## 25. Whitespace and Structural Elements

```ebnf
Whitespace = WhitespaceChar, { WhitespaceChar } ;

WhitespaceChar = " " | "\t" | Newline ;

Newline = "\n" ;

BlankLine = Newline, { " " | "\t" }, Newline ;

Indentation = { "\t" } ;

Tab = "\t" ;
```

---

## 26. Character Classes (Informative)

The following character classes are used but not fully enumerated:

* `AnyCharExceptNewline` — any Unicode scalar except U+000A
* `AnyCharExceptQuoteBackslashNewline` — any Unicode scalar except `"`, `\`, U+000A
* `AnyCharExceptApostropheBackslashNewline` — any Unicode scalar except `'`, `\`, U+000A
* `AnyCharExceptBacktickBackslash` — any Unicode scalar except `` ` ``, `\`
* `AnyCharExceptBracketBackslash` — any Unicode scalar except `]`, `\`

---

## 27. Precedence and Disambiguation

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

**End of Codex Formal Grammar — EBNF v0.1**
