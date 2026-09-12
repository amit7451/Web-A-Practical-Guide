# -*- coding: utf-8 -*-
from helpers import esc, code_panel, callout, keypoints, compare_grid, ref_table, sub, part

def build_part9():
    s1 = sub("p9-why-rerender", "9.1", "Why Components Actually Re-Render", "The real re-render rule", f"""
<p>A persistent and understandable misconception: "a component re-renders when its props change." The actual
rule is broader and catches most people off guard the first time they see it demonstrated: <strong>a component
re-renders when its own state changes, when its parent re-renders (regardless of whether this component's props
actually changed), or when a context value it reads changes.</strong></p>

{code_panel("JSX", '''
function Parent() {
  const [count, setCount] = useState(0);
  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Count: {count}</button>
      <StaticChild /> {/* receives NO props at all */}
    </div>
  );
}

function StaticChild() {
  console.log('StaticChild rendered'); // logs on EVERY click above
  return <p>I never change.</p>;
}
''', "default-rerender-behavior.jsx")}

<p>Clicking the button in <code class="inline">Parent</code> logs <code class="inline">"StaticChild rendered"
</code> every single time, even though <code class="inline">StaticChild</code> receives no props whatsoever and
has no state of its own. This is the default, unoptimized behavior: <strong>React re-renders a component's entire
subtree whenever that component re-renders</strong>, without checking whether children would produce different
output. Preventing this default is opt-in, not automatic &mdash; which is exactly what section 9.2 is for.</p>
""")

    s2 = sub("p9-memo", "9.2", "React.memo, useMemo, useCallback: When They Help", "When memoization helps", f"""
<p><code class="inline">React.memo</code> wraps a component so that React skips re-rendering it when its props
are shallowly equal to what they were last time &mdash; directly opting out of the default behavior shown in
9.1:</p>

{code_panel("JSX", '''
const StaticChild = React.memo(function StaticChild() {
  console.log('StaticChild rendered');
  return <p>I never change.</p>;
});
// Now Parent re-rendering does NOT re-render StaticChild,
// because its props (none) are trivially unchanged.
''', "memo-fixed.jsx")}

<p>The moment a memoized component actually receives props, memoization gets fragile in a specific, predictable
way: <code class="inline">React.memo</code>'s comparison is shallow, meaning it checks whether each prop is
<code class="inline">===</code> the same reference as before &mdash; not deeply equal in content. A brand new
object, array, or function literal is a brand new reference on every render, even if its contents are identical:</p>

{compare_grid(
    "Breaks memoization — new reference every render", "jsx", '''
function Parent() {
  const [count, setCount] = useState(0);
  return (
    <MemoChild
      onSave={() => save(count)}    // NEW function every render
      options={{ sorted: true }}     // NEW object every render
    />
  );
  // MemoChild re-renders every time anyway, memo or not —
  // its props are "different" by reference on every single pass.
}
''',
    "Preserves memoization — stable references", "jsx", '''
function Parent() {
  const [count, setCount] = useState(0);
  const handleSave = useCallback(() => save(count), [count]);
  const options = useMemo(() => ({ sorted: true }), []);

  return <MemoChild onSave={handleSave} options={options} />;
  // Now MemoChild's props are the SAME reference across renders
  // where count hasn't changed — memo can actually skip work.
}
''')}

<p>This is the payoff Part 5.5 pointed toward: <code class="inline">useMemo</code> and
<code class="inline">useCallback</code> earn their cost specifically in combination with
<code class="inline">React.memo</code>, by keeping prop references stable enough for memo's shallow comparison to
actually succeed. Used without a memoized child on the receiving end, they're frequently solving a problem that
doesn't exist yet &mdash; wrapping every function and object "just in case" adds real overhead and reading
friction for no measurable benefit.</p>
""")

    s3 = sub("p9-concurrent", "9.3", "Concurrent Features: startTransition and useDeferredValue", "Concurrent features", f"""
<p>Part 4.5 described priority lanes at the mechanism level; these two APIs are how you actually use them.
<code class="inline">startTransition</code> marks a state update as low-priority, explicitly telling React it's
allowed to interrupt this work for anything more urgent:</p>

{code_panel("JSX", '''
function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  function handleChange(e) {
    setQuery(e.target.value); // urgent: keep the input itself instantly responsive

    startTransition(() => {
      setResults(computeExpensiveResults(e.target.value)); // low-priority:
      // this can lag a moment behind without the user perceiving lag,
      // and React can interrupt it if the user types again before it finishes
    });
  }

  return <input value={query} onChange={handleChange} />;
}
''', "startTransition.jsx")}

<p><code class="inline">useDeferredValue</code> solves a closely related problem from the other direction: instead
of marking the update as low-priority at the point it's made, it takes a value and returns a version of it that's
allowed to "lag behind" during a heavy render, snapping to the latest value once React has spare capacity:</p>

{code_panel("JSX", '''
function SearchPage() {
  const [query, setQuery] = useState('');
  const deferredQuery = useDeferredValue(query);
  // deferredQuery updates a beat behind query during heavy renders,
  // keeping the input field itself perfectly responsive to typing.
  return (
    <>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <ExpensiveResultsList query={deferredQuery} />
    </>
  );
}
''', "useDeferredValue.jsx")}
""")

    s4 = sub("p9-suspense", "9.4", "Suspense and Code-Splitting Fundamentals", "Suspense & code-splitting", f"""
<p><code class="inline">React.lazy</code> defers loading a component's code until it's actually needed, splitting
your JavaScript bundle into smaller pieces the browser fetches on demand instead of all upfront.
<code class="inline">Suspense</code> declares what to show while that loading is in progress:</p>

{code_panel("JSX", '''
const SettingsPanel = React.lazy(() => import('./SettingsPanel'));

function App() {
  return (
    <Suspense fallback={<p>Loading settings...</p>}>
      <SettingsPanel />
      {/* The SettingsPanel.jsx code isn't even downloaded until this
          component actually needs to render, and the fallback shows
          automatically for however long that download takes. */}
    </Suspense>
  );
}
''', "lazy-suspense.jsx")}

<p>The same <code class="inline">Suspense</code> boundary mechanism extends beyond code-splitting to data itself:
newer patterns (tied closely to Server Components in Part 10.4, and the <code class="inline">use()</code> Hook
introduced in React 19) let a component "suspend" while data it needs is still loading, with the nearest
<code class="inline">Suspense</code> boundary automatically showing its fallback in the meantime &mdash; the same
declarative "describe what should show during loading" idea, applied to data fetching instead of just code
loading.</p>
""")

    s5 = sub("p9-profiling", "9.5", "A Mental Model for Profiling", "Profiling mental model", f"""
<p>React DevTools' Profiler tab records a "flame graph" for each commit: a horizontal bar per component,
proportional to how long that component took to render during that commit, nested to match the component tree.
The productive way to read one isn't "find the widest bar and optimize it" &mdash; it's usually more useful to
ask two questions in sequence:</p>

<ul class="plain">
  <li><strong>Did this component need to render at all, this time?</strong> The Profiler can highlight <em>why</em>
  a given component rendered (props changed, state changed, parent rendered, context changed) &mdash; and a
  surprising share of performance problems turn out to be components rendering for no reason connected to 9.1's
  default-cascade behavior, fixable with the memoization patterns from 9.2, rather than the rendering work itself
  being slow.</li>
  <li><strong>Is the rendering work itself actually expensive?</strong> Only once you've confirmed a component's
  re-render is genuinely necessary does it make sense to look at what's slow inside it &mdash; an expensive
  computation that belongs behind <code class="inline">useMemo</code>, or a component subtree wide enough that
  concurrent features (9.3) might help keep the rest of the page responsive while it renders.</li>
</ul>

{keypoints("Part 9, wrapped up", [
    "By default, a component's entire subtree re-renders whenever it does, regardless of whether children's props actually changed — this is the behavior to understand before reaching for any optimization.",
    "React.memo skips a re-render on shallowly-equal props; useMemo/useCallback exist largely to keep those props' references stable enough for memo's comparison to succeed.",
    "startTransition and useDeferredValue are the user-facing API for the priority-lanes mechanism from Part 4.5 — marking work as safe to interrupt or lag behind.",
    "Suspense declares a fallback for in-progress loading — originally for code-split components, and increasingly for in-progress data as well.",
    "Profile in two passes: first confirm a re-render was actually necessary, then look for genuinely expensive work inside renders that are."
])}
""")

    body = s1 + s2 + s3 + s4 + s5
    return part("part-9", "9", "The Performance Model",
                 "Why components actually re-render, and which optimizations do or don't help.",
                 body, prev=("part-8", "Forms, Refs & Escape Hatches"), nxt=("part-10", "Rendering Environments: CSR, SSR, SSG, RSC"))
