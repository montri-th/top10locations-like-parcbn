# PARC Bangna — Fresh Locale Screen

Production: <https://montri-th.github.io/top10locations-like-parcbn/>

The current landing page is the **Board Decision Tool v3.6 release**, dated 3 August 2026. It is an executive-first working tool for the CEO, CFO, and Board to decide which locations deserve field validation for the next PARC—not to review model mechanics.

Release provenance is split deliberately: **v3.3 is the frozen analytical/data release**, **reference analysis v0.1** is the separately governed Sri Iam comparison and 574-locale ranking, and **v3.6 is the executive-story interface release**. The v3.6 builder preserves both embedded payloads byte-for-byte while changing only information order and decision copy.

## Decision requested

Approve field and feasibility validation of four locations first: **เอกมัย-ใต้, วังหิน-ใต้, สัมมากร, and พระราม 3-ตะวันออก**. This is approval for the next evidence stage—not approval to select a parcel, acquire land, or invest.

The study must return with route-based catchments, crossing and ramp logic, verified competitive supply, parcel feasibility, preliminary economics, downside scenarios, and explicit stop reasons.

## Four-location recommendation, four questions, and the prior-portfolio test

The interface leads with the four-location recommendation, the reason each location merits work, the neighbourhood-level land-price warning, and the exact approval boundary. It then reduces the first eight analytical lenses to four questions for the proposed locations: resident base, accessible routine, barrier-aware access, and market position. Answer stability is shown separately as a test of the previous A–J portfolio, not as evidence that the four new recommendations passed those 13 scenarios. The original nine formulas remain available in a collapsed audit trail.

The live simulator is now placed before the long evidence panels. It lets the reader change the four validated Balanced-model weights, barrier assumption, unknown-supply assumption, and market interpretation. It recalculates and reorders the **previous A–J portfolio** in the browser; A–J is explicitly not the current approval request. The tool does **not** claim to recalculate a new rank across all 574 comparable locales because the public payload contains only the ten portfolio rows and six reserves. Component percentiles use the frozen 745-locale base; published candidate ranks are within the 574-locale comparable lane.

The portfolio is not the Top 10 from one all-variable score. Its candidate pool combines nine ranked lenses:

- Fresh baseline;
- resident depth;
- accessible routine;
- activity;
- white-space builder;
- observed-supply challenger;
- demand plus routine;
- barrier-resilient demand;
- balanced full model.

The candidate pool takes the Top 20 from every lens, then applies portfolio quotas: three anchors, three white-space builders, three observed-supply challengers, and one barrier experiment. References A–J identify study hypotheses; they are not ranks.

## Sri Iam reference and benchmark boundary

PARC Bangna does not have a locale row in the 806-record Registry. The 22 excluded records are 12 active primary context locales and ten controlled corridors—not PARC plus 21 branches. They remain outside candidate ranking because they are reference contexts, overlap one another, and are not customer-origin observations.

The reference analysis uses **ศรีเอี่ยม** because it is the locale in the governed dataset whose sampled point is nearest to PARC Bangna (0.30 km). It is scored outside the candidate pool against the frozen 745-locale distributions and shown as an unranked reference. The interface calls it a temporary neighbourhood reference—not a PARC score—and separates contextual similarity from the strength of the candidate neighbourhood before producing a validation queue.

This is not an exact PARC venue or trade-area benchmark. That requires an approved PARC reference geometry and raw inputs aggregated with the same observation unit, venue release, and barrier assumptions. Operating receipts, tenants, traffic, parking, and customer behaviour remain validation evidence and are never candidate features.

## Competition and barriers

Venue Locale Insight is used across the full eligible universe. Existing retail supply has two valid readings:

- **pressure**: incumbent supply may reduce available headroom;
- **market-validation hypothesis**: observed supply may indicate established retail behaviour, while still requiring verification of competitor quality, overlap, and strategic gaps.

The release does not claim that competitor presence proves demand or performance. Unknown venue size is imputed by subtype median for screening and remains visibly uncertain.

River and expressway awareness is calculated as a geometric separation proxy. The central screen discounts separated demand by 55% for the Chao Phraya River and 20% for motorways; optimistic and conservative assumptions are included in 13 one-at-a-time sensitivity scenarios. Detailed study must replace the proxy with a frozen route graph and approved crossing/ramp registry.

## Map integrity

- The overview uses 169 simplified Bangkok khwaeng polygons from the 2018 `pcrete/gsvloader-demo` snapshot as historical orientation context, not current legal boundaries.
- River and motorway overlays come from dated OpenStreetMap extracts and are pinned in the source manifest.
- One reusable MapLibre detail map uses local Positron and Dark style snapshots, with a nonblank static fallback and accessible competitor tables.
- Overview and fallback SVGs use bounded, centered contain rendering so map evidence and labels are not cropped on desktop or mobile.
- Competitor-dialog controls use fixed grid areas, so hiding the back control cannot collapse long venue names into the 44 px control column.
- Root-art and map sizing selectors use direct-child contracts, so nested outline icons keep their component size and state.
- Basemap context is not scoring evidence and no parcel, locale extent, or drive-time catchment is invented.

## Humanized interface and live research

- Thai copy follows a practitioner flow: what is visible, what it may mean, and what must be checked next.
- The page has one approval request only: validate four named locations; the former A–J portfolio is retained as an assumption-testing and evidence layer.
- Technical terms such as host-locale proxy, harmonic mean, and provenance are kept out of the executive path and remain available only in method disclosures.
- Rounded-outline icons carry repeated concepts so the page does not rely on dense labels alone.
- Every rendered competitor row offers a research action with four user intents: latest moves, market perception, tenant mix, or access/parking.
- The interface routes latest moves and access/parking to Google Search for direct-source discovery, while market perception and tenant mix use Google AI Mode for synthesis. The split is visible before activation and remains two Search plus two AI choices for every competitor.
- The exact Thai query or question is editable before a new tab opens. Search and AI results remain discovery-only context; AI citations, dates, and branch identity must be checked, and no external result modifies the frozen release score or evidence payload.
- The supplied butterfly and bougainvillea stock references are not embedded; the release uses its original cleared line/bract motif.

## Current artifacts

- [`index.html`](index.html) — production landing page
- [`PARC_Bangna_Fresh_Locale_Screen_Board_Decision_Tool_v3.6_Executive_Story_2026-08-03.html`](PARC_Bangna_Fresh_Locale_Screen_Board_Decision_Tool_v3.6_Executive_Story_2026-08-03.html) — named v3.6 HTML checkpoint
- [`PARC_Bangna_Fresh_Locale_Screen_Board_Decision_Tool_v3.5_PARC_Core_Fit_Preview_2026-08-01.html`](PARC_Bangna_Fresh_Locale_Screen_Board_Decision_Tool_v3.5_PARC_Core_Fit_Preview_2026-08-01.html) — named v3.5 HTML checkpoint
- [`PARC_Bangna_Fresh_Locale_Screen_Board_Decision_Tool_v3.4_2026-07-31.html`](PARC_Bangna_Fresh_Locale_Screen_Board_Decision_Tool_v3.4_2026-07-31.html) — named HTML checkpoint
- [`analysis/PARC_Bangna_Host_Proxy_Core_Fit_Preview_v0.1_2026-08-01.md`](analysis/PARC_Bangna_Host_Proxy_Core_Fit_Preview_v0.1_2026-08-01.md) — calculation, validation, limits, and decision readout
- [`analysis/parc-host-proxy-core-fit-preview-v0.1.json`](analysis/parc-host-proxy-core-fit-preview-v0.1.json) — machine-readable preview release
- [`analysis/PARC_Bangna_Fresh_Locale_Screen_Multi_Lens_Board_Brief_v0.4_2026-07-28.md`](analysis/PARC_Bangna_Fresh_Locale_Screen_Multi_Lens_Board_Brief_v0.4_2026-07-28.md) — analysis and Board brief
- [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) — third-party data and software notices

Build and release gates:

```bash
python3 scripts/build_v3_6_board_story.py
python3 scripts/qa_v3_6.py
python3 scripts/recompute_parc_core_fit_preview.py /path/to/v2.3.1-registry.xlsx
PARC_CHROMIUM_EXECUTABLE=/path/to/chromium node scripts/qa_v3_6_rendered.cjs
```

The named HTML is a self-contained decision artifact. It embeds the canonical
source-to-render payload, the 169-khwaeng overview, dated river and motorway
overlays, local MapLibre runtime, light/dark style snapshots, static fallback,
and the source/runtime integrity hashes used by release QA.

The named HTML and `index.html` must remain byte-identical. Earlier releases remain in the repository as audit history and do not define the current landing page.
