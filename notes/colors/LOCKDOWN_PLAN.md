# Color Lockdown Plan (notes-only tracking)

Goal: fully specify Codex Color Values so that an implementation can parse, validate, convert, and compare colors **without** relying on external living standards, ambiguous prose, or implementation discretion.

Hard constraints:
- No escape hatches: no optionality language and no permitted alternatives.
- Reject-only semantics: no clamping, no normalization, no hue wrapping, no gamut mapping.
- Determinism: one mandated numeric model and one mandated evaluation procedure.

Status legend:
- [ ] not started
- [~] in progress
- [x] done

---

## Batch 0 — Inventory + guardrails

- [~] Identify all remaining spec dependencies on CSS Color / “interpret as CSS” language.
- [ ] List every supported color spelling form and every supported `color(...)` space token.
- [x] Lock numeric model for Lab/OK validity-by-conversion.
- [x] Add drift-catching conformance cases (hue bounds, out-of-gamut, near-boundary pair).

Status: Batch 0 complete.

Exit criteria:
- A concrete list of what remains unspecified, with links to exact sections.

---

## Batch 1 — Freeze full surface grammar (no opaque payloads)

Replace the current “uninterpreted balanced-parentheses payload” approach with explicit EBNF/PEG for:

- [x] Hex colors (`#RGB`, `#RGBA`, `#RRGGBB`, `#RRGGBBAA`)
- [x] Named colors (`&name`)
- [x] `rgb(...)` / `rgba(...)`
- [x] `hsl(...)` / `hsla(...)`
- [x] `hwb(...)`
- [x] `lab(...)`
- [x] `lch(...)`
- [x] `oklab(...)`
- [x] `oklch(...)`
- [x] `color(<space> ...)`
- [x] `color-mix(...)`
- [x] `device-cmyk(...)`
- [x] Relative color forms (`... from <color> ...`)

Define exact lexical forms for numbers:

- [x] decimal numbers, signed numbers
- [x] percentages
- [x] angles (degrees only unless explicitly expanded)
- [x] separators, whitespace, and slash alpha

Status: Batch 1 complete.

Exit criteria:
- Grammar alone determines what spellings are accepted.

---

## Batch 2 — Define semantic IR for ALL color spellings


- [x] Define the complete semantic color IR shape(s) (including alpha handling) used by semantic validation.
- [x] Specify how each surface spelling maps into IR.
- [x] Specify comparison/equality semantics per IR.

Status: Batch 2 complete.

Exit criteria:
- Schema validation can produce a single typed IR for any accepted color spelling.

---

## Batch 3 — Specify conversions + constants in-spec

Pick a single interchange and define all conversion edges with fixed constants and the mandated numeric model.


- [x] Choose interchange (XYZ D65 + alpha).
- [x] Define transfer functions for sRGB and other permitted RGB spaces.
- [x] Define matrices to/from XYZ for each permitted RGB space token.
- [x] Define chromatic adaptation rules where necessary (both directions).
- [x] Ensure Lab/OK rules are consistent with this conversion graph.

Status: Batch 3 complete.

Exit criteria:
- All conversions needed for validity checks and type conversions are defined in Codex itself.

---

## Batch 4 — Validity + canonicalization (total, explicit, reject-only)


For each color function/space:
- [x] Define required finiteness rules for every numeric input.
- [x] Define exact allowed ranges; out-of-range is SchemaError.
- [x] Define alpha handling and alpha range.
- [x] Define hue range policy consistently (no wrap).
- [x] Define canonical surface form rules (case + any formatting allowed) without rewriting semantics.

Status: Batch 4 complete.

Exit criteria:
- For any parsed color spelling, validity is decidable by spec alone.

---

## Batch 5 — Conformance locking


- [x] Add conformance cases per function for:
  - lexical invalid (ParseError)
  - lexically valid but semantically invalid under schema (SchemaError)
  - near-boundary accept/reject pairs for conversion-heavy paths
  - explicit “no clamp/no hue wrap” traps

Status: Batch 5 complete.

Exit criteria:
- Conformance suite detects drift in parsing, validity, and conversion determinism.

---

## Batch 6 — Remove external dependencies


- [x] Eliminate remaining normative references that act as moving specs for color behavior.
- [x] Any unavoidable external identifier is frozen to exact constants/procedures included in Codex.

Status: Batch 6 complete.

Exit criteria:
- Implementers do not need CSS Color / other specs to implement Codex colors.

---

## Batch 7 — Verification


- [x] Run `python3 tools/token_consistency_scan.py`
- [x] Run `python3 tools/conformance_smokecheck.py conformance/1.0.0/manifest/configuration.cdx`
- [x] Run `python3 tools/readiness_check.py`

Status: Batch 7 complete.

Exit criteria:
- Repo checks pass; no new contradictions introduced.
