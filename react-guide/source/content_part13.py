# -*- coding: utf-8 -*-
from helpers import esc, code_panel, callout, keypoints, compare_grid, ref_table, sub, part

def build_part13():
    s1 = sub("p13-learning-curve", "13.1", "The Learning Curve and Conceptual Overhead", "Learning curve", f"""
<p>Take an honest inventory of what this guide alone has required to reach this point: JSX's compilation model
(Part 2), the reconciler and Fiber (Part 4), the Hooks slot-list mechanism and its non-negotiable rules
(Part 5), closures and their staleness failure mode (Part 6), and at least a working notion of when to lift
state versus reach for Context (Part 7). None of this is optional background knowledge for "real" React
development &mdash; a developer who doesn't understand why an effect's dependency array matters, or why a
conditional Hook call breaks silently, will eventually hit exactly those walls in production code.</p>

<p>Compare this to Part 0.2's jQuery counter: <code class="inline">$('#btn').on('click', fn)</code> requires
none of that conceptual scaffolding to use correctly on day one. React's learning curve is real, front-loaded,
and steeper than "add a script tag and start" &mdash; a genuine cost, not a myth to be dismissed, even though the
payoff at scale (this guide's whole argument, from Part 0 onward) is also real.</p>
""")

    s2 = sub("p13-dependency-array-tax", "13.2", "Boilerplate and the Dependency-Array Tax", "The dependency-array tax", f"""
<p>Part 6.4 showed the stale-closure bug and its fix. Living with that fix day to day has a recurring cost of its
own: every <code class="inline">useEffect</code>, <code class="inline">useMemo</code>, and
<code class="inline">useCallback</code> call requires an accurate dependency array, and keeping one accurate as a
component evolves is genuine, ongoing friction. Add a new variable your effect reads, and you must remember to
add it to the array too &mdash; miss it, and you've reintroduced Part 6.4's exact bug. The
<code class="inline">exhaustive-deps</code> lint rule catches this, but its fixes are sometimes exactly what you
don't want (wrapping a function in <code class="inline">useCallback</code> purely to satisfy the linter, not
because reference stability actually matters there), leading to a real, commonly-reported pattern of developers
either fighting the linter or silencing it, neither of which is a comfortable place to be.</p>
""")

    s3 = sub("p13-not-batteries", "13.3", "Not Batteries-Included: Routing and Data Fetching", "Not batteries-included", f"""
<p>Part 1.3 described this as a deliberate design choice, and it is &mdash; but a deliberate choice can still be a
real cost to whoever pays it. Starting a new React project means deciding on a router, a data-fetching strategy,
and often a rendering framework (Part 10.5), <em>before</em> writing a single line of actual application logic.
Compare this to a batteries-included framework where those decisions are made for you. The React ecosystem's
answer to this criticism has increasingly been "use a framework built on React, like Next.js" &mdash; which is a
legitimate answer, but it's also a concession that plain React alone doesn't want to, and doesn't, solve this
problem.</p>
""")

    s4 = sub("p13-perf-footguns", "13.4", "Performance Footguns: Over-Rendering and Unstable References", "Performance footguns", f"""
<p>Part 9.2 showed exactly how easy it is to accidentally defeat <code class="inline">React.memo</code>: pass a
single new inline object, array, or arrow function as a prop, and memoization silently stops working, with no
warning, no error, and no obvious symptom beyond "this feels slower than it should." This is a sharp edge that
specifically punishes code that <em>looks</em> completely ordinary &mdash; an inline
<code class="inline">onClick={{() =&gt; ...}}</code> is one of the most natural things to write in JSX, and it's
also, in a memoized subtree, a performance bug. Diagnosing this reliably requires the Profiler workflow from Part
9.5; it is not something that announces itself.</p>
""")

    s5 = sub("p13-bundle-size", "13.5", "Bundle Size and Runtime Cost", "Bundle size & runtime cost", f"""
<p>React and ReactDOM together ship a real, non-trivial amount of JavaScript to every client under plain CSR
(Part 10.1) &mdash; the reconciler, the Hooks engine, and the rest of the runtime described throughout Part 4 and
5 all have to be downloaded, parsed, and executed before your application code even starts running. Compiler-based
alternatives like Svelte or Solid take a meaningfully different approach: they compile away most of their
"framework" at build time, shipping little to no comparable runtime to the client at all. This is a genuine,
measurable trade-off, not a matter of opinion &mdash; React's declarative, Fiber-based reconciliation model
(Part 4.4) is powerful precisely because it's a general-purpose runtime engine, and general-purpose runtime
engines cost bytes that a narrower, compile-time approach can sometimes avoid. React Server Components (Part
10.4) are a direct, partial response to this specific criticism, by reducing how much of a tree needs that
runtime shipped to the client at all.</p>
""")

    s6 = sub("p13-churn", "13.6", "API Churn and Migration Fatigue", "API churn & migration fatigue", f"""
<p>Part 1.6's timeline reads, in retrospect, like a tidy sequence of well-motivated improvements. Living through
it as a maintainer of an existing codebase felt different: migrating a large class-component codebase to Hooks
(Part 3.2's history callout) was genuinely substantial work with no automatic upgrade path, undertaken because
the ecosystem and new features increasingly assumed Hooks going forward, not because the old code had stopped
working. More recently, Create React App &mdash; for years the standard, officially-recommended way to start a
new React project &mdash; was <strong>formally deprecated by the React team in February 2025</strong>, with
guidance to migrate to a framework (Next.js, Remix) or a build tool (Vite) instead. A tool the official docs
pointed newcomers to for the better part of a decade is no longer the recommended starting point, and existing
projects built on it now face a real migration decision. This kind of churn is a recurring, legitimate complaint
about working in the React ecosystem long-term, distinct from any single change being a bad idea on its own
merits.</p>
""")

    s7 = sub("p13-seo-ssr", "13.7", "SEO and SSR: Historical Pain and Current State", "SEO & SSR, then and now", f"""
<p>Early React (roughly 2013&ndash;2016), used purely as CSR (Part 10.1), had a real SEO problem: search crawlers
of that era frequently could not execute JavaScript, meaning a pure client-rendered React page could appear
functionally blank to a crawler that never saw the content a real visitor's browser would render. This is
substantially less true today &mdash; major search crawlers now execute JavaScript as a matter of course &mdash;
but "substantially less true" is not "entirely solved," and crawler JavaScript execution can still be slower,
rate-limited, or less reliable than reading plain HTML directly. The honest, complete state of this criticism
today: SSR, SSG, and RSC (Part 10) directly and effectively solve it by sending real HTML immediately, but doing
so requires deliberately choosing and correctly configuring one of those rendering models &mdash; something a
plain static HTML page never had to think about in the first place, because it was already exactly what
crawlers, and users on slow connections, wanted by default.</p>
""")

    s8 = sub("p13-when-not", "13.8", "When Not to Choose React", "When not to choose React", f"""
<p>Every limitation above points toward the same honest conclusion: React earns its complexity when an
application's interactivity and state-management needs genuinely require what Parts 1 through 9 describe.
Plenty of real projects don't reach that bar, and choosing React for them means paying real costs from this
Part for benefits the project will never actually use.</p>

{ref_table(["If your project is mostly this…", "…consider this instead"], [
    ["A mostly-static content site — a blog, a marketing page, documentation", "Plain HTML/CSS, or a static site generator with no client-side framework at all. There's no meaningful “state” for React's model to manage in the first place."],
    ["One or two small interactive widgets on an otherwise static page", "Vanilla JavaScript, or a minimal library (Alpine.js and similar) — the full weight of Part 13.5's bundle cost isn't justified for a single dropdown or accordion."],
    ["A team without existing JavaScript build-tooling experience, on a tight timeline", "A simpler stack the team can ship confidently now — Part 13.1's learning curve is a real, current-project cost, not just a one-time investment that always pays off on schedule."],
    ["An application with genuinely complex, interdependent client-side state and interactivity", "This is, honestly, exactly what Parts 0 through 9 of this guide describe React being built for — the case where React's costs are worth paying."],
])}

{keypoints("Part 13, wrapped up — and the guide's closing point", [
    "The learning curve, the dependency-array tax, and API churn are real, ongoing costs — not myths, and not fully offset just because the underlying design decisions were individually well-motivated.",
    "React's library-not-framework stance (Part 1.3) and its runtime-based reconciliation (Part 4) each have a direct, named cost: ecosystem decision fatigue, and bundle size, respectively.",
    "Old criticisms (SEO, class-component ceremony) have real, current fixes (SSR/RSC, Hooks) — but the fixes each carry their own new complexity, rather than making the original problem disappear for free.",
    "The right question is never “is React good,” it's “does this specific project's complexity match what React costs to adopt” — and for a large share of real projects, honestly, the answer is no."
])}
""")

    body = s1 + s2 + s3 + s4 + s5 + s6 + s7 + s8
    return part("part-13", "13", "Limitations & Honest Critique",
                 "Where React genuinely struggles — stated plainly, as the closing word, not a rebuttal.",
                 body, prev=("part-12", "Patterns & Idioms"), nxt=("part-ref", "Reference & Glossary"))
