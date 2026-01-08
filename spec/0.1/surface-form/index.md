Status: NORMATIVE  
Version: 0.1  
Editor: Charles F. Munat

# Codex Surface Form Contract — Version 0.1

This document defines the **canonical textual surface form** of **Codex** (the language),
as expressed in `.cdx` files.

Its purpose is to ensure that Codex is:

- deterministic
- round-trippable without source offsets
- mechanically enforceable
- human-readable with minimal cognitive load
- unambiguous for compilation to triples

This document is **Normative**.  
Any `.cdx` file that does not conform to this contract is **not Codex** and MUST be rejected.

---

## 1. Canonical Formatting Model

Codex has **exactly one canonical surface form**.

All Codex processing follows this rule:

> `parse → validate → normalize → (re-parse optional) → proceed`

The canonical form is produced by the Codex formatter.  
Any valid Codex AST MUST serialize to **exactly one** canonical textual representation.

---

## 2. Indentation and Whitespace

### Indentation

- Exactly **one tab per nesting level**
- Tabs are canonical
- Parsers MAY accept spaces if indentation is consistent
- Canonical output ALWAYS uses tabs

### Whitespace normalization

- Leading and trailing whitespace outside the document is removed
- The file ends with **exactly one newline**
- No trailing whitespace is permitted on any line

---

## 3. Quotes and Escaping

- **Trait values use double quotes only** (`"`)
- Single quotes (`'`) are never special and never require escaping
- Smart quotes are invalid

### Escaping

- Backslash escape (`\`) is used

Required escapes:

- `\"` for double quote
- `\\` for backslash
- `\n`, `\t` where required

Codex is **not XML**:

- `<`, `>`, and `&` do **not** require escaping inside quoted strings or text nodes
- There are no entity encodings (`&lt;`, `&amp;`, etc.)

---

## 4. Concepts and Structure

### Concept Markers

Codex uses **markers** to denote the boundaries of Concept instances in the surface form.

Markers are **purely syntactic** and have **no semantic meaning**.

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
Concepts are semantic constructs; markers only delimit surface structure.

Malformed, mismatched, or invalid markers result in **parse errors**.

---

### Single Root

- Each `.cdx` file has **exactly one root Concept**
- Any Concept MAY be a root
- A Codex file MAY represent:
  - a single domain individual
  - a domain collection
  - a Module assembly

Codex assigns **no semantic meaning to file boundaries**.

When multiple artifacts appear in one file, they MUST be explicitly grouped using a
domain collection or a Module, according to intent.

---

### Empty Concepts

- Concepts with no content MUST be written as self-closing:

```cdx
<Title />
````

* Expanded empty forms are invalid:

```cdx
<Title>
</Title>
```

* Whether a Concept MAY be empty is defined by schema
* Semantically meaningless empty Concepts are schema errors and halt compilation

---

## 5. Traits

* No whitespace around `=`:

```cdx
amount=200
optional=false
name="Spaghetti"
```

* Traits are printed in canonical order (defined by schema and global rules)

### Trait Values

* Strings are quoted
* Numbers are unquoted
* Booleans are unquoted (`true`, `false`)
* `null` does not exist in Codex

---

### Numeric Types

Codex supports unquoted numeric literals.
Their **semantic type** is defined by ontology/schema, not syntax.

Examples (illustrative):

* Integer (bigint)
* WholeNumber (safe integer)
* Fraction
* PrecisionNumber
* SafeFloat
* Imaginary / complex (future-capable)

The canonical printer MAY normalize numeric literals.
Semantic typing is enforced by schema validation.

---

### Boolean Traits

Boolean traits MAY be written as:

* presence-only (indicating `true`), or
* explicitly as `=true`

The canonical surface form is **presence-only**.

Boolean traits MUST NOT be written with `=false`.
Absence indicates the trait is unspecified.

---

## 6. Content and Text Nodes

Codex strictly separates **structure** from **content**.

### General Text Content

* Text is treated as **opaque data**
* Codex does not interpret prose
* Whitespace is collapsed unless explicitly designated as preformatted
* Codex does not interpret, annotate, or assign meaning to inline text during parsing,
  validation, or compilation

---

### Line Wrapping

* The canonical formatter enforces a maximum line width (TBD)
* Long tokens MAY be split using a trailing `\`
* Continuation lines ignore indentation for width calculation

---

### Preformatted Text

Preformatted content is a distinct case:

* Explicitly designated (mechanism defined elsewhere)
* Whitespace and newlines are preserved exactly

---

## 7. No Inline Formatting in Codex

Codex provides **no inline formatting constructs**.

* There is no inline vs block distinction
* All Concepts are structural
* Formatting such as emphasis, links, stress, or decoration is **not part of Codex**

Codex treats all textual content as **opaque data** throughout its language phases.
Any interpretation or enrichment of inline text occurs **outside the Codex language**,
during rendering or target-specific processing, and does not affect Codex semantics,
validation, or storage.

This separation is deliberate and fundamental.

---

## 8. Sectioning and Blank Lines

* Codex has no intrinsic notion of sections
* Blank lines are controlled by schema-defined sectioning Concepts
* Sectioning Concepts MAY be separated from siblings by a single blank line
* No blank lines appear immediately inside a parent Concept

All blank-line behavior is deterministic and schema-driven.

---

## 9. Annotations

Codex supports **annotations**: non-normative, author-supplied notes preserved through
the full pipeline.

Annotations:

* are not Content
* do not affect semantics or validation
* never alter meaning
* are fully round-trippable

---

### 9.1 Editorial Annotations (`[ ... ]`)

Editorial annotations use square brackets:

```text
[This is an editorial annotation.]
```

Properties:

* Single-line or multi-line
* Whitespace inside brackets is not semantically significant
* May appear anywhere whitespace is permitted outside Content
* Are literal text inside Content

Editorial annotations:

* Attach to the **next Concept instance** in document order
* Are preserved through AST, IR, and storage
* Are ignored by default in non-Codex renderers

---

### 9.2 Typed Editorial Annotations

Editorial annotations MAY specify a kind:

```text
[kind: annotation text]
```

Rules:

* `kind` is a single word
* `:` is required
* Space after `:` is optional

Unrecognized kinds default to `note`.

---

### 9.3 Output Annotations (`<Annotation>`)

Codex defines an explicit **Annotation Concept**:

```cdx
<Annotation kind="warning">
	Do not brown the garlic.
</Annotation>
```

* `<Annotation>` is a normal Concept
* It attaches to its parent Concept
* It carries opaque textual Content
* It is preserved through the pipeline

Renderers MAY emit output annotations according to target policy.

---

### 9.4 Annotation Kinds

Annotation kinds are schema-defined and closed.

Illustrative examples:

* `note`
* `warning`
* `todo`
* `rationale`
* `question`
* `example`
* `provenance`

Schemas MAY extend this set.

---

## 10. Enforcement

A `.cdx` file is valid Codex **iff**:

1. It parses
2. It validates against schema
3. It normalizes to canonical form
4. Canonical form MAY re-parse to an equivalent AST

Non-conforming files MUST be rejected.

---

## 11. Purpose of This Contract

This contract guarantees:

* deterministic formatting
* lossless semantic round-tripping
* stable compilation to triples
* elimination of offset dependence
* low cognitive load for humans and LLMs
* mechanical enforcement of correctness

---

End of Codex Surface Form Contract v0.1.
