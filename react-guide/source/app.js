/* ============================================================
   REACT — IN DEPTH — app logic
   ============================================================ */

/* ---------- 1. Syntax highlighter ---------- */
/* Token-by-token scan via a single alternation regex. Because each
   alternative is tried at the *current* scan position (not searched for
   ahead), a string/template literal is always consumed atomically as one
   token — so a "//" living inside a string (e.g. "https://x.com") is
   swallowed by the string branch before the comment branch ever gets a
   chance to misfire on it. This is what the URL-inside-string /
   URL-inside-comment stress test below checks for. */

const HL = (function(){
  const KEYWORDS = new Set(['const','let','var','function','return','if','else','for','while',
    'import','export','default','from','as','class','extends','new','this','super','try','catch',
    'finally','throw','typeof','instanceof','in','of','async','await','yield','switch','case',
    'break','continue','null','undefined','true','false','void','delete','do','static','get','set',
    'interface','type','implements','public','private','protected','readonly','enum']);

  const HOOK_OR_COMPONENT = /^[A-Z][A-Za-z0-9_]*$|^use[A-Z][A-Za-z0-9_]*$/;

  // Order matters: block comment, line comment, template string, double
  // string, single string, number, JSX-ish tag open, identifier/keyword,
  // punctuation run, whitespace.
  const TOKEN_RE = /(\/\*[\s\S]*?\*\/)|(\/\/[^\n]*)|(`(?:\\[\s\S]|\$\{[^}]*\}|[^`\\])*`)|("(?:\\.|[^"\\])*")|('(?:\\.|[^'\\])*')|(<\/?[A-Za-z][A-Za-z0-9.]*)|(\b\d+(?:\.\d+)?\b)|([A-Za-z_$][A-Za-z0-9_$]*)|([{}()\[\];:,.<>+\-*/%=!&|^~?"'`]+)|(\s+)/g;

  function escapeHtml(s){
    return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }

  function highlight(rawCode){
    let out = '';
    let m;
    TOKEN_RE.lastIndex = 0;
    // JSX attribute-name detection needs real state, not just "the
    // previous character was '<'" — the tag regex below swallows the
    // '<' into the tag token itself (e.g. the whole token is "<button"),
    // so we track "are we between a tag's name and its closing '>'" and
    // "are we inside a {expression} at brace-depth 0 within that tag"
    // explicitly instead.
    let inTagAttrs = false;
    let curlyDepth = 0;
    while((m = TOKEN_RE.exec(rawCode)) !== null){
      const [full, blockComment, lineComment, template, dstr, sstr, tag, num, ident, punc, ws] = m;
      if(blockComment !== undefined || lineComment !== undefined){
        out += `<span class="tok-com">${escapeHtml(full)}</span>`;
      } else if(template !== undefined || dstr !== undefined || sstr !== undefined){
        out += `<span class="tok-str">${escapeHtml(full)}</span>`;
      } else if(tag !== undefined){
        inTagAttrs = !full.startsWith('</');
        curlyDepth = 0;
        out += `<span class="tok-tag">${escapeHtml(full)}</span>`;
      } else if(num !== undefined){
        out += `<span class="tok-num">${escapeHtml(full)}</span>`;
      } else if(ident !== undefined){
        if(KEYWORDS.has(ident)){
          out += `<span class="tok-kw">${escapeHtml(full)}</span>`;
        } else if(inTagAttrs && curlyDepth === 0){
          out += `<span class="tok-attr">${escapeHtml(full)}</span>`;
        } else if(HOOK_OR_COMPONENT.test(ident)){
          out += `<span class="tok-fn">${escapeHtml(full)}</span>`;
        } else {
          out += escapeHtml(full);
        }
      } else if(punc !== undefined){
        if(inTagAttrs){
          for(const ch of full){
            if(ch === '{') curlyDepth++;
            else if(ch === '}') curlyDepth = Math.max(0, curlyDepth - 1);
            else if(ch === '>' && curlyDepth === 0) inTagAttrs = false;
          }
        }
        out += `<span class="tok-punc">${escapeHtml(full)}</span>`;
      } else if(ws !== undefined){
        out += full;
      }
    }
    return out;
  }

  function run(){
    document.querySelectorAll('pre > code[data-lang]').forEach(el => {
      if(el.dataset.hled) return;
      const raw = el.textContent;
      el.innerHTML = highlight(raw);
      el.dataset.hled = '1';
    });
  }

  return { highlight, run, escapeHtml };
})();

/* ---------- 2. Copy buttons ---------- */
function wireCopyButtons(){
  document.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const panel = btn.closest('.code-panel');
      const code = panel.querySelector('code');
      navigator.clipboard.writeText(code.textContent).then(() => {
        const orig = btn.textContent;
        btn.textContent = 'Copied';
        setTimeout(() => btn.textContent = orig, 1400);
      });
    });
  });
}

/* ---------- 3. TOC build + active tracking + read tracking ---------- */
const READ_KEY = 'react-guide-read-sections';
const SCROLL_KEY = 'react-guide-scroll-pos';

function getReadSet(){
  try{ return new Set(JSON.parse(localStorage.getItem(READ_KEY) || '[]')); }
  catch(e){ return new Set(); }
}
function saveReadSet(set){
  try{ localStorage.setItem(READ_KEY, JSON.stringify([...set])); }catch(e){}
}

function buildTOC(){
  const toc = document.getElementById('toc');
  const parts = document.querySelectorAll('main .part');
  const readSet = getReadSet();
  let html = '';
  parts.forEach((part, i) => {
    const partId = part.id;
    const partNum = part.dataset.num;
    const partTitle = part.dataset.title;
    const isPlaceholder = part.classList.contains('is-placeholder');
    const subs = part.querySelectorAll('h2.sub-title');
    let subsHtml = '';
    subs.forEach(sub => {
      const read = readSet.has(sub.id);
      subsHtml += `<a class="toc-sub${read?' read':''}${isPlaceholder?' placeholder':''}" href="#${sub.id}" data-target="${sub.id}">
        <span class="dot"></span>${sub.dataset.short || sub.textContent}
      </a>`;
    });
    html += `<div class="toc-part${i===0?' open':''}${isPlaceholder?' placeholder':''}" data-part="${partId}">
      <div class="toc-part-label">
        <span class="toc-part-num">${partNum}</span>
        <span class="toc-part-title">${partTitle}</span>
        <span class="toc-caret">▸</span>
      </div>
      <div class="toc-subs">${subsHtml}</div>
    </div>`;
  });
  toc.innerHTML = html;

  toc.querySelectorAll('.toc-part-label').forEach(label => {
    label.addEventListener('click', () => {
      label.parentElement.classList.toggle('open');
    });
  });
  toc.querySelectorAll('.toc-sub').forEach(a => {
    a.addEventListener('click', (e) => {
      e.preventDefault();
      const target = document.getElementById(a.dataset.target);
      if(target) target.scrollIntoView({behavior:'smooth', block:'start'});
      if(window.matchMedia('(max-width: 900px)').matches){
        document.body.classList.add('sidebar-collapsed');
      }
    });
  });
  updateProgressLabel();
}

function updateProgressLabel(){
  const el = document.getElementById('tocProgress');
  if(!el) return;
  const total = document.querySelectorAll('main .part:not(.is-placeholder) h2.sub-title').length;
  const read = getReadSet().size;
  el.textContent = `${read} / ${total} sections read`;
}

/* Mark a heading "read" once its section has been scrolled past reasonably.
   Placeholder ("coming soon") sections are excluded so the counter only
   reflects sections that actually have content. */
function wireReadTracking(){
  const headings = [...document.querySelectorAll('main .part:not(.is-placeholder) h2.sub-title')];
  const readSet = getReadSet();
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if(entry.isIntersecting){
        const id = entry.target.id;
        if(!readSet.has(id)){
          readSet.add(id);
          saveReadSet(readSet);
          const link = document.querySelector(`.toc-sub[data-target="${id}"]`);
          if(link) link.classList.add('read');
          updateProgressLabel();
        }
      }
    });
  }, { rootMargin: '-10% 0px -70% 0px' });
  headings.forEach(h => io.observe(h));
}

/* Highlight active TOC entry + fixed reading-progress bar */
function wireScrollProgress(){
  const fill = document.getElementById('progressFill');
  const headings = [...document.querySelectorAll('main h2.sub-title')];
  function onScroll(){
    const doc = document.documentElement;
    const scrolled = doc.scrollTop;
    const height = doc.scrollHeight - doc.clientHeight;
    fill.style.width = height > 0 ? `${Math.min(100,(scrolled/height)*100)}%` : '0%';

    let activeId = null;
    for(const h of headings){
      if(h.getBoundingClientRect().top - 90 <= 0) activeId = h.id;
      else break;
    }
    document.querySelectorAll('.toc-sub.active').forEach(a => a.classList.remove('active'));
    if(activeId){
      const link = document.querySelector(`.toc-sub[data-target="${activeId}"]`);
      if(link){
        link.classList.add('active');
        const part = link.closest('.toc-part');
        if(part && !part.classList.contains('open')) part.classList.add('open');
      }
    }
    try{ sessionStorage.setItem(SCROLL_KEY, String(scrolled)); }catch(e){}
  }
  document.addEventListener('scroll', onScroll, { passive:true });
  onScroll();
}

/* ---------- 4. Search ---------- */
function buildSearchIndex(){
  const index = [];
  document.querySelectorAll('main .part:not(.is-placeholder) h2.sub-title').forEach(h => {
    const part = h.closest('.part');
    const container = document.createElement('div');
    let node = h.nextElementSibling;
    let text = '';
    while(node && node.tagName !== 'H2'){
      text += ' ' + node.textContent;
      node = node.nextElementSibling;
    }
    index.push({
      id: h.id,
      part: part ? part.dataset.title : '',
      title: h.dataset.short || h.textContent,
      text: (h.textContent + ' ' + text).toLowerCase().replace(/\s+/g,' ').trim()
    });
  });
  return index;
}

function wireSearch(){
  const input = document.getElementById('searchInput');
  const results = document.getElementById('searchResults');
  let index = null;
  let activeIdx = -1;

  function render(items){
    if(items.length === 0){
      results.innerHTML = `<div class="search-empty">No matches yet — try another term.</div>`;
    } else {
      results.innerHTML = items.slice(0,8).map((it,i) => `
        <a class="search-result" data-target="${it.id}" data-i="${i}">
          <span class="sr-part">${it.part}</span>
          <span class="sr-title">${it.title}</span>
          <span class="sr-snippet">${it.snippet}</span>
        </a>`).join('');
    }
    results.classList.add('open');
    activeIdx = -1;
  }

  function search(q){
    if(!index) index = buildSearchIndex();
    q = q.trim().toLowerCase();
    if(q.length < 2){ results.classList.remove('open'); return; }
    const hits = [];
    for(const it of index){
      const pos = it.text.indexOf(q);
      if(pos !== -1 || it.title.toLowerCase().includes(q)){
        const start = Math.max(0, pos - 40);
        const snippet = (pos === -1 ? it.text.slice(0,90) : ('…' + it.text.slice(start, pos+60) + '…'));
        hits.push({...it, snippet});
      }
    }
    render(hits);
  }

  input.addEventListener('input', () => search(input.value));
  input.addEventListener('keydown', (e) => {
    const items = [...results.querySelectorAll('.search-result')];
    if(e.key === 'ArrowDown'){ e.preventDefault(); activeIdx = Math.min(items.length-1, activeIdx+1); }
    else if(e.key === 'ArrowUp'){ e.preventDefault(); activeIdx = Math.max(0, activeIdx-1); }
    else if(e.key === 'Enter'){ e.preventDefault(); if(items[activeIdx]) items[activeIdx].click(); return; }
    else if(e.key === 'Escape'){ input.blur(); results.classList.remove('open'); return; }
    else return;
    items.forEach(it => it.classList.remove('active'));
    if(items[activeIdx]) items[activeIdx].classList.add('active');
  });
  results.addEventListener('click', (e) => {
    const a = e.target.closest('.search-result');
    if(!a) return;
    const target = document.getElementById(a.dataset.target);
    if(target){
      target.scrollIntoView({behavior:'smooth', block:'start'});
      input.value = '';
      results.classList.remove('open');
    }
  });
  document.addEventListener('click', (e) => {
    if(!e.target.closest('.search-wrap')) results.classList.remove('open');
  });
}

/* ---------- 5. Keyboard navigation ---------- */
function wireKeyboardNav(){
  document.addEventListener('keydown', (e) => {
    const tag = document.activeElement.tagName;
    if(tag === 'INPUT' || tag === 'TEXTAREA') return;
    if(e.key === '/'){
      e.preventDefault();
      document.getElementById('searchInput').focus();
    } else if(e.key === 'j' || e.key === 'J'){
      moveHeading(1);
    } else if(e.key === 'k' || e.key === 'K'){
      moveHeading(-1);
    } else if(e.key === '['){
      document.body.classList.toggle('sidebar-collapsed');
    }
  });
  function moveHeading(dir){
    const headings = [...document.querySelectorAll('main h2.sub-title')];
    let idx = headings.findIndex(h => h.getBoundingClientRect().top > 100);
    if(dir === 1){
      if(idx === -1) return;
      headings[idx].scrollIntoView({behavior:'smooth', block:'start'});
    } else {
      idx = idx === -1 ? headings.length - 1 : idx - 1;
      if(idx < 0) idx = 0;
      headings[idx].scrollIntoView({behavior:'smooth', block:'start'});
    }
  }
}

/* ---------- 6. Sidebar toggle ---------- */
function wireSidebarToggle(){
  document.getElementById('sidebarToggle').addEventListener('click', () => {
    document.body.classList.toggle('sidebar-collapsed');
  });
}

/* ---------- Init ---------- */
document.addEventListener('DOMContentLoaded', () => {
  HL.run();
  wireCopyButtons();
  buildTOC();
  wireReadTracking();
  wireScrollProgress();
  wireSearch();
  wireKeyboardNav();
  wireSidebarToggle();

  if(location.hash){
    const el = document.getElementById(location.hash.slice(1));
    if(el) setTimeout(() => el.scrollIntoView({block:'start'}), 50);
  }
});
