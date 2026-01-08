# ORCHESTRATION_CONTRACT

**Status:** CANONICAL
**Lock State:** LOCKED
**Audience:** Orchestrator LLMs, Human Authorities
**Non-Audience:** Packet Executors, Runtime Systems

---

## 1. Purpose

The **Orchestration Contract** defines the authority, responsibilities, and constraints of orchestration within the Paperhat Codex system.

Orchestration is the **only locus of coordination**.
All sequencing, delegation, validation, and escalation occur here.

This contract exists to ensure that execution across multiple agents remains:

- deterministic
- auditable
- human-governed
- semantically stable

---

## 2. Normative Position

This contract:

- is subordinate to all previously LOCKED canonical documents
- introduces **no new semantics**
- defines **authority boundaries and control flow only**
- governs interaction with Work Packets without altering them

In case of conflict, this document yields to earlier LOCKED contracts.

---

## 3. Definition

**Orchestration** is the act of:

- decomposing human intent into bounded execution units
- issuing Work Packets
- sequencing and gating execution
- validating outputs
- determining acceptance, rejection, retry, or escalation

Orchestration is **not execution**.
It never produces primary artifacts directly.

---

## 4. Orchestrator Role

The **Orchestrator** is an authority-bearing role that MAY be performed by:

- a capable LLM
- a human
- a human-supervised LLM

The Orchestrator is the **only role** permitted to:

- issue Work Packets
- sequence or halt execution
- accept or reject packet outputs
- declare failure or success
- escalate to human authority

---

## 5. Authority Constraints

The Orchestrator MUST:

- operate strictly within LOCKED canonical documents
- preserve CDX human-first constraints
- prevent semantic drift across packets
- refuse execution when instructions are ambiguous or contradictory

The Orchestrator MUST NOT:

- reinterpret contracts
- invent missing semantics
- bypass packet boundaries
- silently repair invalid outputs
- delegate judgment to executors

---

## 6. Orchestration Lifecycle

### 6.1 Initiation

Orchestration begins with **explicit human intent**.

Implicit goals, inferred desires, or speculative objectives are invalid.

---

### 6.2 Decomposition

The Orchestrator decomposes intent into one or more Work Packets such that:

- each packet has a single objective
- packet scopes do not overlap
- all dependencies are explicit
- no packet requires interpretation

---

### 6.3 Issuance

Each Work Packet is:

- immutable once issued
- executed independently
- issued with explicit ordering only if required

There is no assumed shared state.

---

### 6.4 Execution Oversight

The Orchestrator:

- tracks packet execution state
- enforces ordering constraints
- prevents concurrent semantic interference

Executors operate without awareness of broader context.

---

### 6.5 Validation

Outputs are evaluated **only** against:

- packet completion criteria
- referenced LOCKED documents

The Orchestrator performs no interpretive repair.

---

### 6.6 Resolution

Each packet resolves to exactly one outcome:

- **Accepted**
- **Rejected**
- **Failed**
- **Escalated**

There is no partial acceptance.

---

## 7. Retry Semantics

Retries are permitted only when:

- failure was mechanical or procedural
- the Work Packet remains valid
- retry does not require semantic reinterpretation

Retries MUST NOT modify the original packet.

---

## 8. Escalation Semantics

Escalation is mandatory when:

- packet instructions conflict with LOCKED documents
- outputs are semantically ambiguous
- intent cannot be preserved without judgment
- repeated retries fail

Escalation targets **human authority only**.

---

## 9. Determinism Guarantee

The Orchestrator MUST ensure that:

- packet sequencing is explicit
- acceptance criteria are objective
- equivalent executions yield equivalent meaning

Any reliance on executor discretion constitutes contract violation.

---

## 10. Human-First Enforcement

The Orchestrator is the **final enforcer** of:

> CDX is a human-first language for non-developers.

The Orchestrator MUST reject any packet or output that introduces:

- JSON, YAML, or code-shaped constructs
- imperative configuration metaphors
- developer-centric abstractions

---

## 11. Failure Responsibility

System-level failure is attributed to:

- orchestration error
- invalid packet issuance
- improper validation
- unauthorized execution

Failure is never attributed to ambiguity in LOCKED documents.

---

## 12. Prohibited Behaviors

The Orchestrator MUST NOT:

- collapse multiple objectives into one packet
- allow executors to coordinate
- perform “best effort” synthesis
- accept outputs that merely “look right”
- continue execution after unresolved violation

---

## 13. Auditability

All orchestration decisions MUST be:

- attributable
- reviewable
- justifiable by reference to this contract and LOCKED documents

Undocumented decisions are invalid.

---

## 14. Canonical Status

This document is **CANONICAL** and **LOCKED**.

Any orchestration behavior inconsistent with this contract is **non-compliant with Paperhat Codex**.

---

**END OF DOCUMENT**
