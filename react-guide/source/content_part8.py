# -*- coding: utf-8 -*-
from helpers import esc, code_panel, callout, keypoints, compare_grid, ref_table, sub, part

def build_part8():
    s1 = sub("p8-controlled-uncontrolled", "8.1", "Controlled vs. Uncontrolled Inputs", "Controlled vs uncontrolled", f"""
<p>Every form input in React falls into one of two categories, distinguished by a single question: <strong>who
owns the current value &mdash; React state, or the DOM node itself?</strong></p>

{compare_grid(
    "Controlled — React state owns the value", "jsx", '''
function ControlledInput() {
  const [value, setValue] = useState('');
  return (
    <input
      value={value}
      onChange={e => setValue(e.target.value)}
    />
  );
  // The DOM input's displayed value is FORCED to match React state on
  // every render. React re-renders on every keystroke.
}
''',
    "Uncontrolled — the DOM owns the value", "jsx", '''
function UncontrolledInput() {
  const inputRef = useRef(null);

  function handleSubmit() {
    console.log(inputRef.current.value); // read only when needed
  }

  return <input ref={inputRef} defaultValue="" />;
  // React never re-renders as the user types; the DOM node
  // just holds its own value like a plain HTML form always has.
}
''')}

<p>A controlled input gives you validation-as-you-type, the ability to reformat or reject characters immediately,
and a single source of truth that's trivially easy to reason about &mdash; at the cost of a re-render on every
keystroke. An uncontrolled input is simpler, involves no re-renders while typing, and can be meaningfully faster
for very large forms with many fields &mdash; at the cost of needing a ref to reach in and read the value
whenever you actually need it, and losing the ability to react to each keystroke as it happens.</p>
""")

    s2 = sub("p8-dom-vs-value-refs", "8.2", "DOM Refs vs. Value Refs", "Refs, form-specific view", f"""
<p>Part 5.4 introduced <code class="inline">useRef</code>'s two unrelated jobs in general terms; forms are where
the DOM-node job earns its keep most often. Two everyday patterns:</p>

{code_panel("JSX", '''
function LoginForm() {
  const emailRef = useRef(null);
  const passwordRef = useRef(null);

  function handleSubmit(e) {
    e.preventDefault();
    // Read uncontrolled values only at the moment you need them —
    // no state, no re-renders while the user was typing either field.
    login(emailRef.current.value, passwordRef.current.value);
  }

  function focusEmailOnError() {
    emailRef.current.focus(); // imperatively move focus, something
    // state alone has no vocabulary for — focus is a DOM concept.
  }

  return (
    <form onSubmit={handleSubmit}>
      <input ref={emailRef} type="email" />
      <input ref={passwordRef} type="password" />
    </form>
  );
}
''', "form-refs.jsx")}

<p>Both patterns lean on the same underlying mechanism (a persistent, mutable
<code class="inline">.current</code> that survives renders without causing them), applied to the specific,
common form needs of reading a value on submit and moving focus programmatically &mdash; something no amount of
state modeling can express, because focus is a property of the actual DOM, not a piece of your application's
data.</p>
""")

    s3 = sub("p8-forwardref", "8.3", "forwardRef and useImperativeHandle", "forwardRef & imperative handles", f"""
<p>Passing a <code class="inline">ref</code> to a plain host element like <code class="inline">&lt;input /&gt;
</code> just works, as shown above. Passing a <code class="inline">ref</code> to your <em>own</em> custom
component historically did not &mdash; <code class="inline">ref</code> was treated specially by React and, unlike
every other prop, wasn't automatically forwarded into a function component's <code class="inline">props</code>
object. <code class="inline">forwardRef</code> existed specifically to opt a component into receiving one:</p>

{code_panel("JSX", '''
const FancyInput = React.forwardRef(function FancyInput(props, ref) {
  return <input ref={ref} className="fancy" {...props} />;
});

// Now a parent CAN get a ref pointing at the underlying <input>:
function Form() {
  const inputRef = useRef(null);
  return <FancyInput ref={inputRef} />;
}
''', "forwardRef.jsx")}

<p><code class="inline">useImperativeHandle</code> goes one step further: instead of exposing the raw DOM node
itself, it lets a component control exactly what a parent's ref actually receives &mdash; useful when you want to
expose a narrow, deliberate API (just a <code class="inline">.focus()</code> method, say) rather than the entire
underlying DOM node with all its capabilities:</p>

{code_panel("JSX", '''
const FancyInput = React.forwardRef(function FancyInput(props, ref) {
  const realInputRef = useRef(null);

  useImperativeHandle(ref, () => ({
    focus() { realInputRef.current.focus(); },
    clear() { realInputRef.current.value = ''; }
    // The parent's ref.current is now THIS object, not the raw <input>—
    // it can call .focus() or .clear() but can't reach in and, say,
    // read .value directly or change unrelated DOM attributes.
  }));

  return <input ref={realInputRef} {...props} />;
});
''', "useImperativeHandle.jsx")}

{callout("history", "React 19 simplified the common case", '''
<p>Starting in React 19, function components can receive <code class="inline">ref</code> as a plain prop
directly, without wrapping the component in <code class="inline">forwardRef</code> at all, for the common case
of simply forwarding it to an underlying DOM node. <code class="inline">forwardRef</code> still exists and
still works (and <code class="inline">useImperativeHandle</code> is unaffected), but a meaningful share of its
historical use — the plain pass-through case shown in the first example above — no longer strictly
requires it.</p>
''')}
""")

    s4 = sub("p8-portals", "8.4", "Portals: Rendering Outside the Parent Tree", "Portals", f"""
<p>A portal renders a component's output into a different real DOM node than the one its parent renders into
&mdash; useful whenever a piece of UI needs to visually escape a container's <code class="inline">overflow:
hidden</code>, a constrained <code class="inline">z-index</code> stacking context, or similar CSS containment,
which is exactly the situation modals, tooltips, and dropdown menus tend to run into.</p>

{code_panel("JSX", '''
function Modal({ children }) {
  return ReactDOM.createPortal(
    <div className="modal-overlay">{children}</div>,
    document.getElementById('modal-root') // a DOM node OUTSIDE the app's normal root
  );
}
''', "portal.jsx")}

<p>The one detail worth being precise about: a portal changes <em>where in the real DOM</em> the content is
rendered, but it does not remove that content from the <strong>React</strong> tree. Event bubbling, context
values, and error boundaries all still follow the component tree exactly as if no portal were involved &mdash; a
click inside a portaled modal will still bubble up through its React-tree ancestors' event handlers, even though,
in the actual DOM, that click physically originated from a completely different branch of the document.</p>

{keypoints("Part 8, wrapped up", [
    "Controlled inputs are owned by React state (re-render on every change); uncontrolled inputs are owned by the DOM itself (read via ref only when needed).",
    "useRef's DOM-node job is how forms do the things state can't model directly — reading a value once, moving focus imperatively.",
    "forwardRef opts a custom component into receiving a ref at all; useImperativeHandle controls exactly what that ref exposes, rather than handing over the raw DOM node.",
    "A portal changes where content renders in the real DOM, but the React tree — and everything that depends on it, like event bubbling and context — stays exactly as it would without the portal."
])}
""")

    body = s1 + s2 + s3 + s4
    return part("part-8", "8", "Forms, Refs & Escape Hatches",
                 "The deliberate, narrow exceptions to “never touch the DOM directly.”",
                 body, prev=("part-7", "Data Flow & State Management"), nxt=("part-9", "The Performance Model"))
