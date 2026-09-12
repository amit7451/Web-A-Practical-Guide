# -*- coding: utf-8 -*-
from helpers import part

GLOSSARY_TERMS = [
    ("Declarative", "Code that describes the desired end state, without referencing or depending on whatever state came before it. Contrast with imperative. See 1.2."),
    ("Imperative", "Code that describes the step-by-step instructions for transforming a previous state into a new one. See 1.2."),
    ("Component", "A function (or, historically, a class) that takes props/state as input and returns a description of UI. See 1.1 and Part 3."),
    ("Class component", "The pre-Hooks way of writing a stateful component, using this.state, this.setState, and named lifecycle methods. See 3.2."),
    ("Props", "Read-only data passed into a component from its parent. Covered fully in Part 3."),
    ("children", "A special prop populated implicitly by whatever is nested between a component's opening and closing JSX tags. See 3.4."),
    ("State", "Data a component owns and can change over time, which causes it to re-render when updated. Covered fully in Part 5."),
    ("Unidirectional data flow", "The rule that data only flows down the component tree as props; a child can only affect an ancestor's data by calling a function that ancestor passed down. See 3.5."),
    ("Virtual DOM", "A lightweight, plain-JavaScript-object description of the UI that React compares against the previous description to compute minimal real DOM changes. See 1.4 and 4.1."),
    ("Reconciliation", "The process of comparing a new virtual DOM tree to the previous one and determining the minimal real DOM operations needed. Full treatment in Part 4."),
    ("Key", "A special prop that lets React match array items to rendered elements across re-renders, used by the reconciler's diffing algorithm. See 2.6 and 4.2."),
    ("Fragment", "A JSX root node (<>...</>) that groups children without rendering an extra real DOM element. See 2.5."),
    ("Render phase", "The part of an update where React calls component functions and computes a diff; interruptible, and must be free of side effects. See 4.3."),
    ("Commit phase", "The part of an update where React applies changes to the real DOM; synchronous and uninterruptible. See 4.3."),
    ("Fiber", "The reconciler architecture React adopted in version 16, representing rendering work as an explicit, interruptible linked structure instead of relying on the JS call stack. See 1.6 and 4.4."),
    ("Lane", "React 18's mechanism for tagging updates with a priority level, letting urgent updates interrupt in-progress lower-priority rendering work. See 4.5."),
    ("Batching", "Grouping multiple state updates from one logical event into a single re-render instead of one re-render per update. See 4.6."),
    ("Hooks", "Functions (useState, useEffect, and others) that let function components hold state and run side effects, introduced in React 16.8. Full treatment in Part 5."),
    ("Custom Hook", "An ordinary function, named with a use prefix, that calls built-in Hooks internally to share stateful logic across components. See 5.9."),
    ("Rules of Hooks", "The requirement that Hooks only be called at a component's top level, in the same order every render \u2014 required because Hooks are matched to their stored state by call order. See 5.8."),
    ("Stale closure", "A bug where a function (often inside useEffect) captures a variable's value from the render it was defined in, and that value never updates on subsequent renders. See 6.4."),
    ("Strict Mode", "A development-only React mode that intentionally double-invokes renders and effects to surface missing or incorrect cleanup. See 6.2."),
    ("Memoization", "Caching a computed value or function reference between renders so it isn't unnecessarily recreated. See 5.5 and 9.2."),
    ("React.memo", "A wrapper that skips re-rendering a component when its props are shallowly equal to their previous values. See 9.2."),
    ("Controlled component", "A form input whose value is owned by React state, kept in sync via value and onChange. See 8.1."),
    ("Uncontrolled component", "A form input whose value is owned by the DOM itself, read via a ref only when needed. See 8.1."),
    ("Portal", "A way to render a component's output into a different real DOM node than its parent renders into, while keeping it in the same React tree for events and context. See 8.4."),
    ("Suspense", "A component that declares a fallback UI to show while a child (a lazily-loaded component, or in-progress data) isn't ready yet. See 9.4."),
    ("Concurrent rendering", "React 18's system for marking updates as interruptible/low-priority (via startTransition and useDeferredValue), built on Fiber's lane mechanism. See 4.5 and 9.3."),
    ("Hydration", "The process by which client-side React attaches event handling and state to server-rendered HTML instead of rebuilding it from scratch. See 10.2."),
    ("Server-Side Rendering (SSR)", "Rendering a component tree to HTML on the server, per request, before sending it to the browser. See 10.2."),
    ("Static Site Generation (SSG)", "Rendering to HTML once, at build time, and serving identical static files to every visitor. See 10.3."),
    ("React Server Components (RSC)", "Components that run only on the server and never ship their JavaScript to the client at all. See 10.4."),
    ("Client Component", "In an RSC-enabled app, a component explicitly marked with 'use client' that can use state, effects, and browser APIs. See 10.4."),
    ("Prop drilling", "Passing a value through several intermediate components that don't use it themselves, purely so a distant descendant can receive it. See 7.2."),
    ("Lifting state up", "Moving state to the nearest common ancestor of every component that needs to read or change it. See 7.1."),
    ("Context", "A mechanism for making a value available to an entire subtree without passing it through every intermediate component as a prop. See 5.7 and 7.3."),
    ("Compound component", "A set of components designed to be used together, sharing implicit state through context. See 12.1."),
    ("Render prop", "A prop whose value is a function returning JSX, letting a component control when/with-what-data something renders. See 12.2."),
    ("Higher-Order Component (HOC)", "A function that takes a component and returns a new component with additional behavior wrapped around it. See 12.3."),
    ("N\u00d7M synchronization problem", "The pattern where N places that change a piece of state and M places that display it require N\u00d7M hand-written, hand-maintained update calls in a purely imperative system. See 0.3."),
    ("Digest cycle", "AngularJS's mechanism for detecting changes: repeatedly re-evaluating every watched expression (\u201cdirty-checking\u201d) until a full pass produces no differences. See 0.4."),
    ("XHP", "A Facebook PHP extension that let markup be embedded as a first-class value in server-side code; a direct conceptual ancestor of JSX. See 0.5."),
    ("JSX", "A markup-like syntax extension to JavaScript that compiles to React.createElement (or jsx()) calls. Introduced conceptually in 1.2, full syntax in Part 2."),
]

def build_glossary():
    terms_html = "".join(
        f'<div class="glossary-term"><dt id="gl-{i}">{t}</dt><dd>{d}</dd></div>'
        for i, (t, d) in enumerate(GLOSSARY_TERMS)
    )
    body = f"""
{terms_html}
"""
    return part("part-ref", "\u00a7", "Reference & Glossary",
                 "Every precise term this guide defines, in one place, cross-referenced back to where each one was introduced.",
                 body, prev=("part-13","Limitations & Honest Critique"))

