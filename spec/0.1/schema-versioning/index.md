# Codex Schema Versioning Contract (DRAFT)

## Status

- **DRAFT**  
- Normative once locked  
- Applies to all Codex schemas used for validation, compilation, and tooling

---

## 1. Purpose

This contract defines **how Codex schemas are versioned and evolved**.

Its goals are to:

- allow schemas to change without breaking existing data
- make compatibility explicit and inspectable
- prevent silent semantic drift
- support long-lived data and tooling stability

This contract governs **schema evolution**, not data migration mechanics.

---

## 2. Core Principles

Codex schema versioning is governed by four principles:

1. **Schemas evolve; data persists**
2. **Compatibility is explicit, not inferred**
3. **Breaking changes are deliberate**
4. **Validation must be deterministic**

Schemas must make their versioning intent clear.

---

## 3. Schema Identity

Every Codex schema MUST have:

- a stable schema identifier
- an explicit version designation

The schema identifier identifies **what schema this is**.
The version identifies **which rules apply**.

Schemas without explicit versioning are invalid.

---

## 4. Version Semantics

Schemas MUST use **monotonic versioning**.

Versions may be expressed as:

- semantic versions (e.g. `1.2.0`)
- date-based versions (e.g. `2026-01`)
- another documented, ordered scheme

The specific format is schema-defined, but ordering MUST be unambiguous.

---

## 5. Compatibility Classes (Normative)

Each schema version MUST declare its compatibility class relative to the previous version.

Exactly one of the following MUST be specified:

### 5.1 Backward-Compatible

- Existing valid CDX remains valid
- Meaning of existing Concepts and Traits is preserved
- New Concepts or Traits may be added
- New constraints may be added **only if they do not invalidate existing data**

---

### 5.2 Forward-Compatible

- New CDX may validate under older schema versions
- Existing tools can safely ignore newer constructs
- Typically used for additive, optional extensions

---

### 5.3 Breaking

- Existing valid CDX may become invalid
- Semantics of existing Concepts or Traits may change
- Migration is required

Breaking versions MUST be explicitly marked.

---

## 6. What Counts as a Breaking Change

The following are **breaking changes**:

- removing a Concept
- removing a Trait
- changing Entity eligibility
- changing reference or collection semantics
- tightening constraints that invalidate existing data
- changing the meaning of a Concept or Trait

Breaking changes MUST NOT be introduced silently.

---

## 7. Non-Breaking Changes

The following are **non-breaking** when properly declared:

- adding new Concepts
- adding optional Traits
- adding new structural Concepts
- clarifying documentation
- adding new constraints that only apply to new Concepts

---

## 8. Schema Validation Behavior

When validating CDX:

- the schema version MUST be known
- validation MUST use that version’s rules
- tools MUST NOT “guess” schema intent

If schema version information is missing or ambiguous, validation MUST fail.

---

## 9. Relationship to Data Migration

This contract does **not** define migration mechanisms.

However:

- breaking schema changes imply migration is necessary
- migration tools MUST be explicit and deterministic
- migrated data MUST validate cleanly under the target schema

Schemas define **what changed**, not **how to migrate**.

---

## 10. Tooling Responsibilities

Codex tooling SHOULD:

- surface schema version and compatibility clearly
- warn when data targets a newer schema version
- refuse to validate data against incompatible schemas

Tooling MUST NOT silently reinterpret data across versions.

---

## 11. Non-Goals

This contract does **not**:

- mandate a version number format
- define schema storage or distribution
- prescribe migration tooling
- define deprecation timelines

It defines **versioning semantics and obligations** only.

---

## 12. Summary

- Schemas are versioned and explicit
- Compatibility is declared, not inferred
- Breaking changes are intentional and visible
- Validation is version-aware and deterministic
- Schema evolution is safe, not ad hoc

---
