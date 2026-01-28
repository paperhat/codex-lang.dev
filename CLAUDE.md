# Codex Language — Reference for AI Assistants

## Critical: No Conventions Without Approval

Codex exists to eliminate ambiguity and ensure one canonical implementation. Standard specification conventions (RFC 2119 keywords, precedence clauses, optional features, etc.) often introduce the very ambiguity Codex rejects.

**Do not apply conventional patterns automatically.** Question every inherited practice. Check with the user before introducing any standard spec-writing convention. If uncertain whether something is conventional, ask.

The goal: any two conforming implementations produce byte-identical output for the same input. Every specification choice must serve that goal.

## Specification Principles

- **No may**: Only must and must not. Optional features create implementation variance. This applies at all levels — if a schema could let instance authors choose (e.g., `$MayBeEntity`), that's still optionality. Binary declarations only, no defaults.
- **No redundancy**: Each requirement stated exactly once. Use references, not restatements.
- **No conflict clauses**: The spec has no conflicts. If you find one, it's a defect to fix, not resolve via precedence.
- **Round-trippability**: Core invariant. Applies to *canonical* form, not raw input. Canonicalization (like `gofmt`) normalizes first.
- **Ordering**: Structural ordering has no semantic meaning *to Codex*. Schemas can define semantic ordering for specific constructs. Implementations preserve ordering for both round-trippability and schema-defined constraints.
- **Content vs children mode**: Determined mechanically by first non-indentation character: `<` or `[` = children mode, anything else = content mode. Escapes `\<` and `\[` allow content starting with those characters.
- **Reference implementation scope**: Canonicalization → parsing → validation → triple serialization → triple reconstruction. All five stages required for conformance.
- **Bootstrap schema**: Hardcoded into implementations, not loaded at runtime (avoids circularity). Files in `bootstrap-schema/` are for human readability only.

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
- **Entity** — Schema declares `$MustBeEntity` (must have `id`) or `$MustNotBeEntity` (must not). No default, no `$MayBeEntity`.

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
| `spec/1.0.0/bootstrap-schema/schema.cdx` | **Profile B bootstrap** — Schema-of-schemas as SHACL triples. Validates schema documents. |
| `spec/1.0.0/bootstrap-schema/expanded/schema.cdx` | **Profile A bootstrap** — Human-readable equivalent of the above. |
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

## Established Specification Decisions (§1–§5)

Do not regress these:

- **§1.3**: Only MUST and MUST NOT are normative keywords. MAY is not defined — do not use it.
- **§4.1**: Names are ASCII letters and digits only. Names must be non-empty. PascalCase starts uppercase, camelCase starts lowercase.
- **§4.2**: No 3+ consecutive uppercase letters. This mechanically enforces acronym treatment (e.g., `ASTNode` rejected because A-S-T-N = 4 consecutive).
- **§4.3**: Authors must treat acronyms as single words. Not fully mechanically enforceable (e.g., `iOStream` vs `ioStream` — only 2 consecutive, so not rejected by §4.2).
- **§5.1**: Empty strings permitted (zero or more Unicode scalar values).
- **§5.4**: No infinity/NaN. `-0` preserved distinct from `0`. No leading zeros in integer components (sign not part of integer component). Precision suffix (`p`) only on decimals, not integers.
- **§5.5**: Enumerated tokens use `$` sigil + PascalCase token name.
- **§5.6**: Two grammars — Temporal Value (complete braced literal) and Temporal Body (content within braces).
- **§5.7**: Canonical form requires lowercase for hex digits, color function names, and color space tokens. Named colors use `&` sigil + lowercase letters only (Appendix B).
- **§5.8**: UUID canonical form uses lowercase hex digits.
- **§5.10**: Lookup tokens use `~` sigil + camelCase token name.
- **§5.13–§5.14**: Set and Map duplicates are errors (not silent removal). Canonical ordering preserves source order.
- **§5.13.1**: Value equality is over parsed values. Hex digits, color function names, and color space tokens compared case-insensitively for Colors; hex digits case-insensitive for UUIDs.
