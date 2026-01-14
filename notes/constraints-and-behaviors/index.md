# CONSTRAINTS_AND_BEHAVIORS (CANONICAL)

This document defines the canonical separation between **Constraints**, **Behaviors**, and **Bindings** in Paperhat Codex, including their compilation, enforcement, and target-specific resolution.

This document is **CANONICAL**.

---

## 1. Purpose

Paperhat Codex must support:

- authoritative semantic validity, independent of rendering
- optional runtime enhancement, dependent on render target and environment
- deterministic compilation from CDX into triples and internal representations
- explainability (“why is this valid / invalid?”)
- portability across render targets (DOM, HTML, PDF, LaTeX, Voice, SVG, etc.)
- strict non-JavaScript correctness

To achieve this, Codex distinguishes three concerns:

- **Constraints** — rules that define what is valid
- **Behaviors** — computations that enhance interaction but never define validity
- **Bindings** — target-specific mappings from symbolic variables to value sources

---

## 2. Definitions

### 2.1 Constraint (Authoritative)

A **constraint** is a rule that restricts what values or structures are **valid** in the semantic graph.

Constraints:

- are meaning-level (semantic truth)
- are target-independent
- are referentially transparent
- are enforceable without JavaScript
- compile to **SHACL shapes** (or an explicitly defined equivalent constraint graph)
- are explainable and traceable to source CDX
- are deterministic

Constraints define correctness.

---

### 2.2 Behavior (Non-Authoritative)

A **behavior** is a declaratively expressed computation that may execute in a runtime environment to improve user experience.

Behaviors:

- are optional
- must never be required for correctness
- may provide early feedback, guidance, or derived values
- may depend on runtime environment and render-target capabilities
- are never authoritative

Behaviors may mirror constraints but do not define them.

---

### 2.3 Binding (Target-Specific)

A **binding** maps a symbolic variable name to a value source.

Bindings:

- are authored in CDX
- are owned and resolved by **Kernel**
- are specific to an application and render target
- may reference:
  - user inputs
  - DOM attributes
  - URLs
  - storage
  - clocks
  - API responses
  - constants
  - derived computations

- are resolved at render or execution time

Bindings supply values; they do not define meaning and do not define correctness.

---

### 2.4 Source of Truth Rule (Normative)

**Constraints define correctness.
Behaviors enhance interaction.
Bindings supply values.**

No behavior or binding may redefine correctness.

---

## 3. Hard Invariants

1. Applications MUST function correctly without JavaScript.
2. Constraints MUST NOT depend on runtime-only sources.
3. Constraints MUST be referentially transparent.
4. Behaviors MUST NOT be required for correctness.
5. Bindings MUST be resolved by Kernel, not by expression logic.
6. Compilation MUST be deterministic.
7. All rules MUST be explainable.
8. No implicit inference or silent correction is permitted.

---

## 4. Referential Transparency (Critical)

A rule is **referentially transparent** if its truth value depends only on:

- values present in the semantic graph
- values derivable from the semantic graph
- declared constants or ontology-defined parameters

Constraints MUST be referentially transparent.

Constraints MUST NOT depend on:

- clocks
- cookies
- session state
- local or remote storage
- APIs
- user agents
- render state
- transient user input

Behaviors MAY depend on any of the above.

---

## 5. Vocabulary Ownership

### 5.1 Architect and Domain Libraries

Architect and other domain libraries define:

- semantic concepts and properties
- meaning-level annotations
- semantic projections (e.g. ConceptForm)
- constraint declarations authored in CDX

They define **what is valid**, not how validity is enforced.

---

### 5.2 Kernel

Kernel owns:

- compilation of CDX into triples and internal representations
- compilation of constraint declarations into SHACL shapes
- compilation of behavior declarations into behavior specifications
- resolution of all variable bindings using CDX configuration
- render orchestration for all targets

Kernel is the only component that knows the render target.

---

### 5.3 Warden

Warden enforces constraints by validating candidate graphs against compiled constraint shapes before acceptance or persistence.

---

### 5.4 Expression Evaluation

The expression evaluation layer defines:

- a declarative expression language over **named symbolic variables**
- predicate, arithmetic, and computation operators
- evaluation semantics over an explicit environment
- explainable, serializable behavior specifications

Expression evaluation:

- does not define bindings
- does not resolve bindings
- does not know render targets
- does not care where values originate

Expression evaluation evaluates expressions over provided values and never throws.

---

## 6. Canonical Data Products

### 6.1 Constraint Graph (Authoritative)

Constraints compile to a constraint graph (SHACL or equivalent) that:

- is target-independent
- is authoritative
- is stored and queryable
- is enforced by Warden and server-side validation

---

### 6.2 Behavior Specification (Non-Authoritative)

Behaviors compile to behavior specifications that:

- are serializable
- are deterministic
- may be evaluated given an environment
- may be attached to rendered output as enhancement data

---

### 6.3 Binding Configuration (Target-Specific)

Bindings compile to a binding plan that:

- maps variable names to value sources
- is specific to a render target
- is resolved by Kernel during render orchestration

---

## 7. Expressions (Plain Language)

An **expression** is a piece of CDX that produces a result.

Expressions may produce:

- a usable value
- one or more helps
- no value (explicitly modeled)

Expressions come in two primary categories:

1. **Value expressions** — produce values
2. **Relational expressions** — compare values and produce truth values

Non-lossy accumulation is required where multiple issues are possible.

---

## 8. Canonical Operator Families (CDX)

Canonical names must read like plain English.
Aliases MAY exist, but canonical documentation uses full names.

### 8.1 Logic

- `<And>`
- `<Or>`
- `<Not>`

---

### 8.2 Relational

- `<IsEqualTo>`
- `<IsNotEqualTo>`
- `<IsGreaterThan>`
- `<IsGreaterThanOrEqualTo>`
- `<IsLessThan>`
- `<IsLessThanOrEqualTo>`
- `<IsIncludedIn>`
- `<IsNotIncludedIn>`
- `<MatchesPattern>`

Child naming:

- `<Referent>` (alias: `<Left>`)
- `<Comparator>` (alias: `<Right>`)

Pattern:

- `<Pattern>` (canonical)
- `<RegularExpression>` (alias)

---

### 8.3 Arithmetic

Binary (curried):

- `<Add>` (`<Augend>`, `<Addend>`)
- `<Subtract>` (`<Minuend>`, `<Subtrahend>`)
- `<Multiply>` (`<Multiplicand>`, `<Multiplier>`)
- `<Divide>` (`<Dividend>`, `<Divisor>`)
- `<Power>` (`<Base>`, `<Exponent>`)

Unary:

- `<Negate>`
- `<AbsoluteValue>`
- `<SquareRoot>`
- `<NthRoot>`

Aggregate:

- `<Sum>`
- `<Product>`
- `<Minimum>`
- `<Maximum>`

---

### 8.4 Trigonometry

- `<Sine>`
- `<Cosine>`
- `<Tangent>`
- `<ArcSine>`
- `<ArcCosine>`
- `<ArcTangent>`
- `<DegreesToRadians>`
- `<RadiansToDegrees>`

---

### 8.5 Statistics

- `<Mean>`
- `<Median>`
- `<Mode>`
- `<Variance>`
- `<StandardDeviation>`
- `<RootMeanSquare>`
- `<Count>`

---

### 8.6 Text

- `<Concatenate>`
- `<Trim>`
- `<ToUpperCase>`
- `<ToLowerCase>`
- `<Substring>`
- `<Replace>`

---

### 8.7 Time and Date (Temporal Types)

JavaScript Date objects are not permitted.

Illustrative types:

- `<Instant>`
- `<Duration>`
- `<ZonedDateTime>`
- `<PlainDate>`
- `<PlainTime>`
- `<PlainDateTime>`

Constraints may only use Temporal relationships representable in the constraint graph.

Behaviors may bind Temporal variables to runtime clocks for enhancement only.

---

## 9. Variable Model (Critical)

### 9.1 Variables Are Placeholders

Expressions refer to **named variables**.

Variables are symbolic placeholders, not values.

---

### 9.2 Variables Are Bound by Kernel

Variables are bound exclusively by Kernel using CDX-authored binding configuration.

Expression evaluation never binds variables and never cares where bound values originate.

---

## 10. Parameterized Constraints (Critical)

### 10.1 Definition

A **parameterized constraint** is a constraint whose logical structure is fixed, but whose parameters are supplied by values present in the semantic graph or declared constants.

Parameterized constraints:

- remain referentially transparent
- are fully decidable from the graph
- compile to constraint graphs
- are enforceable without JavaScript

---

### 10.2 Allowed Parameter Sources

Parameters may come from:

- properties of the constrained individual
- properties of related individuals
- ontology-defined values
- policy or configuration individuals stored in the graph
- declared constraint-time constants

---

### 10.3 Forbidden Parameter Sources

Parameters MUST NOT come from:

- runtime inputs
- cookies or storage
- clocks
- APIs
- render state

---

### 10.4 Mirrored Behaviors

The same logical expression used in a parameterized constraint MAY be mirrored as a behavior for interactive feedback.

The difference is solely in **how variables are bound**.

---

## 11. Canonical Example (Variable-First)

Intent:

`(a < x ≤ b) OR (c ≤ x < d)`

All symbols (`x`, `a`, `b`, `c`, `d`) are variables.

- In a **constraint**, all variables must be bound to graph-resident values.
- In a **behavior**, variables may be bound by Kernel to runtime sources.

---

## 12. Prohibited Patterns (Normative)

- using behaviors as the sole source of validity
- binding variables inside expressions
- encoding runtime sources in constraints
- requiring JavaScript for correctness
- silently fixing invalid data
- using JavaScript Date objects

---

## 13. Summary

Paperhat Codex enforces a strict separation:

- **Constraints** define validity.
- **Behaviors** enhance interaction.
- **Variables** are symbolic placeholders.
- **Bindings** are target-specific and resolved by Kernel.
- **All authoring is CDX.**

> **Correctness is semantic.
> Interaction is contextual.
> Execution is optional.**

---

## Status

**CANONICAL**

This document is authoritative.
Anything not explicitly permitted is forbidden.
