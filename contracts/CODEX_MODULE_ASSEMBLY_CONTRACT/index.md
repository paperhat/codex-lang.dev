Status: NORMATIVE
Lock State: LOCKED
Version: 0.1
Editor: Charles F. Munat

# Codex Module Assembly Contract

This document defines **Module assemblies** in Codex.

A **Module** is a **semantic assembly** of heterogeneous Codex artifacts that together form a coherent, modular unit of the Paperhat system.

Modules are the primary unit of **composition, distribution, and reasoning** in Paperhat.

---

## 1. Purpose

This contract exists to:

* define how heterogeneous Codex artifacts are assembled into a coherent unit
* distinguish semantic assembly from domain collections and structure
* provide a stable, inspectable unit of modularity
* enable deterministic compilation and reasoning across artifacts

Modules are **semantic assemblies**, not execution units.

---

## 2. What a Module Is

A `<Module>`:

* is a **single-root Codex document**
* groups **related artifacts of different kinds**
* exists for a specific purpose (feature, domain slice, capability)
* is a first-class semantic object
* compiles to a semantic graph with explicit containment relations

Typical contents include:

* domain data
* views
* design policies
* configuration
* derived plans
* provenance

Example (Illustrative):

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

Modules do **not** replace domain collections.
A Module MAY contain domain collections, individual domain artifacts, or references to either, as authorized by schema.

---

## 3. Identity and Naming (Normative)

* Every Module **MUST** declare an `id` Trait.
* Module identifiers MUST be globally unique and namespaced.
* A Module identifier identifies the Module itself, not its contents.

Example (Illustrative):

```xml
<Module id="module:recipes">
```

---

## 4. Allowed Child Sections (Normative)

A Module MAY contain the following **structural section Concepts**, all optional unless restricted by schema:

* `<Data>` — domain individuals and collections
* `<Views>` — view specifications
* `<Policies>` — design and configuration policies
* `<Plans>` — derived artifacts (e.g. Presentation Plans)
* `<Config>` — system configuration declarations
* `<Provenance>` — authorship and derivation metadata

These section names are **structural** and have meaning only within the Module context.

They do not assert domain semantics.

---

## 5. Containment Semantics (Normative)

* All artifacts inside a Module are semantically asserted to belong to that Module.
* Containment is meaningful and MUST be represented in the semantic graph.
* Artifacts inside a Module MAY reference each other freely.

A Module MUST NOT contain:

* free text outside defined section Concepts
* mixed or ad hoc artifact groupings
* fragments not authorized by schema

---

## 6. Ordering Rules

* Lexical order of artifacts inside a Module MUST be preserved.
* Ordering has **no implicit semantic meaning** unless explicitly defined by the artifact’s schema.
* Canonical formatting MUST NOT reorder Module contents.

---

## 7. Grouping (Optional)

A Module MAY define explicit grouping Concepts for organizational or semantic purposes.

Example (Illustrative):

```xml
<Groups>
	<Group id="group:authoring">
		<Member reference="recipe:spaghetti" />
	</Group>
</Groups>
```

Rules:

* Groups are optional
* Groups contain references, not embedded artifacts
* Groups are flat (no nesting) in version 0.1

---

## 8. Provenance

A Module MAY declare provenance information.

Example (Illustrative):

```xml
<Provenance>
	<AuthoredBy reference="user:chas" />
	<GeneratedBy reference="tool:kernel" />
</Provenance>
```

Provenance is declarative, non-executable, and semantically explicit.

---

## 9. Compilation to the Semantic Graph

For a Module:

* the Module maps to a graph node of type `cdx:Module`
* contained artifacts map to their own nodes
* containment is represented via explicit predicates (e.g. `cdx:contains`)
* provenance is represented as semantic relationships, not annotations

Modules are fully queryable and reconstructable from the semantic graph.

---

## 10. Non-Goals

Modules do **not**:

* imply runtime loading or execution order
* encode imperative behavior
* replace domain collections
* act as presentation views

Modules are **semantic assemblies**, not procedural units.

---

## 11. Summary

A Module is:

* the primary modular unit of Paperhat
* a semantic assembly of heterogeneous artifacts
* explicit, inspectable, and graph-addressable
* the correct place to combine data, views, policies, plans, and provenance
