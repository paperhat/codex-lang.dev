Status: NORMATIVE
Lock State: UNLOCKED
Version: 0.1
Editor: Charles F. Munat

# Codex Schema Loading Specification — Version 0.1

This specification defines **how schemas are associated with documents** for
parsing.

It governs:

* Schema provision mechanisms
* Schema resolution order
* Meta-schema bootstrapping
* Error handling when schema is unavailable

This document is **Normative**.

---

## 1. Purpose

Codex is a schema-first language. A document cannot be parsed without its
governing schema.

This specification defines how parsers obtain the schema for a document.

Its goals are to:

* ensure every parse operation has a schema
* support multiple schema provision mechanisms
* enable bootstrapping via meta-schema
* provide clear errors when schema is unavailable

---

## 2. Schema Provision Mechanisms (Normative)

A conforming parser MUST support **explicit schema provision**.

A conforming parser MAY support additional mechanisms.

### 2.1 Explicit Provision (Required)

The caller provides the schema directly to the parser.

```
parse(document, schema) → AST
```

This is the baseline mechanism. All conforming implementations MUST support it.

### 2.2 Schema Registry (Optional)

The parser MAY consult a registry to resolve schema identifiers.

Implementation details are outside this specification.

---

## 3. Resolution Order (Normative)

When a parser supports multiple provision mechanisms, it MUST follow this order:

1. **Explicit provision** — if caller provides schema, use it
2. **Registry lookup** — if implementation supports registry, consult it
3. **Failure** — if no schema obtained, fail with ParseError

Explicit provision always takes precedence.

---

## 4. Meta-Schema Bootstrapping (Normative)

The **meta-schema** is the schema used to parse schema documents.

### 4.1 Requirements

Every conforming implementation MUST:

* include the complete meta-schema as built-in data
* use the meta-schema when parsing schema documents

### 4.2 Detection

A document is a schema document if its root Concept is `Schema`.

When the parser encounters a root `Schema` Concept:

1. If explicit schema was provided, use it (may be meta-schema or extension)
2. Otherwise, use the built-in meta-schema

### 4.3 Rationale

This enables parsing schema documents without circular dependency. The
meta-schema is compiled into the implementation, not loaded at runtime.

---

## 5. Schema Caching (Informative)

Schemas are immutable within a version. Implementations SHOULD cache parsed
schemas to avoid redundant parsing.

Cache invalidation strategies are implementation-defined.

---

## 6. Error Handling (Normative)

### 6.1 Schema Unavailable

If no schema can be obtained through any supported mechanism:

* Error class: ParseError
* Message SHOULD indicate schema was unavailable
* Parsing MUST NOT proceed

### 6.2 Schema Load Failure

If schema resolution succeeds but loading fails (network error, file not found):

* Error class: ParseError
* Message SHOULD indicate schema could not be loaded
* Message SHOULD include the schema identifier

### 6.3 Invalid Schema

If the loaded schema is not valid Codex or not a valid schema:

* Error class: ParseError
* Message SHOULD indicate schema validation failed
* Underlying schema errors SHOULD be reported

---

## 7. Relationship to Other Specifications

* **Language Specification**: defines schema-first parsing as a core principle
* **Schema Definition Specification**: defines schema structure and ContentRules
* **Validation Error Taxonomy**: defines ParseError class

---

## 8. Non-Goals

This specification does not define:

* Schema authoring workflows
* Schema distribution mechanisms
* Schema registry protocols
* Schema versioning semantics (see Schema Versioning Specification)

---

## 9. Summary

* Parsers MUST support explicit schema provision
* Parsers MAY support schema registries
* Meta-schema is built-in for bootstrapping
* Parsing without schema is a ParseError

---

**End of Codex Schema Loading Specification v0.1**
