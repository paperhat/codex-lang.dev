Status: NORMATIVE
Lock State: LOCKED
Version: 1.0.0
Editor: Charles F. Munat

# Codex Language Documentation Governance

## 1. Purpose

This document defines the **governance rules** for the documentation published at **codex-lang.dev**.

Its purpose is to:

* establish **authority and precedence** among documents
* define **normative status**, lock state, and change control
* clarify the relationship between the Codex language specification and implementations
* prevent ambiguity, drift, or contradictory interpretation

This document governs **documentation only**.

---

## 2. Scope

This governance applies to all content in the codex-lang.dev repository, including:

* the Codex Language Specification
* formal contracts and constraints
* normative supporting documents
* examples and explanatory material

It does **not** govern software implementations, tools, editors, parsers, or runtimes, which are maintained separately and may be licensed independently.

---

## 3. Document Categories

Documentation is categorized as follows.

### 3.1 Normative Documents

Normative documents define **binding rules** of the Codex language.

These include, but are not limited to:

* the Codex Language Specification
* naming and structural rules
* semantic and interpretive constraints
* formally declared invariants

Normative documents may be marked **LOCKED** or **DRAFT**.

### 3.2 Non-Normative Documents

Non-normative documents provide:

* explanation and clarification
* rationale and background
* illustrative examples
* exploratory or historical notes

Non-normative documents are **not authoritative**.

---

## 4. Lock State

### 4.1 LOCKED

A document marked **LOCKED**:

* is authoritative
* must not be changed except via an explicit, versioned revision
* provides a stable reference for implementations and tooling
* is safe to rely upon for automated processing

### 4.2 DRAFT

A document marked **DRAFT**:

* is under active development
* may change without notice
* must not be treated as authoritative

---

## 5. Authority Order

In the event of conflict, documents are interpreted according to the following precedence (highest first):

1. **Codex Language Specification**
2. **Normative Language Contracts**
3. **Normative Supporting Documents**
4. **Examples**
5. **Notes**

Lower-authority documents must not contradict higher-authority documents.

---

## 6. Relationship to Implementations

The Codex documentation:

* defines the **syntax, structure, and semantic intent** of the Codex language
* does **not** mandate any specific implementation strategy
* does **not** grant rights to any software implementation

Implementations of Codex:

* are independent works
* may be licensed separately
* may differ internally, provided they conform to all applicable normative documents

---

## 7. Licensing

All documentation in this repository is licensed under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)** as specified in the repository's `LICENSE` file.

The license applies to **textual, diagrammatic, and illustrative content only**.

No rights are granted to:

* trademarks, service marks, or logos
* project, language, or specification names
* software implementations, unless explicitly stated otherwise

---

## 8. Final Authority

This document is **NORMATIVE and LOCKED**.

Any interpretation of Codex documentation must be consistent with this governance.

---

**End of Codex Language Documentation Governance v1.0.0**
