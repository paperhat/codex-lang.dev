Status: DRAFT

# Schema Imports and Namespaces

This draft proposes a schema import mechanism that preserves strict determinism and supports composition without inheritance. It is a candidate change to the Codex specification.

## 1. Goals

- Allow schema documents to reuse Concepts and Traits from other schemas without duplication.
- Allow data documents to declare the schemas they use, so a Codex file can be self-contained.
- Make all resolution deterministic and closed-world.

## 2. New Concepts

### 2.1 SchemaImports

`SchemaImports` is a document preamble element.

- It may appear at the top level of a schema document and at the top level of a data document.
- It is unordered.
- It MUST contain one or more `SchemaImport` children.
- It is parsed before schema-directed processing and does not appear in the canonical RDF instance graph.

### 2.2 SchemaImport

`SchemaImport` declares one imported schema and its namespace.

Traits:
- `reference` (required; IRI Reference Value)
- `namespace` (required; Text Value)

Rules:
- `namespace` MUST follow the same naming rules as Trait names (camel case, no colon).
- Each `namespace` MUST be unique within the `SchemaImports` block.
- The imported schema IRI MUST resolve to exactly one schema document in the schema registry.

## 3. Namespaced References

A namespaced name is a namespace and a local name separated by a single colon.

Examples:
- `recipe:Description`
- `common:Title`

### 3.1 Namespaced Concept Names

- The local Concept name portion MUST follow Concept naming rules (Pascal case).
- A namespaced Concept name MUST resolve to a Concept definition within the imported schema bound to the namespace.

### 3.2 Namespaced Trait Names

Because importing Traits is a core use case, the draft allows namespaced Trait names.

- The local Trait name portion MUST follow Trait naming rules (camel case).
- A namespaced Trait name MUST resolve to a Trait definition within the imported schema bound to the namespace.

## 4. Strict Namespace Mode

Strict mode is REQUIRED.

When `SchemaImports` is present in a document:
- Any reference to an imported Concept or Trait MUST be namespaced.
- Unprefixed names refer only to local definitions in the current document.
- Data documents have no local definitions, so all Concept names and Trait names MUST be namespaced.
- The `id` Trait is a language-level identifier and remains unprefixed.

## 5. Resolution and Errors

Schema import resolution MUST be deterministic.

Errors (non-exhaustive):
- An imported schema IRI cannot be resolved in the registry.
- Two `SchemaImport` entries declare the same `namespace`.
- A namespaced Concept or Trait does not resolve in the referenced schema.
- A local and imported definition conflict when strict mode is violated.

## 6. Canonicalization

`SchemaImports` is unordered. Canonical order is determined by:
1. `namespace` (lexicographic, ascending)
2. `reference` (lexicographic, ascending)

## 7. Interaction with Validation

- The governing schema set for a document is the union of its local schema definitions and all imported schemas.
- SHACL derivation and validation operate over that union, but each namespaced reference resolves to exactly one definition.
- Imported schemas MUST NOT override local definitions.
- `SchemaImports` itself does not contribute nodes or triples to the instance graph.

## 8. Tooling and Registry

The schema registry is a tooling concern. It maps schema IRIs to local source paths and is not part of canonical semantics.

A conforming tool MAY accept registry configuration outside the document, but the document MUST still declare its `SchemaImports` block to be self-contained.

## 9. Open Questions

- Should namespaced Trait names be mandatory in all documents when `SchemaImports` is present, or only in schemas that import Traits?
- Should the language later support a declared default namespace for interactive authoring convenience?
