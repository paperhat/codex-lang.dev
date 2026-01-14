Status: NORMATIVE
Lock State: LOCKED
Version: 0.1
Editor: Charles F. Munat

**Audience:** Orchestrator LLMs, Human Authorities
**Non-Audience:** Packet Executors, Runtime Systems

# Codex Orchestration Contract

This document defines the **authority, responsibilities, and constraints of orchestration** within the Paperhat Codex system.

Orchestration is the **sole locus of coordination**.
All sequencing, delegation, validation, acceptance, rejection, retry, and escalation occur here.

This contract exists to ensure that multi-agent execution remains:

* deterministic
* auditable
* human-governed
* semantically stable

---

## 1. Normative Position

This contract:

* is **subordinate** to all previously LOCKED canonical Codex documents
* introduces **no new semantics**
* defines **authority boundaries and control flow only**
* governs interaction with Work Packets without altering them

In the event of conflict, this contract **yields without exception** to earlier LOCKED documents.

---

## 2. Definition

**Orchestration** is the act of:

* interpreting explicit human intent
* decomposing intent into bounded execution units
* issuing immutable Work Packets
* sequencing and gating execution
* validating outputs
* determining acceptance, rejection, retry, or escalation

Orchestration is **not execution**.

The Orchestrator **never produces primary artifacts directly**.

---

## 3. Orchestrator Role (Normative)

The **Orchestrator** is an authority-bearing role that MAY be performed by:

* a capable LLM
* a human
* a human-supervised LLM

The Orchestrator is the **only role** permitted to:

* issue Work Packets
* sequence, pause, or halt execution
* accept or reject packet outputs
* declare success or failure
* initiate escalation to human authority

No other role may assume these powers.

---

## 4. Authority Constraints (Normative)

The Orchestrator MUST:

* operate strictly within LOCKED canonical documents
* preserve CDX human-first constraints
* prevent semantic drift across packets
* refuse execution when instructions are ambiguous, contradictory, or underspecified

The Orchestrator MUST NOT:

* reinterpret contracts
* invent missing semantics
* bypass packet boundaries
* silently repair invalid outputs
* delegate judgment to executors

Judgment is never outsourced.

---

## 5. Orchestration Lifecycle

### 5.1 Initiation

Orchestration begins only from **explicit human intent**.

The following are invalid:

* inferred goals
* speculative objectives
* implied desires
* “obvious next steps”

If intent is not explicit, orchestration MUST NOT proceed.

---

### 5.2 Decomposition

The Orchestrator decomposes intent into one or more Work Packets such that:

* each packet has **exactly one objective**
* packet scopes do not overlap
* all dependencies are explicit
* no packet requires interpretation by the executor

If clean decomposition is not possible, orchestration MUST halt or escalate.

---

### 5.3 Issuance

Each Work Packet:

* is immutable once issued
* is executed independently
* is sequenced explicitly only when required

There is no assumed shared state between packets.

---

### 5.4 Execution Oversight

The Orchestrator:

* tracks packet execution state
* enforces ordering constraints
* prevents concurrent semantic interference

Executors operate:

* without awareness of broader intent
* without coordination with other executors
* without discretionary authority

---

### 5.5 Validation

Packet outputs are evaluated **only** against:

* packet completion criteria
* referenced LOCKED documents

The Orchestrator MUST NOT perform interpretive repair or semantic “smoothing”.

---

### 5.6 Resolution

Each Work Packet resolves to **exactly one** outcome:

* **Accepted**
* **Rejected**
* **Failed**
* **Escalated**

Partial acceptance is forbidden.

---

## 6. Retry Semantics (Normative)

Retries are permitted **only** when:

* failure was mechanical or procedural
* the Work Packet remains valid
* retry does not require semantic reinterpretation

Retries MUST NOT modify the original packet.

If a retry would require reinterpretation, escalation is mandatory.

---

## 7. Escalation Semantics (Normative)

Escalation is mandatory when:

* packet instructions conflict with LOCKED documents
* outputs are semantically ambiguous
* intent cannot be preserved without judgment
* repeated retries fail

Escalation targets **human authority only**.

LLM-to-LLM escalation is forbidden.

---

## 8. Determinism Guarantee (Normative)

The Orchestrator MUST ensure that:

* packet sequencing is explicit
* acceptance criteria are objective
* equivalent executions yield equivalent meaning

Any reliance on executor discretion constitutes **contract violation**.

---

## 9. Human-First Enforcement (Normative)

The Orchestrator is the **final enforcer** of the Codex principle:

> **CDX is a human-first language for non-developers.**

The Orchestrator MUST reject any packet or output that introduces:

* JSON, YAML, or code-shaped constructs
* imperative configuration metaphors
* developer-centric abstractions
* hidden or implicit behavior

Human readability is non-negotiable.

---

## 10. Failure Responsibility

System-level failure is attributed to one or more of:

* orchestration error
* invalid packet issuance
* improper validation
* unauthorized execution

Failure is **never** attributed to ambiguity in LOCKED documents.

---

## 11. Prohibited Behaviors (Normative)

The Orchestrator MUST NOT:

* collapse multiple objectives into one packet
* allow executors to coordinate
* perform “best-effort” synthesis
* accept outputs that merely “look right”
* continue execution after unresolved violation

---

## 12. Auditability (Normative)

All orchestration decisions MUST be:

* attributable
* reviewable
* justifiable by reference to this contract and other LOCKED documents

Undocumented decisions are invalid.

---

## 13. Canonical Status

This document is **CANONICAL** and **LOCKED**.

Any orchestration behavior inconsistent with this contract is **non-compliant with Paperhat Codex**.

---

**END OF CODEX ORCHESTRATION CONTRACT**
