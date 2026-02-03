# Canonical Binary Substrate Decision (Workshop)

Workshop defines a single canonical binary interchange substrate for all internal execution, transport, caching, and WASM boundaries. This substrate is **CBOR**, encoded in **canonical form as defined by RFC 8949**. All byte-level identity, hashing, comparison, memoization, and reproducibility guarantees are defined exclusively in terms of this canonical CBOR representation.

Textual formats—including **Codex source**—are **authoring and interchange syntaxes only**. They MAY be used for configuration, properties, human-authored structure, and tool-to-tool exchange, but they MUST NOT be treated as canonical representations for execution, hashing, caching, or semantic identity.

Semantic meaning is activated only by schema-governed validation and derivation. Concrete syntaxes describe structure; the canonical CBOR substrate preserves structure deterministically; schemas define meaning. JSON is not used anywhere in Workshop.


Codex          → concrete syntax (authoring / interchange / config)  
Canonical IR   → structural model (in memory)  
CBOR           → canonical binary substrate (transport / cache / WASM boundary)  
Schema         → semantic activation (validation, derivation, meaning)
