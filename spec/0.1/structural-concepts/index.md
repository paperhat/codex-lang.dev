# Codex Structural Concepts Contract (DRAFT)

## Status

- **DRAFT**
- Normative once locked
- Applies to all Codex schemas and documents that use structural Concepts

---

## 1. Purpose

This contract defines **structural Concepts** in Codex.

Structural Concepts:

- organize, group, or scope other Concepts
- provide **structural meaning**, not domain meaning
- derive their semantics entirely from **context and schema**

This contract exists to:

- prevent accidental semantic collisions with domain vocabularies
- avoid global namespace pollution
- preserve plain-English readability
- make Codex safely interoperable with external schemas (e.g. schema.org)

---

## 2. What a Structural Concept Is

A **Structural Concept** is a Concept whose primary role is to:

- group Concepts
- delimit scope
- express containment or organization
- provide contextual structure

Structural Concepts:

- do **not** express domain meaning on their own
- do **not** imply identity unless explicitly allowed
- do **not** have universal semantics

Their meaning is **entirely schema-defined**.

---

## 3. Contextual Meaning (Normative)

Structural Concepts are interpreted **only within a specific schema-defined context**.

> A Structural Concept name has no global meaning in Codex.

The same Concept name MAY:

- be structural in one context
- be semantic in another context
- or be unused entirely

Codex deliberately avoids global prefixing (e.g. `CodexModule`) in favor of **contextual meaning**.

---

## 4. Codex Module Assembly Context

Within the **Codex module-assembly context**, the following Concepts are defined as **Structural Concepts** by schema:

- `Module`
- `Data`
- `Views`
- `Policies`
- `Plans`
- `Config`
- `Provenance`
- `Groups`
- `Group`

In this context:

- `Module` is a root Structural Concept representing a semantic assembly
- the remaining Concepts define **sectional structure** within a Module

Their meaning exists **only** because the Codex module schema defines it.

---

## 5. Structural Concepts Are Not Domain Claims

Structural Concepts:

- do **not** assert facts about the domain
- do **not** represent entities unless explicitly allowed
- do **not** compete with external vocabularies

For example:

- `Data` does not mean “data” in the abstract
- `Views` does not mean “views” globally
- `Policies` does not define a policy ontology

They are **organizational constructs**, not domain terms.

---

## 6. Identity Rules for Structural Concepts

By default:

- Structural Concepts **must not** declare an `id`
- Structural Concepts are **not Entities**

Exceptions:

- A schema MAY explicitly authorize identity for a specific Structural Concept
- Such authorization must be explicit and documented

Absent explicit authorization, assigning an `id` to a Structural Concept is a schema error.

---

## 7. Use Outside the Module Context

Structural Concept names defined in the Codex module context:

- MAY be reused in other schemas
- MAY have different meanings in other contexts
- MUST NOT be assumed to carry Codex module semantics elsewhere

Codex makes **no global claim** over these names.

---

## 8. Relationship to Domain Collections

Structural Concepts are distinct from **domain collections**.

- Structural Concepts organize **heterogeneous** Concepts
- Domain collections group **multiple individuals of the same domain class**

Structural Concepts MUST NOT be used as substitutes for domain collections.

---

## 9. Non-Goals

This contract does **not**:

- define domain ontologies
- prescribe schema contents
- enforce specific section names outside Codex module context
- restrict external schema design
- impose global namespaces

---

## 10. Summary

- Structural Concepts organize meaning; they do not create it
- Their semantics are **contextual and schema-defined**
- Names are intentionally plain and reusable
- Codex avoids global prefixes in favor of scoped meaning
- Structural Concepts are not domain entities by default
