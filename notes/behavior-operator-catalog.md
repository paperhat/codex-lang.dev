# Behavior Operator Catalog (notes-only proposal)

This document proposes a **schema-defined operator catalog** for Behavior evaluation.

Goal:
- Keep Codex core semantics simple and deterministic.
- Allow a consuming system (e.g., Workshop) to **opt in** to additional operators and behaviors (including range enumeration) without Codex “knowing” about them.

Non-goals:
- This is not a Codex spec change.
- This is not a commitment to any specific implementation language.

---

## 1. Core idea

Codex provides:
- A surface syntax and parse tree.
- A schema system with built-in value types (e.g., `$Range`, `$Integer`, `$PlainDate`).

A consuming system provides:
- A Behavior evaluator (or compiler) that executes expressions.

This proposal adds:
- A **behavior schema** layer that declares which operators exist, their type signatures, and additional execution constraints.

Outcome:
- Operators like `RangeToList` can be used **only** when explicitly permitted by the behavior schema.

---

## 2. Operator catalog as data

### 2.1 Minimum information per operator

An operator definition should include:
- `name`: operator identifier.
- `parameters`: ordered list of parameter types.
- `returns`: return type.
- `purity`: whether it may depend on runtime services.
- `requiresEnumeration`: whether the operator requires enumerating a range.
- `limits`: safety limits (max expansions, max output size, etc.).
- `domainRestrictions`: domain-specific rules needed to make semantics unambiguous.

### 2.2 Sketch (conceptual, not Codex bootstrap)

A minimal catalog shape could be represented in Codex schema-authoring terms like:

- `BehaviorOperatorCatalog`
  - `OperatorDefinition*`

- `OperatorDefinition`
  - traits:
    - `name: Text`
    - `purity: EnumeratedToken` (e.g., `$Pure`, `$ClockDependent`, `$TimeZoneDbDependent`)
    - `requiresEnumeration: Boolean`
    - `maxExpansion: Integer | Absent`
    - `maxOutputElements: Integer | Absent`
    - `maxOutputBytes: Integer | Absent`
  - children:
    - `Parameters`
    - `Returns`
    - `DomainRestrictions`

- `TypeExpression`
  - `base: ValueType` (or a token naming the type)
  - `parameters: List<TypeExpression> | Absent`

Notes:
- This is intentionally “schema-like” rather than hardcoding operator semantics into Codex.
- A consuming evaluator would load this catalog as configuration.

---

## 3. Safety and determinism rules

### 3.1 Gating

If an operator is not listed in the catalog:
- The evaluator must reject it (e.g., `Invalid([UnknownOperator])` or SchemaError at the behavior-validation boundary).

If `requiresEnumeration=true`:
- The evaluator must enforce strict limits (`maxExpansion`, `maxOutputElements`, and/or `maxOutputBytes`).
- If a limit would be exceeded, it must return `Invalid([LimitExceeded])`.

### 3.2 Determinism classes

The catalog should be able to declare whether an operator requires runtime services:
- **Pure**: deterministic, no external inputs.
- **Clock-dependent**: needs a clock.
- **Time zone DB-dependent**: needs a tz database.

A consuming system can then decide:
- whether these operators are allowed,
- and what happens if required services are unavailable.

---

## 4. Range operators as extensions

Codex-conforming tooling must not enumerate range values.
This proposal treats enumeration as an **evaluation extension** (schema-gated).

### 4.1 `RangeLength` (preferred)

Operator:
- `name = "RangeLength"`
- signature: `(Range<Integer>) → Integer`
- `requiresEnumeration = false` (implemented via arithmetic, not listing values)

DomainRestrictions (recommended):
- Endpoints must be finite integers.
- Step must be present OR default step must be explicitly defined by the catalog.
- Step must be non-zero.
- Define inclusivity rules (e.g., inclusive endpoints).
- Define empty-range rules.
- Define overflow behavior.

Limits:
- `maxResult` (optional): reject if length exceeds a cap.

Rationale:
- This is often useful for validation and for UI sizing.
- It does not inherently require producing the full member list.

### 4.2 `RangeToList` (allowed only with strict limits)

Operator:
- `name = "RangeToList"`
- signature: `(Range<Integer>) → List<Integer>`
- `requiresEnumeration = true`

DomainRestrictions (recommended):
- Endpoints must be finite integers.
- Step must be present OR default step must be explicitly defined by the catalog.
- Step must be non-zero.
- Inclusivity rules must be explicit.

Limits (required):
- `maxExpansion` / `maxOutputElements` must be set.

Rationale:
- This is inherently “potentially unbounded”, so it must be opt-in.
- The catalog makes it explicit that this is an evaluator feature, not Codex core semantics.

---

## 5. How this relates to existing notes

In the temporary Behavior notes operator tables:
- `RangeToList` and `RangeLength` currently appear, but are labeled non-conforming for Codex.

With this catalog approach:
- They can be treated as **extension operators** that a consuming system can enable.
- Codex core remains unchanged.

---

## 6. Open decisions

1. Inclusivity model for ranges used by evaluation (inclusive vs exclusive endpoints).
2. Default step semantics (require explicit step vs default step of `1`).
3. Whether non-integer ranges may be enumerated (recommended: no; restrict to integer/character only).
4. Error boundary: whether disallowed operators are SchemaError (behavior-validation) vs Invalid (evaluation).
