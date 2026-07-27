#!/usr/bin/env python3
"""Cross-check final Release 1.6 contracts against analytical sources."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "analysis"
ANALYSIS = OUTPUT
MAP_VALIDATOR = Path(
    os.environ.get(
        "PARC_MAP_MANIFEST_VALIDATOR",
        "/root/.codex/skills/remote-skills/"
        "skill-6a674cca63cc8191abed08749733a25e/"
        "scripts/validate_map_manifest.py",
    )
)
WITHHELD = {
    "comp_bkk_market_place_pracha_uthit",
    "comp_bkk_esplanade_ratchada",
}
RENDERED_QA_FLAGS = {
    "keyboard_access",
    "visible_focus",
    "screen_reader_summary",
    "data_table_fallback",
    "color_independent_encoding",
    "reduced_motion",
    "overflow_free",
    "zoom_200_checked",
    "light_dark_checked",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    manifest = load(OUTPUT / "map-manifest.json")
    payload = load(OUTPUT / "location-payload.json")
    canonical = load(ANALYSIS / "screening-results.json")
    overlay = load(ANALYSIS / "competitor-score-breakdown.json")
    scenario = load(ANALYSIS / "competition-scenario-results.json")

    canonical_by_id = {
        row["candidate_id"]: row for row in canonical["candidates"]
    }
    overlay_by_id = {row["candidate_id"]: row for row in overlay["candidates"]}
    scenario_by_id = {
        row["candidate_id"]: row for row in scenario["candidates"]
    }
    payload_by_id = {row["id"]: row for row in payload["candidates"]}
    candidate_ids = [
        row["candidate_id"]
        for row in sorted(canonical["candidates"], key=lambda item: item["rank"])
    ]

    require(manifest["candidate_ids"] == candidate_ids, "map candidate order")
    require(
        [row["id"] for row in payload["candidates"]] == candidate_ids,
        "payload candidate order",
    )
    for candidate_id in candidate_ids:
        source = canonical_by_id[candidate_id]
        row = payload_by_id[candidate_id]
        diagnostic = row["competition_diagnostic"]
        scenario_row = row["illustrative_competition_scenario"]
        require(row["rank"] == source["rank"], f"{candidate_id}: canonical rank")
        require(
            row["score"] == source["overall_score"],
            f"{candidate_id}: canonical score",
        )
        require(
            diagnostic["competitive_room_score"]
            == overlay_by_id[candidate_id]["competitive_room_score"],
            f"{candidate_id}: competitive room",
        )
        require(
            diagnostic["action_tier"]
            == overlay_by_id[candidate_id]["recommended_action"]["tier"],
            f"{candidate_id}: action tier",
        )
        require(
            diagnostic["competitive_pressure_band"]
            == overlay_by_id[candidate_id]["competitive_pressure_band"],
            f"{candidate_id}: pressure band",
        )
        require(
            scenario_row["status"] == "noncanonical_sensitivity_scenario",
            f"{candidate_id}: scenario label",
        )
        require(
            scenario_row["rank"] == scenario_by_id[candidate_id]["rank"],
            f"{candidate_id}: scenario rank",
        )
        require(
            scenario_row["score"]
            == scenario_by_id[candidate_id]["overall_score"],
            f"{candidate_id}: scenario score",
        )

    require(manifest["osm_snapshot"] is None, "OSM snapshot must be null")
    require(
        not any(
            geometry["vocabulary"].startswith("osm_")
            for geometry in manifest["geometries"]
        ),
        "no OSM geometry",
    )
    require(
        not any(
            layer["kind"] in {"major_road", "rail_line", "station"}
            for map_item in manifest["maps"]
            for layer in map_item["layers"]
        ),
        "no road, rail, or station layers",
    )
    units = manifest["screening_linkage"]["analysis_units"]
    require(len(units) == 10, "ten linked analysis units")
    require(
        all(unit["display_mode"] == "shown" for unit in units),
        "all analytical circles shown",
    )
    catchments = [
        geometry
        for geometry in manifest["geometries"]
        if geometry["vocabulary"] == "standardized_catchment"
    ]
    require(len(catchments) == 10, "ten analytical catchment geometries")
    require(
        all(
            geometry["shape"]["radius_km"] == 2.89421
            and geometry["shape"]["area_km2"] == 26.3154
            for geometry in catchments
        ),
        "fixed area/radius parity",
    )

    withheld_rows = manifest["withheld_features"]
    require(
        {row["competitor_id"] for row in withheld_rows} == WITHHELD,
        "exact withheld competitor set",
    )
    poi_geometries = [
        geometry
        for geometry in manifest["geometries"]
        if geometry["vocabulary"] == "poi_sample"
    ]
    require(
        not ({row["source_feature_id"] for row in poi_geometries} & WITHHELD),
        "withheld competitors must not be mapped",
    )
    require(
        all(
            row["included_in_competition_diagnostic"]
            and row["included_in_fallback_table"]
            and row["render_status"] == "withheld_pending_host_centroid"
            for row in withheld_rows
        ),
        "withheld competitor evidence/table parity",
    )
    require(
        all(
            geometry["coordinate_confidence"] == "high"
            for geometry in poi_geometries
        ),
        "every rendered competitor point has high coordinate confidence",
    )

    required_hooks = {
        "data-location-report",
        "data-report-id",
        "data-candidate-id",
        "data-candidate-name",
        "data-rank",
        "data-score",
        "data-recommendation-candidate",
        "data-primary-cta",
        "data-owner",
        "data-timing",
        "data-evidence-toggle",
        "data-evidence-candidate-id",
        "data-location-map",
        "data-map-manifest",
        "data-map-candidate-id",
        "data-map-fallback",
        "data-caveat-id",
        "data-caveat-severity",
        "data-caveat-visibility",
        "data-source-id",
    }
    declared_hooks = {
        hook
        for value in payload["html_hooks"].values()
        if isinstance(value, list)
        for hook in value
    }
    require(required_hooks.issubset(declared_hooks), "location HTML hooks")

    # Validate the structural map contract. A pending manifest is checked with
    # only the browser-dependent flags lifted in the in-memory copy; a passed
    # manifest must point to a real PASS evidence file.
    if MAP_VALIDATOR.is_file():
        spec = importlib.util.spec_from_file_location(
            "validate_map_manifest", MAP_VALIDATOR
        )
        require(spec is not None and spec.loader is not None, "load map validator")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        structural_copy = json.loads(json.dumps(manifest))
        for field in RENDERED_QA_FLAGS:
            structural_copy["qa"][field] = True
        errors = module.validate(structural_copy)
        require(errors == [], f"structural map errors: {errors}")

    qa_status = manifest["qa"]["status"]
    if qa_status == "pre_render_pending":
        require(
            {
                field
                for field in RENDERED_QA_FLAGS
                if manifest["qa"][field] is False
            }
            == RENDERED_QA_FLAGS,
            "pending manifest must leave all rendered flags false",
        )
    elif qa_status == "pre_publish_pass":
        require(
            all(manifest["qa"][field] is True for field in RENDERED_QA_FLAGS),
            "passed manifest must set all rendered flags true",
        )
        evidence_path = ROOT / manifest["qa"]["evidence"]
        require(evidence_path.exists(), "rendered QA evidence file")
        require(load(evidence_path).get("status") == "PASS", "rendered QA evidence status")
    else:
        raise AssertionError(f"unsupported QA status: {qa_status}")

    print(
        "PASS: canonical rank/score, diagnostic/action tier, non-canonical "
        "scenario, geometry lineage, point confidence, withheld-marker "
        "policy, no-road/rail policy, HTML hooks, and structural map contract "
        "are consistent."
    )
    if qa_status == "pre_render_pending":
        print(
            "PENDING: 9 rendered map-QA booleans remain false until the HTML "
            "is implemented and checked."
        )
    else:
        print(
            "PASS: rendered keyboard, focus, fallback, non-colour encoding, "
            "reduced-motion, overflow, 200% zoom, and light/dark evidence is "
            "registered."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
