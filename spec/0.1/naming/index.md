# Codex Naming Contract (DRAFT)

## Status

- **DRAFT**
- Normative once locked
- Applies to all Codex documentation, tooling, and error messages

---

## 1. Purpose

This contract defines the **core naming vocabulary** and **naming rules** used to describe Codex.

Its goals are to:

- minimize cognitive load by making Codex read like **plain English**
- avoid confusion with HTML / XML / SGML, UI frameworks, and OO terminology
- ensure humans, tools, and LLMs reason consistently about Codex

This contract governs **naming only**. It does not restrict prose or other **Content**.

---

## 2. Core Terms (Normative)

### 2.1 Concept

A **Concept** is the primary surface construct in Codex.

A Concept is:

- a named declarative unit
- composed of **Traits** and child Concepts
- optionally identified with an `id`
- purely declarative (never imperative)

Examples:

- `<Recipe>`
- `<Step>`
- `<Policy>`
- `<Module>`

Notes:

- “Concept” refers to the _surface construct_, not a philosophical abstraction.
- Not all Concepts are entities.

---

### 2.2 Trait

A **Trait** is a named distinguishing characteristic of a Concept.

A Trait:

- binds a **name** to a **Value**
- is declared inline on a Concept
- is schema-defined
- has no independent identity

Examples:

- `name="Bob"`
- `amount=200`
- `optional=false`

---

### 2.3 Value

A **Value** is a literal datum.

Values include:

- strings
- numbers
- booleans

Values are:

- immutable
- schema-typed
- never narrative

Examples:

- `"Bob"`
- `200`
- `true`

---

### 2.4 Content

**Content** is opaque narrative data.

Content:

- is not interpreted by Codex
- may contain prose, code, poetry, or markup
- is always carried inside a Concept

Example:

```xml
<Description>
	A cool dude.
</Description>
```

---

### 2.5 Entity

An **Entity** is a Concept that has identity.

- A Concept **is an Entity iff it has an `id` Trait**
- Entity identity is semantic and graph-addressable
- Identity requirements are defined by schema, not by syntax

Examples:

- `<Recipe id="recipe:spaghetti">` → Entity
- `<Step>` → not an Entity (unless schema explicitly allows it)

---

## 3. Naming and Casing Rules (Normative)

This section defines naming rules for Concept and Trait names.

These rules apply **only to naming**. They do not restrict prose or other Content.

---

### 3.1 Case Conventions

- **Concept names** MUST use **PascalCase**
- **Trait names** MUST use **camelCase**

The following styles are forbidden everywhere in Codex naming:

- kebab-case
- snake_case
- SCREAMING_CASE
- mixed or inconsistent casing

---

### 3.2 Abbreviations (Naming Only)

Codex avoids abbreviations in names.

- In prose, general abbreviations are often identifiable by a trailing period (e.g. “Chas.” for “Charles”).
- Periods are **never permitted** in Concept or Trait names.
- Therefore, general abbreviations MUST NOT be used in Codex naming unless explicitly whitelisted.
- When in doubt, names MUST be spelled out in full.

This rule applies **only to naming**, not to Content.

---

### 3.3 Initialisms and Acronyms

Initialisms and acronyms MAY be used when widely understood.

For naming purposes:

- Initialisms are sequences of letters pronounced individually (e.g. FBI, CIA).
- Acronyms are initialisms intended to be pronounced as words, and may include extra letters for readability.

Both are treated identically for casing.

#### Capitalization Rule (Normative)

- Only the **first letter** is capitalized.
- Remaining letters follow normal word casing.

Examples (correct):

- `AstNode`
- `FbiAgent`
- `PlainHtml`
- `LatexDocument`

Examples (invalid):

- `ASTNode`
- `FBIAgent`
- `PlainHTML`
- `plainHTML`

---

### 3.4 No Shorthand Traits

Shorthand Trait names are forbidden.

Examples of invalid Trait names:

- `ref`
- `lang`
- `href`

Trait names MUST use plain English:

- `reference`
- `language`
- `uri` (or a more specific plain-English alternative)

Longer names are preferred over abbreviated or opaque ones.

---

### 3.5 Design Intent

These rules exist to ensure that Codex:

- reads as **plain English**
- minimizes cognitive load
- avoids legacy markup and programming-language conventions
- remains approachable to humans and LLMs alike

---

## 4. Trait Authorization and Reference Traits (Normative)

### 4.1 Traits Are Schema-Authorized

Traits are **never global**.

All Traits are **authorized by schema** and may be restricted to Concepts in specific semantic roles.

A Trait is valid **only** when explicitly allowed for the Concept on which it appears.

---

### 4.2 Identity Traits

The following Trait is authorized **only** for Entity Concepts:

- `id`

Declaring an `id` Trait makes a Concept an Entity.

Concepts that are not Entities **must not** declare an `id` Trait.

---

### 4.3 Reference Traits

Reference Traits bind a Concept to another Entity by identifier (IRI).

- `reference` is the identifier (IRI) of another Entity.
- Reference Traits are authorized only for Concepts whose schema-defined role is referential.

Codex defines three reference-trait names with distinct intent:

- `reference` — a generic declarative pointer to another Entity (default)
- `target` — the Entity that this Concept is about / applied to / oriented toward
- `for` — the Entity (or Concept kind) this Concept is intended for / applies to

These are naming and intent distinctions. Their precise semantics are defined by schema.

#### Singleton Rule (Normative)

A Concept MUST NOT declare more than one of the following Traits:

- `reference`
- `target`
- `for`

unless explicitly permitted by schema.

---

### 4.4 Examples of `for` (Naming-Intent Examples)

`for` is used when the meaning is **applicability or scope**, not generic reference and not “acted upon”.

Examples (illustrative):

- A view definition that applies to a Concept kind: a view “for Recipe”
- A policy definition that applies to a Concept kind: a policy “for User”
- A configuration Concept that applies to a subsystem concept: config “for SearchIndex”

`for` is declarative scope. It is not UI wiring.

---

## 5. Context and Scope (Normative)

### 5.1 Context-Sensitive Meaning

Concept and Trait names do not have global meaning in Codex.

Their meaning is interpreted within a **schema-defined context**.

The same name MAY have different meaning in different contexts.

---

### 5.2 Structural Meaning Is Contextual

Some Concept names are structural within specific contexts.

Example: within a Codex module-assembly context, the Concept `Module` has assembly meaning because the schema defines it as such.

Outside that context, `Module` is just a name that another schema may define differently.

Codex avoids global prefixing (e.g. `CodexModule`) in favor of schema-scoped meaning.

---

## 6. Structural vs Semantic Concepts

This distinction is **terminological only** (no syntax difference):

- **Semantic Concepts** express domain meaning
  (e.g. `Recipe`, `Person`, `Policy`)
- **Structural Concepts** organize or group meaning
  (e.g. `Steps`, `Data`, `Policies`)

Authors do **not** need to reason about this distinction while writing Codex. It exists to support clear documentation and tooling.

---

## 7. Entity and Identity Rules (Normative)

### 7.1 Identity Is Explicit

A Concept is an Entity **if and only if** it declares an `id` Trait.

Nothing else makes something an Entity.

---

### 7.2 Schema Controls Entity Eligibility

Which Concepts may or must be Entities is defined by schema.

- Some Concepts **must** be Entities (e.g. `Recipe`, `Module`).
- Some Concepts **must never** be Entities (e.g. value-like or structural Concepts such as `Step`, `Description`, `Data`), unless schema explicitly allows it.

This prevents accidental identity explosion and graph pollution.

---

## 8. Forbidden Vocabulary (Normative)

The following terms MUST NOT be used to describe Codex constructs, as they introduce ambiguity or legacy semantics.

Forbidden as replacements for **Concept**:

- element
- component
- tag
- node
- class

Forbidden as replacements for **Trait**:

- prop
- property
- attribute
- field
- parameter

---

## 9. Summary

- Codex is written in **Concepts**
- Concepts declare **Traits**
- Traits bind names to **Values**
- Concepts may carry **Content**
- A Concept is an **Entity iff it has an `id` Trait**
- Naming is plain-English, case-disciplined, and schema-scoped
- `reference`, `target`, and `for` are distinct reference-trait names with a singleton rule
