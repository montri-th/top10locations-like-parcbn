#!/usr/bin/env python3
"""Static integrity and analytical checks for the v3.5 proxy addendum."""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "PARC_Bangna_Fresh_Locale_Screen_Board_Decision_Tool_v3.4_2026-07-31.html"
OUTPUT = ROOT / "PARC_Bangna_Fresh_Locale_Screen_Board_Decision_Tool_v3.5_PARC_Core_Fit_Preview_2026-08-01.html"
INDEX = ROOT / "index.html"
DATA = ROOT / "analysis/parc-host-proxy-core-fit-preview-v0.1.json"


def extract_script(document: str, script_id: str) -> str:
    match = re.search(
        rf'<script type="application/json" id="{re.escape(script_id)}">(.*?)</script>',
        document,
        re.S,
    )
    if not match:
        raise AssertionError(f"missing JSON script: {script_id}")
    return match.group(1).replace("<\\/", "</")


def close(actual: float, expected: float, tolerance: float = 0.015) -> None:
    if not math.isclose(actual, expected, abs_tol=tolerance):
        raise AssertionError(f"{actual} != {expected} within {tolerance}")


source = SOURCE.read_text(encoding="utf-8")
output = OUTPUT.read_text(encoding="utf-8")
index = INDEX.read_text(encoding="utf-8")
data = json.loads(DATA.read_text(encoding="utf-8"))

assert output == index, "index.html differs from named v3.5 checkpoint"
assert hashlib.sha256(output.encode()).hexdigest() == hashlib.sha256(index.encode()).hexdigest()
assert output.rstrip().endswith("</html>"), "document is truncated"

source_report_data = extract_script(source, "report-data")
output_report_data = extract_script(output, "report-data")
assert source_report_data == output_report_data, "v3.3 report-data bytes changed"
payload = json.loads(output_report_data)
assert payload["release"]["id"] == "parc-fresh-vli-multilens-v3.3"
assert len(payload["portfolio"]) == 10
assert len(payload["scenarios"]) == 13

embedded = json.loads(extract_script(output, "parc-core-fit-data"))
assert embedded == data, "embedded preview data differs from its source JSON"
assert data["source"]["candidate_percentile_universe"] == 745
assert data["source"]["comparable_rank_lane"] == 574
assert data["source"]["challenger_lane"] == 171
assert data["source"]["excluded_parc_context_locales"] == 22

reference = data["reference"]
rows = data["top_10_core_fit_before_route_site_and_economics_gates"]
assert reference["candidate_eligible"] is False
assert reference["ranked"] is False
assert reference["locale_id"] not in {row["locale_id"] for row in rows}
assert len(rows) == 10
assert len({row["locale_id"] for row in rows}) == 10
assert [row["rank"] for row in rows] == list(range(1, 11))
assert set(reference["unsupported_scores"]) == {
    "barrier_access",
    "competition_pressure",
    "low_supply_signal",
    "balanced",
    "stability",
}

allowed_archetypes = {
    "residential_general",
    "market_residential",
    "school_led_residential",
    "condo_delivery",
    "hospital_adjacent",
}
proxy_scores = reference["scores_out_of_sample_against_frozen_745"]
rp = proxy_scores["resident"]
bp = proxy_scores["routine_breadth"]
ap = proxy_scores["activity"]
close(rp, 57.6969, 0.0001)
close(bp, 96.1192, 0.0001)
close(ap, 92.2148, 0.0001)
close(proxy_scores["accessible_routine"], 0.65 * bp + 0.35 * ap, 0.0001)
close(
    proxy_scores["fresh_core_opportunity"],
    0.55 * rp + 0.25 * bp + 0.20 * ap,
    0.0001,
)
components = reference["component_percentiles_out_of_sample_against_frozen_745"]
close(
    components["institution"],
    0.65 * components["office_area"] + 0.35 * components["students"],
    0.0001,
)
close(
    bp,
    0.55 * components["grocery_sales_area"] + 0.45 * components["institution"],
    0.0001,
)
previous_decision = float("inf")
for row in rows:
    assert row["peer_archetype"] in allowed_archetypes
    for key in ("resident", "routine_breadth", "activity", "similarity", "opportunity", "decision_score"):
        assert 0 <= row[key] <= 100, f"{row['locale_name_th']} {key} outside 0..100"
    expected_similarity = 100 - (
        0.55 * abs(row["resident"] - rp)
        + 0.25 * abs(row["routine_breadth"] - bp)
        + 0.20 * abs(row["activity"] - ap)
    )
    expected_opportunity = (
        0.55 * row["resident"]
        + 0.25 * row["routine_breadth"]
        + 0.20 * row["activity"]
    )
    expected_decision = 2 * expected_similarity * expected_opportunity / (
        expected_similarity + expected_opportunity
    )
    expected_h40 = 1 / (0.40 / expected_similarity + 0.60 / expected_opportunity)
    expected_h60 = 1 / (0.60 / expected_similarity + 0.40 / expected_opportunity)
    close(row["similarity"], expected_similarity)
    close(row["opportunity"], expected_opportunity)
    close(row["decision_score"], expected_decision)
    close(row["accessible_routine"], 0.65 * row["routine_breadth"] + 0.35 * row["activity"])
    close(row["harmonic_40"], expected_h40)
    close(row["harmonic_60"], expected_h60)
    assert row["decision_score"] <= previous_decision + 1e-9
    previous_decision = row["decision_score"]
    low, high = row["rank_range_40_50_60"]
    assert 1 <= low <= high <= 574
    assert row["ranks_40_50_60"][1] == row["rank"]
    assert [low, high] == [min(row["ranks_40_50_60"]), max(row["ranks_40_50_60"])]

assert [row["locale_name_th"] for row in rows] == [
    "เอกมัย-ใต้",
    "วังหิน-ใต้",
    "สัมมากร",
    "พระราม 3-ตะวันออก",
    "บางรัก",
    "คลองจั่น",
    "เจริญราษฎร์",
    "อารีย์",
    "เย็นอากาศ",
    "สำเหร่",
]
assert data["decision_readout"]["advance_to_route_site_gate"] == [
    "เอกมัย-ใต้",
    "วังหิน-ใต้",
    "สัมมากร",
    "พระราม 3-ตะวันออก",
]

assert 'data-interface-release="v3.5-parc-core-fit-preview"' in output
assert 'data-benchmark-release="parc-host-proxy-core-fit-preview-v0.1"' in output
assert 'data-benchmark-status="proxy-partial"' in output
assert output.count('data-core-fit-locale="') == 10
assert 'id="parc-fit"' in output
assert "ไม่ใช่คะแนนตัวศูนย์" in output
assert "ยังไม่มี exact PARC benchmark" in output
assert "Proxy ไม่เข้าร่วม slider" in output
assert "คะแนนจัดคิว" in output
assert "ขอบเขตที่ยังไม่ใช่ PARC benchmark" in output
assert ".proxy-section{scroll-margin-top:0;" in output
assert 'html[data-theme="dark"] .proxy-reference .status-pill{background:#7a2048;color:#fff}' in output
assert "อันดับฐาน /745" not in output
assert "อันดับเทียบ 745" not in output
assert "อันดับฐาน /574" in output
assert "อันดับเทียบ 574" in output

print("v3.5 QA passed")
print(f"  bytes: {len(output.encode('utf-8')):,}")
print(f"  sha256: {hashlib.sha256(output.encode()).hexdigest()}")
print("  immutable report-data: pass")
print("  preview formulas: pass")
print("  745 score base / 574 rank lane: pass")
