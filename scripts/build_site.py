#!/usr/bin/env python3
"""Build the Release 1.6 HTML report.

This generator intentionally reads only the validated/local Release 1.6 analysis
bundle. It does not geocode, rescore, or invent map context.
"""

from __future__ import annotations

import html
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
OUT = ROOT / "index.html"


def load(name: str):
    return json.loads((ANALYSIS / name).read_text(encoding="utf-8"))


def esc(value) -> str:
    return html.escape(str(value), quote=True)


screening = load("screening-results.json")
scenario = load("competition-scenario-results.json")
breakdown = load("competitor-score-breakdown.json")
registry = load("competitor-registry.public.json")
candidate_metrics = load("candidate-metrics.json")

canonical = {item["candidate_id"]: item for item in screening["candidates"]}
scenario_by_id = {item["candidate_id"]: item for item in scenario["candidates"]}
competition = {item["candidate_id"]: item for item in breakdown["candidates"]}
competitors = {item["competitor_id"]: item for item in registry["competitors"]}
centers = {
    item["candidate_id"]: item["center_wgs84"]
    for item in candidate_metrics["candidates"]
}
hypotheses = {
    item["candidate_id"]: item for item in registry["strategic_gap_hypotheses"]
}

positive_logo = "assets/parc-bangna-logo-transparent.png"
reverse_logo = "assets/parc-bangna-logo-reverse-transparent.png"

baseline_context = {
    "wongwian-yai-east": {
        "traffic": 71.64,
        "fit": 73.58,
        "baseline": "catchment ไม่พึ่งพื้นที่ย่อยเดียว และสัญญาณ resident/visitor แข็ง",
        "gate": "คู่แข่งตรงภายใน 300 ม. และศูนย์ขนาดใหญ่หลายแห่งทำให้สิทธิ์ไซต์หรือจุดต่างต้องชัดมาก",
        "next": "คัดแปลงเฉพาะจุดที่มี access advantage แล้วสำรวจ routine overlap กับ Platform และกลุ่ม ICONSIAM–ICS",
    },
    "charoen-rat": {
        "traffic": 68.79,
        "fit": 76.47,
        "baseline": "PMF สูงและ traffic balance ดี",
        "gate": "KINGSQUARE วางตัวเป็น community mall โดยตรง ขณะที่ Terminal21 Rama 3 และ Central Rama 3 เติม supply กว้าง",
        "next": "ทำ tenant-overlap และ downside economics ก่อนนับ traffic; กลยุทธ์ต้องต่างจาก KINGSQUARE แบบวัดได้",
    },
    "samre": {
        "traffic": 68.50,
        "fit": 76.36,
        "baseline": "resident-led และ fit สมดุล",
        "gate": "จุดกลางเชิงวิเคราะห์เกือบซ้อน Riverside Plaza จึงอาจเป็น artifact ของ candidate center",
        "next": "นิยาม parcel และตั้งจุดกลางใหม่ก่อนสำรวจ demand; ยังไม่ควรหาแปลงจากพิกัดนี้",
    },
    "ban-khaek": {
        "traffic": 69.23,
        "fit": 74.34,
        "baseline": "traffic breadth และ experience fit ดี",
        "gate": "วงกลมครอบ supply หลายฝั่งแม่น้ำ แต่โมเดลยังไม่คิดสะพาน เรือ และเวลาเดินทางจริง",
        "next": "สร้าง network catchment ก่อน แล้วค่อยทดสอบ routine-led gap และ after-school → dinner",
    },
    "talat-phlu-south": {
        "traffic": 59.98,
        "fit": 80.76,
        "baseline": "Offering PMF และ Experience Fit สูงสุด",
        "gate": "The Mall Lifestore Tha Phra อยู่ใกล้มาก และ Riverside Plaza อยู่ในวงเดียวกัน",
        "next": "ทดสอบเฉพาะ format ที่เร็วกว่า สงบกว่า และ routine-led กว่า incumbent; ตรวจ access และ catchment demand",
    },
    "bang-pakok": {
        "traffic": 63.57,
        "fit": 73.97,
        "baseline": "routine/family fit ดี และอันดับฐานคงที่",
        "gate": "Terminal21 Rama 3 อยู่ใกล้ แต่ supply ที่ยืนยันในวงยังเบากว่ากลุ่มอื่น; registry ยังเป็น minimum verified set",
        "next": "เดินหน้าตรวจทำเลเชิงรุก: นับ after-school–evening routine และวัด leakage ไป Terminal21",
    },
    "wang-lang": {
        "traffic": 60.25,
        "fit": 75.92,
        "baseline": "visitor/connector signal รองรับ demand",
        "gate": "Tha Maharaj อยู่ใกล้ และแม่น้ำ/เรือ/สะพานทำให้ระยะเส้นตรงอาจแปลความผิด",
        "next": "ลงพื้นที่และสร้าง travel-time catchment; เปรียบเทียบ compact กับ full format",
    },
    "ratchathewi": {
        "traffic": 59.69,
        "fit": 73.94,
        "baseline": "visitor/daytime signal เด่น",
        "gate": "minimum verified set พบศูนย์ impact สูง 6 แห่งในระยะไม่ถึง 1 กม. และ parcel economics ตึง",
        "next": "หยุด full-format assumption; เดินหน้าต่อเมื่อมีสิทธิ์ไซต์หรือ micro-format ที่ไม่ชน destination cluster",
    },
    "pracha-uthit": {
        "traffic": 62.91,
        "fit": 69.60,
        "baseline": "traffic index ยังแข่งขันได้และ land pressure ต่ำ",
        "gate": "พบ Market Place Pracha Uthit ในวง แต่พิกัด host ยังมาจาก tenant proxy จึงไม่วาดบนแผนที่",
        "next": "ยืนยัน host centroid และสำรวจ noon/after-school/evening ก่อนยกระดับจาก Tier B",
    },
    "din-daeng": {
        "traffic": 60.50,
        "fit": 72.01,
        "baseline": "visitor และ daytime proxy สูง",
        "gate": "supply หนาแน่นทั้ง Rama 9–Ratchada และ Siam edge; registry ยังเป็น minimum verified set",
        "next": "เดินหน้าต่อเฉพาะเมื่อมี format/parcel advantage ชัด; แยก resident vs worker และ multi-tenant stop",
    },
}


def metric_for_marker(comp: dict) -> tuple[float, str, str]:
    """Return SVG radius, reader-facing basis, and machine basis.

    Comparable current leasable area gets first priority. Other operator metrics
    are explicitly identified as non-GLA. If neither exists, use the disclosed
    analytical impact class rather than a fabricated number.
    """

    metrics = comp.get("operator_metrics", [])
    priorities = (
        "leasable_area",
        "commercial_space",
        "total_project_area",
        "retail_complex_area",
        "brand_count_minimum",
        "project_shop_capacity",
    )
    labels = {
        "leasable_area": "พื้นที่ให้เช่าที่ผู้ดำเนินการรายงาน",
        "commercial_space": "พื้นที่พาณิชย์ที่ผู้ดำเนินการรายงาน (ไม่ใช่ GLA ปัจจุบัน)",
        "total_project_area": "พื้นที่โครงการที่ผู้ดำเนินการรายงาน (ไม่ใช่ GLA)",
        "retail_complex_area": "พื้นที่ retail complex เชิงประวัติ (ไม่ใช่ GLA ปัจจุบัน)",
        "brand_count_minimum": "จำนวนแบรนด์ขั้นต่ำที่ผู้ดำเนินการรายงาน",
        "project_shop_capacity": "ความจุร้านตามคำอธิบายโครงการ (ไม่ใช่จำนวนร้านที่เปิดจริง)",
    }
    for name in priorities:
        found = next((m for m in metrics if m["metric_name"] == name), None)
        if not found:
            continue
        value = float(found["value"])
        unit = found["unit"]
        if unit == "sqm":
            radius = 16 if value >= 100000 else 14 if value >= 40000 else 12 if value >= 10000 else 10
        else:
            radius = 16 if value >= 300 else 14 if value >= 100 else 12 if value >= 40 else 10
        value_text = f"{value:,.0f} {unit}"
        return radius, f"{labels[name]} · {value_text}", name

    impact = comp["impact"]["class"]
    radius = {"high": 14, "medium_high": 12, "medium": 10}.get(impact, 10)
    impact_th = {"high": "สูง", "medium_high": "กลาง–สูง", "medium": "กลาง"}.get(impact, impact)
    return radius, f"ชั้น impact เชิงวิเคราะห์ {impact_th}; ไม่ใช่ GLA หรือ tenant count", f"impact_class:{impact}"


def source_kind_label(source_kind: str) -> str:
    labels = {
        "authoritative_external_report": "external current report",
        "authoritative_current_guide": "external current guide",
        "authoritative_current_business_report": "external current business report",
    }
    return labels.get(source_kind, source_kind.replace("_", " "))


def source_links(comp: dict) -> str:
    rows = []
    for index, source in enumerate(comp.get("source_urls", [])[:3], start=1):
        rows.append(
            f'<li><a href="{esc(source["url"])}" rel="noreferrer">{esc(source["publisher"])}</a>'
            f'<span>{esc(source_kind_label(source["source_kind"]))}</span></li>'
        )
    return "".join(rows)


def map_for(candidate: dict, comp_data: dict) -> tuple[str, str]:
    center = centers[candidate["candidate_id"]]
    cx, cy, outer_r = 210.0, 160.0, 118.0
    px_per_km = outer_r / breakdown["catchment_radius_km"]
    cos_lat = math.cos(math.radians(center["latitude"]))
    member_by_id = {item["competitor_id"]: item for item in comp_data["member_loads"]}
    plotted = []
    withheld = []
    for comp_id in comp_data["competitor_ids"]:
        comp = competitors[comp_id]
        if comp["location"]["confidence"] != "high":
            withheld.append(comp)
            continue
        d = member_by_id[comp_id]
        dx_km = (comp["location"]["lon"] - center["longitude"]) * 111.32 * cos_lat
        dy_km = (comp["location"]["lat"] - center["latitude"]) * 110.574
        x = cx + dx_km * px_per_km
        y = cy - dy_km * px_per_km
        radius, size_label, size_basis = metric_for_marker(comp)
        plotted.append((comp, d, x, y, radius, size_label, size_basis))

    marker_bits = []
    detail_bits = []
    map_rows = []
    for marker_index, (comp, d, x, y, radius, size_label, size_basis) in enumerate(plotted, start=1):
        detail_id = f'{candidate["candidate_id"]}-{comp["competitor_id"]}'
        impact = comp["impact"]["class"]
        marker_bits.append(
            f'<a class="competitor-marker impact-{esc(impact)}" href="#competitor-{esc(detail_id)}" '
            f'data-competitor-id="{esc(comp["competitor_id"])}" '
            f'data-map-candidate-id="{esc(candidate["candidate_id"])}" '
            f'data-impact-class="{esc(impact)}" data-size-basis="{esc(size_basis)}" '
            f'aria-label="{esc(comp["canonical_name"])} ระยะ {d["distance_km"]:.2f} กิโลเมตร; เปิดรายละเอียด">'
            f'<title>{esc(comp["canonical_name"])} · {d["distance_km"]:.2f} km · {esc(size_label)}</title>'
            f'<circle class="marker-hit" cx="{x:.1f}" cy="{y:.1f}" r="22"></circle>'
            f'<circle class="marker-shape" cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}"></circle>'
            f'<text x="{x:.1f}" y="{y + 0.8:.1f}">{marker_index}</text></a>'
        )
        map_rows.append(
            f'<tr data-competitor-id="{esc(comp["competitor_id"])}"><td><span class="map-key impact-{esc(impact)}">{marker_index}</span></td>'
            f'<th scope="row"><a href="#competitor-{esc(detail_id)}">{esc(comp["canonical_name"])}</a></th>'
            f'<td>{d["distance_km"]:.2f} km</td><td>{esc(size_label)}</td><td>วาดแล้ว</td></tr>'
        )
        source = comp["location"]["coordinate_source"]
        detail_bits.append(
            f'<details class="competitor-detail" id="competitor-{esc(detail_id)}" '
            f'data-competitor-details data-competitor-detail="{esc(comp["competitor_id"])}" '
            f'data-competitor-id="{esc(comp["competitor_id"])}" data-evidence-status="plotted">'
            f'<summary><span><b>{marker_index}. {esc(comp["canonical_name"])}</b>'
            f'<small>{d["distance_km"]:.2f} km · impact {esc(comp["impact"]["class"].replace("_", "–"))}</small></span>'
            f'<span class="chevron" aria-hidden="true"></span></summary>'
            f'<div class="competitor-detail-body"><p><strong>ขนาด marker:</strong> {esc(size_label)}</p>'
            f'<p><strong>ฐานการจัดชั้นเชิงวิเคราะห์:</strong> {esc(comp["impact"]["basis"])}</p>'
            f'<p><strong>พิกัด:</strong> {esc(comp["location"]["coordinate_basis"].replace("_", " "))}; '
            f'confidence {esc(comp["location"]["confidence"])} · {esc(source["title"])}</p>'
            f'<p class="guardrail">ชั้น impact เป็นการจัดชั้นเพื่อเทียบ supply ไม่ใช่ข้อมูล occupancy, footfall, ยอดขาย หรือความอ่อนแอของคู่แข่ง</p>'
            f'<ul class="source-links">{source_links(comp)}</ul></div></details>'
        )

    for comp in withheld:
        d = member_by_id[comp["competitor_id"]]
        radius, size_label, _ = metric_for_marker(comp)
        detail_id = f'{candidate["candidate_id"]}-{comp["competitor_id"]}'
        map_rows.append(
            f'<tr data-competitor-id="{esc(comp["competitor_id"])}"><td>—</td><th scope="row"><a href="#competitor-{esc(detail_id)}">{esc(comp["canonical_name"])}</a></th>'
            f'<td>{d["distance_km"]:.2f} km</td><td>{esc(size_label)}</td>'
            f'<td><strong>ไม่วาด</strong> · พิกัด {esc(comp["location"]["confidence"])}</td></tr>'
        )
        detail_bits.append(
            f'<details class="competitor-detail withheld" id="competitor-{esc(detail_id)}" '
            f'data-competitor-details data-competitor-detail="{esc(comp["competitor_id"])}" '
            f'data-competitor-id="{esc(comp["competitor_id"])}" data-evidence-status="withheld">'
            f'<summary><span><b>{esc(comp["canonical_name"])}</b>'
            f'<small>{d["distance_km"]:.2f} km · ไม่วาด marker จนกว่าจะยืนยัน host centroid</small></span>'
            f'<span class="chevron" aria-hidden="true"></span></summary>'
            f'<div class="competitor-detail-body"><p><strong>เหตุผลที่ไม่วาด:</strong> '
            f'{esc(comp["location"]["coordinate_basis"].replace("_", " "))}; '
            f'confidence {esc(comp["location"]["confidence"])}.</p>'
            f'<p><strong>หลักฐานด้านตัวตน/สถานะยังใช้ได้:</strong> {esc(comp["operating_status"]["verification_basis"])}</p>'
            f'<ul class="source-links">{source_links(comp)}</ul></div></details>'
        )

    desc = (
        f'วงกลมแสดง analytical catchment รัศมี {breakdown["catchment_radius_km"]:.5f} กิโลเมตร '
        f'จุดกึ่งกลางเป็น restaurant-sample medoid ไม่ใช่แปลงลงทุน '
        f'วาดคู่แข่งที่พิกัด confidence สูง {len(plotted)} แห่ง'
    )
    svg = f"""
    <figure class="clean-map" data-map-role="detail"
      data-map-candidate-id="{esc(candidate["candidate_id"])}" id="map-{esc(candidate["candidate_id"])}">
      <svg viewBox="0 0 420 320" role="img" aria-labelledby="map-title-{esc(candidate["candidate_id"])} map-desc-{esc(candidate["candidate_id"])}">
        <title id="map-title-{esc(candidate["candidate_id"])}">แผนที่เชิงวิเคราะห์ของ {esc(candidate["name"])}</title>
        <desc id="map-desc-{esc(candidate["candidate_id"])}">{esc(desc)}</desc>
        <circle class="analysis-extent" cx="{cx}" cy="{cy}" r="{outer_r}"></circle>
        <path class="candidate-center" d="M {cx} {cy-9} L {cx+9} {cy} L {cx} {cy+9} L {cx-9} {cy} Z">
          <title>จุดกลางเชิงวิเคราะห์ของ {esc(candidate["name"])}; ไม่ใช่ตำแหน่งแปลง</title>
        </path>
        {"".join(marker_bits)}
        <g class="north" aria-hidden="true"><path d="M378 46V20M378 20l-5 8M378 20l5 8"></path><text x="378" y="14">N</text></g>
        <g class="scale" aria-hidden="true"><path d="M28 284h{px_per_km:.1f}"></path><path d="M28 280v8M{28+px_per_km:.1f} 280v8"></path>
          <text x="28" y="303">1 km</text></g>
      </svg>
      <figcaption><strong>แผนที่ตั้งใจเว้นถนน รถไฟ และสถานี</strong> เพราะ Release นี้ยังไม่มี feature-level lineage ที่ตรวจซ้ำได้
      วงกลมคือขอบเขตวิเคราะห์เท่ากันทุกทำเล ไม่ใช่ parcel, legal boundary หรือพื้นที่เดินทางจริง</figcaption>
    </figure>
    """
    table = f"""
    <div class="map-fallback" id="{esc(candidate["candidate_id"])}-competitor-table" data-map-fallback>
      <section class="table-scroll" tabindex="0" aria-label="รายการคู่แข่งของ {esc(candidate["name"])} เลื่อนแนวนอนได้">
        <table><caption>คู่แข่งที่ยืนยันว่าเปิดให้บริการใน analytical catchment</caption>
          <thead><tr><th scope="col">Marker</th><th scope="col">คู่แข่ง</th><th scope="col">ระยะเส้นตรง</th><th scope="col">ฐานขนาด marker</th><th scope="col">สถานะแผนที่</th></tr></thead>
          <tbody>{"".join(map_rows)}</tbody>
        </table>
      </section>
      <div class="competitor-details">{"".join(detail_bits)}</div>
    </div>
    """
    return svg, table


def overview_map() -> str:
    """Render candidate centers at one shared kilometre-per-pixel scale."""
    rows = sorted(screening["candidates"], key=lambda item: item["rank"])
    points = [
        (
            row,
            centers[row["candidate_id"]]["latitude"],
            centers[row["candidate_id"]]["longitude"],
        )
        for row in rows
    ]
    mean_lat = sum(lat for _, lat, _ in points) / len(points)
    mean_lon = sum(lon for _, _, lon in points) / len(points)
    cos_lat = math.cos(math.radians(mean_lat))
    projected = [
        (
            row,
            (lon - mean_lon) * 111.32 * cos_lat,
            (lat - mean_lat) * 110.574,
        )
        for row, lat, lon in points
    ]
    min_x = min(x_km for _, x_km, _ in projected)
    max_x = max(x_km for _, x_km, _ in projected)
    min_y = min(y_km for _, _, y_km in projected)
    max_y = max(y_km for _, _, y_km in projected)
    width, height, pad = 620.0, 340.0, 46.0
    usable_w = width - (2 * pad)
    usable_h = height - (2 * pad)
    km_per_px = max((max_x - min_x) / usable_w, (max_y - min_y) / usable_h)
    px_per_km = 1 / km_per_px
    plotted_w = (max_x - min_x) * px_per_km
    plotted_h = (max_y - min_y) * px_per_km
    offset_x = (width - plotted_w) / 2
    offset_y = (height - plotted_h) / 2
    marks = []
    for row, x_km, y_km in projected:
        x = offset_x + (x_km - min_x) * px_per_km
        y = offset_y + (max_y - y_km) * px_per_km
        marks.append(
            f'<a class="overview-candidate" href="#candidate-{esc(row["candidate_id"])}" '
            f'aria-label="อันดับ {row["rank"]} {esc(row["name"])}">'
            f'<title>อันดับ {row["rank"]} · {esc(row["name"])}</title>'
            f'<circle class="overview-hit" cx="{x:.1f}" cy="{y:.1f}" r="22"></circle>'
            f'<circle class="overview-dot" cx="{x:.1f}" cy="{y:.1f}" r="13"></circle>'
            f'<text x="{x:.1f}" y="{y + 0.8:.1f}">{row["rank"]}</text></a>'
        )
    return f"""
    <figure class="overview-map" data-map-role="overview" id="map-top10-overview">
      <svg viewBox="0 0 {width:.0f} {height:.0f}" role="img"
        aria-labelledby="overview-title overview-desc">
        <title id="overview-title">ภาพรวมจุดอ้างอิงของ Top 10</title>
        <desc id="overview-desc">แสดงตำแหน่งสัมพัทธ์จากพิกัด WGS84 ของจุดกลางเชิงวิเคราะห์ทั้งสิบแห่งด้วยสเกลกิโลเมตรต่อพิกเซลเดียวกันทั้งสองแกน ไม่มีถนน รถไฟ สถานี หรือขอบเขตที่ดิน</desc>
        {"".join(marks)}
        <g class="north" aria-hidden="true"><path d="M585 68V42M585 42l-5 8M585 42l5 8"></path><text x="585" y="35">N</text></g>
        <g class="scale" aria-hidden="true"><path d="M38 302h{5 * px_per_km:.1f}"></path><path d="M38 298v8M{38 + (5 * px_per_km):.1f} 298v8"></path><text x="38" y="324">5 km</text></g>
      </svg>
      <figcaption>ภาพนี้ใช้ดูตำแหน่งสัมพัทธ์ของ candidate centers เท่านั้น โดยรักษาสเกลระยะเท่ากันทั้งสองแกน—เลขตรงกับอันดับฐานและตารางด้านล่าง</figcaption>
    </figure>
    """


cards = []
comparison_rows = []
scenario_rows = []
action_counts = {"A": 0, "B": 0, "C": 0, "D": 0}

for candidate in screening["candidates"]:
    cid = candidate["candidate_id"]
    comp = competition[cid]
    scenario_item = scenario_by_id[cid]
    context = baseline_context[cid]
    registry_id = comp["registry_candidate_id"]
    hypothesis = hypotheses[registry_id]
    tier = comp["recommended_action"]["tier"]
    action_counts[tier] += 1
    group = "opportunity" if tier in {"A", "B"} else "differentiate" if tier == "C" else "highpressure"
    map_html, map_fallback = map_for(candidate, comp)
    gap_caveat = (
        ' data-caveat-id="samre-center-coincides-with-incumbent"'
        ' data-caveat-severity="decision-changing"'
        ' data-caveat-visibility="inline"'
        if cid == "samre"
        else ""
    )

    comparison_rows.append(
        f'<tr data-filter-candidate="{esc(cid)}" data-action-group="{group}">'
        f'<td>{candidate["rank"]}</td><th scope="row"><a href="#candidate-{esc(cid)}">{esc(candidate["name"])}</a></th>'
        f'<td>{candidate["overall_score"]:.2f}</td><td>{context["traffic"]:.2f}</td><td>{context["fit"]:.2f}</td>'
        f'<td>{comp["verified_competitor_count"]}</td><td>{comp["competitive_room_score"]:.2f}</td>'
        f'<td><span class="tier tier-{tier.lower()}">Tier {tier}</span></td></tr>'
    )
    scenario_rows.append(
        f'<tr><th scope="row">{esc(candidate["name"])}</th><td>{candidate["rank"]}</td>'
        f'<td>{scenario_item["rank"]}</td><td>{scenario_item["overall_score"]:.2f}</td></tr>'
    )

    cards.append(
        f"""
        <article class="candidate-card" id="candidate-{esc(cid)}"
          data-candidate-id="{esc(cid)}" data-candidate-name="{esc(candidate["name"])}"
          data-rank="{candidate["rank"]}" data-score="{candidate["overall_score"]}"
          data-action-group="{group}">
          <header class="candidate-heading">
            <div><span class="rank">#{candidate["rank"]}</span>
              <p class="eyebrow">Release 1.5 baseline · {candidate["overall_score"]:.2f}/100</p>
              <h3>{esc(candidate["name"])}</h3></div>
            <div class="candidate-status"><span class="tier tier-{tier.lower()}">Tier {tier}</span>
              <small>{esc(comp["recommended_action"]["label_th"])}</small></div>
          </header>
          <div class="candidate-metrics" role="group" aria-label="ตัวชี้วัดของ {esc(candidate["name"])}">
            <div><strong>{candidate["overall_score"]:.2f}</strong><span>คะแนนฐาน</span></div>
            <div><strong>{comp["competitive_room_score"]:.2f}</strong><span>competitive room*</span></div>
            <div><strong>{comp["competitor_supply_pressure"]:.0f}</strong><span>supply pressure*</span></div>
            <div><strong>{comp["verified_competitor_count"]}</strong><span>คู่แข่งที่ยืนยัน</span></div>
          </div>
          <p class="metric-note">* ดัชนี 0–100 ที่ derive จาก minimum verified set เพื่อกำหนด action tier เท่านั้น ยังไม่แทนคะแนนฐานหรือเป็น final reranking</p>
          <div class="decision-grid">
            <div><p class="label">เหตุผลจาก Release 1.5</p><p>{esc(context["baseline"])}</p></div>
            <div><p class="label">สิ่งที่คู่แข่งเปลี่ยน</p><p>{esc(context["gate"])}</p></div>
            <div><p class="label">การตรวจต่อไป</p><p>{esc(context["next"])}</p></div>
          </div>
          <div class="map-layout">{map_html}{map_fallback}</div>
          <div class="gap-hypothesis"{gap_caveat}>
            <p class="label">Strategic gap · สมมติฐานที่ต้องพิสูจน์</p>
            <p>{esc(hypothesis["hypothesis"])}</p>
            <small>ต้องตรวจ: {esc(" · ".join(hypothesis["validation_required"]))}</small>
          </div>
          <details class="evidence-disclosure">
            <summary data-evidence-toggle data-evidence-candidate-id="{esc(cid)}">
              <span class="evidence-icon" aria-hidden="true"></span>
              <span><b>เปิดหลักฐานและข้อจำกัด</b><small>ฐานคะแนน · สูตรแรงกดดัน · สิ่งที่ยังไม่รู้</small></span>
              <span class="chevron" aria-hidden="true"></span>
            </summary>
            <div class="evidence-body">
              <div><p class="label">ฐานคะแนน</p>
                <p>Catchment Traffic {context["traffic"]:.2f} × Offering PMF {context["fit"]:.2f} / 100 = {candidate["overall_score"]:.2f}</p></div>
              <div><p class="label">Competition overlay</p>
                <p>Pressure load {comp["raw_pressure_load"]:.4g}; cluster-deduplicated ก่อนแปลงเป็น supply pressure {comp["competitor_supply_pressure"]:.2f}. Competitive room = 70% headroom + 30% strategic-gap hypothesis.</p></div>
              <div><p class="label">ความพร้อมของหลักฐาน</p>
                <p>{comp["evidence_readiness_score"]:.0f}/100 · {esc("; ".join(x["reason"].replace("_", " ") for x in comp["evidence_readiness_adjustments"]))}</p></div>
              <div><p class="label">ระยะ</p><p>ระยะ Haversine เส้นตรง ไม่คิดถนน สะพาน เรือ ความติดขัด หรือ pedestrian barrier.</p></div>
            </div>
          </details>
        </article>
        """
    )


sources_seen = set()
source_cards = []
for comp in registry["competitors"]:
    for source in comp.get("source_urls", []):
        url = source["url"]
        if url in sources_seen:
            continue
        sources_seen.add(url)
        source_cards.append(
            f'<li data-competitor-source-id="competitor-source-{len(source_cards)+1}">'
            f'<a href="{esc(url)}" rel="noreferrer">{esc(source["publisher"])}</a>'
            f'<span>{esc(source_kind_label(source["source_kind"]))}</span></li>'
        )


html_doc = f"""<!DOCTYPE html>
<html lang="th" data-brand="parc">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Release 1.6: Top 10 ทำเลแนวคิดแบบ PARC Bangna พร้อม competitive-supply overlay และแผนที่คู่แข่งที่รักษา evidence lineage">
  <meta name="analysis-release" content="Release 1.6 · Competition diagnostic and clean evidence maps">
  <meta name="design-system" content="J Lifestyle Center Design System v0.3">
  <meta name="theme-color" content="#F7F2E9">
  <title>Top 10 ทำเลแบบ PARC Bangna · Release 1.6</title>
  <script>
  (() => {{
    const valid = new Set(["system", "light", "dark"]);
    let state = {{mode:"system", step:0}};
    try {{
      const saved = localStorage.getItem("parc-theme-cycle-v1");
      if (saved) {{
        const parsed = JSON.parse(saved);
        if (valid.has(parsed.mode)) state = {{mode:parsed.mode, step:Number(parsed.step)||0}};
      }} else {{
        const legacy = localStorage.getItem("parc-screening-theme");
        if (legacy === "light" || legacy === "dark") state = {{mode:legacy, step:2}};
      }}
    }} catch (_) {{}}
    window.__parcThemeBoot = state;
    if (state.mode === "light" || state.mode === "dark") document.documentElement.dataset.theme = state.mode;
  }})();
  </script>
  <style>
    @font-face {{
      font-family:"Anuphan"; font-style:normal; font-display:swap; font-weight:300;
      src:url("assets/fonts/anuphan-thai-300-normal.woff2") format("woff2");
      unicode-range:U+02D7,U+0303,U+0331,U+0E01-0E5B,U+200C-200D,U+25CC;
    }}
    @font-face {{
      font-family:"Anuphan"; font-style:normal; font-display:swap; font-weight:300;
      src:url("assets/fonts/anuphan-latin-300-normal.woff2") format("woff2");
      unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD;
    }}
    @font-face {{
      font-family:"IBM Plex Sans Thai Looped"; font-style:normal; font-display:swap; font-weight:400;
      src:url("assets/fonts/ibm-plex-sans-thai-looped-thai-400-normal.woff2") format("woff2");
      unicode-range:U+02D7,U+0303,U+0331,U+0E01-0E5B,U+200C-200D,U+25CC;
    }}
    @font-face {{
      font-family:"IBM Plex Sans Thai Looped"; font-style:normal; font-display:swap; font-weight:400;
      src:url("assets/fonts/ibm-plex-sans-thai-looped-latin-400-normal.woff2") format("woff2");
      unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD;
    }}
    @font-face {{
      font-family:"IBM Plex Sans Thai Looped"; font-style:normal; font-display:swap; font-weight:500;
      src:url("assets/fonts/ibm-plex-sans-thai-looped-thai-500-normal.woff2") format("woff2");
      unicode-range:U+02D7,U+0303,U+0331,U+0E01-0E5B,U+200C-200D,U+25CC;
    }}
    @font-face {{
      font-family:"IBM Plex Sans Thai Looped"; font-style:normal; font-display:swap; font-weight:500;
      src:url("assets/fonts/ibm-plex-sans-thai-looped-latin-500-normal.woff2") format("woff2");
      unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD;
    }}
    :root {{
      color-scheme: light;
      --canvas:#F7F2E9; --surface:#FFFDF8; --surface-2:#EFE6D9; --ink:#24312F;
      --muted:#45514D; --line:#D9CFC2; --brand:#365E55; --brand-strong:#365E55;
      --garden:#365E55; --magenta:#A94372; --bougainvillea:#D84BA2; --warm:#B8AA93;
      --warm-text:#504A45; --marker-text-high:#fff; --marker-text:#1B2522; --marker-text-garden:#fff;
      --action-bg:#365E55; --action-ink:#FFFFFF; --action-support:#E8F0ED;
      --focus:#A94372; --shadow:0 18px 46px rgba(23,51,45,.08);
      --shell:min(1180px,calc(100% - 40px)); --radius:18px;
    }}
    html[data-theme="dark"] {{
      color-scheme:dark; --canvas:#1B2522; --surface:#26322E; --surface-2:#303D38;
      --ink:#F7F1E6; --muted:#D8CDBE; --line:#57615C; --brand:#AFC6BC;
      --brand-strong:#AFC6BC; --garden:#AFC6BC; --magenta:#F19AC3; --bougainvillea:#F19AC3;
      --warm:#C0B3A4; --warm-text:#D8CDBE; --marker-text-high:#1B2522; --marker-text:#1B2522; --marker-text-garden:#1B2522;
      --action-bg:#365E55; --action-ink:#FFFFFF; --action-support:#E8F0ED;
      --focus:#F19AC3; --shadow:0 18px 46px rgba(0,0,0,.24);
    }}
    @media (prefers-color-scheme:dark) {{
      html:not([data-theme]) {{
        color-scheme:dark; --canvas:#1B2522; --surface:#26322E; --surface-2:#303D38;
        --ink:#F7F1E6; --muted:#D8CDBE; --line:#57615C; --brand:#AFC6BC;
        --brand-strong:#AFC6BC; --garden:#AFC6BC; --magenta:#F19AC3; --bougainvillea:#F19AC3;
        --warm:#C0B3A4; --warm-text:#D8CDBE; --marker-text-high:#1B2522; --marker-text:#1B2522; --marker-text-garden:#1B2522;
        --action-bg:#365E55; --action-ink:#FFFFFF; --action-support:#E8F0ED;
        --focus:#F19AC3; --shadow:0 18px 46px rgba(0,0,0,.24);
      }}
    }}
    * {{ box-sizing:border-box; }}
    html {{ scroll-behavior:smooth; scroll-padding-top:90px; }}
    body {{ margin:0; background:var(--canvas); color:var(--ink); font-family:"IBM Plex Sans Thai Looped","Noto Sans Thai",Tahoma,sans-serif; font-size:18px; line-height:1.7; font-synthesis:none; }}
    a {{ color:var(--brand-strong); text-underline-offset:3px; }}
    button,summary,a {{ -webkit-tap-highlight-color:transparent; }}
    button:focus-visible,summary:focus-visible,a:focus-visible {{ outline:3px solid var(--focus); outline-offset:3px; border-radius:5px; }}
    img,svg {{ display:block; max-width:100%; }}
    h1,h2,h3 {{ font-family:"Anuphan","Noto Sans Thai",Tahoma,sans-serif; font-weight:300; letter-spacing:0; line-height:1.18; margin:0; text-wrap:balance; }}
    h1 {{ font-size:clamp(2.67rem,6vw,5.25rem); max-width:14ch; }}
    h2 {{ font-size:clamp(2rem,4vw,3.2rem); }}
    h3 {{ font-size:clamp(1.56rem,3vw,2.25rem); }}
    p {{ margin:.4rem 0 1rem; }}
    .shell {{ width:var(--shell); margin-inline:auto; }}
    .skip-link {{ position:fixed; z-index:100; left:16px; top:10px; transform:translateY(-140%); background:var(--ink); color:var(--canvas); padding:10px 14px; }}
    .skip-link:focus {{ transform:none; }}
    .sr-only {{ position:absolute!important; width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0; }}
    .site-header {{ position:sticky; top:0; z-index:30; background:var(--canvas); border-bottom:1px solid var(--line); }}
    .header-inner {{ min-height:72px; display:flex; align-items:center; justify-content:space-between; gap:24px; }}
    .brand {{ display:flex; align-items:center; min-height:48px; text-decoration:none; }}
    .brand img {{ width:126px; height:auto; }}
    .header-tools {{ display:flex; align-items:center; gap:18px; min-width:0; }}
    nav {{ display:flex; gap:4px; overflow:auto; scrollbar-width:none; }}
    nav a {{ display:flex; min-height:44px; align-items:center; padding:6px 10px; color:var(--muted); text-decoration:none; font-size:.88rem; white-space:nowrap; }}
    nav a:hover {{ color:var(--ink); }}
    .theme-cycle {{
      width:48px; height:48px; flex:0 0 48px; border:1px solid var(--garden); border-radius:50%;
      display:grid; place-items:center; color:var(--ink); background:transparent; cursor:pointer;
    }}
    .theme-cycle:hover {{ background:var(--surface-2); border-color:var(--garden); }}
    .theme-cycle svg {{ width:21px; height:21px; fill:none; stroke:currentColor; stroke-width:1.8; stroke-linecap:round; stroke-linejoin:round; }}
    .theme-cycle [hidden] {{ display:none; }}
    section {{ padding:80px 0; }}
    .hero {{ padding-top:86px; background:linear-gradient(135deg,var(--canvas),color-mix(in srgb,var(--garden) 12%,var(--canvas))); border-bottom:1px solid var(--line); }}
    .hero-grid {{ display:grid; grid-template-columns:minmax(0,1.35fr) minmax(280px,.65fr); gap:clamp(40px,7vw,100px); align-items:end; }}
    .eyebrow,.label {{ margin:0 0 8px; color:var(--brand-strong); font-weight:500; font-size:.82rem; letter-spacing:0; text-transform:none; }}
    .hero .lede {{ max-width:70ch; font-size:clamp(1.05rem,2vw,1.25rem); color:var(--muted); }}
    .hero-facts {{ display:flex; flex-wrap:wrap; gap:10px 24px; color:var(--muted); font-size:.92rem; margin-top:28px; }}
    .hero-score {{ border-left:1px solid var(--line); padding-left:34px; }}
    .hero-score > strong {{ font:300 clamp(4.5rem,10vw,8rem)/.9 "Anuphan",sans-serif; color:var(--brand); }}
    .hero-score > span {{ display:block; margin-top:12px; font-weight:500; }}
    .hero-score p {{ color:var(--muted); font-size:.93rem; }}
    .caveat {{ margin-top:38px; padding:18px 20px; border-left:4px solid var(--magenta); background:var(--surface); max-width:92ch; }}
    .section-head {{ display:grid; grid-template-columns:minmax(0,.9fr) minmax(320px,1.1fr); gap:clamp(30px,6vw,86px); align-items:start; margin-bottom:36px; }}
    .section-head > p,.section-copy {{ color:var(--muted); max-width:70ch; }}
    .decision-strip {{ display:grid; grid-template-columns:repeat(4,1fr); border-block:1px solid var(--line); }}
    .decision-strip > div {{ padding:24px; border-right:1px solid var(--line); }}
    .decision-strip > div:last-child {{ border-right:0; }}
    .decision-strip strong {{ display:block; font:500 2.4rem/1 "IBM Plex Sans Thai Looped",sans-serif; color:var(--brand); font-variant-numeric:tabular-nums; }}
    .decision-strip span {{ display:block; color:var(--muted); margin-top:8px; }}
    .primary-action {{ margin-top:28px; display:grid; grid-template-columns:1.3fr .7fr; gap:32px; align-items:center; background:var(--action-bg); color:var(--action-ink); padding:30px; border-radius:var(--radius); }}
    .primary-action p {{ color:var(--action-support); }}
    .primary-action a {{ justify-self:end; display:inline-flex; align-items:center; min-height:48px; padding:10px 18px; background:#fff; color:#003F3A; text-decoration:none; border-radius:8px; font-weight:500; }}
    .alt {{ background:var(--surface); border-block:1px solid var(--line); }}
    .table-scroll {{ min-width:0; max-width:100%; overflow:auto; border:1px solid var(--line); border-radius:12px; background:var(--surface); }}
    table {{ width:100%; border-collapse:collapse; min-width:760px; font-variant-numeric:tabular-nums; }}
    caption {{ text-align:left; padding:14px 16px; color:var(--muted); font-size:.88rem; }}
    th,td {{ text-align:left; padding:13px 15px; border-top:1px solid var(--line); vertical-align:top; }}
    thead th {{ color:var(--muted); font-size:.89rem; text-transform:none; letter-spacing:0; background:var(--surface-2); border-top:0; }}
    tbody tr:hover {{ background:color-mix(in srgb,var(--garden) 8%,transparent); }}
    .tier {{ display:inline-flex; align-items:center; min-height:28px; padding:2px 9px; border:1px solid currentColor; border-radius:999px; font-size:.77rem; font-weight:500; white-space:nowrap; }}
    .tier-a,.tier-b {{ color:var(--brand-strong); }} .tier-c {{ color:var(--warm-text); }} .tier-d {{ color:var(--magenta); }}
    .scenario-note {{ margin-top:14px; color:var(--muted); font-size:.92rem; }}
    .filter-bar {{ display:flex; gap:8px; flex-wrap:wrap; margin:30px 0 14px; }}
    .filter-bar button {{ min-height:44px; padding:8px 15px; border:1px solid var(--garden); border-radius:8px; color:var(--ink); background:transparent; cursor:pointer; font-family:inherit; font-size:.9rem; font-weight:500; line-height:1.2; }}
    .filter-bar button:hover {{ background:var(--surface-2); }}
    .filter-bar button[aria-pressed="true"] {{ color:var(--action-ink); background:var(--action-bg); border-color:var(--action-bg); }}
    .filter-status {{ color:var(--muted); margin-bottom:30px; }}
    .candidate-list {{ display:grid; grid-template-columns:minmax(0,1fr); gap:28px; }}
    .candidate-card {{ min-width:0; background:var(--surface); border:1px solid var(--line); border-radius:var(--radius); padding:clamp(20px,4vw,38px); box-shadow:var(--shadow); }}
    .candidate-card[hidden], tr[hidden] {{ display:none!important; }}
    .candidate-heading {{ display:flex; justify-content:space-between; gap:22px; align-items:start; padding-bottom:22px; border-bottom:1px solid var(--line); }}
    .candidate-heading .rank {{ float:left; margin-right:14px; color:var(--magenta); font:500 2.2rem/1 "IBM Plex Sans Thai Looped",sans-serif; font-variant-numeric:tabular-nums; }}
    .candidate-status {{ max-width:320px; text-align:right; }}
    .candidate-status small {{ display:block; color:var(--muted); margin-top:7px; }}
    .candidate-metrics {{ display:grid; grid-template-columns:repeat(4,1fr); margin-top:24px; border-block:1px solid var(--line); }}
    .candidate-metrics > div {{ padding:18px 14px; border-right:1px solid var(--line); }}
    .candidate-metrics > div:last-child {{ border-right:0; }}
    .candidate-metrics strong {{ display:block; font:500 1.9rem/1 "IBM Plex Sans Thai Looped",sans-serif; color:var(--brand); font-variant-numeric:tabular-nums; }}
    .candidate-metrics span {{ color:var(--muted); font-size:.8rem; }}
    .metric-note {{ color:var(--muted); font-size:.83rem; margin:9px 0 0; }}
    .decision-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:0; margin:28px 0; border:1px solid var(--line); }}
    .decision-grid > div {{ padding:20px; border-right:1px solid var(--line); }}
    .decision-grid > div:last-child {{ border-right:0; }}
    .decision-grid p:last-child {{ margin-bottom:0; }}
    .map-layout {{ min-width:0; display:grid; grid-template-columns:minmax(0,.9fr) minmax(320px,1.1fr); gap:26px; align-items:start; }}
    .map-layout > *,.map-fallback {{ min-width:0; }}
    .overview-map {{ margin:0 0 24px; border:1px solid var(--line); background:var(--canvas); border-radius:12px; overflow:hidden; }}
    .overview-map svg {{ width:100%; max-height:460px; }}
    .overview-map figcaption {{ padding:13px 16px; color:var(--muted); font-size:.82rem; border-top:1px solid var(--line); }}
    .overview-axis {{ fill:none; stroke:var(--line); stroke-width:1; stroke-dasharray:3 5; }}
    .overview-hit {{ fill:transparent; stroke:none; }}
    .overview-dot {{ fill:var(--brand-strong); stroke:var(--surface); stroke-width:2.5; }}
    .overview-candidate text {{ fill:#fff; font:600 10px/1 sans-serif; text-anchor:middle; dominant-baseline:middle; pointer-events:none; }}
    html[data-theme="dark"] .overview-candidate text {{ fill:#1B2522; }}
    @media (prefers-color-scheme:dark) {{ html:not([data-theme]) .overview-candidate text {{ fill:#1B2522; }} }}
    .map-policy {{ display:grid; grid-template-columns:repeat(3,1fr); gap:1px; margin:-8px 0 28px; border:1px solid var(--line); background:var(--line); }}
    .map-policy p {{ margin:0; padding:16px; background:var(--surface); color:var(--muted); font-size:.88rem; }}
    .clean-map {{ margin:0; border:1px solid var(--line); background:var(--canvas); border-radius:12px; overflow:hidden; }}
    .clean-map svg {{ width:100%; aspect-ratio:420/320; }}
    .clean-map figcaption {{ padding:14px 16px; color:var(--muted); font-size:.82rem; border-top:1px solid var(--line); }}
    .analysis-extent {{ fill:color-mix(in srgb,var(--garden) 9%,transparent); stroke:var(--garden); stroke-width:1.5; stroke-dasharray:4 5; }}
    .candidate-center {{ fill:var(--brand-strong); stroke:var(--surface); stroke-width:2.5; }}
    .marker-hit {{ fill:transparent; stroke:none; }}
    .marker-shape {{ stroke:var(--surface); stroke-width:2.5; transition:transform .15s ease; transform-box:fill-box; transform-origin:center; }}
    .competitor-marker:hover .marker-shape,.competitor-marker:focus .marker-shape {{ transform:scale(1.12); }}
    .competitor-marker text {{ fill:var(--marker-text); font:600 10px/1 sans-serif; text-anchor:middle; dominant-baseline:middle; pointer-events:none; }}
    .competitor-marker.impact-high text {{ fill:var(--marker-text-high); }}
    .competitor-marker.impact-medium text {{ fill:var(--marker-text-garden); }}
    .competitor-marker.impact-high .marker-shape {{ fill:var(--magenta); }}
    .competitor-marker.impact-medium_high .marker-shape {{ fill:var(--warm); }}
    .competitor-marker.impact-medium .marker-shape {{ fill:var(--garden); }}
    .north path,.scale path {{ stroke:var(--muted); stroke-width:1.4; fill:none; }}
    .north text,.scale text {{ fill:var(--muted); font:500 10px/1 sans-serif; text-anchor:middle; }}
    .scale text {{ text-anchor:start; }}
    .map-fallback .table-scroll {{ max-height:360px; }}
    .map-fallback table {{ min-width:680px; font-size:.9rem; }}
    .map-fallback th,.map-fallback td {{ padding:10px 11px; }}
    .map-key {{ display:grid; place-items:center; width:24px; height:24px; border-radius:50%; color:var(--marker-text); font-weight:600; }}
    .map-key.impact-high {{ color:var(--marker-text-high); }}
    .map-key.impact-medium {{ color:var(--marker-text-garden); }}
    .map-key.impact-high {{ background:var(--magenta); }} .map-key.impact-medium_high {{ background:var(--warm); }} .map-key.impact-medium {{ background:var(--garden); }}
    .competitor-details {{ margin-top:10px; border-top:1px solid var(--line); }}
    details {{ border-bottom:1px solid var(--line); }}
    summary {{ list-style:none; cursor:pointer; min-height:52px; display:flex; align-items:center; gap:12px; justify-content:space-between; padding:11px 4px; }}
    summary::-webkit-details-marker {{ display:none; }}
    summary small {{ display:block; color:var(--muted); margin-top:2px; }}
    .chevron {{ width:9px; height:9px; border-right:1.5px solid currentColor; border-bottom:1.5px solid currentColor; transform:rotate(45deg); transition:transform .15s ease; margin:0 8px 5px 16px; flex:0 0 auto; }}
    details[open] > summary .chevron {{ transform:rotate(225deg); margin-bottom:-5px; }}
    .competitor-detail-body {{ padding:2px 12px 18px; font-size:.9rem; }}
    .competitor-detail.withheld summary {{ color:var(--muted); }}
    .guardrail {{ border-left:3px solid var(--magenta); padding-left:12px; color:var(--muted); }}
    .source-links {{ padding-left:20px; margin:10px 0 0; }}
    .source-links li {{ margin:6px 0; }}
    .source-links a {{ overflow-wrap:anywhere; }}
    .source-links span {{ display:block; color:var(--muted); font-size:.8rem; }}
    .gap-hypothesis {{ margin:26px 0 18px; padding:18px 20px; background:var(--surface-2); border-left:3px solid var(--garden); }}
    .gap-hypothesis small {{ color:var(--muted); }}
    .evidence-disclosure {{ border:1px solid var(--line); border-radius:10px; overflow:hidden; }}
    .evidence-disclosure > summary {{ padding:14px 16px; min-height:58px; background:var(--action-bg); color:var(--action-ink); }}
    .evidence-disclosure summary small {{ color:var(--action-support); }}
    .evidence-icon {{ width:22px; height:22px; border:1.5px solid currentColor; border-radius:4px; position:relative; flex:0 0 auto; }}
    .evidence-icon::after {{ content:""; position:absolute; left:5px; right:5px; top:6px; height:1px; background:currentColor; box-shadow:0 4px currentColor,0 8px currentColor; }}
    .evidence-body {{ display:grid; grid-template-columns:repeat(2,1fr); gap:18px; padding:20px; }}
    .evidence-body > div {{ padding-bottom:14px; border-bottom:1px solid var(--line); }}
    .sources {{ columns:2; gap:36px; padding-left:20px; }}
    .sources li {{ break-inside:avoid; margin:0 0 12px; overflow-wrap:anywhere; }}
    .sources span {{ display:block; color:var(--muted); font-size:.8rem; }}
    .sources.release-sources {{ margin-top:28px; }}
    footer {{ border-top:1px solid var(--line); padding:34px 0 48px; color:var(--muted); font-size:.86rem; }}
    .footer-inner {{ display:flex; justify-content:space-between; gap:24px; }}
    @media (max-width:900px) {{
      :root {{ --shell:min(100% - 28px,760px); }}
      .header-inner {{ min-height:64px; }} .brand img {{ width:105px; }}
      nav {{ position:absolute; top:64px; left:0; right:0; padding:0 14px; background:var(--canvas); border-bottom:1px solid var(--line); }}
      .hero {{ padding-top:96px; }} .hero-grid,.section-head,.map-layout {{ grid-template-columns:1fr; }}
      .hero-score {{ border-left:0; border-top:1px solid var(--line); padding:26px 0 0; }}
      .decision-strip,.candidate-metrics {{ grid-template-columns:repeat(2,1fr); }}
      .map-policy {{ grid-template-columns:1fr; }}
      .decision-strip > div:nth-child(2),.candidate-metrics > div:nth-child(2) {{ border-right:0; }}
      .decision-strip > div:nth-child(-n+2),.candidate-metrics > div:nth-child(-n+2) {{ border-bottom:1px solid var(--line); }}
      .primary-action {{ grid-template-columns:1fr; }} .primary-action a {{ justify-self:start; }}
      .decision-grid {{ grid-template-columns:1fr; }} .decision-grid > div {{ border-right:0; border-bottom:1px solid var(--line); }} .decision-grid > div:last-child {{ border-bottom:0; }}
    }}
    @media (max-width:580px) {{
      :root {{ --shell:calc(100% - 24px); }}
      section {{ padding:56px 0; }} h1 {{ font-size:2.67rem; }}
      .header-tools {{ gap:5px; }} .theme-cycle {{ width:44px;height:44px;flex-basis:44px; }}
      .candidate-card {{ padding:18px 14px; border-radius:13px; box-shadow:none; }}
      .candidate-heading {{ display:block; }} .candidate-status {{ text-align:left; margin-top:16px; }}
      .candidate-metrics {{ grid-template-columns:1fr 1fr; }}
      .candidate-metrics > div {{ padding:14px 10px; }}
      .candidate-metrics strong {{ font-size:1.55rem; }}
      .evidence-body {{ grid-template-columns:1fr; padding:16px; }}
      .sources {{ columns:1; }} .footer-inner {{ display:block; }}
      .clean-map figcaption {{ font-size:.78rem; }}
    }}
    @media (prefers-reduced-motion:reduce) {{
      html {{ scroll-behavior:auto; }} *,*::before,*::after {{ scroll-behavior:auto!important; transition:none!important; animation:none!important; }}
    }}
    @media print {{
      :root {{ --canvas:#fff; --surface:#fff; --surface-2:#f4f4f2; --ink:#111; --muted:#444; --line:#bbb; }}
      .site-header,.filter-bar,.filter-status,.primary-action a {{ display:none!important; }}
      section {{ padding:24px 0; }} .candidate-card {{ box-shadow:none; break-inside:avoid; margin-bottom:20px; }}
      details:not([open]) > :not(summary) {{ display:block!important; }}
      .map-layout,.section-head,.hero-grid {{ grid-template-columns:1fr 1fr; }}
      a {{ color:inherit; text-decoration:none; }} a[href^="http"]::after {{ content:" (" attr(href) ")"; font-size:8pt; overflow-wrap:anywhere; }}
    }}
  </style>
</head>
<body data-location-report data-report-id="parc-bangna-top10-release-1-6">
  <a class="skip-link" href="#main">ข้ามไปเนื้อหาหลัก</a>
  <header class="site-header">
    <div class="shell header-inner">
      <a class="brand" href="#top"><img id="brand-logo" src="{positive_logo}" data-logo-positive="{positive_logo}" data-logo-reverse="{reverse_logo}" alt="PARC Bangna"><span class="sr-only">กลับด้านบน</span></a>
      <div class="header-tools">
        <nav aria-label="สารบัญ">
          <a href="#decision">คำตัดสิน</a><a href="#comparison">Top 10</a><a href="#locations">รายทำเล</a><a href="#method">วิธีอ่าน</a>
          <a href="analysis/PARC_Bangna_Bangkok_Top_10_Release_1_6_Competition_Analysis_and_UXUI_2026-07-28.md">รายงาน .md</a>
        </nav>
        <button id="theme-cycle" class="theme-cycle" type="button" data-theme-mode="system" aria-label="ธีม: System">
          <svg data-mode-icon="system" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="4" width="18" height="13" rx="2"></rect><path d="M8 21h8M12 17v4"></path></svg>
          <svg data-mode-icon="light" viewBox="0 0 24 24" aria-hidden="true" hidden><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"></path></svg>
          <svg data-mode-icon="dark" viewBox="0 0 24 24" aria-hidden="true" hidden><path d="M20.5 14.6A8.5 8.5 0 019.4 3.5 8.5 8.5 0 1020.5 14.6z"></path></svg>
        </button>
        <span id="theme-status" class="sr-only" role="status" aria-live="polite"></span>
      </div>
    </div>
  </header>

  <main id="main" data-location-map data-map-manifest="analysis/map-manifest.json">
    <section class="hero" id="top">
      <div class="shell">
        <div class="hero-grid">
          <div>
            <p class="eyebrow">Venue Locale Insight · Release 1.6 · 28 ก.ค. 2026</p>
            <h1>อันดับฐานยังเดิม แต่คู่แข่งเปลี่ยนลำดับสิ่งที่ควรทำต่อ</h1>
            <p class="lede">Release 1.6 รักษาคะแนน Top 10 ของ Release 1.5 แล้วเพิ่ม competitive-supply overlay แยกต่างหาก ผลเบื้องต้นชี้ว่า <strong>บางปะกอก</strong> เป็นทำเลเดียวที่ได้ Tier A สำหรับการตรวจเชิงรุก ขณะที่ผู้นำเดิมเผชิญ supply pressure สูง</p>
            <div class="hero-facts"><span>10 analytical catchments</span><span>26.3154 km² เท่ากัน</span><span>23 operating venues ใน registry</span><span>ไม่มีถนน/รถไฟที่ lineage ไม่ครบ</span></div>
          </div>
          <div class="hero-score" data-recommendation-candidate="bang-pakok">
            <strong>Tier A</strong><span>บางปะกอก · field-validation priority</span>
            <p>ไม่ได้แปลว่าเป็น final investment winner แต่เป็นจุดเริ่มตรวจที่ competitive room และ evidence readiness สมดุลที่สุดใน overlay นี้</p>
          </div>
        </div>
        <div class="caveat" data-caveat-id="baseline-not-final-investment-rank" data-caveat-severity="decision-changing" data-caveat-visibility="inline">
          <strong>ข้อจำกัดที่เปลี่ยนคำตัดสินได้:</strong> competitor registry เป็น <em>minimum verified operating supply</em> ไม่ใช่ census ที่รับรองความครบ และระยะเป็นเส้นตรง ไม่คิดถนน สะพาน เรือ หรือ barrier จึงใช้ competition เพื่อกำหนด action tier ก่อน ยังไม่แทน canonical rank
        </div>
      </div>
    </section>

    <section id="decision">
      <div class="shell">
        <div class="section-head">
          <div><p class="eyebrow">คำตัดสินที่ใช้ได้ตอนนี้</p><h2>ย้าย effort จาก “ผู้นำคะแนน” ไปสู่ “ทำเลที่มีช่องว่างให้พิสูจน์”</h2></div>
          <p>คะแนนเดิมตอบว่าฐานคนและ concept fit อยู่ตรงไหน ส่วน overlay ใหม่ตอบว่าควรใช้เวลาและงบตรวจต่อที่ใด เมื่อ supply ที่เปิดอยู่ถูกนำมาพิจารณาอย่างมีขอบเขต</p>
        </div>
        <div class="decision-strip" role="group" aria-label="จำนวนทำเลในแต่ละ action tier">
          <div><strong>{action_counts["A"]}</strong><span>Tier A · ตรวจเชิงรุก</span></div>
          <div><strong>{action_counts["B"]}</strong><span>Tier B · มีช่องว่างแต่ต้องยืนยัน</span></div>
          <div><strong>{action_counts["C"]}</strong><span>Tier C · ต้องต่างชัด</span></div>
          <div><strong>{action_counts["D"]}</strong><span>Tier D · แข่งขันสูง</span></div>
        </div>
        <div class="primary-action" data-primary-cta data-owner="ทีมพัฒนาทำเล J Lifestyle Center" data-timing="ก่อน final parcel shortlist รอบถัดไป">
          <div><p class="eyebrow">Primary decision CTA</p><h3>อนุมัติ competitive field validation สำหรับบางปะกอก พร้อม network check ที่วังหลังและ coordinate check ที่ประชาอุทิศ</h3>
          <p>เจ้าของงาน: ทีมพัฒนาทำเล J Lifestyle Center · เวลาตัดสิน: ก่อน final parcel shortlist รอบถัดไป</p></div>
          <a href="#candidate-bang-pakok">เปิดหลักฐานบางปะกอก</a>
        </div>
      </div>
    </section>

    <section class="alt" id="comparison">
      <div class="shell">
        <div class="section-head">
          <div><p class="eyebrow">Top 10 + competition overlay</p><h2>คงอันดับฐาน เพื่อไม่ให้ข้อมูลคู่แข่งเบื้องต้นดูแม่นเกินจริง</h2></div>
          <p>Competitive room สูงหมายถึงมี headroom มากกว่าใน minimum verified set; ไม่ได้พิสูจน์ว่าคู่แข่งอ่อนแอ และไม่ใช่การวัดยอดขาย traffic occupancy หรือคุณภาพบริการ</p>
        </div>
        {overview_map()}
        <section class="table-scroll" tabindex="0" aria-label="ตาราง Top 10 และ competition overlay เลื่อนแนวนอนได้">
          <table id="top10-comparison-table"><caption>คะแนนฐาน 0–100 (สูงดีกว่า) และ competition overlay 0–100 (สูง = มี room มากกว่า)</caption>
            <thead><tr><th scope="col">#</th><th scope="col">ทำเล</th><th scope="col">คะแนนฐาน</th><th scope="col">Traffic</th><th scope="col">PMF</th><th scope="col">คู่แข่งยืนยัน</th><th scope="col">Competitive room*</th><th scope="col">Action</th></tr></thead>
            <tbody>{"".join(comparison_rows)}</tbody>
          </table>
        </section>
        <details>
          <summary><span><b>เปิด scenario 80/20</b><small>ภาพทดสอบ ไม่ใช่อันดับ canonical</small></span><span class="chevron" aria-hidden="true"></span></summary>
          <section class="table-scroll" tabindex="0" aria-label="ตาราง scenario 80 ต่อ 20 เลื่อนแนวนอนได้">
            <table><caption>80% คะแนนฐาน + 20% competitive room; ใช้ดูทิศทางเท่านั้น</caption>
              <thead><tr><th scope="col">ทำเล</th><th scope="col">อันดับฐาน</th><th scope="col">อันดับ scenario</th><th scope="col">คะแนน scenario</th></tr></thead>
              <tbody>{"".join(scenario_rows)}</tbody>
            </table>
          </section>
          <p class="scenario-note" data-caveat-id="scenario-is-not-canonical"
            data-caveat-severity="decision-changing" data-caveat-visibility="inline">
            ประชาอุทิศขึ้นอันดับ 1 ใน scenario แต่ยังเป็น Tier B เพราะพิกัด Market Place ใช้ tenant proxy และ evidence readiness ต่ำกว่าเกณฑ์ Tier A; scenario นี้ห้ามแทนอันดับหลัก
            และยังไวต่อน้ำหนักมาก—ประชาอุทิศแกว่งอันดับ 1–7 ส่วนวงเวียนใหญ่–ตะวันออกแกว่งอันดับ 2–7 ใน sensitivity test
          </p>
        </details>
      </div>
    </section>

    <section id="locations">
      <div class="shell">
        <div class="section-head">
          <div><p class="eyebrow">คำตัดสินและแผนที่รายทำเล</p><h2>แผนที่แสดงเท่าที่ตรวจสอบย้อนกลับได้</h2></div>
          <p>แต่ละแผนที่มีเพียง analytical extent, candidate center, คู่แข่งที่พิกัด confidence สูง, ทิศเหนือ และ scale bar ไม่มีถนน รถไฟ สถานี หรือ landmark ที่ยังไม่มี feature-level source ledger. ขนาด marker เป็น visual cue ที่เปิดเผยฐานรายจุดและอาจมาจาก metric ต่างชนิด—ไม่ใช่ GLA scale เดียวกันทั้งแผนที่</p>
        </div>
        <div class="map-policy">
          <p data-caveat-id="strategic-gaps-are-hypotheses" data-caveat-severity="material"
            data-caveat-visibility="evidence"><strong>Strategic gaps เป็นสมมติฐาน:</strong> ยังไม่มีหลักฐานรองรับการกล่าวว่าคู่แข่งรายใด traffic, occupancy, service, tenant mix หรือ performance อ่อน</p>
          <p data-caveat-id="two-host-centroids-withheld" data-caveat-severity="material"
            data-caveat-visibility="evidence"><strong>กัน 2 จุดออกจากแผนที่:</strong> Market Place Pracha Uthit และ Esplanade Ratchada อยู่ในตารางวิเคราะห์ แต่ไม่วาดจนกว่าจะยืนยัน host centroid</p>
          <p data-caveat-id="roads-rail-stations-omitted" data-caveat-severity="context"
            data-caveat-visibility="evidence"><strong>ไม่แสดงถนน/ราง/สถานี:</strong> Release นี้ยังไม่มี feature-level lineage และ snapshot สถานะการใช้งานที่ตรวจซ้ำได้</p>
        </div>
        <div class="filter-bar" role="group" aria-label="กรองทำเลตาม action tier">
          <button type="button" data-filter="all" aria-pressed="true">ทุกทำเล</button>
          <button type="button" data-filter="opportunity" aria-pressed="false">Tier A–B · มีช่องว่าง</button>
          <button type="button" data-filter="differentiate" aria-pressed="false">Tier C · ต้องต่างชัด</button>
          <button type="button" data-filter="highpressure" aria-pressed="false">Tier D · แข่งขันสูง</button>
        </div>
        <p class="filter-status" role="status" aria-live="polite">แสดง 10 จาก 10 ทำเล</p>
        <div class="candidate-list">{"".join(cards)}</div>
      </div>
    </section>

    <section class="alt" id="method">
      <div class="shell">
        <div class="section-head">
          <div><p class="eyebrow">วิธีอ่านและ evidence boundary</p><h2>คู่แข่งเปลี่ยน action tier ไม่เปลี่ยนข้อเท็จจริงของพื้นที่</h2></div>
          <div class="section-copy">
            <p><strong>Supply pressure</strong> ใช้ impact class × routine overlap × proximity แล้ว deduplicate ศูนย์ที่เป็น parent cluster เดียวกัน</p>
            <p><strong>Competitive room</strong> = 70% supply headroom + 30% strategic-gap potential โดย gap เป็นสมมติฐานเสมอ</p>
            <p><strong>Marker size</strong> ใช้พื้นที่ให้เช่าที่ operator รายงานก่อน; รองลงมาเป็น project/commercial area หรือ brand/shop count ที่ระบุชนิด; ถ้าไม่มีจึงใช้ impact class ไม่สร้าง GLA หรือ tenant count แทน</p>
          </div>
        </div>
        <div class="caveat" data-caveat-id="medoid-and-fixed-circle-limit" data-caveat-severity="decision-changing" data-caveat-visibility="inline">
          <strong>Candidate center ไม่ใช่แปลงลงทุน:</strong> เป็น restaurant-sample medoid จาก Release 1.5 และวงกลม 2.89421 km เป็นหน่วยเปรียบเทียบทางวิเคราะห์ ไม่ใช่ source polygon, legal boundary, parcel หรือ drive-time catchment.
        </div>
        <details>
          <summary><span><b>เปิด source register ภายนอก</b><small>operator, venue และหน่วยงานที่รองรับตัวตน/สถานะ/metrics</small></span><span class="chevron" aria-hidden="true"></span></summary>
          <ul class="sources">{"".join(source_cards)}</ul>
        </details>
        <ul class="sources release-sources">
          <li data-source-id="release-15-baseline"><a href="https://github.com/montri-th/top10locations-like-parcbn/blob/563146f6b8f57d25652cea9f60acb6ee9239a054/index.html">Release 1.5 immutable source</a><span>canonical rank และ score baseline</span></li>
          <li data-source-id="release-16-canonical-screening"><span>Venue Locale Insight v2.3.1 · canonical comparable-catchment output</span></li>
          <li data-source-id="release-16-competitor-registry"><span>Competitive supply registry v0.1.0-preliminary · evidence cutoff 2026-07-28</span></li>
          <li data-source-id="release-16-competition-overlay"><span>Competition pressure, room, evidence readiness และ action tier</span></li>
          <li data-source-id="release-16-scenario"><span>Illustrative noncanonical 80/20 sensitivity scenario</span></li>
          <li data-source-id="map-contract-v1"><span>Evidence-grounded location-map contract v1.0</span></li>
        </ul>
      </div>
    </section>
  </main>

  <footer>
    <div class="shell footer-inner">
      <span>Release 1.6 competition diagnostic · 28 ก.ค. 2026</span>
      <span>J Lifestyle Center Design System v0.3 · transparent logo derivative ตามคำสั่ง Release 1.6</span>
    </div>
  </footer>

  <script>
  (() => {{
    const media = matchMedia("(prefers-color-scheme: dark)");
    const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
    const button = document.getElementById("theme-cycle");
    const status = document.getElementById("theme-status");
    const logo = document.getElementById("brand-logo");
    const meta = document.querySelector('meta[name="theme-color"]');
    let state = window.__parcThemeBoot || {{mode:"system", step:0}};

    function resolvedTheme(current=state) {{
      return current.mode === "system" ? (media.matches ? "dark" : "light") : current.mode;
    }}
    function nextThemeState(current, osDark) {{
      if (current.mode === "system") return {{mode: osDark ? "light" : "dark", step:1}};
      if (current.step === 1) return {{mode: current.mode === "light" ? "dark" : "light", step:2}};
      return {{mode:"system", step:0}};
    }}
    window.__themeCycleTest = {{nextThemeState}};
    function persist() {{
      try {{
        localStorage.removeItem("parc-screening-theme");
        if (state.mode === "system") localStorage.removeItem("parc-theme-cycle-v1");
        else localStorage.setItem("parc-theme-cycle-v1", JSON.stringify(state));
      }} catch (_) {{}}
    }}
    function modeName(mode) {{ return mode === "system" ? "System" : mode === "light" ? "Light" : "Dark"; }}
    function render(announce=false) {{
      if (state.mode === "system") delete document.documentElement.dataset.theme;
      else document.documentElement.dataset.theme = state.mode;
      const resolved = resolvedTheme();
      button.dataset.themeMode = state.mode;
      button.dataset.resolvedTheme = resolved;
      button.querySelectorAll("[data-mode-icon]").forEach(icon => {{
        icon.toggleAttribute("hidden", icon.dataset.modeIcon !== state.mode);
      }});
      logo.src = resolved === "dark" ? logo.dataset.logoReverse : logo.dataset.logoPositive;
      meta.content = resolved === "dark" ? "#1B2522" : "#F7F2E9";
      const next = nextThemeState(state, media.matches);
      const currentText = state.mode === "system" ? `System (อุปกรณ์แสดงผล${{resolved === "dark" ? "มืด" : "สว่าง"}})` : modeName(state.mode);
      const label = `ธีม: ${{currentText}}. กดเพื่อใช้ ${{modeName(next.mode)}}`;
      button.setAttribute("aria-label", label);
      button.title = label;
      if (announce) status.textContent = `เปลี่ยนเป็นธีม ${{currentText}}`;
    }}
    button.addEventListener("click", () => {{
      state = nextThemeState(state, media.matches);
      persist();
      render(true);
    }});
    const onSystemChange = () => {{ if (state.mode === "system") render(true); }};
    if (media.addEventListener) media.addEventListener("change", onSystemChange);
    else media.addListener(onSystemChange);
    render(false);

    const filterButtons = [...document.querySelectorAll("[data-filter]")];
    const cards = [...document.querySelectorAll(".candidate-card")];
    const rows = [...document.querySelectorAll("#comparison tbody tr[data-action-group]")];
    const filterStatus = document.querySelector(".filter-status");
    filterButtons.forEach(filterButton => filterButton.addEventListener("click", () => {{
      const selected = filterButton.dataset.filter;
      filterButtons.forEach(item => item.setAttribute("aria-pressed", String(item === filterButton)));
      let visible = 0;
      cards.forEach(card => {{
        const show = selected === "all" || card.dataset.actionGroup === selected;
        card.hidden = !show;
        if (show) visible++;
      }});
      rows.forEach(row => row.hidden = !(selected === "all" || row.dataset.actionGroup === selected));
      filterStatus.textContent = `แสดง ${{visible}} จาก ${{cards.length}} ทำเล`;
    }}));

    let lastDetailTrigger = null;
    document.querySelectorAll(".competitor-marker, .map-fallback a[href^='#competitor-']").forEach(link => {{
      link.addEventListener("click", event => {{
        const target = document.querySelector(link.getAttribute("href"));
        if (!(target instanceof HTMLDetailsElement)) return;
        event.preventDefault();
        lastDetailTrigger = link;
        target.open = true;
        target.scrollIntoView({{behavior: reducedMotion.matches ? "auto" : "smooth", block:"center"}});
        target.querySelector("summary")?.focus({{preventScroll:true}});
        history.replaceState(null, "", link.getAttribute("href"));
      }});
    }});
    document.addEventListener("keydown", event => {{
      if (event.key !== "Escape") return;
      const details = document.activeElement?.closest?.("details.competitor-detail");
      if (!details?.open) return;
      details.open = false;
      lastDetailTrigger?.focus({{preventScroll:true}});
    }});

    let printOpen = [];
    addEventListener("beforeprint", () => {{
      printOpen = [...document.querySelectorAll("details")].filter(item => item.open);
      document.querySelectorAll("details").forEach(item => item.open = true);
      logo.src = logo.dataset.logoPositive;
    }});
    addEventListener("afterprint", () => {{
      document.querySelectorAll("details").forEach(item => item.open = printOpen.includes(item));
      render(false);
    }});
  }})();
  </script>
</body>
</html>
"""

clean_html = "\n".join(line.rstrip() for line in html_doc.splitlines()) + "\n"
OUT.write_text(clean_html, encoding="utf-8")
print(OUT)
