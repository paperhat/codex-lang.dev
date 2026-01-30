# Codex Semantic Markup Language

**Codex** is a declarative semantic markup language designed for expressing structured meaning with deterministic, schema-driven validation.

## Design Goals

Codex prioritizes:

- **Determinism**: Given the same inputs, all conforming implementations produce identical outputs.
- **Closed-world semantics**: Nothing is inferred from omission. All meaning is explicit.
- **Schema authority**: Validity is defined by schema, not convention or heuristic.
- **Canonical form**: Every valid document has exactly one surface representation.
- **Round-trippability**: Documents survive transformation to RDF and back without loss.

## Core Constructs

Codex documents are composed of four primitives:

**Concept** — A named structural unit. Concepts declare Traits and contain either child Concepts or Content, never both.

```cdx
<Recipe id=recipe:carbonara title="Spaghetti Carbonara">
	<Ingredients>
		<Ingredient name="guanciale" amount=150 unit=$Grams />
		<Ingredient name="eggs" amount=4 />
	</Ingredients>
</Recipe>
```

**Trait** — A name-value binding declared on a Concept. Traits are schema-authorized.

```cdx
<Person id=person:alice name="Alice" age=30 active=true />
```

**Value** — A literal datum. Values are parsed, never evaluated. Codex supports strings, booleans, numbers, enumerated tokens, temporal values, colors, UUIDs, collections (lists, sets, maps, records, tuples), ranges, IRI references, and lookup tokens.

**Content** — Opaque narrative text preserved without interpretation.

```cdx
<Description>
	A classic Roman pasta dish. The key is fresh eggs and quality guanciale.
</Description>
```

## Entity and Identity

An **Entity** is a Concept with stable, referenceable identity. Entity eligibility is schema-controlled:

- `$MustBeEntity` — the Concept must declare an `id` trait
- `$MustNotBeEntity` — the Concept must not declare an `id` trait

There is no default. Schemas explicitly declare which Concepts may carry identity.

## Annotations

Annotations are editorial metadata that attach to Concepts. They are preserved through processing but do not affect validation.

```cdx
[TODO: verify ingredient quantities]
<Recipe id=recipe:risotto title="Mushroom Risotto">
```

## Status

This repository contains the Codex language specification. The specification is currently under development and not yet ready for implementation.

## Governance

Codex documentation is maintained under editorial governance. Normative documents are authoritative and versioned.

See [GOVERNANCE.md](GOVERNANCE.md) for document authority, lock states, and change control.

## License

Documentation is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE.md).

See [COPYRIGHT.md](COPYRIGHT.md) for copyright and trademark information.

---

*This repository is a reference specification, not a tutorial or implementation guide.*
