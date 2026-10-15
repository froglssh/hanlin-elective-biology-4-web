# -*- coding: utf-8 -*-
"""產生 選修生物（Ⅳ）教材入口網站：index.html、chapter1–3.html、發布總表。
版面沿用 選生三新網頁（style.css／app.js 不變）。"""
import os, sys, html
from urllib.parse import quote
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chapters4 import CHAPTERS, V, unit_file, lab_file
from PIL import Image

OUT = os.path.dirname(os.path.abspath(__file__))
E = html.escape
ARROW = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
EXT = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
STAR = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" style="color:#d97706"><path d="m12 3 2.8 5.7L21 9.5l-4.5 4.4 1.1 6.1L12 17.2 6.4 20l1.1-6.1L3 9.5l6.2-.8z" fill="currentColor"/></svg>'
BOOK = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5.5C6.5 4.5 9.5 4.5 12 6c2.5-1.5 5.5-1.5 8-.5v13c-2.5-1-5.5-1-8 .5-2.5-1.5-5.5-1.5-8-.5z M12 6v13.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>'
ZOOM = '<span class="zoom"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="m16 16 4.5 4.5M8.5 11h5M11 8.5v5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>放大</span>'
PLAY = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M10 8.5v7l6-3.5z" fill="currentColor"/></svg>'

BOOKNAME = "選修生物Ⅳ（全）"
SITE = "翰林版 選修生物（Ⅳ）"
FOOT = f'''<footer class="foot">
  <div class="foot-in">
    <img src="img/hanlin-logo.png" alt="" width="34" height="34">
    <p>內容整理自翰林版高中《{BOOKNAME}》課本，簡介依課文重點改寫，圖片取自課本，僅供課堂教學使用。</p>
  </div>
</footer>
<div class="lightbox" id="lightbox" hidden>
  <button class="lb-close" aria-label="關閉">×</button>
  <figure><img alt=""><figcaption></figcaption></figure>
</div>
<script src="app.js"></script>
</body>
</html>
'''

def head(title, desc, theme):
    return f'''<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="{theme}">
<link rel="icon" href="img/hanlin-logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&family=Noto+Serif+TC:wght@600;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<script>document.documentElement.classList.add('js')</script>
</head>
'''

def style(c): return f'--a:{c["a"]};--a2:{c["a2"]};--t:{c["t"]}'
nU = sum(len(c['units']) for c in CHAPTERS); nL = sum(len(c['labs']) for c in CHAPTERS)

# ---------------- index.html ----------------
def index():
    cards = []
    for c in CHAPTERS:
        lis = ''.join(f'<li><span>{u["code"]}</span>{u["title"]}</li>' for u in c['units'])
        cards.append(f'''      <a class="ch-card reveal" href="chapter{c['n']}.html" style="{style(c)}">
        <div class="ch-cover"><img src="img/cover{c['n']}.jpg" alt="第{c['n']}章 {c['name']} 章節封面" loading="lazy" width="1000" height="1328"></div>
        <div class="ch-body">
          <div class="ch-kicker">CHAPTER {c['n']:02d} · {c['en']}</div>
          <h2>第 {c['n']} 章　{c['name']}</h2>
          <ul class="ch-list">{lis}</ul>
          <div class="ch-meta"><span>{len(c['units'])} 節正課</span><span>{len(c['labs'])} 個探討活動</span></div>
          <span class="ch-go">進入本章 {ARROW}</span>
        </div>
      </a>''')
    cols = []
    for c in CHAPTERS:
        a = ''.join(f'<a target="_blank" rel="noopener" href="{unit_file(u)}" class="q"><span class="q-code">{u["code"]}</span><span class="q-t">{u["web"]}<small>課本 P.{u["pg"]}</small></span>{EXT}</a>' for u in c['units'])
        a += ''.join(f'<a target="_blank" rel="noopener" href="{lab_file(l)}" class="q q-lab"><span class="q-code">探討{l["code"]}</span><span class="q-t">{l["web"]}<small>探討活動・課本 P.{l["pg"]}</small></span>{EXT}</a>' for l in c['labs'])
        cols.append(f'<div class="qcol reveal" style="--a:{c["a"]};--t:{c["t"]}"><h3><b>{c["n"]}</b>{c["name"]}</h3>{a}</div>')
    desc = f"翰林版高中選修生物Ⅳ（全）三章 {nU} 節與 {nL} 個探討活動的互動教學網頁與教學影片入口"
    return head(f"{SITE}｜互動教學網站", desc, "#9e1c3f") + f'''<body class="home">
<header class="hero">
  <svg class="globe" viewBox="0 0 600 600" aria-hidden="true">
    <g fill="none" stroke="currentColor" stroke-width="1.2">
      <path d="M0 330h150l30-60 40 150 50-260 45 220 30-50h255" stroke-width="3"/>
      <circle cx="300" cy="300" r="290" stroke-dasharray="10 8" opacity=".5"/>
    </g>
  </svg>
  <div class="hero-in">
    <img class="hero-logo" src="img/hanlin-logo-wide.png" alt="翰林出版 HAN LIN PUBLISHING" width="1240" height="324">
    <div class="hero-rule"><span></span><em>自然科學領域　加深加廣選修</em><span></span></div>
    <h1>選修生物（Ⅳ）<span>互動教學網站</span></h1>
    <p class="hero-sub">翰林版《{BOOKNAME}》· 互動闖關教學網頁與教學影片，包含演化、族群遺傳、物種形成、生態學的研究層級、族群、群集、生態系與生物多樣性保育全單元</p>
    <ul class="stats">
      <li><b>{len(CHAPTERS)}</b><span>章</span></li><li><b>{nU}</b><span>節正課</span></li><li><b>{nL}</b><span>個探討活動</span></li><li><b>{nU+nL}</b><span>個互動教學網頁</span></li>
    </ul>
  </div>
</header>
<main>
  <section class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">CHAPTERS</span><h2>選擇章節，開始探索</h2><p>點選章節封面進入章節，瀏覽每一節的課本概念圖、重點簡介與教學影片。</p></div>
    <div class="ch-grid">
{chr(10).join(cards)}
    </div>
  </section>
  <section class="wrap quick-wrap">
    <div class="sec-head reveal"><span class="eyebrow">QUICK ACCESS</span><h2>全部互動教學網頁快速入口</h2><p>老師上課或學生複習時，可直接開啟各節的互動教學網頁（另開新分頁）；教學影片請由章節頁進入。</p></div>
    <div class="quick">{''.join(cols)}</div>
  </section>
</main>
''' + FOOT

# ---------------- chapterN.html ----------------
def ratio(img):
    w, h = Image.open(os.path.join(OUT, 'img', img + '.jpg')).size
    return w / h

def fig(img, cap, cls='fig-btn', extra=''):
    return f'''<button class="{cls}" data-full="img/{img}.jpg" data-cap="{E(cap)}" aria-label="放大圖片：{E(cap)}">
          <img src="img/{img}.jpg" alt="{E(cap)}" loading="lazy" decoding="async">{ZOOM}
        </button>'''

def chapter(c, prev_c, next_c):
    nav = ''.join(f'<a href="chapter{x["n"]}.html" class="nav-ch{" on" if x is c else ""}" style="--a:{x["a"]}"><b>{x["n"]}</b><span>{x["name"]}</span></a>' for x in CHAPTERS)
    jump = ''.join(f'<a href="#u{u["code"]}"><b>{u["code"]}</b>{u["title"]}</a>' for u in c['units'])
    jump += f'<a href="#labs" class="j-lab"><b>探討</b>活動 × {len(c["labs"])}</a>'
    arts = []
    flip = False
    for u in c['units']:
        wide = ratio(u['img']) >= 2.2
        cls = 'unit reveal' + (' wide' if wide else (' flip' if flip else ''))
        if not wide: flip = not flip
        subs = ''.join(f'<li>{E(s)}</li>' for s in u['subs'])
        tags = ''.join(f'<span>{E(t)}</span>' for t in u['tags'])
        f = unit_file(u)
        arts.append(f'''    <article class="{cls}" id="u{u['code']}">
      <figure class="fig">
        {fig(u['img'], u['cap'])}
        <figcaption>{E(u['cap'])}</figcaption>
      </figure>
      <div class="unit-body">
        <div class="unit-top"><span class="code">{u['code']}</span><span class="web-pill">{STAR}互動網頁｜{u['web']}</span><span class="pg-pill">{BOOK}課本 P.{u['pg']}</span></div>
        <h2>{u['title']}</h2>
        <a class="intro" href="{f}" target="_blank" rel="noopener" title="開啟「{u['web']}」互動教學網頁">
          <p>{E(u['intro'])}</p>
          <span class="intro-hint">點選文字即可開啟互動教學網頁 {EXT}</span>
        </a>
        <div class="subs"><h3>本節重點</h3><ol>{subs}</ol></div>
        <div class="tags">{tags}</div>
        <div class="btn-row">
          <a class="btn" href="{f}" target="_blank" rel="noopener">進入「{u['web']}」{EXT}</a>
          <a class="btn ghost vid" href="{V(u['vid'])}" target="_blank" rel="noopener">{PLAY}教學影片</a>
        </div>
      </div>
    </article>''')
    labs = []
    for l in c['labs']:
        f = lab_file(l)
        labs.append(f'''      <article class="lab reveal" id="lab{l['code']}">
        {fig(l['img'], l['cap'], cls='lab-fig fig-btn')}
        <div class="lab-body">
          <div class="unit-top"><span class="code sm">探討活動 {l['code']}</span><span class="web-pill">{STAR}{l['web']}</span><span class="pg-pill">{BOOK}課本 P.{l['pg']}</span></div>
          <h3>{l['title']}</h3>
          <a class="intro" href="{f}" target="_blank" rel="noopener"><p>{E(l['intro'])}</p><span class="intro-hint">開啟互動教學網頁 {EXT}</span></a>
          <div class="btn-row">
            <a class="btn ghost" href="{f}" target="_blank" rel="noopener">進入「{l['web']}」{EXT}</a>
            <a class="btn ghost vid" href="{V(l['vid'])}" target="_blank" rel="noopener">{PLAY}教學影片</a>
          </div>
        </div>
      </article>''')
    grid_cls = 'lab-grid one' if len(c['labs']) == 1 else 'lab-grid'
    pager = '<a class="pg" href="index.html"><small>HOME</small>← 回首頁總覽</a>'
    if next_c:
        pager += f'\n    <a class="pg next" href="chapter{next_c["n"]}.html"><small>NEXT CHAPTER</small>第 {next_c["n"]} 章　{next_c["name"]} →</a>'
    elif prev_c:
        pager += f'\n    <a class="pg next" href="chapter{prev_c["n"]}.html"><small>PREVIOUS CHAPTER</small>← 第 {prev_c["n"]} 章　{prev_c["name"]}</a>'
    return head(f"第 {c['n']} 章 {c['name']}｜{SITE}", c['lead'], c['a']) + f'''<body class="chapter" style="{style(c)}">
<header class="topbar">
  <div class="topbar-in">
    <a class="brand" href="index.html" aria-label="回到首頁">
      <img src="img/hanlin-logo.png" alt="翰林出版" width="40" height="40">
      <span class="brand-t"><small>翰林版</small>選修生物（Ⅳ）</span>
    </a>
    <nav class="nav">{nav}</nav>
  </div>
</header>
<header class="ch-hero">
  <div class="ch-hero-in">
    <div class="ch-hero-text">
      <div class="ch-kicker">CHAPTER {c['n']:02d} · {c['en']}</div>
      <h1><span class="big">{c['n']}</span><span class="t">第 {c['n']} 章<br><strong>{c['name']}</strong></span></h1>
      <p class="lead">{E(c['lead'])}</p>
      <div class="jump">{jump}</div>
    </div>
    <div class="ch-hero-cover"><img src="img/cover{c['n']}.jpg" alt="第 {c['n']} 章 章節封面" width="1000" height="1328"></div>
  </div>
</header>
<main class="wrap units">
{chr(10).join(arts)}
  <section class="labs" id="labs">
    <div class="sec-head reveal"><span class="eyebrow">HANDS-ON INQUIRY</span><h2>探討活動</h2><p>分析資料、動手實作與分組討論，把課文中的概念轉化為自己的科學證據與判斷。</p></div>
    <div class="{grid_cls}">
{chr(10).join(labs)}
    </div>
  </section>
  <nav class="pager">
    {pager}
  </nav>
</main>
''' + FOOT

# ---------------- 發布總表 ----------------
BASE = "https://froglssh.github.io/hanlin-elective-biology-4-web/" + quote("選生四網頁") + "/"
def table():
    L = ["# 翰林版 選修生物 (Ⅳ) 教學網頁發布總表", "",
         f"本清單為 **翰林版選修生物 (Ⅳ)** 教學網頁總表。包含全冊 {len(CHAPTERS)} 大章節、{nU} 個正課單元與 {nL} 個探討活動的 GitHub Pages 線上網址、章節入口與 Google 雲端硬碟教學影片對照。",
         "", "> 網址為 repo `hanlin-elective-biology-4-web` 推送後的預定位置；尚未 commit／push 前不會上線。", "", "---", "",
         "## 🌐 總入口網站", "", "| 網站名稱 | 🚀 網址 (GitHub Pages) | 📌 說明 | 狀態 |", "| :--- | :--- | :--- | :---: |",
         f"| **選修生物 (Ⅳ) 教材網站** | [{BASE}]({BASE}) | 全冊總覽入口：章節封面、各節課本概念圖、重點簡介、互動網頁與教學影片 | ⏳ 待推送 |",
         "", "---", "", "## 📚 各章節詳細瀏覽頁面 (Chapter Overview)", "",
         "| 章節 | 章名 | 🚀 線上瀏覽頁面 (GitHub Pages) | 單元規模 |", "| :---: | :--- | :--- | :---: |"]
    for c in CHAPTERS:
        L.append(f"| **第 {c['n']} 章** | {c['name']} | [第 {c['n']} 章導覽頁]({BASE}chapter{c['n']}.html) | {len(c['units'])} 節正課 + {len(c['labs'])} 個活動 |")
    L += ["", "---", "", f"## 📖 正課單元（{nU} 個）— 獨立互動教學網頁", "",
          "| 單元 | 頁面名稱 | 🚀 獨立網址 (GitHub Pages) | 🎬 雲端硬碟教學影片 | 課本頁碼 |", "| :---: | :--- | :--- | :--- | :---: |"]
    for c in CHAPTERS:
        for u in c['units']:
            f = unit_file(u)
            L.append(f"| **{u['code']}** | {u['web']} | [開啟網頁]({BASE}{quote(f)}) | [觀看影片]({V(u['vid'])}) | P.{u['pg']} |")
    L += ["", "---", "", f"## 🔬 探討活動（{nL} 個）— 獨立互動教學網頁", "",
          "| 單元 | 頁面名稱 | 🚀 獨立網址 (GitHub Pages) | 🎬 雲端硬碟教學影片 | 課本頁碼 |", "| :---: | :--- | :--- | :--- | :---: |"]
    for c in CHAPTERS:
        for l in c['labs']:
            f = lab_file(l)
            L.append(f"| **探討活動 {l['code']}** | {l['web']} | [開啟網頁]({BASE}{quote(f)}) | [觀看影片]({V(l['vid'])}) | P.{l['pg']} |")
    return '\n'.join(L) + '\n'

if __name__ == '__main__':
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf8').write(index())
    for i, c in enumerate(CHAPTERS):
        prev_c = CHAPTERS[i-1] if i > 0 else None
        next_c = CHAPTERS[i+1] if i + 1 < len(CHAPTERS) else None
        open(os.path.join(OUT, f'chapter{c["n"]}.html'), 'w', encoding='utf8').write(chapter(c, prev_c, next_c))
    open(os.path.join(OUT, '選修生物4網頁發布總表new.md'), 'w', encoding='utf8').write(table())
    print('built', nU, 'units', nL, 'labs')
