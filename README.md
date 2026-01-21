# Codex

**Codex** is a declarative semantic markup language for expressing structured meaning independent of runtime, presentation, or target platform.

---

## Core Constructs

Codex documents are built from four primitives:

### Concept

A **Concept** is the primary unit of structure. Concepts have names, may declare Traits, and may contain child Concepts or Content.

```cdx
<Recipe id=recipe:pasta title="Spaghetti Carbonara">
	<Ingredients>
		<Ingredient name="pasta" amount=400 unit=$Grams />
		<Ingredient name="eggs" amount=4 />
	</Ingredients>
</Recipe>
```

Concepts are not elements, components, tags, or nodes.

### Trait

A **Trait** binds a name to a Value. Traits are declared inline on Concepts and are schema-authorized.

```cdx
<Person id=person:alice name="Alice" age=30 active=true />
```

Traits are not properties, attributes, fields, or parameters.

### Value

A **Value** is a literal datum. Codex supports:

- Strings, characters, backtick strings
- Booleans (`true`, `false`)
- Numbers (integers, decimals, scientific, fractions, complex)
- Enumerated tokens (`$Draft`, `$Published`)
- Lists, sets, maps, tuples
- Temporal values, colors, UUIDs, ranges
- IRI references, lookup tokens

Values are parsed but not evaluated. Typing is a schema responsibility.

### Content

**Content** is opaque narrative text. Codex preserves it without interpretation.

```cdx
<Description>
	This recipe makes a classic Roman pasta dish.
	The key is using fresh eggs and quality guanciale.
</Description>
```

Content is distinct from Values. Schemas determine what Content may contain.

---

## Entities and Identity

An **Entity** is a Concept with stable identity that can be referenced by other Concepts.

Entity eligibility is **schema-controlled**:

- `$MustBeEntity` — the Concept MUST declare an `id`
- `$MayBeEntity` — the Concept MAY declare an `id`
- `$MustNotBeEntity` — the Concept MUST NOT declare an `id`

```cdx
<Book id=book:1984 title="1984" author=person:orwell />
```

This prevents identity proliferation. Schemas deliberately restrict which Concepts may be Entities to maintain low semantic density. Adding `id` to a Concept where the schema forbids it is a validation error.

---

## Annotations

**Annotations** are editorial metadata preserved through the pipeline. They attach to the next Concept and do not affect validation.

```cdx
[Review: verify cooking times]
<Recipe id=recipe:risotto>
```

Annotations are not comments.

---

## Key Characteristics

- **Declarative**: Codex expresses what, not how
- **Schema-driven**: Meaning is defined by schema, not inferred
- **Closed-world**: Validation is deterministic; everything is explicit
- **Canonical**: Every valid document has exactly one surface form
- **No evaluation**: Values are parsed, not computed

---

## Specification

The authoritative specification is in [`spec/0.1/`](spec/0.1/).

| Document | Scope |
|----------|-------|
| [Language](spec/0.1/language/) | Conceptual model and terminology |
| [Surface Form](spec/0.1/surface-form/) | Syntax and structure |
| [Naming and Values](spec/0.1/naming-and-values/) | Vocabulary and literal forms |
| [Grammar (EBNF)](spec/0.1/grammar/ebnf/) | Normative formal grammar |
| [Grammar (PEG)](spec/0.1/grammar/peg/) | Informative parsing grammar |
| [Formatting](spec/0.1/formatting-and-canonicalization/) | Canonicalization rules |
| [Schema Definition](spec/0.1/schema-definition/) | Schema authoring |
| [Identifiers](spec/0.1/identifiers/) | Identity rules |
| [Reference Traits](spec/0.1/reference-traits/) | Reference semantics |
| [Validation Errors](spec/0.1/validation-errors/) | Error taxonomy |

---

## Readiness (Repo Gate)

This repo treats “production ready for implementation” as a **repeatable gate**:

```bash
python3 tools/readiness_check.py
```

See [READINESS.md](READINESS.md) and [AI_CONVENTIONS.md](AI_CONVENTIONS.md).

---

## Governance

Codex is maintained under editorial governance. Normative content is authoritative. Changes to locked documents are versioned.

See [`GOVERNANCE.md`](GOVERNANCE.md).

---

## License

Documentation is licensed under [CC BY 4.0](LICENSE.md).

See [`COPYRIGHT.md`](COPYRIGHT.md) for details.

---

*This repository is a reference specification, not a tutorial or community forum.*
