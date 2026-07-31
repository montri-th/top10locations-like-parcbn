# PARC Bangna — Fresh Locale Screen

Production: <https://montri-th.github.io/top10locations-like-parcbn/>

The current landing page is the **Board Decision Tool v3.4 release**, dated 31 July 2026. It is an interactive working tool for CEO, CFO, and Board review of ten curated location hypotheses selected from 745 eligible Bangkok locales.

Release provenance is split deliberately: **v3.3 is the frozen analytical/data release**, while **v3.4 is the interface release**. The v3.4 builder preserves the embedded v3.3 analytical payload byte-for-byte and changes only the reading structure, interaction, metadata, and presentation.

## Decision requested

Approve detailed study of all ten opportunity hypotheses. This is approval for the next evidence stage—not approval to select a parcel, acquire land, or invest.

The study must return with route-based catchments, crossing and ramp logic, verified competitive supply, parcel feasibility, preliminary economics, downside scenarios, and explicit stop reasons.

## Five decision questions and live sensitivity

The reading structure reduces nine analytical lenses to five Board questions: resident base, accessible routine, barrier-aware access, market position, and answer stability. The original nine formulas remain available in a collapsed audit trail.

The live simulator lets the reader change the four validated Balanced-model weights, barrier assumption, unknown-supply assumption, and market interpretation. It recalculates and reorders the A–J portfolio in the browser. It does **not** claim to recalculate a new rank across all 745 locales because the public payload contains only the ten portfolio rows and six reserves.

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

## PARC Bangna benchmark gap

The interface reserves a visible reference row for PARC Bangna but does not invent a score. This exposes—rather than solves—the requested benchmark gap. PARC operating references were excluded from the 745 eligible locales to avoid selecting an existing project, and the PARC Locale Insight v2.3 source does not contain an approved percentile capsule for the same nine-lens release.

A defensible benchmark requires the approved PARC reference geometry and the same raw input fields, empirical distributions, venue release, and barrier assumptions used for v2.3.1. PARC must then be scored out-of-sample against the frozen 745-locale distribution and shown as an unranked reference. Operating performance evidence remains a separate benchmark and must not be blended into the locale opportunity score.

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
- Rounded-outline icons carry repeated concepts so the page does not rely on dense labels alone.
- Every rendered competitor row offers a research action with four user intents: latest moves, market perception, tenant mix, or access/parking.
- The interface routes latest moves and access/parking to Google Search for direct-source discovery, while market perception and tenant mix use Google AI Mode for synthesis. The split is visible before activation and remains two Search plus two AI choices for every competitor.
- The exact Thai query or question is editable before a new tab opens. Search and AI results remain discovery-only context; AI citations, dates, and branch identity must be checked, and no external result modifies the frozen release score or evidence payload.
- The supplied butterfly and bougainvillea stock references are not embedded; the release uses its original cleared line/bract motif.

## Current artifacts

- [`index.html`](index.html) — production landing page
- [`PARC_Bangna_Fresh_Locale_Screen_Board_Decision_Tool_v3.4_2026-07-31.html`](PARC_Bangna_Fresh_Locale_Screen_Board_Decision_Tool_v3.4_2026-07-31.html) — named HTML checkpoint
- [`analysis/PARC_Bangna_Fresh_Locale_Screen_Multi_Lens_Board_Brief_v0.4_2026-07-28.md`](analysis/PARC_Bangna_Fresh_Locale_Screen_Multi_Lens_Board_Brief_v0.4_2026-07-28.md) — analysis and Board brief
- [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) — third-party data and software notices

Build and release gates:

```bash
python3 scripts/build_v3_4_decision_tool.py
python3 scripts/qa_v3_4.py
PARC_CHROMIUM_EXECUTABLE=/path/to/chromium node scripts/qa_v3_4_rendered.cjs
```

The named HTML is a self-contained decision artifact. It embeds the canonical
source-to-render payload, the 169-khwaeng overview, dated river and motorway
overlays, local MapLibre runtime, light/dark style snapshots, static fallback,
and the source/runtime integrity hashes used by release QA.

The named HTML and `index.html` must remain byte-identical. Earlier releases remain in the repository as audit history and do not define the current landing page.
