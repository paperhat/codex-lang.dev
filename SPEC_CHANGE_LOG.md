# Spec Change Log

This file records all changes made to the Codex specification during implementation.

---

## 2026-02-03: §14.6.1 — Make `message` required

**Section:** 14.6.1 Error Payload Shape (Recommended)

**Change:** Changed `message` from `(optional)` to `(required)`.

**Rationale:** The human-readable error message is essential for reducing cognitive load. A tool that emits machine-readable `code` without a human-readable `message` is technically conforming but user-hostile. Humans come first.
