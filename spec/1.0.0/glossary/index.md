Status: DRAFT

# Codex Glossary

This glossary defines terms used in the Codex specification. It is informative unless a term is explicitly marked as normative.

Format notes:

- Each term is a single line entry in a definition list for easy scanning.
- Terms are added in alphabetical order.
- Definitions should be plain English and avoid specification legalese.

## Terms

<dl>
  <dt>Namespace</dt>
  <dd>A camelCase identifier that binds to an imported schema within a <code>SchemaImports</code> block. Used as a prefix in qualified names to reference Concepts and Traits from the imported schema. Each schema declares its canonical namespace via its <code>namespace</code> trait (§11.3).</dd>

  <dt>Qualified Name</dt>
  <dd>A name of the form <code>namespace:ConceptName</code> or <code>namespace:traitName</code> that references a Concept or Trait definition from an imported schema. The namespace prefix identifies the imported schema; the local name follows standard naming rules. Defined in §4.1.1.</dd>

  <dt>Schema Import</dt>
  <dd>A declaration within a <code>SchemaImports</code> block that binds a namespace label to an imported schema IRI. Each <code>SchemaImport</code> has a required <code>reference</code> trait (the schema IRI) and a required <code>namespace</code> trait (the author's label, canonicalized to the imported schema's declared namespace). Defined in §11.3.1.</dd>

  <dt>SchemaImports</dt>
  <dd>A language-level child concept permitted on any root concept (schema or data document). Contains one or more <code>SchemaImport</code> children declaring which external schemas are in scope. The governing schema's definitions are the default namespace; only imported definitions require qualified names. Defined in §11.3.1.</dd>
</dl>
