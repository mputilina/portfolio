#!/usr/bin/env python3
"""Собирает статический сайт из build/content.py.

    python3 build/build.py

Пишет index.html, about.html, experience.html и works/<slug>.html в корень репозитория.
"""
import datetime
import json
import os
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

import sys
sys.path.insert(0, HERE)
from content import (PERSON, FILTERS, CASES, EXPERIENCE, EXPERIENCE_INTRO,  # noqa: E402
                     EDUCATION, TOOLS, ABOUT)

DIMS = json.load(open(os.path.join(HERE, "dims.json")))
CASE_BY_SLUG = {c["slug"]: c for c in CASES}
ASSET_V = "16"


def e(s):
    return escape(s, quote=True)


def img(key, prefix, alt="", cls="", sizes="100vw", eager=False, style=""):
    w, h = DIMS[key]
    attrs = [
        f'src="{prefix}assets/img/{key}.webp"',
        f'width="{w}" height="{h}"',
        f'alt="{e(alt)}"',
        'decoding="async"',
        'loading="eager"' if eager else 'loading="lazy"',
    ]
    if cls:
        attrs.append(f'class="{cls}"')
    if style:
        attrs.append(f'style="{style}"')
    return f"<img {' '.join(attrs)}>"


# ---------------------------------------------------------------- layout

def header(prefix, active):
    links = [
        ("index.html", "Проекты", "work"),
        ("about.html", "Обо мне", "about"),
        ("experience.html", "Опыт", "experience"),
    ]
    items = "".join(
        f'<a href="{prefix}{href}"{" class=\"is-active\" aria-current=\"page\"" if key == active else ""}>{label}</a>'
        for href, label, key in links
    )
    return f"""
<div class="topnav-blur" aria-hidden="true"></div>
<header class="topnav">
  <div class="topnav-side topnav-left"><span class="topnav-badge">{e(PERSON['badge'])}</span></div>
  <a href="{prefix}index.html" class="topnav-logo topnav-wordmark" aria-label="{e(PERSON['name'])} — на главную">{e(PERSON['name'])}</a>
  <nav class="topnav-side topnav-right" aria-label="Основное меню">
    {items}
    <a href="#contacts" class="topnav-cta">Связаться</a>
  </nav>
</header>"""


def footer(prefix):
    """Подвал по схеме kirstenhumpfer.de: фраза + кнопка-пилюля, под линией —
    сетка контактов (слева / на ⅔ ширины / у правого края) и нижняя строка."""
    p = PERSON
    year = datetime.date.today().year
    return f"""
<footer class="site-foot" id="contacts">
  <div class="foot-cta reveal">
    <p class="foot-title">{e(p['footer_title'])}</p>
    <a class="foot-button" href="{p['telegram']}" target="_blank" rel="noopener">{e(p['footer_button'])}</a>
  </div>
  <div class="foot-grid">
    <div class="foot-cell foot-main">
      <p>{e(p['location'])}</p>
    </div>
    <div class="foot-cell foot-side">
      <div>
        <a href="mailto:{p['email']}">{e(p['email'])}</a>
        <a href="{p['phone_href']}">{e(p['phone'])}</a>
      </div>
      <div class="foot-end">
        <a href="{p['telegram']}" target="_blank" rel="noopener">Telegram</a>
        <a href="{prefix}{p['cv']}" download>Резюме, PDF</a>
      </div>
    </div>
    <div class="foot-cell foot-main foot-bottom">
      <p>© {year} {e(p['name'])}</p>
    </div>
    <div class="foot-cell foot-side foot-bottom">
      <div><p>{e(p['badge'])}</p></div>
      <div class="foot-end"><a href="#main" class="foot-top">Наверх ↑</a></div>
    </div>
  </div>
</footer>"""


def page(title, description, body, prefix, active, body_class=""):
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<script>document.documentElement.classList.add('js')</script>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:image" content="{prefix}assets/img/hexway/01.webp">
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Zalando+Sans+SemiExpanded:wght@300;400;500&family=Onest:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}assets/css/style.css?v={ASSET_V}">
</head>
<body class="{body_class}">
<a class="skip" href="#main">К содержанию</a>
{header(prefix, active)}
<main id="main">
{body}
</main>
{footer(prefix)}
<script src="{prefix}assets/js/main.js?v={ASSET_V}" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------- home

def tile(c, prefix):
    tags = " ".join(c["tags"])
    pos = c.get("cover_pos", "50% 50%")
    return f"""
  <a href="{prefix}works/{c['slug']}.html" class="tile reveal" data-tags="{tags}">
    <div class="tile-media">{img(c['cover'], prefix, c['title'], style=f'object-position:{pos}', sizes='33vw')}</div>
    <div class="tile-info">
      <div class="tile-head"><span class="tile-title">{e(c['title'])}</span><span class="tile-meta">{e(c['subtitle'])}</span></div>
      <p class="tile-desc">{e(c['tile_note'])}</p>
    </div>
  </a>"""


def build_home():
    prefix = ""
    pills = "".join(
        f'<button type="button" class="filter{" is-active" if k == "all" else ""}" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{e(lbl)}</button>'
        for k, lbl in FILTERS
    )
    tiles = "".join(tile(c, prefix) for c in CASES)
    body = f"""
<section class="home-intro">
  <h1 class="home-lead">{e(ABOUT['lead'])}</h1>
</section>
<section class="work" aria-label="Проекты">
  <div class="filters" role="group" aria-label="Фильтр проектов">{pills}</div>
  <div class="grid">{tiles}
  </div>
  <p class="grid-empty" hidden>В этой категории пока нет проектов.</p>
</section>"""
    return page(f"{PERSON['name']} — дизайнер", ABOUT["lead"], body, prefix, "work", "page-home")


# ---------------------------------------------------------------- about

def build_about():
    prefix = ""
    a = ABOUT
    bio = "".join(f"<p>{e(p)}</p>" for p in a["bio"])
    exp = "".join(f"<li>→ {e(x)}</li>" for x in a["expertise"])

    def skillrows(rows):
        return "".join(
            f'<div class="skill reveal"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in rows
        )

    body = f"""
<section class="info-hero" data-dark>
  <div class="info-hero-media">{img('hexway/01', prefix, '', eager=True)}</div>
  <h1 class="info-hero-title">{e(a['hero'])}</h1>
</section>
<section class="info-intro">
  <p class="info-lead reveal">{e(a['lead'])}</p>
  <div class="info-cols">
    <p class="reveal">{e(a['col_left'])}</p>
    <p class="reveal">{e(a['col_right'])}</p>
  </div>
</section>
<section class="info-person">
  <figure class="info-photo reveal">{img('main/avatar', prefix, PERSON['name'])}</figure>
  <div class="info-bio reveal">
    {bio}
    <div class="info-expertise">
      <p class="eyebrow">Область экспертизы</p>
      <ul>{exp}</ul>
    </div>
  </div>
</section>
<section class="info-skills">
  <div class="skills-block">
    <p class="eyebrow">Hard skills</p>
    <div class="skills">{skillrows(a['hard'])}</div>
  </div>
  <div class="skills-block">
    <p class="eyebrow">Soft skills</p>
    <div class="skills">{skillrows(a['soft'])}</div>
  </div>
</section>
<section class="info-end reveal">
  <p class="info-quote">{e(a['quote'])}</p>
  <p class="info-since">{e(a['since'])}</p>
</section>"""
    return page(f"Обо мне — {PERSON['name']}", a["lead"], body, prefix, "about", "page-about")


# ---------------------------------------------------------------- experience

def build_experience():
    prefix = ""
    intro = "".join(f'<p class="xp-statement reveal">{e(p)}</p>' for p in EXPERIENCE_INTRO)
    jobs = []
    for j in EXPERIENCE:
        points = "".join(f"<li>{e(p)}</li>" for p in j["points"])
        about = f'<p class="xp-about">{e(j["about"])}</p>' if j.get("about") else ""
        hl = ""
        if j.get("highlights"):
            hl = '<div class="xp-highlights"><p class="eyebrow">Яркие достижения</p><ul>' + "".join(
                f"<li>{e(h)}</li>" for h in j["highlights"]) + "</ul></div>"
        thumbs = []
        for slug in j.get("cases", []):
            c = CASE_BY_SLUG[slug]
            thumbs.append(
                f'<a class="xp-thumb" href="works/{slug}.html">{img(c["cover"], prefix, c["title"])}'
                f'<span class="xp-thumb-label">{e(c["title"])} <span>{e(c["subtitle"])}</span></span></a>')
        for key in j.get("images", []):
            thumbs.append(f'<div class="xp-thumb">{img(key, prefix, j["company"])}</div>')
        thumbs_html = f'<div class="xp-thumbs n{len(thumbs)}">{"".join(thumbs)}</div>' if thumbs else ""
        duration = f'<span class="xp-duration">{e(j["duration"])}</span>' if j["duration"] else ""
        jobs.append(f"""
    <article class="xp-item reveal">
      <div class="xp-top">
        <span class="xp-mono" aria-hidden="true">{e(j['mono'])}</span>
        <span class="xp-date">{e(j['dates'])}</span>
      </div>
      <h3 class="xp-role">{e(j['role'])} <span>в {e(j['company'])}</span></h3>
      {duration}
      {about}
      <ul class="xp-points">{points}</ul>
      {hl}
      {thumbs_html}
    </article>""")

    edu = "".join(
        f'<div class="edu-row reveal"><span class="xp-date">{e(d)}</span><div><h3>{e(t)}</h3>'
        f'{f"<p>{e(s)}</p>" if s else ""}</div></div>' for d, t, s in EDUCATION)
    tools = "".join(f"<li>{e(t)}</li>" for t in TOOLS)

    body = f"""
<section class="xp-hero">
  {intro}
  <a class="btn-wide reveal" href="{PERSON['cv']}" download>Скачать резюме →</a>
</section>
<section class="xp-section">
  <h2 class="xp-heading">Опыт<br>работы</h2>
  <div class="xp-list">{''.join(jobs)}
  </div>
</section>
<section class="xp-section">
  <h2 class="xp-heading">Образование<br>и курсы</h2>
  <div class="xp-list">{edu}</div>
</section>
<section class="xp-section">
  <h2 class="xp-heading">Инструменты</h2>
  <div class="xp-list"><ul class="tools reveal">{tools}</ul></div>
</section>"""
    return page(f"Опыт — {PERSON['name']}", EXPERIENCE_INTRO[0], body, prefix, "experience", "page-experience")


# ---------------------------------------------------------------- case

def render_block(b, prefix, c):
    kind = b[0]
    if kind == "lead":
        return f'<p class="case-lead reveal">{e(b[1])}</p>'
    if kind == "flythrough":
        # Пролёт камеры над длинным скриншотом: 3D-наклон, прокрутка, размытые края.
        key, colors = b[1], b[2]
        style = f"--fly-bg:{colors['bg']};--fly-bg2:{colors['bg2']};--fly-glow:{colors['glow']}"
        return (f'<figure class="case-figure reveal"><div class="fly" data-fly style="{style}" '
                f'role="img" aria-label="Анимация: прокрутка страницы {e(c["title"])} в перспективе">'
                f'<div class="fly-glow" aria-hidden="true"></div>'
                f'<div class="fly-stage"><div class="fly-screen">{img(key, prefix, "")}</div></div>'
                f'<div class="fly-dof fly-dof-top" aria-hidden="true"></div>'
                f'<div class="fly-dof fly-dof-bottom" aria-hidden="true"></div>'
                f'</div></figure>')
    if kind == "text_static":
        # видим сразу, без анимации появления
        return f'<p class="case-text reveal is-in">{e(b[1])}</p>'
    if kind == "cards":
        cards = "".join(
            f'<li class="case-card"><span class="num">{i:02d}</span><p>{e(t)}</p></li>'
            for i, t in enumerate(b[1], 1))
        return f'<ul class="case-cards reveal">{cards}</ul>'
    if kind == "text":
        return f'<p class="case-text reveal">{e(b[1])}</p>'
    if kind == "list":
        items = "".join(
            f'<li><span class="num">{i:02d}</span><span>{e(t)}</span></li>' for i, t in enumerate(b[1], 1))
        return f'<ol class="case-list reveal">{items}</ol>'
    if kind in ("image", "row"):
        # Подпись к фото — сноской под картинкой, а не колонкой рядом.
        return single_figure(b[1], b[2], prefix, c)

    if kind == "images":
        # элемент — файл или (файл, сноска)
        items = [f if isinstance(f, tuple) else (f, None) for f in b[1]]
        files, cols = [f for f, _ in items], b[2]
        figs = "".join(
            f'<figure class="case-figure">{img(f, prefix, c["title"])}'
            f'{f"<figcaption class=case-caption>{e(cap)}</figcaption>" if cap else ""}</figure>'
            for f, cap in items)
        ratios = [DIMS[f][0] / DIMS[f][1] for f in files]
        mode = b[3] if len(b) > 3 else ""
        if mode == "equal":
            # колонки пропорциональны картинкам — одна высота, без обрезки
            cols_css = " ".join(f"{r:.4f}fr" for r in ratios)
            return (f'<div class="case-gallery cols-{cols} equal reveal" '
                    f'style="--cols:{cols_css}">{figs}</div>')
        natural = " natural" if mode == "natural" or max(ratios) / min(ratios) < 1.12 else ""
        return f'<div class="case-gallery cols-{cols}{natural} reveal">{figs}</div>'
    if kind == "scroll":
        return f'<figure class="case-figure reveal">{scroll_frame(b[1], prefix, c)}<figcaption>{e(b[2])}</figcaption></figure>'
    if kind == "compare":
        cols = "".join(
            f'<figure class="case-figure"><figcaption class="compare-label">{e(lbl)}</figcaption>{scroll_frame(f, prefix, c)}</figure>'
            for lbl, f in b[1])
        return f'<div class="case-compare reveal">{cols}</div>'
    if kind == "columns":
        cols = "".join(
            f'<div class="case-col"><h4>{e(t)}</h4><ul>{"".join(f"<li>{e(x)}</li>" for x in items)}</ul></div>'
            for t, items in b[1])
        return f'<div class="case-columns reveal">{cols}</div>'
    if kind == "links":
        cards = "".join(
            f'<a class="site-card" href="{url}" target="_blank" rel="noopener">'
            f'<span class="site-card-media">{img(f, prefix, lbl)}</span>'
            f'<span class="site-card-label">{e(lbl)} <span aria-hidden="true">↗</span></span></a>'
            for lbl, url, f in b[1])
        return f'<div class="site-cards reveal">{cards}</div>'
    if kind == "behance":
        return f'<a class="btn-wide reveal" href="{PERSON["behance"]}" target="_blank" rel="noopener">{e(b[1])} ↗</a>'
    raise ValueError(kind)


def single_figure(key, caption, prefix, c):
    w, h = DIMS[key]
    if h / w > 1.6:          # длинный макет — в окне с прокруткой
        media, cls = scroll_frame(key, prefix, c), ""
    else:                    # вертикальное и квадратное фото не выше экрана
        media, cls = img(key, prefix, c["title"]), (" is-upright" if h / w > 0.9 else "")
    cap = f'<figcaption class="case-caption">{e(caption)}</figcaption>' if caption else ""
    return f'<figure class="case-figure{cls} reveal">{media}{cap}</figure>'


def scroll_frame(key, prefix, c):
    return (f'<div class="scroll-frame" tabindex="0" aria-label="Длинный макет, прокрутите внутри">'
            f'{img(key, prefix, c["title"])}</div>')


def build_case(i):
    c = CASES[i]
    prefix = "../"
    meta = []
    for label, val in c["meta"]:
        if isinstance(val, list):
            val_html = '<span class="dot">·</span>'.join(f"<span>{e(v)}</span>" for v in val)
        else:
            val_html = e(val)
        meta.append(f'<div class="meta-cell"><span class="eyebrow">{e(label)}</span><p>{val_html}</p></div>')

    sections = []
    n = 0
    for s in c["sections"]:
        n += 1
        title = f'<h2 class="section-title reveal">{e(s["title"])}</h2>'
        rest = s["blocks"]
        if rest and rest[0][0] == "list":
            # Заголовок слева, пункты справа на той же высоте — в колонке «Контекста»
            head = f'<div class="section-split">{title}{render_block(rest[0], prefix, c)}</div>'
            rest = rest[1:]
        else:
            head = title
        blocks = "".join(render_block(b, prefix, c) for b in rest)
        body = f'\n    <div class="section-body">{blocks}</div>' if blocks else ""
        sections.append(f"""
  <section class="case-section">
    <div class="section-head reveal"><span class="section-num">{n:02d}</span><span class="section-label">{e(s['label'])}</span></div>
    {head}{body}
  </section>""")

    if c["results"]:
        n += 1
        cells = "".join(
            f'<div class="result reveal"><span class="eyebrow">{e(lbl)}</span><strong>{e(v)}</strong>'
            f'{f"<span class=result-note>{e(note)}</span>" if note else ""}</div>'
            for lbl, v, note in c["results"])
        sections.append(f"""
  <section class="case-section case-results">
    <div class="section-head reveal"><span class="section-num">{n:02d}</span><span class="section-label">{e(c.get('results_label', 'Ключевые результаты'))}</span></div>
    <div class="results n{len(c['results'])}">{cells}</div>
  </section>""")

    prev_c = CASES[(i - 1) % len(CASES)]
    next_c = CASES[(i + 1) % len(CASES)]
    context = "".join(f"<p>{e(p)}</p>" for p in c["context"])

    body = f"""
<article class="case">
  <header class="case-hero">
    <p class="case-eyebrow">{e(c['title'])} · {e(c['subtitle'])}</p>
    <h1 class="case-title">{e(c['headline'])}</h1>
  </header>
  <div class="case-meta">{''.join(meta)}</div>
  <div class="case-intro">
    <div class="reveal"><span class="eyebrow">Коротко</span><p class="case-tldr">{e(c['tldr'])}</p></div>
    <div class="case-context reveal"><span class="eyebrow">Контекст</span>{context}</div>
  </div>
  {''.join(sections)}
  <nav class="case-next" aria-label="Другие проекты">
    <a class="case-next-tile reveal" href="{next_c['slug']}.html">
      <span class="case-next-media">{img(next_c['cover'], prefix, next_c['title'], style='object-position:' + next_c.get('cover_pos', '50% 50%'))}</span>
      <span class="case-next-text"><span class="eyebrow">Следующий проект</span><span class="case-next-title">{e(next_c['title'])}</span><span class="case-next-sub">{e(next_c['tile_note'])}</span></span>
    </a>
    <div class="pager">
      <a href="{prev_c['slug']}.html">← Предыдущий</a>
      <a href="../index.html">Все проекты</a>
      <a href="{next_c['slug']}.html">Следующий →</a>
    </div>
  </nav>
</article>"""
    return page(f"{c['title']}. {c['subtitle']} — {PERSON['name']}", c["tldr"], body, prefix, "work", "page-case")


def main():
    os.makedirs(os.path.join(ROOT, "works"), exist_ok=True)
    out = {
        "index.html": build_home(),
        "about.html": build_about(),
        "experience.html": build_experience(),
    }
    for i, c in enumerate(CASES):
        out[f"works/{c['slug']}.html"] = build_case(i)
    for path, html in out.items():
        with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", path)


if __name__ == "__main__":
    main()
