# Codex Surface Form Contract (DRAFT)

This document defines the **canonical textual form** of Codex (the language), as expressed in `.cdx` files.

Its purpose is to ensure that Codex is:

- deterministic
- round-trippable without source offsets
- mechanically enforceable
- human-readable with minimal cognitive load
- unambiguous for compilation to triples

This contract is **normative**. Any `.cdx` file that does not conform is **not Codex** and must be rejected.

---

## 1. Canonical Formatting Model

Codex has **one canonical surface form**.

All Codex processing follows this rule:

> `parse → validate → normalize → (re-parse optional) → proceed`

The canonical form is produced by the Codex formatter.
Any valid Codex AST must serialize to **exactly one** canonical textual representation.

---

## 2. Indentation and Whitespace

- **Indentation:**
  - Exactly **one tab per nesting level**
  - Tabs are canonical
  - Parsers may optionally accept spaces if indentation is consistent
  - Canonical output always uses tabs

- **Whitespace normalization:**
  - Leading and trailing whitespace outside the document is removed
  - The file ends with **exactly one newline**
  - No trailing whitespace on lines

---

## 3. Quotes and Escaping

- **Trait values use double quotes only** (`"`).
- Single quotes (`'`) are never special and never need escaping.
- Smart quotes are invalid.

### Escaping

- Backslash escape (`\`) is used.

- Required escapes:
  - `\"` for double quote
  - `\\` for backslash
  - `\n`, `\t` where needed

- Codex is **not XML**:
  - `<`, `>`, and `&` do **not** require escaping inside quoted strings or text nodes.

There are no entity encodings (`&lt;`, `&amp;`, etc.) in Codex.

---

## 4. Concepts and Structure

### Concept Markers

Codex uses **markers** to denote the boundaries of Concept instances in the surface form.

A **marker** is a purely syntactic construct. Markers have **no semantic meaning**.

There are three kinds of Concept markers:

- **Opening Concept marker**
  Begins a Concept instance
  Example: `<Recipe>`

- **Closing Concept marker**
  Ends a Concept instance
  Example: `</Recipe>`

- **Self-closing Concept marker**
  Represents an empty Concept instance
  Example: `<Title />`

Markers are not Concepts.

A Concept is a semantic construct; markers merely delimit where a Concept instance begins and ends in the surface form.

Malformed, mismatched, or invalid Concept markers result in **parse errors**.

### Single root

- Each `.cdx` file has **exactly one root concept**.
- Any concept may be a root (`<Recipe>`, `<Recipes>`, `<RecipeView>`, `<Module>`, etc.).
- A Codex file may contain:
  - a single domain individual
  - a domain collection
  - or a Module assembly

- Codex imposes **no semantic meaning on file boundaries**.
- When multiple artifacts appear in one file, they must be explicitly grouped using either a **domain collection** or a **Module**, according to intent.

### Empty concepts

- Concepts with no content **must** be written as self-closing tags:

  ```
  <Title />
  ```

- Expanded empty forms are invalid:

  ```
  <Title>
  </Title>
  ```

- Whether a concept _may_ be empty is defined by the schema.

- Semantically meaningless empty concepts are schema errors and halt compilation.

---

## 5. Traits

- No whitespace around `=`:

  ```
  amount=200
  optional=false
  name="Spaghetti"
  ```

- Traits are printed in canonical order (defined by schema + global rules).

- Trait values:
  - **Strings** are quoted
  - **Numbers** are unquoted
  - **Booleans** are unquoted (`true`, `false`)
  - `null` does not exist in Codex

### Numeric types

Codex supports unquoted numeric literals. Their **semantic type** is determined by the ontology/schema, not by syntax.

Examples of semantic numeric types include (non-exhaustive):

- Integer (bigint)
- WholeNumber (safe integer)
- Fraction
- PrecisionNumber
- SafeFloat
- Imaginary / complex (future-capable)

The canonical printer may normalize numeric literals, but semantic typing is enforced by schema validation.

### Boolean Traits

Traits whose schema-defined value type is boolean MAY be written either:

- as a bare trait name, indicating true, or
- with an explicit `=true` value.

The canonical surface form for boolean traits is presence-only.

Boolean traits MUST NOT be written with `=false`.
Absence of a trait indicates that it is unspecified.

---

## 6. Content and Text Nodes

Codex distinguishes **structure** from **content**.

### General text content

- Text is treated as **opaque data**.
- Codex does not interpret prose.
- Whitespace is collapsed unless explicitly marked as preformatted.

### Line wrapping

- Canonical formatter enforces a maximum line width (TBD, likely 100 chars).
- Long tokens (e.g. URLs) may be split:
  - A trailing `\` indicates continuation
  - Continuation lines ignore indentation for width calculation

### Preformatted text

- Preformatted content (e.g. poetry, code, precise layout) is a **separate case**
- It will be explicitly designated (mechanism TBD)
- Newlines and spacing are preserved exactly

---

## 7. No Inline Formatting in Codex

Codex **does not support inline formatting**.

- There is no concept of “inline vs block” in Codex.
- All concepts are structural.
- Formatting such as bold, emphasis, stress, links, etc. is **not Codex**.

If rich textual markup is needed:

- It is encoded as **opaque content**
- Or handled by a **separate markup language**, explicitly embedded as data

This is a deliberate design decision to avoid HTML-style semantic confusion.

---

## 8. Sectioning and Blank Lines

- Codex itself has no notion of “block” vs “inline”.
- Blank lines are controlled by **schema-designated sectioning concepts**.
- Sectioning concepts may be separated from siblings by a single blank line.
- No blank lines appear immediately inside a parent concept.

All blank line rules are deterministic and schema-driven, not heuristic.

---

## 9. Annotations

Codex supports **annotations**: non-normative, author-supplied textual notes that are preserved through the full Codex pipeline.

Annotations are **not Content**, do not affect validation or semantics, and never alter the meaning of Concepts or Traits.

Annotations exist to preserve **authorial intent, rationale, and editorial context**, and are fully round-trippable.

---

### 9.1 Editorial Annotations (`[ ... ]`)

Editorial annotations use square brackets:

```
[This is an editorial annotation.]
```

#### Properties

- May be **single-line or multi-line**
- Whitespace inside the brackets is not semantically significant
- May appear anywhere **outside Content** where whitespace is allowed
- Are **not recognized inside Content** and are treated as literal text there

Editorial annotations:

- Attach to the **next Concept instance** in document order
- Are preserved through AST, IR, and triple storage
- Are ignored by default in non-CDX renderers (HTML, PDF, voice, etc.)

---

### 9.2 Typed Editorial Annotations

Editorial annotations MAY specify a kind using an editor-style prefix:

```
[kind: annotation text]
```

Rules:

- `kind` must be a single word
- The colon (`:`) is required
- A space after the colon is optional

If `kind` matches a schema-defined annotation kind, it is recorded as such.

If `kind` is not recognized, the entire annotation is treated as plain text and the kind defaults to `note`.

Example:

```
[todo: verify cooking time]
```

Example (untyped due to unrecognized prefix):

```
[bob says: this sucks]
```

---

### 9.3 Output Annotations (`<Annotation>`)

Codex also defines an explicit **Annotation Concept**:

```
<Annotation kind="warning">
	Do not brown the garlic.
</Annotation>
```

Properties:

- `<Annotation>` is a normal Concept
- It attaches to its **parent Concept**
- It carries opaque textual Content
- It is preserved through the full pipeline

Output annotations MAY be rendered by downstream targets (HTML, voice, etc.), according to renderer policy.

---

### 9.4 Annotation Kinds

Annotation kinds are defined by schema as a **closed enumerated set**.

Typical kinds include (illustrative, not normative):

- `note`
- `warning`
- `todo`
- `rationale`
- `question`
- `example`
- `provenance`

Schemas may extend this set.

---

## 10. Enforcement

A `.cdx` file is valid Codex **iff**:

1. It parses
2. It validates against the ontology/schema
3. It can be normalized into canonical form
4. (Optionally) canonical form re-parses to an equivalent AST

Non-conforming files are rejected.

---

## 11. Purpose of This Contract

This surface form contract exists to guarantee:

- Deterministic formatting
- Lossless semantic round-tripping
- Stable compilation to triples
- Elimination of offset/column dependence
- Low cognitive load for humans and LLMs
- Mechanical enforcement of correctness

---

### Status

- **DRAFT**
- Intended to be stored in the Codex repository
- To be reviewed, finalized, then **LOCKED**
