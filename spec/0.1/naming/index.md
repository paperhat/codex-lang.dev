Status: NORMATIVE
Version: 0.1
Editor: Charles F. Munat

# Codex Naming and Value Specification — Version 0.1

## 1. Purpose

This specification defines the **surface vocabulary, naming rules, and literal value spellings** of Codex.

Its goals are to:

* make Codex readable as structured English
* ensure deterministic parsing and reasoning
* support ontology modeling and configuration equally well
* provide first-class data values beyond strings and booleans
* prevent semantic ambiguity and ontology bloat

This document governs **naming and literal values only**.

---

## 2. Core Surface Vocabulary (Normative)

### 2.1 Concept

A **Concept** is the primary structural unit in Codex.

A Concept:

* is named
* may declare Traits
* may contain Content
* may contain child Concepts
* is purely declarative

Concepts express **structure**, not behavior.

---

### 2.2 Trait

A **Trait** binds a name to a Value.

Traits:

* are declared inline on Concepts
* are schema-authorized
* have no identity of their own
* are immutable once declared

Traits are **not properties, attributes, or fields**.

---

### 2.3 Value

A **Value** is a literal datum.

Values are:

* declarative
* immutable
* not expressions
* not evaluated by Codex
* first-class (not strings unless explicitly written as strings)

Codex defines a rich literal value system.

---

### 2.4 Content

**Content** is opaque narrative material.

Content:

* is not a Value
* is not typed
* is not interpreted by Codex
* may contain prose, markup, or code
* is schema-positioned but semantically opaque

This distinction prevents conflating **data** with **text**.

---

### 2.5 Entity

A Concept is an **Entity if and only if it declares an `id` Trait**.

Entities:

* represent high-semantic-density concepts
* participate in graphs and ontologies
* may be referenced by other Concepts

Identity rules are governed by the Identifier Specification.

---

## 3. Naming Rules (Normative)

### 3.1 Casing

* **Concept names** MUST use **PascalCase**
* **Trait names** MUST use **camelCase**

Forbidden everywhere:

* kebab-case
* snake_case
* screaming case
* mixed or inconsistent casing

---

### 3.2 Abbreviations

Abbreviations are forbidden unless explicitly whitelisted.

Rules:

* no periods in names
* no shorthand (`ref`, `def`, `cfg`, etc.)
* names must be full English words

Whitelisted exception:

* `uri`

---

### 3.3 Initialisms and Acronyms

Initialisms and acronyms:

* are treated as normal words
* capitalize only the first letter

Examples (valid):

* `AstNode`
* `HttpRequest`
* `LatexDocument`

---

## 4. Literal Value Spellings (Normative)

Codex defines the following **first-class literal value forms**.

Codex does **not** evaluate or normalize Values.

---

### 4.1 String Values

```text
"some text"
```

* delimited by double quotes
* single-line only
* escaped according to Surface Form rules

---

### 4.2 Boolean Values

```text
true
false
```

---

### 4.3 Numeric Values

Numeric literals are declarative spellings.

Supported:

* integers
* decimals
* scientific notation
* infinities (`Infinity`, `-Infinity`)
* fractions (`3/4`)
* imaginary numbers (`2i`)
* precision-significant numbers (`3.1415p6`)

Codex does not perform arithmetic or normalization.

---

### 4.4 Enumerated Token Values

```text
$Identifier
```

* schema-defined closed sets
* not strings
* not evaluated

---

### 4.5 List Values

```text
[ value, value, ... ]
```

* ordered
* nested allowed
* mixed types allowed
* no expansion

---

### 4.6 Range Values

```text
start..end
start..end s step
```

Ranges are declarative intervals.

Codex does not enumerate ranges.

---

### 4.7 Temporal Values

Temporal values are literal spellings enclosed in `{}`.

Supported forms:

* `{YYYY-MM}` — PlainYearMonth
* `{MM-DD}` — PlainMonthDay
* `{YYYY-MM-DD}` — PlainDate
* `{YYYY-MM-DDThh:mm:ss(.sss)?}` — PlainDateTime (local)
* `{P...}` — Duration
* `{now}`, `{today}` — Reserved literals

Codex does not assign time zones or perform conversions.

---

### 4.8 Color Values

Colors are first-class literals.

Supported:

* hex (`#RGB`, `#RRGGBBAA`)
* functional forms (`rgb(...)`, `oklch(...)`)
* named colors as strings

Codex does not validate or normalize colors.

---

### 4.9 UUID Values

UUIDs are literal tokens.

* not strings
* case-insensitive
* no braces

---

### 4.10 IRI Reference Values

Unquoted tokens representing identity or reference.

Used by:

* `id`
* `reference`
* `target`
* `for`
* `key`

Codex does not resolve or dereference IRIs.

---

## 5. Schema Authority (Normative)

Schemas MUST define:

* which Traits are allowed
* which Value types are valid
* cardinality
* semantic meaning

Codex syntax alone conveys no semantics.

---

## 6. Non-Goals

This specification does **not**:

* define schema syntax
* define inference rules
* define storage formats
* define resolution or normalization
* define dialects or modules
* define inline text markup

---

## 7. Summary

* Codex distinguishes Concepts, Traits, Values, and Content
* Values are first-class and richly typed
* Content is opaque and non-semantic
* Naming is explicit and English-readable
* Semantics come exclusively from schema

---

**End of Codex Naming and Value Specification v0.1**
