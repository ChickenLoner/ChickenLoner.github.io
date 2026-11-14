(function () {
  /* ── Inject styles (scoped to #soc-nav-overlay to avoid conflicts) ── */
  var style = document.createElement('style');
  style.textContent = [
    '#soc-nav-overlay{position:fixed;inset:0;z-index:9999;background:#070b14;display:flex;align-items:center;justify-content:center;opacity:0;pointer-events:none}',
    '#soc-nav-overlay.soc-nav-in{opacity:1;pointer-events:all}',
    '#soc-nav-overlay .snv-bar{position:absolute;top:0;left:0;height:2px;width:0;background:#22e1ff;box-shadow:0 0 12px #22e1ff;animation:snv-prog 1.4s ease-out forwards}',
    '@keyframes snv-prog{0%{width:0}60%{width:75%}100%{width:92%}}',
    '#soc-nav-overlay .snv-inner{display:flex;flex-direction:column;align-items:center;gap:18px}',
    '#soc-nav-overlay .snv-ring{width:42px;height:42px;border:2px solid rgba(34,225,255,.1);border-top-color:#22e1ff;border-radius:50%;box-shadow:0 0 20px rgba(34,225,255,.15);animation:snv-spin .75s linear infinite}',
    '@keyframes snv-spin{to{transform:rotate(360deg)}}',
    '#soc-nav-overlay .snv-meta{display:flex;flex-direction:column;align-items:center;gap:6px}',
    '#soc-nav-overlay .snv-uplink{font-family:"JetBrains Mono",monospace;font-size:9px;font-weight:600;letter-spacing:.2em;color:#3ddc84;display:flex;align-items:center;gap:6px}',
    '#soc-nav-overlay .snv-uplink::before{content:"";width:6px;height:6px;border-radius:50%;background:#3ddc84;box-shadow:0 0 8px #3ddc84;animation:snv-pulse 1.4s ease infinite}',
    '#soc-nav-overlay .snv-status{font-family:"JetBrains Mono",monospace;font-size:11px;color:#6c7a9c;letter-spacing:.08em}',
    '#soc-nav-overlay .snv-blink{animation:snv-blink .8s step-end infinite}',
    '@keyframes snv-blink{50%{opacity:0}}',
    '@keyframes snv-pulse{50%{opacity:.25}}'
  ].join('');
  document.head.appendChild(style);

  /* ── Build overlay ── */
  var KEY = 'soc-nav';
  var arriving = sessionStorage.getItem(KEY) === '1';
  if (arriving) sessionStorage.removeItem(KEY);

  var overlay = document.createElement('div');
  overlay.id = 'soc-nav-overlay';
  overlay.innerHTML =
    '<div class="snv-bar"></div>' +
    '<div class="snv-inner">' +
      '<div class="snv-ring"></div>' +
      '<div class="snv-meta">' +
        '<span class="snv-uplink">UPLINK</span>' +
        '<span class="snv-status">CONNECTING<span class="snv-blink">_</span></span>' +
      '</div>' +
    '</div>';

  /* Start visible on arriving page — content never flashes through */
  if (arriving) overlay.classList.add('soc-nav-in');
  document.documentElement.appendChild(overlay);

  /* Fade out after arrival */
  if (arriving) {
    setTimeout(function () {
      overlay.style.transition = 'opacity .4s ease';
      overlay.classList.remove('soc-nav-in');
    }, 420);
  }

  /* Hide overlay when browser restores page from bfcache (back/forward) */
  window.addEventListener('pageshow', function (e) {
    if (e.persisted) {
      overlay.style.transition = 'none';
      overlay.classList.remove('soc-nav-in');
      sessionStorage.removeItem(KEY);
    }
  });

  /* Intercept internal link clicks */
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href]');
    if (!a) return;
    var href = a.getAttribute('href');
    if (!href || href.charAt(0) === '#') return;
    if (href.indexOf('mailto:') === 0 || href.indexOf('javascript:') === 0) return;
    if (a.target === '_blank') return;
    if (/^https?:\/\//.test(href) && href.indexOf('chickenloner.github.io') === -1) return;

    sessionStorage.setItem(KEY, '1');
    overlay.style.transition = 'opacity .15s ease';
    overlay.classList.add('soc-nav-in');
  });

  /* ── TOC scroll-spy: highlight the section currently being read ──
     Article pages render their TOC with React after load, so wait for it. */
  function initTocSpy() {
    var links = Array.prototype.slice.call(
      document.querySelectorAll('.soc-article .res-toc a[href^="#"], .soc-article .ir-toc a[href^="#"]'));
    if (!links.length) return false;
    var items = links.map(function (a) {
      return { a: a, el: document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1))) };
    }).filter(function (x) { return x.el; });
    if (!items.length) return false;
    var current = null, ticking = false;
    function update() {
      ticking = false;
      var line = 140, active = items[0];
      for (var i = 0; i < items.length; i++) {
        if (items[i].el.getBoundingClientRect().top - line <= 0) active = items[i]; else break;
      }
      // at the very bottom, the last section is the one being read
      if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4) active = items[items.length - 1];
      updateProgress();
      if (active === current) return;
      if (current) current.a.classList.remove('is-active');
      active.a.classList.add('is-active');
      current = active;
      if (now) {
        var num = active.a.querySelector('.res-toc-num, .ir-toc-num');
        var label = active.a.textContent.replace(num ? num.textContent : '', '').trim();
        now.innerHTML = '';
        if (num) { var sp = document.createElement('span'); sp.textContent = num.textContent.trim(); now.appendChild(sp); }
        now.appendChild(document.createTextNode(label));
      }
    }
    /* ── Reading progress: card in the info rail (≥1440) + thin bar under the topbar ── */
    var article = document.querySelector('.soc-article');
    var meta = article.querySelector(':scope > .res-meta-grid, :scope > .ir-meta-grid');
    var hub = /^\/ir-reports\//.test(location.pathname) ? ['/ir-reports/', 'All IR reports']
            : /^\/reviews\//.test(location.pathname) ? ['/reviews/', 'All reviews']
            : ['/research/', 'All research'];
    var fills = [], pct = null, now = null;
    if (meta) {
      var card = document.createElement('div');
      card.className = 'soc-read-card';
      card.innerHTML = '<div class="soc-read-head">Reading progress<b class="soc-read-pct">0%</b></div>' +
        '<div class="soc-read-track"><i></i></div><div class="soc-read-now"></div>' +
        '<div class="soc-read-links"><button type="button">\u2191 Back to top</button><a></a></div>';
      card.querySelector('a').href = hub[0];
      card.querySelector('a').textContent = '\u2190 ' + hub[1];
      card.querySelector('button').addEventListener('click', function () { window.scrollTo({ top: 0 }); });
      meta.appendChild(card);
      fills.push(card.querySelector('.soc-read-track > i'));
      pct = card.querySelector('.soc-read-pct');
      now = card.querySelector('.soc-read-now');
    }
    var bar = document.createElement('div');
    bar.className = 'soc-read-bar';
    bar.innerHTML = '<i></i>';
    document.body.appendChild(bar);
    fills.push(bar.firstChild);
    var tb = document.querySelector('.soc-tb');
    function updateProgress() {
      var r = article.getBoundingClientRect();
      var total = r.height - window.innerHeight;
      var p = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 1;
      if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4) p = 1;
      var w = (p * 100).toFixed(1) + '%';
      for (var i = 0; i < fills.length; i++) fills[i].style.width = w;
      if (pct) pct.textContent = Math.round(p * 100) + '%';
      bar.style.top = (tb ? Math.max(0, tb.getBoundingClientRect().bottom) : 0) + 'px';
    }
    function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    update();
    return true;
  }
  var spyTries = 0;
  (function waitForToc() {
    if (initTocSpy() || ++spyTries > 60) return;
    setTimeout(waitForToc, 150);
  })();
})();
