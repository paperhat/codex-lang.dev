# Codex Authoring Gotchas (DRAFT)

## Status

- **DRAFT**
- Informative
- Applies to humans and LLMs authoring Codex (`.cdx`) files

---

## Purpose

This document lists **common mistakes** made when authoring Codex and explains **why they are invalid**.

Its goals are to:

- reduce frustration during authoring
- prevent repeated validation errors
- reinforce correct mental models
- clarify intent without reintroducing theory

This document introduces **no new rules**.

---

## 1. “Why can’t I add an `id` here?”

Because **identity is intentional**.

- Only Concepts authorized by schema may be Entities.
- Many Concepts (e.g. `Step`, `Description`, `Data`) are **not things** — they are structure or values.
- Giving everything an `id` pollutes the graph and breaks reasoning.

**Rule of thumb:**
If it doesn’t make sense to refer to it independently, it probably must not have an `id`.

---

## 2. “Why does this parse but fail validation?”

Parsing checks **syntax**.
Validation checks **meaning**.

A file can parse correctly but still be invalid because:

- a Trait is not allowed on that Concept
- a required Trait is missing
- a reference points to a non-Entity
- a Concept is used outside its valid context

This is expected and intentional.

---

## 3. “Why can’t I invent a new Concept or Trait?”

Because Codex separates **authoring** from **modeling**.

- Authors use Concepts and Traits
- Schemas define Concepts and Traits

Allowing ad hoc invention would:

- break determinism
- break validation
- make tools disagree about meaning

If something is not documented by a schema, it is not valid Codex.

---

## 4. “Why doesn’t Codex understand my prose?”

Because prose is **Content**, not schema-defined data.

- Content expresses human meaning
- Content is not used for inference
- Content does not implicitly create entities, traits, or constraints

If the system needs to reason about something, it must be expressed as **Concepts or Traits**, not as prose.

---

## 5. “But I _can_ do things inside text — what’s going on?”

Because Content supports **Gloss**.

Inside Content, Codex recognizes **Gloss language constructs**.

Gloss allows authors to:

- add semantic emphasis
- reference declared entities or resources
- annotate meaning inline

However:

- Gloss is **not styling**
- Gloss does **not** create new Concepts or Traits
- Gloss does **not** affect validity unless explicitly defined to do so by schema

Gloss enriches meaning inside Content without turning prose into structure.

---

## 6. “Why didn’t my inline thing affect layout or appearance?”

Because **Gloss is not presentation**.

- Gloss expresses _what something is_
- Design Policy decides _how it appears_
- Renderers decide _how that policy manifests per target_

If you are trying to force layout, spacing, decoration, or visual effects from inside text, you are using the wrong layer.

---

## 7. “Why did my comment disappear from the output?”

Because **annotations are not always rendered**.

Codex supports **annotations**, not code-style comments:

- Editorial annotations (`[ ... ]`) are for authors and tooling
- Output annotations (`<Annotation>`) are for intentional downstream visibility

By default:

- `[ ... ]` annotations are preserved for round-tripping but **ignored by HTML, PDF, or voice renderers**
- `<Annotation>` Concepts may be rendered or spoken, depending on the target

If you want something to appear in rendered output, use an explicit `<Annotation>` Concept.

---

## 8. “Why didn’t this `[ ... ]` annotation show up where I expected?”

Because editorial annotations:

- attach to the **next Concept**, not the previous one
- are **not inline text**
- are ignored inside Content

They behave like **editorial margin notes**, not inline markup.

If you need precise attachment or inline semantics, use Gloss.
If you need visible output, use `<Annotation>`.

---

## 9. “Why didn’t Codex recognize my annotation type?”

Because annotation kinds are **enumerated**.

In an editorial annotation:

```
[todo: verify cooking time]
```

The prefix (`todo`) is treated as a kind **only if it is recognized by schema**.

If the prefix is not recognized:

```
[bob says: this sucks]
```

The entire annotation is treated as plain text, not as a typed annotation.

This avoids accidental or ambiguous typing.

---

## 10. “Why can’t I rely on order here?”

Because **ordering is explicit**.

- Some collections are ordered (e.g. `Steps`)
- Some are unordered (e.g. `Ingredients`)
- Schema decides which is which

Never encode order using:

- numbers in prose
- implicit conventions
- identifiers

If order matters, the schema will say so.

---

## 11. “Why does formatting matter so much?”

Because Codex is **canonical**.

- There is exactly one valid surface form
- Formatting is mechanical, not stylistic
- Canonical form enables round-tripping and stable tooling

If formatting is wrong, the document is invalid — even if the meaning seems obvious.

---

## 12. “Why won’t Codex ‘just fix it’?”

Because silent correction destroys trust.

- Codex tools do not guess
- Codex tools do not auto-correct
- Codex tools do not infer intent

Every change must be explicit and visible.

---

## 13. “Why is Codex so strict?”

Because strictness is what makes everything else possible:

- deterministic compilation
- stable querying
- multiple render targets
- safe automation
- correct LLM assistance

Relaxed rules here would create chaos downstream.

---

## Summary

- Codex is strict by design
- Identity, meaning, and structure are intentional
- Schemas own semantics; authors provide facts
- Content carries human meaning, not inferred data
- Gloss enriches meaning inline without becoming presentation
- Annotations are preserved but selectively rendered
- Canonical form is non-negotiable

If Codex rejects something, it is protecting the system — not being pedantic.
