# -*- coding: utf-8 -*-
from helpers import esc, code_panel, callout, keypoints, compare_grid, ref_table, sub, part

def build_part2():
    s1 = sub("p2-not-html", "2.1", "JSX Is Not HTML", "JSX vs HTML", f"""
<p>JSX looks enough like HTML that it's easy to assume it basically <em>is</em> HTML with some JavaScript
sprinkled in. It isn't. JSX is a syntax extension to JavaScript itself that a compiler (almost always Babel, or
increasingly SWC) transforms into ordinary function calls, before any browser ever sees it. Nothing about JSX is
understood natively by any browser &mdash; by the time your code runs, the JSX is gone entirely.</p>

{code_panel("JSX", '''
function Greeting({ name }) {
  return <h1 className="title">Hello, {name}</h1>;
}
''', "Greeting.jsx")}

<p>compiles to plain JavaScript that looks like this:</p>

{code_panel("JavaScript", '''
function Greeting({ name }) {
  return React.createElement('h1', { className: 'title' }, 'Hello, ', name);
}
''', "Greeting.compiled.js")}

<p>Every rule covered in this Part exists because of that one fact: JSX has to be valid, unambiguous input to a
JavaScript expression compiler. HTML has no such constraint &mdash; it's parsed by a browser's HTML parser, which
tolerates things (unclosed tags, lowercase-only elements, attributes without quotes) that would make a JavaScript
compiler's job ambiguous or impossible. Every difference from HTML you'll meet in this Part traces back to JSX
needing to compile down to valid, well-defined function calls.</p>
""")

    s2 = sub("p2-expr-vs-stmt", "2.2", "Expressions vs. Statements Inside {}", "Expressions, not statements", f"""
<p>Curly braces in JSX are a window back into plain JavaScript &mdash; but only for <strong>expressions</strong>,
never <strong>statements</strong>. The distinction matters more than it sounds like it should, so it's worth
being precise: an expression is anything that evaluates to a single value (<code class="inline">2 + 2</code>,
<code class="inline">someFunction()</code>, <code class="inline">condition ? a : b</code>). A statement is an
instruction that does something but doesn't itself evaluate to a value (<code class="inline">if (x) {'{'} ... {'}'}</code>,
<code class="inline">for (...) {'{'} ... {'}'}</code>, a variable declaration).</p>

<p>This works, because a ternary is an expression:</p>

{code_panel("JSX", '''
<p>{isLoggedIn ? 'Welcome back' : 'Please sign in'}</p>
''', "expression-ok.jsx")}

<p>This does not compile, because an <code class="inline">if</code> block is a statement, and JSX's curly braces
compile to a function-call argument position &mdash; a slot that syntactically requires a value, not an
instruction:</p>

{code_panel("JSX", '''
<p>{if (isLoggedIn) { 'Welcome back' } else { 'Please sign in' } }</p>
// SyntaxError: cannot use an if-statement as an expression
''', "statement-fails.jsx")}

{callout("note", "The practical fix", '''
<p>When you need statement-level logic (branches, loops, intermediate variables), do it <em>before</em> the
<code class="inline">return</code>, in plain JavaScript, and only put the resulting expression inside the JSX:</p>
''')}

{code_panel("JSX", '''
function Status({ isLoggedIn }) {
  let message; // plain JS statement, lives outside JSX
  if (isLoggedIn) {
    message = 'Welcome back';
  } else {
    message = 'Please sign in';
  }
  return <p>{message}</p>; // only the resulting value goes inside {}
}
''', "fixed.jsx")}
""")

    s3 = sub("p2-compile", "2.3", "How JSX Compiles: Babel and the JSX Runtime", "Compilation pipeline", f"""
<p>Section 2.1 showed the compiled output conceptually; here's the actual pipeline. Your build tool (Vite,
webpack, Next.js's internal tooling) runs your <code class="inline">.jsx</code> or <code class="inline">.tsx</code>
files through a compiler &mdash; almost always Babel's <code class="inline">@babel/preset-react</code> plugin, or
the Rust-based SWC compiler used by newer, faster toolchains &mdash; before bundling. That compiler's only job
regarding JSX is the createElement transform shown in 2.1.</p>

<p>One historical detail worth knowing if you read older code or tutorials: before React 17, every file using JSX
needed <code class="inline">import React from 'react'</code> at the top, even if <code class="inline">React</code>
was never referenced directly in that file's own code &mdash; because the compiled output calls
<code class="inline">React.createElement</code>, and that name had to resolve to something. React 17 introduced
an <strong>automatic JSX runtime</strong> that compiles to a call to a dedicated
<code class="inline">jsx()</code>/<code class="inline">jsxs()</code> function imported automatically from
<code class="inline">react/jsx-runtime</code>, so the explicit <code class="inline">import React</code> is no
longer required purely for JSX to work. You'll see both forms in the wild; they compile to functionally
equivalent code.</p>

{keypoints("What actually matters here", [
    "JSX has no runtime existence — by the time code executes in a browser, it has already become plain function calls.",
    "The compiler's transform is mechanical and total: there is nothing JSX can express that React.createElement (or jsx()) cannot.",
    "You can always mentally “decompile” a confusing piece of JSX back into its function-call form to understand exactly what it does — this is a genuinely useful debugging habit."
])}
""")

    s4 = sub("p2-attrs", "2.4", "Attribute Differences: className, htmlFor, camelCase, and style Objects", "Attribute naming rules", f"""
<p>JSX attributes look like HTML attributes but are actually JavaScript object properties passed as the second
argument to <code class="inline">createElement</code> &mdash; and that single fact explains every naming
difference in this section.</p>

{ref_table(["HTML attribute", "JSX equivalent", "Why it's different"], [
    ['<code class="inline">class</code>', '<code class="inline">className</code>', '<code class="inline">class</code> is a reserved word in JavaScript (used to declare classes), so it cannot be used as a plain object property name in this context without friction.'],
    ['<code class="inline">for</code>', '<code class="inline">htmlFor</code>', '<code class="inline">for</code> is a reserved word (used for for-loops) for the same reason.'],
    ['<code class="inline">onclick</code>', '<code class="inline">onClick</code>', 'JSX attributes are JS object properties, and JS convention is camelCase; React also uses this to distinguish its own synthetic event system from raw DOM attributes.'],
    ['<code class="inline">tabindex</code>', '<code class="inline">tabIndex</code>', 'Same camelCase convention, applied consistently to every multi-word attribute.'],
    ["<code class='inline'>style='color: red;'</code>", "<code class='inline'>style={{ color: 'red' }}</code>", "The style attribute takes a JavaScript object (camelCased CSS properties, e.g. backgroundColor) instead of a semicolon-separated string, since it's a real JS value, not text."],
])}

<p>The <code class="inline">style</code> object deserves its own example, since its rules are easy to get
slightly wrong:</p>

{code_panel("JSX", '''
<div style={{ backgroundColor: 'crimson', fontSize: 18, marginTop: 12 }}>
  Numbers are assumed to be pixels for most properties (fontSize: 18 becomes "18px").
  Properties that don't take pixel values (like opacity or lineHeight) use bare numbers instead.
</div>
''', "style-object.jsx")}

<p>Note the double curly braces here aren't special JSX syntax &mdash; the outer
<code class="inline">{'{'}...{'}'}</code> is the normal "insert a JS expression" brace from Part 2.2, and the
inner <code class="inline">{'{'}...{'}'}</code> is just an ordinary JavaScript object literal, which happens to
be the expression being inserted.</p>

{callout("warn", "One notable exception: aria-* and data-*", '''
<p>Accessibility (<code class="inline">aria-label</code>, <code class="inline">aria-hidden</code>) and custom
data attributes (<code class="inline">data-testid</code>) keep their HTML hyphenated form exactly, rather than
being camelCased. They aren't React-managed properties with special handling like <code class="inline">
className</code> or <code class="inline">onClick</code> &mdash; React passes them straight through to the DOM
node as-is, so they keep their standard HTML names.</p>
''')}
""")

    s5 = sub("p2-children-fragments", "2.5", "Children, Fragments, and Conditional Rendering", "Children & fragments", f"""
<p>Anything nested between a component's opening and closing tags becomes available inside that component as
<code class="inline">props.children</code> (Part 3.4 covers this in depth). JSX also enforces something HTML
never requires: <strong>a component can only return a single root node.</strong> This fails to compile:</p>

{code_panel("JSX", '''
function Header() {
  return (
    <h1>Title</h1>
    <p>Subtitle</p>
  ); // SyntaxError: Adjacent JSX elements must be wrapped in an enclosing tag
}
''', "two-roots-fails.jsx")}

<p>For years the fix was wrapping everything in an extra <code class="inline">&lt;div&gt;</code>, which works but
litters the real DOM with wrapper elements that exist for no reason other than satisfying the compiler. React's
actual fix is a <strong>Fragment</strong> &mdash; a root node that groups children without rendering any DOM
element of its own:</p>

{code_panel("JSX", '''
function Header() {
  return (
    <>
      <h1>Title</h1>
      <p>Subtitle</p>
    </>
  ); // the <>...</> shorthand for React.Fragment
}
''', "fragment-fixed.jsx")}

<p>For conditional rendering, three patterns cover nearly everything you'll need:</p>

{code_panel("JSX", '''
{/* 1. Ternary — use when you have two possible outcomes */}
{isLoggedIn ? <Dashboard /> : <LoginForm />}

{/* 2. && — use when you either render something or render nothing */}
{unreadCount > 0 && <Badge count={unreadCount} />}

{/* 3. Early return — use when an entire component has a "nothing to show" case */}
function Badge({ count }) {
  if (count === 0) return null; // returning null renders nothing at all
  return <span className="badge">{count}</span>;
}
''', "conditional-patterns.jsx")}

{callout("warn", "The && number gotcha", '''
<p>Watch what happens if <code class="inline">unreadCount</code> is exactly <code class="inline">0</code> in the
<code class="inline">&&</code> example above: JavaScript's <code class="inline">&&</code> returns its left-hand
value when that value is falsy, and <code class="inline">0</code> is falsy &mdash; but <code class="inline">0
</code> is still a value React will render as literal text. The result is a stray "0" appearing on the page
instead of nothing. The fix is to force a real boolean: <code class="inline">{unreadCount > 0 && ...}</code>
(as written above) rather than <code class="inline">{unreadCount && ...}</code>.</p>
''')}
""")

    s6 = sub("p2-keys", "2.6", "Keys: What They Are and Why They're Required", "Keys in lists", f"""
<p>Whenever you render a list by mapping over an array, React requires a special <code class="inline">key</code>
prop on each resulting element:</p>

{code_panel("JSX", '''
<ul>
  {todos.map(todo => (
    <li key={todo.id}>{todo.text}</li>
  ))}
</ul>
''', "list-with-keys.jsx")}

<p>A key is not a general-purpose prop your component receives &mdash; React intercepts it and never passes it
down as <code class="inline">props.key</code>. Its only job is telling React <strong>which rendered element
corresponds to which array item, across re-renders</strong>, so that when the list changes &mdash; an item is
added, removed, or reordered &mdash; React can match old elements to new ones by identity rather than by raw
position. This is a direct preview of Part 4's diffing algorithm, which relies entirely on keys to do this
matching efficiently.</p>

{callout("warn", "Why array index is usually the wrong key", '''
<p>Using the array index (<code class="inline">todos.map((todo, i) => &lt;li key={i}&gt;)</code>) works only as
long as items are never reordered, inserted in the middle, or removed from anywhere but the end. The moment an
item is removed from the middle of a list keyed by index, every item after it shifts down by one index —
so React believes the item at, say, index 2 has simply changed its text, when in fact a completely different
todo now occupies that slot. If that list item holds its own local state (an input's current text, a checkbox's
open/closed state), that state will now appear attached to the wrong item. Use a stable, unique identifier from
your actual data (a database id, a UUID) whenever one exists.</p>
''')}
""")

    s7 = sub("p2-gotchas", "2.7", "JSX Gotchas and Edge Cases", "Gotchas & edge cases", f"""
<p>A handful of JSX behaviors are easy to trip over the first several times, precisely because they don't have
HTML equivalents to anchor your intuition:</p>

<ul class="plain">
  <li><strong>Comments need braces.</strong> HTML-style <code class="inline">&lt;!-- comment --&gt;</code>
  doesn't work inside JSX; you need <code class="inline">{'{'}/* comment */{'}'}</code>, because a comment
  inside the tag tree still has to be valid inside a JavaScript expression position.</li>
  <li><strong>Void elements must self-close.</strong> HTML tolerates <code class="inline">&lt;img&gt;</code> and
  <code class="inline">&lt;br&gt;</code> without a closing slash; JSX requires <code class="inline">&lt;img
  /&gt;</code> and <code class="inline">&lt;br /&gt;</code>, because the compiler needs an unambiguous signal
  that the element has no children, without relying on a browser's HTML-parsing leniency.</li>
  <li><strong>A typo'd attribute name fails silently.</strong> Writing <code class="inline">class="btn"</code>
  instead of <code class="inline">className="btn"</code> is not a compiler error &mdash; React simply passes an
  unrecognized <code class="inline">class</code> prop through as a plain (and, in modern React, harmless)
  attribute, but styling that depends on the actual DOM <code class="inline">class</code> attribute being set the
  "className way" can behave unexpectedly. Always reach for <code class="inline">className</code> out of habit.</li>
  <li><strong>Case sensitivity decides component vs. HTML tag.</strong> <code class="inline">&lt;Profile /&gt;
  </code> (capitalized) is compiled as a reference to your component variable; <code class="inline">&lt;profile
  /&gt;</code> (lowercase) is compiled as a literal, meaningless HTML tag string. This is precisely why the
  PascalCase naming convention for components (Part 3.1) isn't just a style preference &mdash; it's load-bearing.</li>
  <li><strong><code class="inline">dangerouslySetInnerHTML</code> exists, and its name is a warning.</strong> It
  lets you inject a raw HTML string directly, bypassing JSX's normal escaping &mdash; useful for rendering
  content from a trusted rich-text source, and a direct cross-site-scripting risk if that content ever includes
  unsanitized user input.</li>
</ul>

{keypoints("Part 2, wrapped up", [
    "JSX is compiled syntax for function calls, not a templating language — every rule in this Part exists because of that fact.",
    "Curly braces hold expressions, never statements; branch and loop before the return, then insert the resulting value.",
    "className, htmlFor, and camelCase attributes exist because JSX attributes are JavaScript object properties, and class/for are reserved words.",
    "A key's only job is letting React match array items to elements across re-renders — it is not a general-purpose prop.",
])}
""")

    body = s1 + s2 + s3 + s4 + s5 + s6 + s7
    return part("part-2", "2", "JSX: Syntax and Semantics",
                 "Markup that isn't HTML, compiling into function calls that aren't magic.",
                 body, prev=("part-1", "What React Actually Is"), nxt=("part-3", "Components & Composition"))
