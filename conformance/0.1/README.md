Status: INFORMATIVE
Version: 0.1

# Codex 0.1 Conformance Fixtures

This directory contains **versioned conformance fixtures** for Codex Language Specification v0.1.

These fixtures are intentionally stored **outside** `spec/0.1/` because the spec tree is frozen/locked.

## Goals

- Provide a shared corpus of **valid** and **invalid** `.cdx` documents.
- Provide expected **canonical output** for documents that should canonicalize deterministically.
- Provide expected **primary error class** (per the Validation Error Taxonomy) for invalid inputs.

## What This Is / Is Not

- This is a **fixture pack**, not a parser.
- The included runner (`conformance_smokecheck.py`) validates the fixture pack is internally consistent (files exist, expected outputs exist, newline conventions, etc.).
- A real Codex implementation should use these fixtures to run: normalization → parse → surface-form validation → canonicalization → schema validation.

This fixture pack is **Codex-first**. JSON is not used for normative fixture data.

## Layout

- `manifest/configuration.cdx` — the index of cases (Codex).
- `cases/valid/<case-id>/data.cdx` — syntactically + surface-form valid inputs.
- `cases/invalid/<case-id>/data.cdx` — inputs expected to fail.
- `expected/canonical/<case-id>/data.cdx` — expected canonical form for some valid inputs.
- `expected/errors/<case-id>/data.cdx` — expected primary error class for invalid inputs.

## Running the smoke check

From the repo root:

```bash
python3 codex-lang.dev/tools/conformance_smokecheck.py codex-lang.dev/conformance/0.1/manifest/configuration.cdx
```

## Spec references

- Canonical error classes: `codex-lang.dev/spec/0.1/validation-errors/`
- Surface form: `codex-lang.dev/spec/0.1/surface-form/`
- Formal grammar (EBNF normative): `codex-lang.dev/spec/0.1/grammar/`
