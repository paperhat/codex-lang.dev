# Codex Terminology Guardrails Contract (DRAFT)

## Status

- **DRAFT**  
- Normative once locked  
- Applies to all Codex documentation, schemas, tooling, prompts, and LLM-assisted authoring

---

## 1. Purpose

This contract defines **terminology guardrails** for Codex.

Its goals are to:

- prevent vocabulary drift
- eliminate markup-system and programming-language leakage
- ensure consistent reasoning by humans and LLMs
- make Codex mechanically and semantically unambiguous

This contract governs **language usage**, not surface syntax or schema semantics.

---

## 2. Canonical Vocabulary (Normative)

The following terms are **canonical** and MUST be used with their defined meanings.

### Core Terms

- **Concept** — the primary semantic construct in Codex
- **Trait** — a named characteristic of a Concept
- **Value** — a literal datum bound to a Trait
- **Content** — opaque narrative text carried by a Concept
- **Entity** — a Concept with identity (`id`)
- **Marker** — a syntactic delimiter for Concept instances

These terms are defined in the Naming Contract and Glossary.

---

### Annotation Terms

The following terms are canonical for non-normative author notes.

- **Annotation** — a non-normative, author-supplied textual note preserved through the Codex pipeline
- **Editorial Annotation** — an annotation intended for authors and tooling, not for default rendering
- **Output Annotation** — an annotation explicitly intended for possible downstream rendering or narration
- **Annotation Kind** — a schema-defined classification describing the intent of an annotation (e.g. `note`, `warning`, `todo`)

Annotations:

- do **not** alter domain semantics
- do **not** affect validation
- are **preserved intentionally**, not treated as disposable comments

---

## 3. Forbidden Vocabulary (Normative)

The following terms MUST NOT be used to describe Codex constructs, either in documentation, tooling, or LLM output.

### Forbidden as replacements for **Concept**

- element
- component
- tag
- node
- class
- object

### Forbidden as replacements for **Trait**

- attribute
- prop
- property
- field
- parameter

### Forbidden for surface syntax

- tag
- start tag
- end tag
- open tag
- close tag

Use **marker** instead.

---

### Forbidden Annotation Terminology

The following terms MUST NOT be used to describe Codex annotations:

- comment
- code comment
- inline comment
- XML comment
- HTML comment

Codex does **not** have comments.
Codex has **annotations**.

---

## 4. Casing Guardrails (Normative)

Codex naming MUST follow these rules:

- Concept names → **PascalCase**
- Trait names → **camelCase**
- No kebab-case
- No snake_case
- No SCREAMING_CASE

Initialisms and acronyms capitalize **only the first letter**.

Examples (valid):

- `AstNode`
- `PlainHtml`
- `FbiAgent`

Examples (invalid):

- `ASTNode`
- `plainHTML`
- `FBIAgent`

---

## 5. Abbreviation Guardrails (Normative)

Abbreviations are avoided in Codex naming.

- General abbreviations MUST NOT be used unless explicitly whitelisted
- Periods are never permitted in Concept or Trait names
- Shorthand Trait names are forbidden

Invalid Trait names include:

- `ref`
- `lang`
- `href`

Use plain English instead:

- `reference`
- `language`
- `uri` (or a more specific English alternative)

---

## 6. Context Sensitivity Rule (Normative)

Codex terms are **context-sensitive**.

- Names do not have global meaning
- Meaning is defined by schema and containment context
- The same name MAY have different meaning in different schemas

LLMs MUST NOT assume that a Concept name has universal semantics.

---

## 7. LLM-Specific Requirements (Normative)

When generating Codex-related output, LLMs MUST:

- use canonical Codex terminology
- avoid forbidden vocabulary
- respect casing and abbreviation rules
- distinguish semantic Concepts from syntactic markers
- distinguish **annotations** from Content and Concepts
- avoid introducing new terms unless explicitly instructed

LLMs MUST NOT:

- substitute non-Codex terms for Codex terms
- refer to annotations as comments
- infer semantics from surface syntax
- invent Concepts or Traits not defined by schema
- conflate Concepts with markers

---

## 8. Validation and Enforcement

Tooling MAY enforce this contract via:

- documentation linting
- prompt constraints
- static analysis
- CI checks on generated output

Violations of this contract are **authoring errors**, not stylistic issues.

---

## 9. Non-Goals

This contract does **not**:

- define schema semantics
- define parsing or formatting rules
- define IR or compilation behavior
- constrain prose Content

It exists solely to lock **language discipline**.

---

## 10. Summary

- Codex terminology is closed and intentional
- Canonical terms are mandatory
- Markup- and code-derived vocabulary is forbidden
- **Annotations are not comments**
- Casing and abbreviation rules are strict
- Context determines meaning
- Guardrails exist primarily for LLM correctness

