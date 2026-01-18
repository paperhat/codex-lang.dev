Status: NORMATIVE  
Lock State: LOCKED    
Version: 0.1  
Editor: Charles F. Munat

# **Codex Naming and Value Specification — Version 0.1 (FINAL, CORE)**

This specification defines the **core surface vocabulary**, **naming rules**, and
**literal value spellings** of the Codex language.

It is **language-level and core**.
It contains **no Module, Dialect, Gloss, Paperhat, or tooling concerns**.

---

# Codex Naming and Value Specification — Version 0.1

## 1. Purpose

This specification defines **how things are named** and **how literal data is written**
in Codex.

Its goals are to:

* make Codex read as structured, precise English
* prevent ambiguity for humans and machines
* support ontology authoring, configuration, and data interchange
* provide **first-class data values**, not string encodings
* keep Codex declarative and closed-world

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

A Concept is **not** an element, component, tag, node, or class.

---

### 2.2 Trait

A **Trait** binds a name to a Value.

Traits:

* are declared inline on Concepts
* are schema-authorized
* have no independent identity
* are immutable once declared

Traits are **not properties, attributes, fields, or parameters**.

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

* is **not** a Value
* is **not** typed
* is **not** interpreted by Codex
* may contain prose, markup, code, or other text
* exists only inside Concepts

This distinction prevents conflating **data** with **text**.

---

### 2.5 Entity

A Concept is an **Entity if and only if it declares an `id` Trait**.

Entities:

* represent **high semantic density**
* participate in ontologies and graphs
* may be referenced by other Concepts

Entity eligibility is **explicit and schema-defined**.

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

---

### 3.2 Abbreviations

Abbreviations are forbidden unless explicitly whitelisted.

Rules:

* periods are never permitted
* shorthand names (`ref`, `def`, `cfg`, etc.) are forbidden
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

Examples (invalid):

* `ASTNode`
* `HTMLParser`
* `plainHTML`

---

## 4. Literal Value Spellings (Normative)

Codex defines the following **literal value forms**.

Codex **parses** these values but **does not evaluate, normalize, or interpret them**.
Typing and semantics are schema responsibilities.

---

### 4.1 String Values

```text
"some text"
```

* delimited by double quotes
* single-line only
* escaped per Surface Form rules

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

* integers (`7`, `-42`)
* decimals (`3.14`)
* scientific notation (`1.2e6`)
* infinities (`Infinity`, `-Infinity`)
* fractions (`3/4`)
* imaginary numbers (`2i`)
* precision-significant numbers (`3.1415p6`)

Codex performs **no arithmetic and no normalization**.

---

### 4.4 Enumerated Token Values

```text
$Identifier
```

* drawn from schema-defined closed sets
* not strings
* not evaluated

---

### 4.5 List Values

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

### 4.6 Range Values

```text
start..end
start..end s step
```

Ranges are **declarative intervals**.

* inclusive endpoints
* not enumerated
* semantics are schema-defined

---

### 4.7 Temporal Values

Temporal literals are written in `{}`.

Supported spellings:

* `{YYYY-MM}` — Year-Month
* `{MM-DD}` — Month-Day
* `{YYYY-MM-DD}` — Date
* `{YYYY-MM-DDThh:mm:ss(.sss)?}` — Local Date-Time
* `{P...}` — Duration
* `{now}`, `{today}` — Reserved literals

Codex does **not** assign time zones or perform conversion.

---

### 4.8 Color Values

Colors are **first-class values**, not strings.

Supported:

* hex (`#RGB`, `#RRGGBBAA`)
* functional forms (`rgb(...)`, `hsl(...)`, `oklch(...)`)
* named colors as string values

Codex does not validate or normalize colors.

---

### 4.9 UUID Values

UUID literals:

* are not strings
* contain no braces
* are case-insensitive
* have no mandated version

---

### 4.10 IRI Reference Values

IRI reference values are **unquoted tokens** representing identity or reference.

Used by the following Traits only:

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
* cardinality rules
* semantic meaning

Codex syntax alone carries **no semantics**.

---

## 6. Non-Goals

This specification does **not**:

* define schema syntax
* define inference rules
* define validation logic
* define modules or dialects
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
