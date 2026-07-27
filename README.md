# Top 10 Locations Like PARC Bangna

Interactive single-page executive report for a clean-room screening of Bangkok areas that may support a food-led neighborhood center like PARC Bangna.

## Open the report

Open [`index.html`](index.html). It is a self-contained static page with embedded Thai fonts, CSS, JavaScript, executive maps, comparison charts, filters, evidence disclosures, and print styles.

Production: <https://montri-th.github.io/top10locations-like-parcbn/>

## Clean-room scope

This release supersedes the previous ranking and does not reuse its candidate scores or conclusions.

The calculation uses:

- `Project brief - PARC Bangna(1).md` to define the tenant-mix and PARC-experience offering
- a versioned location-evidence dataset, release `v2.3.1`, for demand evidence
- the `P A R C Project Pack` only for release metadata and the 22 active areas excluded from the alternative-location search
- `J Lifestyle Center Design System v0.3` for the web presentation

It does not use PARC Samyot, Live Ramintra, prior corridor rankings, PARC operating performance, POS, parking utilization, or customer-origin evidence.

## Scoring

- `Traffic = 0.50 Residents + 0.30 Visitors + 0.20 Daytime-Origin Proxy`
- `Offering PMF = Tenant Mix Fit^0.60 × PARC Experience Fit^0.40`
- `Location PMF Index = Traffic × Offering PMF / 100`

The Daytime-Origin Proxy is derived from office, school, hospital, and factory anchors. It is not measured commuter traffic. Restaurant-market location evidence is used as a demand analogue for a food-led center, not as observed shopping-center footfall or sales.

## Result

1. ตลาดพลู-ใต้
2. แยกบ้านแขก
3. วังหิน-ใต้
4. วังหลัง
5. เจริญราษฎร์
6. สำเหร่
7. คลองตัน-ตะวันตก
8. บางปะกอก
9. บางซ่อน
10. บางขุนนนท์-ใต้

The first two locations remain ranks 1 and 2 across all five tested weighting scenarios. Ranks 3–10 require parcel and field validation.

## Evidence drill-down

Each Top 10 location can be opened from the comparison chart or its ranking card. The disclosure shows:

- a local context map with the verified evidence extent, reference points, subdistrict context, center coordinates, and study-area size
- the exact score bridge from Traffic × Offering PMF to Location PMF
- Residents, Visitors, and Daytime-Origin Proxy values with ranks within the Top 10
- Food, Routine/Errand, Family, Wellness, and Connector fit
- Multi-mission breadth, Daypart breadth, and PARC Experience Fit
- ranks under all five sensitivity scenarios
- visitor/daytime evidence coverage, restaurant/review percentiles, area population and size, QA status, and source ID
- the offering to test, the gate that may change the verdict, and the next evidence-gathering action

## Map evidence boundary

The overview map locates all Top 10 areas and links directly to each evidence disclosure. Each local map shows a derived convex hull around reference points verified as being inside the study area.

The derived extent is deliberately not presented as the original study polygon, a land-plot boundary, an administrative boundary, or a customer catchment. Exact source-polygon coordinates were not available in the release used to build the public page.

Bangkok subdistrict geometry is adapted from [`pcrete/gsvloader-demo`](https://github.com/pcrete/gsvloader-demo) under the MIT License, copyright © 2018 Poom Wettayakorn. The full permission notice is preserved in `index.html`.

## Decision boundary

The ranking prioritizes area-level parcel search and evidence gathering. It does not approve a plot, land purchase, lease, development, or investment.

Parking, frontage, ingress/egress, visibility, U-turn access, parcel size, zoning, flood exposure, tenant-by-daypart offering, competition, and real-estate economics remain hard validation gates.

## Verification

- 173 format-gated location records; 173 unique IDs
- Base-score reconciliation within 0.05 points
- Top 10 and five sensitivity scenarios validated in a sequential Python run
- Responsive browser checks at 320, 390, 720, 768, 1024, and 1440 CSS pixels
- 2 responsive overview-map projections, 10 local maps, 10 derived extents, and 20 overview markers verified in the rendered page
- Overview-map selection opens the corresponding evidence disclosure
- Embedded Thai font checks for Anuphan 200 and IBM Plex Sans Thai Looped 400/500
- Comparison-to-disclosure navigation, filter, disclosure, print, reduced-motion, and keyboard-focus checks

Clean-room Release 1.2 · Executive location maps · 27 July 2026
