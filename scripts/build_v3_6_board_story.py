#!/usr/bin/env python3
"""Build v3.6 as an executive-first story without changing the v3.5 data.

The analytical v3.3 payload, the separately versioned Sri Iam reference data,
the 574-locale ranking, and the A-J simulator are preserved. This release only
changes information order, decision copy, and interface labels.
"""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "PARC_Bangna_Fresh_Locale_Screen_Board_Decision_Tool_v3.5_PARC_Core_Fit_Preview_2026-08-01.html"
DATA = ROOT / "analysis/parc-host-proxy-core-fit-preview-v0.1.json"
OUTPUT = ROOT / "PARC_Bangna_Fresh_Locale_Screen_Board_Decision_Tool_v3.6_Executive_Story_2026-08-03.html"
INDEX = ROOT / "index.html"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


def replace_count(text: str, old: str, new: str, expected: int, label: str) -> str:
    count = text.count(old)
    if count != expected:
        raise RuntimeError(f"{label}: expected {expected} matches, found {count}")
    return text.replace(old, new)


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def protect_json_script(text: str, script_id: str, token: str) -> tuple[str, str]:
    start_marker = f'<script type="application/json" id="{script_id}">'
    start = text.index(start_marker)
    end = text.index("</script>", start) + len("</script>")
    block = text[start:end]
    return text[:start] + token + text[end:], block


source = SOURCE.read_text(encoding="utf-8")
data = json.loads(DATA.read_text(encoding="utf-8"))
reference = data["reference"]
scores = reference["scores_out_of_sample_against_frozen_745"]
rows = data["top_10_core_fit_before_route_site_and_economics_gates"]

# Visible-copy replacements must never mutate either governed JSON payload.
source, frozen_report_data = protect_json_script(source, "report-data", "__V36_FROZEN_REPORT_DATA__")
source, frozen_reference_data = protect_json_script(source, "parc-core-fit-data", "__V36_FROZEN_REFERENCE_DATA__")

if len(rows) != 10 or len({row["locale_id"] for row in rows}) != 10:
    raise RuntimeError("v3.6 must retain ten unique ranked locales")


def locale_label(row: dict[str, object]) -> str:
    name = esc(row["locale_name_th"])
    ref = row.get("current_portfolio_ref")
    if ref:
        return f'<a href="#detail-{esc(ref)}">{name} <small>· อยู่ในพอร์ต {esc(ref)}</small></a>'
    return name


def land_badge(row: dict[str, object]) -> str:
    percentile = row.get("land_price_percentile")
    if percentile is None:
        return '<span class="fit-diagnostic missing">ยังไม่มีข้อมูล</span>'
    level = "high" if float(percentile) >= 80 else "watch" if float(percentile) >= 60 else "lower"
    return f'<span class="fit-diagnostic {level}">สูงกว่า {float(percentile):.0f}% ของย่านที่มีข้อมูล</span>'


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
    (
        "เอกมัย-ใต้",
        "ควรเริ่มตรวจเป็นลำดับแรก",
        "รูปแบบย่านคล้ายศรีเอี่ยมและสัญญาณพื้นฐานอยู่ในกลุ่มนำ แต่ราคาประเมินระดับย่านอยู่ในกลุ่มสูงมาก—ต้องเปิดตัวเลขความคุ้มค่าก่อนเรื่องอื่น",
    ),
    (
        "วังหิน-ใต้",
        "สัญญาณพื้นฐานของย่านสูงที่สุดใน 4 ทำเล",
        "ฐานคนอยู่และกิจวัตรเด่น ขณะที่ราคาประเมินระดับย่านต่ำกว่าเอกมัย—ควรเช็กทางเข้าออกและคู่แข่ง",
    ),
    (
        "สัมมากร",
        "รูปแบบย่านคล้ายศรีเอี่ยมที่สุด",
        "รูปแบบฐานคนและกิจวัตรคล้ายจุดอ้างอิงมากที่สุด และมีราคาประเมินระดับย่านต่ำสุดใน 4 ทำเล—แต่ถ้าให้น้ำหนักแต่ละปัจจัยต่างกัน อันดับจะเปลี่ยนมาก",
    ),
    (
        "พระราม 3-ตะวันออก",
        "ยังติดกลุ่มนำเมื่อเปลี่ยนน้ำหนัก",
        "ยังอยู่ช่วงอันดับ 4–6 เมื่อเปลี่ยนน้ำหนัก แต่ราคาประเมินระดับย่านอยู่ในกลุ่มสูง—จึงต้องตรวจความคุ้มค่าตั้งแต่ต้น",
    ),
]
queue_cards = "".join(
    f'<article><span>{index:02d}</span><h3>{esc(name)}</h3><strong>{esc(reason)}</strong><p>{esc(note)}</p></article>'
    for index, (name, reason, note) in enumerate(queue, 1)
)

decision_section = f'''    <section class="section alt proxy-section" id="parc-fit" data-proxy-release="{esc(data["release_id"])}">
      <div class="container">
        <div class="section-head decision-first-head">
          <div class="eyebrow">ผลคัดกรองรอบใหม่ · 574 ย่านที่เทียบเคียงกันได้</div>
          <h2>4 ทำเลที่ควรศึกษาความเป็นไปได้ต่อ</h2>
          <p class="lead">จาก 574 ย่าน รอบนี้เสนอ เอกมัย-ใต้ วังหิน-ใต้ สัมมากร และพระราม 3-ตะวันออก แต่ละทำเลติดกลุ่มนำด้วยเหตุผลต่างกัน และมีเรื่องที่ต้องตรวจไม่เหมือนกันก่อนตัดสินใจลงทุน</p>
        </div>
        <aside class="decision-boundary"><strong>คำตัดสินวันนี้:</strong> อนุมัติให้ทีมศึกษาความเป็นไปได้ของ 4 ทำเลนี้ โดยลงพื้นที่ ตรวจแปลง คู่แข่ง กำลังซื้อ และความคุ้มค่า ยังไม่ใช่อนุมัติซื้อที่ดินหรือเริ่มลงทุน</aside>
        <div class="fit-queue">{queue_cards}</div>

        <div class="proxy-grid decision-reference-grid">
          <aside class="proxy-reference" aria-labelledby="proxy-reference-title">
            <span class="status-pill">จุดอ้างอิงชั่วคราว · ไม่จัดอันดับ</span>
            <h3 id="proxy-reference-title">ศรีเอี่ยม</h3>
            <p>ยังไม่มีข้อมูลของ PARC Bangna ที่วัดด้วยขอบเขตเดียวกับย่านอื่น รอบนี้จึงใช้ศรีเอี่ยม—ย่านที่มีจุดอ้างอิงใกล้ PARC ที่สุด—เป็นจุดตั้งต้น ตัวเลขช่วยบอกว่าย่านไหนมีรูปแบบคล้ายกัน แต่ยังไม่บอกว่าเปิด PARC แล้วจะสำเร็จ</p>
            <div class="proxy-score-grid">
              <div><span>ฐานคนอยู่</span><strong>{scores["resident"]:.1f}</strong></div>
              <div><span>ความหลากหลายของกิจวัตร</span><strong>{scores["routine_breadth"]:.1f}</strong></div>
              <div><span>กิจวัตรที่เข้าถึงได้</span><strong>{scores["accessible_routine"]:.1f}</strong></div>
              <div><span>กิจกรรมนอกบ้าน</span><strong>{scores["activity"]:.1f}</strong></div>
              <div><span>สัญญาณพื้นฐานของย่าน</span><strong>{scores["fresh_core_opportunity"]:.1f}</strong></div>
            </div>
          </aside>
          <div class="proxy-method">
            <h3>คล้ายอย่างเดียวไม่พอ</h3>
            <div class="proxy-axis-grid">
              <div><span>มุมที่ 1</span><strong>รูปแบบย่านคล้ายศรีเอี่ยมแค่ไหน</strong><p>ดูฐานคนอยู่ กิจวัตร และกิจกรรมนอกบ้าน</p></div>
              <div><span>มุมที่ 2</span><strong>สัญญาณพื้นฐานของย่านแข็งแค่ไหน</strong><p>ไม่บังคับว่าทุกอย่างต้องเหมือนย่านรอบ PARC</p></div>
            </div>
            <p>เราดูทั้งความคล้ายของรูปแบบย่านและความแข็งแรงของสัญญาณพื้นฐานในสัดส่วนเท่ากัน เพื่อจัดลำดับการศึกษาเท่านั้น ไม่ใช่ลำดับการลงทุน</p>
            <details class="proxy-audit"><summary>ดูวิธีคำนวณและที่มาของข้อมูล</summary><code>ความคล้ายของรูปแบบย่าน = 100 − [.55|R−Rp| + .25|B−Bp| + .20|A−Ap|]</code><code>สัญญาณพื้นฐาน = .55R + .25B + .20A</code><p>สูตรนี้ใช้ฐานคะแนน 745 ทำเล และจัดอันดับเฉพาะ 574 ย่านที่เทียบเคียงกันได้ ศรีเอี่ยมอยู่นอกกลุ่มผู้สมัคร จึงไม่ทำให้อันดับของย่านอื่นขยับ</p></details>
          </div>
        </div>

        <div class="table-wrap fit-table-wrap">
          <table class="fit-table" data-core-fit-table>
            <caption>10 ย่านที่ได้คะแนนคัดกรองสูงสุด · 4 ทำเลแรกคือชุดที่เสนอให้ศึกษาต่อ</caption>
            <thead><tr><th>อันดับ</th><th>ทำเล</th><th>รูปแบบย่านคล้ายศรีเอี่ยม</th><th>สัญญาณพื้นฐาน</th><th>คะแนนคัดกรอง</th><th>อันดับเมื่อเปลี่ยนน้ำหนัก</th><th>ราคาประเมินระดับย่าน*</th></tr></thead>
            <tbody>{fit_rows}</tbody>
            <tfoot><tr class="benchmark-row"><th scope="row" colspan="2">ศรีเอี่ยม · จุดอ้างอิงตั้งต้น</th><td data-number>—</td><td data-number>{scores["fresh_core_opportunity"]:.1f}</td><td colspan="3">ไม่ใช่ผู้สมัครและไม่จัดอันดับ</td></tr></tfoot>
          </table>
        </div>
        <p class="fit-caption">คะแนนความคล้ายใช้สามองค์ประกอบของย่าน ไม่ใช่ความเหมือนของตัวโครงการ ส่วนราคาประเมินระดับย่านมีไว้เตือนความเสี่ยง ไม่ได้ใช้คำนวณอันดับ และไม่ใช่ราคาซื้อแปลงจริง</p>
        <aside class="fit-warning"><strong>ข้อจำกัดสำคัญ:</strong> ขอบเขตที่เคยใช้ศึกษารอบ PARC Bangna ครอบคลุม 26.3 ตร.กม. แต่ศรีเอี่ยมมีขนาด 1.81 ตร.กม. จึงยังเทียบกันตรง ๆ ไม่ได้ เมื่อเก็บข้อมูล PARC ด้วยขอบเขตเดียวกันแล้ว จึงค่อยเปลี่ยนมาใช้คะแนนของ PARC โดยตรง</aside>
      </div>
    </section>

'''

# Release identity and sharing metadata.
meta_replacements = {
    'data-interface-release="v3.5-parc-core-fit-preview"': 'data-interface-release="v3.6-executive-story"',
    'PARC Bangna Board Decision Tool — ทดสอบน้ำหนักและจัดอันดับพอร์ต A–J สด พร้อมคู่แข่ง แผนที่ barrier และ audit trail.': 'เครื่องมือคัดทำเลสำหรับ PARC แห่งถัดไป — เริ่มจาก 4 ทำเลที่ควรลงพื้นที่ ตรวจแปลง คู่แข่ง และความคุ้มค่าก่อนตัดสินใจลงทุน',
    'PARC Bangna — Board Decision Tool': 'PARC แห่งถัดไป — 4 ทำเลที่ควรศึกษาต่อก่อน',
    'ขยับน้ำหนักเอง แล้วดูอันดับพอร์ต 10 ทำเล A–J เปลี่ยนสด พร้อมหลักฐานและข้อจำกัดที่ตรวจสอบได้': 'เริ่มจาก 4 ทำเลที่ควรศึกษาความเป็นไปได้ต่อ พร้อมเหตุผล ความเสี่ยง และขอบเขตที่ขออนุมัติ',
    'ขยับน้ำหนักเอง แล้วดูอันดับพอร์ต 10 ทำเล A–J เปลี่ยนสด': '4 ทำเลที่ควรศึกษาต่อสำหรับ PARC แห่งถัดไป',
}
for old, new in meta_replacements.items():
    if old not in source:
        raise RuntimeError(f"metadata copy missing: {old}")
    source = source.replace(old, new)

source = replace_once(
    source,
    '<a href="#lenses">5 คำถาม</a><a href="#parc-fit">PARC fit</a><a href="#sensitivity">ลองน้ำหนัก</a>\n        <a href="#portfolio">10 ทำเล</a>\n        <a href="#detail">เจาะรายทำเล</a>\n        <a href="#approval">ขออนุมัติ</a>',
    '<a href="#parc-fit">4 ทำเลที่เสนอ</a><a href="#lenses">4 + 1 คำถาม</a><a href="#sensitivity">พอร์ต A–J เดิม</a>\n        <a href="#portfolio">ที่มาพอร์ตเดิม</a>\n        <a href="#detail">หลักฐาน A–J</a>\n        <a href="#approval">ขออนุมัติ</a>',
    "navigation",
)

hero_replacements = {
    'Fresh Locale Screen · PARC core-fit preview · 1 สิงหาคม 2026': 'เครื่องมือคัดทำเลสำหรับ PARC แห่งถัดไป · 3 สิงหาคม 2026',
    '<h1>10 ทำเลนี้<br><span>น่าสนใจคนละแบบ</span></h1>': '<h1>ถ้าจะสร้าง PARC แห่งถัดไป<br><span>ควรเริ่มที่ไหน</span></h1>',
    'รอบนี้ยังไม่เลือกผู้ชนะ เรากำลังเลือก 10 ทำเลที่คุ้มลงพื้นที่และเปิดโจทย์เชิงพาณิชย์ต่อ—ก่อนแตะที่ดินหรือ capex': 'เราไม่ได้หาย่านที่หน้าตาเหมือน PARC แต่หาย่านที่ศูนย์ใกล้บ้านแบบ PARC มีโอกาสทำให้คนแวะซ้ำได้จริง ผลรอบนี้เสนอให้ศึกษาความเป็นไปได้ของ 4 ทำเลก่อน',
    '<a class="button secondary hero-primary" href="#portfolio">': '<a class="button secondary hero-primary" href="#parc-fit">',
    ' ดูพอร์ต A–J</a>': ' ดู 4 ทำเลที่เสนอ</a>',
    '<span>A–J = รหัส ไม่ใช่อันดับ</span>': '<span>คัดจาก 574 ย่านที่เทียบเคียงกันได้</span>',
    '<span>ทุกทำเลมีข้อที่ต้องพิสูจน์</span>': '<span>ศรีเอี่ยมเป็นย่านอ้างอิง ไม่ใช่คะแนน PARC</span>',
    '<span>คู่แข่ง = ทั้งแรงกดดันและหลักฐานว่ามีตลาด</span>': '<span>ขออนุมัติตรวจทำเล ยังไม่ซื้อที่ดิน</span>',
    '<dt>ทำเลที่เทียบ</dt><dd>745</dd>': '<dt>ฐานคะแนน</dt><dd>745</dd>',
    '<dt>ศูนย์ใน VLI</dt><dd>751</dd>': '<dt>ย่านที่จัดอันดับ</dt><dd>574</dd>',
    '<dt>คำถามตัดสินใจ</dt><dd>5</dd>': '<dt>ทำเลตรวจต่อ</dt><dd>4</dd>',
    '<dt>แบบทดสอบ</dt><dd>13</dd>': '<dt>ชุดน้ำหนัก A–J เดิม</dt><dd>13</dd>',
}
for old, new in hero_replacements.items():
    source = replace_once(source, old, new, f"hero copy: {old[:24]}")

old_decision = '''    <section class="section decision-section">
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
    </section>'''
new_decision = '''    <section class="section decision-section">
      <div class="container">
        <div class="decision-bar">
          <div>
            <div class="eyebrow" style="color:#f1b9d2">สิ่งที่ขออนุมัติรอบนี้</div>
            <h2>ศึกษาความเป็นไปได้ของ 4 ทำเลที่เสนอรอบนี้</h2>
            <p>เอกมัย-ใต้ · วังหิน-ใต้ · สัมมากร · พระราม 3-ตะวันออก—ลงพื้นที่ตรวจเส้นทางเข้าออก แปลงจริง คู่แข่ง กำลังซื้อ และความคุ้มค่าด้วยมาตรฐานเดียวกัน</p>
          </div>
          <a class="button primary" href="#approval" data-approval-cta data-candidate-locales="เอกมัย-ใต้,วังหิน-ใต้,สัมมากร,พระราม 3-ตะวันออก"><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M8 12l2.5 2.5L16 9"></path><circle cx="12" cy="12" r="9"></circle></svg> ดูขอบเขตที่ขออนุมัติ <span aria-hidden="true">↓</span></a>
        </div>
        <div class="decision-steps" aria-label="วิธีใช้เครื่องมือนี้">
          <span><b>1</b> ดู 4 ทำเลที่เสนอ</span>
          <span><b>2</b> อ่านเหตุผลและความเสี่ยง</span>
          <span><b>3</b> อนุมัติขอบเขตการศึกษา</span>
        </div>
      </div>
    </section>'''
source = replace_once(source, old_decision, new_decision, "single approval request")

# Remove the v3.5 analytical addendum from its buried position and reinsert the
# human decision version immediately after the approval bar.
proxy_start = source.index('    <section class="section alt proxy-section" id="parc-fit"')
proxy_end = source.index('    <section class="section" id="sensitivity">', proxy_start)
source = source[:proxy_start] + source[proxy_end:]
source = replace_once(
    source,
    '    <section class="section alt" id="lenses">',
    decision_section + '    <section class="section" id="lenses">',
    "executive decision placement",
)

# Put the interactive A-J assumption tool before the long evidence panels. It
# remains clearly labelled as the previous portfolio, so it cannot be mistaken
# for the current four-location approval request.
sensitivity_start = source.index('    <section class="section" id="sensitivity">')
sensitivity_end = source.index('    <section class="section alt" id="reserves">', sensitivity_start)
sensitivity_section = source[sensitivity_start:sensitivity_end]
source = source[:sensitivity_start] + source[sensitivity_end:]
source = replace_once(
    source,
    '    <section class="section alt" id="detail">',
    sensitivity_section + '    <section class="section alt" id="detail">',
    "live tool placement before long evidence",
)

# Humanize the five-question layer while retaining the technical audit trail.
lens_replacements = {
    '<div class="eyebrow">5 คำถามตัดสินใจ · score base 745 · ranked lane 574</div>': '<div class="eyebrow">4 คำถามสำหรับทำเลที่เสนอ + 1 แบบทดสอบพอร์ต A–J รอบเดิม</div>',
    'ไม่ต้องอ่าน 9 ตารางก่อนรู้ว่าควรถามอะไร': 'สี่คำถามที่ต้องตอบก่อนเลือกทำเล—และหนึ่งแบบทดสอบพอร์ตรอบเดิม',
    'ยุบสูตรเดิมเป็น 5 คำถามที่ Board ใช้ค้านสมมติฐานได้ ส่วนสูตรทั้ง 9 ยังอยู่ใน audit trail ด้านล่าง': 'สี่การ์ดแรกคือคำถามที่ต้องนำไปตรวจใน 4 ทำเลที่เสนอ รายชื่อใต้คำถามเป็นตัวอย่างย่านที่เด่นในฐานเดิม ไม่ใช่ข้อเสนอรอบนี้ ส่วนการ์ดสุดท้ายใช้ทบทวนเฉพาะพอร์ต A–J รอบเดิม',
    'มี resident base มากพอไหม': 'มีคนอยู่มากพอไหม',
    'ใช้ Resident index แยกจาก routine เพื่อไม่ให้กิจกรรมเมืองกลบฐานบ้าน': 'ดูฐานคนอยู่แยกจากกิจกรรมเมือง เพื่อไม่ให้ย่านที่คึกคักแต่ไม่มีฐานบ้านดูดีเกินจริง',
    'Accessible routine รวม routine breadth กับ activity proof เพื่ออ่านความถี่ของชีวิตประจำวัน': 'รวมความหลากหลายของกิจวัตรกับกิจกรรมนอกบ้าน เพื่อดูว่าคนมีเหตุให้กลับมาใช้พื้นที่เป็นประจำหรือไม่',
    '<div class="eyebrow">Barrier-aware access</div>': '<div class="eyebrow">การเข้าถึงเมื่อมีสิ่งกีดขวาง</div>',
    'Demand ยังถึงจริงเมื่อมีแม่น้ำและทางด่วนไหม': 'คนยังเดินทางมาถึงจริงไหม เมื่อมีแม่น้ำหรือทางด่วน',
    'ตัวเลขเป็น geometric screen ไม่ใช่ route time; ใช้ชี้ว่าต้องพิสูจน์จุดข้ามและทางขึ้น–ลงตรงไหน': 'ตัวเลขนี้ช่วยชี้ว่าต้องไปตรวจสะพาน จุดข้าม และทางขึ้นลงตรงไหน ยังไม่ใช่เวลาเดินทางจริง',
    'Supply บางคือช่องว่าง หรือ supply หนาคือหลักฐานว่ามีตลาด': 'คู่แข่งน้อยคือช่องว่าง หรือคู่แข่งมากคือหลักฐานว่าตลาดมีอยู่แล้ว',
    'อ่านได้สองทางและยังไม่มีทางใดพิสูจน์ demand: White-space ใช้หา headroom; Observed supply ใช้ตั้ง market-validation hypothesis': 'อ่านได้สองทาง: คู่แข่งน้อยอาจเป็นช่องว่าง หรืออาจแปลว่าตลาดยังไม่เกิด ส่วนคู่แข่งมากอาจยืนยันพฤติกรรมการใช้จ่าย แต่ยังต้องตรวจว่ามีช่องให้ PARC ชนะ',
    '<strong>ช่องว่าง supply</strong>': '<strong>มองหาช่องว่างในตลาด</strong>',
    '<strong>ตลาดมีของแล้ว</strong>': '<strong>มองหาตลาดที่มีพฤติกรรมอยู่แล้ว</strong>',
    'เมื่อขยับสมมติฐาน ใครยังอยู่ข้างบน': 'ถ้าขยับสมมติฐาน พอร์ต A–J รอบเดิมเปลี่ยนแค่ไหน',
    'ช่วงอันดับนี้มาจาก 13 preset เดิม; ใช้ slider ด้านล่างเพื่อทดสอบน้ำหนักของ Board เองในพอร์ต A–J': 'ผลด้านล่างใช้เฉพาะพอร์ต A–J รอบเดิม เพื่อให้บอร์ดลองน้ำหนักด้วยตัวเอง ไม่ใช่การทดสอบ 4 ทำเลที่เสนอวันนี้',
    'Audit trail: สูตรเดิมทั้ง 9': 'ดูสูตรเดิมทั้ง 9 แบบ',
}
for old, new in lens_replacements.items():
    source = replace_once(source, old, new, f"five-question copy: {old[:24]}")

source = replace_once(
    source,
    '<p class="lead">สี่การ์ดแรกคือคำถามที่ต้องนำไปตรวจใน 4 ทำเลที่เสนอ รายชื่อใต้คำถามเป็นตัวอย่างย่านที่เด่นในฐานเดิม ไม่ใช่ข้อเสนอรอบนี้ ส่วนการ์ดสุดท้ายใช้ทบทวนเฉพาะพอร์ต A–J รอบเดิม</p>',
    '<p class="lead">สี่การ์ดแรกคือคำถามที่ต้องนำไปตรวจใน 4 ทำเลที่เสนอ รายชื่อใต้คำถามเป็นตัวอย่างย่านที่เด่นในฐานเดิม ไม่ใช่ข้อเสนอรอบนี้ ส่วนการ์ดสุดท้ายใช้ทบทวนเฉพาะพอร์ต A–J รอบเดิม</p><aside class="lens-benchmark-note">หมายเหตุ: เรายังไม่มีคะแนนของ PARC Bangna ที่วัดด้วยขอบเขตเดียวกัน จึงไม่ใช้ PARC เป็นเส้นเทียบในสี่คำถามนี้</aside>',
    "single PARC benchmark note",
)

source = replace_count(
    source,
    '<p class="benchmark-slot"><strong>PARC benchmark</strong><span>รอคะแนนจาก release เดียวกัน</span></p>',
    '',
    5,
    "remove repeated PARC benchmark slots",
)

# Make it unmistakable that A-J is the previous portfolio and not this release's
# approval scope.
portfolio_replacements = {
    '<h2>10 ทำเลอยู่ตรงไหนของเมือง</h2>': '<h2>พอร์ต A–J รอบก่อนอยู่ตรงไหนของเมือง</h2>',
    'ขอบแขวงช่วยให้รู้ว่าอยู่ย่านไหน ส่วนแม่น้ำและทางด่วนช่วยชี้จุดที่ต้องเช็ก route จริงในรอบถัดไป': 'ขอบแขวงช่วยบอกตำแหน่งคร่าว ๆ ส่วนแม่น้ำและทางด่วนชี้จุดที่ต้องตรวจเส้นทางจริง หากหยิบทำเลจากพอร์ตเดิมกลับมาศึกษา',
    '<div class="eyebrow">พอร์ต 3 + 3 + 3 + 1 · A–J ไม่ใช่อันดับ</div>': '<div class="eyebrow">พอร์ตคัดกรองรอบก่อน · 3 + 3 + 3 + 1 · A–J ไม่ใช่อันดับ</div>',
    '<h2>10 ทำเลนี้ ถูกเลือกคนละเหตุผล</h2>': '<h2>A–J คือพอร์ตคัดกรองรอบก่อน ไม่ใช่คำขออนุมัติรอบนี้</h2>',
    'ตั้งใจให้พอร์ตมีทั้งตลาดที่ supply ยังบาง ตลาดที่มีคู่แข่งให้เข้าไปชนะ และทำเลที่ต้องพิสูจน์ผลของ barrier': 'เก็บพอร์ตนี้ไว้ให้บอร์ดลองเปลี่ยนน้ำหนักและย้อนดูหลักฐานเดิม มีทั้งย่านที่คู่แข่งยังบาง ย่านที่มีตลาดอยู่แล้ว และย่านที่ต้องตรวจผลของแม่น้ำหรือทางด่วน',
    '<strong>3 ย่านที่ supply ยังบาง</strong>': '<strong>3 ย่านที่คู่แข่งยังบาง</strong>',
    'ฐานบ้านเด่น และ supply ใกล้ยังบางกว่า': 'ฐานบ้านเด่น และคู่แข่งใกล้เคียงยังบางกว่า',
    '<strong>1 barrier test</strong>': '<strong>1 ทำเลทดสอบผลของทางด่วน</strong>',
    'ดูว่าทางด่วนสร้าง routine pocket จริงหรือไม่': 'ดูว่าทางด่วนทำให้เกิดพื้นที่ชีวิตประจำวันแยกออกมาจริงหรือไม่',
    '<span><b>1 · สร้าง candidate pool</b>รวม Top 20 จากสูตรทั้ง 9 และ Pareto fronts</span>': '<span><b>1 · รวมทำเลตั้งต้น</b>รวมย่านที่เด่นจากการมองข้อมูลทั้ง 9 แบบ</span>',
    '<span><b>2 · ลดความซ้ำ</b>ทบทวน host complex, catchment family และความซ้ำเชิงภูมิศาสตร์</span>': '<span><b>2 · ตัดความซ้ำ</b>ตัดย่านที่อยู่ในพื้นที่เดียวกันหรือมีบริบทซ้ำกันออก</span>',
    '<span><b>3 · ใช้ quota หลังคำนวณ</b>3 anchors + 3 white-space + 3 challengers + 1 barrier test; A–J ไม่ใช่อันดับ</span>': '<span><b>3 · เก็บตัวแทนให้ครบโจทย์</b>เลือก 3 ย่านเด่นหลายมุม + 3 ย่านที่คู่แข่งยังบาง + 3 ย่านที่มีผู้เล่นอยู่แล้ว + 1 ย่านทดสอบผลของทางด่วน</span>',
}
for old, new in portfolio_replacements.items():
    source = replace_once(source, old, new, f"portfolio framing: {old[:24]}")

source = replace_once(
    source,
    '<p class="lead">เก็บพอร์ตนี้ไว้ให้บอร์ดลองเปลี่ยนน้ำหนักและย้อนดูหลักฐานเดิม มีทั้งย่านที่คู่แข่งยังบาง ย่านที่มีตลาดอยู่แล้ว และย่านที่ต้องตรวจผลของแม่น้ำหรือทางด่วน</p>',
    '<p class="lead">เก็บพอร์ตนี้ไว้ให้บอร์ดลองเปลี่ยนน้ำหนักและย้อนดูหลักฐานเดิม มีทั้งย่านที่คู่แข่งยังบาง ย่านที่มีตลาดอยู่แล้ว และย่านที่ต้องตรวจผลของแม่น้ำหรือทางด่วน</p><aside class="portfolio-current-note">ใน 4 ทำเลที่ขออนุมัติวันนี้ มีวังหิน-ใต้ (B) และพระราม 3-ตะวันออก (J) อยู่ในพอร์ตเดิม ส่วนเอกมัย-ใต้และสัมมากรติดกลุ่มนำเมื่อคัดใหม่จากย่านเทียบเคียงทั้งหมด 574 แห่ง</aside>',
    "current four versus previous portfolio note",
)

# The simulator remains intact, but its visible copy should sound like a tool,
# not a model-validation memo.
simulator_replacements = {
    '<div class="eyebrow">เครื่องมือทดสอบสมมติฐาน</div>': '<div class="eyebrow">ทบทวนพอร์ตรอบเดิม</div>',
    '<h2>ขยับน้ำหนักเอง แล้วดู A–J เปลี่ยนอันดับสด</h2>': '<h2>ลองเปลี่ยนน้ำหนัก แล้วดูว่าพอร์ต A–J รอบเดิมเปลี่ยนอย่างไร</h2>',
    '<p class="lead">สูตรคำนวณจากข้อมูลที่ฝังอยู่แล้วและจัดอันดับใหม่เฉพาะพอร์ต 10 ทำเล ไม่ได้อ้างว่า recalibrate ทั้ง 745 ทำเลเมื่อใช้ค่าน้ำหนักกำหนดเอง</p>': '<p class="lead">เครื่องมือนี้จัดอันดับใหม่เฉพาะพอร์ต A–J รอบเดิม ให้บอร์ดลองสมมติฐานด้วยตัวเอง ไม่ได้คำนวณอันดับทั้ง 574 ย่านใหม่</p>',
    '<span class="status-pill">Proxy available</span>': '<span class="status-pill">พอร์ตคัดกรองรอบก่อน</span>',
    '<div><h3>มี host-locale proxy แล้ว แต่ยังไม่มี exact PARC benchmark</h3>\n          <p>ดูศรีเอี่ยมและ core-fit shortlist ด้านบนได้ แต่ proxy ยังไม่มี access/supply score จึงไม่เข้าร่วม slider A–J และห้ามใช้แทนคะแนน venue/catchment PARC Bangna</p></div>': '<div><h3>เครื่องมือนี้ใช้ข้อมูลพอร์ต A–J รอบเดิมเท่านั้น</h3>\n          <p>ใช้เพื่อทบทวนว่าสมมติฐานเดิมทำให้อันดับภายในพอร์ตเปลี่ยนอย่างไร ไม่ใช่การทดสอบ 4 ทำเลที่เสนอวันนี้</p></div>',
    'เริ่มจาก preset ที่ตรวจไว้แล้ว': 'เริ่มจากชุดน้ำหนักที่ตรวจไว้แล้ว',
    'กำหนดเองจาก slider': 'ปรับเอง',
    'น้ำหนักที่ใช้จริงจะ normalize รวมเป็น 100%': 'ระบบปรับให้น้ำหนักรวมเป็น 100% อัตโนมัติ',
    'Barrier-aware access': 'การเข้าถึงเมื่อมีสิ่งกีดขวาง',
    'สมมติฐานการข้าม barrier': 'สมมติฐานการข้ามแม่น้ำและทางด่วน',
    'สมมติฐาน supply ที่ไม่ทราบขนาด': 'สมมติฐานเมื่อไม่ทราบขนาดคู่แข่ง',
    'ตีความ supply อย่างไร': 'ตีความคู่แข่งอย่างไร',
    'ช่องว่าง supply': 'คู่แข่งยังบาง',
    'ตลาดมี supply แล้ว': 'ตลาดมีคู่แข่งอยู่แล้ว',
    'โหมด “ตลาดมีคู่แข่งอยู่แล้ว” ใช้ competition pressure เป็น market-validation hypothesis เท่านั้น ไม่ใช่ proof ของ demand, spend หรือ performance': 'การมีคู่แข่งอาจบอกว่าตลาดมีอยู่แล้ว แต่ยังไม่ยืนยันกำลังซื้อ ยอดใช้จ่าย หรือผลประกอบการ',
    '<th>คะแนนสด</th><th>ขยับจากฐาน A–J</th><th>อันดับฐาน /574</th><th>บทบาท</th>': '<th>คะแนนตามน้ำหนักนี้</th><th>เปลี่ยนจากสูตรฐาน</th><th>อันดับจากสูตรเดิม /574</th><th>เหตุผลที่อยู่ในพอร์ต</th>',
    'อันดับสดภายในพอร์ต A–J; อันดับเทียบ 574 แสดงเฉพาะสูตรฐานที่ตรึงไว้': 'อันดับสดภายในพอร์ตทดลอง A–J เท่านั้น; ไม่ใช่อันดับของ 4 ทำเลที่เสนออนุมัติวันนี้',
    'Proxy ไม่เข้าร่วม slider: ยังไม่มี access / supply score ด้วยวิธีเดียวกัน': 'ศรีเอี่ยมไม่เข้าร่วม เพราะยังไม่มีคะแนนการเข้าถึงและคู่แข่งด้วยวิธีเดียวกัน',
    'Audit trail: เปิดดูผล 13 preset × 10 ทำเลที่คำนวณไว้ล่วงหน้า': 'เปิดดูผล 13 ชุดน้ำหนัก × 10 ทำเลที่คำนวณไว้ล่วงหน้า',
    '<h2>6 ทำเลสำรอง ไม่ใช่อันดับ 11–16</h2>': '<h2>6 ทำเลสำรองของพอร์ตเดิม ไม่ใช่อันดับ 11–16</h2>',
    'ใช้แทนเมื่อ A–J ไม่ผ่าน gate โดยเลือกตัวที่ตอบโจทย์ pattern เดียวกัน และไม่ซ้ำ host complex หรือ catchment family': 'ใช้แทนเมื่อทำเลในพอร์ต A–J ไม่ผ่านการตรวจ โดยเลือกทำเลที่ตอบโจทย์ใกล้เคียงกันและไม่ซ้ำพื้นที่ลูกค้ากลุ่มเดิม',
    'กลับไปเครื่องมือทดสอบสมมติฐาน': 'กลับไปทบทวนพอร์ตรอบเดิม',
}
for old, new in simulator_replacements.items():
    if old not in source:
        raise RuntimeError(f"simulator copy missing: {old}")
    source = source.replace(old, new)

# Keep role labels natural both in the initial table and after live recalculation.
role_replacements = {
    'Anchor เด่นหลายมุม': 'เด่นหลายมุม',
    'White-space builder': 'คู่แข่งยังบาง',
    'Observed-supply challenger': 'ตลาดมีคู่แข่ง',
    'Barrier experiment': 'ทดสอบผลของทางด่วน',
}
for old, new in role_replacements.items():
    source = source.replace(old, new)

evidence_copy_replacements = {
    '<div class="eyebrow">เทียบ A–J ด้วย 5 คำถาม</div>': '<div class="eyebrow">เทียบ A–J ด้วย 4 มุมคัดกรอง + 1 แบบทดสอบน้ำหนัก</div>',
    'เด่นหลายมุม ใช้เป็นตัวเทียบของรอบศึกษาต่อ': 'เด่นหลายมุม ใช้เป็นตัวเทียบเมื่อลองเปลี่ยนสมมติฐานของพอร์ตเดิม',
    'ฐานคนอยู่แข็งและเด่นหลายมุม แม้มีศูนย์ใหญ่ใกล้ ๆ โจทย์คือทำ PARC ให้แวะง่ายและสงบกว่า mega mall': 'ฐานคนอยู่แข็งและเด่นหลายมุม แม้มีศูนย์ใหญ่ใกล้ ๆ โจทย์คือทำ PARC ให้แวะง่ายและสงบกว่าห้างใหญ่',
    'ย่านนี้มีทั้ง routine และสัญญาณการใช้งานจริง แม้คู่แข่งแน่น โอกาสอยู่ที่ tenant mix และประสบการณ์ที่ต่าง ไม่ใช่จำนวนร้าน': 'ย่านนี้มีทั้งกิจวัตรและสัญญาณการใช้งานจริง แม้คู่แข่งแน่น โอกาสอยู่ที่ส่วนผสมร้านค้าและประสบการณ์ที่ต่าง ไม่ใช่จำนวนร้าน',
    'ฐานบ้านแข็งและ supply ใกล้ยังบาง แต่ต้องเช็กด้วย route จริงว่าทางด่วนแบ่ง catchment หรือเป็นเพียงเส้นบนแผนที่': 'ฐานบ้านแข็งและคู่แข่งใกล้เคียงยังบาง แต่ต้องตรวจเส้นทางจริงว่าทางด่วนแบ่งพื้นที่ลูกค้า หรือเป็นเพียงเส้นบนแผนที่',
    'ฐานย่านแข็งและถูก barrier กั้นน้อย แต่มีร้านที่ตอบโจทย์ประจำวันอยู่แล้ว ต้องหา service gap ที่ยังไม่มีคนทำ': 'ฐานย่านแข็งและถูกสิ่งกีดขวางน้อย แต่มีร้านที่ตอบโจทย์ประจำวันอยู่แล้ว ต้องหาบริการที่ยังไม่มีใครทำ',
    'ฐานบ้านน่าสนใจ ขณะที่คู่แข่งใกล้ส่วนใหญ่ยังเป็น small format ก่อนเดินหน้าต้องเช็กกำลังซื้อและทางเข้า–ออกแปลง': 'ฐานบ้านน่าสนใจ ขณะที่คู่แข่งใกล้ส่วนใหญ่ยังเป็นศูนย์ขนาดเล็ก ก่อนเดินหน้าต้องเช็กกำลังซื้อและทางเข้าออกแปลง',
    'ฐานบ้านน่าสนใจ แต่สัญญาณการใช้งานจริงยังบาง เหมาะทดสอบ compact format ก่อนคิด full PARC': 'ฐานบ้านน่าสนใจ แต่สัญญาณการใช้งานจริงยังบาง ควรเริ่มทดสอบขนาดเล็กก่อนคิดโครงการ PARC เต็มรูปแบบ',
    'ฐานคนอยู่และ routine เด่น แต่จุดอ้างอิงห่าง Riverside Plaza เพียง 0.03 กม. ต้องเช็กว่าเหมาะกับ repositioning หรือ partnership มากกว่าสร้างใหม่หรือไม่': 'ฐานคนอยู่และกิจวัตรเด่น แต่จุดอ้างอิงห่าง Riverside Plaza เพียง 0.03 กม. ต้องเช็กว่าควรปรับตำแหน่งโครงการเดิมหรือร่วมมือกับเจ้าของพื้นที่ มากกว่าสร้างใหม่หรือไม่',
    'ฐานคนอยู่และ routine เด่น แม้สูตรรวมอยู่ #15 โอกาสมีต่อเมื่อเจอช่องที่ KINGSQUARE, Terminal 21 หรือ wholesale ยังไม่ตอบ': 'ฐานคนอยู่และกิจวัตรเด่น แม้สูตรรวมอยู่ #15 โอกาสมีต่อเมื่อพบความต้องการที่ KINGSQUARE, Terminal 21 หรือตลาดค้าส่งยังไม่ตอบ',
    'ย่านมีศูนย์เดิมหนาแน่นและ routine เด่น ต้องหา mission หรือหมวดร้านที่ยังขาดจริง—ไม่ทำ generic mall': 'ย่านมีศูนย์เดิมหนาแน่นและกิจวัตรเด่น ต้องหาเหตุผลการมาใช้บริการหรือหมวดร้านที่ยังขาดจริง—ไม่ทำห้างทั่วไปเพิ่มอีกแห่ง',
    'Routine และ activity เด่น แต่ screening พบ demand 38.3% อยู่คนละฝั่งทางด่วน ต้องเช็ก route จริงว่ากลายเป็น catchment แยกหรือไม่': 'กิจวัตรและกิจกรรมนอกบ้านเด่น แต่การคัดกรองพบฐานความต้องการ 38.3% อยู่คนละฝั่งทางด่วน ต้องตรวจเส้นทางจริงว่ากลายเป็นพื้นที่ลูกค้าคนละกลุ่มหรือไม่',
    '<h2>เห็นเหตุผลที่เด่น โดยไม่ต้องกวาดตา 9 คอลัมน์</h2>': '<h2>ดูเหตุผลหลักของพอร์ต A–J ได้ในตารางเดียว</h2>',
    'สามคอลัมน์แรกเป็นอันดับเทียบ 574; Market position เก็บการอ่านสองทางไว้ในช่องเดียว; Stability คือช่วงอันดับ Balanced เมื่อผ่าน 13 preset': 'ตารางนี้สรุปฐานคนอยู่ กิจวัตร การเข้าถึง ตำแหน่งในตลาด และความนิ่งของอันดับ ส่วนรายละเอียดสูตรอยู่ในหัวข้อวิธีคำนวณ',
    '5 decision views ของ A–J — ตัวอักษรเป็นรหัส ไม่ใช่อันดับ': '5 มุมมองของพอร์ต A–J — ตัวอักษรเป็นรหัส ไม่ใช่อันดับ',
    '— รอ same-release score; ไม่ใส่อันดับ': '— ยังไม่มีคะแนนที่คำนวณด้วยวิธีเดียวกัน จึงไม่ใส่อันดับ',
    'ค่าน้ำหนักดิบ': 'น้ำหนักที่ตั้ง',
    'ใช้จริงรวม 100.00%': 'ระบบปรับให้รวม 100%',
    '</b> คะแนนรวม</span>': '</b> อันดับจากสูตรเดิม /574</span>',
    'คะแนนรวมอยู่ช่วง': 'อันดับจากสูตรเดิมอยู่ช่วง',
    ' · คะแนนรวม #': ' · อันดับจากสูตรเดิม #',
    'ฐาน 40/25/20/15': 'สูตรตั้งต้น 40/25/20/15',
    'resident −5pp': 'ลดน้ำหนักฐานคนอยู่ 5 จุด',
    'resident +5pp': 'เพิ่มน้ำหนักฐานคนอยู่ 5 จุด',
    'routine −5pp': 'ลดน้ำหนักกิจวัตร 5 จุด',
    'routine +5pp': 'เพิ่มน้ำหนักกิจวัตร 5 จุด',
    'access −5pp': 'ลดน้ำหนักการเข้าถึง 5 จุด',
    'access +5pp': 'เพิ่มน้ำหนักการเข้าถึง 5 จุด',
    'low-supply signal −5pp': 'ลดน้ำหนักสัญญาณคู่แข่งยังบาง 5 จุด',
    'low-supply signal +5pp': 'เพิ่มน้ำหนักสัญญาณคู่แข่งยังบาง 5 จุด',
    'VLI unknown NLA=P75 + radius 3.33 km + cluster extra 50%': 'เผื่อคู่แข่งที่ไม่รู้ขนาดให้ใหญ่และครอบคลุมไกลขึ้น',
    'VLI unknown NLA=P25 + radius 2.50 km + cluster extra 0%': 'เผื่อคู่แข่งที่ไม่รู้ขนาดให้เล็กและครอบคลุมใกล้ลง',
    'river 40% + expressway 10% friction': 'สมมติว่าข้ามแม่น้ำและทางด่วนได้ง่ายขึ้น',
    'river 75% + expressway 35% friction': 'สมมติว่าแม่น้ำและทางด่วนกั้นมากขึ้น',
}
for old, new in evidence_copy_replacements.items():
    if old not in source:
        raise RuntimeError(f"evidence copy missing: {old}")
    source = source.replace(old, new)

# Replace the old A-J approval section with the single four-location request.
approval_start = source.index('    <section class="section approval" id="approval">')
approval_end = source.index('    <section class="section sources" id="sources">', approval_start)
approval = '''    <section class="section approval" id="approval">
      <div class="container approval-grid">
        <div>
          <div class="eyebrow" style="color:#f1b9d2">รอบศึกษาที่ขออนุมัติ</div>
          <h2>ศึกษาความเป็นไปได้ 4 ทำเล ก่อนเลือกแปลงหรือลงทุน</h2>
          <p class="lead">ตรวจเอกมัย-ใต้ วังหิน-ใต้ สัมมากร และพระราม 3-ตะวันออกด้วยมาตรฐานเดียวกัน เพื่อให้รู้ว่าควรไปต่อ เปลี่ยนโจทย์ หรือหยุด</p>
          <ol class="approval-list">
            <li>ยืนยันตำแหน่งและแปลงที่มีโอกาสพัฒนาได้จริง</li>
            <li>ตรวจทางเข้าออก สะพาน จุดข้าม และทางขึ้นลงในเวลาที่คนใช้งานจริง</li>
            <li>วัดพื้นที่ลูกค้าจากการเดินทาง 3 รูปแบบ × 3 ช่วงเวลา</li>
            <li>ตรวจคู่แข่ง พื้นที่ลูกค้าที่ซ้อนกัน และช่องที่ PARC อาจชนะได้</li>
            <li>หาโอกาสด้านร้านค้า บริการ และกิจวัตรที่ทำให้คนแวะซ้ำ</li>
            <li>เช็กกำลังซื้อ ขนาดโครงการ ที่จอดรถ และความคุ้มค่าเบื้องต้น</li>
          </ol>
        </div>
        <aside class="approval-card">
          <div class="eyebrow">สิ่งที่บอร์ดจะได้ใช้ตัดสินใจ</div>
          <p class="scope">เอกมัย-ใต้ · วังหิน-ใต้ · สัมมากร · พระราม 3-ตะวันออก</p>
          <ul>
            <li>ข้อสรุปรายทำเล: ไปต่อ / เปลี่ยนโจทย์ / หยุด พร้อมหลักฐานรองรับ</li>
            <li>ภาพเปรียบเทียบเส้นทาง แปลง คู่แข่ง และความคุ้มค่าด้วยมาตรฐานเดียวกัน</li>
            <li>เจ้าของงาน: ทีมกลยุทธ์ / ทีมพัฒนาโครงการ</li>
          </ul>
          <a class="button" href="#sources">ดูวิธีวิเคราะห์และข้อจำกัด</a>
          <p class="approval-guardrail">การอนุมัติครั้งนี้ครอบคลุมเฉพาะการศึกษาต่อ ยังไม่รวมการซื้อที่ดิน อนุมัติงบลงทุน หรือข้อสรุปว่าทำเลใดพัฒนา PARC ได้</p>
        </aside>
      </div>
    </section>

'''
source = source[:approval_start] + approval + source[approval_end:]

source = replace_once(
    source,
    '<span>PARC Bangna · analytical release v3.3 · proxy preview v0.1 · interface v3.5</span>',
    '<span>PARC Bangna · analytical release v3.3 · reference analysis v0.1 · interface v3.6</span>',
    "footer release identity",
)
source = replace_once(
    source,
    '<span>ใช้เพื่อเลือกโจทย์ศึกษาต่อ · ยังไม่ใช่คำตัดสินลงทุน</span>',
    '<span>ใช้เลือก 4 ทำเลไปศึกษาความเป็นไปได้ต่อ · ยังไม่ใช่คำตัดสินลงทุน</span>',
    "footer purpose",
)

# These replacements affect dynamic status text as well as the initial HTML.
dynamic_replacements = {
    'ตีความ supply เป็น market-validation hypothesis': 'มองคู่แข่งเป็นสัญญาณว่าตลาดอาจมีอยู่แล้ว',
    'ตีความ supply บางเป็นช่องว่าง': 'มองคู่แข่งน้อยเป็นช่องว่าง',
}
for old, new in dynamic_replacements.items():
    source = source.replace(old, new)

# Final language pass for every visible decision surface. Keep formulas and
# source-system names in the closed audit trail, but do not make executives
# translate model shorthand while reading the story or operating the tool.
visible_language_replacements = {
    'aria-label="เปลี่ยน theme"': 'aria-label="เปลี่ยนโทนสี"',
    '<span>Light</span>': '<span>สว่าง</span>',
    'themeLabel.textContent = theme === "dark" ? "Dark" : "Light";': 'themeLabel.textContent = theme === "dark" ? "มืด" : "สว่าง";',
    'Top 10 opportunity portfolio': 'พอร์ตทดลอง A–J รอบก่อน',
    'reference IDs ไม่ใช่อันดับ': 'ตัวอักษรอ้างอิง ไม่ใช่อันดับ',
    '<strong>Fresh baseline</strong>': '<strong>สูตรคัดกรองตั้งต้น</strong>',
    '<strong>Resident</strong>': '<strong>ฐานคนอยู่</strong>',
    '<strong>Accessible routine</strong>': '<strong>กิจวัตรที่เข้าถึงได้</strong>',
    '<strong>Activity proof</strong>': '<strong>กิจกรรมนอกบ้าน</strong>',
    '<strong>Demand + routine</strong>': '<strong>ฐานความต้องการและกิจวัตร</strong>',
    '<strong>Barrier-resilient demand</strong>': '<strong>ฐานความต้องการที่ผ่านสิ่งกีดขวาง</strong>',
    '<strong>Balanced full model</strong>': '<strong>สูตรรวม</strong>',
    'Supply ยังบาง': 'คู่แข่งยังบาง',
    'Supply ใกล้ยังบาง': 'คู่แข่งใกล้เคียงยังบาง',
    'supply ต่ำเพราะมี barrier?': 'คู่แข่งน้อยเพราะมีสิ่งกีดขวางหรือไม่',
    'Barrier test': 'ทดสอบผลของทางด่วน',
    'มีศูนย์เดิมหลายราย ต้องเช็กทั้ง demand และช่องที่ PARC ชนะได้': 'มีศูนย์เดิมหลายราย ต้องเช็กทั้งความต้องการและช่องที่ PARC ชนะได้',
    '<th>2 · Routine</th>': '<th>2 · กิจวัตร</th>',
    '<th>3 · Barrier-resilient</th>': '<th>3 · ผ่านสิ่งกีดขวาง</th>',
    '<th>4 · Market position</th>': '<th>4 · ตำแหน่งในตลาด</th>',
    '<th>5 · Stability</th>': '<th>5 · ความนิ่งของอันดับ</th>',
    ' Resident</span>': ' ฐานคนอยู่</span>',
    ' Routine</span>': ' กิจวัตร</span>',
    '<small>Gap ': '<small>ช่องว่าง ',
    '<small>Observed ': '<small>มีตลาดแล้ว ',
    '>Gap<': '>ช่องว่าง<',
    '>Observed<': '>มีตลาดแล้ว<',
    'PARC Bangna · reference': 'PARC Bangna · จุดอ้างอิง',
    'ฐาน 55% river / 20% expressway': 'สูตรฐาน: แม่น้ำ 55% / ทางด่วน 20%',
    'ฐาน: subtype median': 'สูตรฐาน: ใช้ค่ากลางของประเภท',
    'P75 + radius 3.33 กม.': 'เผื่อขนาดใหญ่ขึ้น · รัศมี 3.33 กม.',
    'P25 + radius 2.50 กม.': 'เผื่อขนาดเล็กลง · รัศมี 2.50 กม.',
    'คะแนน · อันดับเทียบ 574 ของแต่ละ preset': 'คะแนนและอันดับจากชุดน้ำหนักทั้ง 13 แบบ',
    '<th>Preset</th>': '<th>ชุดน้ำหนัก</th>',
    'Basemap ช่วยให้เห็นถนนและย่านจริง': 'แผนที่พื้นฐานช่วยให้เห็นถนนและย่านจริง',
    'กำลังเปิด basemap': 'กำลังเปิดแผนที่พื้นฐาน',
    'คู่แข่ง · ขนาดจุด = impact percentile': 'คู่แข่ง · ขนาดจุด = ระดับผลกระทบ',
    'ไม่ทราบขนาด ≠ ศูนย์: โมเดลใช้ค่ากลางของ subtype · จุดใหญ่แปลว่ามี impact สูงกว่า': 'ไม่ทราบขนาดไม่ได้แปลว่าขนาดเป็นศูนย์: ระบบใช้ค่ากลางของประเภท · จุดใหญ่แปลว่ามีผลกระทบสูงกว่า',
    'เทียบกับ 745 locales': 'เทียบกับฐาน 745 ทำเล',
    'Demand · spend · ยอดขายจริง': 'ความต้องการ · กำลังซื้อ · ยอดขายจริง',
    'Resident base': 'ฐานคนอยู่',
    'Routine ที่เข้าถึงได้': 'กิจวัตรที่เข้าถึงได้',
    '<span>Activity</span>': '<span>กิจกรรมนอกบ้าน</span>',
    'Access หลังคิด barrier': 'การเข้าถึงหลังคิดสิ่งกีดขวาง',
    'Demand คนละฝั่งแม่น้ำ': 'ฐานความต้องการอีกฝั่งแม่น้ำ',
    'Demand คนละฝั่งทางด่วน': 'ฐานความต้องการอีกฝั่งทางด่วน',
    'Access ค่ากลาง': 'คะแนนการเข้าถึงค่ากลาง',
    'Venue Locale Insight competitor evidence —': 'หลักฐานคู่แข่งจาก Venue Locale Insight —',
    '<th>Venue</th><th>Subtype</th><th>Distance</th><th>Size evidence</th><th>Impact size</th><th>Precinct</th>': '<th>สถานที่</th><th>ประเภท</th><th>ระยะห่าง</th><th>หลักฐานขนาด</th><th>ขนาดผลกระทบ</th><th>กลุ่มพื้นที่</th>',
    'ไม่ทราบ; model ใช้ subtype median': 'ไม่ทราบ; ระบบใช้ค่ากลางของประเภท',
    'ไม่ทราบ; model ใช้ median ของประเภท': 'ไม่ทราบ; ระบบใช้ค่ากลางของประเภท',
    'Supermarket anchored': 'ศูนย์ที่มีซูเปอร์มาร์เก็ตเป็นหลัก',
    'Hypermarket anchored': 'ศูนย์ที่มีไฮเปอร์มาร์เก็ตเป็นหลัก',
    'Entertainment anchored': 'ศูนย์ที่มีความบันเทิงเป็นหลัก',
    'Avenue / community format': 'ศูนย์ชุมชนหรือคอมมูนิตี้มอลล์',
    'Mega mall': 'ศูนย์การค้าขนาดใหญ่',
    'Regional mall': 'ศูนย์การค้าระดับภูมิภาค',
    '>Outlet<': '>เอาต์เล็ต<',
    'ดู sensitivity 13 แบบ': 'ดูผลเมื่อเปลี่ยนน้ำหนัก 13 แบบ',
    'ติด Top 10': 'ติด 10 อันดับแรก',
    'อยู่ Top 10 ของสูตรรวม': 'อยู่ใน 10 อันดับแรกของสูตรรวม',
    'อยู่นอก Top 10 ของสูตรรวม': 'อยู่นอก 10 อันดับแรกของสูตรรวม',
    'ลดน้ำหนัก routine 5 จุด': 'ลดน้ำหนักกิจวัตร 5 จุด',
    'เพิ่มน้ำหนัก routine 5 จุด': 'เพิ่มน้ำหนักกิจวัตร 5 จุด',
    'ลดน้ำหนัก access 5 จุด': 'ลดน้ำหนักการเข้าถึง 5 จุด',
    'เพิ่มน้ำหนัก access 5 จุด': 'เพิ่มน้ำหนักการเข้าถึง 5 จุด',
    'ลดน้ำหนักสัญญาณ supply บาง 5 จุด': 'ลดน้ำหนักสัญญาณคู่แข่งยังบาง 5 จุด',
    'เพิ่มน้ำหนักสัญญาณ supply บาง 5 จุด': 'เพิ่มน้ำหนักสัญญาณคู่แข่งยังบาง 5 จุด',
    'route จริง': 'เส้นทางจริง',
    'route graph': 'เครือข่ายเส้นทาง',
    'routing ชี้': 'การคำนวณเส้นทางชี้',
    'quick-in / quick-out': 'เข้าออกได้คล่อง',
    'audit แล้วไม่พบช่องว่างด้าน mission, service หรือ daypart': 'ตรวจแล้วไม่พบช่องว่างด้านเหตุผลที่มาใช้ บริการ หรือช่วงเวลา',
    'ทับ host complex เดิม': 'ทับพื้นที่โครงการเดิม',
    'ข้อได้เปรียบด้าน access': 'ข้อได้เปรียบด้านการเข้าถึง',
    'category gap เล็กเกินกว่าจะชดเชย supply pressure': 'ช่องว่างด้านหมวดร้านเล็กเกินกว่าจะชดเชยแรงกดดันจากคู่แข่ง',
    'retail ecosystem เดิมแข็ง': 'ระบบร้านค้าเดิมแข็ง',
    'ตลาดมี supply แต่ site ต้องชัด': 'ตลาดมีคู่แข่ง แต่ตำแหน่งและแปลงต้องชัด',
    'routine แข็งหลังแนวทางด่วน': 'กิจวัตรแข็งหลังแนวทางด่วน',
    'เจาะทีละทำเล: เห็นอะไร ต้องพิสูจน์อะไร': 'เจาะทีละทำเล: เห็นอะไร ต้องตรวจอะไร',
    'เด่นหลายมุม · ฐานลูกค้าและ routine แข็ง': 'เด่นหลายมุม · ฐานลูกค้าและกิจวัตรแข็ง',
    'เด่นหลายมุม · routine แข็งและสมดุล': 'เด่นหลายมุม · กิจวัตรแข็งและสมดุล',
    'หาก เครือข่ายเส้นทาง ชี้': 'หากเครือข่ายเส้นทางชี้',
    'ไม่ได้แยก catchment จริง': 'ไม่ได้แยกพื้นที่ลูกค้าจริง',
    'ของเดิมครอง routine หลักครบแล้ว': 'ของเดิมครองกิจวัตรหลักครบแล้ว',
    'spend และ daypart ไม่รองรับขนาด PARC': 'กำลังซื้อและช่วงเวลาการใช้งานไม่รองรับขนาด PARC',
    'การแข่งขันคือ supply pressure และ observed-supply market-validation hypothesis; ไม่ใช่ proof ของ demand, spend, footfall, occupancy, tenant health หรือ competitor weakness.': 'คะแนนการแข่งขันอ่านได้สองทาง: คู่แข่งน้อยอาจเป็นช่องว่าง และคู่แข่งมากอาจบอกว่าตลาดมีอยู่แล้ว แต่ยังไม่ยืนยันความต้องการ กำลังซื้อ จำนวนผู้ใช้ อัตราเช่า สุขภาพร้านค้า หรือจุดอ่อนของคู่แข่ง',
    'geometric screening proxy, not routed travel time. Base access = 100 * (1 - 0.55 * river_separated_share - 0.20 * expressway_separated_share). Detailed study ต้องใช้ frozen เครือข่ายเส้นทาง and approved crossing/ramp registry, 3 modes x 3 periods, no Euclidean fallback.': 'การคัดกรองนี้ใช้ระยะเชิงเรขาคณิต ไม่ใช่เวลาเดินทางจริง สูตรฐานคือ access = 100 × (1 − 0.55 × สัดส่วนอีกฝั่งแม่น้ำ − 0.20 × สัดส่วนอีกฝั่งทางด่วน) การศึกษารอบถัดไปต้องใช้เครือข่ายเส้นทางที่ตรึงรุ่นและทะเบียนจุดข้ามหรือทางขึ้นลงที่อนุมัติแล้ว ครบ 3 รูปแบบการเดินทาง × 3 ช่วงเวลา และห้ามใช้ระยะเส้นตรงแทน',
    'River และ motorway overlays: © OpenStreetMap contributors, ODbL 1.0. Motorway geometry เป็น presentation / screening overlay ไม่ใช่ routing, ramp หรือ directionality evidence.': 'ชั้นข้อมูลแม่น้ำและทางด่วน: © OpenStreetMap contributors, ODbL 1.0 รูปทรงทางด่วนใช้ประกอบการนำเสนอและคัดกรอง ไม่ใช่หลักฐานเส้นทาง จุดขึ้นลง หรือทิศทางการเดินรถ',
    'Basemap ใช้ทำอะไร': 'แผนที่พื้นฐานใช้ทำอะไร',
    'Light ใช้ Positron visual language; dark ใช้ Dark Matter visual language ผ่าน OpenFreeMap. Basemap ใช้ orientation เท่านั้น ไม่ได้สร้างคะแนน; ถ้า style/tile fail หน้าแสดง static evidence fallback และ evidence table ต่อเนื่อง.': 'โหมดสว่างใช้ Positron และโหมดมืดใช้ Dark Matter ผ่าน OpenFreeMap แผนที่พื้นฐานใช้เพื่อบอกตำแหน่งเท่านั้น ไม่ได้สร้างคะแนน หากแผนที่ออนไลน์โหลดไม่ได้ หน้ายังแสดงแผนที่หลักฐานสำรองและตารางหลักฐานต่อเนื่อง',
    'PARC Bangna · analytical release v3.3 · reference analysis v0.1 · interface v3.6': 'PARC Bangna · ข้อมูลวิเคราะห์ v3.3 · การวิเคราะห์จุดอ้างอิง v0.1 · หน้าจอ v3.6',
}
for old, new in visible_language_replacements.items():
    source = source.replace(old, new)

v36_css = r'''
.decision-first-head{max-width:66rem!important;margin-bottom:1.2rem}.decision-boundary{margin:0 0 1rem;padding:1rem 1.1rem;border-left:4px solid var(--garden);border-radius:0 var(--radius) var(--radius) 0;background:var(--garden-soft);color:var(--muted)}
.decision-boundary strong{color:var(--garden-deep)}.decision-reference-grid{margin-top:1.4rem}.decision-first-head+.decision-boundary+.fit-queue{margin-bottom:1.4rem}
.proxy-limit{color:var(--ink)!important}.approval-card .scope{font-size:clamp(1rem,1.5vw,1.25rem);line-height:1.5}.fit-table caption{text-align:left;font-weight:500;color:var(--ink)}
.lens-benchmark-note,.portfolio-current-note{margin:0 0 1.2rem;padding:.85rem 1rem;border-left:3px solid var(--amber);background:color-mix(in srgb,var(--card) 90%,var(--amber));color:var(--muted);font-size:.82rem}.portfolio-current-note{margin-top:1rem;border-left-color:var(--garden)}
section[id]{scroll-margin-top:5rem}.proxy-section{scroll-margin-top:5rem}
html[data-theme="dark"] .decision-boundary{background:#20352f;color:#d6dfda}html[data-theme="dark"] .decision-boundary strong{color:#f7f2e9}
'''
style_end = source.rfind('</style>', 0, source.index('</head>'))
if style_end < 0:
    raise RuntimeError("could not locate final head style block")
source = source[:style_end] + v36_css + source[style_end:]

source = replace_once(source, "__V36_FROZEN_REPORT_DATA__", frozen_report_data, "restore v3.3 payload")
source = replace_once(source, "__V36_FROZEN_REFERENCE_DATA__", frozen_reference_data, "restore reference payload")
source = "\n".join(line.rstrip() for line in source.split("\n"))

OUTPUT.write_text(source, encoding="utf-8")
INDEX.write_text(source, encoding="utf-8")
print(f"Built {OUTPUT.name} and index.html ({len(source.encode('utf-8')):,} bytes)")
