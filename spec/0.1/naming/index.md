Status: NORMATIVE  
Version: 0.1  
Editor: Charles F. Munat

# Codex Naming and Value Specification

This document defines the **core surface vocabulary**, **naming rules**, and **literal value spellings** used throughout the Codex language.

Naming and value rules are part of the Codex language specification and are governed by this document.

This document is **Normative**.

---

## 1. Purpose

This specification defines the **terminology, naming rules, and literal value forms**
used to describe Codex.

Its goals are to:

* minimize cognitive load by making Codex read like **plain English**
* avoid confusion with HTML, XML, programming languages, and UI frameworks
* ensure humans, tools, and LLMs reason consistently about Codex
* ensure Codex remains **markup, not code**

This specification governs **naming and literal values only**.
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

* `<Recipe id=recipe:spaghetti>` → Entity
* `<Step>` → not an Entity (unless schema explicitly authorizes it)

Notes:

* The `id` value is an **IRI reference**, not a display label.
* `id` values are written as **unquoted tokens** (see §4.10).
* Consuming systems commonly resolve `id` values against a module-defined base (see the Codex ID Resolution Specification).

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

**Whitelisted exception:**

* `uri` is explicitly permitted by this specification.

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

* `3.141500p`
* `3p`

**Explicit precision**

* `3p6`
* `3.1415p6`

Codex does not normalize precision numbers.

---

### 4.4 Enumerated Token Values

Enumerated values are symbolic tokens drawn from a **schema-defined closed set**.

Form:

```
$Identifier
```

Rules:

* `$` introduces an enumerated token
* `Identifier` MUST follow Concept naming rules (PascalCase recommended)
* Enumerated tokens are **not strings**
* Codex does not define or validate the allowed set

Examples:

```xml
alignment=$Center
status=$Draft
tone=$Friendly
```

---

### 4.5 List Values

Lists are written using square brackets:

```text
[ value, value, ... ]
```

Rules:

* Lists are ordered
* Lists may be empty
* List items MAY be any valid Codex Value spelling
* Lists may be mixed or homogeneous, as defined by schema
* Lists may be nested
* Lists are not expanded by Codex

Examples:

```xml
friends=["sam", "ted", "mary"]
value=[33, "bob", false, ["x", "y", 3], {now}, 1..42]
```

**Parsing rule (Normative):**

* Lists are parsed as a sequence of Value items separated by commas at the list’s top level.
* Nested list brackets `[...]`, temporal braces `{...}`, and color parentheses `(...)` are balanced and do not split items.

---

### 4.6 Range Values

Ranges are declarative interval literals.

Form:

```
start..end
```

Rules:

* Ranges are **inclusive**
* `start` and `end` are any valid Codex Value spellings
* Whether a given range is meaningful is schema-defined
* Ranges are not evaluated or expanded by Codex
* Ordering is preserved as written

Examples:

```xml
ages=3..6
letters="A".."Z"
window={2026-01-01}..{2026-12-31}
```

---

#### 4.6.1 Stepped ranges

Ranges MAY include an explicit step:

```
start..end s step
```

No spaces are permitted.

The `step` MAY be one of:

1. **Numeric literal**

Examples:

```
1..10s2
"A".."Z"s2
```

2. **Keyword step**

Forms:

```
(unit)
N(unit)
```

Where:

* `unit` is a schema-authorized identifier
* `N` is a non-negative integer
* No operators, spaces, or nesting are permitted

Examples:

```
{2026-01-01}..{2026-12-31}s(month)
{2026-01-01}..{2026-12-31}s3(month)
```

3. **Duration literal**

Form:

```
s{P...}
```

Examples:

```
{2026-01-01}..{2026-12-31}s{P3M}
{2026-01-01}..{2026-12-31}s{P3M5D}
```

Notes:

* Steps annotate the range; they do not imply enumeration
* Inclusivity applies to interval endpoints only

---

### 4.7 Temporal Values

Temporal Values are written using **curly braces** `{...}`.

They are literal spellings of ISO 8601 forms.

#### 4.7.1 Date

```
{YYYY-MM-DD}
```

Example:

```
{2026-01-01}
```

---

#### 4.7.2 DateTime

```
{YYYY-MM-DDThh:mm:ss(.sss)?(Z|±HH:MM)}
```

A timezone designator is REQUIRED.

Example:

```
{2023-10-27T14:30:15+02:00}
```

---

#### 4.7.3 Duration

```
{P...}
```

Example:

```
{PT3M15S}
```

---

#### 4.7.4 Special temporal values

Reserved literals:

* `{now}`
* `{today}`

Interpretation is consumer-defined.

---

### 4.8 Color Values

Color Values are literal spellings representing a color.

Codex does not interpret, validate, normalize, or convert colors.

#### 4.8.1 Hex color literals

Permitted forms:

* `#RGB`
* `#RGBA`
* `#RRGGBB`
* `#RRGGBBAA`

Examples:

* `#f00`
* `#f00f`
* `#ff0000`
* `#ff000080`

---

#### 4.8.2 Functional color literals

Functional forms are **atomic literals**, not expressions.

Examples (non-exhaustive):

```
rgb(255,0,0)
rgb(255 0 0 / 0.5)
hsl(120,100%,50%)
hsl(120 100% 50% / 0.5)
oklch(62.8% 0.25 29)
color(display-p3 1 0 0)
```

Rules:

* Parentheses are required
* Codex does not define internal separators, units, or parameter conventions
* Codex performs no whitespace normalization inside the parentheses

---

#### 4.8.3 Named colors

Named colors are represented as **string values**.

Codex defines no global set of named colors.

Example:

```xml
color="firebrick"
```

---

### 4.9 UUID Values

UUID Values are literal spellings representing a UUID.

Form:

```
[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}
```

Rules:

* UUID Values are **not strings**.
* UUID Values MUST NOT contain braces.
* Case is not semantically significant.
* Codex does not mandate a UUID version.

Examples:

```xml
uuid=017f22e2-79b0-7cc3-98c4-dc0c0c07398f
```

---

### 4.10 IRI Reference Values

An **IRI reference value** is an unquoted token used to express identity and references.

Form:

* a single token with no whitespace

Rules:

* IRI reference values are **not strings**.
* Codex does not validate full IRI grammar.
* IRI reference values MUST be written without leading or trailing whitespace.

Special-case (Normative):

The following Traits MUST use IRI reference values (unquoted):

* `id`
* `idBase`
* `reference`
* `target`
* `for`
* `key`

All other Traits MUST NOT accept IRI reference values unless explicitly defined by a future revision of this specification.

Examples:

```xml
<Recipe id=recipe:spaghetti key=spaghetti />
<Module idBase=https://paperhat.dev/id/ />
<View target=recipe:spaghetti />
```

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

## 9. Relationship to Other Specifications (Normative)

This specification must be read in conjunction with:

- the **Codex ID Resolution Specification**
- the **Codex View Definition Specification**

In case of conflict:

- naming and literal spelling rules in this document prevail
- identity resolution rules are governed exclusively by the ID Resolution Specification
- View structure and projection rules are governed exclusively by the View Definition Specification

## 10. Summary

* Codex is written in **Concepts**
* Concepts declare **Traits**
* Traits bind names to **Values**
* Values are literal spellings, not expressions
* Enumerated values are written as `$EnumToken`
* Concepts may carry **Content**
* A Concept is an **Entity if and only if it declares an `id` Trait**
* Naming and values are plain-English, declarative, and schema-scoped
* Lists, ranges, stepped ranges, temporal values, precision numbers, enumerations, and color literals are first-class data forms

---

**End of Codex Naming and Value Specification**
