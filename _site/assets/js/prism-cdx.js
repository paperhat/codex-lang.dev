// assets/js/prism-cdx.js
(function (Prism) {

  /* ============================
   * Value primitives (Appendix A)
   * ============================ */

  // Tokens
  const enumToken       = /\$[A-Z][A-Za-z0-9]*/;
  const lookupToken     = /~[a-z][A-Za-z0-9]*/;

  // Strings
  const stringQuoted    = /"(?:\\.|[^\\"])*"/;
  const stringBacktick  = /`[\s\S]*?`/;

  // Characters
  const character       = /'(?:\\.|[^\\'])'/;

  // Numbers
  const infinity        = /-?Infinity\b/;
  const precisionNumber = /-?(?:0|[1-9]\d*)(?:\.\d+)?p\d+\b/;
  const scientific      = /-?(?:0|[1-9]\d*)(?:\.\d+)?[eE][+-]?\d+\b/;
  const decimal         = /-?(?:0|[1-9]\d*)\.\d+\b/;
  const integer         = /-?(?:0|[1-9]\d*)\b/;

  // Temporal
  const temporal        = /\{[^}\r\n]+\}/;

  // UUID
  const uuid            = /\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b/;

  // IRI reference
  const iri             = /\b[a-zA-Z][a-zA-Z0-9+.-]*:[^\s>]+/;

  // Colors
  const colorHex        = /#[0-9a-fA-F]{3,8}\b/;
  const colorNamed      = /&[a-z]+\b/;
  const colorFunction   = /\b(?:rgb|rgba|hsl|hsla|hwb|lab|lch|oklab|oklch|color|color-mix|device-cmyk)\([^)]*\)/i;

  // Collections (opaque but balanced)
  const list            = /\[(?:[^\[\]]|\[[^\]]*\])*\]/;
  const set             = /set\[(?:[^\[\]]|\[[^\]]*\])*\]/;
  const map             = /map\[(?:[^\[\]]|\[[^\]]*\])*\]/;
  const tuple           = /\((?:[^()]+|\([^)]*\))*\)/;

  // Ranges
  const rangeStep       = /(?:'[^']'|\{[^}]+\}|-?(?:0|[1-9]\d*)(?:\.\d+)?)(?:\.\.)(?:'[^']'|\{[^}]+\}|-?(?:0|[1-9]\d*)(?:\.\d+)?)(?:s-?(?:0|[1-9]\d*)(?:\.\d+)?)\b/;
  const range           = /(?:'[^']'|\{[^}]+\}|-?(?:0|[1-9]\d*)(?:\.\d+)?)(?:\.\.)(?:'[^']'|\{[^}]+\}|-?(?:0|[1-9]\d*)(?:\.\d+)?)\b/;

  /* ============================
   * Prism language definition
   * ============================ */

  Prism.languages.cdx = {

    /* ---------- Annotations ---------- */

    'annotation': {
      pattern: /^\s*\[[\s\S]*?\]/m,
      greedy: true
    },

    /* ---------- Markers ---------- */

    'marker': {
      pattern: /<\/?[A-Z][A-Za-z0-9]*[\s\S]*?>/,
      greedy: true,
      inside: {

        'punctuation': /^<\/?|\/?>$/,

        'concept-name': {
          pattern: /<\/?([A-Z][A-Za-z0-9]*)/,
          lookbehind: true
        },

        'trait': {
          pattern: /\b[a-z][A-Za-z0-9]*=[^\s>]+/,
          inside: {

            'trait-name': /^[a-z][A-Za-z0-9]*(?==)/,
            'operator': /=/,

            /* ---------- Trait value (flat) ---------- */

            'value': {
              pattern: /[^\s>]+$/,
              inside: {

                // Identity & reference
                'iri': iri,
                'uuid': uuid,

                // Tokens
                'enum-token': enumToken,
                'lookup-token': lookupToken,

                // Strings & chars
                'string-backtick': stringBacktick,
                'string': stringQuoted,
                'character': character,

                // Temporal
                'temporal': temporal,

                // Ranges
                'range-step': rangeStep,
                'range': range,

                // Numbers (ordered by specificity)
                'number-infinity': infinity,
                'number-precision': precisionNumber,
                'number-scientific': scientific,
                'number-decimal': decimal,
                'number-integer': integer,

                // Colors
                'color-hex': colorHex,
                'color-named': colorNamed,
                'color-function': colorFunction,

                // Collections
                'set': set,
                'map': map,
                'list': list,
                'tuple': tuple
              }
            }
          }
        }
      }
    }
  };

  Prism.languages.codex = Prism.languages.cdx;

})(Prism);

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('pre code.language-cdx').forEach(block => {
    const lines = block.innerHTML.split('\n');

    block.innerHTML = lines.map(line => {
      // One tab indent + NOT a marker, annotation, or trait
      if (
        line.startsWith('\t') &&
        !/^\t\s*(<|\[|[a-z][A-Za-z0-9]*=)/.test(line)
      ) {
        return `<span class="token content">${line}</span>`;
      }
      return line;
    }).join('\n');
  });
});
