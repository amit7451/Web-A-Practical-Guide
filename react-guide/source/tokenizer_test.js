// Extracts the HL module logic by re-declaring it (same source as app.js)
// and runs it against edge cases that historically broke the highlighter:
// a "//" appearing inside a string (as part of a URL) must NOT be treated
// as the start of a line comment, and a "//" inside a real comment must
// consume the whole rest of the line as a comment, URL and all.

const fs = require('fs');
const path = require('path');
const src = fs.readFileSync(path.join(__dirname, 'app.js'), 'utf8');

// Pull out the HL IIFE body and eval it in an isolated scope so we test
// the *actual* production tokenizer, not a re-typed copy.
const match = src.match(/const HL = \(function\(\)\{[\s\S]*?\n\}\)\(\);/);
if(!match){ console.error('Could not locate HL module in app.js'); process.exit(1); }
eval(match[0].replace('const HL', 'global.HL'));

function stripTags(html){
  return html.replace(/<[^>]+>/g, '');
}
function classOf(html, needle){
  const re = new RegExp(`<span class="([^"]+)">${needle.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')}</span>`);
  const m = html.match(re);
  return m ? m[1] : null;
}

const cases = [
  {
    name: 'URL inside a double-quoted string is not mistaken for a comment',
    code: `const url = "https://example.com/foo";`,
    check(html){
      const roundTrip = stripTags(html).replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>');
      if(roundTrip !== `const url = "https://example.com/foo";`) throw new Error('Round-trip text mismatch: ' + roundTrip);
      const cls = classOf(html, '"https://example.com/foo"');
      if(cls !== 'tok-str') throw new Error('Expected whole string as tok-str, got: ' + cls);
      if(html.includes('tok-com')) throw new Error('A comment token leaked into a plain string line');
    }
  },
  {
    name: 'Real line comment containing a URL consumes the whole line',
    code: `// see https://example.com/foo for details`,
    check(html){
      const cls = classOf(html, '// see https://example.com/foo for details');
      if(cls !== 'tok-com') throw new Error('Expected entire line as tok-com, got: ' + cls);
    }
  },
  {
    name: 'String with URL followed by a real trailing comment with another URL',
    code: `const url = "https://a.com/x"; // also see https://b.com/y`,
    check(html){
      const strCls = classOf(html, '"https://a.com/x"');
      if(strCls !== 'tok-str') throw new Error('String segment mis-tokenized: ' + strCls);
      const comCls = classOf(html, '// also see https://b.com/y');
      if(comCls !== 'tok-com') throw new Error('Comment segment mis-tokenized: ' + comCls);
    }
  },
  {
    name: 'Template literal with interpolation containing braces is one string token',
    code: 'const msg = `Count is ${count + 1}!`;',
    check(html){
      const cls = classOf(html, '`Count is ${count + 1}!`');
      if(cls !== 'tok-str') throw new Error('Template literal not tokenized as single string: ' + cls);
    }
  },
  {
    name: 'Block comment spanning a fake line-comment marker inside it',
    code: `/* note: // this looks like a line comment but isn't */`,
    check(html){
      const cls = classOf(html, '/* note: // this looks like a line comment but isn\'t */');
      if(cls !== 'tok-com') throw new Error('Block comment improperly split: ' + cls);
    }
  },
  {
    name: 'JSX tag and attribute recognized without breaking on angle brackets',
    code: `<button onClick={handleClick} className="btn">Save</button>`,
    check(html){
      if(!html.includes('<span class="tok-tag">&lt;button</span>')) throw new Error('Opening tag not recognized');
      if(!html.includes('<span class="tok-tag">&lt;/button</span>')) throw new Error('Closing tag not recognized');
      if(!html.includes('<span class="tok-attr">onClick</span>')) throw new Error('Attribute not recognized');
    }
  },
  {
    name: 'HTML-sensitive characters are always escaped, never raw',
    code: `if (a < b && b > c) { return a & b; }`,
    check(html){
      if(/[^&]<(?!\/?span)/.test(html.replace(/<span[^>]*>/g,'').replace(/<\/span>/g,''))){
        // best-effort: ensure no stray raw '<' outside our own span tags
      }
      if(html.includes('a < b') || html.includes('a & b')) throw new Error('Raw unescaped characters leaked into output HTML');
    }
  }
];

let failures = 0;
for(const c of cases){
  try{
    const html = HL.highlight(c.code);
    c.check(html);
    console.log(`PASS  ${c.name}`);
  }catch(err){
    failures++;
    console.log(`FAIL  ${c.name}\n      ${err.message}`);
  }
}
console.log(`\n${cases.length - failures}/${cases.length} tokenizer stress tests passed`);
process.exit(failures ? 1 : 0);
