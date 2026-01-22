Status: NON-NORMATIVE (Historical; incorporated into codex-language-specification.md §12.4)
Lock State: UNLOCKED
Version: 0.1
Editor: Charles F. Munat

# Codex Bootstrap Schema-of-Schemas Definition — Version 0.1

This document is retained for historical/reference purposes.

The authoritative normative content is incorporated into `spec/0.1/codex-language-specification.md` §12.4.

This document defines the **bootstrap schema-of-schemas** required by Codex.

Schema documents (root Concept `Schema`) cannot depend on an external schema
document to be **validated** without circularity.

Therefore every conforming implementation MUST include a **built-in, hard-coded**
bootstrap schema-of-schemas.

This document defines that bootstrap schema-of-schemas **normatively**, by
specifying:

- the bootstrapping requirement (built-in, hard-coded)
- which specification is the single source of truth for schema-language constructs
- required error classification when a schema is bootstrap-invalid

---

## 1. Terminology (Normative)

### 1.1 Bootstrap Schema-of-Schemas

The **bootstrap schema-of-schemas** is the built-in schema language runtime. It
is not loaded from disk/network.

It exists so an implementation can parse and validate **schema documents**
without circular dependency.

### 1.2 Meta-Schema

A **meta-schema** (in Codex’s broader ecosystem) is a schema document written in
Codex that is **valid under the bootstrap schema-of-schemas** and that defines a
class of schemas (e.g., data schemas, view schemas, configuration schemas).

Meta-schemas are external artifacts (typically `schema.cdx`) and are not required
to be available until an implementation needs to validate schemas of that class.

---

## 2. Conformance Requirement (Normative)

A conforming Codex implementation MUST embed a bootstrap schema-of-schemas that
is functionally equivalent to:

* the bootstrapping requirements in this document, and
* the schema-language definition in `spec/0.1/codex-language-specification.md` §11.

Equivalence is defined by behavior:

- A schema document that satisfies this document MUST be accepted as a valid
  schema document.
- A schema document that violates this document MUST produce a `SchemaError`
  (unless the document is not structurally readable, in which case it is a
  `ParseError`).

---

## 3. Canonical Schema-Language Definition (Normative)

This document defines **bootstrapping requirements** and error classification.

All schema-language constructs that appear inside schema documents are defined
normatively in exactly one place:

* `spec/0.1/codex-language-specification.md` §11

That specification is the single source of truth for:

- the `Schema` Concept and schema document structure
- concept definitions (`ConceptDefinitions`, `ConceptDefinition`, and rules)
- trait definitions (`TraitDefinitions`, `TraitDefinition`, `AllowedValues`)
- value types (`ValueTypeDefinitions`, `ValueTypeDefinition`, and built-in tokens)
- enumerated value sets (`EnumeratedValueSets`, `EnumeratedValueSet`, `Member`)
- declarative constraints (`ConstraintDefinitions`, rule algebra, paths/quantifiers,
  and atomic constraints)

The bootstrap schema-of-schemas MUST accept exactly the schema documents that
conform to the Schema Definition Specification v0.1.

---

## 4. Error Classification (Normative)

- If a schema document is not structurally readable (e.g., malformed markers),
  the failure is a `ParseError`.
- If a schema document is structurally readable but violates the bootstrap
  schema-of-schemas rules, the failure is a `SchemaError`.

---

**End of Codex Bootstrap Schema-of-Schemas Definition v0.1**
