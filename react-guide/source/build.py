# -*- coding: utf-8 -*-
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from content_part0 import build_part0
from content_part1 import build_part1
from content_part2 import build_part2
from content_part3 import build_part3
from content_part4 import build_part4
from content_part5 import build_part5
from content_part6 import build_part6
from content_part7 import build_part7
from content_part8 import build_part8
from content_part9 import build_part9
from content_part10 import build_part10
from content_part11 import build_part11
from content_part12 import build_part12
from content_part13 import build_part13
from content_glossary import build_glossary

with open(os.path.join(SCRIPT_DIR, 'style.css'), encoding='utf-8') as f:
    CSS = f.read()
with open(os.path.join(SCRIPT_DIR, 'app.js'), encoding='utf-8') as f:
    JS = f.read()

ALL_PARTS = [
    build_part0(), build_part1(), build_part2(), build_part3(),
    build_part4(), build_part5(), build_part6(), build_part7(),
    build_part8(), build_part9(), build_part10(), build_part11(),
    build_part12(), build_part13(), build_glossary(),
]
MAIN_CONTENT = "\n".join(ALL_PARTS)

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>React \u2014 In Depth: A Complete Reference Guide</title>
<meta name="description" content="A comprehensive, deep-dive reference guide to modern React architecture, from the pre-React DOM truth problem to Fiber, Hooks, Suspense, and React Server Components.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,400;1,9..144,500;1,9..144,600&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<meta property="og:title" content="React \u2014 In Depth: A Complete Reference Guide">
<meta property="og:description" content="A comprehensive, deep-dive reference guide to modern React architecture, from the pre-React DOM truth problem to Fiber, Hooks, Suspense, and React Server Components.">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="React \u2014 In Depth: A Complete Reference Guide">
<meta name="twitter:description" content="A comprehensive, deep-dive reference guide to modern React architecture, from the pre-React DOM truth problem to Fiber, Hooks, Suspense, and React Server Components.">
<style>
{CSS}
</style>
</head>
<body>

  <header class="masthead">
    <div class="masthead-top">
      <button class="sidebar-toggle" id="sidebarToggle" aria-label="Toggle navigation">&#9776;</button>
      <a href="../index.html" class="home-nav-link" title="Return to All Guides">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 19-7-7 7-7"/><path d="M19 12H5"/></svg>
        <span>All Guides</span>
      </a>
      <h1 class="masthead-title"><span class="book-icon">&#8983;</span>React <span class="accent">&mdash; In Depth</span></h1>
      <div class="search-wrap">
        <input type="search" id="searchInput" placeholder="Search the guide\u2026  (press /)" autocomplete="off">
        <div class="search-results" id="searchResults"></div>
      </div>
    </div>
    <div class="progress-track"><div class="progress-fill" id="progressFill"></div></div>
  </header>

  <div class="layout">
    <nav class="sidebar" id="sidebar">
      <div class="toc" id="toc"></div>
      <div class="toc-progress" id="tocProgress">0 / 0 sections read</div>
    </nav>

    <main class="content" id="content">
{MAIN_CONTENT}
    </main>
  </div>

<script>
{JS}
</script>
</body>
</html>
"""

# Write to source directory
target_source = os.path.join(SCRIPT_DIR, 'react-guide.html')
with open(target_source, 'w', encoding='utf-8') as f:
    f.write(HTML)

# Synchronize to main guide entrypoint and alias
target_index = os.path.join(PARENT_DIR, 'index.html')
target_alias = os.path.join(PARENT_DIR, 'react-guide.html')
with open(target_index, 'w', encoding='utf-8') as f:
    f.write(HTML)
with open(target_alias, 'w', encoding='utf-8') as f:
    f.write(HTML)

print(f"Build complete: Wrote {len(HTML):,} characters, {len(ALL_PARTS)} parts.")
print(f"  -> {target_source}")
print(f"  -> {target_index}")
print(f"  -> {target_alias}")

