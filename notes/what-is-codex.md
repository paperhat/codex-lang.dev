# What Codex Is and What Makes It Different

## What Codex Is

Codex is a declarative semantic markup language designed for the Paperhat system. It defines structured data -- ontologies and instance data -- that maps losslessly to RDF/OWL2/SHACL/SPARQL triple stores. Documents are written in `.cdx` files using a clean, XML-like surface form built around five core primitives:

- **Concepts**: named structural units (PascalCase). A Concept instance is in exactly one of two body modes: children mode (zero or more child Concepts) or content mode (opaque narrative text).
- **Traits**: name-value pairs declared on Concepts (camelCase). Trait meaning and permissibility are defined by the governing schema.
- **Values**: a rich catalog of literal data types, parsed mechanically and never evaluated.
- **Content**: opaque narrative text carried by a Concept, preserved through processing.
- **Entities**: Concept instances with explicit identity, determined by the governing schema's `entityEligibility` rule.

A Codex document looks like this:

```cdx
<Book
	id=urn:isbn:978-0-618-26030-2
	title="The Hobbit, or There and Back Again"
	author="John Ronald Reuel Tolkien"
/>
```

Schemas govern what Concepts, Traits, and structures are valid. The language separates well-formedness (schema-free syntactic checks) from validity (schema-driven semantic checks), and provides a full schema definition language with constraints, rule algebra, paths, and quantifiers.

---

## What Makes Codex Different

### 1. Absolute Determinism

Most data languages tolerate ambiguity. JSON allows duplicate keys with implementation-defined behavior. XML parsers vary in whitespace handling. YAML's type coercion is notoriously unpredictable. Codex rejects all of this.

Given the same inputs, every conforming implementation must produce identical results -- parsing, validation, canonicalization, everything. No heuristic behavior is permitted. When information is missing or ambiguous, the system must fail with an error rather than guess.

**Why this matters.** Two independent implementations processing the same document will always agree. This eliminates an entire class of interoperability bugs and makes the language trustworthy for mission-critical data.

### 2. Single Canonical Form

Codex mandates that every valid document normalizes to exactly one canonical textual form -- similar to `gofmt` for Go, but elevated to a language invariant. Tabs for indentation, alphabetical trait ordering, deterministic line wrapping, specific blank-line rules -- all specified precisely. There is no room for style preferences.

**Why this matters.** Diff, merge, and version-control operations become meaningful at the byte level. Teams never argue about formatting. Machine-generated and human-written documents are indistinguishable in form.

### 3. Byte-Identical Round-Trippability Through Triple Stores

A canonicalized Codex document can be transformed to RDF triples, stored in a triple store, retrieved via SPARQL, and reconstructed into a byte-identical canonical document. No sidecar files. No metadata loss. Annotations, ordering, structural details -- everything survives the round trip.

**Why this matters.** Codex documents can live in semantic web infrastructure (triple stores, SPARQL endpoints) without any lossy serialization penalty. The `.cdx` file is a faithful, deterministic projection of the graph, and vice versa.

### 4. Only MUST and MUST NOT

Most specifications use RFC 2119 keywords including MAY, SHOULD, and SHOULD NOT, creating a spectrum of optional behaviors that fragment implementations. Codex uses only MUST and MUST NOT. There is no "you may do this" or "you should consider that." Every requirement is binary.

**Why this matters.** Conformance is unambiguous. An implementation either satisfies every requirement or it doesn't. This makes conformance testing tractable and eliminates the gray areas that plague interoperability in other formats.

### 5. Closed-World Semantics

Codex is closed-world: what is not explicitly declared is not present. Implementations must not infer meaning from omission, shape, or other non-specified cues. Defaults exist only where the specification or governing schema explicitly defines them.

**Why this matters.** When a schema says a Concept must have certain Traits, the absence of a Trait is a violation, not a default. When a Concept is not authorized by the schema, it is forbidden. There is no open-world assumption that unmentioned things might be valid.

### 6. Schema-First Architecture with a Self-Hosting Bootstrap

Codex is schema-first: semantic validation requires an explicit governing schema, and that schema must be provided as a direct input -- never inferred or substituted. The entry point is explicit:

```
validate(documentBytes, governingSchema, importedSchemas, documentBaseIri)
```

The schema-of-schemas (bootstrap schema) is built into every conforming implementation as immutable data, making the schema definition language self-hosting without circular dependency.

**Why this matters.** Schema provision is explicit and auditable. You always know exactly what rules govern a document. The bootstrap eliminates the "who validates the validator" problem.

### 7. Conflicts Are Defects, Not Features

Most specifications include conflict-resolution clauses ("in case of conflict between section X and section Y, section X prevails"). Codex declares that conflicts are defects to be reported, not resolved. If an implementer discovers an apparent conflict, they must report it -- not guess which rule wins.

**Why this matters.** This forces the specification itself to be internally consistent and unambiguous, which transitively makes every implementation more reliable.

### 8. Rich Value Type System

Codex defines a remarkably complete set of built-in value types:

- **Numeric**: nine standalone types -- Integer, DecimalNumber, ExponentialNumber, PrecisionNumber, Fraction, ImaginaryNumber, ComplexNumber, PositiveInfinity, NegativeInfinity. Each determined by lexical form at parse time.
- **Temporal**: PlainDate, PlainTime, PlainDateTime, PlainYearMonth, PlainMonthDay, YearWeek, Instant, ZonedDateTime, Duration, and TemporalKeyword.
- **Color**: hex, named (&-prefixed), rgb, hsl, hwb, lab, lch, oklab, oklch, color-mix, device-cmyk, relative colors, and color-space colors. Semantic validation is specified down to 256-bit precision arithmetic with mandated dot-product procedures.
- **Identity and reference**: IRI Reference Values, Lookup Token Values, UUIDs.
- **Text and character**: Text Values (with whitespace normalization), Backtick Text, Character Values.
- **Structured**: host names, email addresses, URLs (with deterministic resolution and canonicalization).
- **Collections**: Lists, Sets (no duplicates), Maps (no duplicate keys), Records (named fields), Tuples (positional), Ranges (inclusive endpoints, never enumerated).
- **Parameterized types**: `$List<$Text>`, `$Map<$Text, $Integer>`, `$Tuple<$Text, $Integer, $Boolean>`, and so on, with arbitrary nesting depth.
- **Other**: Boolean (`true`/`false` only), Enumerated Tokens (`$`-prefixed PascalCase).

**Why this matters.** Schema authors do not need to reinvent value validation. The language natively understands the difference between a fraction and a decimal, between a zoned datetime and a plain date, between an OKLab color and an HSL color. This precision eliminates the coercion bugs that plague loosely-typed formats.

### 9. Deterministic Projection to SHACL/SPARQL

The simplified authoring mode expands deterministically into RDF/SHACL. Every derived IRI, every SPARQL variable name, every constraint shape is computed by a single deterministic algorithm with explicit formulas. Two implementations expanding the same schema must produce byte-identical SHACL output.

**Why this matters.** The validation layer is not a black box. It is a pure function from schema to SHACL, making it auditable, testable, and reproducible.

### 10. Designed for AI Constraint

Codex's design goal is to constrain LLM output via closed-world semantics and deterministic validation. In a world where AI generates increasingly complex structured data, Codex provides a format where a schema can mechanically verify that generated output is exactly correct -- not approximately, not probably, but provably.

**Why this matters.** As AI systems produce more structured output, the gap between "looks right" and "is right" becomes critical. Codex closes that gap with mechanical precision. A Codex schema is a contract: if the document validates, it conforms. No wiggle room. No interpretation.

---

## Summary

Codex occupies a unique position in the landscape of data languages. Where JSON and YAML optimize for human convenience, and RDF/OWL optimize for semantic expressiveness, Codex optimizes for verifiable determinism. It is the only data language that simultaneously guarantees:

1. Byte-identical output across all conforming implementations
2. Byte-identical round-tripping through triple stores
3. A single canonical surface form with no formatting ambiguity
4. A closed-world, schema-first validation model with no optionality
5. A specification written exclusively in MUST/MUST NOT with no conflict-resolution clauses

These properties make it well-suited for scenarios where trust, reproducibility, and mechanical verification matter more than flexibility -- exactly the scenarios that arise when AI systems need to produce structured, validated output at scale.
