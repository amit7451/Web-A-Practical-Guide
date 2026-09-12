# -*- coding: utf-8 -*-
from helpers import esc, code_panel, callout, keypoints, compare_grid, ref_table, requirement_list, sub, part

PHASES_SVG = """<svg class="diagram" viewBox="0 0 720 200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="pArrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="var(--accent-dim)"/>
    </marker>
  </defs>
  <style>
    .pbox{ fill:var(--bg-card); stroke:var(--rule); }
    .plabel{ font-size:13px; font-weight:600; }
    .psub{ font-size:10.5px; fill:var(--ink-faint); }
    .pline{ stroke:var(--accent-dim); stroke-width:1.5; fill:none; marker-end:url(#pArrow); }
    .pband{ fill:var(--sage-soft); }
    .pband2{ fill:var(--brick-soft); }
  </style>

  <rect class="pband" x="10" y="10" width="330" height="150" rx="10"/>
  <text x="25" y="28" style="font-size:11px; fill:var(--sage);">INTERRUPTIBLE (can pause, yield, resume, or abandon)</text>

  <rect class="pband2" x="360" y="10" width="350" height="150" rx="10"/>
  <text x="375" y="28" style="font-size:11px; fill:var(--brick);">SYNCHRONOUS (runs to completion, uninterrupted)</text>

  <rect class="pbox" x="30" y="60" width="140" height="70" rx="8"/>
  <text class="plabel" x="100" y="88" text-anchor="middle">Render</text>
  <text class="psub" x="100" y="104" text-anchor="middle">call component fns,</text>
  <text class="psub" x="100" y="117" text-anchor="middle">build new tree</text>

  <path class="pline" d="M170,95 L195,95"/>

  <rect class="pbox" x="200" y="60" width="140" height="70" rx="8"/>
  <text class="plabel" x="270" y="88" text-anchor="middle">Reconcile</text>
  <text class="psub" x="270" y="104" text-anchor="middle">diff against the</text>
  <text class="psub" x="270" y="117" text-anchor="middle">previous tree</text>

  <path class="pline" d="M340,95 L385,95"/>

  <rect class="pbox" x="390" y="60" width="150" height="70" rx="8"/>
  <text class="plabel" x="465" y="88" text-anchor="middle">Commit</text>
  <text class="psub" x="465" y="104" text-anchor="middle">write real DOM</text>
  <text class="psub" x="465" y="117" text-anchor="middle">mutations</text>

  <path class="pline" d="M540,95 L565,95"/>

  <rect class="pbox" x="570" y="60" width="130" height="70" rx="8"/>
  <text class="plabel" x="635" y="88" text-anchor="middle">Effects</text>
  <text class="psub" x="635" y="104" text-anchor="middle">run useEffect /</text>
  <text class="psub" x="635" y="117" text-anchor="middle">useLayoutEffect</text>
</svg>"""

FIBER_SVG = """<svg class="diagram" viewBox="0 0 640 220" xmlns="http://www.w3.org/2000/svg">
  <style>
    .fn{ fill:var(--bg-card); stroke:var(--rule); }
    .fl{ font-size:11.5px; }
    .fedge{ stroke:var(--ink-faint); stroke-width:1.3; fill:none; }
  </style>
  <rect class="fn" x="260" y="10" width="120" height="42" rx="7"/>
  <text class="fl" x="320" y="35" text-anchor="middle">App fiber</text>

  <path class="fedge" d="M320,52 L200,96"/>
  <rect class="fn" x="140" y="98" width="120" height="42" rx="7"/>
  <text class="fl" x="200" y="123" text-anchor="middle">Header fiber</text>

  <path class="fedge" d="M320,52 L440,96"/>
  <rect class="fn" x="380" y="98" width="120" height="42" rx="7"/>
  <text class="fl" x="440" y="123" text-anchor="middle">List fiber</text>

  <path class="fedge" d="M260,140 L260,186" />
  <text x="130" y="200" style="font-size:10.5px; fill:var(--ink-faint);">child &#8595;</text>

  <path class="fedge" d="M260,119 L380,119" stroke-dasharray="3 3"/>
  <text x="290" y="112" style="font-size:10px; fill:var(--ink-faint);">sibling &#8594;</text>

  <path class="fedge" d="M200,98 L320,54" stroke-dasharray="3 3"/>
  <text x="360" y="80" style="font-size:10px; fill:var(--ink-faint);">return (parent) &#8593;</text>

  <rect class="fn" x="200" y="188" width="120" height="42" rx="7"/>
  <text class="fl" x="260" y="213" text-anchor="middle">Nav fiber</text>
</svg>"""

def build_part4():
    s1 = sub("p4-vdom-precise", "4.1", "What the Virtual DOM Actually Is, Precisely", "The real object shape", f"""
<p>Part 1.4 introduced the virtual DOM as "a lightweight object tree describing the UI." It's worth being exact
about what that object actually looks like, because the phrase "virtual DOM" invites a misleading mental image
&mdash; it is <strong>not</strong> a shadow copy of the browser's DOM API, with its own
<code class="inline">appendChild</code> methods and node types. It's dramatically simpler than that: every call
to <code class="inline">React.createElement(type, props, ...children)</code> returns a plain, ordinary JavaScript
object with a small, fixed shape:</p>

{code_panel("JavaScript", '''
// What React.createElement('h1', { className: 'title' }, 'Hello') actually returns:
{
  type: 'h1',
  key: null,
  props: {
    className: 'title',
    children: 'Hello'
  }
}
''', "element-shape.js")}

<p>That's the entire "virtual DOM node." A full component tree is just a nested structure of these plain objects
&mdash; no special class, no methods, no hidden behavior. When <code class="inline">type</code> is a string
(<code class="inline">'h1'</code>, <code class="inline">'div'</code>), it refers to a real HTML element to
eventually create. When <code class="inline">type</code> is a function (your own component), React knows to call
that function with <code class="inline">props</code> to get back <em>another</em> element tree, and keeps doing
this &mdash; calling function components and expanding their output &mdash; until every branch of the tree
bottoms out in plain host elements like <code class="inline">'div'</code> or <code class="inline">'span'</code>.</p>

{keypoints("The key reframe", [
    "“Virtual DOM” really just means “the return value of your component functions, as plain data.”",
    "Building this object tree is cheap specifically because it involves no real browser API calls — no layout, no style recalculation, no paint. It's just object allocation.",
    "This is what makes “just re-run every component function on every state change” (Part 1.1's UI = f(state)) affordable: the expensive part isn't calling your functions again, it's touching the real DOM — and that's the part reconciliation exists to minimize."
])}
""")

    s2 = sub("p4-diffing", "4.2", "The Diffing Algorithm: Type and Key Rules", "Diffing rules", f"""
<p>A fully general algorithm for finding the minimal edit distance between two arbitrary trees is
computationally expensive &mdash; on the order of O(n&sup3;) for n nodes, far too slow to run on every keystroke
in a real application. React's reconciler doesn't attempt the general case. Instead, it uses two deliberate,
documented heuristics that turn the problem into something it can solve in O(n) time, at the cost of occasionally
doing more work than a theoretically perfect diff would:</p>

{requirement_list([
    ("1", "Different element types produce different trees",
     'If the element at a given position changes type — a <code class="inline">&lt;div&gt;</code> becomes a '
     '<code class="inline">&lt;span&gt;</code>, or one component type is swapped for another — React does not '
     'try to diff their internals at all. It tears down the old subtree completely (including losing any state it '
     'held) and builds the new one from scratch.'),
    ("2", "Keys tell React which list item is which",
     "Covered from the syntax side in Part 2.6: when diffing a list of children, React uses each element's "
     '<code class="inline">key</code> to match old elements to new ones by identity, rather than assuming '
     "position N in the old list corresponds to position N in the new list."),
])}

<p>The practical consequence of rule 1 is worth seeing directly, because it explains a category of bug that looks
like a state-management problem but is really a reconciliation-rule problem:</p>

{code_panel("JSX", '''
function Panel({ isEditing }) {
  return isEditing
    ? <input defaultValue="Edit me" />
    : <div>Static text</div>;
  // Toggling isEditing swaps the element TYPE at this position (input vs div).
  // Every time this flips, React discards the old node entirely and creates
  // a fresh one — so focus, cursor position, and any uncontrolled DOM
  // state on that node is lost on every toggle, even though "conceptually"
  // it feels like the same panel just changing modes.
}
''', "type-swap.jsx")}

{callout("tip", "Same type, same position, different props — the fast path", '''
<p>When the element type at a given position stays the same across a re-render, React does the cheap thing:
it keeps the existing real DOM node and just updates the props/attributes that actually changed, leaving
everything else — including any focus, scroll position, or uncontrolled input state on that exact node
— untouched. This is reconciliation's entire value proposition in one sentence: same type, same position
= surgical update; different type = full replace.</p>
''')}
""")

    s3 = sub("p4-three-phases", "4.3", "Render, Reconciliation, and Commit: the Three Phases", "The three phases", f"""
<p>Every React update moves through three distinct phases, and knowing which phase you're in explains a lot of
otherwise-confusing rules from later Parts &mdash; including why you're never allowed to mutate the DOM or cause
other side effects directly inside a component's function body (Part 5 will lean on this directly).</p>

{PHASES_SVG}

<ul class="plain">
  <li><strong>Render.</strong> React calls your component functions to build the new element tree from Part 4.1
  and runs the Part 4.2 diff against the previous tree. This phase must be free of side effects &mdash; no DOM
  mutation, no network requests directly in the function body &mdash; because React may call your component
  function more than once per update (Part 6.2 covers exactly this, under Strict Mode), or abandon the work
  entirely without ever committing it (Part 4.5). A side effect that ran during a discarded render would have
  happened for no reason, and there'd be no way to undo it.</li>
  <li><strong>Commit.</strong> Once React has decided exactly what needs to change, it applies those changes to
  the real DOM &mdash; and this part happens synchronously, all at once, without interruption. This is
  deliberate: showing the user a half-updated page (some DOM nodes reflecting the new state, others still
  reflecting the old one) would be visibly broken, so once committing starts, React finishes it before yielding
  control back to the browser.</li>
  <li><strong>Effects.</strong> After the commit, React runs your effects (<code class="inline">useEffect</code>
  and <code class="inline">useLayoutEffect</code>, Parts 5.2 and 5.3) &mdash; this is the one place side effects
  are actually safe to perform, precisely because it only runs after real DOM changes are finalized.</li>
</ul>

{keypoints("Why the phase split matters", [
    "“Never call setState/mutate the DOM/fetch data directly in the render body” isn't an arbitrary style rule — render can run speculatively or more than once, so anything with a real-world side effect placed there could run extra times or for nothing.",
    "Commit being synchronous and uninterruptible is what guarantees you never see a flickering, half-applied UI update.",
    "Effects running strictly after commit is what makes them safe for DOM measurement, subscriptions, and data fetching — the DOM they're inspecting is guaranteed to already be up to date."
])}
""")

    s4 = sub("p4-fiber", "4.4", "Fiber: Why the Reconciler Was Rewritten", "The Fiber rewrite", f"""
<p>React's original reconciler (versions 0.3 through 15, roughly 2013&ndash;2017) walked the element tree the
straightforward way: recursively, using the JavaScript call stack itself to track "where am I in this tree."
That approach has one structural problem &mdash; a recursive walk of a big tree, once started, runs to completion.
There's no way to pause partway through a deep recursive call stack, let the browser handle an urgent event (a
keystroke, a click, a scroll), and resume exactly where you left off. For a big enough component tree, this could
block the main thread long enough to visibly drop frames or delay input handling &mdash; the exact kind of jank
React's declarative model was supposed to prevent, resurfacing at a different layer.</p>

<p>React 16 (2017) replaced that reconciler with an entirely different internal architecture called
<strong>Fiber</strong>. Instead of an implicit call stack, React builds an explicit data structure &mdash; a
"fiber" node for every element, linked to its child, its next sibling, and its parent ("return") &mdash;
that React itself walks iteratively:</p>

{FIBER_SVG}

<p>Because this traversal is now explicit data instead of the JavaScript call stack, React can stop after
completing any single fiber's "unit of work," hand control back to the browser to handle something urgent, and
resume later by simply picking up the next fiber pointer where it left off. This is what makes the render phase
in section 4.3 <strong>interruptible</strong> &mdash; and note precisely what's interruptible and what isn't:
Fiber only changes how the render phase is walked. The commit phase is still synchronous and uninterrupted, for
the visible-half-update reason covered above.</p>

{callout("history", "Same public API, entirely different engine", '''
<p>One of Fiber's more remarkable engineering achievements is that essentially none of it was visible from the
outside. Existing components, existing <code class="inline">this.setState</code> calls, existing lifecycle
methods — none of it needed to change for React 16 to ship. The entire reconciliation engine underneath
the public API was replaced without breaking the interface built on top of it, which is precisely what a
correct library/framework boundary (Part 1.3) is supposed to make possible.</p>
''')}
""")

    s5 = sub("p4-priority-lanes", "4.5", "Interruptible Rendering and Priority Lanes", "Priority “lanes”", f"""
<p>Fiber made pausing and resuming rendering <em>possible</em>; React 18 built on that foundation to make
rendering <em>priority-aware</em>, through a system internally called <strong>lanes</strong>. Not all updates
are equally urgent: a user typing into a text field needs to see each keystroke reflected essentially instantly,
while a large list re-filtering itself in response to that typing can afford to lag a frame or two behind without
the user perceiving anything wrong.</p>

<p>Lanes let React tag different updates with different priority levels and, critically, let a high-priority
update <strong>interrupt</strong> in-progress work on a lower-priority one. Concretely: if React is midway through
rendering a large, non-urgent update (marked as such via <code class="inline">startTransition</code>, covered in
full in Part 9.3) and the user types a character, React can pause the big background render, immediately process
the urgent keystroke update, show it, and then resume &mdash; or even fully restart &mdash; the interrupted
background work.</p>

<p>This is the mechanism, not just the marketing description, behind React being able to keep an interface
responsive under heavy rendering load: it isn't that React got faster at doing large updates, exactly &mdash;
it's that React got better at deciding what to do <em>first</em>, using the exact same interruptible traversal
Fiber introduced in 4.4.</p>
""")

    s6 = sub("p4-batching", "4.6", "Batching: Why Multiple setState Calls Can Become One Update", "Update batching", f"""
<p>Consider three state updates fired in a single event handler:</p>

{code_panel("JSX", '''
function handleSubmit() {
  setName('Alex');
  setEmail('alex@example.com');
  setSubmitted(true);
  // Naively, this looks like three separate state changes —
  // does the component really re-render three separate times?
}
''', "batching-example.jsx")}

<p>It does not. React <strong>batches</strong> these three calls into a single re-render, applying all three
state changes together and running the component function once with all of them already reflected. This matters
for a very concrete reason: without batching, the first <code class="inline">setState</code> call would trigger
an immediate re-render using only the new <code class="inline">name</code>, with <code class="inline">email
</code> and <code class="inline">submitted</code> still at their old values &mdash; a real, if extremely
short-lived, inconsistent intermediate state, computed and discarded three times over for one logical update.</p>

{callout("history", "Where batching's boundary used to be, and why React 18 moved it", '''
<p>Before React 18, batching only happened automatically inside React's own event handlers (an onClick, an
onChange). State updates fired inside a <code class="inline">setTimeout</code>, a native
<code class="inline">fetch().then()</code> callback, or a raw DOM event listener attached outside React's
system were <em>not</em> batched — each call triggered its own separate re-render, for reasons that had to
do with how the original event system detected "we're inside a React-managed update" versus not. React 18 made
batching automatic in all of these cases as well, closing a long-standing surprise where seemingly identical
code batched differently depending on which kind of callback it happened to run inside.</p>
''')}

{keypoints("Part 4, wrapped up", [
    "The virtual DOM is just the plain-object return value of createElement — cheap because it involves zero real browser work.",
    "Diffing uses two heuristics — same-type-same-position reuses the DOM node; different-type-same-position tears down and rebuilds — turning an expensive general tree-diff problem into a fast, predictable one.",
    "Render/reconcile is interruptible; commit is synchronous and atomic — that split is what prevents users from ever seeing a half-applied update.",
    "Fiber is the data structure that made “interruptible” possible at all, by replacing the call stack with an explicit, resumable linked structure.",
    "Batching groups multiple state updates from one logical event into a single re-render, and as of React 18 this happens consistently everywhere, not just inside React's own event handlers."
])}
""")

    body = s1 + s2 + s3 + s4 + s5 + s6
    return part("part-4", "4", "The Virtual DOM & Reconciliation",
                 "The full mechanics behind the Part 1 teaser: how React decides what actually changed, and how it stays fast while doing it.",
                 body, prev=("part-3", "Components & Composition"), nxt=("part-5", "Hooks: Mechanics and Rules"))
