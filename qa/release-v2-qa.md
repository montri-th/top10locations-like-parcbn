# Competition-aware Board Explainer v2.0 — Release QA

Date: 28 July 2026  
Audited release commit: `a750ff42357e2262d0dff3e0e2931221d902ded7`  
Release status: **PASS**

## Integrity

- Exact decision scope: 10 candidate IDs in the recommendation, CTA, payload, table, cards, maps, and approval resolution.
- Deterministic QA: 10 candidates, 23 competitor records, and 43 candidate–competitor relationships.
- Named HTML and `index.html` are byte-identical.
- Local HTML SHA-256: `ce4aceda0769ae75af4d5b02ff2750446cc0777361b09b896afd61e11581b805`.
- Production response SHA-256: `ce4aceda0769ae75af4d5b02ff2750446cc0777361b09b896afd61e11581b805`.
- Location payload validator: PASS, 0 errors, 0 warnings.
- Map manifest validator: PASS.
- Interactive report validator: PASS, 0 errors, 0 warnings.

## Rendered production checks

| Check | Result |
|---|---|
| Desktop first screen states the decision, confidence, scope, owner, and timing | PASS |
| 390 px production frame | PASS |
| 320 px production frame | PASS |
| Root horizontal overflow at 390/320 px | None |
| Minimum visible interactive target at 390/320 px | 44 px |
| Map marker visual size remains impact-based while transparent hit area expands responsively | PASS |
| System, light, and dark themes | PASS |
| Dark-theme logo contrast | PASS |
| Quiet cleared-line bougainvillea treatment | PASS |
| Candidate filter and study-priority order | PASS |
| Candidate modal opens from card and overview-map marker | PASS |
| Competitor marker opens the correct evidence panel | PASS |
| Locale tabs replace the map, markers, and table together | PASS |
| Approval dialog requests study of the exact Top 10 only | PASS |
| Escape closes dialogs and restores focus to the opener | PASS |
| Skip link exposes focus and lands on `main` | PASS |
| Decision dock remains hidden over the hero and appears after the first screen | PASS |

The 390 px and 320 px same-origin production frames are a stricter reflow proxy than a 200% desktop viewport. The cloud browser did not expose a reliable browser-zoom control, so this check validates the resulting narrow-layout condition rather than claiming a native zoom-shortcut test.

## Map and evidence safeguards

- All candidate and competitor coordinates are disclosed as presentation reference points.
- No khwaeng boundary, locale extent, parcel, or catchment is invented.
- The visible kilometre grid is the declared simplified-basemap fallback.
- Competitor marker radius uses one categorical impact scale.
- Verified NLA/leasable-area values remain separate numeric context; unknown size is never treated as zero.
- Every clickable competitor marker has a table fallback and an evidence/status panel.

## Environment note

The cloud browser blocked a local `localhost` preview. Structural validation therefore preceded publication, and the complete rendered interaction suite plus exact-byte check ran against the final GitHub Pages production response.
