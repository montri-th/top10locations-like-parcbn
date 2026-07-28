#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const root = path.resolve(__dirname, "..");
const files = {
  html: path.join(root, "PARC_Bangna_Fresh_Locale_Screen_Board_Explainer_v2.0_Competition_Aware_2026-07-28.html"),
  index: path.join(root, "index.html"),
  payload: path.join(root, "analysis", "fresh-competition-aware-payload-v2.json"),
  manifest: path.join(root, "analysis", "fresh-map-manifest-v2.json"),
  report: path.join(root, "PARC_Bangna_Fresh_Locale_Screen_Competition_Aware_Board_Brief_v0.2_2026-07-28.md"),
  publishedReport: path.join(root, "analysis", "PARC_Bangna_Fresh_Locale_Screen_Competition_Aware_Board_Brief_v0.2_2026-07-28.md")
};

const html = fs.readFileSync(files.html, "utf8");
const index = fs.readFileSync(files.index, "utf8");
const payload = JSON.parse(fs.readFileSync(files.payload, "utf8"));
const manifest = JSON.parse(fs.readFileSync(files.manifest, "utf8"));
const report = fs.readFileSync(files.report, "utf8");
const publishedReport = fs.readFileSync(files.publishedReport, "utf8");
const staticHtml = html.slice(0, html.indexOf('<script type="application/json" id="report-data">'));
const failures = [];
const check = (condition, message) => { if (!condition) failures.push(message); };
const ids = (value) => new Set(String(value || "").split(",").map((d) => d.trim()).filter(Boolean));
const sameSet = (a, b) => a.size === b.size && [...a].every((value) => b.has(value));
const sha = (value) => crypto.createHash("sha256").update(value).digest("hex");

check(html === index, "index.html must exactly match the named HTML checkpoint");
check(report === publishedReport, "published report copy must exactly match the root checkpoint");
check(!/(?:__[-A-Z0-9_]+__|\bTODO\b|\bTBD\b|LOREM IPSUM)/i.test(html), "HTML contains an unresolved placeholder");
check(!/project_sources\/(?:06|07|08|09|10)-/i.test(html), "Release must not embed supplied stock-reference imagery");
check((html.match(/data-location-report(?:\s|>)/g) || []).length === 1, "Exactly one report root is required");
check((html.match(/data-primary-cta(?:\s|>)/g) || []).length === 1, "Exactly one primary CTA is required");
check((html.match(/data-location-map(?:\s|>)/g) || []).length === 1, "Exactly one map module root is required");

const dataScript = html.match(/<script type="application\/json" id="report-data">([\s\S]*?)<\/script>/);
check(Boolean(dataScript), "Embedded report payload is missing");
if (dataScript) {
  const embedded = JSON.parse(dataScript[1]);
  check(JSON.stringify(embedded) === JSON.stringify(payload), "Embedded report payload differs from source JSON");
}
for (const match of html.matchAll(/<script(?![^>]*application\/json)[^>]*>([\s\S]*?)<\/script>/g)) {
  try { new Function(match[1]); } catch (error) { failures.push("Inline JavaScript syntax error: " + error.message); }
}

const candidateRows = [...staticHtml.matchAll(/<tr data-candidate-id="([^"]+)" data-candidate-name="([^"]+)" data-rank="([^"]+)" data-score="([^"]+)" data-map-candidate-id="([^"]+)">/g)];
check(candidateRows.length === 10, "Static evidence table must contain ten candidate parity rows");
const rowIds = new Set(candidateRows.map((match) => match[1]));
const payloadIds = new Set(payload.candidates.map((candidate) => candidate.id));
check(sameSet(rowIds, payloadIds), "Static candidate rows differ from payload candidates");
check(candidateRows.every((match) => match[1] === match[5]), "Candidate and mapped candidate IDs differ");
check((staticHtml.match(/data-evidence-toggle(?:\s|>)/g) || []).length === 10, "Each candidate needs exactly one static evidence control");

const recommendationHook = html.match(/data-recommendation-candidate-ids="([^"]+)"/);
const ctaHook = html.match(/data-primary-cta[^>]*data-cta-candidate-ids="([^"]+)"/);
check(Boolean(recommendationHook), "Shortlist recommendation hook is missing");
check(Boolean(ctaHook), "Shortlist CTA hook is missing");
if (recommendationHook && ctaHook) {
  check(sameSet(ids(recommendationHook[1]), payloadIds), "Recommendation hook differs from the Top 10");
  check(sameSet(ids(ctaHook[1]), payloadIds), "CTA hook differs from the Top 10");
}
check(sameSet(new Set(payload.recommendation.candidate_ids), payloadIds), "Payload recommendation differs from the Top 10");
check(sameSet(new Set(payload.cta.candidate_ids), payloadIds), "Payload CTA differs from the Top 10");
check(sameSet(new Set(payload.decision_scope.candidate_ids), payloadIds), "Decision scope differs from the Top 10");

for (const source of payload.sources) {
  check(html.includes(`data-source-id="${source.id}"`), `Source hook is missing: ${source.id}`);
}
for (const caveat of payload.caveats) {
  check(html.includes(`data-caveat-id="${caveat.id}"`), `Caveat hook is missing: ${caveat.id}`);
}

check(sameSet(new Set(manifest.candidate_ids), payloadIds), "Map manifest candidate IDs differ from the payload");
const detailMaps = manifest.maps.filter((map) => map.role === "detail");
check(detailMaps.length === 10, "Map manifest must contain ten detail-map entries");
const competitorLayers = detailMaps.flatMap((map) => map.layers.filter((layer) => layer.kind === "competitor_marker"));
check(competitorLayers.length === 10, "Each detail map needs one competitor layer");
check(new Set(competitorLayers.map((layer) => layer.size_scale_id)).size === 1, "Competitor marker scales differ");
check(detailMaps.every((map) => map.context_fallback?.visible === true), "Every detail map needs a visible context fallback");
check(payload.candidates.every((candidate) =>
  candidate.competitor_ids.every((id) => payload.competitors.some((competitor) => competitor.id === id))
), "Candidate references an unknown competitor");

const reportHref = html.match(/href="([^"]+\.md)" download/);
check(Boolean(reportHref), "Report download link is missing");
if (reportHref) check(fs.existsSync(path.join(root, reportHref[1])), "Report download target does not exist");

if (failures.length) {
  for (const failure of failures) console.error("FAIL:", failure);
  process.exit(1);
}

console.log(JSON.stringify({
  status: "PASS",
  candidates: payload.candidates.length,
  competitors: payload.competitors.length,
  competitor_relations: payload.candidates.reduce((sum, candidate) => sum + candidate.competitor_ids.length, 0),
  html_sha256: sha(html),
  report_sha256: sha(report),
  payload_sha256: sha(fs.readFileSync(files.payload)),
  manifest_sha256: sha(fs.readFileSync(files.manifest))
}, null, 2));
