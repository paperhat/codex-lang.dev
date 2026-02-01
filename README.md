# Codex Semantic Markup Language

**Codex** is a declarative semantic markup language for expressing structured meaning with **deterministic, schema-driven validation**.

Codex is designed as a standards-style language: its specification is authoritative, normative, and intended to support multiple independent conforming implementations.

---

## Design Goals

Codex prioritizes the following principles:

- **Determinism**  
  Given the same inputs, all conforming implementations must produce identical results.

- **Closed-world semantics**  
  Nothing is inferred from omission. All meaning must be explicit and schema-authorized.

- **Schema authority**  
  Validity is defined solely by the governing schema, not by convention, heuristic, or implementation behavior.

- **Canonical representation**  
  Every valid document has exactly one canonical representation as defined by the specification.

- **Round-trippability**  
  Documents can be transformed to RDF and reconstructed without loss of meaning.

---

## Core Constructs

Codex documents are composed of four fundamental primitives.

### Concept

A **Concept** is a named structural unit.  
Concepts may declare Traits and contain either child Concepts or Content, but never both.

```cdx
<Recipe id=recipe:carbonara title="Spaghetti Carbonara">
	<Ingredients>
		<Ingredient name="guanciale" amount=150 unit=$Grams />
		<Ingredient name="eggs" amount=4 />
	</Ingredients>
</Recipe>
```

---

### Trait

A **Trait** is a name–value binding declared on a Concept.
All Traits are schema-authorized.

```cdx
<Person id=person:alice name="Alice" age=30 active=true />
```

---

### Value

A **Value** is a literal datum.
Values are parsed but never evaluated.

Codex supports, among others:

* text values
* booleans and numbers
* enumerated tokens
* temporal values
* colors
* UUIDs
* collections (lists, sets, maps, records, tuples)
* ranges
* IRI references
* lookup tokens

---

### Content

**Content** is opaque narrative text.
It is preserved verbatim and not interpreted semantically.

```cdx
<Description>
	A classic Roman pasta dish. The key is fresh eggs and quality guanciale.
</Description>
```

---

## Entity and Identity

An **Entity** is a Concept with stable, referenceable identity.

Entity eligibility is controlled explicitly by schema:

* `$MustBeEntity` — the Concept must declare an `id` trait
* `$MustNotBeEntity` — the Concept must not declare an `id` trait

There is no default behavior.
Schemas must explicitly declare whether identity is permitted or required.

---

## Annotations

Annotations are **non-semantic metadata** that attach to Concepts.

Annotations are preserved through processing but do not affect validation or semantic interpretation.

```cdx
[TODO: verify ingredient quantities]
<Recipe id=recipe:risotto title="Mushroom Risotto">
```

---

## Status

This repository contains the **authoritative Codex Language Specification**.

Documents marked **NORMATIVE** define binding language rules.
Documents marked **LOCKED** are stable and safe to rely upon for implementation and tooling.

The specification is complete and intended for implementation.

---

## Governance

Codex documentation is maintained under explicit editorial governance.

Document authority, lock states, and change control rules are defined in
[GOVERNANCE.md](GOVERNANCE.md).

---

## License

All content in this repository is licensed under the
**Apache License, Version 2.0**.

See:

* [LICENSE](LICENSE)
* [COPYRIGHT.md](COPYRIGHT.md)
* [TRADEMARK.md](TRADEMARK.md)

---

*This repository is a reference specification. It does not provide tutorials, tooling, or implementation guidance.*
