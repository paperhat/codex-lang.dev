Status: NORMATIVE  
Version: 0.1  
Editor: Charles F. Munat

# Codex Inline Text Markup Contract — Version 0.1

This document defines a **target-agnostic inline text markup language** that MAY appear
inside Codex **Content**.

This contract defines a **Content sub-language**.  
It does **not** define Codex Concepts, Traits, or surface structure.

This document is **Normative**.

---

## 1. Purpose

This contract defines an inline text markup language intended for **post-Codex
interpretation of Content text**.

Its goals are to:

- provide visible, explicit, editor-friendly inline styling without a rich-text editor
- avoid HTML, XML, and Markdown conventions and failure modes
- keep Codex Concepts hygienic by confining presentation markup to Content
- support deterministic parsing and lossless round-tripping
- allow rendering to multiple targets (DOM, HTML, PDF, voice, etc.) without naming target technologies

This contract governs **inline markup embedded in Content strings only**.

---

## 2. Relationship to Codex

- Codex **does not parse** inline text markup.
- Codex treats Content as **opaque text data**.
- Inline text markup is interpreted **only** by tooling or renderers that explicitly opt
  into this contract.

A `.cdx` file MAY be valid Codex regardless of whether inline markup is present or valid.

Tooling MUST report inline text markup errors **separately** from:

- Codex surface form errors
- Codex parse errors
- Codex schema or validation errors

---

## 3. Inline Markup Form

Inline markup uses **brace spans**:

```text
{kind: text}
````

A brace span applies a style or class intent to the **span content** (`text`).

Rules:

* `kind` is a single token (see §4)
* The first `:` following `kind` is the delimiter
* A single optional space after `:` is permitted and ignored

The following forms are equivalent:

* `{b: bold}`
* `{b:bold}`

Brace spans MAY span multiple lines.

Brace spans MUST be properly nested (see §6).

---

## 4. Built-in Kinds (Normative)

Inline markup defines a small, closed set of built-in kinds.

### 4.1 Canonical Built-in Kinds (Unshadowable)

The following kind names are **canonical** and MUST NOT be shadowed by aliases:

* `bold`
* `italic`
* `strikethrough`
* `underline`
* `overline`
* `class`

These canonical names MUST always retain their defined meaning.

---

### 4.2 Shortcut Built-in Kinds (Shadowable)

The following shortcut kinds are provided for authoring convenience and MAY be shadowed
by aliases:

* `b` (default meaning: `bold`)
* `i` (default meaning: `italic`)
* `s` (default meaning: `strikethrough`)
* `u` (default meaning: `underline`)
* `o` (default meaning: `overline`)

Shortcuts exist to reduce authoring friction, not to define semantics.

---

## 5. Style Aliases (Normative)

Inline markup supports declaring **aliases** to reusable style identifiers.

An alias maps a short name to a style identifier string:

```text
{style: hs = header-style}
```

### 5.1 Alias Declaration Form

* Alias declarations use the directive form:

  ```text
  {style: <alias> = <styleIdentifier>}
  ```

* Alias declarations MUST appear at the beginning of the Content value, before any
  non-directive text.

* `<alias>` MUST be a single token.

* `<styleIdentifier>` is an opaque identifier string.

---

### 5.2 Alias Resolution

* After declaration, `{hs: ...}` applies the mapped style identifier.
* Aliases MAY shadow shortcut built-ins.
* Aliases MUST NOT shadow canonical built-ins.

---

### 5.3 Shadowing Policy (Normative)

If an alias shadows a shortcut built-in:

* the alias takes precedence for that shortcut
* the canonical built-in remains available under its canonical name

Example:

```text
{style: b = brand-emphasis}
Then: {b: This uses brand-emphasis.}
But: {bold: This always means bold.}
```

---

## 6. Nesting and Overlap Rules (Normative)

Brace spans MUST be **properly nested**.

Valid:

```text
{bold: This is {italic: very} important.}
```

Overlap is forbidden.

Any input that cannot be parsed as properly nested brace spans is invalid under this
contract.

---

## 7. Unrecognized Kinds (Normative)

If a brace span uses a `kind` that is not:

* a built-in kind, or
* a declared alias

then the entire brace span is treated as **literal text**.

Example:

```text
{Tom: this is what I think!}
```

This MUST NOT be interpreted as markup.

---

## 8. Escaping (Normative)

To include literal characters inside recognized brace spans:

* `\{` for literal `{`
* `\}` for literal `}`
* `\\` for literal `\`

Escaping is meaningful only to tools that interpret inline markup.
Codex itself does not interpret escapes in Content.

---

## 9. Canonicalization and Round-Trip (Normative)

Inline markup MUST be losslessly round-trippable.

* Tools MUST preserve original Content text exactly when round-tripping
* Tools MUST NOT silently rewrite author text without explicit user action
* Normalized or derived forms MAY be provided for editing or rendering purposes only

---

## 10. Rendering Semantics (Normative)

This contract does not mandate a specific render target.

Renderers that interpret inline markup MUST treat:

* `bold`, `italic`, `strikethrough`, `underline`, `overline` as style intents
* alias-based styles as target-specific style hooks

A renderer MAY ignore any or all style intents, but MUST do so deterministically.

---

## 11. Resource References in Content (Normative)

A **Resource** is data.
It is not a link.

A Resource becomes a link or other affordance only when interpreted by a renderer.

### 11.1 Reference Form

```text
{#<resourceId>}
{#<resourceId>: label}
```

Rules:

* `<resourceId>` MUST be a full identifier
* The first `:` after the identifier is the label delimiter
* A single optional space after the delimiter is permitted
* The label MAY contain nested inline markup

Examples:

```text
See {#resource:joe}.
See {#resource:joe: Joe’s site}.
See {#resource:joe: {italic: Joe’s site}}.
```

---

### 11.2 Resource Definition

Resource Concepts are declared in Codex data according to schema.
This contract defines only the Content reference syntax.

---

### 11.3 Rendering Requirements

Renderers that support resource references MUST:

* resolve the referenced Resource by identifier
* emit an appropriate target-specific affordance
* use an explicit label if provided, otherwise a schema-provided label if available

Resolution failures MUST be reported at the renderer or tooling layer.

---

## 12. Non-Goals

This contract does **not**:

* define rich-text editor behavior
* define typographic properties
* define hyperlinks as presentation primitives
* define horizontal rules or separators

These concerns belong to ViewModel and Design Policy.

---

## 13. Summary

* Inline text markup is a Content sub-language
* Codex treats Content as opaque text
* Interpretation occurs outside the Codex language
* Brace spans are explicit and nestable
* Canonical built-ins are unshadowable
* Shortcuts may be shadowed by aliases
* Unknown kinds are literal text
* Resources are data; links are render-time affordances
