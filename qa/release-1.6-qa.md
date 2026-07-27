# PARC Bangna Top 10 — Release 1.6 QA

**Pre-publish status:** PASS
**Post-publish status:** PASS
**Production rendered check:** 28 July 2026, 03:54 ICT
**Browser:** Chromium 149.0.7827.0
**Production URL:** <https://montri-th.github.io/top10locations-like-parcbn/>

## Release scope checked

- 10 canonical candidates, with Release 1.5 rank and score parity
- 1 overview and 10 detail maps
- 23 venues in the public preliminary competitor registry
- 45 plotted candidate–competitor marker instances
- 2 evidence-table venues withheld from positional rendering
- 0 road, rail, station, OSM, inferred-polygon, or sample-restaurant features
- one System / Light / Dark cycle control
- transparent positive and reverse PARC logo derivatives
- named HTML artifact byte-identical to `index.html`

## Contract and static checks

| Check | Result |
|---|---|
| Canonical rank/score and competition-overlay parity | PASS |
| Candidate IDs across payload, manifest, HTML, and report | PASS |
| Marker↔manifest pairs and linked detail targets | PASS |
| Seven caveat hooks and six report-source hooks | PASS |
| Ten fallback IDs referenced by map accessibility records | PASS |
| Public artifact scan for connector IDs and scratch paths | PASS |
| PNG alpha and positive/reverse geometry parity | PASS |
| Theme state-machine test for OS Light and OS Dark | PASS |
| Installed map-manifest validator | PASS |
| Installed location-payload validator | PASS · 0 errors / 0 warnings |
| Installed location-report validator | PASS · 0 errors / 0 warnings |

## Rendered matrix

Rendered in Chromium at 320, 375, 768, 1024, and 1440 CSS pixels.

- no page-level horizontal overflow;
- 44 px minimum targets for theme, filters, disclosures, and marker hit areas;
- opaque sticky header with no backdrop blur;
- Anuphan 300 and IBM Plex Sans Thai Looped 400/500 loaded from local WOFF2 assets;
- Thai headings use zero tracking;
- 18 px body text;
- screen-reader map titles/descriptions and table fallbacks resolve;
- markers retain numbered non-colour encoding;
- core reading content remains available with JavaScript disabled;
- reduced-motion CSS, 200% text zoom, and A4 print output pass;
- print forces the positive transparent logo;
- no console error, page error, failed local request, or missing asset.

## Theme and logo

| Device preference | Press sequence | Result |
|---|---|---|
| Light | System → Dark → Light → System | PASS |
| Dark | System → Light → Dark → System | PASS |

System mode followed a simulated OS preference change without a reload. At every state, icon, accessible label, resolved theme, browser theme colour, and positive/reverse logo derivative remained aligned.

## Interaction

- Tier A–B filter returns 3 of 10 candidates and updates the live status.
- Marker link opens its linked competitor detail with click/tap/Enter.
- Focus moves to the opened summary.
- Escape closes the detail and returns focus to the originating marker.
- Native evidence disclosures operate from the keyboard.
- Tables remain independently scrollable on narrow screens without widening the page.

## Design-system pairs

| Pair | Contrast |
|---|---:|
| Light primary / Canvas | 12.11:1 |
| Light secondary / Canvas | 7.42:1 |
| Light action / Garden | 7.27:1 |
| Light focus / Canvas | 5.05:1 |
| Dark primary / Night Canvas | 14.00:1 |
| Dark secondary / Night Canvas | 10.04:1 |
| Dark Garden accent / Night Canvas | 8.71:1 |
| Dark focus / Night Canvas | 7.61:1 |

Visual inspection covered mobile navigation and filters, one full candidate card and map, the desktop hero in Light, and the desktop hero in Dark. The rendered result retains the J Lifestyle Center v0.3 quiet warm-canvas hierarchy.

## Final release artifact hashes

| Artifact | SHA-256 |
|---|---|
| `index.html` | `b5d3444cdb42f5058e22e43d8b7a429ec3594b54b17ac8546577e5f033bc3f4f` |
| named Release 1.6 HTML | `b5d3444cdb42f5058e22e43d8b7a429ec3594b54b17ac8546577e5f033bc3f4f` |
| `analysis/location-payload.json` | `29717e2503af1a09cab53c2b4b1cbb75096f8ffc6dcd9c2e49f27cbbefa27a14` |
| `analysis/map-manifest.json` | `b13b1c8fb4be89cfa2eb2a57a1c62fb09e74c2858f9d05c1bccd9a74e24afa3c` |
| `analysis/competitor-registry.public.json` | `6cd94958f72183815f76bd7748253b32676e8acc69e855f264d3fce5eb4f9336` |
| positive logo | `ab843d885426c8365afb3958b137e15f3e4a4d7f23abbe5b1a572e850688e755` |
| reverse logo | `dab33a928acb08db8d4317dffb903eccd5be53c89efe50365df6a9c44593990c` |

The production content deployment served `index.html` and the named HTML with the exact hashes above. The final status deployment refreshes the manifest and QA evidence without changing either HTML artifact.

## Post-publish gates

- [x] Production serves the approved content commit `6e372f7`.
- [x] Production `index.html` hash matches the final local artifact.
- [x] Logo, font, JSON, payload, manifest, and report assets return successfully.
- [x] Production interaction smoke test passes.
- [x] Canonical rank, noncanonical 80/20 label, marker count, and held-point disclosure match source.
- [x] Public source links remain present.

Release 1.6 status: **PASS**.
