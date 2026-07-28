# PARC Bangna — Fresh Locale Screen

Production: <https://montri-th.github.io/top10locations-like-parcbn/>

The current landing page is the **Competition-aware Board Explainer v2.0**, dated 28 July 2026. It is designed for CEO, CFO, and Board review of the exact Fresh Top 10 shortlist.

## Decision requested

Approve detailed study of all ten shortlisted locales. This is approval for the next evidence stage—not approval to choose a parcel, acquire land, or invest.

The study must return with:

- 10 locale dossiers;
- 3 market-overlap decisions;
- no more than 3–5 investment candidates;
- stop reasons, preliminary economics, and downside scenarios.

## Competition treatment

The release preserves the published Fresh baseline ranking and adds an evidence-bounded competition diagnostic:

- 23 mapped competitor records across 43 candidate–competitor relationships;
- categorical impact markers on one disclosed scale;
- verified leasable-area context only when a current primary source is available;
- unknown GLA, NLA, tenant count, or lifecycle status never treated as zero;
- no competition-adjusted rerank of all 745 locales until the registry, routing, crossing, and parent-complex rules are frozen consistently.

High competitor supply is not an automatic rejection. Each candidate states the proposition or route advantage that must be true and the kill test that should stop further work.

## Map integrity

The overview and ten interactive detail views use calibrated WGS84 presentation points and a visible kilometre-grid fallback. No approved khwaeng or locale GeoJSON/WKT was supplied, so the release does not invent administrative boundaries, locale extents, parcels, or catchments.

Competitor markers are keyboard accessible, open a detail panel with evidence links, and have table fallbacks. Marker radius uses one categorical impact-class scale; verified NLA or disclosed leasable area appears as separate numeric context.

## Current artifacts

- [`index.html`](index.html) — production landing page
- [`PARC_Bangna_Fresh_Locale_Screen_Board_Explainer_v2.0_Competition_Aware_2026-07-28.html`](PARC_Bangna_Fresh_Locale_Screen_Board_Explainer_v2.0_Competition_Aware_2026-07-28.html) — named HTML checkpoint
- [`analysis/PARC_Bangna_Fresh_Locale_Screen_Competition_Aware_Board_Brief_v0.2_2026-07-28.md`](analysis/PARC_Bangna_Fresh_Locale_Screen_Competition_Aware_Board_Brief_v0.2_2026-07-28.md) — competition-aware analysis and UX/UI brief
- [`analysis/fresh-competition-aware-payload-v2.json`](analysis/fresh-competition-aware-payload-v2.json) — source-to-render contract
- [`analysis/fresh-map-manifest-v2.json`](analysis/fresh-map-manifest-v2.json) — geometry, layer, fallback, and accessibility contract
- [`scripts/build_fresh_competition_v2.js`](scripts/build_fresh_competition_v2.js) — deterministic builder
- [`scripts/qa_fresh_competition_v2.js`](scripts/qa_fresh_competition_v2.js) — deterministic parity and integrity QA
- [`qa/viewport-harness.html`](qa/viewport-harness.html) — same-origin 390 px and 320 px rendered QA harness

## Rebuild and structural QA

```bash
node scripts/build_fresh_competition_v2.js
node scripts/qa_fresh_competition_v2.js
```

The named HTML and `index.html` must remain byte-identical. Earlier releases remain in the repository as audit history and do not define the current landing page.
