Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Codex System Contracts

This section contains **contracts** governing systems, libraries, and pipelines that implement or operate on the Codex language.

Contracts define **required behavior** for compliant systems.  
They do **not** define the Codex language itself.

Unless explicitly stated otherwise, all contracts listed here are **Normative**.

---

## 1. Purpose

Codex contracts exist to:

- define obligations and invariants for Codex-based systems
- allocate responsibility across libraries and subsystems
- prevent semantic drift between implementations
- ensure end-to-end correctness and coherence

Violation of a Normative contract constitutes **non-compliance**.

---

## 2. Relationship to the Codex Specification

- The **Codex Language Specification** (under `/spec/`) defines the language.
- Contracts define how systems must interpret, validate, transform, store, query, plan, or render that language.

In the event of conflict:

1. The Codex Language Specification takes precedence.
2. Contracts must conform to the specification.
3. Informative documents have no authority.

---

## 3. Authority and Governance

Contracts are maintained under the same strong editorial governance model as the Codex specification.

- Contracts are public.
- Contracts are open to review.
- Contracts are not crowd-designed.

Final authority over Normative contracts rests with the **Specification Editor**.

---

## 4. Status and Lock State

Every contract MUST declare:

- **Status**: `DRAFT`, `NORMATIVE`, or `INFORMATIVE`
- **Version**: a monotonic version identifier

A contract MAY additionally declare:

- **Lock State**: `LOCKED`

### 4.1 Meaning of LOCKED

If a contract declares `Lock State: LOCKED`, then:

- its requirements are considered stable
- changes MUST be introduced only by publishing a new version
- editorial clarification MAY be published only as an Informative note (never by modifying the locked contract text)

Lock State does not change the conflict rules in §2.

---

## 5. Versioning and Stability

- Each contract is versioned independently.
- Once a contract version is published, it is **immutable**.
- New requirements result in a new version, not modification of an existing one.

Contracts may evolve at different rates.

---

## 6. Contract Index

The following contracts are currently defined:

- **[CODEX_SYSTEM_CONTRACT](./CODEX_SYSTEM_CONTRACT/)**  
  Defines the **foundational nature, scope, and invariants** of **Paperhat Codex**.

- **[CODEX_CANONICAL_COLLECTION_SEMANTICS_CONTRACT](./CODEX_CANONICAL_COLLECTION_SEMANTICS_CONTRACT/)**  
  Defines the **canonical semantics of collections** in Codex.

- **[CODEX_CDX_TO_IR_BOUNDARY_CONTRACT](./CODEX_CDX_TO_IR_BOUNDARY_CONTRACT/)**  
  Defines the **semantic and responsibility boundary** between **Codex**, authored in `.cdx` files, and the **Intermediate Representation (IR)** consumed by downstream systems (e.g. Scribe, planners, renderers, exporters).

- **[CODEX_DESIGN_POLICY_CONTRACT](./CODEX_DESIGN_POLICY_CONTRACT/)**  
  Defines the **exclusive responsibilities, boundaries, and guarantees** of **Design Policy** in Paperhat Codex.

- **[CODEX_DOMAIN_COLLECTIONS_CONTRACT](./CODEX_DOMAIN_COLLECTIONS_CONTRACT/)**  
  Defines **domain collection Concepts** in Codex.

- **[CODEX_ENTITY_ELIGIBILITY_CONTRACT](./CODEX_ENTITY_ELIGIBILITY_CONTRACT/)**  
  Defines **when a Concept may be an Entity** in Codex.

- **[CODEX_MODULE_ASSEMBLY_CONTRACT](./CODEX_MODULE_ASSEMBLY_CONTRACT/)**  
  Defines **Module assemblies** in Codex.

- **[CODEX_ORCHESTRATION_CONTRACT](./CODEX_ORCHESTRATION_CONTRACT/)**  
  Defines the **authority, responsibilities, and constraints of orchestration** within the Paperhat Codex system.

- **[CODEX_PROVENANCE_CONTRACT](./CODEX_PROVENANCE_CONTRACT/)**  
  Defines **provenance in Codex**.

- **[SCRIBE_PIPELINE_CONTRACT](./SCRIBE_PIPELINE_CONTRACT/)**  
  Defines the **exclusive responsibilities, boundaries, and guarantees** of the **Scribe** library.

Additional contracts may be added as the ecosystem expands.

Contract names appearing in ALL_CAPS are canonical identifiers.

---

## 7. Scope of Compliance

A system may:

- comply with all contracts
- comply with a documented subset of contracts
- intentionally diverge

A system that diverges from a contract MUST NOT claim compliance with that contract.

Only systems that meet all applicable requirements may claim full compliance with the referenced contract(s).

---

## 8. Informative Notes

This index defines contract authority and structure only.

Rationale, design discussion, and implementation guidance belong in `/notes/` and are **not binding**.
