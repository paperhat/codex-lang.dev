// assets/js/prism-cdx.js
(function (Prism) {
  
  // Define reusable patterns
  const enumToken = /\$[A-Z][A-Za-z0-9]*/;
  const lookupToken = /~[a-z][A-Za-z0-9]*/;
  const temporal = /\{[^}]+\}/;
  const precisionNumber = /\b-?\d+(?:\.\d+)?p\d+\b/;
  const rangeStep = /\b.+?\.\..+?s\d+\b/;
  const range = /\b.+?\.\..+?\b/;
  const colorHex = /#[0-9a-fA-F]{3,8}\b/;
  const colorNamed = /&[a-z]+\b/;
  const stringBacktick = /`[\s\S]*?`/;
  const stringQuoted = /"(?:\\.|[^\\"])*"/;
  const character = /'(?:\\.|[^\\'])'/;
  const number = /\b-?\d+(?:\.\d+)?\b/;
  
  // Create a combined pattern for trait values
  const traitValuePattern = new RegExp(
    '(' +
    enumToken.source + '|' +
    lookupToken.source + '|' +
    temporal.source + '|' +
    precisionNumber.source + '|' +
    rangeStep.source + '|' +
    range.source + '|' +
    colorHex.source + '|' +
    colorNamed.source + '|' +
    stringBacktick.source + '|' +
    stringQuoted.source + '|' +
    character.source + '|' +
    number.source +
    ')'
  );
  
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
            'trait-name': /^[a-z][A-Za-z0-9]*(?==)/,
            'operator': /=/,
            'value': {
              pattern: /[^\s>]+$/,
              inside: {
                'enum-token': enumToken,
                'lookup-token': lookupToken,
                'temporal': temporal,
                'number-precision': precisionNumber,
                'range-step': rangeStep,
                'range': range,
                'color-hex': colorHex,
                'color-named': colorNamed,
                'string-backtick': stringBacktick,
                'string': stringQuoted,
                'character': character,
                'number': number
              }
            }
          }
        }
      }
    }
  };
  
  Prism.languages.codex = Prism.languages.cdx;
  
})(Prism);