Status: NORMATIVE  
Lock State: LOCKED    
Version: 0.1  
Editor: Charles F. Munat

# **Codex Identifier Specification — Version 0.1**

This specification defines **identifiers (`id`)** in the Codex language.

Identifiers are part of the Codex language model and are governed by this
specification.

This document is **Normative**.

---

# Codex Identifier Specification — Version 0.1

## 1. Purpose

This specification defines what an **identifier (`id`)** is in Codex.

Its goals are to:

* make identity precise and unambiguous
* ensure identifiers are globally safe and semantically meaningful
* support stable graph construction and reference
* avoid accidental coupling to storage, runtime, or transport concerns

This specification governs **identifier meaning and form**, not persistence,
resolution, or storage mechanisms.

---

## 2. What an Identifier Is

An **identifier** is a **stable, globally unique name** for an **Entity**.

In Codex:

* identifiers are **semantic**, not positional
* identifiers are **declared**, not inferred
* identifiers identify the **Entity itself**, not its representation

Identifiers are expressed exclusively via the `id` Trait.

---

## 3. Identifiers Are IRIs (Normative)

All Codex identifiers MUST be **IRIs**.

* Identifiers MUST be globally unique in intent
* Identifiers MUST be usable as graph identifiers
* Identifiers MUST be comparable as opaque strings

Codex does **not** require identifiers to be dereferenceable.

### 3.1 Surface Form Restriction (Normative)

In Codex surface form, identifier values use the **IRI reference** literal form.
This literal form requires a scheme and a ':' separator (e.g., `recipe:spaghetti`).

Codex IRI references allow the full RFC 3987 **IRI-reference** character set in surface form.
Unicode characters MAY appear directly and do not require percent-encoding.

However, to reduce ambiguity and implementation hazards, Codex identifier surface form MUST NOT contain:

* Unicode whitespace characters
* Unicode control characters
* Unicode bidirectional control characters
* Unicode private-use characters

Percent-encoding remains valid and MAY be used.

This surface form is defined by the **Formal Grammar**.

---

## 4. Identifier Form (Normative)

Codex does not mandate a single concrete syntax.
However, identifiers MUST conform to the following constraints:

* MUST be valid IRIs
* MUST NOT depend on file paths, offsets, or document structure
* MUST NOT encode ordering or position
* MUST NOT rely on implicit context for uniqueness

Codex tools MUST treat identifiers as opaque values.
Tools MUST NOT reinterpret or normalize identifier spellings beyond canonical surface form rules.

Examples (illustrative, not normative):

* `recipe:spaghetti`
* `user:chas`
* `policy:recipe:standard`

The choice of namespace scheme is a schema and project concern.

---

## 5. Stability and Immutability (Normative)

Identifiers are **stable**.

Once assigned:

* an identifier MUST continue to refer to the same Entity
* identifiers MUST NOT be reused for different Entities
* identifiers MUST NOT be repurposed

Changing an identifier creates a **new Entity**.

---

## 6. Identity vs Labels

Identifiers are **not labels**.

* Identifiers are not intended for display
* Human-readable names belong in other Traits (e.g. `name`, `title`)
* Identifiers SHOULD remain stable even if labels change

Presentation concerns MUST NOT be encoded into identifiers.

---

## 7. Relationship to References

* Reference Traits (e.g. `reference`, `target`, `for`) use either identifiers (IRIs) or lookup tokens as their values
* IRI identifiers identify Entities
* Lookup tokens (`~token`) refer to Concepts by `key`, including non-Entities

Identifiers are the mechanism by which Concepts refer to Entities.

---

## 8. Scope and Namespaces

Codex does not impose a global namespace registry.

* Projects MAY define their own namespace conventions
* Schemas SHOULD document expected identifier patterns
* Tools MUST treat identifiers as opaque values

Codex does not interpret namespace prefixes.

---

## 9. Prohibited Identifier Uses (Normative)

The following uses of identifiers are invalid:

* using identifiers as ordering keys
* embedding document structure or hierarchy
* encoding version numbers into identifiers
* using identifiers as mutable state
* auto-generating identifiers implicitly without schema authorization

Identifiers are not metadata dumps.

---

## 10. Non-Goals

This specification does **not**:

* require identifiers to resolve over HTTP
* mandate UUIDs or specific encodings
* define identifier minting workflows
* define cross-document resolution rules
* prescribe registry or catalog mechanisms

---

## 11. Summary

* Identifiers are explicit, semantic, and stable
* All identifiers are IRIs
* Identifiers identify Entities, not representations
* Schemas govern identifier usage
* Identifiers are opaque, not structural

---

**End of Codex Identifier Specification v0.1**
