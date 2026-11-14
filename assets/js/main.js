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

  /* Пролёт камеры над длинным скриншотом ([data-fly]).
     Ключевые кадры: t — секунды; s — масштаб; rx/rz — наклон; p — прокрутка 0…1. */
  var FLY_KEYS = [
    { t: 0,    s: 1,    rx: 0,  rz: 0,   p: 0 },
    { t: 2.4,  s: 1.6,  rx: 34, rz: -11, p: 0.015 },
    { t: 5.5,  s: 1.68, rx: 37, rz: -14, p: 0.25 },
    { t: 8.5,  s: 1.6,  rx: 31, rz: -8,  p: 0.5 },
    { t: 11.5, s: 1.66, rx: 36, rz: -13, p: 0.75 },
    { t: 14.2, s: 1.58, rx: 32, rz: -10, p: 0.985 },
    { t: 16.2, s: 1,    rx: 0,  rz: 0,   p: 1 },
    { t: 17,   s: 1,    rx: 0,  rz: 0,   p: 1 }
  ];
  var FLY_LEN = 17;
  var ease = function (x) { return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };

  function flyFrame(t) {
    var i = 0;
    while (i < FLY_KEYS.length - 2 && t > FLY_KEYS[i + 1].t) i++;
    var a = FLY_KEYS[i], b = FLY_KEYS[i + 1];
    var k = ease(Math.min(1, Math.max(0, (t - a.t) / (b.t - a.t))));
    var o = {};
    ['s', 'rx', 'rz', 'p'].forEach(function (n) { o[n] = a[n] + (b[n] - a[n]) * k; });
    return o;
  }

  document.querySelectorAll('[data-fly]').forEach(function (fly) {
    var screen = fly.querySelector('.fly-screen');
    var pic = screen.querySelector('img');
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var visible = false, last = null, clock = 0;

    function apply(t) {
      var f = flyFrame(t);
      var travel = Math.max(0, pic.offsetHeight - screen.clientHeight);
      screen.style.transform = 'scale(' + f.s + ') rotateX(' + f.rx + 'deg) rotateZ(' + f.rz + 'deg)';
      pic.style.transform = 'translate3d(0,' + (-f.p * travel) + 'px,0)';
      // мягкая склейка цикла
      var fade = t > FLY_LEN - .5 ? (FLY_LEN - t) / .5 : (t < .4 ? t / .4 : 1);
      screen.style.opacity = String(.15 + .85 * fade);
    }

    function tick(now) {
      if (!visible) { last = null; return; }
      if (last !== null) clock = (clock + (now - last) / 1000) % FLY_LEN;
      last = now;
      apply(clock);
      requestAnimationFrame(tick);
    }

    if (reduce) {
      var still = function () { apply(5.5); };
      if (pic.complete) still(); else pic.addEventListener('load', still);
      return;
    }

    apply(0);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          var was = visible;
          visible = en.isIntersecting;
          if (visible && !was) requestAnimationFrame(tick);
        });
      }, { threshold: 0.15 }).observe(fly);
    }
  });
})();
