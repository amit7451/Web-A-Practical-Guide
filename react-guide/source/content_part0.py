# -*- coding: utf-8 -*-
from helpers import esc, code_panel, callout, keypoints, compare_grid, requirement_list, sub, part

def build_part0():
    s1 = sub("p0-dom-truth", "0.1", "The DOM Was the Only Source of Truth", "The DOM as source of truth", f"""
<p>Before you can appreciate what React changed, you have to sit inside the world it was built to escape. In that
world, there was exactly one place your application's truth lived: the browser's live DOM tree. Not a JavaScript
variable, not a data model, not a store &mdash; the actual rendered nodes on the page. If you wanted to know
"what does the user currently see," the honest answer was: whatever <code class="inline">document</code> says
right now.</p>

<p>The entire toolkit for building an interactive page was three primitives, used directly:</p>

<ul class="plain">
  <li><code class="inline">document.querySelector</code> / <code class="inline">getElementById</code> &mdash; find a node</li>
  <li><code class="inline">element.innerHTML</code> / <code class="inline">textContent</code> &mdash; mutate a node</li>
  <li><code class="inline">element.addEventListener</code> &mdash; react to something the user did</li>
</ul>

<p>Here is a complete, working counter built from nothing but those three tools:</p>

{code_panel("JavaScript", '''
let count = 0;

const countLabel = document.querySelector('#count');
const incrementBtn = document.querySelector('#increment');

incrementBtn.addEventListener('click', () => {
  count = count + 1;
  countLabel.textContent = count; // you must remember to do this
});
''', "counter.js")}

<p>Read that last line again: <code class="inline">countLabel.textContent = count</code>. Nothing about the
language or the browser enforces that this line exists. <code class="inline">count</code> is just a number
sitting in memory; the on-screen text is a <em>separate</em> piece of state that happens to currently agree with
it, because a human being remembered to write the synchronization by hand. The moment you forget that line, or
write it in the wrong order, or attach it to the wrong button, the number in memory and the number on screen
silently diverge. The page will look wrong, but nothing will throw an error, because nothing was ever wired to
guarantee they matched in the first place.</p>

<p>This is not a criticism of the programmers who worked this way &mdash; it's a description of the only model
available. HTML gave you a document. JavaScript gave you a way to poke at that document. Keeping the poking
consistent with your data was entirely your job, every single time, everywhere your data was displayed.</p>
""")

    s2 = sub("p0-jquery", "0.2", "jQuery Solved the Browser, Not the Architecture", "jQuery's real contribution", f"""
<p>By the mid-2000s, the practical pain of front-end development wasn't really "how do I update the DOM" &mdash;
it was "how do I update the DOM without Internet Explorer 6 throwing a different error than Firefox, on an API
that Netscape and Microsoft had implemented slightly differently on purpose." <strong>jQuery's actual
contribution was cross-browser normalization</strong>: one consistent API for selecting elements, binding
events, making AJAX requests, and animating properties, that quietly papered over years of incompatible browser
quirks.</p>

{code_panel("JavaScript", '''
$('#increment').on('click', function () {
  count = count + 1;
  $('#count').text(count);
});
''', "counter.jquery.js")}

<p>Notice what did <em>not</em> change: this is the exact same shape of program as the vanilla version. Find a
node, mutate a node, on an event. jQuery made each of those three operations shorter and more reliable across
browsers &mdash; a genuinely huge win for its time &mdash; but it did nothing to change the underlying
architecture. You still had to know, by memory, every place in the DOM that reflected a piece of state, and you
still had to write an explicit statement to update each one, by hand, forever.</p>

{callout("history", "Worth Remembering", '''
<p>jQuery is frequently mocked in retrospect as "the old, bad way to build web apps." That's an unfair
reading of history. jQuery solved a real and painful problem &mdash; browser incompatibility &mdash;
extremely well. It simply wasn't trying to solve the problem React was later built for. Judging jQuery
by React's goals is judging a hammer for not being a screwdriver.</p>
''')}
""")

    s3 = sub("p0-nxm", "0.3", "The N × M Synchronization Problem", "The N×M problem", f"""
<p>The real trouble doesn't show up in a counter demo. It shows up once an application has more than one piece
of state, displayed in more than one place. Consider a shopping cart. As the app grows, "how many items are in
the cart" ends up rendered in the header badge, in a mini-cart dropdown, and in the checkout summary &mdash;
three places, and counting.</p>

{code_panel("JavaScript", '''
let cartItems = [];

function addToCart(item) {
  cartItems.push(item);

  updateHeaderBadge();       // update #1: the little number by the cart icon
  updateMiniCartDropdown();  // update #2: the preview list when you hover the icon
  updateCheckoutTotal();     // update #3: the running total on the checkout page
  // ...and whichever future feature also happens to display cart data,
  // whoever builds it must remember to call their own update function here too.
}

function removeFromCart(itemId) {
  cartItems = cartItems.filter(i => i.id !== itemId);

  updateHeaderBadge();       // ...and all three calls have to be repeated here.
  updateMiniCartDropdown();  // If you edit one function's list and forget the
  updateCheckoutTotal();     // other, the two call sites now silently disagree.
}
''', "cart.js")}

<p>Generalize this and you get the actual technical shape of "spaghetti code": if a codebase has <strong>N</strong>
places that change some piece of state and <strong>M</strong> places that display it, a fully correct
implementation needs on the order of <strong>N &times; M</strong> hand-written, hand-remembered connections. Every
new feature that touches existing state has to rediscover every place that state is shown, and every new place
that shows existing state has to rediscover every place that state can change. Nothing in the language stops you
from missing one. This is not a discipline problem. It is what happens, mechanically, when "the view reflects the
data" is a promise developers keep by memory instead of a guarantee the system enforces.</p>

{keypoints("Why this matters", [
    "State living only in the DOM means there is no single place to ask 'what is true right now' other than the rendered page itself.",
    "Every additional display location for the same state multiplies the number of update call-sites a developer must remember.",
    "Bugs from this pattern don't throw errors &mdash; the UI just quietly shows stale or wrong data, which is often worse, because nothing tells you it happened."
])}
""")

    s4 = sub("p0-frameworks", "0.4", "Early Attempts: Backbone, Knockout, and Angular's Digest Cycle", "Pre-React frameworks", f"""
<p>The industry noticed the N&times;M problem well before React existed, and several serious attempts were made
to solve it.</p>

<p><strong>Backbone.js</strong> (2010) introduced Models and Views as first-class concepts: a Model held data and
emitted a <code class="inline">change</code> event, and a View listened for that event and re-rendered itself.
This was real progress &mdash; state and display were now explicitly connected through an event, not through
whatever the developer remembered to type. But the connection was still manual: you wrote the listener, you wrote
the re-render function, and for every new View that cared about a Model, you wrote that wiring again.</p>

<p><strong>Knockout.js</strong> pushed further with <em>observables</em> and declarative bindings written directly
in HTML:</p>

{code_panel("HTML", '''
<span data-bind="text: cartCount"></span>
''', "template.html")}

<p>This is a genuinely different idea: instead of writing an explicit update statement, you declare, once, "this
element's text should always equal this observable's value," and the library keeps that promise for you. That's
the first real appearance of a principle React would later take much further: <em>make the display a declared
consequence of the data, not a series of manual instructions.</em></p>

<p><strong>AngularJS</strong> (2010, what's now called "Angular 1.x" or "AngularJS" to distinguish it from the
unrelated Angular 2+) generalized two-way binding across an entire application using a mechanism called the
<em>digest cycle</em>. You'd write <code class="inline">{{{{ cartCount }}}}</code> in a template, and whenever
anything in the app might have changed, Angular would run a "digest": walk every expression it was watching,
re-evaluate it, and compare the new value to the last one it recorded, repeating this walk until nothing changed
between passes (dirty-checking).</p>

{callout("warn", "Where the digest cycle hit a ceiling", '''
<p>Dirty-checking works by brute force: on every possible change, re-check <em>everything</em> being watched,
and keep re-checking in a loop until a full pass produces no differences. As an application accumulated more
watched expressions &mdash; which happens naturally as it grows &mdash; each digest pass got more expensive,
and a poorly structured page could trigger multiple digest passes per user interaction. Developers writing
large AngularJS applications learned to watch their watcher count the way you'd watch a budget, because
performance degraded in a way that was directly tied to app size, not to how much had actually changed.</p>
''')}

<p>The pattern across all three: each one made real progress toward "declare the connection once, let the
system maintain it," but each hit a different ceiling &mdash; Backbone's wiring was still manual per-view,
Knockout's bindings were tightly coupled to specific DOM structure, and AngularJS's whole-app dirty-checking
didn't scale cleanly as applications grew. The idea was right. The execution hadn't found a fast, general
mechanism yet.</p>
""")

    s5 = sub("p0-facebook", "0.5", "The Bug That Started It All", "Facebook's actual motivating bug", f"""
<p>React's origin is a specific, well-documented story, not a generic "we wanted something better." Facebook's
engineers were fighting a recurring class of bug in the News Feed and, especially, chat: notification counts and
unread-message indicators would drift out of sync with reality. A message would be read in one part of the UI,
but a badge somewhere else on the page &mdash; updated by a different code path, written by a different engineer,
possibly months apart &mdash; wouldn't get the memo. This is the N&times;M problem from section 0.3, playing out
at the scale of one of the largest JavaScript codebases in the world.</p>

<p>Jordan Walke, an engineer at Facebook, had been experimenting with an idea borrowed partly from
<strong>XHP</strong>, an extension to PHP (Facebook's server-side language at the time) that let you embed markup
directly as a first-class value inside PHP code, rather than building HTML through string concatenation. Walke's
insight was to bring that same idea to the client: what if a UI component were just a function that you called
again, every time something changed, and which simply <em>described</em> what the screen should look like right
now &mdash; and a separate mechanism figured out how to reconcile that description with whatever was actually on
the page?</p>

<p>That prototype became React. It was first used internally on Facebook's News Feed, then on Instagram's website
after Facebook acquired Instagram, and it was open-sourced at JSConf US in May 2013. The initial public reaction
was, by most accounts, mixed to skeptical &mdash; mixing markup and logic in the same file (see Part 2) looked, to
eyes trained on "separation of concerns," like a step backwards. The technical bet underneath it took a few years
to fully land.</p>

{callout("history", "Why this history actually matters", '''
<p>It's tempting to treat "why was X invented" as trivia. It isn't, here. Every non-obvious design decision
covered later in this guide &mdash; why JSX mixes markup into JavaScript instead of the reverse, why React
insists you not touch the DOM directly, why hooks have the strict rules they have &mdash; traces back to this
one goal: make "the UI matches the data" a guarantee the library enforces, not a discipline the developer
maintains by hand across an unbounded number of call sites.</p>
''')}
""")

    s6 = sub("p0-requirements", "0.6", "What a Real Solution Needed to Do", "The requirements list", f"""
<p>Put together, the failures and near-misses above amount to a fairly precise specification. Whatever replaced
manual DOM wiring had to satisfy all five of the following at once &mdash; and note that no single prior attempt
had managed all five together:</p>

{requirement_list([
    ("a", "Be declarative", "Developers describe <em>what</em> the UI should look like for a given piece of state, not the step-by-step instructions for mutating it from its previous look to its new one."),
    ("b", "Be predictable", "The same state should always produce the same UI, regardless of the sequence of events that led to that state. No accumulated drift, no 'depends what order things happened in.'"),
    ("c", "Scale without N×M wiring", "Adding a new display location for existing state, or a new way to change existing state, should not require hunting down and editing every other place that state is touched."),
    ("d", "Stay fast without naive full re-renders", "Recomputing 'what should this look like' on every change is only useful if turning that description into real DOM updates is cheap — you can't just throw away and rebuild the entire page every time a checkbox is ticked; you'd lose scroll position, input focus, and performance."),
    ("e", "Compose from small, reusable pieces", "Large UIs need to be built out of independent, nameable, reusable parts — not one monolithic template or one giant imperative script."),
])}

<p>Requirement (d) is the one every earlier attempt either ignored or hadn't solved efficiently: it's easy to be
declarative if you're willing to be slow (just re-render everything, every time). React's actual technical
contribution &mdash; the piece that made the other four requirements viable in practice &mdash; is a fast,
general algorithm for turning "here is what I want now" into "here is the minimal set of real DOM operations to
get there." That algorithm is the Virtual DOM and its reconciliation process, and it's the subject of Part 4.
Part 1, next, starts with the idea in its simplest form: <strong>UI as a function of state.</strong></p>
""")

    body = s1 + s2 + s3 + s4 + s5 + s6
    return part("part-0", "0", "The World Before React",
                 "Why an entire industry decided the old way of building UI needed to be replaced &mdash; told through the actual bugs, not a marketing pitch.",
                 body, nxt=("part-1", "What React Actually Is"))
