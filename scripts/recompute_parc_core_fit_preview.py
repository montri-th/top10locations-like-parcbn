#!/usr/bin/env python3
"""Recompute and verify the v3.5 PARC host-proxy core-fit preview.

Input is an XLSX export of `ijji Locale Intelligence Registry v1.0`
(source release v2.3.1). The script never adds the PARC reference contexts to
the candidate universe: it scores ศรีเอี่ยม out-of-sample against the frozen
745 rows, then ranks only the 574 comparable locales.

Example:
    python3 scripts/recompute_parc_core_fit_preview.py /path/to/registry.xlsx
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CHECKED_RESULT = ROOT / "analysis/parc-host-proxy-core-fit-preview-v0.1.json"
HOST_ID = "7430567c-5878-422e-97ba-2dbad5f0d9fe"
READY = {"READY", "READY_WITH_COSMETIC_QA_NOTE"}
COMPARABLE = {
    "residential_general",
    "market_residential",
    "school_led_residential",
    "condo_delivery",
    "hospital_adjacent",
}
PARC_CONTEXT_IDS = {
    "7430567c-5878-422e-97ba-2dbad5f0d9fe",
    "01cb2e1c-7985-4afa-b071-20311662d47c",
    "2e954b95-8166-49ed-90a2-e7423697e3ca",
    "7fa1b232-c721-4e58-b599-2ca8dac81ca2",
    "01e92f9e-efec-4655-b28f-981ddce4d688",
    "7a058463-e49f-4565-a250-9dc62013a13b",
    "f9e593d6-48ec-4fd3-9597-c9ea54722a41",
    "71432a68-7978-4d55-9306-049d6109276e",
    "53d8daa4-0f9b-46e1-8c76-c08cb036008a",
    "4ee32851-b9f2-4cdb-92e9-4937e1927f26",
    "fac047df-edfd-4442-b8a8-211bb0130b40",
    "72f4cc35-4296-467b-9bee-f48df4f886f3",
    "70f2187a-914e-44a3-abfa-c7f3270242cc",
    "46e48298-a414-48ad-a34e-82b887069758",
    "3a84763b-0a02-4033-8e1c-a9741a69cfda",
    "dc38403e-93a7-4434-a6e0-9fdfb0788598",
    "cf9cb548-d8aa-4cfd-b5e4-5ded7345e50b",
    "76f73a51-e384-4bbd-9dcd-b7392e7149d3",
    "630f0d84-9c37-4007-93da-326210c2161b",
    "65eb1a73-a15b-451d-99bd-6cc946f0b399",
    "ec486181-ead5-44be-8780-cfd861ff15e0",
    "6d527037-7266-4181-8293-4c58a2b56fa2",
}


def structural_zero(total: pd.Series, count: pd.Series) -> pd.Series:
    """Fill only count=0/null-total rows with a true structural zero."""
    result = pd.to_numeric(total, errors="coerce")
    return result.mask(result.isna() & pd.to_numeric(count, errors="coerce").eq(0), 0.0)


def percentile(series: pd.Series, *, force_raw_zero: bool = False) -> pd.Series:
    result = series.rank(method="average", pct=True) * 100
    if force_raw_zero:
        result = result.mask(series.eq(0), 0.0)
    return result


def frozen_oos_percentile(
    distribution: pd.Series, value: float, *, force_raw_zero: bool = False
) -> float:
    observed = distribution.dropna()
    if force_raw_zero and value == 0:
        return 0.0
    return 100 * (observed.lt(value).sum() + 0.5 * observed.eq(value).sum()) / len(observed)


def institution(row: pd.Series) -> float:
    values = row[["p_student", "p_beds", "p_office"]].dropna().sort_values(ascending=False)
    if values.empty:
        return math.nan
    if len(values) == 1:
        return float(values.iloc[0])
    return float(0.65 * values.iloc[0] + 0.35 * values.iloc[1])


def harmonic(similarity: pd.Series, opportunity: pd.Series, weight_similarity: float) -> pd.Series:
    return 1 / (weight_similarity / similarity + (1 - weight_similarity) / opportunity)


def ordinal_ranks(frame: pd.DataFrame, score: str) -> pd.Series:
    ordered = frame.sort_values([score, "locale_id"], ascending=[False, True], kind="mergesort")
    return pd.Series(range(1, len(ordered) + 1), index=ordered.index)


def build(registry_xlsx: Path) -> dict[str, object]:
    index = pd.read_excel(registry_xlsx, sheet_name="01_LOCALE_INDEX")
    facts = pd.read_excel(registry_xlsx, sheet_name="02_MEASURED_FACTS")
    if index["locale_id"].duplicated().any() or facts["locale_id"].duplicated().any():
        raise ValueError("locale_id must be unique in both required sheets")
    merged = index.merge(facts, on=["locale_id", "locale_name_th"], how="inner", validate="one_to_one")
    if len(merged) != 806:
        raise ValueError(f"expected 806 joined Registry rows, got {len(merged)}")

    host = merged.loc[merged["locale_id"].eq(HOST_ID)].iloc[0].copy()
    universe = merged.loc[
        merged["operational_status"].isin(READY)
        & pd.to_numeric(merged["restaurant_count"], errors="coerce").gt(0)
        & ~merged["locale_id"].isin(PARC_CONTEXT_IDS)
    ].copy()
    if len(universe) != 745:
        raise ValueError(f"expected frozen universe 745, got {len(universe)}")

    for frame in (universe,):
        frame["population"] = pd.to_numeric(frame["population_total"], errors="coerce")
        frame["density"] = frame["population"] / pd.to_numeric(frame["area_sqkm"], errors="coerce")
        frame["activity"] = pd.to_numeric(frame["restaurant_total_ratings"], errors="coerce")
        frame["grocery"] = structural_zero(frame["grocery_total_sales_area_sqm"], frame["grocery_count"])
        frame["student"] = structural_zero(frame["students_total"], frame["school_count"])
        frame["beds"] = structural_zero(frame["hospital_total_beds"], frame["hospital_count"])
        office_avg = pd.to_numeric(frame["office_avg_gla_sqm"], errors="coerce")
        office_count = pd.to_numeric(frame["office_count"], errors="coerce")
        frame["office"] = office_count * office_avg
        frame["office"] = frame["office"].mask(frame["office"].isna() & office_count.eq(0), 0.0)
        frame["land"] = pd.to_numeric(frame["median_land_price_thb_sqw"], errors="coerce")

    universe["p_population"] = percentile(universe["population"])
    universe["p_density"] = percentile(universe["density"])
    universe["p_activity"] = percentile(universe["activity"])
    universe["p_grocery"] = percentile(universe["grocery"], force_raw_zero=True)
    universe["p_student"] = percentile(universe["student"], force_raw_zero=True)
    universe["p_beds"] = percentile(universe["beds"], force_raw_zero=True)
    universe["p_office"] = percentile(universe["office"], force_raw_zero=True)
    universe["p_land"] = percentile(universe["land"])
    universe["resident"] = np.sqrt(universe["p_population"] * universe["p_density"])
    universe["institution"] = universe.apply(institution, axis=1)
    universe["routine_breadth"] = 0.55 * universe["p_grocery"] + 0.45 * universe["institution"]
    universe["accessible_routine"] = 0.65 * universe["routine_breadth"] + 0.35 * universe["p_activity"]

    host_raw = {
        "population": float(host["population_total"]),
        "density": float(host["population_total"] / host["area_sqkm"]),
        "activity": float(host["restaurant_total_ratings"]),
        "grocery": float(host["grocery_total_sales_area_sqm"]),
        "student": float(host["students_total"]),
        "beds": 0.0 if pd.isna(host["hospital_total_beds"]) and host["hospital_count"] == 0 else float(host["hospital_total_beds"]),
        "office": float(host["office_count"] * host["office_avg_gla_sqm"]),
        "land": float(host["median_land_price_thb_sqw"]),
    }
    p_host = {
        key: frozen_oos_percentile(
            universe[key], value, force_raw_zero=key in {"grocery", "student", "beds", "office"}
        )
        for key, value in host_raw.items()
    }
    host_resident = math.sqrt(p_host["population"] * p_host["density"])
    host_institution = 0.65 * max(p_host["student"], p_host["beds"], p_host["office"]) + 0.35 * sorted(
        [p_host["student"], p_host["beds"], p_host["office"]], reverse=True
    )[1]
    host_breadth = 0.55 * p_host["grocery"] + 0.45 * host_institution
    host_activity = p_host["activity"]
    host_accessible = 0.65 * host_breadth + 0.35 * host_activity
    host_fresh = 0.55 * host_resident + 0.25 * host_breadth + 0.20 * host_activity

    comparable = universe.loc[universe["peer_archetype"].isin(COMPARABLE)].copy()
    if len(comparable) != 574:
        raise ValueError(f"expected comparable lane 574, got {len(comparable)}")
    comparable["similarity"] = 100 - (
        0.55 * (comparable["resident"] - host_resident).abs()
        + 0.25 * (comparable["routine_breadth"] - host_breadth).abs()
        + 0.20 * (comparable["p_activity"] - host_activity).abs()
    )
    comparable["opportunity"] = (
        0.55 * comparable["resident"]
        + 0.25 * comparable["routine_breadth"]
        + 0.20 * comparable["p_activity"]
    )
    for label, weight in (("40", 0.40), ("50", 0.50), ("60", 0.60)):
        comparable[f"harmonic_{label}"] = harmonic(comparable["similarity"], comparable["opportunity"], weight)
        comparable[f"rank_{label}"] = ordinal_ranks(comparable, f"harmonic_{label}")

    central = comparable.sort_values(["harmonic_50", "locale_id"], ascending=[False, True]).head(10)
    top_10 = []
    for _, row in central.iterrows():
        ranks = [int(row["rank_40"]), int(row["rank_50"]), int(row["rank_60"])]
        top_10.append(
            {
                "locale_id": row["locale_id"],
                "locale_name_th": row["locale_name_th"],
                "resident": round(float(row["resident"]), 4),
                "routine_breadth": round(float(row["routine_breadth"]), 4),
                "activity": round(float(row["p_activity"]), 4),
                "similarity": round(float(row["similarity"]), 4),
                "opportunity": round(float(row["opportunity"]), 4),
                "decision_score": round(float(row["harmonic_50"]), 4),
                "ranks_40_50_60": ranks,
                "rank_range_40_50_60": [min(ranks), max(ranks)],
                "land_price_thb_sqw": None if pd.isna(row["land"]) else int(row["land"]),
                "land_price_percentile": None if pd.isna(row["p_land"]) else round(float(row["p_land"]), 4),
            }
        )

    return {
        "counts": {"registry": len(merged), "universe": len(universe), "comparable": len(comparable)},
        "reference": {
            "resident": round(host_resident, 4),
            "routine_breadth": round(host_breadth, 4),
            "activity": round(host_activity, 4),
            "accessible_routine": round(host_accessible, 4),
            "fresh_core_opportunity": round(host_fresh, 4),
        },
        "top_10": top_10,
    }


def verify(calculated: dict[str, object]) -> None:
    checked = json.loads(CHECKED_RESULT.read_text(encoding="utf-8"))
    expected_reference = checked["reference"]["scores_out_of_sample_against_frozen_745"]
    for key, expected in expected_reference.items():
        if not math.isclose(calculated["reference"][key], expected, abs_tol=0.0001):
            raise AssertionError(f"reference {key}: {calculated['reference'][key]} != {expected}")
    expected_rows = checked["top_10_core_fit_before_route_site_and_economics_gates"]
    if [row["locale_id"] for row in calculated["top_10"]] != [row["locale_id"] for row in expected_rows]:
        raise AssertionError("Top 10 locale order differs from the checked release")
    numeric = ["resident", "routine_breadth", "activity", "similarity", "opportunity", "decision_score"]
    for actual, expected in zip(calculated["top_10"], expected_rows, strict=True):
        for key in numeric:
            if not math.isclose(actual[key], expected[key], abs_tol=0.0001):
                raise AssertionError(f"{actual['locale_name_th']} {key}: {actual[key]} != {expected[key]}")
        if actual["ranks_40_50_60"] != expected["ranks_40_50_60"]:
            raise AssertionError(f"{actual['locale_name_th']} sensitivity ranks differ")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("registry_xlsx", type=Path)
    parser.add_argument("--print-json", action="store_true", help="print the recomputed audit payload")
    args = parser.parse_args()
    calculated = build(args.registry_xlsx)
    verify(calculated)
    print("PASS — Registry 806 / score base 745 / comparable lane 574")
    print("PASS — host-proxy components and 574-lane Top 10 match the checked release")
    if args.print_json:
        print(json.dumps(calculated, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
