# Codex Naming and Value Contract

**Status:** NORMATIVE
**Version:** 0.2
**Editor:** Charles F. Munat

This document defines the **core surface vocabulary**, **naming rules**, and **literal value spellings** used throughout the Codex language.

Naming and value rules are part of the Codex language specification and are governed by this document.

This document is **Normative**.

---

## 1. Purpose

This contract defines the **terminology, naming rules, and literal value forms**
used to describe Codex.

Its goals are to:

* minimize cognitive load by making Codex read like **plain English**
* avoid confusion with HTML, XML, programming languages, and UI frameworks
* ensure humans, tools, and LLMs reason consistently about Codex
* ensure Codex remains **markup, not code**

This contract governs **naming and literal values only**.
It does not restrict prose or other **Content**.

---

## 2. Core Terms (Normative)

### 2.1 Concept

A **Concept** is the primary surface construct in Codex.

A Concept is:

* a named declarative unit
* composed of **Traits** and child Concepts
* optionally identified with an `id`
* purely declarative (never imperative)

Examples:

* `<Recipe>`
* `<Step>`
* `<Policy>`
* `<Module>`

Notes:

* “Concept” refers to the Codex surface construct, not a philosophical abstraction.
* Not all Concepts are Entities.

---

### 2.2 Trait

A **Trait** is a named distinguishing characteristic of a Concept.

A Trait:

* binds a **name** to a **Value**
* is declared inline on a Concept
* is schema-defined
* has no independent identity

Examples:

* `name="Bob"`
* `amount=200`
* `optional=false`

---

### 2.3 Value

A **Value** is a literal datum.

Values are:

* declarative
* immutable
* schema-typed
* non-narrative
* **not expressions**
* **not evaluated by Codex**

Codex defines specific **Value spellings**.
Their interpretation is the responsibility of consuming systems and schemas.

---

### 2.4 Content

**Content** is opaque narrative data.

Content:

* is not interpreted by Codex
* may contain prose, code, poetry, or markup
* is always carried inside a Concept

Example:

```xml
<Description>
	A cool dude.
</Description>
```

---

### 2.5 Entity

An **Entity** is a Concept that has identity.

* A Concept **is an Entity if and only if it declares an `id` Trait**
* Entity identity is semantic and graph-addressable
* Identity requirements are defined by schema, not by syntax

Examples:

* `<Recipe id="recipe:spaghetti">` → Entity
* `<Step>` → not an Entity (unless schema explicitly authorizes it)

---

## 3. Naming and Casing Rules (Normative)

### 3.1 Case Conventions

* **Concept names** MUST use **PascalCase**
* **Trait names** MUST use **camelCase**

The following styles are forbidden everywhere in Codex naming:

* kebab-case
* snake_case
* SCREAMING_CASE
* mixed or inconsistent casing

---

### 3.2 Abbreviations (Naming Only)

Codex avoids abbreviations in names.

* Periods are **never permitted** in Concept or Trait names.
* General abbreviations MUST NOT be used unless explicitly whitelisted by schema.
* When in doubt, names MUST be spelled out in full.

This rule applies **only to naming**, not to Content or Values.

---

### 3.3 Initialisms and Acronyms

Initialisms and acronyms MAY be used when widely understood.

For naming purposes:

* Initialisms are sequences of letters pronounced individually.
* Acronyms are initialisms intended to be pronounced as words.

Both are treated identically for casing.

**Capitalization Rule (Normative):**

* Only the **first letter** is capitalized.
* Remaining letters follow normal word casing.

Examples (correct):

* `AstNode`
* `FbiAgent`
* `PlainHtml`
* `LatexDocument`

Examples (invalid):

* `ASTNode`
* `FBIAgent`
* `PlainHTML`
* `plainHTML`

---

### 3.4 No Shorthand Traits

Shorthand Trait names are forbidden.

Invalid examples:

* `ref`
* `lang`
* `href`

Required forms:

* `reference`
* `language`
* `uri` (or a more specific plain-English alternative)

---

## 4. Value Spellings (Normative)

Codex defines the following literal **Value spellings**.

These are **data notations**, not expressions.

---

### 4.1 String Values

* Delimited by double quotation marks: `"..."`

Strings are opaque text values.

---

### 4.2 Boolean Values

* `true`
* `false`

---

### 4.3 Numeric Values

Numeric Values are literal spellings of numbers.

Codex does not evaluate numbers.

#### 4.3.1 Standard numeric forms

* integers: `7`, `0`, `-42`
* decimals: `3.1415`
* scientific notation: `1.23e8`, `-2e-3`
* infinities: `Infinity`, `-Infinity`

---

#### 4.3.2 Fraction literals

Fractions are numeric literals, not operations.

Form:

```
[-]?[0-9]+/[0-9]+
```

Rules:

* A leading `-` MAY appear only at the very start

  * `-1/3` ✅
  * `1/-3` ❌
* No spaces are permitted
* No exponent form is permitted
* `0/3` is valid
* `3/0` is syntactically valid; semantic handling is consumer-defined
* Codex performs no normalization

---

#### 4.3.3 Imaginary literals

Imaginary numbers are numeric literals.

Form:

```
[-]?<number>i
```

Examples:

* `3i`
* `-7i`
* `1.2e3i`

Operations such as `√-1` are forbidden.

---

#### 4.3.4 Precision numbers

A numeric literal is **precision-significant if and only if it ends with `p`.**

There is no implicit precision.

Two forms are permitted:

**Inferred precision**

* `3.141500p` → precision = 6 decimal places
* `3p` → precision = 0 decimal places

**Explicit precision**

* `3p6` → precision = 6 decimal places
* `3.1415p6` → precision = 6 decimal places

Codex does not normalize precision numbers.

---

### 4.4 List Values

Lists are written using square brackets:

```text
[ value, value, ... ]
```

Rules:

* Lists are ordered
* Lists may be empty
* Lists may be mixed or homogeneous, as defined by schema
* Lists are not expanded by Codex

Examples:

```xml
friends=["sam", "ted", "mary"]
favoriteNumbers=[3, 7, 12]
```

---

### 4.5 Range Values

Ranges are declarative interval literals.

Form:

```
start..end
```

Rules:

* Ranges are **inclusive**
* Ranges are not evaluated or expanded by Codex
* Ordering is preserved as written

Ranges MAY appear inside lists or wherever schema permits.

Example:

```xml
<Toy forAges=[3..6] />
```

---

#### 4.5.1 Stepped ranges

Ranges MAY include an explicit step:

```
start..end s step
```

Example:

```
1.25..1.75s0.05
```

Rules:

* `s` introduces the step value
* Step is a numeric literal
* No spaces are permitted
* Direction is implied by start/end
* Codex does not require exact alignment or termination

---

### 4.6 Temporal Values

Temporal Values are written using **curly braces** `{...}`.

They are literal spellings of ISO 8601 forms.

#### 4.6.1 Date

```
{YYYY-MM-DD}
```

Example:

```
{2026-01-01}
```

---

#### 4.6.2 DateTime

```
{YYYY-MM-DDThh:mm:ss(.sss)?(Z|±HH:MM)}
```

A timezone designator is REQUIRED.

Example:

```
{2023-10-27T14:30:15+02:00}
```

---

#### 4.6.3 Duration

ISO 8601 duration form:

```
{P...}
```

Example:

```
{PT3M15S}
```

---

#### 4.6.4 Special temporal values

The following are reserved:

* `{now}`
* `{today}`

Their interpretation is context-dependent and consumer-defined.

---

## 5. Trait Authorization and Reference Traits (Normative)

### 5.1 Traits Are Schema-Authorized

Traits are never global.

A Trait is valid only when explicitly authorized by schema for the Concept on which it appears.

---

### 5.2 Identity Traits

The following Trait is authorized **only** for Entity Concepts:

* `id`

Declaring an `id` Trait makes a Concept an Entity.

---

### 5.3 Reference Traits

Codex defines three reference Trait names with distinct intent:

* `reference`
* `target`
* `for`

A Concept MUST NOT declare more than one of these unless explicitly permitted by schema.

---

## 6. Context and Scope (Normative)

Concept and Trait names are schema-scoped.

Codex avoids global prefixing in favor of contextual meaning.

---

## 7. Structural vs Semantic Concepts

This distinction is explanatory only.

* **Semantic Concepts** express domain meaning
* **Structural Concepts** organize or group meaning

Authors do not need to reason about this distinction.

---

## 8. Forbidden Vocabulary (Normative)

Forbidden as replacements for **Concept**:

* element
* component
* tag
* node
* class

Forbidden as replacements for **Trait**:

* prop
* property
* attribute
* field
* parameter

---

## 9. Summary

* Codex is written in **Concepts**
* Concepts declare **Traits**
* Traits bind names to **Values**
* Values are literal spellings, not expressions
* Concepts may carry **Content**
* A Concept is an **Entity if and only if it declares an `id` Trait**
* Naming and values are plain-English, declarative, and schema-scoped
* Lists, ranges, precision numbers, and temporal literals are first-class data forms

---

**End of Codex Naming and Value Contract**
