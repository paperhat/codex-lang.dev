Status: INFORMATIVE
Version: 0.1

# Codex v0.1 Readiness Definition (Repo Gate)

This document defines what “ready for production implementation” means for this repo.

This gate exists specifically to make readiness **verifiable** even when changes
are proposed or applied by fallible automation (including LLM-driven agents).

## Definition

The repo is **ready** if and only if:

- `python3 tools/readiness_check.py` exits with status code 0.

## What the readiness check enforces

- Conformance pack is internally consistent and runnable via `conformance_smokecheck.py`.
- No JSON artifacts exist in the repo working tree (Codex-first posture).
- The repo’s automation policy documents are present.

## How to run

From the repo root:

```bash
python3 tools/readiness_check.py
```
