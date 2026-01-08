Status: NORMATIVE
Version: 0.1
Editor: Charles F. Munat

# Scribe Library Contract

This document defines the **exclusive responsibilities, boundaries, and guarantees** of the **Scribe** library.

Scribe is the **end-to-end pipeline** for Paperhat Codex applications.

---

## 1. Purpose (Hard)

Scribe owns the **entire Codex pipeline** as a single library, split into internal modules.

Scribe is responsible for:

- compiling CDX → AST → IR → RDF/Turtle (pure)
- storing RDF into the triple store (IO boundary via Pathfinder)
- querying the triple store with SPARQL (IO boundary via Pathfinder)
- shaping results into a **ViewModel** (pure)
- applying **Design Policy** to produce a **Presentation Plan** (pure)
- rendering Presentation Plans to:
  - DOM mutation plans (client)
  - HTML strings (SSR/SSG)
  - CDX (round-tripping)
  - SVG, LaTeX, VoiceML, and other target formats
  - JSON/XML/etc. (serialization targets)

Scribe provides a coherent, coordinated pipeline so other libraries can remain focused on their own domains.

---

## 2. What Scribe Owns (Exclusive)

Scribe exclusively owns:

---

### 2.1 Pipeline Orchestration API

Scribe defines and owns the canonical pipeline entry points and modes:

- `compile` (pure)
- `store` (IO boundary; uses Pathfinder)
- `query` (IO boundary; uses Pathfinder)
- `render` (pure)
- `run` / `execute` (optional convenience composition of the above)

Scribe owns the **contracts** for these phases, including their inputs, outputs, invariants, and phase ordering.

---

### 2.2 CDX Compilation

Scribe exclusively owns:

- CDX grammar and syntax rules
- CDX lexical validation (concept names, trait names, structure)
- AST node definitions
- IR shape and canonical normalization
- source-location tracking
- round-trip preservation metadata
- RDF/Turtle emission from IR

No other library may parse CDX or define a competing CDX → IR compiler.

---

### 2.3 ViewModel Shaping Contract

Scribe owns:

- the rule that SPARQL results are shaped into a **ViewModel**
- the stability guarantees of that ViewModel as a render input

The ViewModel is:

- structural
- target-neutral
- deterministic
- independent of rendering decisions

Domain semantics remain external; shaping is structural only.

---

### 2.4 Design Policy Application (Hard)

Scribe owns the **application of design and layout policy** as a pure planning phase.

Design Policy:

- is authored in **CDX** using a **Scribe-owned vocabulary**
- is configuration, not semantic meaning
- introduces no ontology facts
- performs no IO
- is deterministic and explainable

Scribe applies Design Policy to:

- a ViewModel and/or Concept Form IR
- a render target classification (e.g., screen, print, voice)
- declared presentation capacity context

The result is a **Presentation Plan** that is pure, deterministic, and target-neutral.

Design Policy MUST NOT invent semantic structure, modify semantic truth, encode behavior, bindings, or workflows.

---

### 2.5 Render Targets Contract

Scribe owns the definition of render targets and the requirement that rendering is pure and deterministic given:

- a Presentation Plan
- a render target
- render target configuration

Rendering is target-specific realization of a plan, not policy or semantics.

---

## 3. What Scribe Does NOT Own (Hard)

Scribe does **not** own:

- triple store implementation details (Pathfinder owns adapters)
- SPARQL language design beyond issuing queries
- ontology definitions or SHACL constraints (owned by domain libraries; enforced by Warden)
- semantic meaning or projections (Architect owns)
- application workflows or command semantics (e.g. commerce, scheduling)
- behavior modeling or execution semantics (Artificer owns)
- CQRS or event-sourcing mechanics (Operator owns)
- application state containers (Custodian owns)
- pub/sub or event transport (Operator owns)
- scaffolding, dev server, file watching (Quartermaster owns)

Scribe may **invoke** these libraries through defined interfaces, but does not subsume their responsibilities.

---

## 4. Inputs and Outputs

### 4.1 Inputs

- `.cdx` files (all configuration and authoring)
- optional pipeline configuration (authored in CDX)
- optional runtime context (render targets, portal context)

### 4.2 Outputs

- **AST** (typed, location-aware)
- **IR** (canonical, normalized)
- **RDF/Turtle triples**
- **ViewModel**
- **Presentation Plan** (internal, ephemeral)
- **Render outputs**:
  - DOM patch plans / mutations
  - HTML strings
  - CDX text
  - SVG, LaTeX, VoiceML, etc.
  - serialized formats (JSON/XML/etc.)

All pure outputs are deterministic and serializable.

---

## 5. Canonical Phase Separation (Hard)

Scribe phases are strictly separated:

### 5.1 Pure Compilation

CDX → AST → IR → RDF/Turtle

---

### 5.2 IO Boundary (via Pathfinder)

RDF → Store
Store → SPARQL → Results

---

### 5.3 Pure Shaping, Planning, and Rendering

Results → ViewModel → Presentation Plan → Render Target

No IO occurs in compilation, shaping, planning, or rendering.

---

## 6. Modes (Hard)

Scribe supports multiple execution modes.
Modes affect **which phases execute**, not their semantics.

### 6.1 Dev-A (Fast, Non-Authoritative)

- bypasses triple store IO
- uses IR → ViewModel shaping from deterministic fixtures
- applies Design Policy
- renders immediately

Dev-A is ergonomics-only. It MUST produce identical ViewModel and Presentation Plan shapes as the canonical store/SPARQL path when fed equivalent fixtures. Dev-A outputs are non-authoritative and MUST NOT be used for persistence, validation, or acceptance.

---

### 6.2 Dev-B (Safe, Local)

- uses an ephemeral/local store
- full round trip through store + SPARQL
- identical semantics to production

---

### 6.3 Test

- full round trip through a test store
- deterministic fixtures and golden outputs
- never touches production data

---

### 6.4 Prod

- full pipeline through production store
- identical semantics, different targets/config

---

## 7. Grammar and Syntax Responsibilities (Hard)

### 7.1 Concepts

- PascalCase concept names
- Multiple top-level concepts allowed
- No required root concept

### 7.2 Traits

- camelCase only
- case-sensitive
- no kebab-case
- no snake_case
- no leading underscores
- no namespace colons
- no hyphens

Canonical CDX naming rules follow `/spec/0.1/`. Traits that violate these rules are invalid and must be rejected during lexical validation.

---

## 8. Validation and "Help" (error) Handling (Hard)

### 8.1 Structural Validation Only (Compile Phase)

Scribe compile validates:

- grammar correctness
- structural correctness
- lexical correctness

Scribe compile does **not** validate:

- ontology constraints
- business rules
- workflow invariants

Those are enforced by other libraries.

---

### 8.2 Help-Only Failures

Across all phases:

- no throws
- no `null` / `undefined`
- all failures become Help (pedagogical)

---

## 9. Source Location Tracking

Scribe MUST preserve:

- UTF-16 offsets
- line number
- column number

Locations are:

- validated numeric newtypes
- attached to AST and IR nodes
- preserved through RDF emission when required
- used for diagnostics and round-tripping

---

## 10. IR and ViewModel Guarantees (Hard)

### 10.1 IR

IR MUST be:

- canonical
- normalized
- deterministic
- stable for equivalent CDX inputs (modulo location metadata)

---

### 10.2 ViewModel

ViewModel MUST be:

- deterministic for equivalent query results + configuration
- stable under equivalent semantic inputs
- independent of render target and design policy

---

## 11. Rendering (Hard)

Rendering is a pure function of:

- Presentation Plan
- render target configuration

Scribe rendering may delegate to:

- Architect for markup primitives
- Artificer for behavior attachment (optional enhancement)
- other libraries for target-specific adapters

Scribe owns render orchestration and guarantees that rendering performs no IO.

---

## 12. Toolsmith Usage (Hard)

Scribe MUST:

- use Toolsmith monads exclusively
- use Toolsmith newtypes for identifiers and locations
- use Toolsmith help infrastructure
- never inspect monad internals
- never introduce ad-hoc "help" (error) handling

Imperative code may exist **only inside Toolsmith**.

---

## 13. Folder Structure Rules

Scribe follows global folder rules:

- public API is explicit
- private implementation lives under `_` folders
- no junk-drawer folders
- lowest common ancestor rule applies

Folder structure is part of the architecture.

---

## 14. Relationship to Canonical Docs

This contract must be read in conjunction with:

- the Codex Language Specification (/spec/)
- the Codex System Contract (/contracts/CODEX_SYSTEM_CONTRACT)
- the global governance documents (/GOVERNANCE.md)

In case of conflict, **global canonical documents prevail**.
