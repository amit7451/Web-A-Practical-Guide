(function () {
  'use strict';

  var TIER_META = {
    beginner: { label: 'Beginner', roman: 'I', color: 'sage' },
    intermediate: { label: 'Intermediate', roman: 'II', color: 'blue' },
    advanced: { label: 'Advanced', roman: 'III', color: 'red' },
    reference: { label: 'Reference', roman: 'IV', color: 'gold' }
  };
  var TIER_ORDER = ['beginner', 'intermediate', 'advanced', 'reference'];

  function escapeHtml(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function highlight(src, lang) {
    var s = escapeHtml(src);
    if (lang === 'html') {
      s = s.replace(/(&lt;!--[\s\S]*?--&gt;)/g, '<span class="tk-cm">$1</span>');
      s = s.replace(/(&lt;\/?)([a-zA-Z][a-zA-Z0-9-]*)([\s\S]*?)(\/?&gt;)/g, function (m, open, tag, attrs, close) {
        var attrHtml = attrs.replace(/([a-zA-Z_:][a-zA-Z0-9_:-]*)(=)("[^"]*"|'[^']*')/g,
          '<span class="tk-at">$1</span>$2<span class="tk-str">$3</span>');
        return '<span class="tk-pn">' + open + '</span><span class="tk-tg">' + tag + '</span>' + attrHtml + '<span class="tk-pn">' + close + '</span>';
      });
      return s;
    }
    if (lang === 'css') {
      s = s.replace(/(\/\*[\s\S]*?\*\/)/g, '<span class="tk-cm">$1</span>');
      s = s.replace(/([.#]?[a-zA-Z][a-zA-Z0-9_:-]*(?:[\s>+~,]+[.#]?[a-zA-Z][a-zA-Z0-9_:-]*)*)(\s*\{)/g,
        '<span class="tk-tg">$1</span>$2');
      s = s.replace(/([a-zA-Z-]+)(\s*:)(\s*)([^;{}\n]+)(;)/g,
        '<span class="tk-at">$1</span>$2$3<span class="tk-str">$4</span>$5');
      return s;
    }
    if (lang === 'js') {
      s = s.replace(/(\/\/[^\n]*)/g, '<span class="tk-cm">$1</span>');
      s = s.replace(/('(?:[^'\\]|\\.)*'|"(?:[^"\\]|\\.)*")/g, '<span class="tk-str">$1</span>');
      s = s.replace(/\b(const|let|var|function|return|if|else|new|await|async|for|of|in|class|extends|import|from|export|default|true|false|null|undefined|this|document|addEventListener)\b/g,
        '<span class="tk-kw">$1</span>');
      return s;
    }
    return s;
  }

  function parseLibrary() {
    var byTier = {}; TIER_ORDER.forEach(function (t) { byTier[t] = []; });
    document.querySelectorAll('#library .topic-tpl').forEach(function (node) {
      var tier = node.getAttribute('data-tier');
      if (!byTier[tier]) return;
      var codeEl = node.querySelector('.topic-code');
      var noteEl = node.querySelector('.topic-note');
      var kp = Array.prototype.map.call(node.querySelectorAll('.topic-keypoints li'), function (li) { return li.innerHTML; });
      byTier[tier].push({
        id: node.getAttribute('data-id'),
        title: node.getAttribute('data-title'),
        tier: tier,
        bodyHtml: node.querySelector('.topic-body').innerHTML,
        code: codeEl ? { lang: codeEl.getAttribute('data-lang'), filename: codeEl.getAttribute('data-filename'), src: codeEl.textContent.trim() } : null,
        keyPoints: kp,
        note: noteEl ? { kind: noteEl.getAttribute('data-kind'), html: noteEl.innerHTML } : null
      });
    });
    return byTier;
  }

  var byTier = parseLibrary();
  var flat = [];
  TIER_ORDER.forEach(function (t) { byTier[t].forEach(function (topic) { flat.push(topic); }); });
  var indexById = {}; flat.forEach(function (t, i) { indexById[t.id] = i; });

  var state = { completed: {}, lastViewed: null };

  function loadState() {
    return Promise.resolve().then(function () {
      if (window.storage && window.storage.get) {
        return window.storage.get('html-guide-state').then(function (res) {
          if (res && res.value) {
            var parsed = JSON.parse(res.value);
            if (parsed && typeof parsed === 'object') {
              state.completed = parsed.completed || {};
              state.lastViewed = parsed.lastViewed || null;
            }
          }
        }).catch(function () { });
      } else if (window.localStorage) {
        try {
          var raw = localStorage.getItem('html-guide-state');
          if (raw) {
            var parsed = JSON.parse(raw);
            if (parsed && typeof parsed === 'object') {
              state.completed = parsed.completed || {};
              state.lastViewed = parsed.lastViewed || null;
            }
          }
        } catch (e) { /* localStorage access disabled or restricted */ }
      }
    });
  }

  function saveState() {
    if (window.storage && window.storage.set) {
      try { window.storage.set('html-guide-state', JSON.stringify(state)).catch(function () { }); }
      catch (e) { }
    } else if (window.localStorage) {
      try { localStorage.setItem('html-guide-state', JSON.stringify(state)); }
      catch (e) { }
    }
  }

  var tocEl = document.getElementById('toc');
  var pageEl = document.getElementById('page');
  var pageInnerEl = document.getElementById('pageInner');
  var searchEl = document.getElementById('search');
  var progressTextEl = document.getElementById('progressText');
  var progressBarEl = document.getElementById('progressBarFill');

  var currentId = null;

  function buildToc(filter) {
    var q = (filter || '').trim().toLowerCase();
    tocEl.innerHTML = '';
    TIER_ORDER.forEach(function (tierId) {
      var topics = byTier[tierId];
      if (!topics.length) return;
      var meta = TIER_META[tierId];
      var matched = topics.filter(function (t) { return !q || t.title.toLowerCase().indexOf(q) !== -1; });
      if (matched.length === 0) return;
      var doneCount = topics.filter(function (t) { return state.completed[t.id]; }).length;
      var tierWrap = document.createElement('div');
      tierWrap.className = 'tier tier-' + meta.color;
      var head = document.createElement('div');
      head.className = 'tier-head';
      head.innerHTML = '<span class="stamp">' + meta.roman + '</span><span class="tier-label">' + meta.label + '</span><span class="tier-count">' + doneCount + '/' + topics.length + '</span>';
      tierWrap.appendChild(head);
      var list = document.createElement('div');
      list.className = 'tier-list';
      matched.forEach(function (topic) {
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'toc-item' + (topic.id === currentId ? ' active' : '') + (state.completed[topic.id] ? ' done' : '');
        btn.innerHTML = '<span class="chk">' + (state.completed[topic.id] ? '✓' : '') + '</span><span>' + topic.title + '</span>';
        btn.addEventListener('click', function () { goTo(topic.id); closeDrawer(); });
        list.appendChild(btn);
      });
      tierWrap.appendChild(list);
      tocEl.appendChild(tierWrap);
    });
  }

  function updateProgressChrome() {
    var total = flat.length;
    var done = flat.filter(function (t) { return state.completed[t.id]; }).length;
    progressTextEl.textContent = done + ' of ' + total + ' read';
    progressBarEl.style.width = (total ? (done / total * 100) : 0) + '%';
  }

  function flashCopied(btn) {
    var orig = btn.textContent;
    btn.textContent = 'Copied';
    setTimeout(function () { btn.textContent = orig; }, 1400);
  }
  function fallbackCopy(text, btn) {
    try {
      var ta = document.createElement('textarea');
      ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      flashCopied(btn);
    } catch (e) { /* clipboard unavailable */ }
  }

  function renderTopic(id, opts) {
    opts = opts || {};
    var idx = indexById[id];
    if (idx === undefined) return;
    var topic = flat[idx];
    currentId = id;
    state.lastViewed = id;
    var meta = TIER_META[topic.tier];
    var prev = flat[idx - 1];
    var next = flat[idx + 1];

    var html = '';
    html += '<div class="page-head">';
    html += '<span class="tier-pill tier-pill-' + meta.color + '">' + meta.label + '</span>';
    html += '<span class="page-count">Page ' + (idx + 1) + ' of ' + flat.length + '</span>';
    html += '</div>';
    html += '<h1 class="topic-title">' + topic.title + '</h1>';
    html += '<div class="topic-mark"><button type="button" class="mark-btn' + (state.completed[id] ? ' done' : '') + '" id="markBtn">' +
      (state.completed[id] ? '✓ Read' : 'Mark as read') + '</button></div>';
    html += '<div class="prose">' + topic.bodyHtml + '</div>';

    if (topic.code) {
      html += '<div class="code-panel">';
      html += '<div class="code-head"><span class="code-dot dot-' + meta.color + '"></span><span class="code-filename">' + topic.code.filename + '</span>' +
        '<button type="button" class="copy-btn" id="copyBtn">Copy</button></div>';
      html += '<pre class="code-body"><code>' + highlight(topic.code.src, topic.code.lang) + '</code></pre>';
      html += '</div>';
    }

    if (topic.keyPoints && topic.keyPoints.length) {
      html += '<div class="keypoints"><h2>Key points</h2><ul>' +
        topic.keyPoints.map(function (k) { return '<li>' + k + '</li>'; }).join('') + '</ul></div>';
    }

    if (topic.note) {
      var kindLabel = topic.note.kind === 'mistake' ? 'Common mistake' : (topic.note.kind === 'tip' ? 'Try it' : 'Note');
      html += '<div class="callout callout-' + topic.note.kind + '"><strong>' + kindLabel + '.</strong> ' + topic.note.html + '</div>';
    }

    html += '<div class="pager">';
    html += prev ? '<button type="button" class="pager-btn pager-prev" data-id="' + prev.id + '"><span class="pager-arrow">←</span><span><span class="pager-label">Previous</span><span class="pager-title">' + prev.title + '</span></span></button>' : '<span></span>';
    html += next ? '<button type="button" class="pager-btn pager-next" data-id="' + next.id + '"><span><span class="pager-label">Next</span><span class="pager-title">' + next.title + '</span></span><span class="pager-arrow">→</span></button>' : '<span></span>';
    html += '</div>';

    pageInnerEl.innerHTML = html;
    if (!opts.skipScroll) pageEl.scrollTop = 0;

    document.getElementById('markBtn').addEventListener('click', function () { toggleComplete(id); });
    var copyBtn = document.getElementById('copyBtn');
    if (copyBtn) {
      copyBtn.addEventListener('click', function () {
        var codeText = topic.code.src;
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(codeText).then(function () { flashCopied(copyBtn); }).catch(function () { fallbackCopy(codeText, copyBtn); });
        } else {
          fallbackCopy(codeText, copyBtn);
        }
      });
    }
    Array.prototype.forEach.call(pageInnerEl.querySelectorAll('.pager-btn'), function (b) {
      b.addEventListener('click', function () { goTo(b.getAttribute('data-id')); });
    });

    buildToc(searchEl.value);
    updateProgressChrome();
    saveState();
  }

  function toggleComplete(id) {
    state.completed[id] = !state.completed[id];
    renderTopic(id);
  }

  function goTo(id) { renderTopic(id); }

  var drawerToggle = document.getElementById('drawerToggle');
  var drawerClose = document.getElementById('drawerClose');
  var backdrop = document.getElementById('backdrop');
  var tocPanel = document.getElementById('tocPanel');
  function openDrawer() { tocPanel.classList.add('open'); backdrop.classList.add('show'); }
  function closeDrawer() { tocPanel.classList.remove('open'); backdrop.classList.remove('show'); }
  if (drawerToggle) drawerToggle.addEventListener('click', openDrawer);
  if (drawerClose) drawerClose.addEventListener('click', closeDrawer);
  if (backdrop) backdrop.addEventListener('click', closeDrawer);

  if (searchEl) searchEl.addEventListener('input', function () { buildToc(searchEl.value); });

  document.addEventListener('keydown', function (e) {
    var tag = (document.activeElement && document.activeElement.tagName) || '';
    if (tag === 'INPUT' || tag === 'TEXTAREA') return;
    var idx = indexById[currentId];
    if (e.key === 'ArrowRight' && flat[idx + 1]) goTo(flat[idx + 1].id);
    if (e.key === 'ArrowLeft' && flat[idx - 1]) goTo(flat[idx - 1].id);
  });

  loadState().then(function () {
    buildToc('');
    var startId = (state.lastViewed && indexById[state.lastViewed] !== undefined) ? state.lastViewed : flat[0].id;
    renderTopic(startId);
  });
})();
