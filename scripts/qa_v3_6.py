#!/usr/bin/env python3
"""Deterministic release gate for the v3.6 executive-story interface."""

from __future__ import annotations

import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "PARC_Bangna_Fresh_Locale_Screen_Board_Decision_Tool_v3.5_PARC_Core_Fit_Preview_2026-08-01.html"
OUTPUT = ROOT / "PARC_Bangna_Fresh_Locale_Screen_Board_Decision_Tool_v3.6_Executive_Story_2026-08-03.html"
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


class DocumentAudit(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.hash_links: list[str] = []
        self.text: list[str] = []
        self.suppressed = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(str(values["id"]))
        href = values.get("href")
        if href and href.startswith("#") and len(href) > 1:
            self.hash_links.append(href[1:])
        if tag in {"script", "style"}:
            self.suppressed += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self.suppressed:
            self.suppressed -= 1

    def handle_data(self, data: str) -> None:
        if not self.suppressed:
            clean = " ".join(data.split())
            if clean:
                self.text.append(clean)


source = SOURCE.read_text(encoding="utf-8")
output = OUTPUT.read_text(encoding="utf-8")
index = INDEX.read_text(encoding="utf-8")
data = json.loads(DATA.read_text(encoding="utf-8"))

assert output == index, "index.html differs from the named v3.6 checkpoint"
assert output.rstrip().endswith("</html>"), "document is truncated"
assert hashlib.sha256(output.encode()).hexdigest() == hashlib.sha256(index.encode()).hexdigest()

# v3.6 is an interface/story release only.
assert extract_script(source, "report-data") == extract_script(output, "report-data"), "v3.3 payload changed"
assert extract_script(source, "parc-core-fit-data") == extract_script(output, "parc-core-fit-data"), "reference analysis changed"
assert json.loads(extract_script(output, "parc-core-fit-data")) == data

parser = DocumentAudit()
parser.feed(output)
ids = set(parser.ids)
assert len(ids) == len(parser.ids), "duplicate element IDs found"
dead = sorted({target for target in parser.hash_links if target not in ids})
assert not dead, f"dead hash anchors: {dead}"
visible = " ".join(parser.text)

assert 'data-interface-release="v3.6-executive-story"' in output
assert 'data-benchmark-release="parc-host-proxy-core-fit-preview-v0.1"' in output
assert "ถ้าจะสร้าง PARC แห่งถัดไป" in visible
assert "4 ทำเลที่ควรศึกษาความเป็นไปได้ต่อ" in visible
assert "ศึกษาความเป็นไปได้ของ 4 ทำเลที่เสนอรอบนี้" in visible
assert "ตัวเลขช่วยบอกว่าย่านไหนมีรูปแบบคล้ายกัน แต่ยังไม่บอกว่าเปิด PARC แล้วจะสำเร็จ" in visible
assert "ยังไม่ใช่อนุมัติซื้อที่ดินหรือเริ่มลงทุน" in visible
assert "A–J คือพอร์ตคัดกรองรอบก่อน ไม่ใช่คำขออนุมัติรอบนี้" in visible
assert visible.count("เรายังไม่มีคะแนนของ PARC Bangna ที่วัดด้วยขอบเขตเดียวกัน จึงไม่ใช้ PARC เป็นเส้นเทียบในสี่คำถามนี้") == 1
assert "10 ย่านที่ได้คะแนนคัดกรองสูงสุด · 4 ทำเลแรกคือชุดที่เสนอให้ศึกษาต่อ" in visible
assert "ชุดน้ำหนัก A–J เดิม 13" in visible
assert "ราคาประเมินระดับย่าน" in visible
assert "รูปแบบย่านคล้ายศรีเอี่ยม" in visible
assert '<p class="benchmark-slot">' not in output

for name in ["เอกมัย-ใต้", "วังหิน-ใต้", "สัมมากร", "พระราม 3-ตะวันออก"]:
    assert name in visible
assert data["decision_readout"]["advance_to_route_site_gate"] == [
    "เอกมัย-ใต้",
    "วังหิน-ใต้",
    "สัมมากร",
    "พระราม 3-ตะวันออก",
]

for forbidden in [
    "ศึกษาต่อ 10 ทำเล A–J",
    "PARC core-fit",
    "Top 10 PARC core-fit",
    "host-locale proxy",
    "exact PARC benchmark",
    "Central leader",
    "Opportunity-led",
    "สิ่งที่ Board จะได้กลับมา",
    "มีศูนย์เดิมหลายราย ต้องเช็กทั้ง demand",
    "2 · Routine",
    "3 · Barrier-resilient",
    "4 · Market position",
    "5 · Stability",
    "PARC Bangna · reference",
    "คะแนน · อันดับเทียบ 574 ของแต่ละ preset",
    "Supply ใกล้ยังบาง",
    "Barrier test",
    "ชุดน้ำหนักที่ทดสอบ 13",
    "บริบทใกล้ศรีเอี่ยม",
    "พิสูจน์ 4 ทำเล",
]:
    assert forbidden not in visible, f"robot/ambiguous visible copy remains: {forbidden}"

order = [
    output.index('id="parc-fit"'),
    output.index('id="lenses"'),
    output.index('id="overview"'),
    output.index('id="portfolio"'),
    output.index('id="sensitivity"'),
    output.index('id="detail"'),
    output.index('id="reserves"'),
    output.index('id="approval"'),
]
assert order == sorted(order), "executive-first section order changed"

decision_slice = output[order[0]:order[1]]
assert decision_slice.count("<article>") == 4, "decision queue must contain four cards"
assert decision_slice.count('data-core-fit-locale="') == 10, "full ranked table must retain ten rows"
for row in data["top_10_core_fit_before_route_site_and_economics_gates"]:
    assert row["locale_name_th"] in decision_slice
assert "ศรีเอี่ยม · จุดอ้างอิงตั้งต้น" in decision_slice
assert "ศรีเอี่ยม · host-locale proxy" not in decision_slice

assert "og:title" in output and "og:description" in output and "og:image" in output
assert "twitter:title" in output and "twitter:description" in output and "twitter:image" in output
assert "canonical" in output
assert "IMG_2280" not in output and "IMG_2282" not in output and "IMG_2279" not in output and "IMG_2283" not in output

print("v3.6 QA passed")
print(f"  bytes: {len(output.encode('utf-8')):,}")
print(f"  sha256: {hashlib.sha256(output.encode()).hexdigest()}")
print(f"  anchors: {len(parser.hash_links)} links / 0 dead / 0 duplicate IDs")
print("  frozen v3.3 payload: unchanged")
print("  reference analysis v0.1: unchanged")
print("  one approval request: four locations")
