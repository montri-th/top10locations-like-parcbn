#!/usr/bin/env python3
"""Build the Release 1.6 competitive overlay from the public-safe registry.

The script never treats missing as zero. It uses only operating venues already
inside the registry, deduplicates integrated precincts, and keeps the overlay
separate from the Release 1.5 comparable-catchment baseline.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "analysis" / "competitor-registry.public.json"
METRICS_PATH = ROOT / "analysis" / "candidate-metrics.json"
BREAKDOWN_PATH = ROOT / "analysis" / "competitor-score-breakdown.json"

CATCHMENT_AREA_KM2 = 26.3154
CATCHMENT_RADIUS_KM = 2.89421
PRESSURE_SATURATION_LOAD = 12.0

# Stable IDs deliberately omit rank.
CANDIDATES = [
    ("wongwian-yai-east", "cand_01_wongwian_yai_east", "วงเวียนใหญ่–ตะวันออก", 52.71, 81),
    ("charoen-rat", "cand_02_charoen_rat", "เจริญราษฎร์", 52.61, 83),
    ("samre", "cand_03_samre", "สำเหร่", 52.31, 67),
    ("ban-khaek", "cand_04_ban_khaek", "แยกบ้านแขก", 51.46, 63),
    ("talat-phlu-south", "cand_05_talat_phlu_south", "ตลาดพลู–ใต้", 48.44, 57),
    ("bang-pakok", "cand_06_bang_pakok", "บางปะกอก", 47.02, 57),
    ("wang-lang", "cand_07_wang_lang", "วังหลัง", 45.74, 76),
    ("ratchathewi", "cand_08_ratchathewi", "ราชเทวี", 44.14, 85),
    ("pracha-uthit", "cand_09_pracha_uthit", "ประชาอุทิศ", 43.78, 45),
    ("din-daeng", "cand_10_din_daeng", "ดินแดง", 43.57, 78),
]

IMPACT_WEIGHT = {
    "high": 5.0,
    "medium_high": 4.0,
    "medium": 3.0,
}

# This is an analytical overlap classification, not a claim about performance.
TYPE_OVERLAP = {
    "community_mall": 1.00,
    "open_air_shopping_center": 0.90,
    "department_store_led_shopping_center": 0.80,
    "shopping_center": 0.80,
    "destination_shopping_center": 0.55,
    "specialty_shopping_center": 0.55,
}

OVERLAP_OVERRIDES = {
    "comp_bkk_platform_wongwian_yai": 0.90,
    "comp_bkk_kingsquare_community_mall": 1.00,
    "comp_bkk_riverside_plaza_bangkok": 0.90,
    "comp_bkk_the_old_siam_plaza": 0.55,
    "comp_bkk_tha_maharaj": 0.55,
    "comp_bkk_market_place_pracha_uthit": 1.00,
    "comp_bkk_the_street_ratchada": 0.90,
}

EVIDENCE_ADJUSTMENTS = {
    "samre": [("candidate_center_artifact", -20)],
    "ban-khaek": [("river_and_bridge_network_not_modelled", -20)],
    "wang-lang": [("river_ferry_and_bridge_network_not_modelled", -20)],
    "ratchathewi": [("dense_cluster_is_minimum_verified_set", -15)],
    "pracha-uthit": [("host_centroid_uses_tenant_in_mall_proxy", -20)],
    "din-daeng": [("dense_cluster_is_minimum_verified_set", -15)],
}


def classify_action(competitive_room: float, readiness: float) -> dict:
    """Turn the diagnostic into an action gate, not a replacement ranking."""
    if competitive_room >= 45.0 and readiness >= 80.0:
        return {
            "tier": "A",
            "label_th": "เดินหน้าตรวจทำเลเชิงรุก",
            "decision_rule": "competitive_room >= 45 and evidence_readiness >= 80",
        }
    if competitive_room >= 45.0:
        return {
            "tier": "B",
            "label_th": "มีช่องว่าง แต่ต้องยืนยันภาคสนามก่อน",
            "decision_rule": "competitive_room >= 45 and evidence_readiness < 80",
        }
    if competitive_room >= 20.0:
        return {
            "tier": "C",
            "label_th": "พิจารณาเฉพาะกลยุทธ์ที่ต่างจากคู่แข่งชัด",
            "decision_rule": "20 <= competitive_room < 45",
        }
    return {
        "tier": "D",
        "label_th": "แข่งขันสูง—เดินหน้าต่อเมื่อมีสิทธิ์ไซต์หรือจุดต่างเหนือกว่า",
        "decision_rule": "competitive_room < 20",
    }


def pressure_band(pressure: float) -> str:
    if pressure >= 75.0:
        return "high"
    if pressure >= 45.0:
        return "medium"
    return "low"


def proximity_weight(distance_km: float) -> float:
    if distance_km <= 1.0:
        return 1.0
    if distance_km <= 2.0:
        return 0.75
    if distance_km <= CATCHMENT_RADIUS_KM:
        return 0.50
    raise ValueError(f"distance {distance_km} is outside the declared catchment")


def build() -> tuple[dict, dict]:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    competitors = {item["competitor_id"]: item for item in registry["competitors"]}
    registry_candidates = {item["candidate_id"]: item for item in registry["candidates"]}

    metric_rows: list[dict] = []
    breakdown_rows: list[dict] = []

    for stable_id, registry_id, name, baseline_score, land_pressure in CANDIDATES:
        registry_candidate = registry_candidates[registry_id]
        visible_ids = [
            item["competitor_id"]
            for item in registry["competitors"]
            if registry_id in item["within_release_1_5_catchment_candidate_ids"]
        ]
        if not visible_ids:
            raise ValueError(f"{stable_id}: no verified operating competitor in registry")

        member_rows: list[dict] = []
        grouped: dict[str, list[dict]] = {}
        for competitor_id in visible_ids:
            venue = competitors[competitor_id]
            if venue["operating_status"]["status"] != "operating":
                raise ValueError(f"{competitor_id}: non-operating venue entered scoring")
            distance = float(venue["distance_km_by_candidate"][registry_id])
            impact_class = venue["impact"]["class"]
            if impact_class not in IMPACT_WEIGHT:
                raise ValueError(f"{competitor_id}: unsupported impact class {impact_class}")
            overlap = OVERLAP_OVERRIDES.get(
                competitor_id,
                TYPE_OVERLAP.get(venue["venue_type"]),
            )
            if overlap is None:
                raise ValueError(f"{competitor_id}: missing routine-overlap policy")
            proximity = proximity_weight(distance)
            load = IMPACT_WEIGHT[impact_class] * proximity * overlap
            cluster_id = venue["parent_cluster_id"] or competitor_id
            member = {
                "competitor_id": competitor_id,
                "name": venue["canonical_name"],
                "parent_cluster_id": venue["parent_cluster_id"],
                "distance_km": distance,
                "impact_class": impact_class,
                "impact_weight": IMPACT_WEIGHT[impact_class],
                "routine_overlap_factor": overlap,
                "proximity_weight": proximity,
                "member_pressure_load": round(load, 4),
            }
            member_rows.append(member)
            grouped.setdefault(cluster_id, []).append(member)

        cluster_rows: list[dict] = []
        total_load = 0.0
        for cluster_id, members in sorted(grouped.items()):
            loads = sorted((float(item["member_pressure_load"]) for item in members), reverse=True)
            contribution = loads[0] + 0.25 * sum(loads[1:])
            total_load += contribution
            cluster_rows.append(
                {
                    "cluster_id": cluster_id,
                    "member_competitor_ids": [item["competitor_id"] for item in members],
                    "cluster_pressure_load": round(contribution, 4),
                    "deduplication_rule": "maximum member load plus 25% of each additional member load",
                }
            )

        pressure = min(100.0, total_load / PRESSURE_SATURATION_LOAD * 100.0)
        headroom = 100.0 - pressure

        direct_distances = [
            item["distance_km"]
            for item in member_rows
            if item["routine_overlap_factor"] >= 0.90
        ]
        nearest_distance = min(item["distance_km"] for item in member_rows)
        destination_load = sum(
            item["member_pressure_load"]
            for item in member_rows
            if item["routine_overlap_factor"] <= 0.55
        )
        all_member_load = sum(item["member_pressure_load"] for item in member_rows)

        strategic_gap = 55.0
        gap_adjustments: list[dict] = []
        if direct_distances:
            nearest_direct = min(direct_distances)
            if nearest_direct <= 2.0:
                strategic_gap -= 20.0
                gap_adjustments.append({"reason": "direct_routine_competitor_within_2km", "delta": -20})
            else:
                strategic_gap -= 10.0
                gap_adjustments.append({"reason": "direct_routine_competitor_in_outer_catchment", "delta": -10})
        if nearest_distance <= 0.30:
            strategic_gap -= 10.0
            gap_adjustments.append({"reason": "competitor_within_300m", "delta": -10})
        if stable_id == "samre":
            strategic_gap -= 10.0
            gap_adjustments.append({"reason": "candidate_center_nearly_coincides_with_riverside_plaza", "delta": -10})
        if all_member_load > 0 and destination_load / all_member_load >= 0.60:
            strategic_gap += 10.0
            gap_adjustments.append({"reason": "destination_or_specialist_supply_dominates_verified_load", "delta": 10})
        strategic_gap = min(70.0, max(20.0, strategic_gap))

        # Headroom is the stronger term. Gap remains a hypothesis.
        competitive_room = 0.70 * headroom + 0.30 * strategic_gap

        readiness = 85.0  # preliminary registry is not completeness-certified
        readiness_adjustments = [{"reason": "preliminary_minimum_verified_registry", "delta": -15}]
        for reason, delta in EVIDENCE_ADJUSTMENTS.get(stable_id, []):
            readiness += delta
            readiness_adjustments.append({"reason": reason, "delta": delta})
        readiness = min(100.0, max(0.0, readiness))
        action = classify_action(competitive_room, readiness)

        metric_rows.append(
            {
                "candidate_id": stable_id,
                "name": name,
                "catchment": {
                    "geometry_id": f"{stable_id}-analysis-unit",
                    "area_km2": CATCHMENT_AREA_KM2,
                },
                "metrics": {
                    "release_1_5_opportunity_score": baseline_score,
                    "competitive_room_score": round(competitive_room, 2),
                    "evidence_readiness_score": round(readiness, 2),
                    "land_pressure_percentile": land_pressure,
                },
                "center_wgs84": {
                    "latitude": registry_candidate["lat"],
                    "longitude": registry_candidate["lon"],
                },
                "metric_provenance": {
                    "release_1_5_opportunity_score": "published Release 1.5 baseline",
                    "competitive_room_score": "derived by competitor-score-breakdown.json; analytical scenario only",
                    "evidence_readiness_score": "derived from disclosed registry limitations",
                    "land_pressure_percentile": "Release 1.5 readiness proxy; not observed land price",
                },
            }
        )
        breakdown_rows.append(
            {
                "candidate_id": stable_id,
                "registry_candidate_id": registry_id,
                "name": name,
                "verified_competitor_count": len(member_rows),
                "competitor_ids": visible_ids,
                "member_loads": member_rows,
                "cluster_loads": cluster_rows,
                "raw_pressure_load": round(total_load, 4),
                "pressure_saturation_load": PRESSURE_SATURATION_LOAD,
                "competitor_supply_pressure": round(pressure, 2),
                "supply_headroom": round(headroom, 2),
                "strategic_gap_potential": round(strategic_gap, 2),
                "strategic_gap_status": "hypothesis",
                "strategic_gap_adjustments": gap_adjustments,
                "competitive_room_formula": "0.70 × supply_headroom + 0.30 × strategic_gap_potential",
                "competitive_room_score": round(competitive_room, 2),
                "competitive_pressure_band": pressure_band(pressure),
                "evidence_readiness_score": round(readiness, 2),
                "evidence_readiness_adjustments": readiness_adjustments,
                "recommended_action": action,
            }
        )

    metrics = {
        "schema_version": "1.0",
        "locale_release_id": "venue-locale-insight-v2.3.1",
        "catchment_rule_id": "fixed-area-26.3154km2-medoid-v1",
        "candidates": metric_rows,
    }
    # A deliberately adverse, noncanonical census sensitivity for the only
    # Tier A candidate. It demonstrates how fragile the action tier is while
    # the registry remains a minimum verified set.
    bang_pakok = next(
        row for row in breakdown_rows if row["candidate_id"] == "bang-pakok"
    )
    added_direct_load = (
        IMPACT_WEIGHT["high"]
        * TYPE_OVERLAP["community_mall"]
        * proximity_weight(1.0)
    )
    stress_total_load = bang_pakok["raw_pressure_load"] + added_direct_load
    stress_pressure = min(
        100.0,
        stress_total_load / PRESSURE_SATURATION_LOAD * 100.0,
    )
    stress_headroom = 100.0 - stress_pressure
    stress_strategic_gap = 35.0
    stress_room = (
        0.70 * stress_headroom
        + 0.30 * stress_strategic_gap
    )
    stress_action = classify_action(
        stress_room,
        bang_pakok["evidence_readiness_score"],
    )

    breakdown = {
        "schema_version": "1.0",
        "model_id": "parc-bangna-competitive-overlay-v1.6",
        "as_of": registry["evidence_cutoff"],
        "status": "preliminary_minimum_verified_supply",
        "registry_scope": registry["release_context"]["registry_scope"],
        "catchment_radius_km": CATCHMENT_RADIUS_KM,
        "impact_weight": IMPACT_WEIGHT,
        "proximity_bands": [
            {"max_distance_km": 1.0, "weight": 1.0},
            {"max_distance_km": 2.0, "weight": 0.75},
            {"max_distance_km": CATCHMENT_RADIUS_KM, "weight": 0.5},
        ],
        "type_overlap_defaults": TYPE_OVERLAP,
        "overlap_overrides": OVERLAP_OVERRIDES,
        "cluster_rule": "maximum member load plus 25% of each additional member load",
        "pressure_formula": "min(100, deduplicated_pressure_load / 12 × 100)",
        "competitive_room_formula": "0.70 × (100 − pressure) + 0.30 × strategic_gap_potential",
        "stress_tests": [
            {
                "id": "bang-pakok-plus-one-direct-high-impact",
                "status": "noncanonical_sensitivity_scenario",
                "candidate_id": "bang-pakok",
                "assumption": (
                    "The completed census finds one additional independent "
                    "high-impact direct-routine community mall at 1.0 km."
                ),
                "additional_pressure_load": round(added_direct_load, 4),
                "modeled_pressure_load": round(stress_total_load, 4),
                "modeled_supply_pressure": round(stress_pressure, 2),
                "modeled_strategic_gap_potential": stress_strategic_gap,
                "modeled_competitive_room_score": round(stress_room, 2),
                "modeled_evidence_readiness_score": (
                    bang_pakok["evidence_readiness_score"]
                ),
                "modeled_action_tier": stress_action["tier"],
                "interpretation": (
                    "Bang Pakok is a provisional field-validation priority, "
                    "not a robust investment winner. Complete the competitor "
                    "census before treating Tier A as stable."
                ),
            }
        ],
        "candidates": breakdown_rows,
    }
    return metrics, breakdown


def main() -> int:
    metrics, breakdown = build()
    METRICS_PATH.write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    BREAKDOWN_PATH.write_text(
        json.dumps(breakdown, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"WROTE {METRICS_PATH}")
    print(f"WROTE {BREAKDOWN_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
