# Readiness

This document defines the repo’s readiness gates.

## Required checks
- `python3 tools/readiness_check.py`

The readiness check enforces:
- Required docs exist: `AI_CONVENTIONS.md`, `READINESS.md`.
- No RFC-2119 keyword leakage outside versioned spec documents.
- No ambiguous “validate/validation” wording in spec prose.
- No unfenced `$Token` in Markdown prose.
- Codex annotation well-formedness + canonical blank-line rules across `spec/` and `conformance/`.
- Conformance smokecheck passes for the current conformance pack.
- No `*.json` files exist in the repo working tree (Codex-first rule).

## Conformance pack
- Manifest: `conformance/1.0.0/manifest/configuration.cdx`
- Quick run: `python3 tools/conformance_smokecheck.py conformance/1.0.0/manifest/configuration.cdx`

## Codex annotation lint
- Default run: `python3 tools/annotation_lint.py`
- Scan specific files/dirs: `python3 tools/annotation_lint.py spec/1.0.0/bootstrap-schema/schema.cdx`

## Notes
- If you intentionally need JSON for compatibility, add an explicit, documented exception and update the readiness gate.

## Tooling notes
- Obsolete Codex tooling scripts are archived under `/Users/guy/Workspace/@paperhat/specifications/obsolete/codex-lang.dev/tools/`.
- Active maintenance tools include `tools/schemas_vs_spec_audit.py` and `tools/token_consistency_scan.py`.
