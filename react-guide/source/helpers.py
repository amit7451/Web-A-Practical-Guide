# -*- coding: utf-8 -*-
"""
Content-assembly helpers for the React guide.
Keeps code-sample escaping in ONE place (esc) so JSX/JS samples containing
<, >, & never break the surrounding HTML — same approach used for the
JavaScript guide's templating pipeline.
"""

_slug_seen = {}

def esc(code: str) -> str:
    """HTML-escape raw code text for safe embedding inside <code>."""
    return (code.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))

def code_panel(lang: str, code: str, filename: str = "") -> str:
    code = code.strip("\n")
    file_html = f'<span class="file-label">{filename}</span>' if filename else ""
    return f"""<div class="code-panel">
  <div class="code-panel-header">
    <span class="lang-badge">{lang}</span>
    {file_html}
    <button class="copy-btn">Copy</button>
  </div>
  <pre><code data-lang="{lang.lower()}">{esc(code)}</code></pre>
</div>"""

def callout(kind: str, title: str, body_html: str) -> str:
    return f"""<div class="callout {kind}">
  <p class="callout-title">{title}</p>
  {body_html}
</div>"""

def keypoints(title: str, items: list) -> str:
    lis = "\n".join(f"    <li>{i}</li>" for i in items)
    return f"""<div class="keypoints">
  <p class="keypoints-title">{title}</p>
  <ul>
{lis}
  </ul>
</div>"""

def compare_grid(bad_label, bad_lang, bad_code, good_label, good_lang, good_code) -> str:
    return f"""<div class="compare-grid">
  <div class="compare-col bad">
    <div class="compare-label">{bad_label}</div>
    <pre><code data-lang="{bad_lang.lower()}">{esc(bad_code.strip(chr(10)))}</code></pre>
  </div>
  <div class="compare-col good">
    <div class="compare-label">{good_label}</div>
    <pre><code data-lang="{good_lang.lower()}">{esc(good_code.strip(chr(10)))}</code></pre>
  </div>
</div>"""

def requirement_list(items: list) -> str:
    """items: list of (letter, title, body_html)"""
    lis = []
    for letter, title, body in items:
        lis.append(f"""  <li>
    <span class="req-letter">{letter}</span>
    <div><strong>{title}</strong><br>{body}</div>
  </li>""")
    return '<ul class="requirement-list">\n' + "\n".join(lis) + "\n</ul>"

def ref_table(headers: list, rows: list) -> str:
    thead = "".join(f"<th>{h}</th>" for h in headers)
    trs = []
    for row in rows:
        tds = "".join(f"<td>{c}</td>" for c in row)
        trs.append(f"<tr>{tds}</tr>")
    return f"""<table class="ref-table">
  <thead><tr>{thead}</tr></thead>
  <tbody>
{''.join(trs)}
  </tbody>
</table>"""

def sub(id_, num, title, short, body_html) -> str:
    """One numbered sub-section (renders as h2.sub-title + body)."""
    return f"""<h2 class="sub-title" id="{id_}" data-short="{short}"><span class="sub-num">{num}</span>{title}</h2>
{body_html}"""

def placeholder_sub(id_, num, title, short, teaser) -> str:
    return f"""<h2 class="sub-title" id="{id_}" data-short="{short}"><span class="sub-num">{num}</span>{title}</h2>
<p style="color:var(--ink-faint); font-style:italic;">{teaser}</p>"""

def part(id_, num, title, dek, body_html, placeholder=False, prev=None, nxt=None) -> str:
    """
    One full Part wrapper. prev/nxt are (href, label) tuples for the
    footer part-nav; omit for the first/last part.
    """
    cls = "part is-placeholder" if placeholder else "part"
    nav = ""
    if prev or nxt:
        prev_html = f'<a href="#{prev[0]}"><span class="pn-label">Previous</span>{prev[1]}</a>' if prev else "<span></span>"
        next_html = f'<a class="pn-next" href="#{nxt[0]}"><span class="pn-label">Next</span>{nxt[1]}</a>' if nxt else "<span></span>"
        nav = f'<div class="part-nav">{prev_html}{next_html}</div>'
    return f"""<section class="{cls}" id="{id_}" data-num="{num}" data-title="{title}">
  <p class="part-eyebrow">Part {num}</p>
  <h1 class="part-title">{title}</h1>
  <p class="part-dek">{dek}</p>
  {body_html}
  {nav}
</section>"""

def placeholder_part(id_, num, title, dek, teaser_html) -> str:
    body = f"""<div class="placeholder-section">
    <h3>Coming in the next pass</h3>
    {teaser_html}
  </div>"""
    return part(id_, num, title, dek, body, placeholder=True)
