# AI Conventions (Codex)

This repo contains normative language specifications and conformance artifacts.

## Scope
- AI assistance is allowed for drafting and editing, but humans remain responsible for correctness.
- The spec is a closed-world conformance target: prefer explicit, testable requirements over open-ended guidance.

## Normativity
- Use RFC 2119/8174 requirement keywords with discipline (use the capitalized forms defined by the spec, in the spec).
- Do not use **SHOULD** and **SHOULD NOT**.
- When changing grammar or surface syntax, update all authoritative forms (e.g., EBNF + PEG) in lockstep.

## Determinism
- Eliminate ambiguity. If two implementations could diverge, specify a deterministic rule.
- Prefer enumerated closed sets ("exactly one of…") over heuristic inference.

## Editing rules
- Make small, targeted changes.
- Do not introduce new terminology without defining it.
- Keep section references stable; if renaming/moving, update all links.

## Validation
Run these from the `codex-lang.dev/` folder:
- `python3 tools/readiness_check.py`
- `python3 tools/conformance_smokecheck.py conformance/1.0.0/manifest/configuration.cdx`
