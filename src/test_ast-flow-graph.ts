const CFG = require( 'ast-flow-graph' );
const fs = require( 'fs' );


const code = fs.readFileSync("./src/hello.js", 'utf8');
const cfg = new CFG(code, {
  parser:    {
      loc:          true,
      range:        true,
      comment:      true,
      tokens:       true,
      ecmaVersion:  9,
      sourceType:   'module',
      ecmaFeatures: {
          impliedStrict: true,
          experimentalObjectRestSpread: true
      }
  }
});

cfg.generate();
console.log( cfg.toTable() );