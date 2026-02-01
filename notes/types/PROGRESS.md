# Types audit progress (notes-only tracking)

- [x] Boolean — Surface form `true`/`false` only; consistent across spec prose, EBNF, PEG, and bootstrap schemas.
- [x] Text terminology — Eliminated Codex “string/strings” terminology across docs, notes, schemas, tools, and site assets (excluding `_site/`). Remaining `xsd:string` references in the spec are intentional external identifiers. Canonical bootstrap schema no longer uses `...XMLSchema#string` ranges.
- [x] Scalars — Scalar values/tokens are consistent and fully spelled out (`Text`/`$Text`, `Character`/`$Character`, `Boolean`/`$Boolean`); no "char" abbreviations remain.
- [x] Wrapper value kinds — Added HostName/EmailAddress/Url wrapper values to the spec and token list; propagated them into both bootstrap schemas and into Behavior notes (types, tokens, and operators).
- [x] Integer classifiers — Disallowed integer `-0`; added `Zero`/`NegativeInteger`/`NonPositiveInteger` classifications and tokens; propagated into both bootstrap schemas and Behavior notes; strict token scan passes.

- [x] Real numbers edge cases — Confirmed `0` is permitted; confirmed `-0.0` is permitted; kept integer `-0` invalid; added conformance fixtures to lock this down.
- [x] Infinity — Added conformance for `Infinity`/`-Infinity` and updated the notes’ numeric ordering domains so ordering/statistics/sorting operators accept infinities where appropriate.
- [x] Collections — Audited List/Set/Map/Tuple/Range/Record rules; added conformance fixtures for set element uniqueness, map key uniqueness (including key-kind collisions), and acceptance of multiple key kinds.
- [x] Canonical order preservation — Added conformance demonstrating canonical output preserves literal order even when a collection is semantically unordered.
- [x] Ranges — Added conformance for character and temporal ranges; clarified in notes that ranges are declarative and must not be enumerated by core evaluation.
- [x] Temporals (lexical + semantic) — Added conformance fixtures covering major temporal spellings; updated notes to state schema-driven conversion produces concrete runtime temporal types and conversion failures are SchemaError.
- [x] TemporalKeyword pass-through — Clarified that `{now}`/`{today}` remain unevaluated `TemporalKeyword` values until rendering/consumption; tightened temporal operator signatures to require deterministic temporals for arithmetic/comparison and allow keywords only for formatting.

- [x] Colors (Batch 1: full surface grammar) — Drafted a deterministic conversion-based semantic validity rule with mandated `p=256` binary floating-point arithmetic (ties-to-even), correctly-rounded trig, and a single mandated dot-product procedure for all matrix multiplies; explicit constants; no clamping/normalization/hue wrapping. Appendix A now specifies explicit argument grammar (EBNF + PEG) for all currently-listed color function spellings: `rgb(...)`/`rgba(...)`, `hsl(...)`/`hsla(...)`, `hwb(...)`, `lab(...)`, `lch(...)`, `oklab(...)`, `oklch(...)`, `color(...)`, `color-mix(...)`, `device-cmyk(...)`, and relative `from <color>` forms.
