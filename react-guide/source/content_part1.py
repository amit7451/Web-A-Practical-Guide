# -*- coding: utf-8 -*-
from helpers import esc, code_panel, callout, keypoints, compare_grid, ref_table, sub, part

DIAGRAM_SVG = """<svg class="diagram" viewBox="0 0 760 210" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="var(--accent-dim)"/>
    </marker>
  </defs>
  <style>
    .diag-box{ fill:var(--bg-card); stroke:var(--rule); stroke-width:1; rx:10; }
    .diag-label{ font-size:12px; }
    .diag-sub{ font-size:10.5px; fill:var(--ink-faint); }
    .diag-line{ stroke:var(--accent-dim); stroke-width:1.5; fill:none; marker-end:url(#arrow); }
  </style>
  <rect class="diag-box" x="10" y="70" width="130" height="64"/>
  <text class="diag-label" x="75" y="98" text-anchor="middle">State changes</text>
  <text class="diag-sub" x="75" y="114" text-anchor="middle">e.g. setCount(3)</text>

  <path class="diag-line" d="M140,102 L172,102"/>

  <rect class="diag-box" x="176" y="60" width="150" height="84"/>
  <text class="diag-label" x="251" y="94" text-anchor="middle">Component function</text>
  <text class="diag-sub" x="251" y="110" text-anchor="middle">runs again</text>
  <text class="diag-sub" x="251" y="124" text-anchor="middle">(just a JS function call)</text>

  <path class="diag-line" d="M326,102 L358,102"/>

  <rect class="diag-box" x="362" y="60" width="150" height="84"/>
  <text class="diag-label" x="437" y="94" text-anchor="middle">New UI description</text>
  <text class="diag-sub" x="437" y="110" text-anchor="middle">a plain JS object tree</text>
  <text class="diag-sub" x="437" y="124" text-anchor="middle">("virtual DOM")</text>

  <path class="diag-line" d="M512,102 L544,102"/>

  <rect class="diag-box" x="548" y="60" width="200" height="84"/>
  <text class="diag-label" x="648" y="86" text-anchor="middle">Diffed against the</text>
  <text class="diag-label" x="648" y="102" text-anchor="middle">previous description</text>
  <text class="diag-sub" x="648" y="118" text-anchor="middle">(Part 4 covers this in full)</text>

  <path class="diag-line" d="M648,144 L648,168 L 400,168 L400,168" />
  <path class="diag-line" d="M648,150 C 648,185 250,185 130,150" />
  <rect class="diag-box" x="15" y="150" width="220" height="46" />
  <text class="diag-label" x="125" y="178" text-anchor="middle">Only the real changes are</text>
  <text class="diag-sub" x="125" y="192" text-anchor="middle" style="display:none"></text>
</svg>"""

def build_part1():
    s1 = sub("p1-thesis", "1.1", "React's Core Thesis: UI as a Function of State", "UI = f(state)", f"""
<p>Strip away every implementation detail &mdash; JSX, hooks, the virtual DOM, all of it &mdash; and React reduces
to one sentence: <strong>the UI you see should be a pure, predictable output of your current data, not an
accumulated history of manual instructions.</strong> Formally, this is often written as:</p>

{code_panel("Text", "UI = f(state)", "the whole idea, in one line")}

<p>Read this the way you'd read a math function, not a metaphor. A function takes an input and returns an output;
given the same input, it always returns the same output; and it does this without caring how it got called or
what happened before. React asks you to write your UI the same way: a component is a function that takes the
current state (and props) as input, and returns a description of what the screen should look like &mdash; not a
set of steps for changing what's already there.</p>

<p>This is the direct, engineered answer to the N&times;M problem from Part 0. If the badge, the dropdown, and the
checkout total are each just functions of <code class="inline">cartItems</code>, then there is no separate
"remember to update the badge" step. There is one place cart data lives, and three functions that each say "given
this data, here's what I look like" &mdash; and something else entirely (Part 4) is responsible for noticing what
changed and updating only that.</p>
""")

    s2 = sub("p1-declarative", "1.2", "Declarative vs. Imperative, Rewriting the Badge", "Declarative vs imperative", f"""
<p>"Declarative" and "imperative" get thrown around loosely, so let's ground them in the exact cart badge example
from Part 0.3. The imperative version says <em>how</em> to get from the old screen to the new one:</p>

{code_panel("JavaScript", '''
function addToCart(item) {
  cartItems.push(item);
  document.querySelector('#badge').textContent = cartItems.length; // HOW to update
}
''', "imperative.js")}

<p>A declarative version says <em>what</em> the screen should look like, full stop, and never mentions the
previous screen at all:</p>

{code_panel("JavaScript", '''
function CartBadge({ count }) {
  return React.createElement('span', { className: 'badge' }, count); // WHAT it should look like
}
''', "declarative.js")}

<p>That second function does not know or care whether the badge previously showed <code class="inline">2</code>
or <code class="inline">200</code> or never existed at all. It only knows how to answer one question: "given a
count, what should this look like?" You call it again whenever <code class="inline">count</code> changes, and
something else &mdash; React itself &mdash; is responsible for comparing this description to whatever's actually
on the page and making the minimum number of real changes.</p>

{callout("note", "React.createElement, before JSX", '''
<p><code class="inline">React.createElement('span', { className: 'badge' }, count)</code> is real, runnable
React &mdash; and it's exactly what JSX compiles into. Part 2 introduces the <code class="inline">&lt;span
className="badge"&gt;{count}&lt;/span&gt;</code> syntax you've likely already seen, but it's worth seeing the
function-call form first: JSX has zero magic underneath it. It's markup-shaped syntax for ordinary function
calls that build plain JavaScript objects.</p>
''')}

{keypoints("The actual difference, precisely stated", [
    "Imperative code contains a reference to the *previous* state of the world (&ldquo;take what&#39;s there and change it&rdquo;). Declarative code does not — it only ever describes the *current* desired state.",
    "This is why declarative code can't accumulate drift: there's no history to get out of sync with, because nothing refers to history.",
    "The cost you accept in exchange is that *something* still has to figure out the efficient path from the old screen to the new one — that's not free, it's just no longer your problem to hand-write. That something is the reconciler (Part 4)."
])}
""")

    s3 = sub("p1-library-not-framework", "1.3", "A Library, Not a Framework &mdash; and What That Costs You", "Library vs. framework", f"""
<p>React describes itself as "a library for building user interfaces," and the word choice is deliberate and
consequential. A <strong>framework</strong> (AngularJS was one; so are Vue and Angular 2+, and, on the server,
Rails or Django) hands you an opinionated, mostly-complete set of answers for routing, data fetching, form
handling, state management, and build tooling &mdash; you work inside its structure. A <strong>library</strong>
solves one problem well and stays quiet about everything else.</p>

<p>React solves exactly one problem: turning component state into DOM updates efficiently and predictably. It
has no built-in opinion about:</p>

<ul class="plain">
  <li><strong>Routing</strong> &mdash; which URL shows which component. (You reach for React Router, or a
  framework built on React like Next.js or Remix, which bundle this in.)</li>
  <li><strong>Data fetching</strong> &mdash; how you get data from a server into state. (Plain
  <code class="inline">fetch</code>, or a library like TanStack Query, or a framework's built-in data layer.)</li>
  <li><strong>Global state management</strong> beyond what a single component tree needs. (Context, covered in
  Part 7, gets you fairly far; Redux, Zustand, and others exist for the rest.)</li>
  <li><strong>Build tooling</strong> &mdash; something still has to compile JSX into
  <code class="inline">React.createElement</code> calls and bundle your files. That's Babel and a bundler
  (Vite, webpack, etc.), not React itself.</li>
</ul>

<p>This is not a gap or an oversight &mdash; it's the entire design philosophy, and it's exactly why the React
ecosystem is large and occasionally overwhelming: you assemble the rest yourself, or you adopt a framework built
on top of React (Next.js is the most common) that makes those choices for you. Part 13 returns to this as a
genuine, honestly-stated limitation. For now, hold onto the distinction: <strong>everything this guide covers
through Part 9 is React itself.</strong> Part 10 onward starts describing decisions the wider ecosystem makes
<em>using</em> React.</p>
""")

    s4 = sub("p1-vdom-teaser", "1.4", "The Virtual DOM, in One Paragraph", "Virtual DOM (first look)", f"""
<p>You cannot get away with calling a function that rebuilds "the whole UI description" on every keystroke unless
turning that description into real DOM changes is extremely cheap. React's answer is to never touch the real DOM
directly as its first move. Instead, calling a component function produces a lightweight, plain JavaScript object
tree describing the UI &mdash; the <strong>virtual DOM</strong>. Real DOM nodes are comparatively expensive to
create and mutate (the browser has to run layout, style, and paint machinery on them); plain JS objects are
essentially free. React keeps the previous object tree around, compares it to the new one whenever state changes,
computes the minimal set of real differences, and only then touches the actual DOM &mdash; and only the parts
that actually changed.</p>

{DIAGRAM_SVG}

<p>That's the whole idea at the altitude Part 1 needs. The actual comparison algorithm, the rules about
<code class="inline">key</code> props, and the Fiber architecture that makes this interruptible for large updates
are substantial enough to deserve their own full treatment &mdash; that's all of Part 4. What matters here is the
shape of the bargain: <strong>you get to write simple, throwaway-and-redescribe code, and React does the harder
job of figuring out the cheap way to make it real.</strong></p>
""")

    s5 = sub("p1-truth-shift", "1.5", "The Shift in Where Truth Lives", "Where truth lives now", f"""
<p>Section 0.1 opened with a specific claim: in the pre-React world, the DOM itself was the only source of truth.
React inverts this completely. <strong>State is the source of truth; the DOM is a disposable, derived projection
of it that React is free to throw away and rebuild at will.</strong> You are meant to stop thinking of the
rendered page as a thing you maintain, and start thinking of it as a byproduct React generates on demand from
data you actually care about.</p>

<p>The practical, load-bearing consequence of this shift is a rule that will resurface constantly for the rest of
this guide: <strong>if you find yourself reaching for <code class="inline">document.querySelector</code> or
directly mutating a DOM node inside a React component, that is almost always a sign you're fighting the model
instead of using it.</strong> There are legitimate, narrow exceptions &mdash; focus management, text selection,
integrating a non-React library &mdash; and React provides a deliberate escape hatch for exactly those cases
(refs, covered in Part 8). But they're escape hatches precisely because the default path is supposed to be
"change the state, and let React figure out the DOM."</p>

{callout("tip", "A one-question test", '''
<p>When you're unsure whether some piece of information belongs in React state, ask: "if I threw away the
current DOM and asked a component to render fresh from scratch, would this information still be
recoverable?" If the honest answer is no &mdash; the information only exists because of some sequence of
manual DOM edits &mdash; it's a sign that information should have been state all along.</p>
''')}
""")

    s6 = sub("p1-timeline", "1.6", "How We Got From 2013 to Now", "A brief timeline", f"""
<p>React did not arrive complete and hasn't stood still since. Knowing the rough shape of its evolution will make
several later design decisions (especially around Hooks in Part 5, and rendering environments in Part 10) make
much more sense, because each major shift was a response to a specific, named limitation of what came before it.</p>

{ref_table(["Year", "Milestone", "What it actually solved"], [
    ["2013", "React open-sourced (JSConf US)", "The declarative, component-function model described in this Part, made public."],
    ["2015", "React Native announced", "The same component + reconciliation model, targeting native mobile views instead of the DOM &mdash; proof the core idea wasn't DOM-specific."],
    ["2017", "React 16: the “Fiber” rewrite", "Replaced the original reconciler with an architecture that can pause, resume, and prioritize rendering work instead of blocking the browser until a full tree diff finishes. Full mechanics in Part 4."],
    ["2019", "React 16.8: Hooks", "Let function components hold state and side effects directly, removing the need for class components for the vast majority of use cases. All of Part 5."],
    ["2022", "React 18: concurrent rendering, official", "Made Fiber's interruptible rendering something you can opt into deliberately (<code class='inline'>startTransition</code>, <code class='inline'>useDeferredValue</code>), plus automatic batching and Suspense on the server. Part 9."],
    ["2022–2023", "React Server Components popularized", "A model for rendering components on the server with zero client-side JS cost for the parts that don't need interactivity, mainstreamed through Next.js's App Router. Part 10."],
    ["2024", "React 19", "Stabilized Server Components in core, added Actions and related hooks for handling form submissions and pending/optimistic UI, and simplified ref handling."],
])}

<p>Notice the pattern: nearly every major version exists because something earlier in this list ran into a
concrete wall. Fiber exists because the original synchronous reconciler could freeze the browser on large updates.
Hooks exist because class components made sharing stateful logic between components awkward (Part 5 covers this
history in detail). Server Components exist because sending every byte of JavaScript to every client, even for
content that never changes after the server renders it, is wasteful. Nothing here is change for its own sake
&mdash; it's the same core thesis from section 1.1, re-applied every time its previous implementation revealed a
new limit.</p>

{keypoints("Part 1, wrapped up", [
    "React's core thesis is UI = f(state): components are functions from data to a description of the screen, not scripts that mutate a previous screen.",
    "It is deliberately a library, not a framework — it owns rendering and leaves routing, data fetching, and global state architecture to you or to a framework built on top of it.",
    "The virtual DOM exists to make “just redescribe everything, every time” cheap enough to actually do — full mechanics in Part 4.",
    "State is now the source of truth; the DOM is a derived, disposable output — which is why directly touching the DOM inside a component is a code smell, not a shortcut."
])}
""")

    body = s1 + s2 + s3 + s4 + s5 + s6
    return part("part-1", "1", "What React Actually Is",
                 "Not a templating language, not a framework, not magic — a specific, deliberate answer to the requirements Part 0 laid out.",
                 body, prev=("part-0", "The World Before React"), nxt=("part-2", "JSX: Syntax and Semantics"))
