# -*- coding: utf-8 -*-
from helpers import esc, code_panel, callout, keypoints, compare_grid, ref_table, sub, part

def build_part12():
    s1 = sub("p12-compound", "12.1", "Compound Components", "Compound components", f"""
<p>A compound component is a set of components designed to be used together, sharing implicit state through
context rather than requiring the parent to wire that state through explicit props to every child:</p>

{code_panel("JSX", '''
const SelectContext = React.createContext(null);

function Select({ children, value, onChange }) {
  return (
    <SelectContext.Provider value={{ value, onChange }}>
      <div className="select">{children}</div>
    </SelectContext.Provider>
  );
}

function Option({ value: optionValue, children }) {
  const { value, onChange } = useContext(SelectContext);
  return (
    <div
      className={optionValue === value ? 'option selected' : 'option'}
      onClick={() => onChange(optionValue)}
    >
      {children}
    </div>
  );
}
Select.Option = Option;

// Usage reads like a single, cohesive unit despite being several components:
<Select value={color} onChange={setColor}>
  <Select.Option value="red">Red</Select.Option>
  <Select.Option value="blue">Blue</Select.Option>
</Select>
''', "compound-components.jsx")}

<p>The payoff is API ergonomics: the consumer never has to manually pass <code class="inline">value</code> and
<code class="inline">onChange</code> down to every <code class="inline">Option</code> &mdash; Context (Part 7.3)
handles that invisibly, while the JSX at the call site stays declarative and readable as a single logical
unit.</p>
""")

    s2 = sub("p12-render-props", "12.2", "Render Props", "Render props", f"""
<p>A render prop is a prop whose value is a function that returns JSX &mdash; letting a component control
<em>when</em> and <em>with what data</em> something renders, while the consumer retains full control over
<em>what</em> actually gets rendered:</p>

{code_panel("JSX", '''
function MouseTracker({ render }) {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  function handleMove(e) {
    setPosition({ x: e.clientX, y: e.clientY });
  }

  return (
    <div onMouseMove={handleMove}>
      {render(position)} {/* the consumer decides what to do with position */}
    </div>
  );
}

// Usage:
<MouseTracker render={({ x, y }) => <p>Mouse at {x}, {y}</p>} />
''', "render-prop.jsx")}

<p>Before Hooks existed, render props (alongside Higher-Order Components, 12.3) were one of the two primary
patterns for sharing stateful logic across components without duplicating it &mdash; here, the mouse-tracking
logic lives in one place, and any number of consumers can reuse it with entirely different rendering output. A
custom Hook (Part 5.9) now covers the large majority of these use cases more directly, with no extra component
layer required, which is why render props show up far less in code written since Hooks became standard &mdash;
though the pattern remains genuinely useful in the narrower case where a component needs to control the
<em>rendering</em> itself, not just share logic (certain animation and virtualization libraries still use it for
exactly this reason).</p>
""")

    s3 = sub("p12-hoc", "12.3", "Higher-Order Components, and Why Hooks Replaced Most of Them", "Higher-order components", f"""
<p>A Higher-Order Component (HOC) is a function that takes a component and returns a new component with
additional behavior wrapped around it &mdash; the component equivalent of a decorator:</p>

{code_panel("JSX", '''
function withLoading(WrappedComponent) {
  return function WithLoading(props) {
    if (props.isLoading) return <p>Loading...</p>;
    return <WrappedComponent {...props} />;
  };
}

const ProductListWithLoading = withLoading(ProductList);
// Usage: <ProductListWithLoading isLoading={loading} products={products} />
''', "hoc.jsx")}

{callout("history", "Wrapper hell, and the ref problem", '''
<p>HOCs share the same class-component-era motivation as render props: reusing stateful logic without
duplicating it. Composing several HOCs around one component nests them visually (“wrapper hell” in
component-tree inspectors), makes props harder to trace back to their origin (a prop might be injected by any
of several wrapping HOCs), and refs don't pass through a HOC automatically — reaching a wrapped
component's ref requires the forwardRef pattern from Part 8.3, applied inside the HOC itself. Custom Hooks
sidestep every one of these problems at once: no extra component in the tree, no naming collisions between
injected props, and no ref-forwarding gymnastics, which is why they've displaced HOCs for the majority of
former use cases.</p>
''')}
""")

    s4 = sub("p12-container-presentational", "12.4", "Container/Presentational Split", "Container vs presentational", f"""
<p>This pattern separates two concerns into two different components: a "container" that handles data fetching
and business logic, and a "presentational" component that only knows how to render props it's handed, with no
awareness of where that data came from:</p>

{code_panel("JSX", '''
// Container: knows HOW to get the data
function ProductListContainer() {
  const [products, setProducts] = useState([]);
  useEffect(() => { fetchProducts().then(setProducts); }, []);
  return <ProductList products={products} />;
}

// Presentational: only knows how to DISPLAY data it's given
function ProductList({ products }) {
  return <ul>{products.map(p => <li key={p.id}>{p.name}</li>)}</ul>;
}
''', "container-presentational.jsx")}

<p>The presentational half becomes trivially reusable and testable in isolation &mdash; it has no dependencies on
a particular data source, so it's just as happy rendering mock data in a test or a design tool as real fetched
data in production. The rise of custom Hooks has reduced how often this split needs its own dedicated
<em>component</em>, though: a <code class="inline">useProducts()</code> custom Hook can carry exactly the same
"how to get the data" responsibility the container component used to hold, without needing a wrapping component
at all &mdash; the presentational component can call that Hook directly and stay just as reusable.</p>
""")

    s5 = sub("p12-typescript", "12.5", "TypeScript With React", "TypeScript with React", f"""
<p>TypeScript adds static types on top of everything covered so far, without changing any of React's actual
runtime behavior. A handful of patterns cover the overwhelming majority of everyday use:</p>

{code_panel("TypeScript", '''
interface ProductCardProps {
  name: string;
  price: number;
  onAddToCart?: () => void; // optional prop, marked with ?
}

function ProductCard({ name, price, onAddToCart }: ProductCardProps) {
  return <div>{name}: ${price.toFixed(2)}</div>;
}

// Typing useState: TypeScript infers the type from the initial value automatically,
// but a generic is useful when the initial value doesn't cover every later possibility:
const [user, setUser] = useState<User | null>(null);

// Typing an event handler:
function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
  console.log(e.target.value);
}

// Typing children: React.ReactNode covers anything JSX can legally render
interface CardProps {
  children: React.ReactNode;
}
''', "typed-react.tsx")}

<p>The type system doesn't add any new mental model beyond what this entire guide has already covered &mdash;
props are still read-only data (Part 3.3), <code class="inline">useState</code> still works exactly as described
in Part 5.1. What it adds is compile-time verification that the props a component expects match what it's
actually given, catching a category of bug (a missing required prop, a typo'd property name) before the code
ever runs, rather than as a runtime error or, worse, a silent <code class="inline">undefined</code>.</p>

{keypoints("Part 12, wrapped up", [
    "Compound components share implicit state via context so a family of components can be used together with a clean, cohesive API.",
    "Render props and Higher-Order Components were the two pre-Hooks patterns for sharing stateful logic — custom Hooks have replaced most, though not all, of their former use cases.",
    "The container/presentational split separates data logic from display; a custom Hook can now carry the “container” half without a wrapping component.",
    "TypeScript adds compile-time type checking on top of React without changing any runtime behavior — the same components, props, and Hooks, just verified before they run."
])}
""")

    body = s1 + s2 + s3 + s4 + s5
    return part("part-12", "12", "Patterns & Idioms",
                 "Recurring shapes experienced React codebases converge on — and the ones Hooks made largely obsolete.",
                 body, prev=("part-11", "React vs. Plain HTML, CSS, and JS"), nxt=("part-13", "Limitations & Honest Critique"))
