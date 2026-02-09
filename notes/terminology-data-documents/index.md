# Terminology: Data Documents and Schemas

This note defines terms used in the Codex ecosystem. It is informative.

## Core Terms

Data document  
A Codex document whose Concepts represent individuals in the governing schema.

Schema document  
A Codex document whose Concepts define a schema (Concept definitions, Trait definitions, constraints, value types, and validators).

Bootstrap schema  
The built-in schema-of-schemas used to validate schema documents.

Domain schema  
A schema document intended to define Concepts for data documents (for example, Recipe, Essay, Organization).

Trait bundle schema  
A domain schema whose primary purpose is to define reusable Trait definitions (for example, identity, title, language, timestamps) for composition in other schemas.

Schema import set  
A SchemaImports block that declares which schemas are in scope for a document and what namespace each schema uses.

Schema registry  
A tooling-level mapping from schema IRI to local source path. The registry is not part of canonical semantics.

## Notes

- A data document may import multiple schemas and use namespace prefixes for Concepts from imported schemas. Trait names on Concept instances remain unqualified; the Concept definition resolves which TraitDefinition each trait name refers to.
- A schema document may import other schemas for composition rather than inheritance. Schema meta-language references (`RequiresTrait`, `AllowsTrait`, `AllowsChildConcept`, etc.) use `namespace:name` to reference imported Concept and Trait definitions.
- A document remains self-contained when it declares its schema import set directly in the document.
