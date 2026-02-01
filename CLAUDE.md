# Codex Language — AI Reference

## Specification Lock

**The specification (`spec/1.0.0/index.md`) is LOCKED.** Do not edit the specification without explicit permission from the human. This includes adding, removing, or modifying any normative requirements, examples, or appendices.

**"Editing" includes any change to the specification text**, regardless of intent. The following all require explicit permission:

- Rewording for "clarity" or "readability"
- Restructuring sections or paragraphs
- Adding explanatory text or examples
- Fixing perceived inconsistencies or ambiguities
- Correcting what appears to be an error
- Improving formatting or style

If something in the specification appears unclear, inconsistent, or wrong, **report it rather than fix it**. The specification's exact wording is deliberate.

## Critical: No Conventions Without Approval

Codex eliminates ambiguity for byte-identical output across implementations. Standard spec conventions (RFC 2119, precedence clauses, optional features) introduce the ambiguity Codex rejects.

**Do not apply conventional patterns automatically.** Ask before introducing any standard spec-writing convention.

## Specification Principles

- **No `may`**: Only `must`/`must not`. No optionality at any level.
- **No redundancy**: Each requirement stated once. Use references.
- **No conflict clauses**: Conflicts are defects to fix, not resolve via precedence.
- **Round-trippability**: Applies to canonical form. Canonicalization normalizes first.
- **Ordering**: No semantic meaning to Codex; preserved for round-trippability.
- **Content vs children**: First non-indentation character `<` or `[` = children mode; else content mode.
- **Bootstrap schema**: Hardcoded, not loaded at runtime.

## What Codex Is

Declarative semantic markup for the Paperhat Workshop system, backed by RDF/OWL2/SHACL/SPARQL. Primary use: ontologies and instance data in triple stores. Design goal: constrain LLM output via closed-world semantics and deterministic validation.

## Core Primitives

- **Concept**: Named unit (PascalCase). Children XOR Content.
- **Trait**: Name-value pair (camelCase). Schema-authorized.
- **Value**: Literal datum. Parsed, never evaluated.
- **Content**: Opaque text. Preserved without interpretation.
- **Entity**: `$MustBeEntity` or `$MustNotBeEntity`. No default.

## Authoring Modes and Canonical Representation

- **Canonical Representation** (semantic authority): RDF 1.1 graph (optionally expressed as SHACL / SHACL-SPARQL).
- **Canonical Authoring Mode**: the author writes the Canonical Representation directly via `RdfGraph`/`RdfTriple`.
- **Simplified Authoring Mode**: the author writes Codex-native schema-definition concepts; this is an authoring surface only and expands deterministically and losslessly into the Canonical Representation.

## Key Invariants

- **Closed-world**: No inference from omission.
- **Deterministic**: Same inputs → identical outputs.
- **Canonical**: One surface form per valid document.
- **Schema-first**: Well-formedness is schema-free; validity requires schema.

## File Locations

| Path | Purpose |
|------|---------|
| `spec/1.0.0/index.md` | Normative specification |
| `spec/1.0.0/bootstrap-schema/schema.cdx` | Canonical Authoring Mode bootstrap (SHACL) |
| `spec/1.0.0/bootstrap-schema/simplified/schema.cdx` | Simplified Authoring Mode bootstrap (human-readable) |
| `conformance/1.0.0/` | Conformance test suite |

## Specification Structure

§1-2: Front matter, invariants · §3: Core model · §4: Naming (PascalCase/camelCase) · §5: Value literals · §6: Identity · §7: Reference Traits · §8: Surface form · §9: Schema architecture, Canonical Representation, SHACL · §10: Canonicalization · §11: Schema definition · §12: Bootstrapping · §13: Versioning · §14: Errors · Appendix A: Grammars · Appendix B: Named colors

## Established Decisions (§1–§14)

Do not regress:

- **§1.3**: Only must/must not. may undefined.
- **§1.3.1**: Conflicts are defects to report, not resolve via precedence.
- **§2.2**: Determinism: no heuristics.
- **§4.1**: Names: ASCII letters/digits, non-empty. PascalCase uppercase-first, camelCase lowercase-first.
- **§4.2**: No 3+ consecutive uppercase (mechanically enforces acronym-as-word).
- **§4.3**: Authors must treat acronyms as words (not fully mechanical).
- **§5.1**: Empty text values permitted.
- **§5.3**: Boolean is exactly `true` or `false`. No other spellings.
- **§5.4**: No NaN. `Infinity`/`-Infinity` permitted; `+Infinity` not permitted. `-0` distinct from `0`. No leading zeros (sign excluded). Precision `p` on any numeric (inferred from decimal places; explicit overrides).
- **§5.5**: Enumerated tokens: `$` + PascalCase.
- **§5.6**: Two grammars: Temporal Value (braced literal) vs Temporal Body (content).
- **§5.7**: Lowercase canonical: hex digits, function names, color space tokens. Named colors: `&` + lowercase (Appendix B).
- **§5.8**: UUID: lowercase hex canonical.
- **§5.9**: IRI must contain `:`. No whitespace/control/bidi/private-use characters. Compared as opaque sequences of Unicode scalar values. Never dereferenced.
- **§5.10**: Lookup tokens: `~` + camelCase.
- **§5.11**: Character literal delimiter: single quote (`'`).
- **§5.13**: Value equality over parsed values. Case-insensitive: hex/function names/color space tokens (Colors), hex (UUIDs).
- **§5.14–15**: Set/Map duplicates are errors. Canonical order = source order.
- **§5.16**: Tuple must have ≥1 element.
- **§5.17**: Range endpoints inclusive. Ranges never enumerated.
- **§6.1**: Two identity mechanisms: `id` (IRI, global scope) and `key` (Lookup Token, document scope).
- **§6.2.1**: Tools MUST NOT synthesize `id` or `key` traits.
- **§6.2.2**: Entity must have exactly one `id`; non-Entity must not have `id`. Values unique within document.
- **§6.2.3**: `id` stability: changing `id` = creating new Entity.
- **§6.3**: Concept has zero or one `key`. Resolution via §9.8 bindings.
- **§7.1**: Exactly three reference traits: `reference`, `target`, `for`. Values: IRI or Lookup Token. must not imply dereferencing/loading/execution/transformation.
- **§7.2–4**: Intent statements are non-normative guidance for schema authors.
- **§7.5**: Singleton rule via `ReferenceConstraint(type=ReferenceSingleton)`.
- **§8.1–2**: UTF-8 default (no BOM); UTF-16 requires BOM. LF canonical; CRLF normalized; bare CR error; trailing LF required.
- **§8.3**: Tabs only (U+0009) for indentation. Spaces in indentation = error.
- **§8.4**: No leading blank line. No consecutive blanks outside content/annotations. One blank between siblings. No blank at start/end of children block.
- **§8.5–6**: Empty block `<X></X>` is error; use self-closing. No whitespace around `=`. 1–2 traits inline; 3+ multiline with `>` or `/>` on own line.
- **§8.7**: No Value type inference. No Value type coercion.
- **§8.8**: Content is opaque. Escaping: `\<` anywhere; `\[` line-initial only. Indentation stripped (schema-free). `whitespaceMode`: `$Preformatted` (preserve) or `$Flow` (collapse, wrap 100 characters) — schema-directed.
- **§8.9**: Three annotation kinds: attached, grouping, general. Block directives: `FLOW:`, `CODE:`, `MARKDOWN:`.
- **§8.9.7**: GROUP/END must match via stack-based nesting.
- **§9.1**: External inputs (environment, config, registries, network, clocks, randomness) MUST NOT influence processing.
- **§9.4**: Exactly one authoring mode per schema (`$SimplifiedMode` or `$CanonicalMode`). No mixing.
- **§9.6**: Canonical Representation: no RDF blank nodes. All RDF nodes MUST be IRIs. Deterministic skolem IRIs.
- **§9.7**: Instance graph `nodeIri` MUST NOT derive from `id` trait. Declared `id` stored via `codex:declaredId`.
- **§9.8**: Lookup bindings MUST NOT be inferred, synthesized, or imported implicitly.
- **§9.10**: Fail with error rather than guess when required info is missing or ambiguous.
- **§10.5**: Two-phase canonicalization: Phase 1 (schema-free) for encoding/indentation/layout; Phase 2 (schema-directed) for content whitespace mode.
- **§10.5.1**: `$Unordered` collection sort: Concept name → `id` → `key` → source order.
- **§11.2**: Schemas are declarative data, not executable. All authorization explicit.
- **§11.4.3–4**: Default closed-world: traits/children not explicitly allowed/required are forbidden.
- **§11.6.4**: Built-in enumerated sets (`ConceptKind`, `EntityEligibility`, `CompatibilityClass`, `Ordering`, `Cardinality`) MUST NOT be redefined.
- **§11.7**: Constraints MUST NOT execute code or depend on implicit inference.
- **§11.12**: Derived representations MUST NOT introduce semantics beyond spec/schema. MUST NOT override/weaken Codex validation.
- **§12.2**: Governing schema must be explicit. MUST NOT substitute, infer, or override.
- **§12.3**: Bootstrap schema-of-schemas: built-in, immutable. Root `Schema` = schema document. Not substitutable for instance docs.
- **§13.3**: `id`, `version`, `versionScheme` all required on root `Schema`.
- **§13.4.1**: Four version schemes: `$Semver`, `$DateYYYYMM`, `$DateYYYYMMDD`, `$Lexical`.
- **§13.5**: Four compatibility classes: `$Initial`, `$BackwardCompatible`, `$ForwardCompatible`, `$Breaking`. First version MUST use `$Initial`.
- **§13.8**: Validation strictly per declared version. MUST NOT infer, substitute, or relax.
- **§14.3**: Closed set of 9 error classes. No additional classes. Halt at first failure.
- **§14.5**: Errors are not warnings. No best-effort recovery.
