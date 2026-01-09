Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Scribe Library Contract

This document defines the **exclusive responsibilities, boundaries, and guarantees** of the **Scribe** library.

Scribe is the **end-to-end processing pipeline** for Paperhat Codex applications.

---

## 1. Purpose (Hard)

Scribe owns the **entire Codex processing pipeline** as a single library, internally composed of modules.

Scribe is responsible for:

* compiling CDX → AST → IR → RDF/Turtle (pure)
* storing RDF into a triple store (IO boundary via Pathfinder)
* querying the triple store using SPARQL (IO boundary via Pathfinder)
* shaping query results into a **ViewModel** (pure)
* applying **Design Policy** to produce a **Presentation Plan** (pure)
* rendering Presentation Plans to:

  * DOM mutation plans (client)
  * HTML strings (SSR/SSG)
  * CDX (round-tripping)
  * SVG, LaTeX, VoiceML, and other targets
  * serialized formats (JSON/XML/etc.)

Scribe provides a coordinated pipeline so other libraries remain focused on their own domains.

---

## 2. What Scribe Owns (Exclusive)

Scribe exclusively owns the responsibilities defined below.

---

### 2.1 Pipeline Orchestration API

Scribe defines and owns the pipeline entry points and execution phases:

* `compile` (pure)
* `store` (IO boundary; via Pathfinder)
* `query` (IO boundary; via Pathfinder)
* `render` (pure)
* `run` / `execute` (optional convenience composition)

Scribe owns the **contracts** governing:

* phase ordering
* inputs and outputs
* invariants
* purity and IO boundaries

---

### 2.2 CDX Compilation

Scribe exclusively owns:

* CDX grammar and syntax rules
* lexical validation (Concept names, Trait names, structure)
* AST node definitions
* IR shape and normalization rules
* source-location tracking
* round-trip preservation metadata
* RDF/Turtle emission from IR

No other library may parse CDX or define an alternative CDX → IR compiler.

---

### 2.3 ViewModel Shaping

Scribe owns the rule that SPARQL query results are shaped into a **ViewModel**.

The ViewModel is:

* structural
* target-neutral
* deterministic
* independent of rendering and design decisions

Scribe shapes structure only; **semantic meaning remains external**.

---

### 2.4 Design Policy Application (Hard)

Scribe owns the **application** of Design Policy as a pure planning phase.

Design Policy:

* is authored in **CDX**
* uses a **Scribe-defined vocabulary**
* is configuration, not semantic meaning
* introduces no ontology facts
* performs no IO
* is deterministic and explainable

Scribe applies Design Policy to:

* a ViewModel and/or Concept-form IR
* a render-target classification (e.g. screen, print, voice)
* declared presentation-capacity context

The result is a **Presentation Plan** that is:

* pure
* deterministic
* target-neutral

Design Policy MUST NOT invent structure, modify semantic truth, encode behavior, bindings, or workflows.

---

### 2.5 Render Targets

Scribe owns the definition of render targets and the requirement that rendering is pure and deterministic given:

* a Presentation Plan
* a render target
* render-target configuration

Rendering is realization of a plan, not policy or semantics.

---

## 3. What Scribe Does NOT Own (Hard)

Scribe does **not** own:

* triple-store implementations (Pathfinder owns adapters)
* SPARQL language design
* ontologies or SHACL constraints (domain libraries; enforced by Warden)
* semantic meaning or projections (Architect owns)
* application workflows or commands
* behavior modeling or execution semantics (Artificer owns)
* CQRS or event-sourcing mechanics (Operator owns)
* application state containers (Custodian owns)
* pub/sub or transport (Operator owns)
* scaffolding, dev server, file watching (Quartermaster owns)

Scribe may **invoke** other libraries via defined interfaces but does not subsume their responsibilities.

---

## 4. Inputs and Outputs

### 4.1 Inputs

* `.cdx` files (all authoring and configuration)
* optional pipeline configuration (authored in CDX)
* optional runtime context (render targets, portal context)

### 4.2 Outputs

* AST (typed, location-aware)
* IR (normalized, deterministic)
* RDF/Turtle triples
* ViewModel
* Presentation Plan (internal, ephemeral)
* Render outputs:

  * DOM mutation plans
  * HTML strings
  * CDX text
  * SVG, LaTeX, VoiceML
  * serialized formats

All pure outputs are deterministic and serializable.

---

## 5. Phase Separation (Hard)

Scribe phases are strictly separated.

### 5.1 Pure Compilation

CDX → AST → IR → RDF/Turtle

---

### 5.2 IO Boundary (via Pathfinder)

RDF → Store
Store → SPARQL → Results

---

### 5.3 Pure Shaping, Planning, and Rendering

Results → ViewModel → Presentation Plan → Render Output

No IO occurs outside the IO boundary.

---

## 6. Execution Modes (Hard)

Modes affect **which phases execute**, not semantics.

### 6.1 Dev-A (Fast, Non-Authoritative)

* bypasses store IO
* uses deterministic fixtures
* applies Design Policy
* renders immediately

Dev-A is ergonomics-only and MUST NOT be used for persistence or acceptance.

---

### 6.2 Dev-B (Safe, Local)

* full round-trip through local/ephemeral store
* semantics identical to production

---

### 6.3 Test

* deterministic fixtures and golden outputs
* never touches production data

---

### 6.4 Production

* full pipeline through production store
* identical semantics; different configuration

---

## 7. Grammar and Syntax Responsibilities (Hard)

### 7.1 Concepts

* PascalCase names
* Multiple top-level Concepts permitted
* Root requirements are schema-defined, not grammatical

### 7.2 Traits

* camelCase only
* case-sensitive
* no kebab-case, snake_case, colons, hyphens, or leading underscores

Invalid Traits MUST be rejected during lexical validation.

---

## 8. Validation and Help Handling (Hard)

### 8.1 Compile-Phase Validation

Scribe validates:

* grammar
* structure
* lexical correctness

Scribe does **not** validate:

* ontology constraints
* business rules
* workflows

---

### 8.2 Help-Only Failures

Across all phases:

* no throws
* no `null` / `undefined`
* all failures are Help values

---

## 9. Source Location Tracking

Scribe MUST preserve:

* UTF-16 offsets
* line numbers
* column numbers

Locations are validated newtypes attached to AST and IR nodes.

---

## 10. IR and ViewModel Guarantees (Hard)

### 10.1 IR

IR MUST be:

* normalized
* deterministic
* stable for equivalent CDX inputs (modulo location metadata)

---

### 10.2 ViewModel

ViewModel MUST be:

* deterministic
* stable for equivalent semantic inputs
* independent of render target and Design Policy

---

## 11. Rendering (Hard)

Rendering is a pure function of:

* Presentation Plan
* render-target configuration

Rendering performs no IO.

---

## 12. Toolsmith Usage (Hard)

Scribe MUST:

* use Toolsmith monads exclusively
* use Toolsmith newtypes for identifiers and locations
* use Toolsmith Help infrastructure
* never inspect monad internals
* never introduce ad-hoc error handling

Imperative code exists **only inside Toolsmith**.

---

## 13. Folder Structure Rules

Scribe follows global folder rules:

* explicit public API
* private implementation under `_` folders
* no junk-drawer folders
* lowest-common-ancestor rule applies

Folder structure is architectural.

---

## 14. Relationship to Higher-Authority Documents

This contract must be read in conjunction with:

* the Codex Language Specification (`/spec/`)
* the Codex System Contract
* global governance documents

In case of conflict, **higher-authority documents prevail**.

---

**End of Scribe Library Contract v0.1**
