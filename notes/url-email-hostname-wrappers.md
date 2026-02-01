# URL / Email / Hostname wrappers (informative)

This note records the decision to represent certain structured, canonicalized identifiers as **lexically distinct wrapper values** rather than as plain Text values.

The normative definitions live in the locked spec: `Host Name Values`, `Email Address Values`, and `URL Values`.

## Goals

- Preserve deterministic canonicalization (same input → same canonical spelling).
- Avoid accidental mixing with plain Text values.
- Keep `IriReference` semantics unchanged (still an opaque identifier).

## Wrapper spellings

- Hostname: `host("<hostname>")`
- Email: `email("<address>")`
- URL:
	- Absolute: `url("<absolute-url>")`
	- Base + relative: `url("<base-url>", "<relative-reference>")`

## Canonicalization and equality (high level)

These wrappers are intended to compare by **canonicalized** representation, not by raw input spelling.

- Hostname/domain:
	- Normalize to NFC.
	- Convert to ASCII per UTS #46 (ToASCII).
	- Lowercase the resulting ASCII hostname.

- Email:
	- Require exactly one `@`.
	- Canonicalize the domain using the hostname rules above.
	- Preserve the local part codepoint-for-codepoint (no case folding).

- URL:
	- Parse/resolve/serialize using the WHATWG URL Standard model (DOM `new URL()` semantics).
	- Two-argument form resolves relative reference against the base.
	- Canonical spelling is the serializer output.

## Tokens

These wrappers are intended to have corresponding built-in value type tokens in schema space:

- `$HostName`
- `$EmailAddress`
- `$Url`

