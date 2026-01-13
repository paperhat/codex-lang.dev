# Codex Evolution and Migration Guidelines (DRAFT)

## Status

- **DRAFT**  
- Informative  
- Applies to humans and tools evolving Codex schemas and data over time

---

## 1. Purpose

This document provides **practical guidance** for evolving Codex schemas and migrating existing CDX data.

Its goals are to:

- reduce risk during schema evolution
- make migrations predictable and auditable
- preserve semantic intent over time
- avoid silent or implicit changes

This document introduces **no new rules**.
It explains how to work _within_ the existing contracts.

---

## 2. Core Principle

> **Schemas may change. Data must remain meaningful.**

Evolution in Codex is always explicit, intentional, and inspectable.

---

## 3. When a Migration Is Required

A migration is required whenever a schema change is **breaking**.

Common triggers include:

- a Concept is removed or renamed
- a Trait is removed or renamed
- Entity eligibility changes
- reference or collection semantics change
- constraints are tightened in ways that invalidate existing data

If existing valid CDX would fail validation under the new schema, migration is required.

---

## 4. Preferred Evolution Strategies

### 4.1 Add, Don’t Mutate

Whenever possible:

- add new Concepts instead of changing existing ones
- add new optional Traits instead of changing meanings
- phase out old Concepts gradually

This minimizes migration pressure.

---

### 4.2 Phase-Out Before Removal

When a Concept or Trait must be removed:

1. Mark it as scheduled for removal in the schema
2. Allow both old and new forms temporarily
3. Migrate data explicitly
4. Remove old forms in a later breaking version

Never remove silently.

---

## 5. Migration Mechanics

Migration is a **separate, explicit step**.

- Migration tools transform CDX data
- Migration output MUST validate cleanly against the target schema
- Migration MUST be deterministic and repeatable

CDX itself does not encode migration logic.

---

## 6. Identity Preservation

During migration:

- Entity identifiers SHOULD be preserved whenever meaning is preserved
- Changing an identifier implies a new Entity
- Identifier reuse for different meaning is forbidden

If meaning changes materially, create a new Entity.

---

## 7. Trait and Concept Renaming

Renaming is not cosmetic.

- Renaming a Concept or Trait is a breaking change
- Migration MUST rewrite affected CDX explicitly
- Aliases may be supported temporarily, but only by schema

Never rely on tooling to “know” that two names mean the same thing.

---

## 8. Reference Integrity

After migration:

- all references MUST point to valid Entities
- no dangling references are permitted
- reference intent (`reference`, `target`, `for`) MUST be preserved

Migration tools MUST fail if reference integrity cannot be guaranteed.

---

## 9. Collection Semantics

When migrating collections:

- preserve ordering where ordering is semantic
- do not invent ordering where none existed
- preserve membership meaning exactly

Changing collection semantics is a breaking change and requires migration.

---

## 10. Validation After Migration

All migrated CDX MUST:

- pass surface form validation
- pass schema validation
- satisfy identity and reference rules
- normalize to canonical form

If migrated data does not validate, the migration is incorrect.

---

## 11. Human Review

Even when migrations are automated:

- changes SHOULD be reviewable
- diffs SHOULD be inspectable
- intent SHOULD be documented

Codex favors **explicit change** over silent convenience.

---

## 12. Non-Goals

These guidelines do **not**:

- mandate migration tooling
- prescribe workflows or approvals
- define rollback strategies
- automate schema evolution

They describe **good practice**, not enforcement.

---

## 13. Summary

- Schema evolution is expected and supported
- Breaking changes require explicit migration
- Identity and meaning must be preserved intentionally
- Migration is separate from authoring
- Validation is the final authority
