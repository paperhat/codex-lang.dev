# Codex Inline Text Markup Contract (DRAFT)

## Status

- **DRAFT**
- Normative once locked
- Applies to any Codex tooling that interprets **Content** as styled text
- This contract defines a **Content sub-language**, not Codex Concepts/Traits/Markers

---

## 1. Purpose

This contract defines a **target-agnostic inline text markup language** that MAY appear inside Codex **Content**.

Its goals are to:

- provide visible, explicit, editor-friendly inline styling without a rich-text editor
- avoid HTML / XML / Markdown conventions and failure modes
- keep Codex Concepts hygienic by confining presentation markup to Content
- support deterministic parsing and lossless round-tripping
- allow rendering to many targets (DOM, HTML, PDF, voice, etc.) without naming target technologies

This contract governs **inline styling markup inside Content strings** only.

---

## 2. Relationship to Codex

- Codex **does not parse** inline markup.
- Codex treats Content as **opaque**.
- Inline text markup is interpreted **only** by tools that opt into this contract.

A `.cdx` file may be valid Codex even if a renderer chooses to reject invalid inline markup.
Tooling MUST report inline markup errors distinctly from Codex parse/surface/schema errors.

---

## 3. Inline Markup Form

Inline markup uses **brace spans**:

```
{kind: text}
```

A brace span applies a style (or class) to the **span content** (`text`).

- `kind` is a single token (see §4)
- The first `:` following `kind` is the delimiter
- A single optional space after `:` is permitted and ignored

Both forms are equivalent:

- `{b: bold}`
- `{b:bold}`

Brace spans MAY span multiple lines.

Brace spans MUST be properly nested (§6).

---

## 4. Built-in Kinds (Normative)

Inline markup defines a small, closed set of built-in kinds.

### 4.1 Canonical Built-in Kinds (Unshadowable)

The following kind names are **canonical** and MUST NOT be shadowed by aliases (§5):

- `bold`
- `italic`
- `strikethrough`
- `underline`
- `overline`
- `class`

These canonical names MUST always have their built-in meaning.

### 4.2 Shortcut Built-in Kinds (Shadowable)

The following shortcuts are provided for convenience and MAY be shadowed by aliases (§5):

- `b` (default meaning: `bold`)
- `i` (default meaning: `italic`)
- `s` (default meaning: `strikethrough`)
- `u` (default meaning: `underline`)
- `o` (default meaning: `overline`)

Shortcuts exist to reduce authoring friction, not to define semantics.

---

## 5. Style Aliases (Normative)

Inline markup supports declaring **aliases** to reusable style identifiers.

An alias maps a short name to a style identifier string:

```
{style: hs = header-style}
```

### 5.1 Alias Declaration Form

- Alias declarations use the directive form:

  ```
  {style: <alias> = <styleIdentifier>}
  ```

- Alias declarations MUST appear at the beginning of the Content value, before any non-directive text.

- `<alias>` MUST be a single token.

- `<styleIdentifier>` is an opaque identifier string (not interpreted by this contract).

### 5.2 Alias Resolution

- After declaration, `{hs: ...}` is equivalent in intent to applying the mapped style identifier to the span content.
- Aliases MAY shadow shortcut built-ins (`b`, `i`, `s`, `u`, `o`).
- Aliases MUST NOT shadow canonical built-ins (`bold`, `italic`, `strikethrough`, `underline`, `overline`, `class`).

### 5.3 Shadowing Policy (Normative)

If an alias uses a name that matches a shortcut built-in:

- the alias takes precedence for that shortcut name
- the canonical built-in remains available under its canonical name

Example:

```
{style: b = brand-emphasis}
Then: {b: This uses brand-emphasis.}
But: {bold: This always means bold.}
```

---

## 6. Nesting and Overlap Rules (Normative)

Brace spans MUST be **properly nested**.

- Nesting is permitted:

  ```
  {bold: This is {italic: very} important.}
  ```

- Overlap is forbidden (and impossible to represent without closing markers).

Any input that cannot be parsed as properly nested brace spans is invalid under this contract.

---

## 7. Unrecognized Kinds (Normative)

If a brace span uses a `kind` that is not:

- a built-in kind, or
- a declared alias

then it is treated as **plain text**, not markup.

Example:

```
{Tom: this is what I think!}
```

This is literal text and MUST NOT be interpreted as markup.

This rule prevents accidental markup and supports editorial brace usage.

---

## 8. Escaping (Normative)

To include literal braces inside a recognized brace span, escaping is permitted:

- `\{` for literal `{`
- `\}` for literal `}`
- `\\` for literal `\`

Escaping is only meaningful to tools that interpret inline markup.
Codex itself does not interpret escapes in Content.

---

## 9. Canonicalization and Round-Trip (Normative)

Inline markup MUST be losslessly round-trippable.

- Tools MUST preserve the original Content text exactly when round-tripping CDX → store → CDX.
- Tools MAY additionally provide a normalized form for editing or rendering, but MUST NOT silently rewrite author text without explicit user action.

---

## 10. Rendering Semantics (Normative)

This contract does not mandate a specific render target.

However, all renderers that interpret inline markup MUST treat:

- `bold`, `italic`, `strikethrough`, `underline`, `overline` as style intents
- alias-based styles as target-specific style hooks

A renderer MAY ignore any or all style intents, but MUST do so deterministically.

---

## 11. Resource References in Content (Normative)

A **Resource** is data. It is not a link.

A Resource becomes a link (or other target-specific affordance) only when it is referenced from Content and interpreted by a renderer.

### 11.1 Reference Form

Content MAY reference a Resource by identifier using the following inline form:

```
{#<resourceId>}
```

or with an explicit label override:

```
{#<resourceId>: label}
```

Rules:

- `<resourceId>` MUST be a full identifier (e.g. `resource:joe`, `https://example.com/resource/joe`, etc.)
- The first `:` after the id is treated as the label delimiter (if present)
- A single optional space after the delimiter is permitted and ignored
- The label, if present, is opaque text and MAY contain nested inline markup

Examples:

```
See {#resource:joe}.
See {#resource:joe: Joe’s site}.
See {#resource:joe: {italic: Joe’s site}}.
```

### 11.2 Resource Definition

Resource Concepts are declared in Codex data according to schema (out of scope for this contract).

This contract does not define the Resource schema shape, only the Content reference syntax.

### 11.3 Rendering Requirements

Renderers that support resource references MUST:

- resolve the referenced Resource by identifier
- render an appropriate affordance for the target (HTML link, PDF reference, spoken reference, etc.)
- use the explicit label if provided; otherwise use a schema-provided label if available

If resolution fails, tools MUST report an error in the appropriate layer (renderer/tooling), distinct from Codex parse/surface/schema errors.

---

## 12. Non-Goals

This contract does **not**:

- define rich-text editor behaviors
- define typographic properties (fonts, sizes, colors)
- define hyperlinks as presentation primitives
- define horizontal rule or separator primitives (these belong to ViewModel and/or DesignPolicy)

---

## 13. Summary

- Inline text markup is a Content sub-language, not Codex markup
- It uses explicit brace spans: `{kind: text}`
- Proper nesting is required; overlap is forbidden
- Built-ins are minimal; aliases enable reusable styles
- Canonical built-ins are unshadowable; shortcuts may be shadowed
- Unknown kinds are treated as literal text
- Resources are data and become links only when referenced from Content via `{#<resourceId> ... }`
- Horizontal rules/separators are not Content primitives and belong to ViewModel/DesignPolicy
