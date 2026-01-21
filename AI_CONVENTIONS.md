Status: INFORMATIVE
Version: 0.1

# AI + Automation Conventions (Codex spec repo)

This document is **not part of the Codex language specification**. It exists to
prevent regressions in a multi-session, multi-agent workflow.

## Reality Check (LLM Limitations)

This repo assumes automation may be driven by LLMs.

LLMs can be helpful, but they are not authoritative: they can hallucinate, miss
context, produce inconsistent output across sessions, and “helpfully” regress
policy (e.g., reintroducing JSON).

Therefore:

- Treat chat output as non-authoritative; only committed artifacts + gates count.
- Prefer deterministic checks over intent.
- Require tools/scripts to verify claims.

## Non-Negotiables

- **Codex-first**: normative artifacts MUST be Codex (`.cdx`) or Markdown (`.md`).
- **No JSON by default**: do not add or generate JSON in this repo.
- **Compat-only exception**: if JSON is unavoidable for an external consumer, it MUST:
  - be explicitly marked **DEPRECATED / compat-only** in adjacent documentation, and
  - have a named consumer and a removal plan.

## Tooling Output Policy

- Tools MUST emit reports as `.cdx` or `.md`.
- Tools MUST NOT emit `.json` reports.

## Verification Rules

- Every change that claims to improve “readiness” MUST be validated by running `python3 tools/readiness_check.py`.
- Avoid “speculative edits”: if a change is not directly supported by the spec text or a concrete schema artifact, write a short decision record in Markdown instead of silently changing behavior.
- If a file contains conflict markers (e.g., `<<<<<<<`), resolve them before claiming readiness.

## Single Source of Truth (Required)

To prevent permanent drift across sessions (human or automated), this repo
requires a **single source of truth** for every normative definition.

- A Concept, Trait, token set, rule, default, error classification, or other
  normative construct MUST be **defined in exactly one place**.
- Any other document that needs to mention that construct MUST:
  - link to the single defining location, and
  - avoid restating the definition (no “duplicate definitions”, even if the
    wording is intended to be identical).

If a document needs to summarize behavior for readability, it MUST do so using
non-normative prose and a direct pointer to the defining clause.

When we find duplicated definitions, the fix is always:

1. Pick the canonical defining location.
2. Delete the duplicate text.
3. Replace it with a reference.

## Conformance Fixture Layout

- Case directory name is the document “name”.
- Primary document file name is `data.cdx`.
- Reserved special documents may use specific names (e.g., `configuration.cdx`).

## Canonical Surface Form Requirements

When producing canonical expected outputs, follow the spec’s deterministic rules:

- Trait layout: 1–2 traits single-line; 3+ traits multiline (one per line), indented one level deeper than the Concept marker.
- Children-mode blank lines: exactly one blank line between sibling Concepts; forbidden elsewhere (except Content and annotation-specific rules).
- `CODE:` / `MD:` block annotations are byte-preserving (no trim/reindent/wrap; only newline normalization).

## Definition of Done (“Production Ready”)

In this repo, **“production ready” means**: all checks in `tools/readiness_check.py` pass on a clean checkout.
