Status: NORMATIVE  
Version: 0.1  
Editor: Charles F. Munat

# Codex ID Resolution Specification

This specification defines how Codex **Entity ids** are interpreted as **IRI references** and how those references are resolved to **absolute IRIs** using module-defined bases.

This document governs **ID resolution only**.
It does not define schemas, ontologies, or application semantics.

---

## 1. Purpose

Codex Entities declare an `id` Trait to establish identity.

Many consuming systems require identity to be expressed as an **absolute IRI**.
Codex therefore defines a normative mechanism to resolve string `id` values into absolute IRIs using the active module’s declared base.

Goals:

* preserve human-friendly ids (for example, slug strings)
* support deterministic graph identity
* keep Codex declarative (no evaluation, no computation beyond resolution)
* avoid global naming prefixes in authored documents

---

## 2. Core Terms (Normative)

### 2.1 IRI

An **IRI** is an Internationalized Resource Identifier, used to uniquely identify an entity.

### 2.2 IRI Reference

An **IRI Reference** is a string that may be either:

* an absolute IRI
* a relative reference intended to be resolved against a base IRI

### 2.3 Base IRI

A **Base IRI** is an absolute IRI declared by a module and used as the default base for resolving Entity ids.

---

## 3. Module Base Declaration (Normative)

### 3.1 Module Concept

A module MUST declare a `<Module>` root Concept in its `module.cdx`.

A module MAY declare one or more base traits used for ID resolution.

### 3.2 `idBase`

If present, the `idBase` Trait declares the module’s default Base IRI.

Form:

```xml
<Module idBase="https://example.test/id/some-module/" />
```

Rules:

* `idBase` MUST be a string value.
* `idBase` MUST be an absolute IRI reference (consumer-validated).
* Codex does not validate IRI syntax.

Notes:

* Consumers SHOULD require `idBase` to end with `/` for unambiguous concatenation.
* If a consumer accepts an `idBase` that does not end with `/`, it MUST still apply the resolution rules in §4.

---

## 4. ID Resolution (Normative)

### 4.1 When an `id` is resolved

A Concept is an Entity if and only if it declares an `id` Trait.

Whenever a consuming system requires an Entity’s **absolute identity**, it MUST resolve that Entity’s `id` value to an absolute IRI using this specification.

### 4.2 Inputs

Resolution requires:

* the Entity’s `id` value (a string)
* the active module’s `idBase` value (a string), if present

### 4.3 Absolute `id`

If the Entity’s `id` string is an **absolute IRI reference**, the resolved IRI is the `id` value itself.

Codex does not define the full IRI grammar; consumers decide how to recognize absolute IRIs.

### 4.4 Relative `id`

If the Entity’s `id` string is not absolute, it is a **relative IRI reference**.

If `idBase` is present, the resolved IRI is produced by resolving the relative reference against `idBase`.

Consumers MUST apply a deterministic, standards-based resolution algorithm.

Recommended algorithm:

* resolve as an IRI reference against a base IRI using standard URL/IRI resolution rules.

Codex does not modify or normalize either component.

### 4.5 Missing `idBase`

If an Entity `id` is relative and no `idBase` is available, resolution fails.

In this case, a consumer MUST report a validation error.

### 4.6 Examples

Given:

```cdx
<Module
	id="module:recipe"
	idBase="https://paperhat.dev/id/examples/recipe/"
>
	<Data />
	<Views />
	<DesignPolicies />
</Module>
```

The `<Data>`, `<Views>`, and `<DesignPolicies>` Concepts are section/role markers within the module. They do not change the resolution algorithm; they only participate to the extent that they may carry `idBase` values that scope for their subtrees.

And:

```cdx
<Recipe id="spaghetti-aglio-e-olio">
	...
</Recipe>
```

Resolved IRI:

```
https://paperhat.dev/id/examples/recipe/spaghetti-aglio-e-olio
```

---

## 5. Multiple Bases (Optional Extension)

This specification defines a single default base: `idBase`.

A module MAY define additional base traits for specialized resolution contexts.

If additional bases are defined, their selection rules MUST be specified by the governing schema or module contract.

---

## 6. Non-Goals (Normative)

This specification does not:

* require any particular IRI scheme
* require that ids be slugs, kebab-case, or any other spelling
* define whether ids must be unique (schema responsibility)
* define how ids are stored in any triple store or database
* define prefixes, CURIEs, or QName-like syntax

---

## 7. Relationship to Other Specifications (Normative)

This specification must be read in conjunction with:

- the **Codex Naming and Value Specification**
- the **Codex View Definition Specification**

In case of conflict:

- this specification is authoritative for all rules governing `id` interpretation and IRI resolution
- naming, casing, and literal spelling are governed by the Naming and Value Specification
- Views may reference resolved IRIs but do not define identity rules

---

**End of Codex ID Resolution Specification**
