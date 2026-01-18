Status: NORMATIVE  
Version: 0.1  
Editor: Charles F. Munat

# **Codex Schema Versioning Specification — Version 0.1**

This document defines **how schemas are versioned and evolved** in the Codex
language.

Schema versioning rules are part of the Codex language specification and are
governed by this document.

This document is **Normative**.

---

## 1. Purpose

This specification defines **how Codex schemas are versioned and evolved**.

Its goals are to:

* allow schemas to change without breaking existing data
* make compatibility explicit and inspectable
* prevent silent semantic drift
* support long-lived data and tooling stability

This specification governs **schema evolution semantics**, not data migration
mechanisms.

---

## 2. Core Principles

Codex schema versioning is governed by the following principles:

1. **Schemas evolve; data persists**
2. **Compatibility is explicit, not inferred**
3. **Breaking changes are deliberate**
4. **Validation is deterministic and version-aware**

Schemas MUST make their versioning intent explicit.

---

## 3. Schema Identity

Every Codex schema MUST declare:

* a stable schema identifier
* an explicit version designation

The schema identifier defines **what schema this is**.
The version defines **which rules apply**.

Schemas without explicit version information are invalid.

---

## 4. Version Semantics

Schemas MUST use **monotonic versioning**.

Versions MAY be expressed as:

* semantic versions (e.g. `1.2.0`)
* date-based versions (e.g. `2026-01`)
* another documented, totally ordered scheme

The specific format is schema-defined, but ordering MUST be unambiguous.

---

## 5. Compatibility Classes (Normative)

Each schema version MUST declare its compatibility class relative to the
previous version.

Exactly **one** of the following MUST be specified.

---

### 5.1 Backward-Compatible

A backward-compatible version guarantees:

* existing valid Codex data remains valid
* meaning of existing Concepts and Traits is preserved
* new Concepts or Traits MAY be added
* new constraints MAY be added **only if they do not invalidate existing data**

---

### 5.2 Forward-Compatible

A forward-compatible version guarantees:

* Codex data authored for the new version MAY validate under older versions
* older tools can safely ignore newer constructs
* new constructs are optional and additive

Forward compatibility is typically used for extension-oriented evolution.

---

### 5.3 Breaking

A breaking version declares that:

* existing valid Codex data MAY become invalid
* semantics of existing Concepts or Traits MAY change
* migration is required

Breaking versions MUST be explicitly marked.

---

## 6. What Constitutes a Breaking Change

The following changes are **breaking**:

* removing a Concept
* removing a Trait
* changing Entity eligibility
* changing reference semantics
* changing collection semantics
* tightening constraints that invalidate existing data
* changing the meaning of a Concept or Trait

Breaking changes MUST NOT be introduced silently.

---

## 7. Non-Breaking Changes

The following changes are **non-breaking** when properly declared:

* adding new Concepts
* adding optional Traits
* adding new Structural Concepts
* clarifying documentation
* adding new constraints that apply only to newly introduced Concepts

---

## 8. Schema Validation Behavior

When validating Codex data:

* the applicable schema version MUST be known
* validation MUST use that version’s rules
* tools MUST NOT infer or guess schema intent

If schema version information is missing, ambiguous, or incompatible,
validation MUST fail.

---

## 9. Relationship to Data Migration

This specification does **not** define migration mechanisms.

However:

* breaking schema changes imply migration is required
* migration tooling MUST be explicit and deterministic
* migrated data MUST validate cleanly under the target schema version

Schemas define **what changed**, not **how to migrate**.

---

## 10. Tooling Responsibilities

Codex tooling SHOULD:

* surface schema identifiers and versions clearly
* surface declared compatibility classes
* warn when data targets a newer schema version
* refuse to validate data against incompatible schema versions

Tooling MUST NOT silently reinterpret data across schema versions.

---

## 11. Non-Goals

This specification does **not**:

* mandate a specific version numbering format
* define schema storage or distribution mechanisms
* prescribe migration tooling or workflows
* define deprecation timelines or policies

It defines **versioning semantics and obligations** only.

---

## 12. Summary

* Schemas are versioned and explicit
* Compatibility is declared, not inferred
* Breaking changes are intentional and visible
* Validation is version-aware and deterministic
* Schema evolution is controlled, not ad hoc

---

**End of Codex Schema Versioning Specification v0.1**
