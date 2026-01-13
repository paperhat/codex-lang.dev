Status: NORMATIVE
Lock State: LOCKED
Version: 0.1
Editor: Charles F. Munat

# Architect Library Contract

This document defines the **exclusive responsibilities, boundaries, and guarantees**
of the **Architect** library in Paperhat.

Architect is the **owner of meaning and structure**: it defines semantic
vocabularies (Concepts and Traits), schema authorization, **document and domain
structure**, and ontology alignment used across the Paperhat system.

This document is **Normative** and is governed by global Paperhat change control.

---

## 1. Purpose (Hard)

Architect exists to:

* define **semantic vocabularies** (Concepts and Traits) used by Codex documents
* define **schemas** that authorize which Traits may appear on which Concepts
* define **document, domain, and collection structure** (e.g. sections, lists, tables)
* define when a Concept is an **Entity** and what identity means for it
* align Concept vocabularies to **ontologies**, including schema.org where applicable
* provide the canonical semantic and structural definitions consumed by Kernel,
  Gloss, Design Policy, and renderers

Architect defines meaning and structure; it does not execute pipelines.

---

## 2. What Architect Owns (Exclusive)

Architect exclusively owns the responsibilities defined below.

---

## 2.1 Vocabulary and Schema Authorization (Hard)

Architect defines:

* which Concept names exist in a given vocabulary
* which Traits are authorized for each Concept
* which Traits are required vs optional (schema-defined)
* the schema-scoped meaning of Concepts and Traits

No other library may redefine Architect-owned vocabulary meaning.

---

## 2.2 Structural Semantics (Hard)

Architect is the **exclusive owner of structure**.

This includes, but is not limited to:

* document structure (e.g. `Article`, `Section`, `Heading`, `Sidebar`, `Appendix`)
* collections and groupings (e.g. lists, glossaries, bibliographies, references)
* tabular structure (e.g. tables, rows, cells, captions)
* block-level quotation and layout constructs
* domain-specific structural groupings

Structural Concepts:

* define containment, ordering, or hierarchy
* are **not inline**
* are **never Gloss targetable**

Gloss MAY annotate text *within* Architect-defined structures, but MUST NOT define
or replace them.

---

## 2.3 Entity Semantics (Hard)

Architect owns the definition and authorization of **Entities**.

Rules:

* A Concept is an Entity **if and only if** it declares an `id` Trait **and**
  the schema authorizes that Concept as Entity-eligible.
* Entity identity is semantic and graph-addressable.
* Entity identifiers MAY be IRIs (including colons and other IRI characters).

Architect defines which Concepts are Entity-eligible and what their identity
represents.

---

## 2.4 schema.org Coverage (Normative)

Architect MAY include schema.org-aligned vocabularies, including:

* the full schema.org class hierarchy (e.g. `Thing`, `CreativeWork`, `Event`, etc.)
* schema.org properties represented as Traits (schema-defined)

Architect owns:

* the mapping strategy from Architect Concepts/Traits to schema.org meaning
* any constraints or required properties used to form a valid schema.org entity
  representation

The schema.org hierarchy is **entirely Architect-owned**.  
Gloss may reference individual schema.org-aligned Entities via `@`, but never
defines or enumerates them.

---

## 2.5 Inline Annotation Vocabularies for Gloss (Hard)

Architect owns all **domain vocabularies** that Gloss may reference, including but
not limited to:

* semantic inline concepts (e.g. `Stress`, `Important`, `Highlight`, `Quotation`)
* temporal, numeric, color, and measurement Concepts used for “no magic values”
  authoring
* affective, cognitive, narrative, rhetorical, and performance semantics
  (open vocabulary)
* linguistic semantics (e.g. pronunciation, register, foreign terms)
* scientific, cultural, historical, and editorial inline semantics
* any additional non-HTML semantics needed for multi-target authoring

Architect defines the **meaning**, **authorized Traits**, and **Entity eligibility**
of these Concepts.

Architect does **not** define how they are rendered.

---

## 3. Architect and Gloss (Normative)

Gloss is an inline semantic annotation language that references
Architect-defined Concepts.

Architect owns the meaning, structure, and authorization of all Concepts
referenced by Gloss.

---

## 3.1 `@` vs `#` (Hard)

Architect’s Entity semantics are used by Gloss addressing rules:

* `@` references **Entities only**
* `#` references **non-Entity Concepts only**

Rules:

* Any Concept intended for inline semantic annotation (tone, emotion, narrative
  framing, linguistic nuance, numeric meaning, etc.) SHOULD be schema-defined as
  **non-Entity** and referenced via `#`.
* Concepts referenced via `@` participate in identity-based behavior such as
  metadata emission (e.g. schema.org JSON-LD), but Architect does not mandate how
  that emission occurs.

Architect is the sole authority on whether a Concept is an Entity.

---

## 3.2 Open Vocabulary Rule (Hard)

Architect MAY define open-ended families of Concepts for inline semantics,
including:

* discrete Concepts (e.g. `Sad`, `Angry`, `Dream`, `InternalDialogue`)
* structured Concepts (e.g. `Emotion`, `Tone`, `MentalState`, `NarrativeMode`)
* modifier Concepts (e.g. `WithIntent`, `WithRegister`, `WithAudience`,
  `WithContext`, `WithNuance`, `WithTone`, `WithPace`, `WithRhythm`)
* linguistic and pronunciation Concepts (e.g. `SpokenAs`, `PhoneticTranscription`)

Architect MAY support both discrete and structured forms simultaneously.

Architect MUST NOT require Gloss syntax to change to support new vocabularies.

---

## 4. Label Policy Ownership (Normative)

Architect MAY define default label strategies for Entity types.

Rules:

* Default label strategies MAY be defined per Concept type (preferred) or per
  instance (exceptional).
* Label strategies are schema-defined and target-independent.
* Design Policy MAY override label selection per target/context.
* Gloss label override (`{| label}`) is always permitted and is local to the span.

Architect defines what “label” means for a given Entity type.

---

## 5. Metadata Eligibility (Normative)

Architect defines which Entities are eligible for metadata emission (e.g.
schema.org JSON-LD) by virtue of:

* their Concept type
* their authorized Trait set
* their ontology alignment

Architect does not prescribe emission format, placement, or aggregation.
Those decisions belong to Kernel/renderers and Design Policy.

---

## 6. What Architect Does NOT Own (Hard)

Architect does **not** own:

* the CDX grammar, parsing, AST, IR, or RDF/Turtle compilation (Kernel owns)
* pipeline orchestration, storage, or query execution (Kernel owns; IO via a configured graph store adapter)
* Design Policy (authored externally; applied by Kernel)
* Presentation Plans and render outputs (Kernel + renderers)
* renderer implementation details (targets own)
* behavior, state, workflows, or event semantics
  (outside this contract)

Architect defines **meaning and structure only**.

---

## 7. Determinism and Explainability (Hard)

Architect-defined vocabulary and schema rules MUST support explainability:

* A system must be able to explain why a Trait is valid or invalid for a Concept.
* A system must be able to explain whether a Concept is Entity-eligible and why.
* A system must be able to explain the meaning of Architect-defined Concepts
  referenced by Gloss.
* A system must be able to explain whether a Concept is structural or inline and
  why it is (or is not) Gloss-addressable.

Opaque, implicit, or inferential semantics are forbidden.

---

## 8. Related Informative Material

The current, authoritative classification of Concepts across Architect and Gloss
is recorded in:

```
https://gloss-lang.dev/notes/architect-vs-gloss-concept-inventory/
```

This inventory is **informative**, not normative, but is maintained to prevent
scope drift and duplication.

---

## 9. Summary

Architect owns:

* semantic vocabularies (Concepts + Traits)
* schema authorization rules
* document and domain structure
* Entity eligibility and identity semantics
* schema.org alignment and coverage where provided
* all domain vocabularies used by Gloss for inline semantics

Architect does not own:

* parsing, compilation, storage, querying, rendering, or Design Policy application
* inline span-binding mechanics (Gloss owns)

---

**End of Architect Library Contract v0.1**
