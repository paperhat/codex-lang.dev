# Trait Values in Codex

This guide explains all the different kinds of values you can use with Traits in Codex.

A Trait is a name-value pair attached to a Concept. The name tells you what the Trait represents. The value is the actual data. This guide focuses on values — what they look like and how to write them.

---

## Text

Text values are written in double quotes.

```cdx
title="Spaghetti Bolognese"
author="Jane Doe"
description="A classic Italian pasta dish."
```

Text values must stay on one line. If you need special characters, use escapes:

```cdx
message="She said \"hello\" to me."
path="C:\\Users\\Jane"
multiline="Line one\nLine two"
```

Available escapes:
- `\"` for a literal quote
- `\\` for a literal backslash
- `\n` for a newline
- `\r` for a carriage return
- `\t` for a tab
- `\uXXXX` for a Unicode character (4 hex digits)
- `\u{XXXXXX}` for a Unicode character (1-6 hex digits)

---

## Backtick Text

Backtick text lets you write text across multiple lines in your source file. The whitespace gets collapsed into single spaces, producing a one-line result.

```cdx
summary=`This is a long description
	that spans multiple lines in the source
	but becomes a single line when parsed.`
```

This becomes equivalent to:

```cdx
summary="This is a long description that spans multiple lines in the source but becomes a single line when parsed."
```

Use backticks sparingly. If you need a lot of text, consider using Content instead of a Trait.

---

## Characters

A character is a single Unicode character. Wrap it in single quotes.

```cdx
grade='A'
separator='-'
newline='\n'
emoji='\u{1F600}'
```
Characters are not text values. `'A'` is a character. `"A"` is a text value containing one character.


---

## Booleans

Two possible values: `true` or `false`. No quotes.

```cdx
isPublished=true
isDraft=false
```

---

## Numbers

### Integers

Whole numbers, positive or negative.

```cdx
count=42
temperature=-5
zero=0
```

### Decimals

Numbers with a decimal point.

```cdx
price=19.99
ratio=0.5
pi=3.14159
```

### Scientific Notation

For very large or very small numbers.

```cdx
distance=1.5e11
tiny=2.5e-10
```

### Infinity

```cdx
maximum=Infinity
minimum=-Infinity
```

### Fractions

Written with a slash.

```cdx
proportion=3/4
half=1/2
```

### Imaginary Numbers

For complex math. Use the `i` suffix.

```cdx
imaginary=2i
alsoImaginary=3.5i
```

### Complex Numbers

Combine real and imaginary parts.

```cdx
complex=2+3i
another=1.5-2.5i
```

### Precision-Significant Numbers

When the precision of a number matters (like in scientific measurements), use the `p` suffix. The number of decimal places you write determines the precision, or you can specify it explicitly.

```cdx
measurement=3.1415p
moreZeros=3.141500p
explicit=3.1415p6
simple=2.0p
twoDecimals=2.00p
```

- `3.1415p` has precision 4 (four decimal places)
- `3.141500p` has precision 6 (trailing zeros count)
- `3.1415p6` has precision 6 (explicitly stated)
- `2.0p` has precision 1
- `2.00p` has precision 2

---

## Enumerated Tokens

These are fixed values from a predefined set. They start with `$` and use PascalCase.

```cdx
status=$Draft
difficulty=$Medium
color=$Red
priority=$High
dayOfWeek=$Monday
```

The available tokens are defined by the schema. You cannot make up your own — they must be declared.

---

## Lookup Tokens

These reference other Concepts by their `key` Trait. They start with `~` and use camelCase.

```cdx
author=~janeDoe
recipe=~spaghettiCarbonara
category=~mainDishes
parent=~recipe42
```

Somewhere else in the document, there must be a Concept with a matching `key`:

```cdx
<Author key=~janeDoe name="Jane Doe" />
```

---

## IRI References

IRIs (Internationalized Resource Identifiers) are used for identity and references. They contain a colon separating a scheme from the rest. No quotes.

```cdx
id=recipe:spaghetti
reference=book:the-hobbit
target=https://example.org/resource/123
```

---

## UUIDs

UUIDs are written in the standard 8-4-4-4-12 format. No quotes, no braces.

```cdx
id=550e8400-e29b-41d4-a716-446655440000
session=a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

Case does not matter, but lowercase is the canonical form.

---

## Lists

Ordered collections. Use square brackets with comma-separated values.

```cdx
tags=["italian", "pasta", "dinner"]
numbers=[1, 2, 3, 4, 5]
mixed=["hello", 42, true]
empty=[]
```

Lists can be nested:

```cdx
matrix=[[1, 2], [3, 4], [5, 6]]
```

Lists can contain any value type, and can mix types:

```cdx
dates=[{2024-01-01}, {2024-06-15}, {2024-12-31}]
tokens=[$Red, $Green, $Blue]
mixed=["hello", 42, true, {2024-01-01}, $Draft, ~someReference]
```

---

## Sets

Unordered collections with unique values. Use `set[]` syntax.

```cdx
categories=set[$Featured, $Sale, $New]
colors=set["red", "green", "blue"]
numbers=set[1, 2, 3]
emptySet=set[]
```

Duplicates are ignored — `set[1, 1, 2]` is the same as `set[1, 2]`.

Sets can contain any value type:

```cdx
references=set[~apple, ~banana, ~cherry]
nested=set[map[a: 1], map[b: 2]]
```

---

## Maps

Key-value collections. Use `map[]` syntax with colons.

```cdx
dimensions=map[width: 100, height: 200]
person=map[name: "John", age: 30]
emptyMap=map[]
```

Keys can be:
- Unquoted identifiers (start lowercase, letters and digits only)
- Text (for keys with spaces or special characters)
- Characters
- Integers
- Enumerated tokens

```cdx
simple=map[name: "John", age: 30]
textKeys=map["first name": "John", "last name": "Doe"]
tokenKeys=map[$Red: "#ff0000", $Green: "#00ff00"]
intKeys=map[1: "one", 2: "two", 3: "three"]
charKeys=map['A': "alpha", 'B': "bravo"]
```

Maps can be nested:

```cdx
config=map[
	database: map[host: "localhost", port: 5432],
	cache: map[enabled: true, ttl: 3600]
]
```

---

## Tuples

Fixed-length, ordered collections where position determines meaning. Use parentheses.

```cdx
point=(10, 20)
point3d=(10, 20, 30)
person=("John", "Doe", 30)
boundingBox=((0, 0), (100, 100))
```

Tuples differ from lists:
- Lists are for collections of similar things
- Tuples are for fixed structures where each position has specific meaning
- A 2D point is `(x, y)`, not `[x, y]`

Tuples must have at least one value.

---

## Ranges

Ranges define intervals between two values of the same type. Use `..` between the endpoints.

### Numeric Ranges

```cdx
oneToTen=1..10
negativeToPositive=-10..10
decimal=0.0..1.0
```

With a step value (use `s` for step):

```cdx
odds=1..100s2
byFives=0..100s5
decimalStep=0.0..1.0s0.1
```

### Character Ranges

```cdx
uppercase='A'..'Z'
lowercase='a'..'z'
digits='0'..'9'
everyOther='A'..'Z's2
```

### Temporal Ranges

```cdx
year2024={2024-01-01}..{2024-12-31}
dailyStep={2024-01-01}..{2024-12-31}s{P1D}
monthlyStep={2024-01}..{2024-12}s{P1M}
workHours={09:00}..{17:00}s{PT1H}
```

---

## Temporal Values

Dates, times, and durations are wrapped in curly braces.

### Year-Month

```cdx
month={2024-06}
fiscalStart={2024-01}
```

### Month-Day

```cdx
birthday={03-15}
holiday={12-25}
```

### Date

```cdx
published={2024-06-15}
deadline={2025-01-01}
```

### Time

```cdx
startTime={09:30}
precise={14:30:45}
withMillis={14:30:45.500}
```

### Local Date-Time

No timezone information.

```cdx
meeting={2024-06-15T09:30}
withSeconds={2024-06-15T14:30:45}
withMillis={2024-06-15T14:30:45.500}
```

### Zoned Date-Time

With timezone information.

```cdx
utc={2024-06-15T09:30:00Z}
offset={2024-06-15T09:30:00+05:30}
withTimezone={2024-06-15T09:30:00-05:00[America/New_York]}
tokyo={2024-06-15T09:30:00+09:00[Asia/Tokyo]}
```

### Duration

ISO 8601 duration format.

```cdx
oneDay={P1D}
oneWeek={P7D}
oneMonth={P1M}
oneYear={P1Y}
twoHours={PT2H}
thirtyMinutes={PT30M}
complex={P1Y2M3DT4H5M6S}
```

### Reserved Literals

```cdx
timestamp={now}
date={today}
```

---

## Colors

Colors are first-class values, not text values.

### Hexadecimal

```cdx
red=#f00
redWithAlpha=#f00a
fullRed=#ff0000
fullRedWithAlpha=#ff0000aa
```

### RGB

Legacy (comma-separated):

```cdx
orange=rgb(255, 128, 0)
orangeAlpha=rgba(255, 128, 0, 0.5)
```

Modern (space-separated):

```cdx
orange=rgb(255 128 0)
orangeAlpha=rgb(255 128 0 / 50%)
```

### HSL

Legacy:

```cdx
orange=hsl(30, 100%, 50%)
orangeAlpha=hsla(30, 100%, 50%, 0.5)
```

Modern:

```cdx
orange=hsl(30 100% 50%)
orangeAlpha=hsl(30 100% 50% / 50%)
```

### Lab and LCH

```cdx
labColor=lab(70% 20 -30)
labAlpha=lab(70% 20 -30 / 50%)
lchColor=lch(70% 45 30)
lchAlpha=lch(70% 45 30 / 50%)
```

### OKLab and OKLCH

```cdx
oklabColor=oklab(0.7 -0.1 0.1)
oklabAlpha=oklab(0.7 -0.1 0.1 / 50%)
oklchColor=oklch(0.7 0.15 180)
oklchAlpha=oklch(0.7 0.15 180 / 50%)
```

### Wide Gamut (color function)

```cdx
p3Color=color(display-p3 1 0.5 0)
p3Alpha=color(display-p3 1 0.5 0 / 50%)
srgb=color(srgb 1 0.5 0)
rec2020=color(rec2020 0.7 0.2 0.1)
xyz=color(xyz-d65 0.5 0.4 0.3)
```

Supported color spaces: `srgb`, `srgb-linear`, `display-p3`, `a98-rgb`, `prophoto-rgb`, `rec2020`, `xyz`, `xyz-d50`, `xyz-d65`.

### Named Colors

Named colors must be text values:

```cdx
color="red"
special="rebeccapurple"
clear="transparent"
```

---

## Quick Reference

| Type | Example |
|------|---------|
| Text | `"hello world"` |
| Backtick Text | `` `multi line text` `` |
| Character | `'A'` |
| Boolean | `true`, `false` |
| Integer | `42`, `-5` |
| Decimal | `3.14` |
| Scientific | `1.5e10` |
| Infinity | `Infinity`, `-Infinity` |
| Fraction | `3/4` |
| Imaginary | `2i` |
| Complex | `2+3i` |
| Precision | `3.14p`, `3.14p4` |
| Enum Token | `$Draft` |
| Lookup Token | `~recipe` |
| IRI | `recipe:pasta` |
| UUID | `550e8400-e29b-41d4-a716-446655440000` |
| List | `[1, 2, 3]` |
| Set | `set[1, 2, 3]` |
| Map | `map[a: 1, b: 2]` |
| Tuple | `(10, 20)` |
| Range | `1..10`, `1..10s2` |
| Date | `{2024-06-15}` |
| Time | `{09:30}` |
| DateTime | `{2024-06-15T09:30}` |
| Zoned | `{2024-06-15T09:30Z}` |
| Duration | `{P1D}`, `{PT2H}` |
| Hex Color | `#ff0000` |
| RGB | `rgb(255 0 0)` |
| HSL | `hsl(0 100% 50%)` |
