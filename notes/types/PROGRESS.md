# Types audit progress (notes-only tracking)

- [x] Boolean — Surface form `true`/`false` only; consistent across spec prose, EBNF, PEG, and bootstrap schemas.
- [x] Text terminology — Eliminated Codex “string/strings” terminology across docs, notes, schemas, tools, and site assets (excluding `_site/`). Remaining `xsd:string` references in the spec are intentional external identifiers. Canonical bootstrap schema no longer uses `...XMLSchema#string` ranges.
- [x] Scalars — Scalar values/tokens are consistent and fully spelled out (`Text`/`$Text`, `Character`/`$Character`, `Boolean`/`$Boolean`); no "char" abbreviations remain.
- [x] Wrapper value kinds — Added HostName/EmailAddress/Url wrapper values to the spec and token list; propagated them into both bootstrap schemas and into Behavior notes (types, tokens, and operators).
- [x] Integer classifiers — Disallowed integer `-0`; added `Zero`/`NegativeInteger`/`NonPositiveInteger` classifications and tokens; propagated into both bootstrap schemas and Behavior notes; strict token scan passes.
