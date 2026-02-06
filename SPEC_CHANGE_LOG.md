# Spec Change Log

This file records all changes made to the Codex specification during implementation.

---

## 2026-02-03: §14.6.1 — Make `message` required

**Section:** 14.6.1 Error Payload Shape (Recommended)

**Change:** Changed `message` from `(optional)` to `(required)`.

**Rationale:** The human-readable error message is essential for reducing cognitive load. A tool that emits machine-readable `code` without a human-readable `message` is technically conforming but user-hostile. Humans come first.

---

## 2026-02-05: §5.4 + A.1.12 — Remove `+` sign from numeric values

**Sections:** §5.4 Numeric Values, A.1.12 Numeric Values grammar

**Changes:**
1. Added prose: "Explicit `+` signs are not permitted; absence of a sign indicates a positive value."
2. Changed `Integer` grammar from `[ Sign ]` to `[ "-" ]`
3. Changed `DecimalNumber` grammar from `[ Sign ]` to `[ "-" ]`

**Rationale:** Round-trippability. If `+42` were accepted and stored as `Integer(42)`, we could not preserve the exact spelling on output. The spec requires "Numeric spellings MUST be preserved exactly." Rejecting `+` is the simplest, most deterministic approach.

---

## 2026-02-05: PEG grammar — Align `Integer` and `DecimalNumber` with EBNF amendment

**Section:** PEG grammar (Appendix A.2)

**Changes:**
1. Changed `Integer` PEG from `'0' / Sign? [1-9] Digit*` to `'0' / '-'? [1-9] Digit*`
2. Changed `DecimalNumber` PEG from `Sign? IntDigits '.' Digits` to `'-'? IntDigits '.' Digits`

**Rationale:** The EBNF grammar (A.1.12) was amended on 2026-02-05 to use `[ "-" ]` instead of `[ Sign ]`, but the corresponding PEG grammar was missed. This change brings the PEG grammar into alignment.

---

## 2026-02-06: §5.17 + A.1.24 + A.2.21 — Restrict Range endpoints to ordered numeric types

**Sections:** §5.17 Range Values, A.1.24 Range Values grammar, A.2.21 Range Values PEG grammar

**Changes:**
1. Added prose to §5.17: Range endpoints and step values MUST be ordered numeric types (Integer, DecimalNumber, Fraction, ExponentialNumber, or PrecisionNumber), Temporal Values, or Character Values. ComplexNumber, ImaginaryNumber, and Infinity MUST NOT appear as range endpoints or step values.
2. Introduced `OrderedNumericValue` production in both EBNF and PEG grammars, listing the five permitted numeric types.
3. Changed `RangeStart`, `RangeEnd`, and `StepValue` to reference `OrderedNumericValue` instead of `NumericValue`.
4. Fixed incorrect example in §5.17: "both Integer, both Text" → "both Integer, both PlainDate" (Text was never a valid range endpoint).

**Rationale:** ComplexNumber and ImaginaryNumber lack a total ordering, making interval semantics undefined. Infinity as an inclusive range endpoint is contradictory. Only numeric types on the real number line with well-defined ordering are meaningful as range bounds.
