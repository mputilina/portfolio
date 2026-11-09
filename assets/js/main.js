(function () {
  'use strict';

  /* Появление блоков при прокрутке */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.01 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* Фильтр проектов на главной */
  var filters = document.querySelectorAll('.filter');
  var tiles = document.querySelectorAll('.tile');
  var empty = document.querySelector('.grid-empty');
  filters.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var f = btn.getAttribute('data-filter');
      filters.forEach(function (b) {
        var on = b === btn;
        b.classList.toggle('is-active', on);
        b.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
      var shown = 0;
      tiles.forEach(function (t) {
        var tags = (t.getAttribute('data-tags') || '').split(' ');
        var show = f === 'all' || tags.indexOf(f) !== -1;
        t.classList.toggle('is-hidden', !show);
        if (show) { shown++; t.classList.add('is-in'); }
      });
      if (empty) empty.hidden = shown !== 0;
    });
  });

  /* Меню белеет над тёмными кадрами ([data-dark]) — по каждой группе отдельно */
  var groups = document.querySelectorAll('.topnav-left, .topnav-right, .topnav-logo');
  var darks = document.querySelectorAll('[data-dark]');
  if (darks.length) {
    var ticking = false;
    var update = function () {
      ticking = false;
      groups.forEach(function (g) {
        var r = g.getBoundingClientRect();
        var y = r.top + r.height / 2;
        var on = false;
        darks.forEach(function (d) {
          var dr = d.getBoundingClientRect();
          if (y >= dr.top && y <= dr.bottom && r.right >= dr.left && r.left <= dr.right) on = true;
        });
        g.classList.toggle('on-dark', on);
      });
    };
    var req = function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
    window.addEventListener('scroll', req, { passive: true });
    window.addEventListener('resize', req);
    update();
  }
})();
