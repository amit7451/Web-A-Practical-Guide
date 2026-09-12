# -*- coding: utf-8 -*-
from helpers import esc, code_panel, callout, keypoints, compare_grid, ref_table, sub, part

def build_part7():
    s1 = sub("p7-lifting-state", "7.1", "Lifting State Up", "Lifting state up", f"""
<p>Part 3.5 established that data only flows down the component tree. This creates an immediate, practical
question: what do you do when two sibling components both need access to the same piece of state? A child cannot
reach sideways to another child, and it cannot reach up and grab something from a parent that doesn't have it
either. The answer is always the same: move the state up to the nearest common ancestor of everything that needs
it, then pass it back down as props &mdash; a pattern universally called <strong>lifting state up</strong>.</p>

{compare_grid(
    "Before — state stuck in the wrong place", "jsx", '''
function SearchBox() {
  const [query, setQuery] = useState('');
  return <input value={query} onChange={e => setQuery(e.target.value)} />;
  // ResultsList, a SIBLING, has no way to read this query at all.
}

function ResultsList() {
  return <ul>{/* needs "query" from SearchBox, but can't reach it */}</ul>;
}
''',
    "After — state lifted to the common parent", "jsx", '''
function SearchPage() {
  const [query, setQuery] = useState(''); // now lives in the shared ancestor

  return (
    <>
      <SearchBox query={query} onQueryChange={setQuery} />
      <ResultsList query={query} />
    </>
  );
}

function SearchBox({ query, onQueryChange }) {
  return <input value={query} onChange={e => onQueryChange(e.target.value)} />;
}
''')}

<p>Nothing about the state itself changed &mdash; it's still a single <code class="inline">useState</code> call.
What changed is <em>where</em> it lives in the tree: one level higher, at the first component that is an ancestor
of every component that needs to read or write it.</p>
""")

    s2 = sub("p7-prop-drilling", "7.2", "Prop Drilling: Real Problem vs. Premature Abstraction", "Prop drilling", f"""
<p>Lifting state up has an obvious cost: the components between the ancestor holding the state and the descendant
that actually uses it now have to accept and forward props they never use themselves, purely so the data can pass
through them. This is called <strong>prop drilling</strong>, and it earns a reputation as an anti-pattern that's
somewhat exaggerated in casual conversation &mdash; it's worth being precise about when it's a real problem and
when reaching for a "fix" is premature.</p>

{code_panel("JSX", '''
function App() {
  const [user, setUser] = useState(null);
  return <Layout user={user} />;
}
function Layout({ user }) {
  return <Sidebar user={user} />; // Layout never reads "user" itself
}
function Sidebar({ user }) {
  return <UserMenu user={user} />; // neither does Sidebar
}
function UserMenu({ user }) {
  return <span>{user.name}</span>; // finally used, three levels down
}
''', "prop-drilling.jsx")}

<p>Two or three levels of this, as shown above, is simply what explicit data flow looks like &mdash; it's
verbose, but every value's origin is traceable by reading the code, with no hidden wiring anywhere. It becomes a
genuine problem when the drilling depth grows large, when many unrelated props are drilled through the same long
chain simultaneously, or when a component in the middle of the chain has to be modified every time a distant
descendant's data needs change &mdash; at that point, the chain itself has become a maintenance burden independent
of the feature being built. That's the threshold where Context (7.3) or a state library (7.4) earns its added
complexity; below that threshold, they're often solving a problem you don't actually have yet.</p>
""")

    s3 = sub("p7-context-full", "7.3", "The Context API, in Full", "Context, in full", f"""
<p>Context lets a value skip the prop chain entirely: a <code class="inline">Provider</code> makes a value
available to every descendant in its subtree, and any of those descendants can read it directly with
<code class="inline">useContext</code> (introduced briefly in Part 5.7), no matter how deeply nested.</p>

{code_panel("JSX", '''
const UserContext = React.createContext(null);

function App() {
  const [user, setUser] = useState(null);
  return (
    <UserContext.Provider value={{ user, setUser }}>
      <Layout /> {/* no "user" prop needed anywhere in this chain now */}
    </UserContext.Provider>
  );
}

function UserMenu() {
  const { user } = useContext(UserContext); // reads directly, however deep it is
  return <span>{user?.name}</span>;
}
''', "context-full.jsx")}

<p>Providers can be nested, and a component reading context always gets the value from the <strong>nearest</strong>
matching Provider above it &mdash; an inner Provider for the same context effectively overrides an outer one for
everything inside it, which is occasionally useful for scoping a value (a themed section within an otherwise
differently-themed page, for instance).</p>

{callout("warn", "The real performance gotcha", '''
<p>Every component that calls <code class="inline">useContext</code> for a given context re-renders whenever
that Provider's <code class="inline">value</code> changes — <strong>in full</strong>, regardless of which
specific field inside that value the component actually uses. If a single context holds
<code class="inline">{{ user, theme, notifications }}</code> and only <code class="inline">notifications</code>
changes, every component reading that context re-renders, including ones that only ever look at
<code class="inline">user</code>. The two common fixes are splitting one large context into several
narrower ones (so a component only subscribes to the slice it actually needs), and memoizing the value object
itself with <code class="inline">useMemo</code> so a Provider's re-render doesn't manufacture a brand new object
reference on every pass when the underlying data hasn't actually changed.</p>
''')}
""")

    s4 = sub("p7-when-redux", "7.4", "When to Reach for Redux, Zustand, or Jotai", "External state libraries", f"""
<p>Context solves "how do I avoid drilling this value through many components," but it was never designed as a
full state-management solution, and doesn't include things like fine-grained update subscriptions, built-in
devtools, or a standard pattern for complex, cross-cutting state logic. For applications where state genuinely
outgrows what local state and Context comfortably handle, three popular philosophies dominate the ecosystem, each
trading off differently:</p>

{ref_table(["Library", "Core idea", "Trade-off"], [
    ["Redux", "A single global store, updated only through pure reducer functions dispatched actions (Part 5.6's pattern, applied app-wide).", "The most ceremony (actions, reducers, often middleware) in exchange for the most predictability, traceability, and mature devtools, including time-travel debugging."],
    ["Zustand", "A minimal hook-based store created with a plain function, read directly via a custom hook, with no Provider wrapping required.", "Dramatically less boilerplate than Redux, at the cost of some of the structural conventions Redux enforces by design."],
    ["Jotai", "Atomic state: many small, independent “atoms” instead of one big central object, composed together as needed.", "Excellent fine-grained re-render behavior (components only subscribe to the atoms they actually read) but a different mental model to learn than a single unified store."],
])}

<p>None of these replace Context or local <code class="inline">useState</code> outright &mdash; they solve a
different point on the same spectrum. A reasonable default progression, connecting directly back to 7.1 and 7.2:
start with local state; lift it up when siblings need to share it; reach for Context when drilling depth and
prop-chain maintenance genuinely become the bottleneck; and reach for one of these libraries when the sheer
volume or cross-cutting complexity of shared state makes even well-organized Context unwieldy to reason about.</p>

{keypoints("Part 7, wrapped up", [
    "Lifting state up means moving it to the nearest common ancestor of everything that needs it — the data itself doesn't change, only where in the tree it lives.",
    "Prop drilling is explicit, traceable data flow, not automatically a problem — it becomes one at real depth or volume, not at two or three levels.",
    "Context skips the prop chain but re-renders every consumer in full on any change to its value — split contexts or memoize the value to avoid over-rendering.",
    "Redux, Zustand, and Jotai occupy different points on a ceremony-vs-flexibility spectrum — reach for one when Context's simplicity stops scaling with your app's actual complexity."
])}
""")

    body = s1 + s2 + s3 + s4
    return part("part-7", "7", "Data Flow & State Management",
                 "Getting state to the components that need it, without over-engineering the ones that don't.",
                 body, prev=("part-6", "The Component Lifecycle, Through Hooks"), nxt=("part-8", "Forms, Refs & Escape Hatches"))
