# Readiness

This document defines the repo’s readiness gates.

## Required checks
- `python3 tools/readiness_check.py`

The readiness check enforces:
- Required docs exist: `AI_CONVENTIONS.md`, `READINESS.md`.
- Conformance smokecheck passes for the current conformance pack.
- No `*.json` files exist in the repo working tree (Codex-first rule).

## Conformance pack
- Manifest: `conformance/1.0.0/manifest/configuration.cdx`
- Quick run: `python3 tools/conformance_smokecheck.py conformance/1.0.0/manifest/configuration.cdx`

## Notes
- If you intentionally need JSON for compatibility, add an explicit, documented exception and update the readiness gate.
