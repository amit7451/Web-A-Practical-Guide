# -*- coding: utf-8 -*-
from helpers import esc, code_panel, callout, keypoints, compare_grid, ref_table, sub, part

def build_part6():
    s1 = sub("p6-mount-update-unmount", "6.1", "Mount, Update, Unmount: Mapped Onto Hooks", "Lifecycle, mapped", f"""
<p>Class components (Part 3.2) organized side effects around three named moments: mounting (first appearing in
the DOM), updating (re-rendering due to new props or state), and unmounting (being removed). Hooks don't have
three separate named moments &mdash; they have one unified concept, the effect, and derive all three from how its
dependency array behaves:</p>

{ref_table(["Class lifecycle method", "Hook equivalent", "Note"], [
    ["<code class='inline'>componentDidMount</code>", "<code class='inline'>useEffect(fn, [])</code>", "Runs once, after the first render — an empty dependency array means “never run again after mount.”"],
    ["<code class='inline'>componentDidUpdate</code>", "<code class='inline'>useEffect(fn, [dep])</code>", "Runs after any render where a listed dependency changed — there's no separate “on-mount vs on-update” distinction; the same effect handles both by design."],
    ["<code class='inline'>componentWillUnmount</code>", "the function returned from <code class='inline'>useEffect</code>", "The cleanup function (Part 5.2) runs on unmount, and also before every subsequent re-run of that same effect."],
])}

<p>That middle row is worth sitting with, because it's a genuine design difference, not just a syntax swap.
<code class="inline">componentDidMount</code> and <code class="inline">componentDidUpdate</code> were two separate
methods, which meant logic that needed to run on both (subscribing based on a prop's current value, say) had to
be duplicated across both methods, or extracted into a shared helper called from both. A single
<code class="inline">useEffect</code> call with the right dependency array handles both cases with one block of
code, because "run this after the render where these values were used" is a single concept that mount and update
are just two instances of.</p>
""")

    s2 = sub("p6-strict-mode", "6.2", "Strict Mode's Double-Invocation, Explained", "Strict Mode's double-run", f"""
<p>If you've ever wrapped your app in <code class="inline">&lt;React.StrictMode&gt;</code> during development and
noticed effects, and sometimes component function bodies, apparently running twice for what looks like a single
render, this is not a bug in your code or in React. It's deliberate, development-only behavior: Strict Mode
intentionally mounts a component, immediately unmounts it, and mounts it again, specifically to surface effects
whose cleanup functions are missing or incorrect.</p>

{code_panel("JSX", '''
useEffect(() => {
  const id = setInterval(tick, 1000);
  // If you forget: return () => clearInterval(id);
  // ...Strict Mode's mount → unmount → remount cycle in development
  // will create a SECOND interval on top of the first, making the bug
  // impossible to miss during development — instead of shipping
  // silently to production and leaking timers there instead.
}, []);
''', "strict-mode-reveals-leak.jsx")}

<p>The reasoning connects directly back to Part 4.5's discussion of interruptible, potentially-repeated render
work: if React's architecture allows a component to be rendered, discarded, and rendered again under some
circumstances, then effects that assume "I will only ever run once, cleanly" are relying on a guarantee React
never actually made. Strict Mode makes that assumption fail loudly and immediately, in development, rather than
occasionally and mysteriously, in production. <strong>This double-invocation never happens in a production
build</strong> &mdash; it's a development-only diagnostic, not a runtime behavior your users will experience.</p>
""")

    s3 = sub("p6-cleanup-ordering", "6.3", "Effect Cleanup Ordering", "Cleanup ordering", f"""
<p>Two ordering guarantees matter in practice. First, within a single component, if it defines multiple effects,
their cleanup functions on unmount run in the same order the effects themselves were declared &mdash; effect A's
cleanup, then effect B's cleanup, matching the order A and B appear in your code. Second, across a tree, child
components unmount &mdash; and their effects clean up &mdash; before their parent's own effects clean up, mirroring
the fact that children are logically "inside" their parent and should finish tearing down first.</p>

{code_panel("JSX", '''
function Parent() {
  useEffect(() => {
    return () => console.log('Parent cleanup');
  }, []);
  return <Child />;
}

function Child() {
  useEffect(() => {
    return () => console.log('Child cleanup');
  }, []);
  return <div>Child content</div>;
}

// Unmounting <Parent /> logs, in order:
//   "Child cleanup"
//   "Parent cleanup"
''', "cleanup-order.jsx")}

<p>The practical takeaway is narrower than it might sound: you rarely need to reason about cross-component
cleanup ordering directly, because each effect's cleanup should only be responsible for undoing what that exact
effect set up. When that discipline holds, ordering between unrelated effects and components simply doesn't
matter to correctness &mdash; it only becomes relevant in the rarer case of effects that intentionally coordinate
with each other across the tree.</p>
""")

    s4 = sub("p6-stale-closures", "6.4", "Stale Closures and Other Classic Lifecycle Bugs", "Stale closures", f"""
<p>The single most common Hook-era bug has a consistent shape: an effect captures a variable's value from the
render it was defined in, and that captured value never updates, even though the component has since re-rendered
with a new one. This is not a React quirk &mdash; it's ordinary JavaScript closure behavior, applied to a function
(your component) that happens to get called repeatedly.</p>

{compare_grid(
    "Buggy — stale closure", "jsx", '''
function Timer() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setCount(count + 1); // "count" here is frozen at 0 forever —
      // this effect ran ONCE (empty deps), so this closure only
      // ever sees the "count" value from that first render.
    }, 1000);
    return () => clearInterval(id);
  }, []); // count is used inside, but not listed — the classic trigger

  return <p>{count}</p>; // stays stuck at 1, never climbs higher
}
''',
    "Fixed — functional update", "jsx", '''
function Timer() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setCount(c => c + 1); // reads the LATEST pending value,
      // regardless of which render's closure this function came from
    }, 1000);
    return () => clearInterval(id);
  }, []); // safe to keep an empty array now — nothing stale is read

  return <p>{count}</p>; // climbs correctly, once per second
}
''')}

<p>The general rule this points to: either include every value an effect reads in its dependency array (letting
the effect re-run, and re-capture fresh closures, whenever those values change), or, when re-running the whole
effect isn't desirable, use the functional update form (Part 5.1) or a ref (Part 5.4) to read the latest value
without needing it in the dependency array at all. The official <code class="inline">exhaustive-deps</code> ESLint
rule exists specifically to catch the first half of this &mdash; a dependency your effect reads but doesn't
declare &mdash; before it ships as a bug.</p>

{keypoints("Part 6, wrapped up", [
    "useEffect unifies mount and update handling into one concept — the dependency array decides when it re-runs, rather than needing separate methods for each moment.",
    "Strict Mode's development-only double-invocation exists to surface missing or incorrect cleanup before it reaches production.",
    "Cleanup runs child-first, parent-second across the tree, and in declaration order within a single component — though well-scoped effects rarely need to care.",
    "Stale closures happen because your component function is just a regular JavaScript function being called repeatedly — an effect's callback captures whatever a variable's value was during the specific render that effect belongs to."
])}
""")

    body = s1 + s2 + s3 + s4
    return part("part-6", "6", "The Component Lifecycle, Through Hooks",
                 "Mount, update, and unmount — mapped onto the Hooks that replaced lifecycle methods, and the bugs that show up when the mapping is misunderstood.",
                 body, prev=("part-5", "Hooks: Mechanics and Rules"), nxt=("part-7", "Data Flow & State Management"))
