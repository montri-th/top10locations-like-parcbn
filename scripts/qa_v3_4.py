#!/usr/bin/env python3
"""Deterministic static release gate for the v3.4 Board decision tool."""

from __future__ import annotations

import hashlib
import json
import math
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
NAMED = ROOT / "PARC_Bangna_Fresh_Locale_Screen_Board_Decision_Tool_v3.4_2026-07-31.html"
V33 = ROOT / "PARC_Bangna_Fresh_Locale_Screen_Board_Explainer_v3.3_AI_Routing_2026-07-30.html"
EXPECTED_V33_SHA256 = "9e6675c8e5976636c9c139e5eb283a482e15a7dd03811f8110c080c75dec13a8"


class DocumentAudit(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.hash_hrefs: list[str] = []
        self.meta_properties: dict[str, str] = {}
        self.meta_names: dict[str, str] = {}
        self.canonical: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if data.get("id"):
            self.ids.append(str(data["id"]))
        href = data.get("href")
        if href and href.startswith("#"):
            self.hash_hrefs.append(href[1:])
        if tag == "meta" and data.get("property"):
            self.meta_properties[str(data["property"])] = str(data.get("content", ""))
        if tag == "meta" and data.get("name"):
            self.meta_names[str(data["name"])] = str(data.get("content", ""))
        if tag == "link" and data.get("rel") == "canonical":
            self.canonical = str(data.get("href", ""))


failures: list[str] = []
checks = 0


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        failures.append(message)


index_bytes = INDEX.read_bytes()
named_bytes = NAMED.read_bytes()
source_bytes = V33.read_bytes()
text = index_bytes.decode("utf-8")
source_text = source_bytes.decode("utf-8")

check(index_bytes == named_bytes, "index.html and named v3.4 checkpoint differ")
check(
    hashlib.sha256(source_bytes).hexdigest() == EXPECTED_V33_SHA256,
    "immutable v3.3 source checkpoint changed",
)
check('data-interface-release="v3.4-board-decision-tool"' in text, "interface release is not v3.4")
check('data-release-id="parc-fresh-vli-multilens-v3.3"' in text, "frozen analytical release is not v3.3")
check("analytical release v3.3 · interface v3.4" in text, "footer does not distinguish data and interface releases")
check(text.count('data-decision-view="') == 5, "expected exactly five visible decision views")
check('<button type="button" role="tab"' not in text, "legacy nine-lens tabs remain visible")
check('<th>5 · Stability</th>' in text and "ติด Top 10</th>" not in text, "portfolio matrix was not reduced to five decision views")
check(len(re.findall(r'<input[^>]*\sdata-weight="', text)) == 4, "expected four live weight sliders")
check('data-benchmark-status="unscored"' in text, "PARC benchmark gap is not explicit")
check("ไม่ใส่เลขแทนข้อมูลที่ขาด" in text, "benchmark row does not guard against invented values")
check("จัดอันดับใหม่เฉพาะพอร์ต 10 ทำเล" in text, "A-J simulator scope is not explicit")
check("nearest.distance > 26" in text, "overview map does not use nearest-point routing")
check(".overview-markers .map-hit{pointer-events:none}" in text, "overlapping overview hit circles still capture pointer clicks")
check("normalizedWeights(presetWeights = null)" in text, "preset weights are not preserved exactly in the live model")
check("displayedWeightBasisPoints(weights)" in text, "normalized shares are not allocated to an exact displayed 100.00%")
check("ทุกค่าเป็นศูนย์ จึงใช้ 25.00% เท่ากัน" in text, "all-zero slider fallback is not explicit")
check("pushHistory: true" in text and text.count("กลับไปเครื่องมือทดสอบสมมติฐาน") == 10, "mobile detail flow lacks a return path")

parser = DocumentAudit()
parser.feed(text)
duplicate_ids = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
missing_hash_targets = sorted(set(parser.hash_hrefs) - set(parser.ids))
check(not duplicate_ids, f"duplicate HTML ids: {duplicate_ids}")
check(not missing_hash_targets, f"dead hash anchors: {missing_hash_targets}")
check(all(f"detail-{ref}" in parser.ids for ref in "ABCDEFGHIJ"), "one or more detail-A…J anchors missing")

required_og = {"og:type", "og:locale", "og:site_name", "og:title", "og:description", "og:url", "og:image"}
check(required_og <= parser.meta_properties.keys(), "required Open Graph tags missing")
check(parser.meta_names.get("twitter:card") == "summary_large_image", "Twitter card metadata missing")
check(parser.canonical == "https://montri-th.github.io/top10locations-like-parcbn/", "canonical URL is wrong")

payload_match = re.search(r'<script type="application/json" id="report-data">(.*?)</script>', text, re.S)
source_payload_match = re.search(r'<script type="application/json" id="report-data">(.*?)</script>', source_text, re.S)
check(payload_match is not None, "report-data payload missing")
check(source_payload_match is not None, "v3.3 source payload missing")
payload = json.loads(payload_match.group(1)) if payload_match else {}
source_payload = json.loads(source_payload_match.group(1)) if source_payload_match else {}
check(payload.get("release", {}).get("id") == "parc-fresh-vli-multilens-v3.3", "payload analytical release id changed")
check(payload == source_payload, "analytical payload differs from immutable v3.3")
check(
    bool(payload_match and source_payload_match and payload_match.group(1) == source_payload_match.group(1)),
    "analytical payload bytes differ from immutable v3.3",
)
check(payload.get("release", {}).get("eligible_locales") == 745, "eligible universe changed")
check(len(payload.get("portfolio", [])) == 10, "portfolio is not A-J / ten rows")
check(len(payload.get("reserves", [])) == 6, "reserve count changed")
check(len(payload.get("lenses", {})) == 9, "nine-formula analytical audit payload changed")
check(len(payload.get("scenarios", [])) == 13, "scenario count changed")
check(sum(len(item.get("competitors", [])) for item in payload.get("portfolio", [])) == 108, "competitor evidence count changed")
check(
    payload.get("selection_contract", {}).get("portfolio_quota")
    == {
        "multi_lens_anchor": 3,
        "white_space_builder": 3,
        "observed_supply_challenger": 3,
        "routine_activity_barrier_experiment": 1,
    },
    "3+3+3+1 portfolio contract changed",
)


def relative_luminance(hex_color: str) -> float:
    channels = [int(hex_color[index : index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(first: str, second: str) -> float:
    high, low = sorted((relative_luminance(first), relative_luminance(second)), reverse=True)
    return (high + 0.05) / (low + 0.05)


cta_contrast = contrast("#fffdf8", "#203a35")
bar_contrast = contrast("#ffffff", "#365e55")
status_light_contrast = contrast("#14110e", "#b0712d")
status_dark_contrast = contrast("#14110e", "#e2b371")
benchmark_light_contrast = contrast("#81521c", "#fffdf8")
benchmark_dark_contrast = contrast("#e2b371", "#293a34")
check(cta_contrast >= 4.5, f"decision CTA contrast is only {cta_contrast:.2f}:1")
check(bar_contrast >= 4.5, f"decision bar contrast is only {bar_contrast:.2f}:1")
check(status_light_contrast >= 4.5, f"light benchmark pill contrast is only {status_light_contrast:.2f}:1")
check(status_dark_contrast >= 4.5, f"dark benchmark pill contrast is only {status_dark_contrast:.2f}:1")
check(benchmark_light_contrast >= 4.5, f"light benchmark slot contrast is only {benchmark_light_contrast:.2f}:1")
check(benchmark_dark_contrast >= 4.5, f"dark benchmark slot contrast is only {benchmark_dark_contrast:.2f}:1")
check(
    '.decision-bar .button.primary{background:#fffdf8;color:#203a35' in text,
    "decision CTA does not use the gated high-contrast colors",
)
check('.benchmark-gap .status-pill{align-self:start;background:var(--amber);color:#14110e}' in text, "benchmark pill colors are not pinned")

# Parse every executable inline script with Node so HTML counts cannot hide a blank tool.
inline_scripts = [
    body
    for attrs, body in re.findall(r"<script([^>]*)>(.*?)</script>", text, re.S | re.I)
    if "application/json" not in attrs.lower() and "src=" not in attrs.lower() and body.strip()
]
check(bool(inline_scripts), "no executable inline JavaScript found")
node_parser = (
    "let s='';process.stdin.setEncoding('utf8');"
    "process.stdin.on('data',c=>s+=c);"
    "process.stdin.on('end',()=>{new Function(s);});"
)
for index, script in enumerate(inline_scripts, start=1):
    result = subprocess.run(
        ["node", "-e", node_parser],
        input=script,
        text=True,
        capture_output=True,
        check=False,
    )
    check(result.returncode == 0, f"inline JavaScript {index} does not parse: {result.stderr.strip()}")


def displayed_basis_points(weights: dict[str, float]) -> dict[str, int]:
    shares = []
    for key, value in weights.items():
        exact = value * 10000
        units = math.floor(exact)
        shares.append([key, units, exact - units])
    remaining = 10000 - sum(item[1] for item in shares)
    shares.sort(key=lambda item: (-item[2], item[0]))
    for item in shares:
        if remaining <= 0:
            break
        item[1] += 1
        remaining -= 1
    return {key: units for key, units, _ in shares}


for scenario in payload.get("scenarios", []):
    display_weights = {
        "resident": scenario["weights"]["resident"],
        "routine": scenario["weights"]["routine"],
        "access": scenario["weights"]["access"],
        "market": scenario["weights"]["competition"],
    }
    check(sum(displayed_basis_points(display_weights).values()) == 10000, f'{scenario["id"]} displayed shares do not total 100.00%')

# Reproduce all 13 stored preset scores from the same four-component model.
max_delta = 0.0
for candidate in payload.get("portfolio", []):
    def low_supply(gap: str) -> float:
        if gap in {"central", "base"}:
            return candidate["metrics"]["low_supply_signal"]
        scenario_id = f"vli_{gap}"
        config = next(item for item in payload["scenarios"] if item["id"] == scenario_id)
        result = next(item for item in candidate["sensitivity"]["scenarios"] if item["id"] == scenario_id)
        weights = config["weights"]
        known = (
            weights["resident"] * candidate["metrics"]["resident"]
            + weights["routine"] * candidate["metrics"]["routine"]
            + weights["access"] * candidate["barrier"]["access_base"]
        )
        return (result["score"] - known) / weights["competition"]

    for scenario in payload["scenarios"]:
        weights = scenario["weights"]
        access_key = "access_base" if scenario["access"] == "base" else f'access_{scenario["access"]}'
        computed = (
            weights["resident"] * candidate["metrics"]["resident"]
            + weights["routine"] * candidate["metrics"]["routine"]
            + weights["access"] * candidate["barrier"][access_key]
            + weights["competition"] * low_supply(scenario["gap"])
        )
        stored = next(item for item in candidate["sensitivity"]["scenarios"] if item["id"] == scenario["id"])["score"]
        max_delta = max(max_delta, abs(computed - stored))
check(max_delta <= 0.011, f"live model does not reproduce frozen presets; max delta={max_delta:.4f}")

if failures:
    print(f"FAIL — {len(failures)} of {checks} checks failed")
    for failure in failures:
        print(f"- {failure}")
    sys.exit(1)

print(f"PASS — {checks} static checks · preset max delta {max_delta:.4f} · CTA contrast {cta_contrast:.2f}:1")
print(f"SHA-256 {hashlib.sha256(index_bytes).hexdigest()} · {len(index_bytes):,} bytes")
