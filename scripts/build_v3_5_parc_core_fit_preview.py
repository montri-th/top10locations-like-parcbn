#!/usr/bin/env python3
"""Build v3.5 by adding a separate PARC host-proxy core-fit preview to v3.4.

The immutable v3.3 report-data payload and the v3.4 A-J sensitivity tool are
preserved. The addendum is a new, explicitly versioned analytical preview built
from the current v2.3.1 Registry snapshot. It must not be called a PARC Bangna
venue or trade-area benchmark.
"""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "PARC_Bangna_Fresh_Locale_Screen_Board_Decision_Tool_v3.4_2026-07-31.html"
DATA = ROOT / "analysis/parc-host-proxy-core-fit-preview-v0.1.json"
OUTPUT = ROOT / "PARC_Bangna_Fresh_Locale_Screen_Board_Decision_Tool_v3.5_PARC_Core_Fit_Preview_2026-08-01.html"
INDEX = ROOT / "index.html"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def fmt(value: float | None, digits: int = 1) -> str:
    return "—" if value is None else f"{value:.{digits}f}"


source = SOURCE.read_text(encoding="utf-8")
data = json.loads(DATA.read_text(encoding="utf-8"))
reference = data["reference"]
scores = reference["scores_out_of_sample_against_frozen_745"]
rows = data["top_10_core_fit_before_route_site_and_economics_gates"]

if len(rows) != 10 or len({row["locale_id"] for row in rows}) != 10:
    raise RuntimeError("core-fit preview must contain 10 unique locales")


def locale_label(row: dict[str, object]) -> str:
    name = esc(row["locale_name_th"])
    ref = row.get("current_portfolio_ref")
    if ref:
        return f'<a href="#detail-{esc(ref)}">{name} <small>· พอร์ต {esc(ref)}</small></a>'
    return name


def land_badge(row: dict[str, object]) -> str:
    percentile = row.get("land_price_percentile")
    if percentile is None:
        return '<span class="fit-diagnostic missing">ยังขาด</span>'
    level = "high" if float(percentile) >= 80 else "watch" if float(percentile) >= 60 else "lower"
    return f'<span class="fit-diagnostic {level}">p{float(percentile):.1f}</span>'


fit_rows = "".join(
    f'''<tr data-core-fit-locale="{esc(row["locale_id"])}">
      <td data-number>#{row["rank"]}</td>
      <th scope="row">{locale_label(row)}</th>
      <td data-number>{row["similarity"]:.1f}</td>
      <td data-number>{row["opportunity"]:.1f}</td>
      <td data-number><strong>{row["decision_score"]:.1f}</strong></td>
      <td data-number>#{row["rank_range_40_50_60"][0]}–#{row["rank_range_40_50_60"][1]}</td>
      <td>{land_badge(row)}</td>
    </tr>'''
    for row in rows
)

queue = [
    ("เอกมัย-ใต้", "Central leader", "Core-fit 86.3 · land p91.2"),
    ("วังหิน-ใต้", "Opportunity-led", "Opportunity 90.7 · land p53.8"),
    ("สัมมากร", "ใกล้ proxy ที่สุด", "Similarity 98.6 · land p46.6"),
    ("พระราม 3-ตะวันออก", "อันดับนิ่ง", "ช่วง #4–6 · ต้องพิสูจน์ economics"),
]
queue_cards = "".join(
    f'<article><span>{index:02d}</span><h3>{esc(name)}</h3><strong>{esc(reason)}</strong><p>{esc(note)}</p></article>'
    for index, (name, reason, note) in enumerate(queue, 1)
)

proxy_section = f'''    <section class="section alt proxy-section" id="parc-fit" data-proxy-release="{esc(data["release_id"])}">
      <div class="container">
        <div class="section-head">
          <div class="eyebrow">PARC core-fit preview · 574 comparable locales</div>
          <h2>เทียบกับบริบทใกล้ PARC โดยไม่เอา PARC กลับเข้าฐานผู้สมัคร</h2>
          <p class="lead">ศรีเอี่ยมเป็น working host-locale proxy ที่ใกล้หมุด PARC ที่สุด 0.30 กม. ใช้ช่วยอ่านรูปแบบบริบท ไม่ใช่คะแนนตัวศูนย์ ไม่ใช่ catchment 26.3 ตร.กม. และไม่ใช่ measured trade area</p>
        </div>
        <div class="proxy-grid">
          <aside class="proxy-reference" aria-labelledby="proxy-reference-title">
            <span class="status-pill">Proxy · ไม่จัดอันดับ</span>
            <h3 id="proxy-reference-title">ศรีเอี่ยม</h3>
            <p>คำนวณ out-of-sample เทียบ CDF 745 ที่ตรึงไว้; locale นี้และ PARC contexts อีก 21 รายการไม่อยู่ในผู้สมัคร</p>
            <div class="proxy-score-grid">
              <div><span>Resident</span><strong>{scores["resident"]:.1f}</strong></div>
              <div><span>Routine breadth</span><strong>{scores["routine_breadth"]:.1f}</strong></div>
              <div><span>Accessible routine</span><strong>{scores["accessible_routine"]:.1f}</strong></div>
              <div><span>Activity</span><strong>{scores["activity"]:.1f}</strong></div>
              <div><span>Core opportunity</span><strong>{scores["fresh_core_opportunity"]:.1f}</strong></div>
            </div>
            <p class="proxy-limit"><strong>ยังไม่รองรับ:</strong> barrier access, competition pressure, low-supply, Balanced และ stability</p>
          </aside>
          <div class="proxy-method">
            <h3>อย่ารวม “คล้าย” กับ “น่าสนใจ” แบบซ่อนน้ำหนัก</h3>
            <div class="proxy-axis-grid">
              <div><span>แกน 1</span><strong>Similarity</strong><p>องค์ประกอบ Resident / Routine / Activity ใกล้ proxy แค่ไหน</p></div>
              <div><span>แกน 2</span><strong>Opportunity</strong><p>core demand signals แข็งแรงแค่ไหน ไม่บังคับว่าต้องเท่ากับ PARC</p></div>
            </div>
            <p>ลำดับเดียวด้านล่างใช้ harmonic mean 50/50 เพื่อจัดคิวเท่านั้น และแสดงช่วงอันดับเมื่อให้น้ำหนัก Similarity 40/50/60 เพื่อให้เห็นความไวของคำตอบ</p>
            <details class="proxy-audit"><summary>สูตรและ provenance</summary><code>Similarity = 100 − [.55|R−Rp| + .25|B−Bp| + .20|A−Ap|]</code><code>Opportunity = .55R + .25B + .20A</code><p>Fresh transform ที่กู้คืนได้ตรวจย้อนกลับกับ 16 แถวของ v3.3 แล้วตรงหลังปัดตามหน้าจอ แต่ proxy ยังไม่มี Access / Competition จึงห้ามใช้ preview แทน Balanced, Market หรือ Stability score</p></details>
          </div>
        </div>
        <div class="table-wrap fit-table-wrap">
          <table class="fit-table" data-core-fit-table>
            <caption>Top 10 PARC core-fit ก่อน route, site, competition และ economics gates</caption>
            <thead><tr><th>อันดับ</th><th>Locale</th><th>Similarity</th><th>Opportunity</th><th>คะแนนจัดคิว</th><th>ช่วงอันดับ</th><th>Land diagnostic</th></tr></thead>
            <tbody>{fit_rows}</tbody>
            <tfoot><tr class="benchmark-row"><th scope="row" colspan="2">ศรีเอี่ยม · host-locale proxy</th><td data-number>100.0</td><td data-number>{scores["fresh_core_opportunity"]:.1f}</td><td colspan="3">Reference เท่านั้น · ไม่จัดอันดับ</td></tr></tfoot>
          </table>
        </div>
        <p class="fit-caption">Similarity 100 หมายถึง profile เหมือน proxy ในสามมิติ ไม่ได้แปลว่าเป็นโอกาสดีที่สุด ส่วน land percentile เป็น diagnostic น้ำหนัก 0—ห้ามอ่านแทนราคาซื้อที่ดินหรือ feasibility</p>
        <div class="section-head compact">
          <div class="eyebrow">คิวพิสูจน์ต่อ</div>
          <h2>สี่ทำเลที่ควรเปิด route + site + competition + economics gate ก่อน</h2>
        </div>
        <div class="fit-queue">{queue_cards}</div>
        <p class="fit-caption">คิวนี้ตั้งใจครอบคลุม central leader, opportunity-led, closest analog และ stable high-land case ไม่ใช่ score band; ตลาดพลู-ใต้และราชเทวีอยู่ใน sensitivity union ส่วนคลองจั่นต้องปิดช่องว่าง land evidence</p>
        <aside class="fit-warning"><strong>ขอบเขตที่ยังไม่ใช่ PARC benchmark:</strong> working catchment PARC 26.3 ตร.กม. คนละหน่วยกับศรีเอี่ยม 1.81 ตร.กม. ต้อง regenerate ด้วย geometry rule เดียวกันก่อนใช้อนุมัติลงทุน</aside>
      </div>
    </section>

'''

source = replace_once(
    source,
    '    <section class="section" id="sensitivity">',
    proxy_section + '    <section class="section" id="sensitivity">',
    "PARC core-fit preview section",
)

source = replace_once(
    source,
    '<a href="#lenses">5 คำถาม</a><a href="#sensitivity">ลองน้ำหนัก</a>',
    '<a href="#lenses">5 คำถาม</a><a href="#parc-fit">PARC fit</a><a href="#sensitivity">ลองน้ำหนัก</a>',
    "navigation link",
)

source = replace_once(
    source,
    'data-interface-release="v3.4-board-decision-tool"',
    'data-interface-release="v3.5-parc-core-fit-preview" data-benchmark-release="parc-host-proxy-core-fit-preview-v0.1"',
    "release metadata",
)

source = replace_once(
    source,
    'Fresh Locale Screen · Board decision tool · 31 กรกฎาคม 2026',
    'Fresh Locale Screen · PARC core-fit preview · 1 สิงหาคม 2026',
    "hero release date",
)

source = replace_once(
    source,
    '<span>PARC Bangna · analytical release v3.3 · interface v3.4</span>',
    '<span>PARC Bangna · analytical release v3.3 · proxy preview v0.1 · interface v3.5</span>',
    "footer provenance",
)

# Correct the rank denominator without changing the 745-score-base wording.
rank_replacements = {
    '5 คำถามตัดสินใจ · 745 ทำเล': '5 คำถามตัดสินใจ · score base 745 · ranked lane 574',
    'สามคอลัมน์แรกเป็นอันดับเทียบ 745': 'สามคอลัมน์แรกเป็นอันดับเทียบ 574',
    'อันดับฐาน /745': 'อันดับฐาน /574',
    'อันดับเทียบ 745 แสดงเฉพาะสูตรฐานที่ตรึงไว้': 'อันดับเทียบ 574 แสดงเฉพาะสูตรฐานที่ตรึงไว้',
    'คะแนน · อันดับเทียบ 745 ของแต่ละ preset': 'คะแนน · อันดับเทียบ 574 ของแต่ละ preset',
}
for old, new in rank_replacements.items():
    if old not in source:
        raise RuntimeError(f"rank denominator copy missing: {old}")
    source = source.replace(old, new)

old_gap = '''        <aside class="benchmark-gap" data-benchmark-status="unscored">
          <span class="status-pill">Benchmark gap</span>
          <div><h3>PARC Bangna ยังไม่มีคะแนนที่เทียบด้วยกติกาเดียวกัน</h3>
          <p>นี่ไม่ใช่คะแนน 0: PARC ถูกกันออกจาก 745 ทำเลเพื่อไม่คัดทับโครงการเดิม และ Locale Insight v2.3 ระบุว่ายังไม่มี approved percentile capsule. ต้องได้ reference geometry และ raw inputs ชุดเดียวกับ v2.3.1 แล้ว score แบบ out-of-sample เทียบ distribution 745 ที่ตรึงไว้—จากนั้นจึงปัก PARC เป็นเส้นอ้างอิงโดยไม่ให้อันดับ</p></div>
        </aside>'''
new_gap = '''        <aside class="benchmark-gap" data-benchmark-status="proxy-partial">
          <span class="status-pill">Proxy available</span>
          <div><h3>มี host-locale proxy แล้ว แต่ยังไม่มี exact PARC benchmark</h3>
          <p>ดูศรีเอี่ยมและ core-fit shortlist ด้านบนได้ แต่ proxy ยังไม่มี access/supply score จึงไม่เข้าร่วม slider A–J และห้ามใช้แทนคะแนน venue/catchment PARC Bangna</p></div>
        </aside>'''
source = replace_once(source, old_gap, new_gap, "benchmark status card")

source = replace_once(
    source,
    '— ยังไม่มี same-release score; ไม่ใส่เลขแทนข้อมูลที่ขาด',
    'Proxy ไม่เข้าร่วม slider: ยังไม่มี access / supply score ด้วยวิธีเดียวกัน',
    "live table proxy footer",
)

css = r'''
.proxy-section{scroll-margin-top:0;padding-top:clamp(3.25rem,5vw,4.75rem)}
.proxy-section .section-head{max-width:62rem}
.proxy-grid{display:grid;grid-template-columns:minmax(18rem,.82fr) minmax(0,1.18fr);gap:1rem;margin-bottom:1.2rem}
.proxy-reference,.proxy-method{padding:1.25rem;border:1px solid var(--line);border-radius:var(--radius);background:var(--card)}
.proxy-reference{border-color:var(--petal);background:color-mix(in srgb,var(--card) 89%,var(--petal))}
.proxy-reference .status-pill{display:inline-flex;background:var(--petal-deep);color:#fff}
.proxy-reference h3,.proxy-method h3{margin:.65rem 0 .3rem}
.proxy-reference>p,.proxy-method>p{color:var(--muted);font-size:.86rem}
.proxy-score-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.65rem;margin:1rem 0}
.proxy-score-grid>div{padding:.8rem;border:1px solid var(--line);border-radius:.65rem;background:var(--canvas)}
.proxy-score-grid span{display:block;color:var(--muted);font-size:.72rem}.proxy-score-grid strong{font-family:var(--display);font-size:1.55rem;color:var(--garden-deep)}
.proxy-limit{padding-top:.8rem;border-top:1px dashed var(--line)}
.proxy-axis-grid{display:grid;grid-template-columns:1fr 1fr;gap:.7rem;margin:.9rem 0}
.proxy-axis-grid>div{padding:.9rem;border-radius:.7rem;background:var(--canvas)}
.proxy-axis-grid span{display:block;color:var(--petal-deep);font-size:.7rem;text-transform:uppercase}.proxy-axis-grid strong{display:block;margin:.15rem 0}.proxy-axis-grid p{margin:0;color:var(--muted);font-size:.8rem}
.proxy-audit{margin-top:1rem;padding:.75rem;border:1px solid var(--line);border-radius:.65rem;background:var(--canvas)}
.proxy-audit summary{min-height:32px;cursor:pointer;font-weight:500}.proxy-audit code{display:block;margin:.45rem 0;white-space:normal;color:var(--garden-deep);font-size:.75rem}.proxy-audit p{color:var(--muted);font-size:.76rem}
.fit-table-wrap{margin-top:1rem}.fit-table th small{color:var(--muted);font-weight:400}.fit-table a{color:var(--petal-deep);text-underline-offset:.18em}
.fit-diagnostic{display:inline-flex;align-items:center;min-height:1.7rem;padding:.15rem .5rem;border-radius:999px;font-size:.72rem;font-weight:500}
.fit-diagnostic.lower{background:var(--garden-soft);color:var(--garden-deep)}.fit-diagnostic.watch{background:#f5e9cf;color:#714710}.fit-diagnostic.high{background:var(--petal-soft);color:#7a2048}.fit-diagnostic.missing{background:var(--canvas);color:var(--muted);border:1px solid var(--line)}
html[data-theme="dark"] .fit-diagnostic.watch{background:#493a20;color:#f1ce87}html[data-theme="dark"] .fit-diagnostic.high{background:#4b2636;color:#f4bdd5}
html[data-theme="dark"] .proxy-reference .status-pill{background:#7a2048;color:#fff}
.fit-caption{margin:.65rem 0 1.5rem;color:var(--muted);font-size:.76rem}.section-head.compact{margin-top:1.5rem}.section-head.compact h2{font-size:clamp(1.45rem,2.4vw,2rem)}
.fit-queue{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.75rem}.fit-queue article{position:relative;padding:1rem;border:1px solid var(--line);border-radius:var(--radius);background:var(--card)}
.fit-queue article>span{position:absolute;right:.8rem;top:.65rem;color:var(--petal-deep);font-family:var(--display);font-size:1.2rem}.fit-queue h3{margin:0 2rem .4rem 0}.fit-queue strong{font-size:.8rem;color:var(--garden-deep)}.fit-queue p{margin:.35rem 0 0;color:var(--muted);font-size:.78rem}
.fit-warning{margin-top:1rem;padding:.85rem 1rem;border-left:4px solid var(--amber);background:color-mix(in srgb,var(--card) 88%,var(--amber));color:var(--muted);font-size:.82rem}.fit-warning strong{color:var(--ink)}
'''
source = replace_once(source, '@media(max-width:900px){', css + '\n@media(max-width:900px){', "v3.5 styles")
source = replace_once(
    source,
    '  .decision-bar{grid-template-columns:1fr}.decision-view-grid{grid-template-columns:1fr}.market-view{grid-column:auto}.pattern-grid{grid-template-columns:repeat(2,1fr)}',
    '  .decision-bar{grid-template-columns:1fr}.decision-view-grid{grid-template-columns:1fr}.market-view{grid-column:auto}.pattern-grid{grid-template-columns:repeat(2,1fr)}\n  .proxy-grid{grid-template-columns:1fr}.fit-queue{grid-template-columns:repeat(2,minmax(0,1fr))}',
    "v3.5 tablet layout",
)
source = replace_once(
    source,
    '  .decision-steps,.decision-view-grid,.market-readings,.pattern-grid,.lens-grid,.diagnostic-grid,.reserve-grid,.formula-audit ul{grid-template-columns:1fr}.market-view{grid-column:auto}.signal-row{grid-template-columns:repeat(2,1fr)}',
    '  .decision-steps,.decision-view-grid,.market-readings,.pattern-grid,.lens-grid,.diagnostic-grid,.reserve-grid,.formula-audit ul{grid-template-columns:1fr}.market-view{grid-column:auto}.signal-row{grid-template-columns:repeat(2,1fr)}\n  .proxy-score-grid,.proxy-axis-grid,.fit-queue{grid-template-columns:1fr}',
    "v3.5 mobile layout",
)

embedded = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
source = replace_once(
    source,
    '</body>',
    f'  <script type="application/json" id="parc-core-fit-data">{embedded}</script>\n</body>',
    "embedded proxy data",
)

OUTPUT.write_text(source, encoding="utf-8")
INDEX.write_text(source, encoding="utf-8")
print(f"wrote {OUTPUT.name} and index.html ({len(source):,} chars)")
