# Bootstrap Schema Review Plan (Spec 1.0.0)

## Purpose
Produce three artifacts without editing normative sources:
1. Requirement-to-schema traceability matrix.
2. Spec-vs-schema mismatch report.
3. Change recommendation set (proposed fixes only; no direct edits).

## Ground Rules (locked)
- Normative source of truth: `specifications/codex-lang.dev/spec/1.0.0/index.md`.
- Informative implementation artifact under review: `specifications/codex-lang.dev/spec/1.0.0/bootstrap-schema/schema.cdx`.
- If conflict appears, default assumption is schema is wrong until proven otherwise.
- No edits to `index.md` or `schema.cdx` during this process.
- Any potential "spec bug" is recorded as an explicit discussion item, not resolved unilaterally.

## Artifacts to produce
- `specifications/codex-lang.dev/spec/1.0.0/review/01-requirement-matrix.csv`
- `specifications/codex-lang.dev/spec/1.0.0/review/02-mismatch-report.md`
- `specifications/codex-lang.dev/spec/1.0.0/review/03-change-recommendations.md`
- Working notes (checkpoints): `specifications/codex-lang.dev/spec/1.0.0/review/00-review-log.md`

## Matrix schema (CSV columns)
- `req_id`
- `spec_section`
- `spec_lines`
- `normative_text_summary`
- `normative_keyword` (MUST/SHOULD/MAY/REQUIRED/implicit-deterministic)
- `representable_in_bootstrap_schema` (yes/no/partial)
- `schema_group`
- `schema_lines`
- `coverage_status` (covered/partial/missing/extra-schema)
- `evidence`
- `severity` (P0/P1/P2/P3)
- `notes`

## Deterministic batching strategy
### Pass A: spec extraction (forward)
- A1: Sections 1-4 (front matter, invariants, model, naming)
- A2: Section 5 (value literals)
- A3: Sections 6-8 (identity, references, surface form)
- A4: Section 9 (schema-first architecture)
- A5: Sections 10-12 (semantics, context, constraints)
- A6: Sections 13-14 + Appendix A normative portions
- A7: Informative-only filtering and normalization

### Pass B: schema inventory (reverse)
- B1: bootstrap preamble and top-level `Schema` traits
- B2: `[GROUP]` blocks 1-20
- B3: `[GROUP]` blocks 21-40
- B4: `[GROUP]` blocks 41-60
- B5: `[GROUP]` blocks 61-80
- B6: global consistency checks (references, closure, cardinalities)

### Pass C: reconciliation
- C1: complete forward mapping (spec -> schema)
- C2: complete reverse mapping (schema -> spec)
- C3: classify mismatches and severity
- C4: draft recommendations with minimal-risk patch intent

## Severity rubric
- P0: determinism/conformance break; valid docs rejected or invalid docs accepted in core behavior.
- P1: normative rule missing or contradicted, likely interoperability issue.
- P2: narrower/wider constraints than spec with bounded impact.
- P3: editorial or low-risk ambiguity in schema encoding.

## Resume protocol
When interrupted, resume from first unchecked item in `00-review-log.md` and continue batch order without skipping.

## Checkpoint checklist
- [ ] Initialize `00-review-log.md` with batch ledger.
- [ ] Create empty `01-requirement-matrix.csv` with header.
- [ ] Execute Pass A and log extracted requirements.
- [ ] Execute Pass B and log schema coverage anchors.
- [ ] Execute Pass C and produce artifacts 02 and 03.
- [ ] Final sanity pass: every mismatch has evidence and section/line references.
