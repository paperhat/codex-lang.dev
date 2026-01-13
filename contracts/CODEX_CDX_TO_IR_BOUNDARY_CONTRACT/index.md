Status: NORMATIVE
Lock State: LOCKED
Version: 0.1
Editor: Charles F. Munat

# Codex CDX → IR Boundary Contract

This document defines the **semantic and responsibility boundary** between **Codex**, authored in `.cdx` files, and the **Intermediate Representation (IR)** consumed by downstream systems (e.g. Kernel, planners, renderers, exporters).

Its requirements apply to all tooling that consumes Codex and produces an IR.

---

## 1. Purpose

This contract exists to:

* make responsibilities at the Codex → IR boundary explicit
* prevent semantic leakage across layers
* guarantee deterministic, tool-independent interpretation
* allow multiple downstream targets without reinterpreting Codex

This contract governs **what Codex guarantees to the IR**, and **what the IR MUST NOT assume**.

---

## 2. Role of Codex

Codex is a **semantic authoring language**.

Codex (as expressed in `.cdx` files) is responsible for:

* declaring **Concepts**, **Traits**, **Values**, and **Content**
* enforcing canonical surface form
* validating against schema
* enforcing identity, reference, collection, and context rules
* producing a deterministic semantic structure
* preserving all author-intended annotations

Codex defines **what exists**, not how it is rendered, stored, queried, or executed.

---

## 3. Role of the Intermediate Representation (IR)

The IR is a **normalized semantic representation** derived from Codex.

The IR exists to:

* serve as a stable interface between Codex and downstream systems
* enable compilation to multiple targets (HTML, voice, documents, APIs, etc.)
* support analysis, querying, planning, and transformation

The IR is **not authored directly** by humans and is **not a language surface**.

---

## 4. Boundary Guarantee (Normative)

A valid Codex document guarantees that:

* all Concepts are well-formed and schema-valid
* all Traits are authorized and correctly typed
* all Entities have explicit, valid identifiers
* all references point to valid Entities
* all collections obey schema-defined semantics
* all context-sensitive meanings are resolved
* all annotations are fully captured and deterministically attached

The IR MUST NOT need to re-validate Codex semantics.

---

## 5. What Codex Does Not Guarantee

Codex does **not** guarantee:

* rendering intent
* presentation structure
* layout, styling, or visual hierarchy
* execution order
* evaluation semantics
* target-specific constraints

Any such assumptions belong **strictly downstream** of the IR boundary.

---

## 6. Semantic Preservation (Normative)

The transformation from Codex to IR MUST be:

* **lossless** with respect to semantic meaning
* **lossless** with respect to annotations
* **deterministic**
* **independent of surface formatting**
* **independent of file layout or textual ordering**

The IR MUST preserve:

* Concept identity
* Trait values
* collection membership and ordering (when semantic)
* explicit relationships and references
* declared provenance
* all annotations, including their:

  * kind
  * type
  * text
  * attachment target

Nothing intentionally authored in Codex may be discarded at the boundary.

---

## 7. Content Handling

Codex **Content** is opaque.

At the Codex → IR boundary:

* Content MUST be preserved verbatim
* Content MUST NOT be interpreted or transformed
* Content MUST NOT be used to infer semantics

Downstream systems MAY choose to interpret Content, but only **after** the IR boundary.

---

## 8. Annotations (Normative)

Annotations are **first-class, non-normative semantic artifacts**.

At the Codex → IR boundary:

* All annotations MUST be preserved
* Annotation text MUST be preserved verbatim
* Annotation attachment targets MUST be explicit in the IR
* Annotation kinds MUST be preserved as typed values

Annotations:

* do **not** affect validation
* do **not** alter semantic meaning
* do **not** participate in inference
* MAY be used by downstream systems for rendering, tooling, diagnostics, or provenance

The IR MUST distinguish, at minimum:

* **Editorial annotations** (originating from `[ ... ]`)
* **Output annotations** (originating from `<Annotation>` Concepts)

This distinction MUST be preserved across the boundary.

---

## 9. Identity and References

At the Codex → IR boundary:

* Entity identity is explicit and stable
* References are resolved by identifier, not by position or structure
* No implicit relationships are introduced

The IR MUST NOT invent identity or relationships.

---

## 10. Error Responsibility

All errors in the following categories MUST be resolved **before** IR generation:

* parse errors
* surface form errors
* schema errors
* identity errors
* reference errors
* collection errors
* context errors

The IR MUST assume **error-free input**.

---

## 11. Non-Goals

This contract does **not**:

* define the structure of the IR
* mandate a specific IR format
* define triple encodings
* prescribe query languages
* define rendering pipelines

It defines **responsibility boundaries**, not implementations.

---

## 12. Summary

* Codex is authoritative for semantics **and annotations**
* The IR is authoritative for downstream processing
* The Codex → IR boundary is strict and explicit
* Semantics and annotations MUST be fully resolved before IR generation
* Downstream systems MUST NOT reinterpret Codex
