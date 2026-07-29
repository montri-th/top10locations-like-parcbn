# PARC Bangna — Fresh Locale Screen

Production: <https://montri-th.github.io/top10locations-like-parcbn/>

The current landing page is the **Multi-lens Opportunity Portfolio v3.2.4 mobile-dialog fix**, dated 29 July 2026. It is an executive explainer for CEO, CFO, and Board review of ten curated location hypotheses selected from 745 eligible Bangkok locales.

## Decision requested

Approve detailed study of all ten opportunity hypotheses. This is approval for the next evidence stage—not approval to select a parcel, acquire land, or invest.

The study must return with route-based catchments, crossing and ramp logic, verified competitive supply, parcel feasibility, preliminary economics, downside scenarios, and explicit stop reasons.

## Multi-lens selection

The portfolio is not the Top 10 from one all-variable score. It combines nine ranked lenses:

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
- The interface previews the exact Thai query before opening Google in a new tab. Live search results remain supplemental context and never modify the frozen release score or evidence payload.
- The supplied butterfly and bougainvillea stock references are not embedded; the release uses its original cleared line/bract motif.

## Current artifacts

- [`index.html`](index.html) — production landing page
- [`PARC_Bangna_Fresh_Locale_Screen_Board_Explainer_v3.2.4_Mobile_Dialog_Fix_2026-07-29.html`](PARC_Bangna_Fresh_Locale_Screen_Board_Explainer_v3.2.4_Mobile_Dialog_Fix_2026-07-29.html) — named HTML checkpoint
- [`analysis/PARC_Bangna_Fresh_Locale_Screen_Multi_Lens_Board_Brief_v0.4_2026-07-28.md`](analysis/PARC_Bangna_Fresh_Locale_Screen_Multi_Lens_Board_Brief_v0.4_2026-07-28.md) — analysis and Board brief
- [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) — third-party data and software notices

The named HTML is a self-contained decision artifact. It embeds the canonical
source-to-render payload, the 169-khwaeng overview, dated river and motorway
overlays, local MapLibre runtime, light/dark style snapshots, static fallback,
and the source/runtime integrity hashes used by release QA.

The named HTML and `index.html` must remain byte-identical. Earlier releases remain in the repository as audit history and do not define the current landing page.
