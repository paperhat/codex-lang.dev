
# Codex 0.1 Consolidation Notes (Working)

Goal: reorganize Codex 0.1 so that **every normative requirement is stated exactly once**, in **one** authoritative document.

This file proposes the **information hierarchy** and a **source-to-target mapping** from the current multi-document spec.

Status: WORKING / NON-NORMATIVE

---

## A. Proposed Single-Document Hierarchy

Working title for the unified document:

`spec/0.1/codex-language-specification.md`

### A.1 Front Matter

1. Status, version, editor, lock state
2. Scope and non-goals (what Codex defines / does not define)
3. Normativity and precedence rules
	 - Define “Normative” vs “Informative”
	 - Define precedence order for resolving conflicts inside this one document

### A.2 Language Invariants (Global)

1. Declarative / closed-world model
2. Determinism + explainability
3. Separation of responsibility (language vs schema vs storage/rendering)
4. Target agnosticism

### A.3 Core Model (Terms)

Define exactly once:

1. Concept
2. Trait
3. Value
4. Content
5. Entity (and how `id` + schema `entityEligibility` define it)
6. Marker
7. Annotation

### A.4 Naming Rules

1. Concept name casing (PascalCase)
2. Trait name casing (camelCase)
3. Acronym/initialism capitalization rule
4. General abbreviation prohibition + schema-scoped exception rule

### A.5 Value Literal Catalog (Syntax + Structural Rules)

This section is the single home for:

1. Primitive literals: string, backtick string, char, boolean
2. Numeric literals (incl. Infinity, fraction, imaginary/complex, precision-significant `p`)
3. Enumerated tokens `$Token`
4. Temporal values `{...}`
5. Color values
6. UUID values
7. IRI reference values
8. Lookup tokens `~token` + lookup resolution contract (if retained as “language-level surface token”; otherwise move to “consuming systems”)
9. Composite values: list, set, map, tuple, range
	 - Include structural constraints (e.g., map key uniqueness, set uniqueness semantics)

### A.6 Identity

1. `id` trait defines identifiers
2. Identifiers are IRIs
3. IRI surface profile restrictions (no unicode whitespace/control/bidi/private-use)
4. Identifier immutability + prohibited uses
5. Opaqueness / normalization rules

### A.7 Reference Traits

1. Exactly three reference traits: `reference`, `target`, `for`
2. Semantic intent of each
3. Default singleton rule + schema-authorized exceptions
4. What values they accept (IRI reference or lookup token)
5. “for references concept types via ConceptDefinition entity” rule

### A.8 Surface Form (Concrete `.cdx` Text)

1. File encoding + BOM rules
2. Line endings rules
3. Indentation rules (tabs-only canonical)
4. Blank line rules in children mode
5. Concept marker forms
	 - Opening / closing / self-closing
	 - “empty block <X></X> is invalid”
6. Trait surface syntax
	 - `name=value` and whitespace constraints
	 - Value termination and delimiter balancing
	 - Canonical trait layout rule (1–2 inline; 3+ multiline)
7. Content blocks
	 - Schema-directed content vs children mode
	 - Content escaping rules (what must be escaped, what escapes exist)
	 - Content indentation normalization semantics
8. Annotations
	 - Inline vs block syntax
	 - Attachment rules and ambiguity rules
	 - Grouping annotations (`GROUP:`/`END:`)
	 - Canonicalization + directives (`FLOW:`/`CODE:`/`MD:`)

### A.9 Schema-First Architecture

1. Schema-directed dispatch requirement (concept body interpretation is schema-driven)
2. What can be done schema-less (well-formedness + formatting only)
3. What cannot be done without schema (semantic validation)

### A.10 Formatting + Canonicalization Pipeline

1. Required processing phases (schema-less canonicalization first)
2. Canonical form requirement (“exactly one canonical textual form”)
3. Canonicalization allowed vs forbidden transformations
4. What constitutes canonicalization failure

### A.11 Schema Definition Language (Schema-as-Codex)

1. Schema document structure (`Schema` root concept, required traits)
2. Concept definitions
	 - `ConceptDefinition` structure + `ContentRules` + `TraitRules` + `ChildRules` + `CollectionRules`
3. Trait definitions (`TraitDefinition`, `AllowedValues`)
4. Value types
	 - Built-in value type tokens
	 - Optional `ValueTypeDefinition`
5. Enumerated value sets
	 - Schema-defined and built-in enumerations
6. Constraint model
	 - Targets, rule algebra, paths/quantifiers, atomic constraints
7. Relationship to external derivations (SHACL/OWL are derived, not authoritative)

### A.12 Schema Loading + Bootstrapping

1. Schema provision mechanisms (explicit required, registry optional)
2. Resolution order
3. Bootstrap schema-of-schemas requirement
	 - “root Schema uses bootstrap if no explicit schema”
	 - Error classification boundary for schema docs

### A.13 Schema Versioning

1. Required schema identity + explicit version
2. Monotonic ordering requirement
3. Compatibility classes and their semantics
4. Breaking vs non-breaking change classification
5. Tooling responsibilities

### A.14 Validation Errors (Taxonomy)

1. Closed set of primary error classes
2. Definitions + classification guidance
3. Fatality rule (no warnings)
4. Reporting expectations

### A.15 Formal Grammar (Appendix)

1. Normative EBNF grammar as the single syntactic definition
2. (Optionally) informative PEG for implementers, but only if it is made consistent with the normative syntax and with the surface-form rules.

---

## B. Consolidation Decisions (So There’s Only One Source of Truth)

These are the decisions implied by the hierarchy above.

1. **One authoritative document** contains all normative rules; anything else becomes either:
	 - an appendix extracted from the authoritative doc, or
	 - an informative implementation note, or
	 - deleted.

2. **EBNF is the sole normative syntax**.
	 - If PEG is kept, it is explicitly informative and must not contradict EBNF or surface-form rules.

3. **Exactly one home per rule**:
	 - Syntax spelling rules live under Surface Form / Value Catalog / EBNF appendix.
	 - Processing obligations live under Formatting + Canonicalization Pipeline.
	 - Error-class rules live under Validation Errors.
	 - Schema-language ontology lives under Schema Definition Language.

4. **Resolve the known conflict** (required):
	 - PEG currently claims “no escaping is required/recognized in content”, which contradicts Surface Form + EBNF content escaping.
	 - Outcome for consolidation: Surface Form + EBNF rule wins; PEG must be corrected or removed.

---

## C. Source-to-Target Mapping (Current Files → Unified Sections)

This mapping is intended to support a mechanical rewrite later.

### Entry and scope

- Current: [codex-lang.dev/spec/0.1/index.md](codex-lang.dev/spec/0.1/index.md)
	- Move to: A.1 Front Matter (scope/non-goals, authority/precedence, “entry point” language)

- Current: [codex-lang.dev/spec/0.1/FROZEN.md](codex-lang.dev/spec/0.1/FROZEN.md)
	- Move to: A.1 Front Matter as informative status note OR move out of 0.1 normative set entirely.

### Language invariants

- Current: [codex-lang.dev/spec/0.1/language/index.md](codex-lang.dev/spec/0.1/language/index.md)
	- Move to: A.2 Language Invariants; A.9 Schema-First Architecture (only the architectural bits)

### Core vocabulary, naming, values

- Current: [codex-lang.dev/spec/0.1/naming-and-values/index.md](codex-lang.dev/spec/0.1/naming-and-values/index.md)
	- Move to: A.3 Core Model; A.4 Naming Rules; A.5 Value Literal Catalog

### Identity

- Current: [codex-lang.dev/spec/0.1/identifiers/index.md](codex-lang.dev/spec/0.1/identifiers/index.md)
	- Move to: A.6 Identity

### Reference traits

- Current: [codex-lang.dev/spec/0.1/reference-traits/index.md](codex-lang.dev/spec/0.1/reference-traits/index.md)
	- Move to: A.7 Reference Traits

### Surface form

- Current: [codex-lang.dev/spec/0.1/surface-form/index.md](codex-lang.dev/spec/0.1/surface-form/index.md)
	- Move to: A.8 Surface Form

### Formatting/canonicalization

- Current: [codex-lang.dev/spec/0.1/formatting-and-canonicalization/index.md](codex-lang.dev/spec/0.1/formatting-and-canonicalization/index.md)
	- Move to: A.10 Formatting + Canonicalization Pipeline

### Formal grammar

- Current: [codex-lang.dev/spec/0.1/grammar/index.md](codex-lang.dev/spec/0.1/grammar/index.md)
	- Move to: A.1 (precedence rules) + A.15 (appendix intro)

- Current: [codex-lang.dev/spec/0.1/grammar/ebnf/index.md](codex-lang.dev/spec/0.1/grammar/ebnf/index.md)
	- Move to: A.15 Formal Grammar (Appendix) as the normative grammar

- Current: [codex-lang.dev/spec/0.1/grammar/peg/index.md](codex-lang.dev/spec/0.1/grammar/peg/index.md)
	- Move to: A.15 Formal Grammar (Appendix) as informative ONLY, after conflict fix; otherwise drop.

### Schema: definition, loading, versioning

- Current: [codex-lang.dev/spec/0.1/schema-definition/index.md](codex-lang.dev/spec/0.1/schema-definition/index.md)
	- Move to: A.11 Schema Definition Language

- Current: [codex-lang.dev/spec/0.1/schema-loading/index.md](codex-lang.dev/spec/0.1/schema-loading/index.md)
	- Move to: A.12 Schema Loading + Bootstrapping

- Current: [codex-lang.dev/spec/0.1/schema-loading/bootstrap-schema-of-schemas/index.md](codex-lang.dev/spec/0.1/schema-loading/bootstrap-schema-of-schemas/index.md)
	- Move to: A.12 Schema Loading + Bootstrapping

- Current: [codex-lang.dev/spec/0.1/schema-versioning/index.md](codex-lang.dev/spec/0.1/schema-versioning/index.md)
	- Move to: A.13 Schema Versioning

### Errors

- Current: [codex-lang.dev/spec/0.1/validation-errors/index.md](codex-lang.dev/spec/0.1/validation-errors/index.md)
	- Move to: A.14 Validation Errors

---

## D. Next Step (Discussion Prompt)

If this hierarchy looks right, the next mechanical step is:

1. Create `spec/0.1/codex-language-specification.md` with these headings.
2. Move content into it once, deleting duplicates.
3. Decide what to do with PEG (fix and keep as informative vs remove).

