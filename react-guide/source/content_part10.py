# -*- coding: utf-8 -*-
from helpers import esc, code_panel, callout, keypoints, compare_grid, ref_table, sub, part

ENV_SVG = """<svg class="diagram" viewBox="0 0 720 250" xmlns="http://www.w3.org/2000/svg">
  <style>
    .en{ fill:var(--bg-card); stroke:var(--rule); }
    .el{ font-size:12px; font-weight:600; }
    .es{ font-size:10px; fill:var(--ink-faint); }
    .erow{ font-size:10.5px; fill:var(--ink-dim); }
  </style>
  <text x="10" y="18" style="font-size:11px; fill:var(--ink-dim);">Where does rendering to HTML actually happen, and when?</text>

  <rect class="en" x="10"  y="34" width="165" height="90" rx="8"/>
  <text class="el" x="92" y="56" text-anchor="middle">CSR</text>
  <text class="erow" x="92" y="74" text-anchor="middle">Browser, after JS loads</text>
  <text class="es" x="92" y="92" text-anchor="middle">Blank shell first,</text>
  <text class="es" x="92" y="105" text-anchor="middle">then everything at once</text>

  <rect class="en" x="190" y="34" width="165" height="90" rx="8"/>
  <text class="el" x="272" y="56" text-anchor="middle">SSR</text>
  <text class="erow" x="272" y="74" text-anchor="middle">Server, per request</text>
  <text class="es" x="272" y="92" text-anchor="middle">Real HTML immediately,</text>
  <text class="es" x="272" y="105" text-anchor="middle">then hydrates client-side</text>

  <rect class="en" x="370" y="34" width="165" height="90" rx="8"/>
  <text class="el" x="452" y="56" text-anchor="middle">SSG</text>
  <text class="erow" x="452" y="74" text-anchor="middle">Server, at build time</text>
  <text class="es" x="452" y="92" text-anchor="middle">Same HTML for everyone,</text>
  <text class="es" x="452" y="105" text-anchor="middle">served instantly from cache</text>

  <rect class="en" x="550" y="34" width="165" height="90" rx="8"/>
  <text class="el" x="632" y="56" text-anchor="middle">RSC</text>
  <text class="erow" x="632" y="74" text-anchor="middle">Server, per request</text>
  <text class="es" x="632" y="92" text-anchor="middle">Some components never</text>
  <text class="es" x="632" y="105" text-anchor="middle">ship JS to the client at all</text>

  <text x="10" y="150" style="font-size:11px; fill:var(--ink-faint);">First paint speed:  SSG/RSC ≈ SSR &gt;&gt; CSR &nbsp;&nbsp;|&nbsp;&nbsp; Data freshness: CSR/SSR/RSC &gt;&gt; SSG &nbsp;&nbsp;|&nbsp;&nbsp; Client JS shipped: CSR &gt; SSR &gt; RSC</text>
</svg>"""

def build_part10():
    s1 = sub("p10-csr", "10.1", "Client-Side Rendering, What Plain React Does By Default", "CSR, the baseline", f"""
<p>Everything covered through Part 9 describes React running entirely inside the browser: a server sends a nearly
empty HTML file (often just <code class="inline">&lt;div id="root"&gt;&lt;/div&gt;</code> and a script tag), the
browser downloads and executes the JavaScript bundle, and React builds the entire page from scratch, client-side,
using exactly the render/reconcile/commit pipeline from Part 4.3. This is <strong>Client-Side Rendering</strong>
(CSR) &mdash; it's what a plain <code class="inline">create-vite-app</code>-style React setup does with zero
extra configuration, and it's the baseline every other model in this Part is compared against.</p>

{ENV_SVG}

<p>CSR's characteristic trade-off: the very first thing a visitor sees is a blank (or minimal loading-state)
screen until the JavaScript bundle finishes downloading, parsing, and running &mdash; there is genuinely nothing
meaningful in the initial HTML for a search crawler or a slow connection to work with before that happens. Once
that initial cost is paid, though, every subsequent interaction is instant, client-side reconciliation, with no
further round trips to a server required just to update what's on screen.</p>
""")

    s2 = sub("p10-ssr-hydration", "10.2", "Server-Side Rendering and Hydration", "SSR & hydration", f"""
<p><strong>Server-Side Rendering</strong> (SSR) runs your component tree on the server, for each incoming
request, producing real, complete HTML that's sent to the browser immediately &mdash; the user sees actual
content the instant the page loads, without waiting for any JavaScript to download and run first.</p>

<p>That HTML alone isn't interactive, though &mdash; clicking a button in it does nothing yet, because no event
listeners are attached and no React state exists on the client side to respond to anything. <strong>Hydration
</strong> is the process that follows: React runs again, this time in the browser, walks the already-rendered
HTML, and attaches its event handling and internal state to the existing DOM nodes rather than throwing them away
and rebuilding from scratch.</p>

{callout("warn", "Hydration mismatches", '''
<p>Hydration assumes the HTML the server sent matches exactly what the client would have rendered on its own.
When it doesn't — a classic cause is a component that behaves differently based on
<code class="inline">window</code> or other browser-only values that don't exist during server rendering, or
genuinely nondeterministic content like the current time rendered without care — React detects the mismatch
and either patches the difference or, in more serious cases, throws a visible hydration error. This entire
category of bug is specific to SSR and doesn't exist at all under plain CSR, where there's no pre-rendered HTML
to disagree with in the first place.</p>
''')}
""")

    s3 = sub("p10-ssg", "10.3", "Static Site Generation", "Static site generation", f"""
<p><strong>Static Site Generation</strong> (SSG) runs the same server-rendering step as SSR, but once, at build
time, rather than on every incoming request. The resulting HTML files are identical for every visitor and can be
served instantly from a CDN cache with no server-side rendering work happening live at all &mdash; the fastest
possible first paint of the four models in this Part, and the cheapest to serve at scale, in exchange for the
most significant limitation: the content is fixed at build time and can't reflect anything that's changed since
the last build without either a full rebuild or additional client-side fetching layered on top to patch in
fresher data after the static shell loads.</p>
""")

    s4 = sub("p10-rsc", "10.4", "React Server Components, the Newest Model", "React Server Components", f"""
<p><strong>React Server Components</strong> (RSC) are a different kind of split entirely, not just a different
timing for the same work. A Server Component runs <em>only</em> on the server &mdash; not once at build time like
SSG, but potentially on every request like SSR &mdash; and, critically, <strong>its JavaScript is never sent to
the client at all.</strong> It can directly access server-only resources (a database, the filesystem, private
environment variables) without an API layer in between, but it cannot use state, effects, or any browser API,
because it never runs in the browser in the first place.</p>

{code_panel("JSX", '''
// A Server Component — runs only on the server, ships zero JS to the client
async function ProductPage({ id }) {
  const product = await db.products.findById(id); // direct database access
  return (
    <div>
      <h1>{product.name}</h1>
      <AddToCartButton productId={id} /> {/* a Client Component, marked below */}
    </div>
  );
}
''', "ServerComponent.jsx")}

{code_panel("JSX", '''
'use client'; // this directive marks everything below as a Client Component

function AddToCartButton({ productId }) {
  const [added, setAdded] = useState(false); // state — only legal in a Client Component
  return (
    <button onClick={() => { addToCart(productId); setAdded(true); }}>
      {added ? 'Added!' : 'Add to cart'}
    </button>
  );
}
''', "ClientComponent.jsx")}

<p>The two component types coexist in a single tree, and the practical payoff is real: content that's purely
informational (product details, article text, anything that doesn't need interactivity) contributes zero bytes to
the client JavaScript bundle, while genuinely interactive pieces opt in explicitly with
<code class="inline">'use client'</code>. This directly attacks one of the concrete costs raised in Part 13's
critique of bundle size &mdash; not by making React's client-side runtime smaller, but by needing less of the
tree to run client-side at all.</p>
""")

    s5 = sub("p10-frameworks", "10.5", "Where Next.js and Remix Fit In", "Frameworks built on React", f"""
<p>None of SSR, SSG, or RSC are things a plain <code class="inline">import React from 'react'</code> setup
decides on its own &mdash; they require a build system and a server runtime coordinating file routing, data
fetching, and which rendering model applies to which page. That coordination is exactly what frameworks
<strong>built on top of React</strong> &mdash; Next.js and Remix being the two most widely used &mdash; provide.
This is Part 1.3's library-versus-framework distinction, made concrete: React itself has no opinion about
routing or which of these four rendering models a given page should use; Next.js's App Router, for instance,
defaults new pages to Server Components and layers file-based routing, data-fetching conventions, and SSR/SSG
choices on top of the plain React this entire guide has covered up to this point.</p>

{keypoints("Part 10, wrapped up", [
    "CSR is what plain React does with no extra tooling: blank shell first, everything rendered client-side after JS loads.",
    "SSR renders real HTML per-request on the server, then hydration attaches React's behavior to that existing HTML client-side.",
    "SSG is SSR run once at build time instead of per-request — fastest to serve, least able to reflect fresh data.",
    "Server Components run only on the server and ship zero JS to the client — a different axis (where code runs) from SSR/SSG/CSR (when HTML is produced).",
    "Next.js and Remix are frameworks built on React that make these rendering-model and routing decisions for you — React itself stays opinion-free on all of it."
])}
""")

    body = s1 + s2 + s3 + s4 + s5
    return part("part-10", "10", "Rendering Environments: CSR, SSR, SSG, RSC",
                 "Where the component-function-to-HTML translation actually happens, and why it now happens in more than one place.",
                 body, prev=("part-9", "The Performance Model"), nxt=("part-11", "React vs. Plain HTML, CSS, and JS"))
