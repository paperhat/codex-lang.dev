# Codex Language — AI Reference

## Critical: No Conventions Without Approval

Codex eliminates ambiguity for byte-identical output across implementations. Standard spec conventions (RFC 2119, precedence clauses, optional features) introduce the ambiguity Codex rejects.

**Do not apply conventional patterns automatically.** Ask before introducing any standard spec-writing convention.

## Specification Principles

- **No MAY**: Only MUST/MUST NOT. No optionality at any level.
- **No redundancy**: Each requirement stated once. Use references.
- **No conflict clauses**: Conflicts are defects to fix, not resolve via precedence.
- **Round-trippability**: Applies to canonical form. Canonicalization normalizes first.
- **Ordering**: No semantic meaning to Codex; preserved for round-trippability.
- **Content vs children**: First non-indentation char `<` or `[` = children mode; else content mode.
- **Bootstrap schema**: Hardcoded, not loaded at runtime.

## What Codex Is

Declarative semantic markup for the Paperhat Workshop system, backed by RDF/OWL2/SHACL/SPARQL. Primary use: ontologies and instance data in triple stores. Design goal: constrain LLM output via closed-world semantics and deterministic validation.

## Core Primitives

- **Concept**: Named unit (PascalCase). Children XOR Content.
- **Trait**: Name-value pair (camelCase). Schema-authorized.
- **Value**: Literal datum. Parsed, never evaluated.
- **Content**: Opaque text. Preserved without interpretation.
- **Entity**: `$MustBeEntity` or `$MustNotBeEntity`. No default.

## Two-Layer Architecture

**Layer A** (human-readable): `ConceptDefinition`, `TraitDefinition`, etc.
**Layer B** (machine): `RdfGraph`/`RdfTriple`, SHACL-SPARQL.
A expands deterministically to B.

## Key Invariants

- **Closed-world**: No inference from omission.
- **Deterministic**: Same inputs → identical outputs.
- **Canonical**: One surface form per valid document.
- **Schema-first**: Well-formedness is schema-free; validity requires schema.

## File Locations

| Path | Purpose |
|------|---------|
| `spec/1.0.0/index.md` | Normative specification |
| `spec/1.0.0/bootstrap-schema/schema.cdx` | Profile B bootstrap (SHACL) |
| `spec/1.0.0/bootstrap-schema/expanded/schema.cdx` | Profile A bootstrap (human-readable) |
| `conformance/1.0.0/` | Conformance test suite |

## Specification Structure

§1-2: Front matter, invariants · §3: Core model · §4: Naming (PascalCase/camelCase) · §5: Value literals · §6: Identity · §7: Reference Traits · §8: Surface form · §9: Schema architecture, Layer B, SHACL · §10: Canonicalization · §11: Schema definition · §12: Bootstrapping · §13: Versioning · §14: Errors · Appendix A: Grammars · Appendix B: Named colors

## Established Decisions (§1–§8)

Do not regress:

- **§1.3**: Only MUST/MUST NOT. MAY undefined.
- **§4.1**: Names: ASCII letters/digits, non-empty. PascalCase uppercase-first, camelCase lowercase-first.
- **§4.2**: No 3+ consecutive uppercase (mechanically enforces acronym-as-word).
- **§4.3**: Authors must treat acronyms as words (not fully mechanical).
- **§5.1**: Empty strings permitted.
- **§5.4**: No infinity/NaN. `-0` distinct from `0`. No leading zeros (sign excluded). Precision `p` on any numeric (inferred from decimal places; explicit overrides).
- **§5.5**: Enumerated tokens: `$` + PascalCase.
- **§5.6**: Two grammars: Temporal Value (braced literal) vs Temporal Body (content).
- **§5.7**: Lowercase canonical: hex digits, function names, color space tokens. Named colors: `&` + lowercase (Appendix B).
- **§5.8**: UUID: lowercase hex canonical.
- **§5.10**: Lookup tokens: `~` + camelCase.
- **§5.11**: Character literal delimiter: single quote (`'`).
- **§5.13**: Value equality over parsed values. Case-insensitive: hex/function names/color space tokens (Colors), hex (UUIDs).
- **§5.14–15**: Set/Map duplicates are errors. Canonical order = source order.
- **§6.1**: Two identity mechanisms: `id` (IRI, global scope) and `key` (Lookup Token, document scope).
- **§6.2**: Entity MUST have exactly one `id`; non-Entity MUST NOT have `id`. Values unique within document.
- **§6.3**: Concept has zero or one `key`. Resolution via §9.8 bindings.
- **§7.1**: Exactly three reference traits: `reference`, `target`, `for`. Values: IRI or Lookup Token. MUST NOT imply dereferencing/loading/execution/transformation.
- **§7.2–4**: Intent statements are non-normative guidance for schema authors.
- **§7.5**: Singleton rule via `ReferenceConstraint(type=ReferenceSingleton)`.
- **§8.1–2**: UTF-8 default (no BOM); UTF-16 requires BOM. LF canonical; CRLF normalized; bare CR error; trailing LF required.
- **§8.3**: Tabs only (U+0009) for indentation. Spaces in indentation = error.
- **§8.5–6**: Empty block `<X></X>` is error; use self-closing. No whitespace around `=`. 1–2 traits inline; 3+ multiline with `>` or `/>` on own line.
- **§8.8**: Content is opaque. Escaping: `\<` and `\[` (line-initial only). Indentation stripped (schema-free). `whitespaceMode`: `$Preformatted` (preserve) or `$Flow` (collapse, wrap 100 chars) — schema-directed.
- **§8.9**: Three annotation kinds: attached, grouping, general. Block directives: `FLOW:`, `CODE:`, `MARKDOWN:`.
- **§10.5**: Two-phase canonicalization: Phase 1 (schema-free) for encoding/indentation/layout; Phase 2 (schema-directed) for content whitespace mode.
