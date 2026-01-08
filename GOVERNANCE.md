# Codex Specification Governance

Status: NORMATIVE  
Version: 0.1  
Editor: Charles F. Munat

---

## Authority

The Codex Language Specification is maintained under a **strong editorial governance model**.

* The specification is public.
* The specification is open to review.
* The specification is not crowd-designed.

Final authority over **Normative** content rests with the **Specification Editor**.

---

## Origin and Stewardship

Codex was originated by **Charles F. Munat**, who serves as the **Specification Editor**.

The Codex Language Specification and all associated Normative documents are stewarded under a **single-editor governance model** to ensure long-term coherence, semantic integrity, and architectural consistency.

The Specification Editor holds final responsibility and authority for:

* defining the canonical meaning of the Codex language
* approving, rejecting, and ratifying normative changes
* maintaining versioned, authoritative specifications and contracts
* determining compatibility, conformance, and compliance criteria

While the specification is public and open to review, **decision-making authority over Normative content is centralized** in the Specification Editor in order to preserve clarity, continuity, and conceptual integrity.

If the Specification Editor is unable or unwilling to continue in this role, editorial authority may be transferred by the outgoing editor, or, in their absence, by a process publicly defined in this repository.

This stewardship model prioritizes correctness, stability, and semantic coherence over consensus or majority rule.

---

## Authority Lattice (Normative)

This section defines the **authoritative ordering of documents and artifacts** within the Codex ecosystem.

In the event of conflict, **higher-tier documents take precedence over lower-tier documents**.
Lower-tier documents MUST conform to higher-tier documents.

### 1. Codex Language Specification (`/spec/`)

* Defines the Codex language itself
* Defines syntax, structure, naming, identity, collections, schemas, and validation
* Is **immutable once published**
* Is the highest authority in the system

Nothing may contradict the specification.

---

### 2. Codex System Contract

* Defines the foundational invariants and guarantees of Paperhat Codex as a system
* Interprets the specification into system-level obligations
* MUST conform fully to the Codex Language Specification

---

### 3. Normative Contracts (`/contracts/`)

* Define required behavior, boundaries, and responsibilities of systems and libraries
* Include (but are not limited to):

  * pipeline contracts
  * library responsibility contracts
  * orchestration and provenance contracts

All Normative contracts:

* MUST conform to the Codex Language Specification
* MUST conform to the Codex System Contract
* MAY further constrain behavior, but MUST NOT redefine semantics

---

### 4. Lock State

A document marked with:

```
Lock State: LOCKED
```

is **frozen within its authority tier**.

* LOCKED documents MUST NOT be reinterpreted
* Changes require a new version
* LOCKED does **not** elevate a document above its tier
* LOCKED only enforces immutability, not authority

Lock State applies primarily to **Normative contracts** and governance-critical documents.

---

### 5. Orchestration and Process Documents

Documents governing orchestration, delegation, or process:

* define control flow and authority boundaries
* introduce no new semantics
* MUST conform to all higher tiers
* MAY enforce stricter discipline on execution and tooling

They govern **how work proceeds**, not **what Codex means**.

---

### 6. Informative Documents

Informative documents:

* include notes, rationale, examples, and guidance
* carry **no authority**
* MUST NOT be used to justify behavior
* MAY be changed or removed without formal process

If an Informative document conflicts with a Normative one, it is wrong by definition.

---

## Normative Changes

Changes to **Normative** documents:

* must be explicit and intentional
* must preserve declared guarantees
* must be versioned
* are ratified by the Specification Editor

Once published, a version of a Normative document is **immutable**.

---

## Informative Content

Informative documents:

* may change without formal process
* do not define required behavior
* do not participate in authority resolution

They exist to aid understanding, not to govern systems.

---

## Implementations

This repository defines **language and system requirements**, not implementations.

Implementations may:

* reimplement Codex independently
* extend it experimentally
* diverge intentionally

Only documents designated as **Normative** define Codex.

---

## Compatibility & Claims

Use of the terms “Codex”, “Codex-compatible”, or similar claims of compliance may be subject to additional requirements defined by the Specification Editor.

False or misleading claims of compliance constitute non-conformance.

---

### End of GOVERNANCE.md
