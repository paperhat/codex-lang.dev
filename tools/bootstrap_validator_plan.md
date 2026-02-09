Status: DRAFT
Owner: Codex tools
Spec target: Codex 1.0.0

# Bootstrap Schema Validator Plan

## Language Choice
Python 3 (standard library only). Rationale: existing tooling is Python, fast iteration, no external dependency risk in this repo.

## Goals
- Spec-aware validation of the bootstrap schemas:
  - `spec/1.0.0/bootstrap-schema/schema.cdx`
  - `spec/1.0.0/bootstrap-schema/simplified/schema.cdx`
- Prove consistency with Codex 1.0.0 rules in §11, not just token presence.
- Provide a deterministic, reproducible test harness with negative and positive cases.

## Non-Goals
- Full general-purpose Codex implementation for all user schemas.
- Full RDF projection pipeline or SHACL engine.
- Performance tuning beyond what is needed for the bootstrap corpus.

## Proposed Layout
- `tools/bootstrap_validator/`
- `tools/bootstrap_validator/__init__.py`
- `tools/bootstrap_validator/cli.py`
- `tools/bootstrap_validator/lexer.py`
- `tools/bootstrap_validator/parser.py`
- `tools/bootstrap_validator/ast.py`
- `tools/bootstrap_validator/values.py`
- `tools/bootstrap_validator/canonicalize.py`
- `tools/bootstrap_validator/schema_rules.py`
- `tools/bootstrap_validator/simplified_expand.py`
- `tools/bootstrap_validator/fuzz.py`
- `tools/bootstrap_validator/testdata/`
- `tools/bootstrap_validator/tests.py`

## Spec Coverage Map
We will explicitly link spec sections to code modules:
- Surface form parsing: §5, Appendix A (EBNF/PEG) -> `lexer.py`, `parser.py`
- Text normalization and canonicalization rules: §5.1, §10.5.2 -> `values.py`, `canonicalize.py`
- Schema rules: §11 + relevant invariants in §2 -> `schema_rules.py`
- Simplified-mode expansion: §11.6–§11.7 and related mapping -> `simplified_expand.py`

## Data Model
- `ast.py` defines:
  - `Document`, `Concept`, `Trait`, `Value` variants
  - `TextValue`, `BooleanValue`, `NumericValue`, `EnumeratedTokenValue`, `CharValue`, `BacktickTextValue`, `ListValue`, `MapValue`, `TupleValue`, `RecordValue`
  - `SourceSpan` for precise error reporting
- `values.py` implements:
  - escape interpretation for Text and Char
  - whitespace normalization for Text
  - numeric literal classification

## Parsing
- `lexer.py`: whitespace, identifiers, symbols, literals, backtick blocks
- `parser.py`: recursive descent driven by Appendix A
  - Parse is schema-free.
  - Output AST with exact source spans.
  - Preserve ordering for round-trip relevance.

## Canonicalization
- `canonicalize.py` implements Phase 1 canonicalization for schema docs:
  - text formatting per §10.5.2 with 100-column rule (tabs=2)
  - trait ordering, layout rules, whitespace normalization
  - no schema-directed changes in Phase 1

## Schema Validation (Spec-Aware)
- `schema_rules.py` encodes §11 constraints as explicit checks:
  - Required concepts and traits for schema documents
  - Value type constraints for each schema construct
  - Trait uniqueness, naming rules, and value kind constraints
  - Cross-references (e.g., trait names used by `Trait` declarations)
  - Enforcement of schema-first architecture
- Return structured errors:
  - `SurfaceFormError`, `SchemaError`, `FormattingError` as defined by §14

## Simplified Mode Expansion
- `simplified_expand.py` converts simplified schemas into canonical form:
  - deterministic generation of IR nodes and triples
  - strict mapping rules per spec
- Validate that:
  - simplified expands to canonical form
  - canonical form validates against bootstrap schema

## Test Strategy
- `tests.py`:
  - Validate both bootstrap schemas.
  - Assert consistent behavior with conformance fixtures when applicable.
  - Add targeted tests for edge cases:
    - Text escaping (`\"`, `\\`, `\uXXXX`, `\u{...}`) and canonicalization choices.
    - Backtick block wrapping behavior.
    - Value type constraints and list/map/record/tuple/union checks.
- `fuzz.py`:
  - Generate spec-valid schemas.
  - Generate systematic mutations for each §11 rule (missing traits, invalid tokens).
  - Compare spec validator results vs bootstrap schema validation results.

## CLI
- `cli.py`:
  - `validate-bootstrap` command:
    - validates canonical and simplified bootstrap schema files
    - outputs summary + detailed errors
  - `fuzz-bootstrap` command:
    - runs property-based tests with deterministic seed
    - outputs failing cases to `tools/bootstrap_validator/testdata/`

## Deliverables
1. Spec-aware parser + validator that validates both bootstrap schema files.
2. Simplified-mode expansion and equivalence checks.
3. Deterministic test harness and reports.

## Milestones
1. Parser + Text normalization + canonicalization (Phase 1).
2. Schema rules engine for §11 (bootstrap canonical schema acceptance).
3. Simplified-mode expansion + equivalence checks.
4. Fuzz + regression harness.
