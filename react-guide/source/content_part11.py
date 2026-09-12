# -*- coding: utf-8 -*-
from helpers import esc, code_panel, callout, keypoints, compare_grid, ref_table, sub, part

def build_part11():
    s1 = sub("p11-same-feature", "11.1", "The Same Feature, Three Ways", "One feature, three ways", f"""
<p>Every difference described abstractly so far in this guide is easiest to see concretely. Here is one small,
complete feature &mdash; a "like" button with a live count &mdash; built three ways: plain vanilla JavaScript,
jQuery, and React. Nothing about the feature itself changes; what changes is how each approach keeps the display
in sync with the underlying number.</p>

{code_panel("JavaScript", '''
let liked = false;
let count = 42;

const btn = document.querySelector('#like-btn');
const countEl = document.querySelector('#like-count');

btn.addEventListener('click', () => {
  liked = !liked;
  count = liked ? count + 1 : count - 1;

  // Every place this data is shown has to be updated by hand, here:
  countEl.textContent = count;
  btn.textContent = liked ? 'Liked' : 'Like';
  btn.classList.toggle('active', liked);
});
''', "vanilla.js")}

{code_panel("JavaScript", '''
let liked = false;
let count = 42;

$('#like-btn').on('click', function () {
  liked = !liked;
  count = liked ? count + 1 : count - 1;

  // Same three manual updates, just through jQuery's shorter API:
  $('#like-count').text(count);
  $(this).text(liked ? 'Liked' : 'Like').toggleClass('active', liked);
});
''', "jquery.js")}

{code_panel("JSX", '''
function LikeButton() {
  const [liked, setLiked] = useState(false);
  const [count, setCount] = useState(42);

  function handleClick() {
    setLiked(!liked);
    setCount(liked ? count - 1 : count + 1);
  }

  // Describe what it should look like for the current state.
  // Nothing here mentions the DOM, or what it looked like a moment ago.
  return (
    <button onClick={handleClick} className={liked ? 'active' : ''}>
      {liked ? 'Liked' : 'Like'} ({count})
    </button>
  );
}
''', "react.jsx")}

<p>The vanilla and jQuery versions are, structurally, the exact same program &mdash; find nodes, mutate nodes,
three separate manual update statements per click, exactly Part 0.2's observation that jQuery shortened the
syntax without changing the architecture. The React version has no equivalent list of manual update statements
at all, because there's nothing to keep in sync by hand: the returned JSX is simply re-evaluated against the
current values of <code class="inline">liked</code> and <code class="inline">count</code> every time either one
changes, and Part 4's reconciler decides what, if anything, actually needs to change in the real DOM.</p>
""")

    s2 = sub("p11-what-react-adds", "11.2", "What React Adds on Top of JavaScript", "What React actually adds", f"""
<p>Having now covered React in full depth, it's possible to give an exact, complete answer to "what does React
actually add to plain JavaScript" &mdash; and the honest answer is: <strong>three things, precisely.</strong></p>

{ref_table(["What React adds", "Covered in"], [
    ["JSX — a compile step that turns markup-like syntax into function calls", "Part 2"],
    ["The reconciler — an algorithm that turns “new UI description” into minimal real DOM changes", "Part 4"],
    ["The Hooks engine — a mechanism for function components to hold state and run side effects across renders", "Part 5"],
])}

<p>That's the complete list. Everything else this guide has covered &mdash; components, props, the rules about
data flow, forms, performance patterns, even rendering environments &mdash; is either a direct consequence of
those three things, or ordinary JavaScript applied inside a React component's function body. There is no fourth
category of "React magic" hiding somewhere else.</p>
""")

    s3 = sub("p11-still-dom-calls", "11.3", "What Doesn't Change: It's Still Just DOM Calls", "Still just DOM calls", f"""
<p>Follow any React update all the way down, past the virtual DOM (4.1), past the diff (4.2), past the commit
phase (4.3), and you arrive at exactly the same browser APIs the vanilla example in 11.1 called directly:
<code class="inline">appendChild</code>, <code class="inline">setAttribute</code>,
<code class="inline">removeChild</code>, <code class="inline">textContent</code> assignments. React is not a
new way of talking to the browser &mdash; browsers have no idea React exists. It is an automation layer that
decides, on your behalf, which of those exact same calls to make and when, so that you don't have to work out
the answer by hand every time your data changes.</p>

{callout("note", "A genuinely useful reframe", '''
<p>“Learning React” is, in a real and specific sense, mostly “learning a particular, disciplined
way to keep writing JavaScript” — plus the three additions from 11.2. Every event handler, every array
method used to transform data before rendering it, every conditional, every piece of business logic inside a
component is exactly the JavaScript you already know. Nothing about switching to React makes JavaScript
knowledge obsolete; it sits directly underneath everything React does.</p>
''')}
""")

    s4 = sub("p11-styling", "11.4", "Styling in React: className, CSS Modules, and Styled Components", "Styling landscape", f"""
<p>CSS itself is completely unaffected by React &mdash; every selector, property, and cascade rule works exactly
as it always has. What varies across the ecosystem is <em>how class names get attached to elements and scoped to
components</em>, and it's worth knowing the landscape rather than treating one approach as "the React way":</p>

{ref_table(["Approach", "How it works", "Trade-off"], [
    ["Plain CSS files + className", "Write ordinary <code class='inline'>.css</code> files, import them, and apply class names via <code class='inline'>className</code> exactly as covered in Part 2.4.", "Simplest, zero extra tooling — but class names are global by default, so naming collisions across a large codebase are the developer's problem to manage."],
    ["CSS Modules", "Files named e.g. <code class='inline'>Button.module.css</code>; the build tool automatically generates unique class names per file, avoiding collisions entirely.", "Solves scoping with no new syntax to learn, at the cost of a small amount of build configuration most modern toolchains already include."],
    ["CSS-in-JS (styled-components, Emotion)", "Write CSS directly inside JavaScript, co-located with the component that uses it, often as tagged template literals.", "Styles and logic live in the same file and can reference JS values/props directly, at the cost of a runtime or compile-time dependency and, for runtime variants, some performance overhead."],
    ["Utility-first (Tailwind CSS)", "Compose pre-defined utility classes directly in <code class='inline'>className</code> instead of writing custom CSS rules at all.", "Very fast iteration once the utility vocabulary is familiar, at the cost of longer, denser className strings and a real learning curve for that vocabulary."],
])}

<p>None of these is React-specific in the way JSX or Hooks are &mdash; CSS Modules and Tailwind both work happily
in non-React projects too. React's only actual involvement in styling, full stop, is the
<code class="inline">className</code> and <code class="inline">style</code> object mechanics from Part 2.4;
everything in the table above is an ecosystem choice layered on top.</p>
""")

    s5 = sub("p11-boundary", "11.5", "Where the Browser Ends and React Begins", "The precise boundary", f"""
<p>A clean way to close the loop on this Part: HTML, CSS, and JavaScript are the actual substrate that runs
&mdash; the only three languages a browser natively understands, full stop. React is not a fourth language, and
it does not replace any of the three. It's a JavaScript library, written in JavaScript, that generates and
updates HTML elements and reads and writes their attributes, using the exact same DOM APIs available to any
plain script, following the specific, deliberate model this entire guide has covered: describe the desired state
declaratively (Part 1), express that description in JSX (Part 2), organize it into composable functions
(Part 3), and let a reconciliation engine (Part 4) figure out the efficient path from what's currently on screen
to what you just described.</p>

<p>This means the honest prerequisite for learning React well is not "learn React instead of HTML/CSS/JS"
&mdash; it's "know HTML, CSS, and JavaScript reasonably well first," because every single thing React does is
built directly on top of them, assumes you understand them, and gives you no separate vocabulary for the things
those three languages already handle.</p>

{keypoints("Part 11, wrapped up", [
    "The same feature built in vanilla JS, jQuery, and React reveals the real difference precisely: manual, per-location update statements versus one description, re-evaluated.",
    "React adds exactly three things to JavaScript — JSX, the reconciler, and the Hooks engine — and nothing else.",
    "Every React update eventually becomes the exact same DOM calls a vanilla script would make; React decides which calls to make and when, but invents no new way of talking to the browser.",
    "CSS is completely unaffected by React; styling approaches like CSS Modules, CSS-in-JS, and Tailwind are ecosystem choices layered on top of plain className, not React features.",
    "React is built entirely on top of HTML, CSS, and JavaScript, and assumes fluency in all three — it replaces none of them."
])}
""")

    body = s1 + s2 + s3 + s4 + s5
    return part("part-11", "11", "React vs. Plain HTML, CSS, and JS",
                 "The explicit, side-by-side comparison: what actually changes, and what quietly doesn't.",
                 body, prev=("part-10", "Rendering Environments: CSR, SSR, SSG, RSC"), nxt=("part-12", "Patterns & Idioms"))
