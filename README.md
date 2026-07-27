# Top 10 Locations Like PARC Bangna

Interactive single-page executive report for screening Bangkok areas that may support a food-led neighborhood center like PARC Bangna.

## Open the report

Open [`index.html`](index.html). The static page includes embedded Thai fonts, CSS, JavaScript, executive maps, comparison charts, filters, evidence disclosures, light/dark themes, and print styles. The header uses the approved PARC Bangna logo.

Production: <https://montri-th.github.io/top10locations-like-parcbn/>

## Scope

This release supersedes the previous ranking. Candidate scores and conclusions are recalculated from source evidence.

The calculation uses:

- `Project brief - PARC Bangna(1).md` to define the intended shops and PARC experience
- a versioned location-evidence dataset, release `v2.3.1`, for area-level demand evidence
- the `P A R C Project Pack` for release metadata, the reference catchment size, and the 22 active areas excluded from the alternative-location search
- `J Lifestyle Center Design System v0.3` for the web presentation

It does not use prior corridor rankings, PARC operating performance, POS, parking utilization, or customer-origin evidence.

## Scoring

- Every candidate uses an equal-area screening catchment of `26.3154 km²` (radius `2.894 km`), comparable with the PARC Bangna reference.
- All coordinate-qualified surrounding records inside that catchment contribute to the demand indices. Nearby records receive more weight than distant records.
- `Catchment demand = 0.50 nearby residents + 0.30 people coming from outside + 0.20 daytime reasons to visit`
- `PARC fit = shop fit^0.60 × experience fit^0.40`
- `Overall score = catchment demand × PARC fit / 100`

The model uses weighted averages rather than adding population, reviews, students, patients, or workers across overlapping source areas. The daytime index comes from office, school, hospital, and factory anchors; it is not an observed traveller count. Restaurant-market evidence is used as an analogue for a food-led center, not as measured shopping-center visits or sales.

## Result

1. วงเวียนใหญ่-ตะวันออก
2. เจริญราษฎร์
3. สำเหร่
4. แยกบ้านแขก
5. ตลาดพลู-ใต้
6. บางปะกอก
7. วังหลัง
8. ราชเทวี
9. ประชาอุทิศ
10. ดินแดง

The leading group remains within the Top 4 across all five tested catchment/weighting cases. ตลาดพลู-ใต้ remains rank 5 in all five. ราชเทวี, ประชาอุทิศ, and ดินแดง are more sensitive to model assumptions and require stronger field evidence.

## Evidence drill-down

Each Top 10 location can be opened from a visible evidence action in the comparison chart or its ranking card. The disclosure shows:

- a simplified context map with a clearly labelled fallback extent, selected major roads, and active rail/BRT lines and stations where present
- the exact bridge from catchment demand × PARC fit to the overall score
- indices for nearby residents, people coming from outside, and daytime reasons to visit
- evidence for the intended shops and the PARC experience
- the six surrounding records contributing most to the catchment result
- ranks under all five catchment/weighting cases
- the offer to test, what could change the decision, and the next field action

## Map context and boundary

The overview map locates all Top 10 areas across the full Bangkok administrative extent and links to each evidence disclosure. It intentionally omits roads, transit lines, and screening-catchment circles.

Each local map currently uses a clearly labelled fallback extent: a convex hull around the available coordinate-qualified evidence points for that location. The source outputs confirm that a strict upstream polygon exists and provide its area, but the public release files do not contain the coordinate rings needed to draw it faithfully. The fallback is therefore dashed and subdued rather than presented as the supplied location boundary.

The map fits to that fallback with modest context padding, then adds at most two locally useful major roads and active rail/BRT context from the static OpenStreetMap snapshot. It does not show the individual sampled venue points, secondary street networks, lanes, or landmarks.

The evidence polygon is not the equal-area catchment used by the scoring model. It is also not a land-plot boundary, an administrative boundary, a drive-time isochrone, or a confirmed trade area. The scores continue to use the comparable `26.3154 km²` catchment described above.

Bangkok subdistrict geometry is adapted from [`pcrete/gsvloader-demo`](https://github.com/pcrete/gsvloader-demo) under the MIT License, copyright © 2018 Poom Wettayakorn. The full permission notice is preserved in `index.html`.

Roads, rail/BRT context, and active stations are from [OpenStreetMap](https://www.openstreetmap.org/copyright), © OpenStreetMap contributors, under the Open Database License. The map snapshot is dated 27 July 2026.

## Decision boundary

The ranking prioritizes where to search for plots and gather evidence. It does not approve a plot, land purchase, lease, development, or investment.

Parking, frontage, ingress/egress, visibility, U-turn access, plot size, zoning, flood exposure, shops needed at different times of day, competition, and real-estate economics must still be checked.

## Verification

- 173 format-gated location records; 173 unique IDs
- 776 coordinate-qualified records contribute to the catchment calculation
- Base-score reconciliation within 0.05 points
- Top 10 and five catchment/weighting cases validated in a sequential Python run
- Responsive browser checks at 320, 390, 720, 768, 1024, and 1440 CSS pixels
- 2 responsive full-Bangkok overview projections, 10 local maps, 10 clearly labelled fallback extents, and 20 overview markers verified in the rendered page
- zero overview roads, rail lines, stations, landmarks, or catchment circles
- zero local-map sampled venue dots, catchment circles, landmarks, uncurated secondary street networks, or road labels beginning with `ซอย`
- 10 evidence actions in the comparison chart and 10 full-width disclosure actions with icons, visible labels, and open-state chevrons
- Overview-map selection opens the corresponding evidence disclosure
- Embedded Thai font checks for Anuphan 200 and IBM Plex Sans Thai Looped 400/500
- Device-theme default, light/dark controls, comparison-to-disclosure navigation, filter, disclosure, print, reduced-motion, and keyboard-focus checks

Release 1.5 · Clear evidence actions, reduced text, and cleaner local maps · 27 July 2026
