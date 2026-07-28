# Third-party notices

Snapshot date: 28 July 2026

This release vendors the map renderer and two style documents so the report does not depend on a mutable CDN for executable code or on a MapTiler API key. The style documents still request public map tiles, glyphs and sprites from `tiles.openfreemap.org` at runtime.

## MapLibre GL JS 5.24.0

- Package: `maplibre-gl@5.24.0`
- Exact source: <https://registry.npmjs.org/maplibre-gl/-/maplibre-gl-5.24.0.tgz>
- Retrieved: 28 July 2026
- npm integrity: `sha512-ALyFxgtd5R+65UqZ/++lOqwWcC0SNho9c27fYSyLmG7AfnAul2o46F05aDJGPbFU57wos9dgcIySHs0Xe6ia3A==`
- Tarball SHA-256: `5cbf83c328c9d39cb24e3f2cefc9b407d69dd104ba0b41e84c0bfbb31c44e283`
- License: BSD 3-Clause
- Full bundled notice: [`assets/vendor/maplibre-gl-LICENSE-5.24.0.txt`](assets/vendor/maplibre-gl-LICENSE-5.24.0.txt)

Vendored files:

| File | Bytes | SHA-256 |
|---|---:|---|
| `assets/vendor/maplibre-gl.js` | 1,056,837 | `45a9b07a9189ce56054c620a947ccf41e291e58c95e9b61533b740aaa65ee5cb` |
| `assets/vendor/maplibre-gl.css` | 70,024 | `ab1e70d59ec40465bae7e7030da2f3ccf28133fd502e62bd598eefbadfd7a732` |

## OpenFreeMap runtime styles

The local style JSON files are exact runtime snapshots from OpenFreeMap. They contain no MapTiler endpoint, API-key placeholder or access token. Their only remote host is `tiles.openfreemap.org`.

| Mode | Exact source | Source last modified | Local snapshot | Bytes | SHA-256 |
|---|---|---|---|---:|---|
| Light / Positron | <https://tiles.openfreemap.org/styles/positron> | 27 July 2026 14:32:23 UTC | `assets/styles/openfreemap-positron-snapshot.json` | 25,153 | `a0f5b8487480a47ba5a5eaf25e165a19789dfa422f9ef9442f04da79c7d216db` |
| Dark / Dark Matter | <https://tiles.openfreemap.org/styles/dark> | 27 July 2026 13:38:13 UTC | `assets/styles/openfreemap-dark-snapshot.json` | 20,959 | `4ba4a1990dc5e1b72b38483dfbb92ffdd945bcc13e9f1235466dae900bc51631` |

The snapshots were retrieved on 28 July 2026. For design provenance, the current upstream style repositories at retrieval time were:

- Positron: <https://github.com/openmaptiles/positron-gl-style/tree/a6953507454fea072734d822b7341dd21d7b61d2>
- Dark Matter: <https://github.com/openmaptiles/dark-matter-gl-style/tree/d17442cb66bad8c82bda59d199d5dafeead410cf>

Licensing and attribution recorded by the upstream projects:

- OpenFreeMap project code: MIT.
- Positron and Dark Matter style code: BSD 3-Clause.
- Positron and Dark Matter visual design: Creative Commons Attribution 4.0.
- The styles derive from CartoDB Basemaps designed by Stamen and Paul Norman for CartoDB Inc., licensed under Creative Commons Attribution 3.0.
- OpenStreetMap data: Open Data Commons Open Database License; attribution is required.
- Natural Earth raster data: public domain.
- Noto Sans fonts: SIL Open Font License 1.1.
- Maki icons: CC0 1.0 Universal.

Bundled upstream notices:

- [`assets/vendor/openfreemap-LICENSE-2026-07-28.md`](assets/vendor/openfreemap-LICENSE-2026-07-28.md)
- [`assets/vendor/openmaptiles-positron-dark-style-LICENSE-2026-07-28.md`](assets/vendor/openmaptiles-positron-dark-style-LICENSE-2026-07-28.md)

Every browsable map in this report must expose these credits in or immediately adjacent to the map:

> OpenFreeMap · © OpenMapTiles · © OpenStreetMap contributors

## Runtime integrity contract

The named HTML checkpoint embeds the exact runtime, styles, source URLs, hashes,
licenses, permitted host, theme-switch behaviour and required attribution. The
report uses one reusable MapLibre instance; after a light/dark style change it
restores decision overlays on `style.load`.
