#!/usr/bin/env python3
"""Build the Release 1.6 map and explainer contracts.

The canonical ranking remains the published Release 1.5 comparable-catchment
ranking. Competition is carried as a diagnostic/action gate. The 80/20 result
is attached only as an explicitly non-canonical scenario.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
OUTPUT = ANALYSIS

REPORT_ID = "parc-bangna-top10-release-1-6"
MODEL_ID = "parc-bangna-comparable-catchment-baseline-v1.6"
LOCALE_RELEASE_ID = "venue-locale-insight-v2.3.1"
CATCHMENT_RULE_ID = "fixed-area-26.3154km2-medoid-v1"
CATCHMENT_RADIUS_KM = 2.89421
CATCHMENT_AREA_KM2 = 26.3154

# The Market Place point is an in-mall tenant proxy, not a verified host
# centroid. Esplanade is also a tenant-branch proxy. Both remain in the
# competition diagnostic/table but are withheld from positional rendering.
WITHHELD_COMPETITOR_POINTS = {
    "comp_bkk_market_place_pracha_uthit": (
        "Host centroid is unresolved; the available coordinate is an in-mall "
        "tenant proxy point."
    ),
    "comp_bkk_esplanade_ratchada": (
        "Host centroid is unresolved; the available coordinate is a tenant-"
        "branch proxy point."
    ),
}


def load(name: str) -> dict:
    return json.loads((ANALYSIS / name).read_text(encoding="utf-8"))


def compact_size_basis(competitor: dict) -> dict:
    """Choose a disclosed marker-size basis without inventing a metric."""
    priority = (
        "leasable_area",
        "commercial_space",
        "retail_complex_area",
        "brand_count_minimum",
        "total_project_area",
    )
    metrics = {
        item.get("metric_name"): item
        for item in competitor.get("operator_metrics", [])
        if isinstance(item, dict)
    }
    for metric_name in priority:
        metric = metrics.get(metric_name)
        if metric:
            return {
                "basis": "operator_metric",
                "metric_name": metric_name,
                "value": metric.get("value"),
                "unit": metric.get("unit"),
                "metric_as_of": metric.get("metric_as_of"),
                "definition": metric.get("definition"),
                "visual_scale_note": (
                    "Marker size is binned for legibility; it is not a "
                    "proportional area diagram."
                ),
            }
    return {
        "basis": "disclosed_impact_class",
        "impact_class": competitor["impact"]["class"],
        "fact_status": competitor["impact"]["fact_status"],
        "basis_text": competitor["impact"]["basis"],
        "prohibition": competitor["impact"]["prohibition"],
        "visual_scale_note": (
            "No suitable current GLA or tenant-count metric was found; marker "
            "size uses the disclosed analytical impact class."
        ),
    }


def build() -> tuple[dict, dict]:
    registry = load("competitor-registry.public.json")
    metrics = load("candidate-metrics.json")
    canonical = load("screening-results.json")
    overlay = load("competitor-score-breakdown.json")
    scenario = load("competition-scenario-results.json")
    rendered_qa_path = ROOT / "qa" / "rendered-qa-results.json"
    rendered_qa = (
        json.loads(rendered_qa_path.read_text(encoding="utf-8"))
        if rendered_qa_path.exists()
        else {}
    )
    rendered_qa_pass = rendered_qa.get("status") == "PASS"
    index_path = ROOT / "index.html"
    index_sha256 = (
        hashlib.sha256(index_path.read_bytes()).hexdigest()
        if index_path.exists()
        else None
    )
    post_publish_pass = (
        rendered_qa_pass
        and rendered_qa.get("target") == "production"
        and rendered_qa.get("release_index_sha256") == index_sha256
    )

    metric_by_id = {item["candidate_id"]: item for item in metrics["candidates"]}
    canonical_by_id = {item["candidate_id"]: item for item in canonical["candidates"]}
    overlay_by_id = {item["candidate_id"]: item for item in overlay["candidates"]}
    scenario_by_id = {item["candidate_id"]: item for item in scenario["candidates"]}
    competitor_by_id = {
        item["competitor_id"]: item for item in registry["competitors"]
    }
    stable_ids = [
        item["candidate_id"]
        for item in sorted(canonical["candidates"], key=lambda row: row["rank"])
    ]

    # The upstream registry uses rank-bearing IDs only as source keys. The
    # public contracts use stable IDs everywhere.
    registry_id_by_stable = {
        item["candidate_id"]: overlay_by_id[item["candidate_id"]][
            "registry_candidate_id"
        ]
        for item in canonical["candidates"]
    }

    sources = [
        {
            "id": "release-15-baseline",
            "site_id": "shared",
            "kind": "published_report",
            "release": "1.5",
            "snapshot_date": "2026-07-27",
            "locator": (
                "https://github.com/montri-th/top10locations-like-parcbn/"
                "blob/563146f6b8f57d25652cea9f60acb6ee9239a054/index.html"
            ),
        },
        {
            "id": "release-16-canonical-screening",
            "site_id": "shared",
            "kind": "screening_model",
            "release": MODEL_ID,
            "snapshot_date": "2026-07-28",
            "locator": "analysis/screening-results.json",
        },
        {
            "id": "release-16-competitor-registry",
            "site_id": "shared",
            "kind": "competitor_registry",
            "release": registry["schema_version"],
            "snapshot_date": registry["evidence_cutoff"],
            "locator": "analysis/competitor-registry.public.json",
        },
        {
            "id": "release-16-competition-overlay",
            "site_id": "shared",
            "kind": "analytical_diagnostic",
            "release": overlay["model_id"],
            "snapshot_date": overlay["as_of"],
            "locator": "analysis/competitor-score-breakdown.json",
        },
    ]

    geometries: list[dict] = []
    analysis_units: list[dict] = []
    detail_maps: list[dict] = []
    map_competitors_by_candidate: dict[str, list[str]] = {}
    withheld_features: list[dict] = []

    for candidate_id in stable_ids:
        metric = metric_by_id[candidate_id]
        canonical_row = canonical_by_id[candidate_id]
        overlay_row = overlay_by_id[candidate_id]
        center = metric["center_wgs84"]
        center_id = f"{candidate_id}-center"
        analysis_id = metric["catchment"]["geometry_id"]

        geometries.append(
            {
                "id": center_id,
                "site_id": candidate_id,
                "vocabulary": "center_point",
                "source_id": "release-15-baseline",
                "source_feature_id": f"{candidate_id}-release-15-medoid",
                "derivation": "none",
                "derived_from": [],
                "disclosure": (
                    "Release 1.5 restaurant-sample medoid; this is an "
                    "analytical reference point, not a parcel or committed "
                    "development site."
                ),
                "coordinates_wgs84": [
                    center["longitude"],
                    center["latitude"],
                ],
                "rank_release_1_5": canonical_row["rank"],
            }
        )
        geometries.append(
            {
                "id": analysis_id,
                "site_id": candidate_id,
                "vocabulary": "standardized_catchment",
                "source_id": "release-16-canonical-screening",
                "source_feature_id": CATCHMENT_RULE_ID,
                "derivation": "buffer",
                "derived_from": [center_id],
                "disclosure": (
                    "Fixed-area analytical circle (26.3154 km²; radius "
                    "2.89421 km) centered on the Release 1.5 medoid. It is "
                    "used only for like-for-like comparison and is not a "
                    "parcel, legal boundary, source polygon, or proven trade "
                    "area."
                ),
                "shape": {
                    "type": "circle",
                    "radius_km": CATCHMENT_RADIUS_KM,
                    "area_km2": CATCHMENT_AREA_KM2,
                    "center_geometry_id": center_id,
                },
            }
        )
        analysis_units.append(
            {
                "candidate_id": candidate_id,
                "geometry_id": analysis_id,
                "display_mode": "shown",
                "disclosure": (
                    "The visible circle is the exact standardized analytical "
                    "unit used by the canonical baseline; it is labelled as "
                    "analytical and must not be read as a parcel or proven "
                    "catchment."
                ),
            }
        )

        poi_geometry_ids: list[str] = []
        mapped_competitor_ids: list[str] = []
        registry_candidate_id = registry_id_by_stable[candidate_id]
        for competitor_id in overlay_row["competitor_ids"]:
            competitor = competitor_by_id[competitor_id]
            if competitor_id in WITHHELD_COMPETITOR_POINTS:
                withheld_features.append(
                    {
                        "candidate_id": candidate_id,
                        "competitor_id": competitor_id,
                        "canonical_name": competitor["canonical_name"],
                        "render_status": "withheld_pending_host_centroid",
                        "reason": WITHHELD_COMPETITOR_POINTS[competitor_id],
                        "included_in_competition_diagnostic": True,
                        "included_in_fallback_table": True,
                        "fallback_table_id": f"{candidate_id}-competitor-table",
                    }
                )
                continue
            geometry_id = f"{candidate_id}-poi-{competitor_id.removeprefix('comp_bkk_')}"
            distance_km = competitor["distance_km_by_candidate"][
                registry_candidate_id
            ]
            geometries.append(
                {
                    "id": geometry_id,
                    "site_id": candidate_id,
                    "vocabulary": "poi_sample",
                    "source_id": "release-16-competitor-registry",
                    "source_feature_id": competitor_id,
                    "derivation": "none",
                    "derived_from": [],
                    "disclosure": (
                        "Operating shopping-center competitor point used as "
                        "evidence. Coordinates are venue-registry points, not "
                        "surveyed parcel centroids."
                    ),
                    "coordinates_wgs84": [
                        competitor["location"]["lon"],
                        competitor["location"]["lat"],
                    ],
                    "canonical_name": competitor["canonical_name"],
                    "operating_status": competitor["operating_status"]["status"],
                    "operating_as_of": competitor["operating_status"]["as_of"],
                    "coordinate_basis": competitor["location"][
                        "coordinate_basis"
                    ],
                    "coordinate_confidence": competitor["location"]["confidence"],
                    "distance_to_candidate_km": distance_km,
                    "impact": {
                        "class": competitor["impact"]["class"],
                        "fact_status": competitor["impact"]["fact_status"],
                        "confidence": competitor["impact"]["confidence"],
                    },
                    "marker_sizing": compact_size_basis(competitor),
                    "interaction": {
                        "trigger": "svg_link",
                        "opens_details_id": (
                            f"competitor-{candidate_id}-{competitor_id}"
                        ),
                        "minimum_target_px": 44,
                    },
                }
            )
            poi_geometry_ids.append(geometry_id)
            mapped_competitor_ids.append(competitor_id)

        map_competitors_by_candidate[candidate_id] = mapped_competitor_ids
        layers = [
            {
                "id": f"{candidate_id}-analytical-catchment",
                "kind": "standardized_catchment",
                "geometry_ids": [analysis_id],
                "visible": True,
                "legend_label": "กรอบวิเคราะห์ 26.3154 ตร.กม. (ไม่ใช่แนวเขตแปลง)",
                "visual_treatment": "quiet_dashed_circle",
            },
            {
                "id": f"{candidate_id}-candidate-center",
                "kind": "candidate_marker",
                "geometry_ids": [center_id],
                "visible": True,
                "marker": "numbered_candidate_marker",
                "legend_label": "จุดอ้างอิงทำเล",
                "direct_labels": True,
            },
        ]
        if poi_geometry_ids:
            layers.append(
                {
                    "id": f"{candidate_id}-verified-competitors",
                    "kind": "poi_sample",
                    "geometry_ids": poi_geometry_ids,
                    "visible": True,
                    "marker": "impact_scaled_competitor_marker",
                    "legend_label": (
                        "คู่แข่งที่ยืนยันสถานะเปิดให้บริการและมีพิกัดพอสำหรับแสดง"
                    ),
                    "direct_labels": False,
                    "interaction": "link_opens_linked_details",
                    "minimum_touch_target_px": 44,
                    "size_basis_priority": [
                        "operator_metric",
                        "disclosed_impact_class",
                    ],
                }
            )

        omitted_note = (
            "ไม่แสดงถนน รถไฟ หรือสถานี เพราะ Release 1.6 ไม่มี feature "
            "lineage และสถานะปฏิบัติการที่ผ่านการยืนยันสำหรับชั้นเหล่านั้น"
        )
        if any(
            item["candidate_id"] == candidate_id for item in withheld_features
        ):
            omitted_note += (
                "; จุดคู่แข่งที่พิกัด host centroid ยังไม่ยืนยันถูกถอนไว้จาก "
                "map แต่ยังอยู่ในตารางและ diagnostic"
            )
        detail_maps.append(
            {
                "id": f"{candidate_id}-detail",
                "role": "detail",
                "site_ids": [candidate_id],
                "layers": layers,
                "omitted_context": {
                    "roads": "omitted_unverified",
                    "rail": "omitted_unverified",
                    "stations": "omitted_unverified",
                    "landmarks": "omitted_not_required",
                    "disclosure": omitted_note,
                },
                "accessibility": {
                    "summary": (
                        f"แผนที่ {metric['name']} แสดงจุดอ้างอิง กรอบวิเคราะห์ "
                        "และคู่แข่งที่มีพิกัดพร้อมใช้; รายการทั้งหมดซ้ำในตาราง"
                    ),
                    "data_table_id": f"{candidate_id}-competitor-table",
                },
            }
        )

    overview = {
        "id": "top10-overview",
        "role": "overview",
        "site_ids": stable_ids,
        "layers": [
            {
                "id": "candidate-centers",
                "kind": "candidate_marker",
                "geometry_ids": [f"{item}-center" for item in stable_ids],
                "visible": True,
                "marker": "numbered_candidate_marker",
                "legend_label": "10 ทำเลตามอันดับ baseline",
                "direct_labels": True,
            }
        ],
        "accessibility": {
            "summary": (
                "ภาพรวมจุดอ้างอิงของ 10 ทำเลตามอันดับ canonical baseline "
                "Release 1.5"
            ),
            "data_table_id": "top10-comparison-table",
        },
    }

    map_manifest = {
        "contract_version": "1.0",
        "report_id": REPORT_ID,
        "scope": {"mode": "comparison", "site_ids": stable_ids},
        "candidate_ids": stable_ids,
        "screening_linkage": {
            "status": "linked",
            "model_id": MODEL_ID,
            "catchment_rule_id": CATCHMENT_RULE_ID,
            "locale_release_id": LOCALE_RELEASE_ID,
            "analysis_units": analysis_units,
        },
        "sources": sources,
        "geometries": geometries,
        "osm_snapshot": None,
        "maps": [overview, *detail_maps],
        "withheld_features": withheld_features,
        "render_contract": {
            "map_root": {
                "attributes": {
                    "data-location-map": "",
                    "data-map-manifest": "analysis/map-manifest.json",
                }
            },
            "candidate_map": {
                "attribute": "data-map-candidate-id",
                "value_source": "candidate_id",
            },
            "competitor_marker": {
                "required_attributes": [
                    "data-competitor-id",
                    "data-map-candidate-id",
                    "data-impact-class",
                    "data-size-basis",
                ],
                "semantics": (
                    "SVG link with an accessible name; click, tap, or Enter "
                    "opens a linked competitor detail block. Escape closes "
                    "that block and returns focus. Target is at least 44 px."
                ),
            },
            "competitor_details": {
                "required_attributes": [
                    "data-competitor-details",
                    "data-competitor-id",
                    "data-evidence-status",
                ]
            },
            "fallback_table": {
                "required_attribute": "data-map-fallback",
                "row_attribute": "data-competitor-id",
            },
        },
        "qa": {
            "status": (
                "post_publish_pass"
                if post_publish_pass
                else "pre_publish_pass"
                if rendered_qa_pass
                else "pre_render_pending"
            ),
            "evidence": (
                "qa/rendered-qa-results.json" if rendered_qa_pass else None
            ),
            "checked_at": (
                rendered_qa.get("post_hardening_smoke", {}).get("checked_at")
                if post_publish_pass
                else rendered_qa.get("checked_at")
            ),
            "orphan_dot_count": 0,
            "keyboard_access": rendered_qa_pass,
            "visible_focus": rendered_qa_pass,
            "screen_reader_summary": rendered_qa_pass,
            "data_table_fallback": rendered_qa_pass,
            "color_independent_encoding": rendered_qa_pass,
            "reduced_motion": rendered_qa_pass,
            "overflow_free": rendered_qa_pass,
            "zoom_200_checked": rendered_qa_pass,
            "light_dark_checked": rendered_qa_pass,
            "responsive_widths": (
                rendered_qa.get("post_hardening_smoke", {}).get(
                    "viewports",
                    [320, 375, 768, 1024, 1440],
                )
                if post_publish_pass
                else [320, 375, 768, 1024, 1440]
            ),
            "min_label_px": 11,
            "min_touch_target_px": 44,
            "text_contrast_ratio": 4.5,
            "non_text_contrast_ratio": 3,
            "note": (
                "Rendered pre-publish and post-publish Production QA passed; "
                "the recorded Production index hash matches this release."
                if post_publish_pass
                else "Rendered pre-publish QA passed; post-publish production "
                "QA remains required."
                if rendered_qa_pass
                else "The nine boolean checks remain false until rendered "
                "HTML QA; all structural and lineage checks are complete."
            ),
        },
    }

    # Build an explainer payload whose canonical ranks remain untouched.
    payload_candidates: list[dict] = []
    for candidate_id in stable_ids:
        row = canonical_by_id[candidate_id]
        diagnostic = overlay_by_id[candidate_id]
        scenario_row = scenario_by_id[candidate_id]
        action = diagnostic["recommended_action"]
        payload_candidates.append(
            {
                "id": candidate_id,
                "name": row["name"],
                "rank": row["rank"],
                "score": row["overall_score"],
                "status": f"competition-action-tier-{action['tier']}",
                "evidence_ids": [
                    "release-15-baseline",
                    "release-16-canonical-screening",
                    "release-16-competitor-registry",
                    "release-16-competition-overlay",
                ],
                "competition_diagnostic": {
                    "status": "diagnostic_not_rank_replacement",
                    "verified_operating_competitor_count": diagnostic[
                        "verified_competitor_count"
                    ],
                    "competitor_supply_pressure": diagnostic[
                        "competitor_supply_pressure"
                    ],
                    "competitive_pressure_band": diagnostic[
                        "competitive_pressure_band"
                    ],
                    "strategic_gap_potential": diagnostic[
                        "strategic_gap_potential"
                    ],
                    "strategic_gap_status": diagnostic[
                        "strategic_gap_status"
                    ],
                    "competitive_room_score": diagnostic[
                        "competitive_room_score"
                    ],
                    "evidence_readiness_score": diagnostic[
                        "evidence_readiness_score"
                    ],
                    "action_tier": action["tier"],
                    "action_label_th": action["label_th"],
                    "decision_rule": action["decision_rule"],
                    "competitor_ids": diagnostic["competitor_ids"],
                    "mapped_competitor_ids": map_competitors_by_candidate[
                        candidate_id
                    ],
                },
                "illustrative_competition_scenario": {
                    "status": "noncanonical_sensitivity_scenario",
                    "baseline_weight": 0.8,
                    "competitive_room_weight": 0.2,
                    "rank": scenario_row["rank"],
                    "score": scenario_row["overall_score"],
                    "prohibition": (
                        "Do not present this scenario rank as the Release 1.6 "
                        "canonical rank or an investment recommendation."
                    ),
                },
            }
        )

    payload_sources = [
        {
            "id": "release-15-baseline",
            "label": (
                "Published PARC Bangna Bangkok Top 10 Release 1.5 baseline, "
                "27 July 2026"
            ),
        },
        {
            "id": "release-16-canonical-screening",
            "label": (
                "Canonical Release 1.6 comparable-catchment output; Release "
                "1.5 rank and score preserved"
            ),
        },
        {
            "id": "release-16-competitor-registry",
            "label": (
                "Preliminary minimum verified operating-shopping-center "
                "registry, evidence cutoff 28 July 2026"
            ),
        },
        {
            "id": "release-16-competition-overlay",
            "label": (
                "Competition pressure, strategic-gap hypothesis, evidence "
                "readiness, and action-tier diagnostic"
            ),
        },
        {
            "id": "release-16-scenario",
            "label": (
                "Illustrative non-canonical 80% baseline / 20% competitive-"
                "room sensitivity scenario"
            ),
        },
        {
            "id": "map-contract-v1",
            "label": "Evidence-grounded location-map contract v1.0",
        },
    ]

    all_ids = stable_ids
    payload = {
        "report": {
            "id": REPORT_ID,
            "title": (
                "PARC Bangna Bangkok Top 10 — Release 1.6 "
                "competition diagnostic"
            ),
            "as_of": "2026-07-28",
            "audience": "J Lifestyle Center decision team",
            "decision": (
                "Preserve the Release 1.5 comparable-catchment ranking as the "
                "canonical baseline and use verified competition pressure to "
                "set action tiers and the next validation wave."
            ),
        },
        "score": {
            "min": 0,
            "max": 100,
            "higher_is_better": True,
            "status": (
                "Canonical score is the published Release 1.5 baseline; "
                "competition is diagnostic, not a replacement rank."
            ),
        },
        "candidates": payload_candidates,
        "recommendation": {
            "candidate_id": "bang-pakok",
            "summary": (
                "Retain Wongwian Yai East as the canonical baseline leader, "
                "but use Bang Pakok as the first competition-aware field-"
                "validation case because it has the strongest balance of "
                "competitive room and evidence readiness in this overlay."
            ),
            "confidence": (
                "medium for field-validation priority; low for investment "
                "advancement until parcel, network, and completeness checks "
                "are complete"
            ),
            "evidence_ids": [
                "release-15-baseline",
                "release-16-canonical-screening",
                "release-16-competitor-registry",
                "release-16-competition-overlay",
            ],
        },
        "cta": {
            "label": "อนุมัติ competitive field validation",
            "action": (
                "Validate Bang Pakok with a complete operating-venue census "
                "and network catchment; verify the apparent room at Wang Lang "
                "and Pracha Uthit; keep the canonical leaders behind a "
                "competition-first gate."
            ),
            "owner": "ทีมพัฒนาทำเล J Lifestyle Center",
            "timing": "ก่อน final parcel shortlist รอบถัดไป",
        },
        "map": {
            "status": "included",
            "manifest": "analysis/map-manifest.json",
            "candidate_ids": stable_ids,
            "fallback": (
                "The ranked comparison and a competitor table repeat every "
                "mapped candidate and competitor. Market Place Pracha Uthit "
                "and Esplanade Ratchada remain in the diagnostic/table but "
                "are not plotted until their host centroids are verified."
            ),
        },
        "caveats": [
            {
                "id": "baseline-not-final-investment-rank",
                "severity": "decision-changing",
                "visibility": "inline",
                "text": (
                    "The canonical order preserves Release 1.5 because the "
                    "competitor registry is a minimum verified set, not a "
                    "completeness-certified census. Competition changes the "
                    "action tier, not the canonical rank, in this release."
                ),
                "candidate_ids": all_ids,
                "evidence_ids": [
                    "release-16-canonical-screening",
                    "release-16-competitor-registry",
                ],
            },
            {
                "id": "scenario-is-not-canonical",
                "severity": "decision-changing",
                "visibility": "inline",
                "text": (
                    "The 80/20 competition scenario is a sensitivity test "
                    "only. Its rank must not replace the canonical ranking or "
                    "be presented as an investment recommendation."
                ),
                "candidate_ids": all_ids,
                "evidence_ids": ["release-16-scenario"],
            },
            {
                "id": "medoid-and-fixed-circle-limit",
                "severity": "decision-changing",
                "visibility": "inline",
                "text": (
                    "Candidate centers are restaurant-sample medoids, not "
                    "parcels. The 2.89421 km fixed circle ignores bridges, "
                    "ferries, congestion, pedestrian barriers, and actual "
                    "site access."
                ),
                "candidate_ids": all_ids,
                "evidence_ids": [
                    "release-15-baseline",
                    "release-16-canonical-screening",
                ],
            },
            {
                "id": "samre-center-coincides-with-incumbent",
                "severity": "decision-changing",
                "visibility": "inline",
                "text": (
                    "The Samre analytical center is about 0.034 km from "
                    "Riverside Plaza. Confirm a real parcel and recenter the "
                    "analysis before treating Samre as an independent "
                    "development opportunity."
                ),
                "candidate_ids": ["samre"],
                "evidence_ids": [
                    "release-16-competitor-registry",
                    "release-16-competition-overlay",
                ],
            },
            {
                "id": "strategic-gaps-are-hypotheses",
                "severity": "material",
                "visibility": "evidence",
                "text": (
                    "Strategic gaps describe testable positioning hypotheses. "
                    "No credible evidence currently supports claims that an "
                    "incumbent has weak traffic, occupancy, service, tenant "
                    "mix, or commercial performance."
                ),
                "candidate_ids": all_ids,
                "evidence_ids": [
                    "release-16-competitor-registry",
                    "release-16-competition-overlay",
                ],
            },
            {
                "id": "two-host-centroids-withheld",
                "severity": "material",
                "visibility": "evidence",
                "text": (
                    "Market Place Pracha Uthit and Esplanade Ratchada are "
                    "included in the diagnostic and fallback tables but "
                    "withheld from the map because their available coordinates "
                    "are tenant proxy points rather than verified host "
                    "centroids."
                ),
                "candidate_ids": ["pracha-uthit", "din-daeng"],
                "evidence_ids": [
                    "release-16-competitor-registry",
                    "map-contract-v1",
                ],
            },
            {
                "id": "roads-rail-stations-omitted",
                "severity": "context",
                "visibility": "evidence",
                "text": (
                    "Release 1.6 shows no road, rail, or station layer because "
                    "no current feature-level lineage and operating-status "
                    "snapshot was validated for those map features."
                ),
                "candidate_ids": all_ids,
                "evidence_ids": ["map-contract-v1"],
            },
        ],
        "sources": payload_sources,
        "html_hooks": {
            "report_root": ["data-location-report", "data-report-id"],
            "candidate": [
                "data-candidate-id",
                "data-candidate-name",
                "data-rank",
                "data-score",
            ],
            "recommendation": ["data-recommendation-candidate"],
            "primary_cta": ["data-primary-cta", "data-owner", "data-timing"],
            "evidence_toggle": [
                "data-evidence-toggle",
                "data-evidence-candidate-id",
            ],
            "map": [
                "data-location-map",
                "data-map-manifest",
                "data-map-candidate-id",
            ],
            "map_fallback": ["data-map-fallback"],
            "competitor_marker": [
                "data-competitor-id",
                "data-map-candidate-id",
                "data-impact-class",
                "data-size-basis",
            ],
            "caveat": [
                "data-caveat-id",
                "data-caveat-severity",
                "data-caveat-visibility",
            ],
            "source": ["data-source-id"],
            "canonical_score_serialization": (
                "Use canonical JSON number text in data-score."
            ),
        },
    }

    return map_manifest, payload


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    map_manifest, payload = build()
    (OUTPUT / "map-manifest.json").write_text(
        json.dumps(map_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (OUTPUT / "location-payload.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"WROTE {OUTPUT / 'map-manifest.json'}")
    print(f"WROTE {OUTPUT / 'location-payload.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
