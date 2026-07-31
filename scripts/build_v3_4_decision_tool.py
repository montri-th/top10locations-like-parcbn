#!/usr/bin/env python3
"""Build the v3.4 Board decision tool from the immutable v3.3 checkpoint.

The analytical payload is preserved. This release changes the reading structure,
adds an A-J live sensitivity simulator, and exposes the missing PARC benchmark
without fabricating a comparable score.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "PARC_Bangna_Fresh_Locale_Screen_Board_Explainer_v3.3_AI_Routing_2026-07-30.html"
OUTPUT = ROOT / "PARC_Bangna_Fresh_Locale_Screen_Board_Decision_Tool_v3.4_2026-07-31.html"
INDEX = ROOT / "index.html"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


def between_replace(text: str, start: str, end: str, replacement: str, label: str) -> str:
    start_index = text.find(start)
    if start_index < 0:
        raise RuntimeError(f"{label}: start marker not found")
    end_index = text.find(end, start_index)
    if end_index < 0:
        raise RuntimeError(f"{label}: end marker not found")
    return text[:start_index] + replacement + text[end_index:]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


source = SOURCE.read_text(encoding="utf-8")
payload_match = re.search(
    r'<script type="application/json" id="report-data">(.*?)</script>', source, re.S
)
if not payload_match:
    raise RuntimeError("report-data payload not found")
payload = json.loads(payload_match.group(1))
portfolio = payload["portfolio"]
portfolio_by_ref = {item["ref"]: item for item in portfolio}


def leaders(key: str, limit: int = 3) -> str:
    return "".join(
        f'<li><span>{item["rank"]}</span><strong>{esc(item["name"])}</strong>'
        f'<em>{item["score"]:.1f}</em></li>'
        for item in payload["lenses"][key]["leaders"][:limit]
    )


def portfolio_leaders(metric: str, limit: int = 3) -> str:
    ranked = sorted(portfolio, key=lambda item: (-item["metrics"][metric], item["ref"]))
    return "".join(
        f'<li><span>{index}</span><strong>{esc(item["ref"])} · {esc(item["name"])}</strong>'
        f'<em>{item["metrics"][metric]:.1f}</em></li>'
        for index, item in enumerate(ranked[:limit], 1)
    )


stable = sorted(
    portfolio,
    key=lambda item: (
        item["sensitivity"]["balanced_rank_range"][1]
        - item["sensitivity"]["balanced_rank_range"][0],
        -item["sensitivity"]["balanced_top10_frequency"],
        item["ref"],
    ),
)[:3]
stable_list = "".join(
    f'<li><span>{index}</span><strong>{esc(item["ref"])} · {esc(item["name"])}</strong>'
    f'<em>#{item["sensitivity"]["balanced_rank_range"][0]}–#{item["sensitivity"]["balanced_rank_range"][1]}</em></li>'
    for index, item in enumerate(stable, 1)
)

formula_audit = "".join(
    f'<li><strong>{esc(lens["label"])}</strong><code>{esc(lens["formula"])}</code></li>'
    for lens in payload["lenses"].values()
)

decision_and_views = f'''    <section class="section decision-section">
      <div class="container">
        <div class="decision-bar">
          <div>
            <div class="eyebrow" style="color:#f1b9d2">สิ่งที่ขออนุมัติรอบนี้</div>
            <h2>ศึกษาต่อ 10 ทำเล A–J</h2>
            <p>นำทั้ง 10 ทำเลไปเช็ก route, site, คู่แข่ง และ commercial evidence ด้วยมาตรฐานเดียวกัน—ยังไม่ใช่การอนุมัติซื้อที่ดินหรือลงทุน</p>
          </div>
          <a class="button primary" href="#approval" data-approval-cta data-candidate-refs="A,B,C,D,E,F,G,H,I,J"><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M8 12l2.5 2.5L16 9"></path><circle cx="12" cy="12" r="9"></circle></svg> ดูขอบเขตที่ขออนุมัติ <span aria-hidden="true">↓</span></a>
        </div>
        <div class="decision-steps" aria-label="วิธีใช้เครื่องมือนี้">
          <span><b>1</b> อ่าน 5 คำถามตัดสินใจ</span>
          <span><b>2</b> ขยับน้ำหนักด้วยตัวเอง</span>
          <span><b>3</b> เปิดทำเลที่อันดับยังนิ่งไปพิสูจน์</span>
        </div>
      </div>
    </section>

    <section class="section alt" id="lenses">
      <div class="container">
        <div class="section-head">
          <div class="eyebrow">5 คำถามตัดสินใจ · 745 ทำเล</div>
          <h2>ไม่ต้องอ่าน 9 ตารางก่อนรู้ว่าควรถามอะไร</h2>
          <p class="lead">ยุบสูตรเดิมเป็น 5 คำถามที่ Board ใช้ค้านสมมติฐานได้ ส่วนสูตรทั้ง 9 ยังอยู่ใน audit trail ด้านล่าง</p>
        </div>
        <div class="decision-view-grid">
          <article class="decision-view" data-decision-view="resident">
            <span class="view-number">01</span><div class="eyebrow">ฐานคนอยู่</div>
            <h3>มี resident base มากพอไหม</h3>
            <p>ใช้ Resident index แยกจาก routine เพื่อไม่ให้กิจกรรมเมืองกลบฐานบ้าน</p>
            <ol class="leader-list">{leaders("resident")}</ol>
            <p class="benchmark-slot"><strong>PARC benchmark</strong><span>รอคะแนนจาก release เดียวกัน</span></p>
          </article>
          <article class="decision-view" data-decision-view="routine">
            <span class="view-number">02</span><div class="eyebrow">กิจวัตรที่เข้าถึงได้</div>
            <h3>มีเหตุให้กลับมาเป็นประจำไหม</h3>
            <p>Accessible routine รวม routine breadth กับ activity proof เพื่ออ่านความถี่ของชีวิตประจำวัน</p>
            <ol class="leader-list">{leaders("routine")}</ol>
            <p class="benchmark-slot"><strong>PARC benchmark</strong><span>รอคะแนนจาก release เดียวกัน</span></p>
          </article>
          <article class="decision-view" data-decision-view="access">
            <span class="view-number">03</span><div class="eyebrow">Barrier-aware access</div>
            <h3>Demand ยังถึงจริงเมื่อมีแม่น้ำและทางด่วนไหม</h3>
            <p>ตัวเลขเป็น geometric screen ไม่ใช่ route time; ใช้ชี้ว่าต้องพิสูจน์จุดข้ามและทางขึ้น–ลงตรงไหน</p>
            <ol class="leader-list">{leaders("barrier_resilient")}</ol>
            <p class="benchmark-slot"><strong>PARC benchmark</strong><span>รอคะแนนจาก release เดียวกัน</span></p>
          </article>
          <article class="decision-view market-view" data-decision-view="market">
            <span class="view-number">04</span><div class="eyebrow">ตำแหน่งในตลาด</div>
            <h3>Supply บางคือช่องว่าง หรือ supply หนาคือหลักฐานว่ามีตลาด</h3>
            <p>อ่านได้สองทางและยังไม่มีทางใดพิสูจน์ demand: White-space ใช้หา headroom; Observed supply ใช้ตั้ง market-validation hypothesis</p>
            <div class="market-readings">
              <div><strong>ช่องว่าง supply</strong><ol class="leader-list">{leaders("white_space")}</ol></div>
              <div><strong>ตลาดมีของแล้ว</strong><ol class="leader-list">{leaders("proven_market")}</ol></div>
            </div>
            <p class="benchmark-slot"><strong>PARC benchmark</strong><span>รอคะแนนจาก release เดียวกัน</span></p>
          </article>
          <article class="decision-view" data-decision-view="stability">
            <span class="view-number">05</span><div class="eyebrow">ความนิ่งของคำตอบ</div>
            <h3>เมื่อขยับสมมติฐาน ใครยังอยู่ข้างบน</h3>
            <p>ช่วงอันดับนี้มาจาก 13 preset เดิม; ใช้ slider ด้านล่างเพื่อทดสอบน้ำหนักของ Board เองในพอร์ต A–J</p>
            <ol class="leader-list">{stable_list}</ol>
            <p class="benchmark-slot"><strong>PARC benchmark</strong><span>รอคะแนนจาก release เดียวกัน</span></p>
            <a class="button secondary" href="#sensitivity">เปิดเครื่องมือขยับน้ำหนัก</a>
          </article>
        </div>
        <details class="lens-method formula-audit" id="nine-lens-audit">
          <summary><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"></circle><path d="M12 11v5M12 8h.01"></path></svg> Audit trail: สูตรเดิมทั้ง 9</summary>
          <ul>{formula_audit}</ul>
        </details>
      </div>
    </section>

'''

source = between_replace(
    source,
    '    <section class="section">\n      <div class="container">\n        <div class="decision-bar">',
    '    <section class="section" id="overview">',
    decision_and_views,
    "decision and five-view structure",
)

head_old = '''  <meta name="description" content="PARC Bangna Fresh Locale Screen — 10 ทำเลที่น่าสนใจคนละแบบ พร้อมคู่แข่ง แผนที่ barrier และ sensitivity analysis.">
  <meta name="theme-color" content="#f7f2e9">'''
head_new = '''  <meta name="description" content="PARC Bangna Board Decision Tool — ทดสอบน้ำหนักและจัดอันดับพอร์ต A–J สด พร้อมคู่แข่ง แผนที่ barrier และ audit trail.">
  <link rel="canonical" href="https://montri-th.github.io/top10locations-like-parcbn/">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="th_TH">
  <meta property="og:site_name" content="PARC Bangna">
  <meta property="og:title" content="PARC Bangna — Board Decision Tool">
  <meta property="og:description" content="ขยับน้ำหนักเอง แล้วดูอันดับพอร์ต 10 ทำเล A–J เปลี่ยนสด พร้อมหลักฐานและข้อจำกัดที่ตรวจสอบได้">
  <meta property="og:url" content="https://montri-th.github.io/top10locations-like-parcbn/">
  <meta property="og:image" content="https://montri-th.github.io/top10locations-like-parcbn/assets/parc-bangna-logo-transparent.png">
  <meta property="og:image:width" content="1023">
  <meta property="og:image:height" content="377">
  <meta property="og:image:alt" content="PARC Bangna">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="PARC Bangna — Board Decision Tool">
  <meta name="twitter:description" content="ขยับน้ำหนักเอง แล้วดูอันดับพอร์ต 10 ทำเล A–J เปลี่ยนสด">
  <meta name="twitter:image" content="https://montri-th.github.io/top10locations-like-parcbn/assets/parc-bangna-logo-transparent.png">
  <meta name="theme-color" content="#f7f2e9">'''
source = replace_once(source, head_old, head_new, "social metadata")
source = replace_once(
    source,
    '<title>PARC Bangna — 10 ทำเลที่น่าสนใจคนละแบบ</title>',
    '<title>PARC Bangna — Board Decision Tool</title>',
    "document title",
)
source = replace_once(
    source,
    '<body data-release-id="parc-fresh-vli-multilens-v3.3" data-interface-release="v3.3-ai-routing" data-design-system="J Lifestyle Center v0.3">',
    '<body data-release-id="parc-fresh-vli-multilens-v3.3" data-interface-release="v3.4-board-decision-tool" data-design-system="J Lifestyle Center v0.3">',
    "body release metadata",
)
source = replace_once(
    source,
    'Fresh Locale Screen · Board working view · 29 กรกฎาคม 2026',
    'Fresh Locale Screen · Board decision tool · 31 กรกฎาคม 2026',
    "hero release date",
)
source = replace_once(
    source,
    '<dt>มุมมอง</dt><dd>9</dd>',
    '<dt>คำถามตัดสินใจ</dt><dd>5</dd>',
    "hero view count",
)
source = replace_once(
    source,
    '<span>PARC Bangna · Fresh Locale Screen · parc-fresh-vli-multilens-v3.3</span>',
    '<span>PARC Bangna · analytical release v3.3 · interface v3.4</span>',
    "footer release provenance",
)

css = r'''
.decision-section{padding:clamp(2rem,4vw,3.5rem) 0 clamp(2.2rem,3.5vw,3.5rem)}
.decision-section+#lenses{padding-top:clamp(2.3rem,3.5vw,3.5rem)}
.decision-section .decision-bar,.approval{background:#365e55;color:#fff}
.overview-markers .map-hit{pointer-events:none}
.overview-visual-markers .candidate-dot{cursor:pointer}
.decision-bar .button.primary{background:#fffdf8;color:#203a35;border-color:#fffdf8;box-shadow:0 .45rem 1.2rem rgb(0 0 0 / 14%)}
.decision-bar .button.primary:hover{background:#f3e0e8;color:#203a35;border-color:#f3e0e8}
.decision-bar .button.primary:focus-visible{outline-color:#fffdf8;box-shadow:0 0 0 6px rgb(32 58 53 / 72%)}
.decision-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;margin-top:1rem;overflow:hidden;border:1px solid var(--line);border-radius:var(--radius);background:var(--line)}
.decision-steps span{display:flex;align-items:center;gap:.65rem;min-height:54px;padding:.65rem .9rem;background:var(--card);font-size:.82rem;color:var(--muted)}
.decision-steps b{display:grid;place-items:center;flex:0 0 auto;width:1.65rem;height:1.65rem;border-radius:50%;background:var(--garden-soft);color:var(--garden-deep)}
.decision-view-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem}
.decision-view{position:relative;min-width:0;padding:1.35rem;background:var(--card);border:1px solid var(--line);border-radius:var(--radius)}
.decision-view h3{padding-right:2.5rem}
.decision-view>p{color:var(--muted);font-size:.88rem}
.view-number{position:absolute;right:1rem;top:1rem;font-family:var(--display);font-size:1.4rem;color:var(--petal-deep)}
.market-view{grid-column:span 2}
.market-readings{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
.market-readings>div{min-width:0;padding:1rem;border-radius:.7rem;background:var(--canvas)}
.market-readings>div>strong{display:block;margin-bottom:.45rem}
.benchmark-slot{display:flex;align-items:center;justify-content:space-between;gap:.75rem;margin:1rem 0 0!important;padding-top:.75rem;border-top:1px dashed var(--line);font-size:.72rem!important}
.benchmark-slot strong{color:var(--ink)}.benchmark-slot span{color:#81521c}
html[data-theme="dark"] .benchmark-slot span{color:#e2b371}
.formula-audit{margin-top:1.2rem;padding:.8rem 1rem;border:1px solid var(--line);border-radius:var(--radius);background:var(--card)}
.formula-audit ul{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.55rem 1.4rem;padding:0;margin:.7rem 0;list-style:none}
.formula-audit li{display:grid;gap:.15rem;padding:.5rem 0;border-top:1px solid var(--line);font-size:.78rem}
.formula-audit code{white-space:normal;color:var(--muted)}
.portfolio-origin{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;margin:0 0 1.2rem;border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;background:var(--line)}
.portfolio-origin span{padding:.8rem 1rem;background:var(--canvas);font-size:.8rem;color:var(--muted)}
.portfolio-origin b{display:block;color:var(--ink);font-size:.86rem}
.benchmark-gap{display:grid;grid-template-columns:auto 1fr;gap:.8rem 1rem;margin-bottom:1.2rem;padding:1rem 1.1rem;border:1px solid var(--amber);border-radius:var(--radius);background:color-mix(in srgb,var(--card) 88%,var(--amber));font-size:.84rem}
.benchmark-gap .status-pill{align-self:start;background:var(--amber);color:#14110e}
.benchmark-gap h3{margin:0;font-size:1.12rem}.benchmark-gap p{margin:.25rem 0 0;color:var(--muted)}
.decision-tool{display:grid;grid-template-columns:minmax(18rem,.7fr) minmax(0,1.3fr);gap:1.4rem;align-items:start}
.tool-controls{position:sticky;top:6rem;padding:1.2rem;border:1px solid var(--line);border-radius:var(--radius);background:var(--card)}
.tool-controls>label,.control-group>label,.control-title{display:block;margin:.9rem 0 .35rem;font-weight:500;font-size:.84rem}
.tool-controls select{display:block;width:100%;min-height:48px;padding:.6rem 2.7rem .6rem .8rem;border:1px solid var(--line);border-radius:.55rem;background:var(--canvas);color:var(--ink)}
.weight-control{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:.15rem .7rem;align-items:center;padding:.45rem 0;border-top:1px solid var(--line)}
.weight-control label{font-size:.82rem}.weight-control output{font-variant-numeric:tabular-nums;color:var(--garden-deep);font-weight:500}
.weight-control input[type="range"]{grid-column:1/-1;width:100%;min-height:36px;accent-color:var(--garden);cursor:pointer}
.weight-total{margin:.35rem 0 .7rem;font-size:.75rem;color:var(--muted)}
.segmented{display:grid;grid-template-columns:1fr 1fr;gap:.45rem}
.segmented label{position:relative;display:block;cursor:pointer}
.segmented input{position:absolute;opacity:0;pointer-events:none}
.segmented span{display:flex;align-items:center;justify-content:center;min-height:48px;padding:.5rem .65rem;border:1px solid var(--line);border-radius:.6rem;background:var(--canvas);font-size:.78rem;text-align:center}
.segmented input:checked+span{border-color:var(--garden);background:var(--garden-soft);color:var(--garden-deep);font-weight:500}
.segmented input:focus-visible+span{outline:3px solid var(--petal);outline-offset:2px}
.tool-actions{display:flex;gap:.6rem;margin-top:1rem}.tool-actions .button{min-height:44px;padding:.55rem .85rem}
.live-ranking{min-width:0}.live-summary{min-height:3.5rem;margin:0 0 .7rem;padding:.75rem 1rem;border-left:3px solid var(--garden);background:var(--garden-soft);color:var(--garden-deep);font-size:.86rem}
.live-table a{color:var(--petal-deep);font-weight:500;text-decoration-thickness:.08em;text-underline-offset:.18em}
.rank-move{font-variant-numeric:tabular-nums}.rank-move.up{color:var(--garden-deep)}.rank-move.down{color:var(--petal-deep)}
.benchmark-row th,.benchmark-row td{background:color-mix(in srgb,var(--card) 82%,var(--amber));border-top:2px solid var(--amber)}
.benchmark-row td{color:var(--muted)}
.scenario-audit{margin-top:1.2rem;padding:.8rem 1rem;border:1px solid var(--line);border-radius:var(--radius);background:var(--card)}
.scenario-audit summary{display:flex;align-items:center;min-height:44px;cursor:pointer;font-weight:500}
.scenario-audit .table-wrap{margin-top:.7rem}.scenario-audit table{font-size:.76rem}
.back-to-tool{display:none}
@media(max-height:800px) and (min-width:901px){.tool-controls{position:static}}
'''
source = replace_once(
    source,
    '@media(max-width:900px){',
    css + '''
@media(max-width:900px){''',
    "v3.4 styles",
)
source = replace_once(
    source,
    '  .decision-bar{grid-template-columns:1fr}.principle-grid,.pattern-grid{grid-template-columns:repeat(2,1fr)}',
    '  .decision-bar{grid-template-columns:1fr}.decision-view-grid{grid-template-columns:1fr}.market-view{grid-column:auto}.pattern-grid{grid-template-columns:repeat(2,1fr)}\n  .decision-tool{grid-template-columns:1fr}.tool-controls{position:static}.portfolio-origin{grid-template-columns:1fr}\n  .back-to-tool{display:inline-flex;align-items:center;min-height:44px;margin:0 0 .8rem;color:var(--petal-deep);font-weight:500}',
    "tablet layout",
)
source = replace_once(
    source,
    '  .principle-grid,.pattern-grid,.lens-grid,.diagnostic-grid,.reserve-grid{grid-template-columns:1fr}.signal-row{grid-template-columns:repeat(2,1fr)}',
    '  .decision-steps,.decision-view-grid,.market-readings,.pattern-grid,.lens-grid,.diagnostic-grid,.reserve-grid,.formula-audit ul{grid-template-columns:1fr}.market-view{grid-column:auto}.signal-row{grid-template-columns:repeat(2,1fr)}\n  .benchmark-slot{align-items:flex-start;flex-direction:column}.segmented{grid-template-columns:1fr}',
    "mobile layout",
)

portfolio_lead = '<p class="lead">ตั้งใจให้พอร์ตมีทั้งตลาดที่ supply ยังบาง ตลาดที่มีคู่แข่งให้เข้าไปชนะ และทำเลที่ต้องพิสูจน์ผลของ barrier</p>'
portfolio_origin = portfolio_lead + '''
          <div class="portfolio-origin" aria-label="ที่มาของพอร์ต 3 บวก 3 บวก 3 บวก 1">
            <span><b>1 · สร้าง candidate pool</b>รวม Top 20 จากสูตรทั้ง 9 และ Pareto fronts</span>
            <span><b>2 · ลดความซ้ำ</b>ทบทวน host complex, catchment family และความซ้ำเชิงภูมิศาสตร์</span>
            <span><b>3 · ใช้ quota หลังคำนวณ</b>3 anchors + 3 white-space + 3 challengers + 1 barrier test; A–J ไม่ใช่อันดับ</span>
          </div>'''
source = replace_once(source, portfolio_lead, portfolio_origin, "portfolio provenance")

def rank_badge(rank: int) -> str:
    top = " top" if rank <= 10 else ""
    return f'<span class="matrix-rank{top}">#{rank}</span>'


five_matrix_rows = "".join(
    f'''<tr data-matrix-ref="{item["ref"]}">
      <th scope="row">{item["ref"]} · {esc(item["name"])}</th>
      <td>{rank_badge(item["ranks"]["resident"])}</td>
      <td>{rank_badge(item["ranks"]["routine"])}</td>
      <td>{rank_badge(item["ranks"]["barrier_resilient"])}</td>
      <td><small>Gap {rank_badge(item["ranks"]["white_space"])}</small><small>Observed {rank_badge(item["ranks"]["proven_market"])}</small></td>
      <td data-number>#{item["sensitivity"]["balanced_rank_range"][0]}–#{item["sensitivity"]["balanced_rank_range"][1]}</td>
    </tr>'''
    for item in portfolio
)

five_matrix = f'''    <section class="section">
      <div class="container">
        <div class="section-head">
          <div class="eyebrow">เทียบ A–J ด้วย 5 คำถาม</div>
          <h2>เห็นเหตุผลที่เด่น โดยไม่ต้องกวาดตา 9 คอลัมน์</h2>
          <p>สามคอลัมน์แรกเป็นอันดับเทียบ 745; Market position เก็บการอ่านสองทางไว้ในช่องเดียว; Stability คือช่วงอันดับ Balanced เมื่อผ่าน 13 preset</p>
        </div>
        <div class="table-wrap matrix">
          <table data-portfolio-matrix>
            <caption>5 decision views ของ A–J — ตัวอักษรเป็นรหัส ไม่ใช่อันดับ</caption>
            <thead><tr><th>ทำเล</th><th>1 · ฐานคนอยู่</th><th>2 · Routine</th><th>3 · Barrier-resilient</th><th>4 · Market position</th><th>5 · Stability</th></tr></thead>
            <tbody>{five_matrix_rows}</tbody>
            <tfoot><tr class="benchmark-row"><th scope="row">PARC Bangna · reference</th><td colspan="5">— รอ same-release score; ไม่ใส่อันดับ</td></tr></tfoot>
          </table>
        </div>
      </div>
    </section>

'''
source = between_replace(
    source,
    '    <section class="section">\n      <div class="container">\n        <div class="section-head">\n          <div class="eyebrow">เทียบ A–J ทุกมุม</div>',
    '    <section class="section alt" id="detail">',
    five_matrix,
    "five-view portfolio matrix",
)

for ref in "ABCDEFGHIJ":
    pattern = rf'<article class="detail-panel" data-detail-panel="{ref}"(.*?)>'
    source, count = re.subn(
        pattern,
        rf'<article class="detail-panel" id="detail-{ref}" data-detail-panel="{ref}"\1><a class="back-to-tool" href="#sensitivity">← กลับไปเครื่องมือทดสอบสมมติฐาน</a>',
        source,
        count=1,
    )
    if count != 1:
        raise RuntimeError(f"detail anchor {ref}: expected one panel, found {count}")

role_labels = {
    "A": "Anchor เด่นหลายมุม",
    "B": "Anchor เด่นหลายมุม",
    "C": "White-space builder",
    "D": "Anchor เด่นหลายมุม",
    "E": "White-space builder",
    "F": "White-space builder",
    "G": "Observed-supply challenger",
    "H": "Observed-supply challenger",
    "I": "Observed-supply challenger",
    "J": "Barrier experiment",
}

base_results = {
    item["ref"]: next(result for result in item["sensitivity"]["scenarios"] if result["id"] == "base")
    for item in portfolio
}
base_order = sorted(portfolio, key=lambda item: (-base_results[item["ref"]]["score"], item["ref"]))
initial_rows = "".join(
    f'''<tr data-live-ref="{item["ref"]}">
      <td data-number>#{index}</td>
      <th scope="row"><a href="#detail-{item["ref"]}" data-live-detail="{item["ref"]}">{item["ref"]} · {esc(item["name"])}</a></th>
      <td data-number>{base_results[item["ref"]]["score"]:.2f}</td>
      <td><span class="rank-move">—</span></td>
      <td data-number>#{item["ranks"]["balanced"]}</td>
      <td>{esc(role_labels[item["ref"]])}</td>
    </tr>'''
    for index, item in enumerate(base_order, 1)
)

scenario_options = '<option value="custom">กำหนดเองจาก slider</option>' + "".join(
    f'<option value="{esc(scenario["id"])}">{esc(scenario["label"])}</option>'
    for scenario in payload["scenarios"]
)
scenario_audit_head = "".join(f"<th>{ref}</th>" for ref in "ABCDEFGHIJ")
scenario_audit_rows = "".join(
    '<tr><th scope="row">' + esc(scenario["label"]) + "</th>" + "".join(
        f'<td data-number>{next(result for result in portfolio_by_ref[ref]["sensitivity"]["scenarios"] if result["id"] == scenario["id"])["score"]:.2f} · #{next(result for result in portfolio_by_ref[ref]["sensitivity"]["scenarios"] if result["id"] == scenario["id"])["rank"]}</td>'
        for ref in "ABCDEFGHIJ"
    ) + "</tr>"
    for scenario in payload["scenarios"]
)

sensitivity = f'''    <section class="section" id="sensitivity">
      <div class="container">
        <div class="section-head">
          <div class="eyebrow">เครื่องมือทดสอบสมมติฐาน</div>
          <h2>ขยับน้ำหนักเอง แล้วดู A–J เปลี่ยนอันดับสด</h2>
          <p class="lead">สูตรคำนวณจากข้อมูลที่ฝังอยู่แล้วและจัดอันดับใหม่เฉพาะพอร์ต 10 ทำเล ไม่ได้อ้างว่า recalibrate ทั้ง 745 ทำเลเมื่อใช้ค่าน้ำหนักกำหนดเอง</p>
        </div>
        <aside class="benchmark-gap" data-benchmark-status="unscored">
          <span class="status-pill">Benchmark gap</span>
          <div><h3>PARC Bangna ยังไม่มีคะแนนที่เทียบด้วยกติกาเดียวกัน</h3>
          <p>นี่ไม่ใช่คะแนน 0: PARC ถูกกันออกจาก 745 ทำเลเพื่อไม่คัดทับโครงการเดิม และ Locale Insight v2.3 ระบุว่ายังไม่มี approved percentile capsule. ต้องได้ reference geometry และ raw inputs ชุดเดียวกับ v2.3.1 แล้ว score แบบ out-of-sample เทียบ distribution 745 ที่ตรึงไว้—จากนั้นจึงปัก PARC เป็นเส้นอ้างอิงโดยไม่ให้อันดับ</p></div>
        </aside>
        <div class="decision-tool">
          <aside class="tool-controls" aria-label="ตัวควบคุมน้ำหนักและสมมติฐาน">
            <label for="scenario-select">เริ่มจาก preset ที่ตรวจไว้แล้ว</label>
            <select id="scenario-select" data-scenario-select>{scenario_options}</select>

            <div class="control-title">น้ำหนักที่ใช้จริงจะ normalize รวมเป็น 100%</div>
            <div class="weight-control"><label for="weight-resident">ฐานคนอยู่</label><output for="weight-resident" data-weight-share="resident">40.00%</output><input id="weight-resident" type="range" min="0" max="100" step="0.1" value="40" data-weight="resident" aria-valuetext="ใช้จริง 40.00%"></div>
            <div class="weight-control"><label for="weight-routine">กิจวัตรที่เข้าถึงได้</label><output for="weight-routine" data-weight-share="routine">25.00%</output><input id="weight-routine" type="range" min="0" max="100" step="0.1" value="25" data-weight="routine" aria-valuetext="ใช้จริง 25.00%"></div>
            <div class="weight-control"><label for="weight-access">Barrier-aware access</label><output for="weight-access" data-weight-share="access">20.00%</output><input id="weight-access" type="range" min="0" max="100" step="0.1" value="20" data-weight="access" aria-valuetext="ใช้จริง 20.00%"></div>
            <div class="weight-control"><label for="weight-market">ตำแหน่งในตลาด</label><output for="weight-market" data-weight-share="market">15.00%</output><input id="weight-market" type="range" min="0" max="100" step="0.1" value="15" data-weight="market" aria-valuetext="ใช้จริง 15.00%"></div>
            <p class="weight-total" id="weight-total" data-weight-total>ค่าน้ำหนักดิบ 100 · ใช้จริงรวม 100.00%</p>

            <div class="control-group"><label for="access-assumption">สมมติฐานการข้าม barrier</label><select id="access-assumption" data-access-assumption><option value="base">ฐาน 55% river / 20% expressway</option><option value="optimistic">ข้ามง่ายขึ้น 40% / 10%</option><option value="conservative">กั้นมากขึ้น 75% / 35%</option></select></div>
            <div class="control-group"><label for="gap-assumption">สมมติฐาน supply ที่ไม่ทราบขนาด</label><select id="gap-assumption" data-gap-assumption><option value="central">ฐาน: subtype median</option><option value="conservative">P75 + radius 3.33 กม.</option><option value="optimistic">P25 + radius 2.50 กม.</option></select></div>
            <fieldset class="control-group" style="border:0;padding:0;margin:0"><legend class="control-title">ตีความ supply อย่างไร</legend><div class="segmented">
              <label><input type="radio" name="market-mode" value="gap" checked data-market-mode><span>ช่องว่าง supply</span></label>
              <label><input type="radio" name="market-mode" value="observed" data-market-mode><span>ตลาดมี supply แล้ว</span></label>
            </div></fieldset>
            <div class="tool-actions"><button class="button secondary" type="button" data-reset-tool>กลับสูตรฐาน</button></div>
            <p class="method-note">โหมด “ตลาดมี supply แล้ว” ใช้ competition pressure เป็น market-validation hypothesis เท่านั้น ไม่ใช่ proof ของ demand, spend หรือ performance</p>
          </aside>
          <div class="live-ranking">
            <p class="live-summary" data-live-summary aria-live="polite">กำลังคำนวณอันดับ A–J…</p>
            <div class="table-wrap">
              <table class="live-table" data-live-ranking>
                <caption>อันดับสดภายในพอร์ต A–J; อันดับเทียบ 745 แสดงเฉพาะสูตรฐานที่ตรึงไว้</caption>
                <thead><tr><th>อันดับสด A–J</th><th>ทำเล</th><th>คะแนนสด</th><th>ขยับจากฐาน A–J</th><th>อันดับฐาน /745</th><th>บทบาท</th></tr></thead>
                <tbody data-live-rank-body>{initial_rows}</tbody>
                <tfoot><tr class="benchmark-row"><th scope="row" colspan="2">PARC Bangna · reference</th><td colspan="4">— ยังไม่มี same-release score; ไม่ใส่เลขแทนข้อมูลที่ขาด</td></tr></tfoot>
              </table>
            </div>
          </div>
        </div>
        <details class="scenario-audit">
          <summary>Audit trail: เปิดดูผล 13 preset × 10 ทำเลที่คำนวณไว้ล่วงหน้า</summary>
          <div class="table-wrap"><table><caption>คะแนน · อันดับเทียบ 745 ของแต่ละ preset</caption><thead><tr><th>Preset</th>{scenario_audit_head}</tr></thead><tbody>{scenario_audit_rows}</tbody></table></div>
        </details>
      </div>
    </section>

'''
source = between_replace(
    source,
    '    <section class="section" id="sensitivity">',
    '    <section class="section alt" id="reserves">',
    sensitivity,
    "live sensitivity tool",
)

old_select = '''  function selectCandidate(ref, options = {}) {
    const candidate = portfolioByRef.get(ref);
    if (!candidate) return;
    activeRef = ref;
    detailSelect.value = ref;
    document.querySelectorAll("[data-detail-panel]").forEach((panel) => {
      panel.hidden = panel.dataset.detailPanel !== ref;
    });
    staticFallback.innerHTML = staticDetail(candidate);
    updateMapData(candidate, true);
    if (options.scroll) document.getElementById("detail").scrollIntoView({ behavior: "smooth", block: "start" });
    history.replaceState(null, "", `#detail-${ref}`);
  }'''
new_select = '''  function selectCandidate(ref, options = {}) {
    const candidate = portfolioByRef.get(ref);
    if (!candidate) return;
    activeRef = ref;
    detailSelect.value = ref;
    document.querySelectorAll("[data-detail-panel]").forEach((panel) => {
      panel.hidden = panel.dataset.detailPanel !== ref;
    });
    staticFallback.innerHTML = staticDetail(candidate);
    updateMapData(candidate, true);
    const detailTarget = document.getElementById(`detail-${ref}`);
    if (options.scroll && detailTarget) detailTarget.scrollIntoView({ behavior: "smooth", block: "start" });
    if (options.updateHash !== false && location.hash !== `#detail-${ref}`) {
      const method = options.pushHistory ? "pushState" : "replaceState";
      history[method](null, "", `#detail-${ref}`);
    }
  }'''
source = replace_once(source, old_select, new_select, "working detail anchors")

overview_listener = '''  const overviewSvg = document.querySelector("[data-overview-map] > svg");
  overviewSvg?.addEventListener("click", (event) => {
    if (event.detail === 0 || event.target.closest("[data-overview-marker]")) return;
    const matrix = overviewSvg.getScreenCTM();
    if (!matrix) return;
    const point = overviewSvg.createSVGPoint();
    point.x = event.clientX; point.y = event.clientY;
    const local = point.matrixTransform(matrix.inverse());
    const nearest = [...overviewSvg.querySelectorAll("[data-overview-marker]")].map((marker) => {
      const circle = marker.querySelector("circle");
      const dx = local.x - circle.cx.baseVal.value;
      const dy = local.y - circle.cy.baseVal.value;
      return { marker, distance: Math.hypot(dx, dy) };
    }).sort((a, b) => a.distance - b.distance)[0];
    if (!nearest || nearest.distance > 26) return;
    event.preventDefault();
    selectCandidate(nearest.marker.dataset.ref, { scroll: true });
  });

'''
source = replace_once(
    source,
    '  document.querySelectorAll("[data-overview-marker],[data-overview-mobile]").forEach((marker) => {',
    overview_listener + '  document.querySelectorAll("[data-overview-marker],[data-overview-mobile]").forEach((marker) => {',
    "nearest-point overview routing",
)

scenario_js_start = '  const scenarioSelect = document.querySelector("[data-scenario-select]");'
scenario_js_end = '  const hashMatch = location.hash.match(/^#detail-([A-J])$/);'
scenario_js = r'''  const scenarioSelect = document.querySelector("[data-scenario-select]");
  const weightInputs = [...document.querySelectorAll("[data-weight]")];
  const accessAssumption = document.querySelector("[data-access-assumption]");
  const gapAssumption = document.querySelector("[data-gap-assumption]");
  const liveRankBody = document.querySelector("[data-live-rank-body]");
  const liveSummary = document.querySelector("[data-live-summary]");
  const roleLabels = {
    A: "Anchor เด่นหลายมุม", B: "Anchor เด่นหลายมุม", C: "White-space builder",
    D: "Anchor เด่นหลายมุม", E: "White-space builder", F: "White-space builder",
    G: "Observed-supply challenger", H: "Observed-supply challenger", I: "Observed-supply challenger",
    J: "Barrier experiment"
  };
  const baseScoreByRef = new Map(payload.portfolio.map((candidate) => [candidate.ref,
    candidate.sensitivity.scenarios.find((scenario) => scenario.id === "base").score
  ]));
  const baseOrder = [...payload.portfolio].sort((a, b) => baseScoreByRef.get(b.ref) - baseScoreByRef.get(a.ref) || a.ref.localeCompare(b.ref));
  const basePortfolioRank = new Map(baseOrder.map((candidate, index) => [candidate.ref, index + 1]));
  const clamp = (value) => Math.max(0, Math.min(100, value));

  function displayedWeightBasisPoints(weights) {
    const shares = Object.entries(weights).map(([key, value]) => {
      const exact = value * 10000;
      return { key, units: Math.floor(exact), remainder: exact - Math.floor(exact) };
    });
    let remaining = 10000 - shares.reduce((sum, share) => sum + share.units, 0);
    shares.sort((a, b) => b.remainder - a.remainder || a.key.localeCompare(b.key));
    shares.forEach((share) => { if (remaining-- > 0) share.units += 1; });
    return Object.fromEntries(shares.map(({ key, units }) => [key, units]));
  }

  function normalizedWeights(presetWeights = null) {
    const raw = presetWeights
      ? Object.fromEntries(Object.entries(presetWeights).map(([key, value]) => [key, value * 100]))
      : Object.fromEntries(weightInputs.map((input) => [input.dataset.weight, Number(input.value)]));
    const total = Object.values(raw).reduce((sum, value) => sum + value, 0);
    const divisor = total > 0 ? total : 4;
    const weights = total > 0
      ? Object.fromEntries(Object.entries(raw).map(([key, value]) => [key, value / divisor]))
      : { resident: .25, routine: .25, access: .25, market: .25 };
    const displayed = displayedWeightBasisPoints(weights);
    Object.entries(displayed).forEach(([key, units]) => {
      const share = `${(units / 100).toFixed(2)}%`;
      document.querySelector(`[data-weight-share="${key}"]`).textContent = share;
      document.querySelector(`[data-weight="${key}"]`)?.setAttribute("aria-valuetext", `ใช้จริง ${share}`);
    });
    document.querySelector("[data-weight-total]").textContent = total > 0
      ? `ค่าน้ำหนักดิบ ${fmt(total, 1)} · ใช้จริงรวม 100.00%`
      : "ค่าน้ำหนักดิบ 0 · ทุกค่าเป็นศูนย์ จึงใช้ 25.00% เท่ากัน";
    return weights;
  }

  function setWeights(weights) {
    const values = {
      resident: weights.resident,
      routine: weights.routine,
      access: weights.access,
      market: weights.competition
    };
    weightInputs.forEach((input) => { input.value = String(Math.round(values[input.dataset.weight] * 1000) / 10); });
  }

  function lowSupplyValue(candidate, gap) {
    if (gap === "central") return candidate.metrics.low_supply_signal;
    const scenarioId = gap === "conservative" ? "vli_conservative" : "vli_optimistic";
    const scenario = payload.scenarios.find((item) => item.id === scenarioId);
    const result = candidate.sensitivity.scenarios.find((item) => item.id === scenarioId);
    const known = scenario.weights.resident * candidate.metrics.resident
      + scenario.weights.routine * candidate.metrics.routine
      + scenario.weights.access * candidate.barrier.access_base;
    return clamp((result.score - known) / scenario.weights.competition);
  }

  function accessValue(candidate, assumption) {
    if (assumption === "optimistic") return candidate.barrier.access_optimistic;
    if (assumption === "conservative") return candidate.barrier.access_conservative;
    return candidate.barrier.access_base;
  }

  function currentMarketMode() {
    return document.querySelector("[data-market-mode]:checked")?.value || "gap";
  }

  function scoreCandidate(candidate, weights) {
    const lowSupply = lowSupplyValue(candidate, gapAssumption.value);
    const market = currentMarketMode() === "observed" ? 100 - lowSupply : lowSupply;
    return weights.resident * candidate.metrics.resident
      + weights.routine * candidate.metrics.routine
      + weights.access * accessValue(candidate, accessAssumption.value)
      + weights.market * market;
  }

  function renderLiveRanking(presetWeights = null) {
    const weights = normalizedWeights(presetWeights);
    const ranked = payload.portfolio.map((candidate) => ({ candidate, score: scoreCandidate(candidate, weights) }))
      .sort((a, b) => b.score - a.score || a.candidate.ref.localeCompare(b.candidate.ref));
    liveRankBody.innerHTML = ranked.map(({ candidate, score }, index) => {
      const liveRank = index + 1;
      const move = basePortfolioRank.get(candidate.ref) - liveRank;
      const moveText = move > 0 ? `↑ ${move}` : move < 0 ? `↓ ${Math.abs(move)}` : "—";
      const moveClass = move > 0 ? "up" : move < 0 ? "down" : "";
      return `<tr data-live-ref="${candidate.ref}">
        <td data-number>#${liveRank}</td>
        <th scope="row"><a href="#detail-${candidate.ref}" data-live-detail="${candidate.ref}">${candidate.ref} · ${esc(candidate.name)}</a></th>
        <td data-number>${fmt(score, 2)}</td>
        <td><span class="rank-move ${moveClass}">${moveText}</span></td>
        <td data-number>#${candidate.ranks.balanced}</td>
        <td>${roleLabels[candidate.ref]}</td>
      </tr>`;
    }).join("");
    const modeLabel = currentMarketMode() === "observed" ? "ตีความ supply เป็น market-validation hypothesis" : "ตีความ supply บางเป็นช่องว่าง";
    liveSummary.textContent = `อันดับ 1 ในพอร์ต: ${ranked[0].candidate.ref} · ${ranked[0].candidate.name} (${fmt(ranked[0].score, 2)}) · ${modeLabel} · เป็นอันดับ A–J ไม่ใช่อันดับใหม่ของ 745 ทำเล`;
  }

  function applyScenario(scenarioId) {
    const scenario = payload.scenarios.find((item) => item.id === scenarioId);
    if (!scenario) { renderLiveRanking(); return; }
    setWeights(scenario.weights);
    gapAssumption.value = scenario.gap === "base" ? "central" : scenario.gap;
    accessAssumption.value = scenario.access;
    const gapMode = document.querySelector('[data-market-mode][value="gap"]');
    gapMode.checked = true;
    renderLiveRanking({
      resident: scenario.weights.resident,
      routine: scenario.weights.routine,
      access: scenario.weights.access,
      market: scenario.weights.competition
    });
  }

  scenarioSelect.addEventListener("change", () => applyScenario(scenarioSelect.value));
  weightInputs.forEach((input) => input.addEventListener("input", () => {
    scenarioSelect.value = "custom";
    renderLiveRanking();
  }));
  [accessAssumption, gapAssumption].forEach((control) => control.addEventListener("change", () => {
    scenarioSelect.value = "custom";
    renderLiveRanking();
  }));
  document.querySelectorAll("[data-market-mode]").forEach((control) => control.addEventListener("change", () => {
    scenarioSelect.value = "custom";
    renderLiveRanking();
  }));
  document.querySelector("[data-reset-tool]").addEventListener("click", () => {
    scenarioSelect.value = "base";
    applyScenario("base");
  });
  liveRankBody.addEventListener("click", (event) => {
    const link = event.target.closest("[data-live-detail]");
    if (!link) return;
    event.preventDefault();
    selectCandidate(link.dataset.liveDetail, { scroll: true, pushHistory: true });
  });
  scenarioSelect.value = "base";
  applyScenario("base");

'''
source = between_replace(source, scenario_js_start, scenario_js_end, scenario_js, "live tool JavaScript")

hash_old = '''  const hashMatch = location.hash.match(/^#detail-([A-J])$/);
  if (hashMatch) selectCandidate(hashMatch[1]);
  initializeMap();'''
hash_new = '''  function selectDetailFromHash(scroll = false) {
    const match = location.hash.match(/^#detail-([A-J])$/);
    if (!match) return false;
    selectCandidate(match[1], { scroll, updateHash: false });
    return true;
  }
  window.addEventListener("hashchange", () => selectDetailFromHash(true));
  if (selectDetailFromHash(false)) requestAnimationFrame(() => selectDetailFromHash(true));
  initializeMap();'''
source = replace_once(source, hash_old, hash_new, "direct detail hash handling")

source = source.replace(
    '<a href="#lenses">มุมมอง</a>',
    '<a href="#lenses">5 คำถาม</a><a href="#sensitivity">ลองน้ำหนัก</a>',
    1,
)

OUTPUT.write_text(source, encoding="utf-8")
INDEX.write_text(source, encoding="utf-8")
print(f"Wrote {OUTPUT.name} and index.html ({len(source.encode('utf-8')):,} bytes each)")
