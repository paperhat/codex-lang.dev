// assets/js/prism-cdx.js
(function (Prism) {
Prism.languages.cdx = {
  'annotation': {
    pattern: /^\s*\[[\s\S]*?\]/m,
    greedy: true
  },

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
          'trait-name': /^[a-z][A-Za-z0-9]*/,
          'operator': /=/,
          'value': {
            inside: {
              // Enumerated token
              'enum-token': /\$[A-Z][A-Za-z0-9]*/,

              // Lookup token
              'lookup-token': /~[a-z][A-Za-z0-9]*/,

              // Temporal
              'temporal': /\{[^}]+\}/,

              // Precision number
              'number-precision': /\b-?\d+(\.\d+)?p\d+\b/,

              // Range with step
              'range-step': /\b.+?\.\..+?s\d+\b/,

              // Range
              'range': /\b.+?\.\..+?\b/,

              // Hex color
              'color-hex': /#[0-9a-fA-F]{3,8}\b/,

              // Named color
              'color-named': /&[a-z]+\b/,

              // Backtick string
              'string-backtick': {
                pattern: /`[\s\S]*?`/,
                greedy: true
              },

              // Quoted string
              'string': {
                pattern: /"(?:\\.|[^\\"])*"/,
                greedy: true
              },

              // Character
              'character': /'(?:\\.|[^\\'])'/,

              // Number (fallback)
              'number': /\b-?\d+(\.\d+)?\b/
            }
          }
        }
      }
    }
  }
};

Prism.languages.codex = Prism.languages.cdx;

  
})(typeof globalThis !== 'undefined' ? globalThis.Prism : typeof window !== 'undefined' ? window.Prism : undefined);



