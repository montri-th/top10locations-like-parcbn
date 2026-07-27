# Top 10 Locations Like PARC Bangna

Release 1.6 is a static executive report for screening Bangkok locations that may support a concept inspired by PARC Bangna. It keeps the comparable-catchment ranking from Release 1.5 and adds an evidence-bounded view of operating shopping-center supply.

Production: <https://montri-th.github.io/top10locations-like-parcbn/>

## Release 1.6

- Preserves the canonical Top 10 and scores from Release 1.5.
- Adds a separate competition diagnostic: verified operating venues, cluster-deduplicated supply pressure, competitive room, evidence readiness, and action tier.
- Keeps the illustrative `80% baseline + 20% competitive room` scenario visibly noncanonical.
- Uses 23 venues in a preliminary minimum-verified registry. It is not a completeness-certified competitor census.
- Renders 45 candidate–competitor marker instances with high-confidence venue coordinates.
- Retains Market Place Pracha Uthit and Esplanade Ratchada in the evidence tables but withholds their markers because the available coordinates are tenant proxies.

The current field-work priority is **Bang Pakok / บางปะกอก (Tier A)**. This is not a final investment winner: parcel, access, network travel, legal, financial, and field evidence remain open.

## Canonical result

| Rank | Location | Baseline score |
|---:|---|---:|
| 1 | วงเวียนใหญ่–ตะวันออก | 52.71 |
| 2 | เจริญราษฎร์ | 52.61 |
| 3 | สำเหร่ | 52.31 |
| 4 | แยกบ้านแขก | 51.46 |
| 5 | ตลาดพลู–ใต้ | 48.44 |
| 6 | บางปะกอก | 47.02 |
| 7 | วังหลัง | 45.74 |
| 8 | ราชเทวี | 44.14 |
| 9 | ประชาอุทิศ | 43.78 |
| 10 | ดินแดง | 43.57 |

Every baseline candidate uses Venue Locale Insight release `v2.3.1` and the same fixed-area analytical catchment: `26.3154 km²`, radius `2.89421 km`.

## Public artifacts

- [`index.html`](index.html) — static interactive report
- [`PARC_Bangna_Bangkok_Top_10_Release_1_6_Competitive_Report_2026-07-28.html`](PARC_Bangna_Bangkok_Top_10_Release_1_6_Competitive_Report_2026-07-28.html) — named HTML copy of the approved release
- [`analysis/PARC_Bangna_Bangkok_Top_10_Release_1_6_Competition_Analysis_and_UXUI_2026-07-28.md`](analysis/PARC_Bangna_Bangkok_Top_10_Release_1_6_Competition_Analysis_and_UXUI_2026-07-28.md) — full analysis and UX/UI specification
- [`analysis/location-payload.json`](analysis/location-payload.json) — source-to-render report contract
- [`analysis/map-manifest.json`](analysis/map-manifest.json) — geometry, layer, omission, and accessibility contract
- [`analysis/competitor-registry.public.json`](analysis/competitor-registry.public.json) — sanitized public evidence registry
- [`analysis/competitor-score-breakdown.json`](analysis/competitor-score-breakdown.json) — competition calculations

The internal registry containing connector locators is intentionally gitignored and is not a public artifact.

## Map integrity

The overview and ten detail maps use one consistent kilometre projection. Detail maps show only:

- the standardized analytical circle;
- the Release 1.5 analytical center, explicitly not a parcel;
- competitor points with high coordinate confidence;
- north and a scale bar.

Roads, rail lines, stations, inferred polygons, sampled restaurant dots, and decorative POIs are omitted because this release does not carry sufficient feature-level lineage to render them credibly. Marker size uses an operator-reported metric when available; otherwise it uses a disclosed analytical impact class. The marker population is therefore not one common GLA scale.

## UX/UI

The page follows J Lifestyle Center Design System v0.3:

- self-hosted Anuphan 300 and IBM Plex Sans Thai Looped 400/500 WOFF2 assets;
- canonical Canvas, Card, Garden, Ink, and approved dark tokens;
- opaque sticky header, readable Thai typography, visible control boundaries, and 44 px minimum targets;
- transparent positive and reverse PARC logo derivatives selected by rendered surface;
- one clean, quiet theme control.

Theme starts at **System** on a fresh visit. Each press cycles:

`System → explicit theme opposite the current OS theme → the other explicit theme → System`

The icon, accessible label, logo derivative, and browser theme colour follow the active state. System mode continues to respond to an OS theme change.

## Build and verification

```bash
python3 scripts/build_public_registry.py
python3 scripts/build_analysis.py
python3 scripts/build_contracts.py
python3 scripts/build_site.py
python3 scripts/validate_contracts.py
python3 scripts/qa_static.py
```

The installed location-payload and location-report validators are also run during release QA. Rendered and post-publish evidence is recorded in [`qa/release-1.6-qa.md`](qa/release-1.6-qa.md).

## Decision boundary

Competition pressure and strategic gaps are diagnostic, not direct observations of sales, traffic, occupancy, vacancy, service quality, or tenant weakness. The registry is a minimum verified set and straight-line distance ignores bridges, boats, road travel, congestion, and pedestrian barriers.

Before any parcel or investment decision, complete the competitor census, validate the two held centroids, rerun network catchments where rivers or dense clusters matter, and inspect candidate parcels, access, zoning, flood exposure, economics, and real operating evidence.

Font assets are distributed under their bundled Open Font License files in [`assets/fonts`](assets/fonts).
