#!/usr/bin/env python3
"""Create the public Release 1.6 competitor registry.

The analytical registry may carry private connector identifiers that are useful
inside the workspace but are unnecessary in a public GitHub release. This
script removes those identifiers while preserving the facts, public URLs,
coordinates, confidence notes, and analytical classifications used by the
report.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "competitor-registry.json"
OUTPUT = ROOT / "analysis" / "competitor-registry.public.json"
PUBLIC_SOURCE_KINDS = {
    "authoritative_external_report": "external_current_report",
    "authoritative_current_guide": "external_current_guide",
    "authoritative_current_business_report": "external_current_business_report",
}


def sanitize(value):
    if isinstance(value, list):
        return [sanitize(item) for item in value]
    if not isinstance(value, dict):
        return value

    clean = {}
    for key, item in value.items():
        if key in {"spreadsheet_id", "sheet_name"}:
            continue
        if key == "source_kind" and isinstance(item, str):
            item = PUBLIC_SOURCE_KINDS.get(item, item)
        clean[key] = sanitize(item)

    if clean.get("source_id") == "venue_shoppingcenter_finaldata_merge_all_final5":
        clean["source_id"] = "venue-locale-fundamental-shopping-centers-v0.1"
    if clean.get("title") == "Venue_ShoppingCenter_finalData":
        clean["title"] = "Venue Locale Fundamental shopping-center registry"
    return clean


def main() -> int:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    public = sanitize(copy.deepcopy(source))
    public["publication_note"] = (
        "Workspace connector identifiers were removed. Public facts, source URLs, "
        "coordinates, confidence notes, and analytical classifications are unchanged."
    )
    OUTPUT.write_text(
        json.dumps(public, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"WROTE {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
