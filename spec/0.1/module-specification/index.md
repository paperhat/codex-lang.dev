Status: NORMATIVE  
Version: 0.1  
Editor: Charles F. Munat

# Codex Module Specification

This specification defines the **Module construct** in Codex, including its purpose, authorized Concepts, and the rules governing **identifier base scoping** within a module.

This document governs **module structure and base resolution only**.
It does not define schemas, domain models, or application behavior.

---

## 1. Purpose

A Codex **Module** is the unit of **semantic scope and composition**.

Modules:

* establish identity boundaries
* declare base IRIs for Entity resolution
* group related data, views, and design policies
* serve as the unit of reuse, import, and distribution

In Paperhat terminology, the module section for design and presentation policy is named `DesignPolicies`.

This specification defines:

* the `<Module>` Concept
* its authorized child Concepts
* how identifier bases (`idBase`) are declared and scoped

---

## 2. Core Concepts (Normative)

### 2.1 Module

`<Module>` is the root Concept of a module definition.

A module document MUST contain exactly one `<Module>` as its root Concept.

Example:

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

---

### 2.2 Module Identity

A `<Module>` MAY declare an `id` Trait.

If present:

* the module is an Entity
* the `id` identifies the module itself
* the interpretation of the module’s `id` is consumer-defined

The module `id` does **not** participate in Entity resolution for child Concepts.

---

## 3. Authorized Child Concepts (Normative)

A `<Module>` MAY contain the following child Concepts, in any order:

* `<Data>`
* `<Views>`
* `<DesignPolicies>`

No other child Concepts are authorized by this specification.

Each of these child Concepts establishes a **semantic section** within the module.

These section Concepts act as **role markers**: they declare which kinds of artifacts (dialects) are present in the module, and they may carry traits such as `idBase` that scope within that role.
This specification does not define the evaluation semantics of those dialects.

---

### 3.1 Data

`<Data>` contains Concepts representing **domain data**.

Examples include (non-exhaustive):

* entities
* records
* domain objects
* factual content

`<Data>` MAY be empty.

---

### 3.2 Views

`<Views>` contains Concepts representing **views over data**.

Views may include:

* projections
* presentations
* selections
* derived structures

The semantics of views are defined elsewhere.

`<Views>` MAY be empty.


---

### 3.3 Design Policies

`<DesignPolicies>` contains Concepts representing **design and presentation policy**.

Examples include:

* design policies
* styling rules
* layout guidance
The semantics of design policies are defined elsewhere.

`<DesignPolicies>` MAY be empty.

---

## 4. Identifier Base Declaration (Normative)

### 4.1 `idBase` Trait

The `idBase` Trait declares a **Base IRI** for resolving Entity ids.

Form:

```cdx
idBase="https://example.test/id/base/"
```

Rules:

* `idBase` MUST be a string value
* `idBase` MUST be an absolute IRI reference (consumer-validated)
* Codex does not validate IRI syntax

---

### 4.2 Where `idBase` May Appear

The `idBase` Trait MAY appear on:

* `<Module>`
* `<Data>`
* `<Views>`
* `<DesignPolicies>`

No other Concepts are authorized to declare `idBase`.

---

## 5. Base Scoping and Inheritance (Normative)

### 5.1 Base Scope

An `idBase` applies to:

* the Concept on which it is declared
* all descendant Concepts, unless overridden

This establishes **lexical base scoping**.

---

### 5.2 Base Resolution Order

When resolving an Entity `id`, the active Base IRI is determined as follows:

1. If the Entity itself declares an `idBase`, that base is used
2. Else, the nearest ancestor Concept declaring `idBase` is used
3. Else, the module-level `idBase` is used
4. Else, no base is available

If no base is available and the Entity `id` is relative, resolution fails.

---

### 5.3 Base Override

Declaring `idBase` on a child Concept **overrides** any inherited base for that subtree.

Example:

```cdx
<Module idBase="https://example.test/id/">
	<Data idBase="https://example.test/id/data/">
		<Thing id="x" />
	</Data>
</Module>
```

Resolved IRI for `Thing`:

```
https://example.test/id/data/x
```

---

## 6. Interaction with ID Resolution Specification (Normative)

This specification defines **where bases come from and how they scope**.

The **Codex ID Resolution Specification** defines:

* how relative and absolute `id` values are resolved
* what constitutes resolution failure

Both specifications MUST be applied together.

---

## 7. Non-Goals (Normative)

This specification does not:

* define schemas for Data, Views, or DesignPolicies
* define what constitutes a valid domain Concept
* define how modules are imported or linked
* define versioning or dependency mechanisms
* define how views or design policies are evaluated

---

## 8. Summary

* A module is defined by a single `<Module>` root Concept
* Modules may contain `<Data>`, `<Views>`, and `<DesignPolicies>`
* `idBase` declares a Base IRI for Entity id resolution
* Bases are lexically scoped and inheritable
* Child bases override parent bases
* Resolution behavior is defined jointly with the ID Resolution Specification

---

**End of Codex Module Specification**

---
