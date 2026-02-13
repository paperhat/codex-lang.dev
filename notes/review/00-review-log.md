# Review Log

## Scope lock
- Spec (normative): `specifications/codex-lang.dev/spec/1.0.0/index.md`
- Schema (informative): `specifications/codex-lang.dev/spec/1.0.0/bootstrap-schema/schema.cdx`
- No source edits allowed.

## Batch ledger
- [x] A1 Sections 1-4 extracted
- [x] A2 Section 5 extracted
- [x] A3 Sections 6-8 extracted
- [x] A4 Section 9 extracted
- [x] A5 Sections 10-12 extracted
- [x] A6 Sections 13-14 + Appendix A normative portions extracted
- [x] A7 Informative filtering complete
- [x] B1 Schema preamble and top-level `Schema` traits indexed
- [x] B2 GROUP blocks 1-20 indexed
- [x] B3 GROUP blocks 21-40 indexed
- [x] B4 GROUP blocks 41-60 indexed
- [x] B5 GROUP blocks 61-80 indexed
- [x] B6 Global consistency checks complete
- [x] C1 Forward mapping complete
- [x] C2 Reverse mapping complete
- [x] C3 Mismatch classification complete
- [x] C4 Recommendations drafted

## Running notes
- Built extracted triple index (`tmp-schema-triples.tsv`) and logical-shape index (`tmp-schema-shape-logical.tsv`) to avoid manual interpretation errors.
- Confirmed mode-conditional `Schema` children are encoded via root `sh:xone` subshapes.
- Confirmed high-severity contradiction: `Schema` requires `codex:declaredId` but fixes `codex:isEntity=false`.
- Produced required deliverables:
  - `01-requirement-matrix.csv`
  - `02-mismatch-report.md`
  - `03-change-recommendations.md`
