# -*- coding: utf-8 -*-
from helpers import esc, code_panel, callout, keypoints, compare_grid, ref_table, sub, part

TREE_SVG = """<svg class="diagram" viewBox="0 0 640 260" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowDown" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="var(--accent-dim)"/>
    </marker>
    <marker id="arrowUp" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="var(--amber)"/>
    </marker>
  </defs>
  <style>
    .n{ fill:var(--bg-card); stroke:var(--rule); }
    .nl{ font-size:12px; }
    .down{ stroke:var(--accent-dim); stroke-width:1.5; fill:none; marker-end:url(#arrowDown); }
    .up{ stroke:var(--amber); stroke-width:1.5; fill:none; stroke-dasharray:4 3; marker-end:url(#arrowUp); }
  </style>

  <rect class="n" x="255" y="10" width="130" height="46" rx="8"/>
  <text class="nl" x="320" y="38" text-anchor="middle">&lt;App /&gt;</text>

  <path class="down" d="M300,56 L165,104"/>
  <path class="up"   d="M175,104 L305,58"/>
  <path class="down" d="M340,56 L470,104"/>
  <path class="up"   d="M480,104 L350,58"/>

  <rect class="n" x="95"  y="108" width="140" height="46" rx="8"/>
  <text class="nl" x="165" y="136" text-anchor="middle">&lt;CartBadge /&gt;</text>

  <rect class="n" x="400" y="108" width="150" height="46" rx="8"/>
  <text class="nl" x="475" y="136" text-anchor="middle">&lt;ProductList /&gt;</text>

  <path class="down" d="M440,154 L360,202"/>
  <path class="up"   d="M368,202 L448,156"/>
  <path class="down" d="M500,154 L560,202"/>
  <path class="up"   d="M568,202 L508,156"/>

  <rect class="n" x="290" y="206" width="150" height="46" rx="8"/>
  <text class="nl" x="365" y="234" text-anchor="middle">&lt;ProductCard /&gt;</text>

  <rect class="n" x="510" y="206" width="120" height="46" rx="8"/>
  <text class="nl" x="570" y="234" text-anchor="middle">&lt;AddButton /&gt;</text>

  <text x="10" y="20" style="font-size:11px; fill:var(--accent-dim);">&#8594; props (data, always downward)</text>
  <text x="10" y="36" style="font-size:11px; fill:var(--amber);">&#8594; callback props, called upward (e.g. onAddToCart)</text>
</svg>"""

def build_part3():
    s1 = sub("p3-function-components", "3.1", "Function Components, the Modern Default", "Function components", f"""
<p>Strip away every convention, and a React component is nothing more exotic than a JavaScript function that
returns a description of UI (the createElement tree from Part 2.1) and follows exactly one naming rule:</p>

{code_panel("JSX", '''
function ProductCard({ name, price }) {
  return (
    <div className="card">
      <h3>{name}</h3>
      <p>${price.toFixed(2)}</p>
    </div>
  );
}
''', "ProductCard.jsx")}

<p>That naming rule &mdash; <strong>PascalCase</strong> &mdash; isn't a style preference; it's load-bearing, and
Part 2.7 already showed why: JSX's compiler decides whether <code class="inline">&lt;ProductCard /&gt;</code>
means "call the ProductCard function" or "create a literal HTML tag named productcard" purely by checking whether
the first letter is capitalized. Name a component <code class="inline">productCard</code> and the compiler will
silently treat it as an unknown HTML element instead of your function, with no error &mdash; just a component
that mysteriously never renders its content.</p>

<p>The parameter is, by convention, a single object &mdash; <code class="inline">props</code> &mdash; almost
always destructured directly in the function signature as shown above (<code class="inline">{'{'} name, price {'}'}
</code> instead of <code class="inline">props</code> then <code class="inline">props.name</code> everywhere).
This isn't a special React feature; it's ordinary JavaScript destructuring syntax, applied to the first function
argument. React itself never sees "name" or "price" as separate things &mdash; it always passes one props object;
destructuring is just how you conveniently unpack it.</p>
""")

    s2 = sub("p3-class-components", "3.2", "Class Components (Legacy, Still Worth Knowing)", "Class components", f"""
<p>Before Hooks (Part 5) existed, function components couldn't hold state or run side effects at all &mdash; they
were called "stateless functional components" for exactly that reason. Anything stateful had to be written as a
<strong>class component</strong>, extending <code class="inline">React.Component</code>:</p>

{code_panel("JSX", '''
class Counter extends React.Component {
  constructor(props) {
    super(props);
    this.state = { count: 0 };
    this.handleClick = this.handleClick.bind(this); // see the note below
  }

  handleClick() {
    this.setState({ count: this.state.count + 1 });
  }

  componentDidMount() {
    console.log('Counter is now in the DOM');
  }

  componentWillUnmount() {
    console.log('Counter is about to be removed');
  }

  render() {
    return <button onClick={this.handleClick}>Count: {this.state.count}</button>;
  }
}
''', "Counter.jsx")}

<p>You will still encounter class components constantly in older codebases, tutorials, and libraries with
long histories, so recognizing this shape matters even though you're unlikely to write new ones. A few
things worth being able to read at a glance: <code class="inline">this.state</code> holds all state as a single
object; <code class="inline">this.setState()</code> merges in a partial update and schedules a re-render;
<code class="inline">render()</code> is the method that returns JSX (the equivalent of a function component's own
return value); and named lifecycle methods (<code class="inline">componentDidMount</code>,
<code class="inline">componentDidUpdate</code>, <code class="inline">componentWillUnmount</code>) are where side
effects live &mdash; Part 6.1 maps each of these directly onto its Hook equivalent.</p>

{callout("history", "The 'this' problem, and why it mattered", '''
<p>Notice the <code class="inline">.bind(this)</code> call in the constructor above. In JavaScript, a method
detached from the object it's called on (which is exactly what happens when you pass
<code class="inline">this.handleClick</code> as an <code class="inline">onClick</code> callback) loses its
<code class="inline">this</code> binding by default. Forgetting to bind was one of the single most common
beginner bugs in React's class-component era — <code class="inline">this.setState</code> would fail
inside an unbound handler with a confusing "cannot read property of undefined" error. This specific,
persistent source of friction is one of several concrete reasons the React team went looking for something
better — which Part 5 picks up directly.</p>
''')}
""")

    s3 = sub("p3-props", "3.3", "Props: Read-Only Data Flowing Down", "Props are read-only", f"""
<p>Props are how a parent component passes data to a child. The single rule that governs everything about them:
<strong>props are read-only from the receiving component's point of view.</strong> A component must never mutate
its own <code class="inline">props</code>:</p>

{code_panel("JSX", '''
function ProductCard({ name, price }) {
  price = price * 1.1; // NEVER do this — mutating a prop directly
  return <div>{name}: ${price}</div>;
}
''', "dont-do-this.jsx")}

<p>This isn't a stylistic nitpick enforced by convention alone &mdash; React assumes it. If a discount calculation
needs to happen, compute a new value and use that, without touching the incoming prop itself:</p>

{code_panel("JSX", '''
function ProductCard({ name, price }) {
  const discountedPrice = price * 1.1; // a new value, not a mutation of the original
  return <div>{name}: ${discountedPrice.toFixed(2)}</div>;
}
''', "correct.jsx")}

<p>A few supporting conventions round out how props are used day to day. <strong>Default values</strong> use
ordinary JavaScript default-parameter syntax during destructuring:</p>

{code_panel("JSX", '''
function Avatar({ size = 40, src }) {
  return <img src={src} width={size} height={size} />;
}
''', "defaults.jsx")}

<p>And the <strong>spread operator</strong> is commonly used to forward a whole bag of props through to an
underlying element or component, when a wrapper doesn't need to inspect most of what it receives:</p>

{code_panel("JSX", '''
function PrimaryButton(props) {
  return <button className="btn-primary" {...props} />;
  // spreads onClick, disabled, children, or anything else the caller passed,
  // straight onto the real <button>, without this component needing to name each one
}
''', "spread.jsx")}
""")

    s4 = sub("p3-children-composition", "3.4", "Children as Props, Composition Over Inheritance", "Composition, not inheritance", f"""
<p>Whatever you nest between a component's opening and closing tags is passed to that component as a special prop
named <code class="inline">children</code> &mdash; it works exactly like any other prop, it's just populated
implicitly by JSX nesting instead of an explicit attribute:</p>

{code_panel("JSX", '''
function Card({ children }) {
  return <div className="card">{children}</div>;
}

// Usage:
<Card>
  <h3>Wireless Mouse</h3>
  <p>$29.99</p>
</Card>
// Card has no idea what it's wrapping — it just renders whatever it's handed.
''', "children-prop.jsx")}

<p>This single mechanism is doing more work than it looks like. React deliberately provides <strong>no class
inheritance model for components</strong> &mdash; there is no <code class="inline">class SpecialCard extends Card
</code> pattern anywhere in idiomatic React, even though class components technically support JavaScript's
<code class="inline">extends</code> keyword for other purposes. Instead, every case where another UI library
might reach for inheritance, React reaches for <strong>composition</strong>: wrapping components inside other
components, and passing behavior down through props (including the <code class="inline">children</code> prop, and
functions passed as props for more specific customization points).</p>

{callout("note", "Why composition won out over inheritance here", '''
<p>Inheritance hierarchies create tight, fragile coupling: a change to a base class can silently break every
subclass, and a component that needs "some, but not all" of a parent's behavior often ends up overriding
methods in increasingly awkward ways (this is a well-known problem in object-oriented design generally, often
called the "fragile base class problem," not something unique to UI code). Composition avoids it structurally
— a Card component that wraps arbitrary children has no idea what's inside it and doesn't need to; there's
no shared base class whose internals both sides depend on. You compose small, independent pieces instead of
inheriting from increasingly specific ones.</p>
''')}
""")

    s5 = sub("p3-tree-unidirectional", "3.5", "The Component Tree and Unidirectional Data Flow", "Unidirectional data flow", f"""
<p>Every React application is, structurally, a single tree of components, rooted at whatever you pass to
<code class="inline">createRoot(...).render()</code>. Data moves through that tree in exactly one direction: down,
from parent to child, as props. There is no built-in mechanism for a child to directly modify a value that lives
in its parent.</p>

{TREE_SVG}

<p>This is a deliberate constraint, not a missing feature. Section 0.4 covered AngularJS's two-way data binding,
where a child input changing its value could reach up and directly modify a parent's data — convenient to
write, but it meant data could change from almost anywhere, making "what caused this value to change" often
genuinely hard to trace in a large application. React's answer is that a child that needs to cause a change in
its parent's data does so indirectly: <strong>the parent passes a callback function down as a prop, and the
child calls that function.</strong> The data itself still only ever flows one way &mdash; what flows upward is
just a function call, a request, not a direct mutation.</p>

{code_panel("JSX", '''
function ProductList({ products, onAddToCart }) {
  return products.map(p => (
    <ProductCard key={p.id} product={p} onAdd={() => onAddToCart(p.id)} />
    // onAddToCart flows DOWN as a prop; calling it is how the child
    // triggers a change that actually lives in a parent/ancestor's state.
  ));
}
''', "unidirectional.jsx")}

{keypoints("Part 3, wrapped up", [
    "A component is a function (nearly always, today) that takes props and returns a UI description — PascalCase naming is what tells the JSX compiler it's your function, not an HTML tag.",
    "Props are read-only; never mutate them, compute new values instead.",
    "children is just a prop, populated by JSX nesting — and it's the mechanism composition uses in place of the inheritance React deliberately doesn't offer for components.",
    "Data flows down the component tree as props; a child causes change in an ancestor only by calling a function that ancestor handed it — never by reaching up and mutating something directly."
])}
""")

    body = s1 + s2 + s3 + s4 + s5
    return part("part-3", "3", "Components & Composition",
                 "The unit of reuse in React, and the rules that make composing them safe.",
                 body, prev=("part-2", "JSX: Syntax and Semantics"), nxt=("part-4", "The Virtual DOM & Reconciliation"))
