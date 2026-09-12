# -*- coding: utf-8 -*-
from helpers import esc, code_panel, callout, keypoints, compare_grid, ref_table, sub, part

HOOKLIST_SVG = """<svg class="diagram" viewBox="0 0 700 170" xmlns="http://www.w3.org/2000/svg">
  <style>
    .hn{ fill:var(--bg-card); stroke:var(--rule); }
    .hl{ font-size:11px; font-family: var(--font-mono); }
    .hedge{ stroke:var(--accent-dim); stroke-width:1.4; fill:none; }
  </style>
  <text x="10" y="20" style="font-size:11.5px; fill:var(--ink-dim);">Fiber's hook list for one component instance, in call order:</text>

  <rect class="hn" x="10"  y="40" width="150" height="60" rx="8"/>
  <text class="hl" x="85" y="64" text-anchor="middle">useState(0)</text>
  <text class="hl" x="85" y="80" text-anchor="middle" fill="var(--ink-faint)">slot 1: count</text>

  <path class="hedge" d="M160,70 L185,70"/>

  <rect class="hn" x="190" y="40" width="150" height="60" rx="8"/>
  <text class="hl" x="265" y="64" text-anchor="middle">useEffect(...)</text>
  <text class="hl" x="265" y="80" text-anchor="middle" fill="var(--ink-faint)">slot 2: effect</text>

  <path class="hedge" d="M340,70 L365,70"/>

  <rect class="hn" x="370" y="40" width="150" height="60" rx="8"/>
  <text class="hl" x="445" y="64" text-anchor="middle">useState('')</text>
  <text class="hl" x="445" y="80" text-anchor="middle" fill="var(--ink-faint)">slot 3: name</text>

  <path class="hedge" d="M520,70 L545,70"/>

  <rect class="hn" x="550" y="40" width="140" height="60" rx="8"/>
  <text class="hl" x="620" y="64" text-anchor="middle">useRef(null)</text>
  <text class="hl" x="620" y="80" text-anchor="middle" fill="var(--ink-faint)">slot 4: ref</text>

  <text x="10" y="135" style="font-size:11.5px; fill:var(--brick);">On the NEXT render, React walks this same list in the SAME order —</text>
  <text x="10" y="152" style="font-size:11.5px; fill:var(--brick);">it has no names, only positions. Skip a hook conditionally, and slot 3 becomes slot 2's data.</text>
</svg>"""

def build_part5():
    s1 = sub("p5-usestate", "5.1", "useState: What's Actually Stored, and Where", "useState internals", f"""
<p>The single most important mental model in this entire Part is one most tutorials skip: <strong>where does the
value returned by <code class="inline">useState</code> actually live?</strong> Not in a variable in your
component function &mdash; that function gets re-run, top to bottom, from scratch, on every single render, so any
plain local variable would simply be reset to its initial value every time. The state has to live somewhere that
survives across separate calls to your function entirely.</p>

<p>It lives on the <strong>fiber</strong> &mdash; the Part 4.4 data structure React maintains per component
instance. Each fiber keeps an ordered list of "hook" entries, and every <code class="inline">useState</code>,
<code class="inline">useEffect</code>, or other Hook call inside your component claims the <em>next slot</em> in
that list, strictly in the order those calls appear in your code:</p>

{HOOKLIST_SVG}

<p>On the very first render, React creates a new list entry for each Hook call and stores its initial value. On
every subsequent render, React does not re-run any special "set up state" logic &mdash; it simply walks the
<em>same list, in the same order</em>, and hands back whatever is already stored in each slot. This is precisely
why the Hook call order has to be identical on every single render, a rule made fully explicit in section 5.8.</p>

{code_panel("JSX", '''
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>Count: {count}</button>;
}
''', "Counter.jsx")}

<p>Calling <code class="inline">setCount</code> does two things: it updates the value stored in that fiber's slot,
and it schedules a re-render of this component. On that new render, <code class="inline">useState(0)</code> runs
again &mdash; but the <code class="inline">0</code> argument is only ever used for the very first render of that
slot; every render after that, React ignores it and returns whatever value is currently stored.</p>

{callout("tip", "Functional updates avoid a subtle trap", '''
<p><code class="inline">setCount(count + 1)</code> uses whatever value <code class="inline">count</code> was
inside <em>this particular render's</em> function call — which, combined with batching (Part 4.6), can
cause a surprising result if you call it multiple times in a row expecting each call to build on the last:
three calls to <code class="inline">setCount(count + 1)</code> in the same handler all see the same
<code class="inline">count</code> and all schedule "set it to count + 1," not "+3." The functional form,
<code class="inline">setCount(c =&gt; c + 1)</code>, receives the truly latest pending value as its argument
and composes correctly no matter how many times it's called before the next render.</p>
''')}
""")

    s2 = sub("p5-useeffect", "5.2", "useEffect: Timing, Dependencies, and Cleanup", "useEffect mechanics", f"""
<p><code class="inline">useEffect</code> is where side effects belong, for exactly the reason Part 4.3 laid out:
it runs strictly after the commit phase, once the real DOM already reflects the latest render, and it runs
asynchronously with respect to painting &mdash; specifically, after the browser has had a chance to paint the
screen, so a slow effect won't visibly delay what the user sees.</p>

{code_panel("JSX", '''
useEffect(() => {
  console.log('runs after every render where deps changed');

  return () => {
    console.log('cleanup: runs before the next effect run, and on unmount');
  };
}, [dep1, dep2]); // the dependency array
''', "useEffect-shape.jsx")}

<p>The second argument &mdash; the dependency array &mdash; controls exactly when the effect function runs
again, and the three forms behave distinctly enough that mixing them up is one of the most common early
mistakes:</p>

{ref_table(["Dependency array", "When the effect re-runs"], [
    ["<code class='inline'>[]</code> (empty array)", "Only once, after the very first render — conceptually similar to componentDidMount."],
    ["<code class='inline'>[dep1, dep2]</code>", "After the first render, and again any time dep1 or dep2 is different from its previous value."],
    ["omitted entirely (no second argument)", "After every single render, with no exception — rarely what you actually want."],
])}

<p>The <strong>cleanup function</strong> &mdash; whatever you return from the effect &mdash; runs at two specific
moments: right before the effect runs again (to undo whatever the previous run set up, before setting it up
again), and once more on unmount. A subscription is the canonical example:</p>

{code_panel("JSX", '''
useEffect(() => {
  function handleResize() {
    setWidth(window.innerWidth);
  }
  window.addEventListener('resize', handleResize);

  return () => window.removeEventListener('resize', handleResize);
  // Without this cleanup, every re-render that re-runs this effect would add
  // ANOTHER listener without removing the old one — a classic, silent leak.
}, []);
''', "subscription-cleanup.jsx")}
""")

    s3 = sub("p5-uselayouteffect", "5.3", "useLayoutEffect vs useEffect", "Layout vs passive effects", f"""
<p><code class="inline">useLayoutEffect</code> has an identical API to <code class="inline">useEffect</code> and
a subtly different timing guarantee: it runs synchronously, immediately after the DOM has been mutated but
<strong>before</strong> the browser paints anything to the screen. <code class="inline">useEffect</code>, by
contrast, is deliberately allowed to run after paint.</p>

<p>That difference matters for exactly one category of problem: when an effect needs to measure something about
the newly-committed DOM and then <em>synchronously</em> change it again before the user sees anything, to avoid a
visible flicker.</p>

{code_panel("JSX", '''
function Tooltip({ targetRef }) {
  const [position, setPosition] = useState({ top: 0, left: 0 });

  useLayoutEffect(() => {
    const rect = targetRef.current.getBoundingClientRect();
    setPosition({ top: rect.bottom, left: rect.left });
    // Runs, measures, and re-renders BEFORE paint — the tooltip
    // never visibly appears in the wrong place first.
  }, [targetRef]);

  return <div style={{ position: 'absolute', top: position.top, left: position.left }}>Tip!</div>;
}
''', "Tooltip.jsx")}

{callout("tip", "The default should be useEffect", '''
<p>useLayoutEffect blocks the browser from painting until it finishes, which is exactly the cost
<code class="inline">useEffect</code>'s async timing exists to avoid (Part 4.3's phase split). Reach for
<code class="inline">useLayoutEffect</code> specifically when you have a measurable visual flicker to fix, not
as a general-purpose "run this effect a bit sooner" tool.</p>
''')}
""")

    s4 = sub("p5-useref", "5.4", "useRef and the Mutable Escape Hatch", "useRef's two jobs", f"""
<p><code class="inline">useRef</code> returns a plain mutable object with a single property,
<code class="inline">.current</code>, that persists across renders &mdash; and, critically, <strong>changing
<code class="inline">.current</code> does not trigger a re-render</strong>, unlike <code class="inline">
useState</code>. This one property makes it useful for two genuinely different jobs that happen to share an
implementation:</p>

{code_panel("JSX", '''
function Example() {
  // Job 1: a mutable value that survives renders, without causing new ones
  const renderCount = useRef(0);
  renderCount.current += 1; // safe to mutate directly, unlike state

  // Job 2: a handle to an actual DOM node
  const inputRef = useRef(null);
  function focusInput() {
    inputRef.current.focus(); // .current is the real <input> DOM element once mounted
  }

  return <input ref={inputRef} />;
}
''', "useRef-two-jobs.jsx")}

<p>Job 2 is React's sanctioned way of doing the "reach into the DOM directly" work Part 1.5 flagged as an
exception to the normal rule: focusing an input, reading a scroll position, or integrating a non-React library
that needs a real DOM node. Job 1 is a general storage cell for anything that needs to persist between renders
but has no business causing a re-render when it changes &mdash; a previous value for comparison, a timer ID, a
flag.</p>
""")

    s5 = sub("p5-usememo-usecallback", "5.5", "useMemo and useCallback: Memoization Mechanics", "Memoization", f"""
<p>Both hooks solve the same underlying problem &mdash; recomputing something on every render that didn't need to
change &mdash; for two different kinds of "something."</p>

{code_panel("JSX", '''
// useMemo caches a VALUE
const sortedList = useMemo(() => {
  return [...items].sort((a, b) => a.price - b.price); // an expensive sort
}, [items]); // only re-sorts when items actually changes

// useCallback caches a FUNCTION REFERENCE
const handleClick = useCallback(() => {
  onSelect(item.id);
}, [item.id, onSelect]); // only creates a new function when these change
''', "memo-hooks.jsx")}

<p><code class="inline">useCallback(fn, deps)</code> is, precisely, shorthand for
<code class="inline">useMemo(() =&gt; fn, deps)</code> &mdash; it's memoizing the function itself as a value, no
different in kind from memoizing a sorted array. Both compare the dependency array to its previous values
(using the same reference-equality check, <code class="inline">Object.is</code>, under the hood) and only
recompute when something in that array has actually changed.</p>

{callout("warn", "Memoization is not free, and doesn't always help", '''
<p>Both hooks still run on every render — they run the dependency comparison, and if nothing changed, they
skip the expensive recomputation and return the previously cached value instead. For a cheap computation
(concatenating two short strings, adding two numbers), the comparison overhead can exceed the cost of just
redoing the work, making the "optimization" a net negative. These hooks earn their cost specifically when
either the wrapped computation is genuinely expensive, or when reference stability itself matters — which
is precisely the scenario Part 9.2 covers, where an unstable function or object passed as a prop can defeat
React.memo entirely.</p>
''')}
""")

    s6 = sub("p5-usereducer", "5.6", "useReducer: Local State With Redux-Shaped Logic", "useReducer", f"""
<p><code class="inline">useReducer</code> manages state through a <strong>reducer function</strong> &mdash; a
pure function of the shape <code class="inline">(state, action) =&gt; newState</code> &mdash; instead of a
direct setter. It's the same pattern Redux popularized (and, not coincidentally, the same shape Part 7.4 will
describe Redux's global store using):</p>

{code_panel("JSX", '''
function todosReducer(state, action) {
  switch (action.type) {
    case 'added':
      return [...state, { id: action.id, text: action.text, done: false }];
    case 'toggled':
      return state.map(t => t.id === action.id ? { ...t, done: !t.done } : t);
    case 'removed':
      return state.filter(t => t.id !== action.id);
    default:
      return state;
  }
}

function TodoList() {
  const [todos, dispatch] = useReducer(todosReducer, []);

  function handleAdd(text) {
    dispatch({ type: 'added', id: crypto.randomUUID(), text });
  }
  // ...
}
''', "useReducer.jsx")}

<p>Reach for this over several separate <code class="inline">useState</code> calls specifically when: several
pieces of state change together as one logical unit (adding a todo touches both the list and, potentially, an
input's contents); the next state depends on the previous state in a way that's more involved than a single
value flip; or the sheer number of distinct ways state can change makes a named, centralized switch statement
easier to follow than scattered setter calls throughout the component.</p>
""")

    s7 = sub("p5-usecontext", "5.7", "useContext: Reading Context Without Prop Drilling", "useContext (preview)", f"""
<p><code class="inline">useContext</code> reads whatever value the nearest matching
<code class="inline">Context.Provider</code> above it in the tree currently holds, without that value needing to
be threaded down as a prop through every intermediate component:</p>

{code_panel("JSX", '''
const ThemeContext = React.createContext('light');

function ThemedButton() {
  const theme = useContext(ThemeContext); // reads whatever the nearest Provider set
  return <button className={`btn-${theme}`}>Click me</button>;
}
''', "useContext-basic.jsx")}

<p>This is intentionally a brief preview &mdash; Part 7.3 covers the full Context API, including how Providers
are set up, what happens with multiple nested Providers, and a real performance gotcha around how broadly a
context value's changes propagate. What matters here is where it fits among the other Hooks: it's the
Hook-based way of consuming a value that was deliberately made available outside the normal parent-to-child
prop chain.</p>
""")

    s8 = sub("p5-rules-of-hooks", "5.8", "The Rules of Hooks, and Why They're Not Arbitrary", "The Rules of Hooks", f"""
<p>React enforces two rules about how Hooks can be called, both non-negotiable, both directly explained by
section 5.1's slot-list mechanism:</p>

{ref_table(["Rule", "Why it exists"], [
    ["Only call Hooks at the top level — never inside conditions, loops, or nested functions.", "React matches Hook calls to their stored data purely by call order, not by name or any other identifier. If a Hook call is skipped on some renders (because it was inside an if-statement) but not others, every Hook call after it shifts by one slot, and each one silently reads a different piece of state than it did before."],
    ["Only call Hooks from React function components or from custom Hooks.", "The slot list in 5.1 lives on a component's fiber. Calling a Hook from a plain utility function gives React no fiber to attach that state to at all."],
])}

<p>The first rule is worth seeing broken, because the failure mode is genuinely confusing if you haven't seen
the mechanism behind it:</p>

{code_panel("JSX", '''
function Profile({ userId }) {
  if (userId) {
    const [user, setUser] = useState(null); // BREAKS THE RULE: conditional Hook call
  }
  const [isEditing, setIsEditing] = useState(false);
  // On a render where userId is falsy, the useState(null) call above is
  // SKIPPED entirely — so isEditing's useState call claims slot 1
  // instead of slot 2. On a render where userId IS present, isEditing's
  // call claims slot 2 again. The two renders now disagree about which
  // slot holds which state, and React has no way to detect this from
  // the outside — it just silently returns the wrong stored value.
}
''', "broken-conditional-hook.jsx")}

{callout("tip", "The linter catches this for you", '''
<p>The official <code class="inline">eslint-plugin-react-hooks</code> package's
<code class="inline">rules-of-hooks</code> rule statically detects exactly this pattern and errors at build
time, before the bug ever reaches a running app. If your editor flags a Hook call as conditional, this
section is the actual reason why — not an arbitrary style preference.</p>
''')}
""")

    s9 = sub("p5-custom-hooks", "5.9", "Writing Your Own Custom Hooks", "Custom hooks", f"""
<p>A custom Hook is nothing more than a regular JavaScript function, named with a <code class="inline">use</code>
prefix by convention, that calls one or more of React's built-in Hooks internally. That naming convention isn't
cosmetic &mdash; it's how the Rules of Hooks linter from 5.8 knows to apply its checks to your function too.</p>

{code_panel("JSX", '''
function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    const stored = window.localStorage.getItem(key);
    return stored !== null ? JSON.parse(stored) : initialValue;
  });

  useEffect(() => {
    window.localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue]; // same shape as useState, by convention
}

// Usage, indistinguishable from a built-in Hook at the call site:
function Settings() {
  const [theme, setTheme] = useLocalStorage('theme', 'light');
  return <button onClick={() => setTheme('dark')}>Current: {theme}</button>;
}
''', "useLocalStorage.jsx")}

<p>Every call to <code class="inline">useLocalStorage</code> gets its own, completely independent state &mdash;
calling it doesn't share data between components, the same way calling <code class="inline">useState</code>
twice in two different components never shares state between them. What's actually being shared is the
<em>logic</em> &mdash; the stateful behavior itself, written once, is now reusable across as many components as
need it. This is the direct answer to the class-component limitation flagged back in Part 3.2's history callout:
before Hooks, sharing this exact kind of behavior required patterns like Higher-Order Components or render props
(both covered in Part 12), which wrapped components in extra layers just to inject shared logic. A custom Hook
does the same job with a plain function call and no extra component in the tree at all.</p>

{keypoints("Part 5, wrapped up", [
    "State lives on the fiber, in an ordered list; Hook calls claim slots strictly by call order, every single render.",
    "useEffect runs after paint for side effects; useLayoutEffect runs before paint, only when a measure-then-adjust flicker needs fixing.",
    "useMemo and useCallback are the same mechanism — caching a value versus caching a function — and only pay off when the cached work is genuinely expensive or reference stability matters.",
    "The Rules of Hooks exist because call order IS the identification mechanism; skip a Hook conditionally and every subsequent Hook reads the wrong stored data.",
    "A custom Hook shares stateful LOGIC across components, not the state itself — each call site gets its own independent copy."
])}
""")

    body = s1 + s2 + s3 + s4 + s5 + s6 + s7 + s8 + s9
    return part("part-5", "5", "Hooks: Mechanics and Rules",
                 "How function components hold state and run side effects, and why the Rules of Hooks aren't arbitrary.",
                 body, prev=("part-4", "The Virtual DOM & Reconciliation"), nxt=("part-6", "The Component Lifecycle, Through Hooks"))
