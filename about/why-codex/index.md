# Why Codex Exists

**Codex** is a **declarative semantic language** for expressing **meaning,
structure, and intent** without embedding behavior, presentation, or execution.

Codex exists because existing systems conflate:

- data and logic
- structure and presentation
- identity and layout
- content and behavior

That conflation makes systems fragile, opaque, and difficult to repurpose.

Codex separates these concerns deliberately and permanently.

**This is what Codex looks like.**  
No programming code. No styling. No behavior.  
Just data expressed in **declarative, semantic markup**, with meaning made explicit.

Inline meaning inside prose is added using [**Gloss**](https://gloss-lang.dev/about/why-gloss/), without breaking the text.

**This is the entire `.cdx` file. No other code required.**

```cdx
<Article id="article:bread:intro" title="Making Bread at Home">
  <Author id="person:smith" name="Jane Smith" />

  <Paragraph>
    Bread has been made for {#duration:millennia | thousands of years},
    but many people find the process {#intimidating}.
  </Paragraph>

  <Paragraph>
    This recipe uses only {#count:ingredients | four ingredients}:
    flour, water, salt, and yeast.
  </Paragraph>

  <Ingredient id="ingredient:flour" name="Flour">
    <Quantity id="qty:flour" value=500 unit="gram" />
  </Ingredient>

  <Ingredient id="ingredient:water" name="Water">
    <Quantity id="qty:water" value=325 unit="milliliter" />
  </Ingredient>

  <Step id="step:mix">
    <Instruction>
      Mix the ingredients until the dough is {#texture:smooth}.
    </Instruction>
  </Step>

  <Note>
    The dough should feel {#soft} but not {#sticky}.
  </Note>
</Article>
```

Codex expresses:

* **structure** (`Article`, `Paragraph`, `Ingredient`, `Step`)
* **identity** (`id` values)
* **semantic data** (`Quantity`, `Duration`)
* **inline meaning** (`{#intimidating}`, `{#soft}`) via Gloss

No layout. No logic. No presentation.  
Only meaning.

> Codex: the earliest form of book, replacing the scrolls and wax tablets of earlier times. [Dictionary.com](https://www.dictionary.com/browse/codex)

---

## The Problem Codex Solves

Most modern systems express meaning indirectly:

- HTML pretends structure is semantics
- JSON and YAML pretend data shape is meaning
- frameworks embed behavior into configuration
- schemas validate form, not intent

As a result:

- meaning is implicit
- semantics are guessed
- reuse is brittle
- non-web targets are second-class
- correctness depends on convention

Codex was designed to make **meaning explicit**.

---

## What Codex Is

Codex is:

- **Declarative** — no logic, no execution, no control flow
- **Semantic** — Concepts and Traits have defined meaning
- **Structured** — hierarchy and collections are explicit
- **Identity-aware** — Entities are first-class
- **Target-independent** — not tied to the web, HTML, or UI
- **Ontology-aligned** — integrates cleanly with schema.org and RDF

Codex expresses **what is**, not **what happens**.

---

## What Codex Is Not

Codex is **not**:

- a programming language
- a template language
- a UI framework
- a CMS
- a database schema
- a runtime configuration format

Codex is an **authoring and semantic modeling language**, not an execution
environment.

---

## A Simple Example

### What we want to express

> A recipe has ingredients, quantities, and units.

### Typical JSON

```json
{
  "ingredients": [
    { "name": "Flour", "amount": "2 cups" }
  ]
}
```

Problems:

* `"2 cups"` is a string
* units are implicit
* no identity
* no semantic validation
* meaning is inferred by convention

---

### Codex

```cdx
<Recipe id="recipe:bread">
  <Ingredient id="ingredient:flour" name="Flour">
    <Quantity value=2 unit="cup" />
  </Ingredient>
</Recipe>
```

What Codex makes explicit:

* `Recipe`, `Ingredient`, and `Quantity` are Concepts
* units are semantic, not textual
* identity is explicit
* meaning is inspectable
* validation is semantic, not structural

No guessing. No magic strings.

---

## Structure Without Behavior

Codex defines:

* documents
* modules
* collections
* relationships
* constraints

Codex does **not** define:

* control flow
* event handling
* rendering
* side effects
* application logic

Those belong to other layers.

This separation keeps Codex stable and predictable.

---

## Codex and the Paperhat System

Codex sits at the **semantic center** of Paperhat:

* **Architect** defines vocabularies and schemas
* **Kernel** compiles and preserves meaning
* **Gloss** binds meaning inline in prose
* **Design Policy** determines presentation
* **Renderers** produce target-specific output

Codex is the **single source of semantic truth**.

---

## Why This Matters

When meaning is explicit:

* systems become explainable
* accessibility improves automatically
* multiple targets are first-class
* content survives redesigns
* data outlives frameworks
* AI systems can reason safely

Codex is designed for **longevity**, not trends.

---

## The Core Principle

> **Everything is data.**
> **Everything has meaning.**
> **Nothing is guessed.**

That is what Codex enforces.

---

## Summary

* Codex defines meaning and structure
* It separates semantics from behavior
* It is target-independent by design
* It enables systems like Gloss to exist cleanly
* It replaces ad-hoc conventions with explicit intent

Codex is not flashy.

It is foundational.

That is the point.
