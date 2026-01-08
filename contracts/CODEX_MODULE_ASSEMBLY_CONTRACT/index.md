# Codex Module Assembly Contract (DRAFT)

## Status

- **DRAFT**
- Normative once locked
- Applies to mixed-artifact Codex documents rooted at `<Module>`

---

## 1. Purpose

This document defines **Module assemblies** in Codex.

A Module is a **semantic assembly** of heterogeneous Codex artifacts that together form a coherent, modular unit of the Paperhat system.

Modules are the primary unit of composition, distribution, and reasoning in Paperhat.

---

## 2. What a Module Is

A `<Module>`:

- is a **single-root Codex document**
- groups **related artifacts of different kinds**
- exists for a specific purpose (feature, domain slice, capability)
- is a first-class semantic object
- compiles to triples with explicit containment relations

Typical contents include:

- domain data
- views
- design policies
- configuration
- derived plans
- provenance

Example:

```xml
<Module id="module:recipes">
	<Data>
		<Recipe id="recipe:spaghetti">…</Recipe>
	</Data>

	<Views>
		<RecipeView id="view:recipe-default" for="Recipe">…</RecipeView>
	</Views>

	<Policies>
		<DesignPolicy id="policy:recipe:standard">…</DesignPolicy>
	</Policies>
</Module>
```

Modules do **not** replace domain collections. A Module may contain domain collections, individual domain artifacts, or references to either.

---

## 3. Identity and Naming

- Every Module **must** have an `id`.
- Module IDs must be globally unique and namespaced.
- Module IDs identify the module itself, not its contents.

Example:

```xml
<Module id="module:recipes">
```

---

## 4. Allowed Child Sections

A Module may contain the following **section concepts** (all optional unless restricted by schema):

- `<Data>` — domain individuals and collections
- `<Views>` — view specifications
- `<Policies>` — design and configuration policies
- `<Plans>` — derived artifacts (e.g. PresentationPlan)
- `<Config>` — system configuration declarations
- `<Provenance>` — authorship and derivation metadata

These section names are **structural**, not semantic domain claims.

---

## 5. Containment Semantics

- All artifacts inside a Module are semantically asserted to belong to that Module.
- Containment is meaningful and must be represented in triples.
- Artifacts inside a Module may reference each other freely.

Modules may **not** contain:

- free text outside defined sections
- domain collections that mix unrelated artifacts
- arbitrary fragments

---

## 6. Ordering Rules

- Lexical order of artifacts inside a Module is preserved.
- Ordering has **no implicit semantic meaning** unless explicitly defined by the artifact’s schema.
- Canonical formatting must never reorder Module contents.

---

## 7. Grouping (Optional)

Modules may define explicit grouping for organizational or semantic purposes:

```xml
<Groups>
	<Group id="group:authoring">
		<Member ref="recipe:spaghetti" />
	</Group>
</Groups>
```

Rules:

- Groups are optional
- Groups contain references, not embedded artifacts
- Groups are flat (no nesting) in v1

---

## 8. Provenance

Modules may declare provenance:

```xml
<Provenance>
	<AuthoredBy ref="user:chas" />
	<GeneratedBy ref="tool:scribe" />
</Provenance>
```

Provenance is declarative and non-executable.

---

## 9. Compilation to Triples

For a Module:

- the Module itself maps to a node of type `cdx:Module`
- contained artifacts map to their own nodes
- containment is represented via explicit predicates (e.g. `cdx:contains`)
- provenance is mapped as relationships, not annotations

Modules are fully queryable and reconstructable from triples.

---

## 10. Non-Goals

Modules do **not**:

- imply runtime loading or execution order
- encode imperative behavior
- replace domain collections
- act as presentation views

They are **semantic assemblies**, not procedural units.

---

## 11. Summary

A Module is:

- the primary modular unit of Paperhat
- a semantic assembly of heterogeneous artifacts
- explicit, inspectable, and graph-addressable
- the correct place to combine data, views, policies, and plans
