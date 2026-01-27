# Codex Language — Reference for AI Assistants

## What Codex Is

Codex is a declarative semantic markup language that serves as the storage/serialization format for the Paperhat Workshop Semantic Authoring System. It is backed by RDF, OWL2, SHACL, and SPARQL.

**Primary use**: Storing ontologies and instance data in a triple store. Users typically interact through auto-generated forms, not raw Codex.

**Secondary uses**: Configuration, templating.

**Design goal**: Highly restrictive to constrain LLM output — closed-world semantics, canonical forms, and deterministic validation make it easy to validate and reject invalid LLM-generated content.

## Core Primitives

- **Concept** — Named structural unit (PascalCase). May contain child Concepts OR Content, not both.
- **Trait** — Name-value pair on a Concept (camelCase). Schema-authorized.
- **Value** — Literal datum (strings, numbers, booleans, IRIs, UUIDs, colors, temporals, collections, etc.). Parsed, never evaluated.
- **Content** — Opaque narrative text. Preserved without interpretation.
- **Entity** — A Concept with an `id` Trait. Entity eligibility is schema-controlled.

## Two-Layer Architecture

### Layer A (Profile A) — Human-Readable Schema Authoring
Uses Codex-native concepts: `ConceptDefinition`, `TraitDefinition`, `EnumeratedValueSet`, constraints, etc.

### Layer B (Profile B) — RDF/SHACL Representation
Uses `RdfGraph` containing `RdfTriple` elements (subject/predicate/object). Full SHACL-SPARQL power.

**Relationship**: Profile A expands deterministically to Profile B. They are semantically equivalent; A is for humans, B is the canonical machine form.

## RDF Instance Graph Mapping (§9.7)

Every Codex document maps deterministically to an RDF graph:
- Each Concept instance → RDF node with skolem IRI (no blank nodes)
- Traits → RDF triples
- Parent/child relationships → dedicated predicates
- Validation via SHACL shapes derived from schema

## Key Invariants

- **Closed-world**: Meaning must be explicitly declared. No inference from omission.
- **Deterministic**: Same inputs → identical outputs. No heuristics.
- **Canonical**: Every valid document has exactly one surface form.
- **Schema-first**: Well-formedness (syntax) is schema-free; validity (semantics) requires a governing schema.

## File Locations

| Path | Purpose |
|------|---------|
| `spec/1.0.0/index.md` | **Normative specification** (~5000 lines). All requirements defined here. |
| `spec/1.0.0/bootstrap-schema/index.cdx` | **Profile B bootstrap** — Schema-of-schemas as SHACL triples. Validates schema documents. |
| `spec/1.0.0/bootstrap-schema/expanded/index.cdx` | **Profile A bootstrap** — Human-readable equivalent of the above. |
| `conformance/1.0.0/` | Conformance test suite (valid/invalid cases, expected outputs). |
| `notes/index.md` | Informative documentation on value types. |

## Specification Structure (index.md)

- §1-2: Front matter, language invariants
- §3: Core model (Concept, Trait, Value, Content, Entity)
- §4: Naming rules (PascalCase/camelCase)
- §5: Value literal catalog (all value types)
- §6: Identity (IRIs, `id` Trait)
- §7: Reference Traits (`reference`, `target`, `for`)
- §8: Surface form (encoding, markers, indentation, content)
- §9: **Schema-first architecture** — Profiles, Layer B (`RdfGraph`/`RdfTriple`), instance graph mapping, SHACL projection
- §10: Formatting and canonicalization
- §11: Schema definition language
- §12: Schema bootstrapping
- §13: Schema versioning
- §14: Error classification
- Appendix A: EBNF (normative) and PEG (informative) grammars
- Appendix B: Named colors

## For Implementation Work

- Read the spec section relevant to your task
- The bootstrap schemas are the authoritative examples of valid Codex
- Profile A (`expanded/index.cdx`) is easier to read than Profile B
- Conformance tests show expected parsing/canonicalization behavior
- All validation ultimately goes through SHACL — understand §9.7 (instance graph mapping) and §9.6 (Layer B) for validation work
