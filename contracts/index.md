Status: NORMATIVE
Version: 0.1
Editor: Charles F. Munat

# Codex System Contracts

This section contains **Normative contracts** governing systems, libraries, and pipelines that implement or operate on the Codex language.

These documents define **required behavior** for compliant systems.
They do **not** define the Codex language itself.

---

## Purpose

Codex contracts exist to:

- define obligations and invariants for Codex-based systems
- allocate responsibility across libraries and subsystems
- prevent semantic drift between implementations
- ensure end-to-end correctness and coherence

Violation of a Normative contract constitutes **non-compliance**.

---

## Relationship to the Codex Specification

- The **Codex Language Specification** (under `/spec/`) defines the language.
- **Contracts** define how systems must interpret, validate, transform, or render that language.

In the event of conflict:

1. The Codex Language Specification takes precedence.
2. Contracts must conform to the specification.
3. Informative documents have no authority.

---

## Contract Authority

All contracts in this section are maintained under the same **strong editorial governance model** as the Codex specification.

- Contracts are public.
- Contracts are open to review.
- Contracts are not crowd-designed.

Final authority over Normative contracts rests with the **Specification Editor**.

---

## Versioning and Stability

- Each contract is versioned independently.
- Once a contract version is published, it is **immutable**.
- New requirements result in a new version, not modification of an existing one.

Contracts may evolve at different rates.

---

## Contract Index

The following contracts are currently defined:

- **CODEX_SYSTEM_CONTRACT**
  Defines baseline requirements for any system that processes Codex documents.

- **SCRIBE_PIPELINE_CONTRACT**
  Defines the required stages, invariants, and responsibilities of the Codex processing pipeline.

Additional contracts may be added as the ecosystem expands.

---

## Scope of Compliance

A system may:

- comply with all contracts
- comply with a documented subset of contracts
- intentionally diverge

Only systems that meet all applicable requirements may claim full compliance with the referenced contract(s).

---

## Informative Notes

This index defines **contract authority and structure only**.

Rationale, design discussion, and implementation guidance belong in `/notes/` and are **not binding**.
