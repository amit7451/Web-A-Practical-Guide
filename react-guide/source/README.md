# React — In Depth: source pipeline

This is the Python assembly pipeline behind `react-guide.html`, following the same pattern used for the
HTML/CSS/JavaScript/Runtime guides: modular content files, a shared set of HTML-safe helper functions, and a
single build script that inlines everything into one self-contained file.

## Rebuilding

```
python3 build.py
```

Regenerates `react-guide.html` in this directory from the content modules below. No dependencies beyond Python 3.

## Files

- `helpers.py` — HTML-safe building blocks: `code_panel` (escapes code before embedding), `callout`,
  `keypoints`, `compare_grid`, `ref_table`, `requirement_list`, `sub`, `part`.
- `content_part0.py` … `content_part13.py` — one module per Part, each exporting a `build_partN()` function
  that returns that Part's HTML.
- `content_glossary.py` — the 44-term glossary/reference section.
- `style.css` / `app.js` — the design system and interactive layer (search, TOC, syntax highlighter,
  read-progress tracking via localStorage). Inlined into the final HTML by `build.py`.
- `build.py` — assembles everything into `react-guide.html`.
- `tokenizer_test.js` — stress tests for the syntax highlighter's tokenizer (run with `node tokenizer_test.js`).
  Covers the URL-inside-string/URL-inside-comment edge case, JSX tag/attribute recognition, and HTML-escaping
  safety. Reuse this suite as-is for any future guide that embeds the same highlighter.

## Editing content

Each `content_partN.py` builds its Part from `sub(...)` calls (one per numbered sub-section) joined together and
wrapped in `part(...)`. Code samples passed to `code_panel(...)`, `callout(...)`, `compare_grid(...)`, etc. are
**plain Python strings, not f-strings** — write single braces for real JS/JSX braces (`{ count }`), not doubled
ones. Only the outer prose body passed to `sub(...)` is an f-string; a literal single brace inside *that* prose
needs the `{'{'}` / `{'}'}` idiom (or `{{` / `}}`).

After editing, re-run `python3 build.py` and spot-check with:

```
node --check <(python3 -c "import re; print(re.search(r'<script>\n(.*)\n</script>', open('react-guide.html').read(), re.S).group(1))")
```

or just re-run the same validation steps used during the original build (tag-balance via `html.parser`,
`node tokenizer_test.js`, and a grep for stray `{{`/`}}` in rendered code panels).
