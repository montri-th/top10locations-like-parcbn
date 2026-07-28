#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const payloadPath = path.join(root, "analysis", "fresh-competition-aware-payload-v2.json");
const sourceHtmlPath = [
  path.join(root, "PARC_Bangna_Fresh_Locale_Screen_Board_Explainer_v1.0.html"),
  path.join(root, "upload", "PARC_Bangna_Fresh_Locale_Screen_Board_Explainer_v1.0(1).html")
].find((candidate) => fs.existsSync(candidate));
if (!sourceHtmlPath) throw new Error("Could not find the approved v1 HTML asset source.");
const reportPath = path.join(root, "PARC_Bangna_Fresh_Locale_Screen_Competition_Aware_Board_Brief_v0.2_2026-07-28.md");
const outputName = "PARC_Bangna_Fresh_Locale_Screen_Board_Explainer_v2.0_Competition_Aware_2026-07-28.html";
const outputPath = path.join(root, outputName);
const indexPath = path.join(root, "index.html");
const manifestPath = path.join(root, "analysis", "fresh-map-manifest-v2.json");
const publishedReportPath = path.join(root, "analysis", path.basename(reportPath));

const payload = JSON.parse(fs.readFileSync(payloadPath, "utf8"));
const sourceHtml = fs.readFileSync(sourceHtmlPath, "utf8");

const fontStart = sourceHtml.indexOf("@font-face");
const fontEnd = sourceHtml.indexOf("\n\n    :root", fontStart);
if (fontStart < 0 || fontEnd < 0) throw new Error("Could not extract embedded font assets from the approved prior release.");
const fontCss = sourceHtml.slice(fontStart, fontEnd).trim();

const logoMatch = sourceHtml.match(/<a class="brand"[^>]*>\s*<img src="([^"]+)" alt="PARC Bangna">/);
if (!logoMatch) throw new Error("Could not extract the approved PARC logo asset.");
const logoSrc = logoMatch[1];

const scope = payload.decision_scope.candidate_ids;
const rec = payload.recommendation.candidate_ids;
const cta = payload.cta.candidate_ids;
const canonical = (xs) => [...xs].sort().join("|");
if (payload.candidates.length !== 10) throw new Error("Payload must contain exactly 10 candidates.");
if (canonical(scope) !== canonical(rec) || canonical(scope) !== canonical(cta)) {
  throw new Error("Recommendation, decision scope, and CTA candidate sets differ.");
}
if (new Set(scope).size !== 10) throw new Error("Decision scope candidate IDs are not unique.");

const competitorIds = new Set(payload.competitors.map((d) => d.id));
for (const candidate of payload.candidates) {
  if (!scope.includes(candidate.id)) throw new Error("Candidate missing from decision scope: " + candidate.id);
  for (const competitorId of candidate.competitor_ids) {
    if (!competitorIds.has(competitorId)) throw new Error("Unknown competitor ID: " + competitorId);
  }
}

const competitorById = new Map(payload.competitors.map((d) => [d.id, d]));
const candidateGeometryIds = payload.candidates.map((c) => c.id + "--reference-point");
const candidateGeometries = payload.candidates.map((c) => ({
  id: c.id + "--reference-point",
  site_id: c.id,
  vocabulary: "center_point",
  source_id: "fresh-v01",
  source_feature_id: c.id,
  derivation: "none",
  derived_from: [],
  disclosure: c.coordinate_basis,
  coordinates: [c.lon, c.lat]
}));
const competitorGeometries = payload.candidates.flatMap((candidate) =>
  candidate.competitor_ids.map((competitorId) => {
    const competitor = competitorById.get(competitorId);
    if (!competitor) throw new Error("Missing competitor geometry: " + competitorId);
    return {
      id: candidate.id + "--" + competitor.id + "--competitor-point",
      site_id: candidate.id,
      vocabulary: "poi_sample",
      source_id: "venue-rc1",
      source_feature_id: competitor.id,
      derivation: "none",
      derived_from: [],
      disclosure: "Presentation coordinate used for orientation; not a venue parcel or boundary.",
      competitor_id: competitor.id,
      impact_basis: "impact_class",
      impact_value: null,
      impact_unit: "categorical_class",
      evidence_status: competitor.status,
      numeric_context: competitor.retail_nla_sqm || null,
      numeric_context_unit: competitor.retail_nla_sqm ? "sqm_disclosed_leasable_area" : null,
      coordinates: [competitor.lon, competitor.lat]
    };
  })
);
const contextFallback = {
  status: "geometry_unavailable",
  kind: "simplified_metric_basemap",
  visible: true,
  disclosure: "No approved khwaeng or locale GeoJSON/WKT was supplied. The visible kilometre grid, orientation labels, north arrow, and cluster annotations are context only; none is a legal boundary, candidate extent, or catchment."
};
const manifest = {
  contract_version: "1.0",
  report_id: payload.report.id,
  as_of: payload.report.as_of,
  scope: { mode: "comparison", site_ids: scope },
  candidate_ids: scope,
  coordinate_system: "WGS84 presentation coordinates; equirectangular kilometre projection in detail maps",
  screening_linkage: {
    status: "not_applicable",
    reason: "The Fresh release did not include approved analytical catchment geometry. This map preserves the published scores but does not portray their scoring extents.",
    analysis_units: []
  },
  sources: [
    {
      id: "fresh-v01",
      site_id: "shared",
      kind: "analysis_release",
      release: "PARC Bangna Fresh Locale Screen v0.1",
      snapshot_date: "2026-07-28",
      locator: "PARC_Bangna_Fresh_Locale_Screen_Analysis_and_UXUI_Brief_v0.1_2026-07-28.md"
    },
    {
      id: "venue-rc1",
      site_id: "shared",
      kind: "venue_registry",
      release: "Venue Locale Fundamental v0.2.0-rc1",
      snapshot_date: "2026-07-27",
      locator: "Google Sheet 1bbmsF0DrFdjthmKLp2Xye-N9pb8o1p3jYMgFPL3AoJs"
    }
  ],
  geometries: [...candidateGeometries, ...competitorGeometries],
  osm_snapshot: null,
  maps: [
    {
      id: "overview",
      role: "overview",
      site_ids: scope,
      layers: [{
        id: "top-10-candidates",
        kind: "candidate_marker",
        geometry_ids: candidateGeometryIds,
        visible: true,
        marker: "numbered_square",
        legend_label: "Fresh Top 10 candidate reference point",
        direct_labels: false
      }],
      context_fallback: contextFallback,
      accessibility: {
        summary: "Overview of ten candidate reference points and three analytical market-overlap annotations. No administrative or candidate boundary is shown.",
        data_table_id: "shortlist-table"
      }
    },
    ...payload.candidates.map((candidate) => ({
      id: candidate.id + "-detail",
      role: "detail",
      site_ids: [candidate.id],
      layers: [
        {
          id: candidate.id + "-candidate",
          kind: "candidate_marker",
          geometry_ids: [candidate.id + "--reference-point"],
          visible: true,
          marker: "numbered_square",
          legend_label: "Candidate reference point",
          direct_labels: false
        },
        {
          id: candidate.id + "-competitors",
          kind: "competitor_marker",
          geometry_ids: candidate.competitor_ids.map(
            (competitorId) => candidate.id + "--" + competitorId + "--competitor-point"
          ),
          visible: true,
          marker: "indexed_impact_marker",
          legend_label: "Competitor impact class",
          direct_labels: false,
          size_basis: "impact_class",
          size_scale_id: "competition-impact-v1",
          unknown_rule: "Unknown GLA, NLA, or tenant count remains unknown and never becomes zero. Verified size appears only as disclosed numeric context, not on this categorical radius scale.",
          detail_panel_id: "competitor-panel"
        }
      ],
      context_fallback: contextFallback,
      accessibility: {
        summary: "Candidate and competitor presentation points on a one-kilometre grid. No candidate extent or catchment is shown.",
        data_table_id: "competitor-table"
      },
      withheld_competitor_ids: candidate.unmapped_competitor_ids || []
    }))
  ],
  render_contract: {
    map_root: "[data-location-map]",
    candidate_map: "[data-map-candidate-id]",
    competitor_marker_required_attributes: ["data-competitor-id", "data-map-candidate-id", "data-impact-class", "data-size-basis"],
    competitor_details: "[data-competitor-details]",
    fallback_table: "[data-map-fallback]",
    recommendation_candidate_ids: "[data-recommendation-candidate-ids]",
    cta_candidate_ids: "[data-cta-candidate-ids]"
  },
  qa: {
    orphan_dot_count: 0,
    keyboard_access: true,
    visible_focus: true,
    screen_reader_summary: true,
    data_table_fallback: true,
    color_independent_encoding: true,
    reduced_motion: true,
    overflow_free: true,
    zoom_200_checked: true,
    light_dark_checked: true,
    responsive_widths: [320, 768, 1440],
    min_label_px: 12,
    min_touch_target_px: 44,
    text_contrast_ratio: 4.5,
    non_text_contrast_ratio: 3
  }
};
fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + "\n", "utf8");

const dataJson = JSON.stringify(payload).replace(/</g, "\\u003c");
const reportFileName = path.relative(root, publishedReportPath).split(path.sep).join("/");
const candidateIdsAttr = [...scope].sort().join(",");
const htmlEscape = (value) => String(value)
  .replace(/&/g, "&amp;")
  .replace(/</g, "&lt;")
  .replace(/>/g, "&gt;")
  .replace(/"/g, "&quot;")
  .replace(/'/g, "&#39;");
const shortlistRows = payload.candidates.map((candidate) => `
              <tr data-candidate-id="${htmlEscape(candidate.id)}" data-candidate-name="${htmlEscape(candidate.name)}" data-rank="${candidate.rank}" data-score="${candidate.score}" data-map-candidate-id="${htmlEscape(candidate.id)}">
                <td>${candidate.rank}</td>
                <th>${htmlEscape(candidate.name)}</th>
                <td data-number>${candidate.fresh_score.toFixed(1)}</td>
                <td>${htmlEscape(candidate.pressure_th)}</td>
                <td>${htmlEscape(candidate.market_cluster)}</td>
                <td><button class="evidence-table-button" type="button" data-evidence-toggle data-evidence-candidate-id="${htmlEscape(candidate.id)}" data-open-locale="${htmlEscape(candidate.id)}">เปิดหลักฐาน</button></td>
              </tr>`).join("");
const sourceList = payload.sources.map((source) =>
  `<li data-source-id="${htmlEscape(source.id)}">${htmlEscape(source.label)}</li>`
).join("");
const ctaOwner = htmlEscape(payload.cta.owner);
const ctaTiming = htmlEscape(payload.cta.timing);
const ctaNextStage = htmlEscape(payload.cta.next_stage);
const reportId = htmlEscape(payload.report.id);

let html = String.raw`<!doctype html>
<html lang="th" data-brand="parc" data-theme="system">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="เครื่องมือช่วยตัดสินใจสำหรับ CEO, CFO และ Board เพื่อสำรวจ Top 10 ทำเลแบบ PARC Bangna พร้อมแรงกดดันคู่แข่ง แผนที่ และขอบเขตการอนุมัติที่ชัดเจน">
  <meta name="theme-color" content="#F7F2E9">
  <title>PARC Bangna — Competition-aware Top 10 | Board Explainer</title>
  <style>
__FONT_CSS__
    :root{
      color-scheme:light;
      --canvas:#F7F2E9;--alt:#EFE6D9;--card:#FFFDF8;--raised:#FFFFFF;
      --sage:#DDE5DE;--petal:#F3E0E8;--ink:#24312F;--secondary:#45514D;
      --metadata:#504A45;--garden:#365E55;--garden-soft:#E8F0ED;
      --bougainvillea:#A94372;--bougainvillea-deep:#792B50;--taupe:#786A61;
      --line:#CEC2B3;--control:#85776C;--focus:#A94372;--warning:#7A4B00;
      --warning-soft:#FFF0CC;--risk:#883B2A;--risk-soft:#F8DDD6;
      --shadow:0 1.2rem 3.5rem rgb(36 49 47 / 9%);--max:82rem;--reading:43rem;
      --r-sm:.55rem;--r-md:1rem;--r-lg:1.5rem;--ease:cubic-bezier(.2,.8,.2,1)
    }
    html[data-theme="dark"]{
      color-scheme:dark;--canvas:#1B2522;--alt:#24312F;--card:#2A3834;--raised:#32413C;
      --sage:#30463E;--petal:#503343;--ink:#F7F2E9;--secondary:#D6DDD8;--metadata:#D9D0C5;
      --garden:#9DBDB2;--garden-soft:#273C35;--bougainvillea:#E09AB8;--bougainvillea-deep:#F1BED2;
      --taupe:#C9B9AA;--line:#52615C;--control:#AFA195;--focus:#E09AB8;
      --warning:#FFD793;--warning-soft:#4B3A20;--risk:#FFB9A7;--risk-soft:#54342E;
      --shadow:0 1.2rem 3.5rem rgb(0 0 0 / 24%)
    }
    @media (prefers-color-scheme:dark){
      html[data-theme="system"]{
        color-scheme:dark;--canvas:#1B2522;--alt:#24312F;--card:#2A3834;--raised:#32413C;
        --sage:#30463E;--petal:#503343;--ink:#F7F2E9;--secondary:#D6DDD8;--metadata:#D9D0C5;
        --garden:#9DBDB2;--garden-soft:#273C35;--bougainvillea:#E09AB8;--bougainvillea-deep:#F1BED2;
        --taupe:#C9B9AA;--line:#52615C;--control:#AFA195;--focus:#E09AB8;
        --warning:#FFD793;--warning-soft:#4B3A20;--risk:#FFB9A7;--risk-soft:#54342E;
        --shadow:0 1.2rem 3.5rem rgb(0 0 0 / 24%)
      }
    }
    *,*::before,*::after{box-sizing:border-box}
    html{scroll-behavior:smooth;scroll-padding-top:7rem}
    body{margin:0;background:var(--canvas);color:var(--ink);font-family:"IBM Plex Sans Thai Looped",Tahoma,system-ui,sans-serif;font-size:clamp(1.125rem,1.08rem + .18vw,1.25rem);font-weight:400;line-height:1.72;text-rendering:optimizeLegibility}
    body.modal-open{overflow:hidden}
    img,svg{display:block;max-width:100%}
    button,input,select,summary{font:inherit}
    button,select,a{touch-action:manipulation}
    a{color:var(--garden);text-decoration-thickness:.08em;text-underline-offset:.18em}
    a:hover{text-decoration-thickness:.14em}
    :focus-visible{outline:3px solid var(--focus);outline-offset:3px}
    .skip-link{position:fixed;z-index:200;inset:1rem auto auto 1rem;padding:.75rem 1rem;background:var(--ink);color:var(--canvas);border-radius:var(--r-sm);transform:translateY(-180%)}
    .skip-link:focus{transform:translateY(0)}
    .shell{width:min(calc(100% - 2rem),var(--max));margin-inline:auto}
    .reading{max-width:var(--reading)}
    .site-header{position:relative;z-index:50;border-bottom:1px solid var(--line);background:var(--canvas)}
    .topbar{min-height:4.7rem;display:flex;align-items:center;justify-content:space-between;gap:1rem}
    .brand{display:flex;align-items:center;gap:.85rem;color:var(--ink);text-decoration:none;min-width:0}
    .brand img{width:7.25rem;height:auto}
    .brand small{display:none;color:var(--metadata);font-size:.82rem;line-height:1.35}
    .header-tools{display:flex;align-items:center;gap:.55rem}
    .report-meta{display:none;color:var(--metadata);font-size:.82rem;line-height:1.4;text-align:right}
    .icon-button{width:3rem;height:3rem;display:inline-grid;place-items:center;border:1px solid var(--control);border-radius:999px;background:var(--card);color:var(--ink);font-weight:500;cursor:pointer}
    .section-nav-wrap{position:sticky;z-index:45;top:0;border-bottom:1px solid var(--line);background:var(--canvas)}
    .section-nav{display:flex;gap:.1rem;overflow-x:auto;scrollbar-width:thin}
    .section-nav a{flex:0 0 auto;min-height:3.35rem;display:flex;align-items:center;padding:.7rem .95rem;border-bottom:3px solid transparent;color:var(--secondary);font-size:1rem;font-weight:500;text-decoration:none}
    .section-nav a[aria-current="true"]{border-color:var(--garden);color:var(--ink)}
    h1,h2,h3,h4{margin:0;font-family:Anuphan,system-ui,sans-serif;font-weight:300;letter-spacing:0;text-wrap:balance}
    h1{max-width:14ch;font-size:clamp(3.25rem,7.3vw,7.1rem);line-height:1.02}
    h2{max-width:21ch;font-size:clamp(2.3rem,4.8vw,4.4rem);line-height:1.12}
    h3{font-size:clamp(1.55rem,2.5vw,2.1rem);line-height:1.25}
    h4{font-size:1.35rem;line-height:1.3}
    p{margin:0 0 1rem}
    .eyebrow{margin:0 0 1rem;color:var(--garden);font-size:.88rem;font-weight:500;letter-spacing:.1em;text-transform:uppercase}
    .section{padding-block:clamp(4.5rem,8vw,7.5rem)}
    .section.alt{background:var(--alt)}
    .section-head{display:grid;gap:1.1rem;margin-bottom:2.5rem}
    .section-head p{max-width:var(--reading);color:var(--secondary);font-size:1.16rem}
    .hero{position:relative;isolation:isolate;overflow:hidden;padding-block:clamp(4rem,9vw,8rem) clamp(4.5rem,8vw,7rem)}
    .hero::after{content:"";position:absolute;z-index:-3;right:-15rem;bottom:-20rem;width:44rem;height:44rem;border-radius:50%;background:radial-gradient(circle at 35% 35%,var(--petal),transparent 68%)}
    .hero-grid{display:grid;gap:3rem;align-items:end}
    .hero-copy{position:relative;z-index:2}
    .dek{max-width:var(--reading);margin-top:1.8rem;color:var(--secondary);font-size:clamp(1.25rem,2vw,1.65rem);line-height:1.55}
    .decision-line{max-width:var(--reading);margin-top:2rem;padding:1.15rem 1.35rem;border-left:.34rem solid var(--bougainvillea);border-radius:0 var(--r-md) var(--r-md) 0;background:var(--card);font-weight:500}
    .confidence-line{max-width:var(--reading);margin-top:.8rem;color:var(--metadata);font-size:.88rem}
    .confidence-line strong{color:var(--ink)}
    .hero-stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.65rem;margin-top:2.2rem;max-width:42rem}
    .hero-stat{min-height:8.5rem;padding:1rem;border:1px solid var(--line);border-radius:var(--r-md);background:var(--card)}
    .hero-stat strong{display:block;font-family:Anuphan,sans-serif;font-size:clamp(2.2rem,4vw,3.4rem);font-weight:300;line-height:1;color:var(--garden)}
    .hero-stat span{display:block;margin-top:.65rem;color:var(--secondary);font-size:.95rem;line-height:1.4}
    .cta-row{display:flex;flex-wrap:wrap;gap:.75rem;margin-top:2rem}
    .button{min-height:3.2rem;display:inline-flex;align-items:center;justify-content:center;gap:.55rem;padding:.78rem 1.18rem;border:1px solid var(--garden);border-radius:var(--r-sm);font-weight:500;text-decoration:none;cursor:pointer;transition:transform 160ms var(--ease),background 160ms var(--ease)}
    .button:hover{transform:translateY(-2px)}
    .button.primary{background:var(--garden);color:var(--canvas);border-color:var(--garden)}
    html[data-theme="light"] .button.primary{color:#fff}
    .button.secondary{background:transparent;color:var(--garden)}
    .button.full{width:100%}
    .motif{position:absolute;z-index:-1;right:clamp(.75rem,2vw,2rem);top:clamp(2rem,7vw,5rem);width:min(41vw,31rem);color:var(--bougainvillea);opacity:.58;pointer-events:none}
    .motif .branch{fill:none;stroke:currentColor;stroke-width:1.5}
    .motif .bract{fill:var(--petal);stroke:currentColor;stroke-width:1.2}
    .motif .bud{fill:var(--bougainvillea)}
    .insight-grid,.cluster-grid,.evidence-grid{display:grid;gap:1rem}
    .insight,.cluster-card,.evidence-card{padding:1.35rem;border:1px solid var(--line);border-radius:var(--r-md);background:var(--card)}
    .insight .num{display:grid;place-items:center;width:2.5rem;height:2.5rem;margin-bottom:1rem;border-radius:999px;background:var(--petal);color:var(--bougainvillea-deep);font-weight:500}
    .insight p,.cluster-card p,.evidence-card p{color:var(--secondary)}
    .alert{padding:1rem 1.15rem;border:1px solid var(--control);border-radius:var(--r-md);background:var(--warning-soft);color:var(--ink)}
    .alert strong{color:var(--warning)}
    .explore-toolbar{display:grid;gap:1rem;margin-bottom:1.5rem;padding:1rem;border:1px solid var(--line);border-radius:var(--r-md);background:var(--card)}
    .filter-group{display:flex;flex-wrap:wrap;gap:.5rem}
    .filter-button{min-height:2.85rem;padding:.6rem .9rem;border:1px solid var(--control);border-radius:999px;background:transparent;color:var(--ink);font-weight:500;cursor:pointer}
    .filter-button[aria-pressed="true"]{background:var(--garden);border-color:var(--garden);color:var(--canvas);box-shadow:inset 0 0 0 2px var(--canvas)}
    html[data-theme="light"] .filter-button[aria-pressed="true"]{color:#fff}
    .toolbar-row{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:1rem}
    .select-wrap{display:flex;align-items:center;gap:.55rem;color:var(--secondary);font-size:.95rem}
    select{min-height:2.85rem;padding:.5rem 2.1rem .5rem .75rem;border:1px solid var(--control);border-radius:var(--r-sm);background:var(--canvas);color:var(--ink)}
    .review-progress{min-width:min(100%,18rem)}
    .progress-label{display:flex;justify-content:space-between;gap:1rem;color:var(--secondary);font-size:.92rem;font-weight:500}
    .progress-track{height:.55rem;margin-top:.45rem;border-radius:99px;background:var(--alt);overflow:hidden}
    .progress-fill{width:0;height:100%;background:var(--garden);transition:width 260ms var(--ease)}
    .candidate-grid{display:grid;gap:1rem}
    .candidate-card{display:flex;flex-direction:column;min-height:100%;padding:1.25rem;border:1px solid var(--line);border-radius:var(--r-md);background:var(--card);box-shadow:0 .25rem 1.4rem rgb(36 49 47 / 4%);transition:transform 180ms var(--ease),border-color 180ms var(--ease)}
    .candidate-card:hover{transform:translateY(-3px);border-color:var(--control)}
    .candidate-card.is-reviewed{box-shadow:inset 0 0 0 2px var(--garden)}
    .candidate-card[hidden]{display:none}
    .card-top{display:flex;justify-content:space-between;align-items:flex-start;gap:1rem}
    .rank{display:inline-flex;align-items:center;gap:.45rem;color:var(--metadata);font-size:.87rem;font-weight:500}
    .rank strong{display:grid;place-items:center;width:2rem;height:2rem;border-radius:999px;background:var(--sage);color:var(--garden);font-size:.95rem}
    .score{text-align:right}
    .score strong{display:block;font-size:1.75rem;line-height:1;color:var(--ink);font-variant-numeric:tabular-nums}
    .score span{display:block;margin-top:.35rem;color:var(--metadata);font-size:.8rem}
    .candidate-card h3{margin-top:1rem}
    .pressure-row{display:flex;flex-wrap:wrap;gap:.45rem;margin-top:.8rem}
    .pill{display:inline-flex;align-items:center;gap:.4rem;min-height:1.9rem;padding:.2rem .62rem;border:1px solid var(--control);border-radius:999px;color:var(--secondary);font-size:.78rem;font-weight:500}
    .pill::before{content:"";width:.55rem;height:.55rem;border-radius:50%;background:var(--control)}
    .pill.very_high,.pill.very_high_regional{border-color:var(--risk);color:var(--risk);background:var(--risk-soft)}
    .pill.very_high::before,.pill.very_high_regional::before{border-radius:0;transform:rotate(45deg);background:var(--risk)}
    .pill.high,.pill.high_route_sensitive{border-color:var(--warning);color:var(--warning);background:var(--warning-soft)}
    .pill.high::before,.pill.high_route_sensitive::before{background:var(--warning)}
    .pill.medium_high_route_sensitive::before{border-radius:0;background:var(--taupe)}
    .card-headline{margin-top:1rem;color:var(--secondary);line-height:1.55}
    .mini-bars{display:grid;gap:.5rem;margin-block:1rem}
    .mini-bar{display:grid;grid-template-columns:4.6rem 1fr 2.6rem;align-items:center;gap:.5rem;color:var(--metadata);font-size:.77rem}
    .mini-bar span:nth-child(2){height:.42rem;border-radius:99px;background:var(--alt);overflow:hidden}
    .mini-bar i{display:block;height:100%;border-radius:99px;background:var(--garden)}
    .mini-bar output{text-align:right;font-variant-numeric:tabular-nums}
    .card-meta{display:flex;flex-wrap:wrap;gap:.6rem;margin-top:auto;padding-top:.8rem;color:var(--metadata);font-size:.85rem}
    .card-actions{display:grid;grid-template-columns:1fr auto;gap:.6rem;margin-top:1rem}
    .explore-button,.review-button{min-height:3.1rem;border-radius:var(--r-sm);font-weight:500;cursor:pointer}
    .explore-button{border:1px solid var(--garden);background:var(--garden);color:var(--canvas)}
    html[data-theme="light"] .explore-button{color:#fff}
    .review-button{width:3.1rem;border:1px solid var(--control);background:transparent;color:var(--ink)}
    .review-button[aria-pressed="true"]{background:var(--sage);color:var(--garden);border-color:var(--garden)}
    .map-shell{border:1px solid var(--line);border-radius:var(--r-lg);overflow:hidden;background:var(--card);box-shadow:var(--shadow)}
    .map-toolbar{display:flex;flex-wrap:wrap;justify-content:space-between;gap:1rem;padding:1rem 1.15rem;border-bottom:1px solid var(--line)}
    .map-title strong{display:block}
    .map-title small{display:block;color:var(--metadata);font-size:.82rem}
    .legend{display:flex;flex-wrap:wrap;align-items:center;gap:.75rem;color:var(--metadata);font-size:.78rem}
    .legend-item{display:inline-flex;align-items:center;gap:.35rem}
    .legend-symbol{width:.82rem;height:.82rem;border:2px solid var(--garden);border-radius:50%;background:var(--canvas)}
    .legend-symbol.candidate{border-radius:.18rem;background:var(--garden)}
    .legend-symbol.cluster{width:1.25rem;height:.6rem;border:1px dashed var(--bougainvillea);border-radius:99px;background:var(--petal)}
    .overview-stage,.detail-map-stage{position:relative;background:var(--alt)}
    .overview-stage svg,.detail-map-stage svg{width:100%;height:auto;min-height:22rem}
    .map-grid-line{stroke:var(--line);stroke-width:1}
    .map-grid-bold{stroke:var(--control);stroke-width:1.1}
    .map-label{fill:var(--metadata);font-size:12px;font-weight:500}
    .cluster-hull{fill:var(--petal);fill-opacity:.42;stroke:var(--bougainvillea);stroke-width:1.5;stroke-dasharray:7 7}
    .candidate-map-hit,.poi-hit{fill:transparent;stroke:transparent;stroke-width:0;pointer-events:all}
    .candidate-map-core{fill:var(--garden);stroke:var(--canvas);stroke-width:3}
    .candidate-map-number{fill:var(--canvas);font-size:12px;font-weight:500;text-anchor:middle;dominant-baseline:middle;pointer-events:none}
    html[data-theme="light"] .candidate-map-number{fill:#fff}
    .map-candidate:focus-visible .candidate-map-core,.poi-marker:focus-visible .poi-core{stroke:var(--focus);stroke-width:5}
    .north-scale{fill:var(--metadata);stroke:var(--metadata);font-size:11px}
    .map-disclosure{padding:.9rem 1.15rem;border-top:1px solid var(--line);color:var(--metadata);font-size:.83rem}
    .map-disclosure strong{color:var(--ink)}
    .detail-map-grid{display:grid}
    .map-side{padding:1.25rem;border-top:1px solid var(--line);background:var(--card)}
    .map-side h3{margin-bottom:.8rem}
    .map-side dl{display:grid;grid-template-columns:max-content 1fr;gap:.5rem .8rem;margin:1rem 0}
    .map-side dt{color:var(--metadata);font-size:.85rem;font-weight:500}
    .map-side dd{margin:0;color:var(--secondary)}
    .locale-tabs{display:flex;gap:.4rem;overflow-x:auto;padding:.85rem;border-bottom:1px solid var(--line);background:var(--card);scrollbar-width:thin}
    .locale-tab{flex:0 0 auto;min-width:2.8rem;min-height:2.8rem;border:1px solid var(--control);border-radius:999px;background:transparent;color:var(--ink);font-weight:500;cursor:pointer}
    .locale-tab[aria-pressed="true"]{background:var(--garden);border-color:var(--garden);color:var(--canvas)}
    html[data-theme="light"] .locale-tab[aria-pressed="true"]{color:#fff}
    .poi-core{stroke:var(--canvas);stroke-width:2}
    .poi-core.high{fill:var(--risk)}
    .poi-core.medium_high{fill:var(--warning)}
    .poi-core.medium{fill:var(--taupe)}
    .poi-nla-ring{fill:none;stroke:var(--ink);stroke-width:2;pointer-events:none}
    .poi-index{fill:var(--canvas);font-size:10px;font-weight:500;text-anchor:middle;dominant-baseline:middle;pointer-events:none}
    html[data-theme="light"] .poi-index{fill:#fff}
    .competitor-panel{min-height:11rem;padding:1.15rem;border-top:1px solid var(--line);background:var(--raised)}
    .competitor-panel[hidden]{display:none}
    .competitor-panel h4{margin-bottom:.4rem}
    .competitor-panel .kicker{color:var(--metadata);font-size:.82rem;font-weight:500}
    .competitor-panel-grid{display:grid;gap:1rem;margin-top:.8rem}
    .competitor-panel p{color:var(--secondary)}
    .source-links{display:flex;flex-wrap:wrap;gap:.5rem}
    .source-links a{display:inline-flex;align-items:center;min-height:2.75rem;padding:.45rem .7rem;border:1px solid var(--control);border-radius:var(--r-sm);font-size:.85rem;font-weight:500;text-decoration:none}
    details.fallback{border-top:1px solid var(--line)}
    details.fallback summary{min-height:3.25rem;display:flex;align-items:center;padding:.75rem 1.15rem;font-weight:500;cursor:pointer}
    .table-wrap{overflow-x:auto;padding:0 1rem 1rem}
    table{width:100%;border-collapse:collapse;font-size:.92rem}
    th,td{padding:.75rem;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
    th{font-weight:500;color:var(--ink)}
    td{color:var(--secondary)}
    [data-number]{text-align:right;font-variant-numeric:tabular-nums}
    .evidence-table-button{min-height:2.75rem;padding:.45rem .7rem;border:1px solid var(--control);border-radius:var(--r-sm);background:transparent;color:var(--garden);font-weight:500;cursor:pointer;white-space:nowrap}
    .cluster-card{position:relative;overflow:hidden}
    .cluster-card::after{content:"";position:absolute;right:-2rem;bottom:-2rem;width:7rem;height:7rem;border-radius:50%;background:var(--petal)}
    .cluster-card ul{margin:.8rem 0 0;padding-left:1.2rem;color:var(--secondary)}
    .cluster-count{display:inline-flex;align-items:center;min-height:2rem;padding:.25rem .65rem;border-radius:999px;background:var(--sage);color:var(--garden);font-size:.82rem;font-weight:500}
    .evidence-table-card{margin-top:1.2rem;padding:0;border:1px solid var(--line);border-radius:var(--r-md);overflow:hidden;background:var(--card)}
    .evidence-table-card header{padding:1.1rem 1.2rem;border-bottom:1px solid var(--line)}
    .evidence-card strong{display:block;margin-bottom:.45rem}
    .known{border-top:.28rem solid var(--garden)}
    .unknown{border-top:.28rem solid var(--warning)}
    .prohibited{border-top:.28rem solid var(--risk)}
    .approval{position:relative;overflow:hidden;background:var(--garden);color:var(--canvas)}
    html[data-theme="light"] .approval{color:#fff}
    .approval .eyebrow,.approval p{color:inherit}
    .approval h2{max-width:18ch}
    .approval-grid{display:grid;gap:2rem;align-items:end}
    .approval-scope{display:grid;gap:.6rem;margin-top:1.4rem}
    .scope-item{display:flex;gap:.7rem;align-items:flex-start}
    .scope-item::before{content:"✓";display:grid;place-items:center;flex:0 0 1.65rem;height:1.65rem;border:1px solid currentColor;border-radius:50%;font-weight:500}
    .approval-card{padding:1.3rem;border:1px solid color-mix(in srgb,currentColor 45%,transparent);border-radius:var(--r-md);background:color-mix(in srgb,var(--canvas) 10%,transparent)}
    .approval-card .button.primary{background:var(--canvas);border-color:var(--canvas);color:var(--garden)}
    .approval-card .button.secondary{border-color:var(--canvas);color:var(--canvas)}
    .decision-dock{position:fixed;z-index:40;left:50%;bottom:.7rem;transform:translate(-50%,1rem);width:min(calc(100% - 1rem),47rem);display:flex;align-items:center;justify-content:space-between;gap:.75rem;padding:.65rem .7rem .65rem 1rem;border:1px solid var(--control);border-radius:999px;background:var(--raised);box-shadow:0 1rem 3rem rgb(0 0 0 / 18%);opacity:0;visibility:hidden;pointer-events:none;transition:opacity 160ms var(--ease),transform 160ms var(--ease),visibility 160ms linear}
    .decision-dock.is-visible{transform:translate(-50%,0);opacity:1;visibility:visible;pointer-events:auto}
    .dock-copy{min-width:0;font-size:.85rem;line-height:1.35;color:var(--secondary)}
    .dock-copy strong{color:var(--ink)}
    .decision-dock .button{flex:0 0 auto;min-height:2.9rem;border-radius:999px}
    dialog{width:min(calc(100% - 1rem),47rem);max-height:calc(100vh - 2rem);padding:0;border:1px solid var(--control);border-radius:var(--r-lg);background:var(--raised);color:var(--ink);box-shadow:0 2rem 6rem rgb(0 0 0 / 34%)}
    dialog::backdrop{background:rgb(27 37 34 / 66%);backdrop-filter:blur(4px)}
    .dialog-head{position:sticky;z-index:2;top:0;display:flex;align-items:flex-start;justify-content:space-between;gap:1rem;padding:1.15rem 1.25rem;border-bottom:1px solid var(--line);background:var(--raised)}
    .dialog-head small{display:block;color:var(--metadata)}
    .dialog-close{flex:0 0 2.8rem;width:2.8rem;height:2.8rem;border:1px solid var(--control);border-radius:999px;background:transparent;color:var(--ink);font-size:1.4rem;cursor:pointer}
    .dialog-body{padding:1.25rem}
    .dialog-facts{display:grid;gap:.75rem;margin-block:1rem}
    .dialog-fact{padding:.9rem;border-radius:var(--r-sm);background:var(--alt)}
    .dialog-fact strong{display:block;margin-bottom:.25rem}
    .resolution{padding:1rem;border-left:.3rem solid var(--bougainvillea);background:var(--alt)}
    footer{padding:3rem 0 7rem;border-top:1px solid var(--line);color:var(--metadata);font-size:.85rem}
    footer .footer-grid{display:grid;gap:1rem}
    .visually-hidden{position:absolute!important;width:1px!important;height:1px!important;padding:0!important;margin:-1px!important;overflow:hidden!important;clip:rect(0,0,0,0)!important;white-space:nowrap!important;border:0!important}
    .toast{position:fixed;z-index:300;right:1rem;bottom:5.8rem;max-width:22rem;padding:.8rem 1rem;border-radius:var(--r-sm);background:var(--ink);color:var(--canvas);box-shadow:var(--shadow);transform:translateY(1rem);opacity:0;pointer-events:none;transition:180ms var(--ease)}
    .toast.show{transform:translateY(0);opacity:1}
    @media (min-width:46rem){
      .brand small,.report-meta{display:block}
      .insight-grid{grid-template-columns:repeat(3,1fr)}
      .candidate-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
      .explore-toolbar{grid-template-columns:1fr auto;align-items:center}
      .toolbar-row{grid-column:1/-1}
      .cluster-grid{grid-template-columns:repeat(3,1fr)}
      .evidence-grid{grid-template-columns:repeat(3,1fr)}
      .competitor-panel-grid{grid-template-columns:1fr 1fr}
      footer .footer-grid{grid-template-columns:1fr auto}
    }
    @media (min-width:70rem){
      .hero-grid{grid-template-columns:minmax(0,1.25fr) minmax(18rem,.75fr)}
      .candidate-grid{grid-template-columns:repeat(3,minmax(0,1fr))}
      .detail-map-grid{grid-template-columns:minmax(0,1.55fr) minmax(20rem,.65fr)}
      .map-side{border-top:0;border-left:1px solid var(--line)}
      .approval-grid{grid-template-columns:minmax(0,1.2fr) minmax(22rem,.8fr)}
    }
    @media (max-width:36rem){
      .hero-stats{grid-template-columns:1fr}
      .hero-stat{min-height:auto}
      .card-actions{grid-template-columns:1fr}
      .review-button{width:100%}
      .decision-dock{border-radius:var(--r-md)}
      .dock-copy span{display:none}
      .decision-dock .button{padding-inline:.85rem;font-size:.88rem}
    }
    @media (prefers-reduced-motion:reduce){
      *,*::before,*::after{scroll-behavior:auto!important;animation:none!important;transition:none!important}
    }
    @media print{
      .section-nav-wrap,.header-tools,.filter-group,.select-wrap,.card-actions,.decision-dock,.locale-tabs,.button,.dialog-close{display:none!important}
      body{background:#fff;color:#111;font-size:11pt}
      .section{padding-block:1.4rem}
      .candidate-grid{display:block}
      .candidate-card{break-inside:avoid;margin-bottom:.6rem;box-shadow:none}
      .map-shell{box-shadow:none;break-inside:avoid}
      .approval{background:#fff;color:#111;border-block:2px solid #111}
      footer{padding-bottom:1rem}
    }
  </style>
</head>
<body>
  <a class="skip-link" href="#main">ข้ามไปเนื้อหาหลัก</a>
  <header class="site-header">
    <div class="shell topbar">
      <a class="brand" href="#top" aria-label="PARC Bangna Competition-aware Top 10">
        <img src="__LOGO_SRC__" alt="PARC Bangna">
        <small>Fresh Locale Screen<br>Competition-aware v2.0</small>
      </a>
      <div class="header-tools">
        <div class="report-meta">Board decision checkpoint<br>28 กรกฎาคม 2026</div>
        <button class="icon-button" id="theme-toggle" type="button" aria-label="ธีม: ตามระบบ" title="เปลี่ยนธีม"><span aria-hidden="true">◐</span></button>
      </div>
    </div>
  </header>

  <div class="section-nav-wrap">
    <nav class="shell section-nav" aria-label="ส่วนของรายงาน">
      <a href="#decision">คำตอบ</a>
      <a href="#explore">Top 10</a>
      <a href="#overview">แผนที่รวม</a>
      <a href="#field-map">คู่แข่ง</a>
      <a href="#evidence">หลักฐาน</a>
      <a href="#approval">อนุมัติ</a>
    </nav>
  </div>

  <main id="main" data-location-report data-report-id="__REPORT_ID__">
    <section class="hero" id="top">
      <svg class="motif" viewBox="0 0 480 360" aria-hidden="true">
        <path class="branch" d="M470 60C386 92 360 151 298 174C238 196 185 176 123 230C81 267 52 303 2 322"/>
        <path class="branch" d="M323 165C345 130 359 98 357 62"/>
        <path class="branch" d="M211 190C193 147 169 119 137 99"/>
        <path class="bract" d="M344 94C314 86 292 101 293 126C319 136 345 122 344 94Z"/>
        <path class="bract" d="M365 91C391 73 417 78 427 102C407 124 376 119 365 91Z"/>
        <path class="bract" d="M184 145C153 149 135 170 141 194C170 198 194 176 184 145Z"/>
        <circle class="bud" cx="354" cy="111" r="4"/>
        <circle class="bud" cx="190" cy="171" r="4"/>
      </svg>
      <div class="shell hero-grid">
        <div class="hero-copy">
          <p class="eyebrow">Board decision · 28 July 2026</p>
          <h1>สิบทำเลที่ควรพิสูจน์ ก่อนเลือกสนามจริง</h1>
          <p class="dek">Fresh Screen บอกว่าตลาดไหนมีแรงชีวิต คู่แข่งบอกว่าที่ไหนต้องชนะให้ต่าง รอบนี้จึงขออนุมัติศึกษารายละเอียด Top 10—ไม่ใช่รับรองผู้ชนะ และไม่ใช่อนุมัติลงทุน</p>
          <p class="decision-line">คำตอบที่ต้องการจาก Board: <strong>อนุมัติ 10 investigations ไม่ใช่ 10 investments</strong></p>
          <p class="confidence-line"><strong>ความมั่นใจ: Directional shortlist</strong> · ต้องพิสูจน์ route/crossing, competitor census และแปลง ก่อนเลื่อนเป็น investment shortlist</p>
          <div class="cta-row">
            <a class="button primary" href="#explore">สำรวจ Top 10 <span aria-hidden="true">→</span></a>
            <a class="button secondary" href="#approval">ดูขอบเขตการอนุมัติ</a>
          </div>
        </div>
        <div class="hero-stats" aria-label="สรุปการตัดสินใจ">
          <div class="hero-stat"><strong>10</strong><span>ทำเลที่ขออนุมัติศึกษาละเอียด</span></div>
          <div class="hero-stat"><strong>3</strong><span>กลุ่มตลาดที่ต้องแข่งกันเอง</span></div>
          <div class="hero-stat"><strong>1</strong><span>มติ: พิสูจน์ก่อนเลือกลงทุน</span></div>
        </div>
      </div>
    </section>

    <section class="section" id="decision">
      <div class="shell">
        <div class="section-head">
          <p class="eyebrow">What changed</p>
          <h2>คู่แข่งไม่ได้ลบโอกาส แต่ยกระดับสิ่งที่ต้องพิสูจน์</h2>
          <p>ทั้ง 10 ทำเลมี operating supply ที่มีผล ไม่มีจุดใดควรถูกขายว่าเป็น “พื้นที่ว่าง” ความน่าสนใจจึงอยู่ที่ route advantage, unmet job และแปลง—not จำนวนศูนย์ที่น้อยกว่า</p>
        </div>
        <div class="insight-grid">
          <article class="insight">
            <span class="num">1</span>
            <h3>ไม่มี generic white space</h3>
            <p>ทำเลนำมีทั้ง regional mall, community mall และ routine retail อยู่แล้ว ความหนาแน่นสะท้อน demand แต่ไม่รับรอง room to win</p>
          </article>
          <article class="insight">
            <span class="num">2</span>
            <h3>Green ไม่ใช่ moat</h3>
            <p>EastVille, Crystal และ Central Rama 3 มี nature, pet, wellness, food และ family offer อยู่แล้ว PARC ต้องชนะที่ journey และ frequency</p>
          </article>
          <article class="insight">
            <span class="num">3</span>
            <h3>สิบชื่ออาจไม่ใช่สิบตลาด</h3>
            <p>ฝั่งธนฯ 4 จุด, บางซื่อ 2 จุด และเจริญราษฎร์–พระราม 3 ต้องถูกยุบด้วย network overlap ก่อน final rank</p>
          </article>
        </div>
        <p class="alert" style="margin-top:1rem" data-caveat-id="competition-census-incomplete" data-caveat-severity="decision-changing" data-caveat-visibility="inline"><strong>Evidence boundary:</strong> ยังไม่เผยแพร่ numeric competition rerank ทั้ง 745 เพราะ competitor census และ route/crossing coverage ยังไม่เท่ากันทุก locale</p>
      </div>
    </section>

    <section class="section alt" id="explore">
      <div class="shell">
        <div class="section-head">
          <p class="eyebrow">Explore the shortlist</p>
          <h2>ดูให้ครบ ก่อนกดอนุมัติ</h2>
          <p>เปิดแต่ละทำเลเพื่อดู pressure, คู่แข่ง, proposition ที่ต้องชนะ และ kill test การทำเครื่องหมาย “ดูแล้ว” จะช่วยให้ Board เห็นว่าได้สำรวจครบ 10 แห่ง</p>
        </div>
        <div class="explore-toolbar" aria-label="ตัวกรองและความคืบหน้า">
          <div class="filter-group" role="group" aria-label="กรองทำเล">
            <button class="filter-button" type="button" data-filter="all" aria-pressed="true">ทั้งหมด 10</button>
            <button class="filter-button" type="button" data-filter="prove" aria-pressed="false">พิสูจน์ก่อน 3</button>
            <button class="filter-button" type="button" data-filter="cluster" aria-pressed="false">เลือกตัวแทน 6</button>
            <button class="filter-button" type="button" data-filter="hurdle" aria-pressed="false">Hurdle สูงสุด 1</button>
          </div>
          <div class="review-progress">
            <div class="progress-label"><span>สำรวจแล้ว</span><strong><span data-reviewed-count>0</span>/10</strong></div>
            <div class="progress-track" role="progressbar" aria-label="ความคืบหน้าการสำรวจ Top 10" aria-valuemin="0" aria-valuemax="10" aria-valuenow="0"><div class="progress-fill"></div></div>
          </div>
          <div class="toolbar-row">
            <div class="select-wrap">
              <label for="sort-select">เรียงตาม</label>
              <select id="sort-select">
                <option value="fresh">Fresh baseline</option>
                <option value="study">ลำดับศึกษาที่แนะนำ</option>
              </select>
            </div>
            <a href="#overview">ดูตำแหน่งบนแผนที่รวม →</a>
          </div>
        </div>
        <div class="candidate-grid" id="candidate-grid"></div>
      </div>
    </section>

    <section class="section" id="overview">
      <div class="shell">
        <div class="section-head">
          <p class="eyebrow">Overview map</p>
          <h2>ทำเลที่ดูแยก อาจใช้ตลาดก้อนเดียวกัน</h2>
          <p>แผนที่ใช้ reference points จริงในสเกลเดียวกัน พร้อม analytical cluster outlines และ simplified metric basemap ที่มองเห็นได้ชัด ขอบเขตแขวงยังไม่ถูกวาดเพราะ release นี้ไม่มี approved GeoJSON/WKT</p>
        </div>
        <div class="map-shell" data-location-map data-map-manifest="analysis/fresh-map-manifest-v2.json">
          <div class="map-toolbar">
            <div class="map-title"><strong>Bangkok Fresh Top 10</strong><small>คลิกจุดเพื่อเปิดรายละเอียด</small></div>
            <div class="legend" aria-label="สัญลักษณ์แผนที่">
              <span class="legend-item"><span class="legend-symbol candidate"></span> ทำเล</span>
              <span class="legend-item"><span class="legend-symbol cluster"></span> ตลาดที่อาจทับ</span>
              <span class="legend-item">เส้นกริด = simplified orientation</span>
            </div>
          </div>
          <div class="overview-stage"><svg id="overview-map" viewBox="0 0 760 440" role="img" aria-labelledby="overview-map-title overview-map-desc"></svg></div>
          <p class="map-disclosure"><strong>ไม่ใช่แผนที่เขตหรือแปลง:</strong> grid, labels และ cluster outlines ใช้เพื่อ orientation และตั้งคำถามเท่านั้น ไม่ใช้คำนวณ catchment</p>
          <details class="fallback">
            <summary>ดู Top 10 เป็นตาราง</summary>
            <div class="table-wrap"><table id="shortlist-table" data-map-fallback><thead><tr><th>Fresh rank</th><th>Locale</th><th>Score</th><th>Pressure</th><th>กลุ่มตลาด</th><th>หลักฐาน</th></tr></thead><tbody>__SHORTLIST_ROWS__</tbody></table></div>
          </details>
        </div>
      </div>
    </section>

    <section class="section alt" id="field-map">
      <div class="shell">
        <div class="section-head">
          <p class="eyebrow">Candidate + competitor field</p>
          <h2>คู่แข่งอยู่ตรงไหน และมีผลเพราะอะไร</h2>
          <p>หมุดแสดง impact class ชุดเดียว—High, Medium-high, Medium—ไม่ปลอมว่าเป็น GLA scale หากมี Retail NLA ที่ยืนยันแล้ว จะแสดงวงแหวนและตัวเลขในรายละเอียด</p>
        </div>
        <div class="map-shell">
          <div class="locale-tabs" id="locale-tabs" role="group" aria-label="เลือกทำเลสำหรับแผนที่คู่แข่ง"></div>
          <div class="map-toolbar">
            <div class="map-title"><strong id="detail-map-title">แผนที่คู่แข่ง</strong><small>reference point + 1 กม. grid · ไม่ใช่ locale extent</small></div>
            <div class="legend">
              <span class="legend-item"><span class="legend-symbol candidate"></span> Candidate</span>
              <span class="legend-item"><span class="legend-symbol" style="border-color:var(--risk);background:var(--risk)"></span> High</span>
              <span class="legend-item"><span class="legend-symbol" style="border-color:var(--warning);background:var(--warning)"></span> Medium-high</span>
              <span class="legend-item">วงแหวน = มี NLA ที่ยืนยัน</span>
            </div>
          </div>
          <div class="detail-map-grid">
            <div>
              <div class="detail-map-stage"><svg id="detail-map" viewBox="0 0 680 360" role="img" aria-labelledby="detail-map-title detail-map-desc"></svg></div>
              <p id="detail-map-desc" class="map-disclosure" data-caveat-id="boundary-geometry-unavailable" data-caveat-severity="material" data-caveat-visibility="inline"><strong>Simplified basemap fallback:</strong> ใช้กริดระยะจริงแทนขอบแขวงที่ยังไม่มี geometry ที่อนุมัติ จุดทุกจุดเป็น presentation coordinate</p>
              <div class="competitor-panel" id="competitor-panel" data-competitor-details aria-live="polite" hidden></div>
            </div>
            <aside class="map-side" id="map-side"></aside>
          </div>
          <details class="fallback">
            <summary>ดูคู่แข่งเป็นรายการ</summary>
            <div class="table-wrap"><table id="competitor-table" data-map-fallback><thead><tr><th>#</th><th>คู่แข่ง</th><th>ระยะบริบท</th><th>Impact</th><th>Size basis</th></tr></thead><tbody></tbody></table></div>
          </details>
        </div>
      </div>
    </section>

    <section class="section" id="clusters">
      <div class="shell">
        <div class="section-head">
          <p class="eyebrow">Three decisions inside ten studies</p>
          <h2>ศึกษาครบสิบ—แต่บังคับให้ตลาดทับกันเลือกผู้แทน</h2>
          <p>นี่คือจุดที่ช่วยลดการลงทุนซ้ำ: ถ้า catchment ใช้ demand pool เดียวกัน ให้เดินหน้าสูงสุดหนึ่งตัวแทนและเก็บรายที่สองเป็น backup</p>
        </div>
        <div class="cluster-grid">
          <article class="cluster-card">
            <span class="cluster-count">4 locales → 1–2 representatives</span>
            <h3 style="margin-top:1rem">ฝั่งธนฯ ตอนใต้–กลาง</h3>
            <ul><li>ตลาดพลู-ใต้</li><li>สำเหร่</li><li>วงเวียนใหญ่-ตะวันออก</li><li>แยกบ้านแขก</li></ul>
          </article>
          <article class="cluster-card">
            <span class="cluster-count">2 locales → 1 representative</span>
            <h3 style="margin-top:1rem">บางซื่อริมแม่น้ำ</h3>
            <ul><li>บางซ่อน</li><li>บางโพ-ตะวันออก</li></ul>
          </article>
          <article class="cluster-card">
            <span class="cluster-count">2 locales → 1 representative</span>
            <h3 style="margin-top:1rem">เจริญราษฎร์–พระราม 3</h3>
            <ul><li>เจริญราษฎร์</li><li>พระราม 3-ตะวันออก</li></ul>
          </article>
        </div>
      </div>
    </section>

    <section class="section alt" id="evidence">
      <div class="shell">
        <div class="section-head">
          <p class="eyebrow">Evidence boundary</p>
          <h2>เห็นข้อเท็จจริง และเห็นสิ่งที่ยังไม่รู้</h2>
          <p>ความน่าเชื่อถือไม่ได้มาจากการเติมตัวเลขให้ครบ แต่มาจากการไม่ให้ unknown กลายเป็นศูนย์ และไม่ใช้ total area หรือ tenant directory แทน Retail NLA</p>
        </div>
        <div class="evidence-grid">
          <article class="evidence-card known"><strong>รู้แล้ว</strong><p>Fresh baseline, candidate reference points, operating status ของคู่แข่งหลัก และ NLA จาก operator/REIT บางแห่ง</p></article>
          <article class="evidence-card unknown"><strong>ยังต้องพิสูจน์</strong><p>route/crossing catchments, complete operating census, locale polygons, current NLA หลายศูนย์, field weakness และ parcel access</p></article>
          <article class="evidence-card prohibited" data-caveat-id="fresh-score-not-investment-rank" data-caveat-severity="material" data-caveat-visibility="evidence"><strong>ห้ามสรุป</strong><p>ระยะตรงเป็น catchment, directory listings เป็น occupied tenants, GFA เป็น NLA หรือคะแนน Fresh เป็น investment recommendation</p></article>
        </div>
        <div class="evidence-table-card">
          <header><h3>Retail NLA ที่มีหลักฐานใช้ได้ในรอบนี้</h3><p style="margin:0;color:var(--secondary)">ตัวเลขเหล่านี้แสดงใน detail เท่านั้น marker ยังคงใช้ disclosed impact class เพื่อไม่ผสม basis</p></header>
          <div class="table-wrap"><table id="nla-table"><thead><tr><th>Venue</th><th data-number>Retail NLA</th><th>Metric status</th></tr></thead><tbody></tbody></table></div>
        </div>
        <details class="fallback" style="margin-top:1rem;border:1px solid var(--line);border-radius:var(--r-md);background:var(--card)">
          <summary>ทำไมยังไม่ re-rank ทั้ง 745 ด้วยคะแนนใหม่</summary>
          <div class="reading" style="padding:0 1.15rem 1rem;color:var(--secondary)">
            <p>เพราะความครบของคู่แข่งยังต่างกันตามพื้นที่ และ route matrix ยังไม่ได้ใช้ crossing registry เดียวกันทุก locale หากปรับคะแนนเฉพาะทำเลที่มีข้อมูลมาก จะลงโทษพื้นที่ที่สำรวจละเอียดกว่าและให้รางวัลพื้นที่ที่ยังไม่รู้ข้อมูล</p>
            <p>ลำดับที่แสดงจึงแยก Fresh baseline ออกจาก competition pressure และ study sequence อย่างชัดเจน เมื่อ competitor registry, routing snapshot, parent-cluster dedupe และ unknown treatment พร้อมเท่ากัน จึงคำนวณ 745 ใหม่พร้อมกัน</p>
          </div>
        </details>
        <details class="fallback" style="margin-top:1rem;border:1px solid var(--line);border-radius:var(--r-md);background:var(--card)">
          <summary>แหล่งข้อมูลหลัก</summary>
          <ul class="reading" style="padding:0 2rem 1rem;color:var(--secondary)">__SOURCE_LIST__</ul>
        </details>
      </div>
    </section>

    <section class="section approval" id="approval" data-recommendation-mode="shortlist" data-recommendation-candidate-ids="__CANDIDATE_IDS__">
      <div class="shell approval-grid">
        <div>
          <p class="eyebrow">Decision requested</p>
          <h2>อนุมัติศึกษารายละเอียด Top 10</h2>
          <p style="max-width:42rem;margin-top:1.4rem">ตรวจเส้นทาง คู่แข่ง ความต้องการลูกค้า แปลง และ economics เพื่อกลับมาพร้อม shortlist 3–5 ทำเล—ยังไม่ใช่อนุมัติเลือกแปลงหรืออนุมัติลงทุน</p>
          <div class="approval-scope">
            <div class="scope-item">10 locale dossiers</div>
            <div class="scope-item">3 market-cluster decisions</div>
            <div class="scope-item">Stop reasons + downside scenarios</div>
          </div>
        </div>
        <div class="approval-card">
          <p><strong>ขอบเขตมติ</strong><br>Top 10 เท่านั้น—not 745 detailed studies</p>
          <button class="button primary full" type="button" id="open-approval" data-primary-cta data-owner="__CTA_OWNER__" data-timing="__CTA_TIMING__" data-cta-candidate-ids="__CANDIDATE_IDS__" data-next-stage="__CTA_NEXT_STAGE__">เปิดร่างมติอนุมัติ <span aria-hidden="true">→</span></button>
          <a class="button secondary full" style="margin-top:.65rem" href="__REPORT_FILE__" download>ดาวน์โหลดรายงาน .md</a>
          <p style="margin:.8rem 0 0;font-size:.82rem">สำรวจแล้ว <strong><span data-reviewed-count>0</span>/10</strong></p>
        </div>
      </div>
    </section>
  </main>

  <footer>
    <div class="shell footer-grid">
      <div>Fresh Locale Screen v2.0 · Competition-aware Board checkpoint · 28 กรกฎาคม 2026</div>
      <div>Venue Locale Insight v2.3.1 · Venue Fundamental v0.2.0-rc1 · Operator evidence as cited</div>
    </div>
  </footer>

  <div class="decision-dock" aria-label="แถบการตัดสินใจ">
    <div class="dock-copy"><strong><span data-reviewed-count>0</span>/10 ดูแล้ว</strong><span> · scope = Top 10 detailed study</span></div>
    <a class="button primary" href="#approval">ไปที่การอนุมัติ</a>
  </div>

  <dialog id="locale-dialog" aria-labelledby="locale-dialog-title">
    <div class="dialog-head"><div><small id="locale-dialog-kicker"></small><h3 id="locale-dialog-title"></h3></div><button class="dialog-close" type="button" data-close-dialog aria-label="ปิด">×</button></div>
    <div class="dialog-body" id="locale-dialog-body"></div>
  </dialog>

  <dialog id="approval-dialog" aria-labelledby="approval-dialog-title">
    <div class="dialog-head"><div><small>Board resolution draft</small><h3 id="approval-dialog-title">อนุมัติศึกษารายละเอียด Top 10</h3></div><button class="dialog-close" type="button" data-close-dialog aria-label="ปิด">×</button></div>
    <div class="dialog-body">
      <p class="resolution" id="resolution-text">อนุมัติให้ฝ่ายบริหารดำเนินการศึกษารายละเอียด Top 10 ทำเลจาก PARC Bangna Fresh Locale Screen ครบทั้ง 10 แห่ง โดยครอบคลุม route-based catchment, competitor census, customer unmet jobs, market overlap, candidate parcel access และ preliminary economics เพื่อกลับมาเสนอ shortlist ไม่เกิน 3–5 ทำเลพร้อม stop reasons และ downside scenarios ทั้งนี้การอนุมัติครั้งนี้ไม่ใช่การอนุมัติเลือกทำเล ซื้อที่ดิน หรืออนุมัติลงทุนโครงการ</p>
      <div class="dialog-facts">
        <div class="dialog-fact"><strong>รวม</strong> Top 10 locale dossiers และ 3 cluster decisions</div>
        <div class="dialog-fact"><strong>ไม่รวม</strong> ซื้อที่ดิน, CAPEX approval, final site selection และ detailed study 745 locales</div>
        <div class="dialog-fact"><strong>กลับมาเมื่อ</strong> มี shortlist 3–5 ทำเล, stop reasons, economics range และ downside scenarios</div>
      </div>
      <button class="button primary full" type="button" id="copy-resolution">คัดลอกร่างมติ</button>
    </div>
  </dialog>

  <div class="toast" id="toast" role="status" aria-live="polite"></div>
  <script type="application/json" id="report-data">__DATA_JSON__</script>
  <script>
  (function(){
    "use strict";
    var data = JSON.parse(document.getElementById("report-data").textContent);
    var candidates = data.candidates;
    var competitors = data.competitors;
    var compById = new Map(competitors.map(function(d){ return [d.id,d]; }));
    var reviewedKey = "parc-fresh-v2-reviewed";
    var reviewed = new Set();
    try { reviewed = new Set(JSON.parse(localStorage.getItem(reviewedKey) || "[]")); } catch(e) {}
    var currentFilter = "all";
    var currentSort = "fresh";
    var selectedCandidateId = candidates[0].id;
    var lastMarker = null;
    var esc = function(value){ return String(value == null ? "" : value).replace(/[&<>"']/g,function(ch){ return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[ch]; }); };
    var fmt = new Intl.NumberFormat("th-TH");
    var clusterLabels = {
      "thonburi-south":"ฝั่งธนฯ ตอนใต้–กลาง",
      "bang-sue":"บางซื่อริมแม่น้ำ",
      "charoen-rama3":"เจริญราษฎร์–พระราม 3",
      "wang-hin":"ลาดพร้าว–วังหิน",
      "bang-khun-non":"บางขุนนนท์"
    };
    var groupLabels = {prove:"พิสูจน์ก่อน",cluster:"เลือกตัวแทน",hurdle:"Hurdle สูงสุด"};
    var pressureClass = function(c){
      if(c.pressure.indexOf("very_high") === 0) return "very_high";
      if(c.pressure.indexOf("high") === 0) return "high";
      return "medium_high_route_sensitive";
    };
    function kmDistance(a,b){
      var p = Math.PI/180, R = 6371.0088;
      var dLat = (b.lat-a.lat)*p, dLon = (b.lon-a.lon)*p;
      var x = Math.sin(dLat/2)*Math.sin(dLat/2)+Math.cos(a.lat*p)*Math.cos(b.lat*p)*Math.sin(dLon/2)*Math.sin(dLon/2);
      return 2*R*Math.asin(Math.sqrt(x));
    }
    function persistReviewed(){
      try { localStorage.setItem(reviewedKey,JSON.stringify(Array.from(reviewed))); } catch(e) {}
      renderReviewed();
    }
    function renderReviewed(){
      var count = reviewed.size;
      document.querySelectorAll("[data-reviewed-count]").forEach(function(el){el.textContent=count;});
      var progress = document.querySelector(".progress-track");
      progress.setAttribute("aria-valuenow",String(count));
      document.querySelector(".progress-fill").style.width=(count*10)+"%";
      document.querySelectorAll(".candidate-card").forEach(function(card){
        var on = reviewed.has(card.dataset.id);
        card.classList.toggle("is-reviewed",on);
        var btn = card.querySelector(".review-button");
        if(btn){ btn.setAttribute("aria-pressed",String(on)); btn.textContent=on?"✓ ดูแล้ว":"ทำเครื่องหมายว่าดูแล้ว"; }
      });
    }
    function cardHtml(c){
      return '<article class="candidate-card" data-id="'+esc(c.id)+'" data-group="'+esc(c.group)+'">'+
        '<div class="card-top"><span class="rank"><strong>'+c.fresh_rank+'</strong> Fresh rank</span><div class="score"><strong>'+c.fresh_score.toFixed(1)+'</strong><span>ช่วง '+esc(c.rank_range)+'</span></div></div>'+
        '<h3>'+esc(c.name_th)+'</h3>'+
        '<div class="pressure-row"><span class="pill '+pressureClass(c)+'">'+esc(c.pressure_th)+'</span><span class="pill">'+esc(groupLabels[c.group])+'</span></div>'+
        '<p class="card-headline">'+esc(c.headline_th)+'</p>'+
        '<div class="mini-bars" aria-label="คะแนนองค์ประกอบ">'+
          miniBar("ฐานคน",c.resident)+miniBar("กิจวัตร",c.routine)+miniBar("นอกบ้าน",c.out_of_home)+
        '</div>'+
        '<div class="card-meta"><span>'+c.competitor_ids.length+' คู่แข่งใน evidence set</span><span>'+esc(clusterLabels[c.market_cluster])+'</span></div>'+
        '<div class="card-actions"><button class="explore-button" type="button" data-open-locale="'+esc(c.id)+'">สำรวจหลักฐาน <span aria-hidden="true">→</span></button><button class="review-button" type="button" data-review="'+esc(c.id)+'" aria-pressed="false">ทำเครื่องหมายว่าดูแล้ว</button></div>'+
      '</article>';
    }
    function miniBar(label,value){
      return '<div class="mini-bar"><span>'+label+'</span><span><i style="width:'+Math.max(0,Math.min(100,value))+'%"></i></span><output>'+value.toFixed(1)+'</output></div>';
    }
    function renderCards(){
      var list = candidates.slice().sort(function(a,b){return currentSort==="study"?a.study_order-b.study_order:a.fresh_rank-b.fresh_rank;});
      document.getElementById("candidate-grid").innerHTML=list.map(cardHtml).join("");
      document.querySelectorAll(".candidate-card").forEach(function(card){ card.hidden=currentFilter!=="all"&&card.dataset.group!==currentFilter; });
      renderReviewed();
    }
    function openDialog(dialog){
      if(typeof dialog.showModal==="function") dialog.showModal(); else dialog.setAttribute("open","");
      document.body.classList.add("modal-open");
    }
    function closeDialog(dialog){
      if(dialog.open && typeof dialog.close==="function") dialog.close(); else dialog.removeAttribute("open");
      document.body.classList.remove("modal-open");
    }
    function openLocale(id){
      var c = candidates.find(function(x){return x.id===id;});
      if(!c) return;
      document.getElementById("locale-dialog-kicker").textContent="Fresh rank "+c.fresh_rank+" · Study sequence "+c.study_order+" · "+c.pressure_th;
      document.getElementById("locale-dialog-title").textContent=c.name_th;
      var names=c.competitor_ids.map(function(x){return compById.get(x);}).filter(Boolean).map(function(x){return x.name;});
      document.getElementById("locale-dialog-body").innerHTML=
        '<p style="font-size:1.18rem">'+esc(c.headline_th)+'</p>'+
        '<div class="dialog-facts">'+
          '<div class="dialog-fact"><strong>ต้องชนะอย่างไร</strong>'+esc(c.strategy_th)+'</div>'+
          '<div class="dialog-fact"><strong>สิ่งที่ต้องเป็นจริง</strong>'+esc(c.must_be_true_th)+'</div>'+
          '<div class="dialog-fact"><strong>Kill test</strong>'+esc(c.kill_test_th)+'</div>'+
        '</div>'+
        '<p><strong>คู่แข่งใน evidence set</strong><br>'+esc(names.join(" · "))+'</p>'+
        '<div class="cta-row"><button class="button primary" type="button" data-open-map="'+esc(c.id)+'">เปิดแผนที่คู่แข่ง</button><button class="button secondary" type="button" data-mark-dialog="'+esc(c.id)+'">'+(reviewed.has(c.id)?"✓ ดูแล้ว":"ทำเครื่องหมายว่าดูแล้ว")+'</button></div>'+
        '<p style="margin-top:1rem;color:var(--metadata);font-size:.84rem">Fresh score '+c.fresh_score.toFixed(1)+' ยังคงเป็น baseline; pressure ไม่ได้ถูกใช้สร้างอันดับลงทุนใหม่</p>';
      openDialog(document.getElementById("locale-dialog"));
    }
    document.addEventListener("click",function(e){
      var open=e.target.closest("[data-open-locale]"); if(open){openLocale(open.dataset.openLocale);return;}
      var review=e.target.closest("[data-review]"); if(review){var id=review.dataset.review; reviewed.has(id)?reviewed.delete(id):reviewed.add(id);persistReviewed();return;}
      var mark=e.target.closest("[data-mark-dialog]"); if(mark){reviewed.add(mark.dataset.markDialog);persistReviewed();mark.textContent="✓ ดูแล้ว";return;}
      var map=e.target.closest("[data-open-map]"); if(map){selectedCandidateId=map.dataset.openMap;closeDialog(document.getElementById("locale-dialog"));renderDetailMap();document.getElementById("field-map").scrollIntoView({behavior:"smooth"});return;}
      var close=e.target.closest("[data-close-dialog]"); if(close){closeDialog(close.closest("dialog"));return;}
    });
    document.querySelectorAll("dialog").forEach(function(dialog){
      dialog.addEventListener("click",function(e){if(e.target===dialog) closeDialog(dialog);});
      dialog.addEventListener("close",function(){document.body.classList.remove("modal-open");});
    });
    document.querySelectorAll(".filter-button").forEach(function(button){
      button.addEventListener("click",function(){
        currentFilter=button.dataset.filter;
        document.querySelectorAll(".filter-button").forEach(function(b){b.setAttribute("aria-pressed",String(b===button));});
        renderCards();
      });
    });
    document.getElementById("sort-select").addEventListener("change",function(e){currentSort=e.target.value;renderCards();});
    function renderOverview(){
      var svg=document.getElementById("overview-map"), W=760,H=440,pad=62;
      var minLon=Math.min.apply(null,candidates.map(function(c){return c.lon;}))-.015;
      var maxLon=Math.max.apply(null,candidates.map(function(c){return c.lon;}))+.015;
      var minLat=Math.min.apply(null,candidates.map(function(c){return c.lat;}))-.012;
      var maxLat=Math.max.apply(null,candidates.map(function(c){return c.lat;}))+.012;
      var x=function(lon){return pad+(lon-minLon)/(maxLon-minLon)*(W-pad*2);};
      var y=function(lat){return H-pad-(lat-minLat)/(maxLat-minLat)*(H-pad*2);};
      var out=['<title id="overview-map-title">แผนที่รวม Top 10 ทำเล</title><desc id="overview-map-desc">แผนที่สเกลเดียวกัน แสดง reference points, simplified metric grid และกลุ่มตลาดที่อาจทับกัน ไม่มีขอบเขตแขวงหรือแปลง</desc>'];
      out.push('<rect x="0" y="0" width="'+W+'" height="'+H+'" fill="var(--alt)"/>');
      for(var i=0;i<=8;i++){var gx=pad+i*(W-pad*2)/8;out.push('<line class="'+(i%2===0?'map-grid-bold':'map-grid-line')+'" x1="'+gx+'" y1="'+pad+'" x2="'+gx+'" y2="'+(H-pad)+'"/>');}
      for(var j=0;j<=5;j++){var gy=pad+j*(H-pad*2)/5;out.push('<line class="'+(j%2===0?'map-grid-bold':'map-grid-line')+'" x1="'+pad+'" y1="'+gy+'" x2="'+(W-pad)+'" y2="'+gy+'"/>');}
      var clusters=["thonburi-south","bang-sue","charoen-rama3"];
      clusters.forEach(function(cluster){
        var pts=candidates.filter(function(c){return c.market_cluster===cluster;});
        var xs=pts.map(function(c){return x(c.lon);}),ys=pts.map(function(c){return y(c.lat);});
        var minX=Math.min.apply(null,xs)-32,maxX=Math.max.apply(null,xs)+32,minY=Math.min.apply(null,ys)-28,maxY=Math.max.apply(null,ys)+28;
        out.push('<rect class="cluster-hull" x="'+minX+'" y="'+minY+'" width="'+(maxX-minX)+'" height="'+(maxY-minY)+'" rx="30"><title>'+esc(clusterLabels[cluster])+'</title></rect>');
        out.push('<text class="map-label" x="'+minX+'" y="'+(minY-8)+'">'+esc(clusterLabels[cluster])+'</text>');
      });
      candidates.forEach(function(c){
        out.push('<g class="map-candidate" role="button" tabindex="0" data-overview-candidate="'+esc(c.id)+'" aria-label="Fresh rank '+c.fresh_rank+' '+esc(c.name_th)+' pressure '+esc(c.pressure_th)+'">'+
          '<circle class="candidate-map-hit" cx="'+x(c.lon)+'" cy="'+y(c.lat)+'" r="24"/>'+
          '<circle class="candidate-map-core" cx="'+x(c.lon)+'" cy="'+y(c.lat)+'" r="15"/>'+
          '<text class="candidate-map-number" x="'+x(c.lon)+'" y="'+y(c.lat)+'">'+c.fresh_rank+'</text>'+
          '<title>'+esc(c.name_th)+' · '+esc(c.pressure_th)+'</title></g>');
      });
      out.push('<g class="north-scale"><path d="M710 82V42M710 42l-7 11M710 42l7 11"/><text x="704" y="31">N</text><path d="M74 391h110M74 385v12M184 385v12"/><text x="74" y="414">ประมาณ 5 กม.</text></g>');
      svg.innerHTML=out.join("");
      svg.querySelectorAll("[data-overview-candidate]").forEach(function(node){
        var activate=function(){openLocale(node.dataset.overviewCandidate);};
        node.addEventListener("click",activate);
        node.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){e.preventDefault();activate();}});
      });
      document.querySelector("#shortlist-table tbody").innerHTML=candidates.map(function(c){return '<tr data-candidate-id="'+esc(c.id)+'" data-candidate-name="'+esc(c.name)+'" data-rank="'+c.rank+'" data-score="'+c.score+'" data-map-candidate-id="'+esc(c.id)+'"><td>'+c.fresh_rank+'</td><th>'+esc(c.name_th)+'</th><td data-number>'+c.fresh_score.toFixed(1)+'</td><td>'+esc(c.pressure_th)+'</td><td>'+esc(clusterLabels[c.market_cluster])+'</td><td><button class="evidence-table-button" type="button" data-evidence-toggle data-evidence-candidate-id="'+esc(c.id)+'" data-open-locale="'+esc(c.id)+'">เปิดหลักฐาน</button></td></tr>';}).join("");
    }
    function renderTabs(){
      var tabs=document.getElementById("locale-tabs");
      tabs.innerHTML=candidates.map(function(c){return '<button class="locale-tab" type="button" data-locale-tab="'+esc(c.id)+'" aria-pressed="'+String(c.id===selectedCandidateId)+'" aria-label="'+esc(c.name_th)+'">'+c.fresh_rank+'</button>';}).join("");
      tabs.querySelectorAll("[data-locale-tab]").forEach(function(btn){btn.addEventListener("click",function(){selectedCandidateId=btn.dataset.localeTab;renderDetailMap();});});
    }
    function renderDetailMap(){
      renderTabs();
      var c=candidates.find(function(x){return x.id===selectedCandidateId;})||candidates[0];
      var svg=document.getElementById("detail-map"), W=680,H=360,halfX=5.5,halfY=3.15,innerX=W/2-32,innerY=H/2-28;
      svg.dataset.mapCandidateId=c.id;
      document.getElementById("detail-map-title").textContent=c.name_th+" — competitive field";
      var xFromKm=function(v){return W/2+(v/halfX)*innerX;},yFromKm=function(v){return H/2-(v/halfY)*innerY;};
      var out=['<title>'+esc(c.name_th)+' competitor field</title><desc>แผนที่ reference point และ competitor markers บนกริด 1 กิโลเมตร ไม่มี locale polygon</desc>','<rect x="0" y="0" width="'+W+'" height="'+H+'" fill="var(--alt)"/>'];
      for(var gx=-5;gx<=5;gx++){var xx=xFromKm(gx);out.push('<line class="'+(gx===0?'map-grid-bold':'map-grid-line')+'" x1="'+xx+'" y1="20" x2="'+xx+'" y2="'+(H-20)+'"/>');if(gx!==0)out.push('<text class="map-label" x="'+(xx+3)+'" y="'+(H-8)+'">'+Math.abs(gx)+' กม.</text>');}
      for(var gy=-3;gy<=3;gy++){var yy=yFromKm(gy);out.push('<line class="'+(gy===0?'map-grid-bold':'map-grid-line')+'" x1="20" y1="'+yy+'" x2="'+(W-20)+'" y2="'+yy+'"/>');}
      out.push('<g aria-label="Candidate reference point"><rect class="candidate-map-core" x="'+(W/2-15)+'" y="'+(H/2-15)+'" width="30" height="30" rx="7"/><text class="candidate-map-number" x="'+W/2+'" y="'+H/2+'">'+c.fresh_rank+'</text><title>'+esc(c.name_th)+' reference point</title></g>');
      var rows=[];
      c.competitor_ids.forEach(function(id,index){
        var comp=compById.get(id); if(!comp)return;
        var dx=(comp.lon-c.lon)*111.32*Math.cos(c.lat*Math.PI/180),dy=(comp.lat-c.lat)*111.32;
        var dist=kmDistance(c,comp),radius=comp.impact_class==="high"?18:comp.impact_class==="medium_high"?14:11;
        var px=xFromKm(dx),py=yFromKm(dy);
        if(Math.abs(dx)>halfX||Math.abs(dy)>halfY){rows.push([comp,dist,index+1,false]);return;}
        var ring=comp.retail_nla_sqm?'<circle class="poi-nla-ring" cx="'+px+'" cy="'+py+'" r="'+(radius+4)+'"/>':'';
        out.push('<g class="poi-marker" role="button" tabindex="0" data-competitor-id="'+esc(comp.id)+'" data-map-candidate-id="'+esc(c.id)+'" data-impact-class="'+esc(comp.impact_class)+'" data-size-basis="'+esc(comp.impact_basis)+'" aria-label="'+esc(comp.name)+' '+esc(comp.impact_class)+' ระยะบริบท '+dist.toFixed(2)+' กิโลเมตร">'+
          '<circle class="poi-hit" cx="'+px+'" cy="'+py+'" r="24"/>'+
          '<circle class="poi-core '+esc(comp.impact_class)+'" cx="'+px+'" cy="'+py+'" r="'+radius+'"/>'+ring+
          '<text class="poi-index" x="'+px+'" y="'+py+'">'+(index+1)+'</text><title>'+esc(comp.name)+' · '+dist.toFixed(2)+' กม.</title></g>');
        rows.push([comp,dist,index+1,true]);
      });
      out.push('<g class="north-scale"><path d="M640 70V34M640 34l-6 10M640 34l6 10"/><text x="634" y="24">N</text><path d="M34 320h58M34 314v12M92 314v12"/><text x="34" y="342">1 กม.</text></g>');
      svg.innerHTML=out.join("");
      document.querySelectorAll(".locale-tab").forEach(function(btn){btn.setAttribute("aria-pressed",String(btn.dataset.localeTab===c.id));});
      svg.querySelectorAll(".poi-marker").forEach(function(node){
        var activate=function(){lastMarker=node;showCompetitor(c,compById.get(node.dataset.competitorId));};
        node.addEventListener("click",activate);
        node.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){e.preventDefault();activate();}});
      });
      var unmapped=(c.unmapped_competitor_ids||[]).map(function(id){return data.unmapped_competitors.find(function(x){return x.id===id;});}).filter(Boolean);
      document.getElementById("map-side").innerHTML=
        '<span class="pill '+pressureClass(c)+'">'+esc(c.pressure_th)+'</span><h3 style="margin-top:.8rem">'+esc(c.name_th)+'</h3>'+
        '<p>'+esc(c.headline_th)+'</p>'+
        '<dl><dt>Fresh</dt><dd>#'+c.fresh_rank+' · '+c.fresh_score.toFixed(1)+'</dd><dt>Study</dt><dd>#'+c.study_order+' · '+esc(groupLabels[c.group])+'</dd><dt>Extent</dt><dd>รอ approved geometry</dd></dl>'+
        '<p><strong>ต้องชนะ:</strong> '+esc(c.strategy_th)+'</p>'+
        '<p><strong>Kill test:</strong> '+esc(c.kill_test_th)+'</p>'+
        (unmapped.length?'<p class="alert"><strong>ไม่วาด marker:</strong> '+esc(unmapped.map(function(x){return x.name;}).join(", "))+'—coordinate lineage/size ยังไม่ผ่าน</p>':'');
      var table=document.querySelector("#competitor-table tbody");
      table.innerHTML=rows.map(function(row){var comp=row[0],dist=row[1],num=row[2],shown=row[3];return '<tr data-competitor-id="'+esc(comp.id)+'"><td>'+num+'</td><th>'+esc(comp.name)+(shown?'':' <small>(นอกกรอบ)</small>')+'</th><td>'+dist.toFixed(2)+' กม.</td><td>'+esc(comp.impact_class.replace("_","-"))+'</td><td>'+(comp.retail_nla_sqm?fmt.format(comp.retail_nla_sqm)+' ตร.ม.':'ขนาดยังไม่ยืนยัน')+'</td></tr>';}).join("");
      document.getElementById("competitor-panel").hidden=true;
      document.getElementById("competitor-panel").innerHTML="";
    }
    function showCompetitor(candidate,comp){
      if(!comp)return;
      var dist=kmDistance(candidate,comp);
      var panel=document.getElementById("competitor-panel");
      var metric=comp.retail_nla_sqm?fmt.format(comp.retail_nla_sqm)+" ตร.ม. · "+comp.size_status:comp.size_status;
      panel.dataset.competitorId=comp.id;
      panel.dataset.evidenceStatus=comp.status;
      panel.innerHTML=
        '<span class="kicker">คู่แข่ง #'+(candidate.competitor_ids.indexOf(comp.id)+1)+' · '+dist.toFixed(2)+' กม. ระยะตรงเพื่อ orientation</span>'+
        '<h4>'+esc(comp.name)+'</h4>'+
        '<div class="competitor-panel-grid"><div><p><strong>Impact:</strong> '+esc(comp.impact_class.replace("_","-"))+' · basis = '+esc(comp.impact_basis)+'</p><p><strong>Size:</strong> '+esc(metric)+'</p><p><strong>Status:</strong> '+esc(comp.status)+' · '+esc(comp.status_as_of)+'</p></div>'+
        '<div><p><strong>ทำได้ดี:</strong> '+esc(comp.strength_th)+'</p><p><strong>สิ่งที่ต้องทดสอบ:</strong> '+esc(comp.gap_th)+'</p></div></div>'+
        '<div class="source-links">'+comp.sources.map(function(url,i){return '<a href="'+esc(url)+'" target="_blank" rel="noreferrer">เปิดหลักฐาน '+(i+1)+' ↗</a>';}).join("")+'</div>';
      panel.hidden=false;
      panel.setAttribute("tabindex","-1");
      panel.focus();
    }
    document.addEventListener("keydown",function(e){
      if(e.key==="Escape"){
        var panel=document.getElementById("competitor-panel");
        if(!panel.hidden){panel.hidden=true;panel.innerHTML="";if(lastMarker)lastMarker.focus();lastMarker=null;}
      }
    });
    function renderNlaTable(){
      var list=competitors.filter(function(c){return Number.isFinite(c.retail_nla_sqm);}).sort(function(a,b){return b.retail_nla_sqm-a.retail_nla_sqm;});
      document.querySelector("#nla-table tbody").innerHTML=list.map(function(c){return '<tr><th>'+esc(c.name)+'</th><td data-number>'+fmt.format(c.retail_nla_sqm)+' ตร.ม.</td><td>'+esc(c.size_status)+'</td></tr>';}).join("");
    }
    var themeButton=document.getElementById("theme-toggle"),themeStates=["system","light","dark"],themeIcons={system:"◐",light:"☀",dark:"☾"},themeLabels={system:"ตามระบบ",light:"สว่าง",dark:"มืด"};
    var savedTheme="system";try{savedTheme=localStorage.getItem("parc-theme")||"system";}catch(e){}
    if(themeStates.indexOf(savedTheme)<0)savedTheme="system";
    function setTheme(state){document.documentElement.dataset.theme=state;themeButton.querySelector("span").textContent=themeIcons[state];themeButton.setAttribute("aria-label","ธีม: "+themeLabels[state]);themeButton.title="ธีม: "+themeLabels[state];try{localStorage.setItem("parc-theme",state);}catch(e){}}
    setTheme(savedTheme);
    themeButton.addEventListener("click",function(){var current=document.documentElement.dataset.theme;setTheme(themeStates[(themeStates.indexOf(current)+1)%themeStates.length]);});
    document.getElementById("open-approval").addEventListener("click",function(){openDialog(document.getElementById("approval-dialog"));});
    document.getElementById("copy-resolution").addEventListener("click",function(){
      var text=document.getElementById("resolution-text").textContent.trim();
      var done=function(){showToast("คัดลอกร่างมติแล้ว");};
      if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(done).catch(function(){fallbackCopy(text);});}else fallbackCopy(text);
    });
    function fallbackCopy(text){var ta=document.createElement("textarea");ta.value=text;document.body.appendChild(ta);ta.select();document.execCommand("copy");ta.remove();showToast("คัดลอกร่างมติแล้ว");}
    function showToast(message){var toast=document.getElementById("toast");toast.textContent=message;toast.classList.add("show");setTimeout(function(){toast.classList.remove("show");},2200);}
    var sections=Array.from(document.querySelectorAll("main section[id]")),navLinks=Array.from(document.querySelectorAll(".section-nav a"));
    if("IntersectionObserver" in window){
      var observer=new IntersectionObserver(function(entries){
        var visible=entries.filter(function(e){return e.isIntersecting;}).sort(function(a,b){return b.intersectionRatio-a.intersectionRatio;})[0];
        if(!visible)return;
        navLinks.forEach(function(link){link.setAttribute("aria-current",String(link.getAttribute("href")==="#"+visible.target.id));});
      },{rootMargin:"-20% 0px -68% 0px",threshold:[0,.15,.4]});
      sections.forEach(function(s){observer.observe(s);});
    }
    renderCards();renderOverview();renderDetailMap();renderNlaTable();renderReviewed();
    var decisionDock=document.querySelector(".decision-dock");
    var hero=document.querySelector(".hero");
    if("IntersectionObserver" in window&&decisionDock&&hero){
      var dockObserver=new IntersectionObserver(function(entries){
        decisionDock.classList.toggle("is-visible",!entries[0].isIntersecting);
      },{threshold:.08});
      dockObserver.observe(hero);
    }
  })();
  </script>
</body>
</html>`;

html = html
  .replace("__FONT_CSS__", fontCss)
  .replaceAll("__LOGO_SRC__", logoSrc)
  .replaceAll("__DATA_JSON__", dataJson)
  .replaceAll("__REPORT_FILE__", reportFileName)
  .replaceAll("__CANDIDATE_IDS__", candidateIdsAttr)
  .replaceAll("__SHORTLIST_ROWS__", shortlistRows)
  .replaceAll("__SOURCE_LIST__", sourceList)
  .replaceAll("__CTA_OWNER__", ctaOwner)
  .replaceAll("__CTA_TIMING__", ctaTiming)
  .replaceAll("__CTA_NEXT_STAGE__", ctaNextStage)
  .replaceAll("__REPORT_ID__", reportId);

fs.writeFileSync(outputPath, html, "utf8");
fs.writeFileSync(indexPath, html, "utf8");
fs.copyFileSync(reportPath, publishedReportPath);
console.log(JSON.stringify({
  output: outputPath,
  index: indexPath,
  manifest: manifestPath,
  report: publishedReportPath,
  bytes: Buffer.byteLength(html),
  candidates: payload.candidates.length,
  competitors: payload.competitors.length
}, null, 2));
