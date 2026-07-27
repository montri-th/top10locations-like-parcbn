#!/usr/bin/env python3
"""Static release-contract QA for the Release 1.6 HTML.

This test deliberately checks rendered structure and public references without
searching reader-facing caveat prose for words such as "road" or "station".
Those words are allowed when the report explains why a layer is omitted; an
actual map feature or layer carrying that role is not.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

from lxml import html
from PIL import Image


RELEASE_ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = RELEASE_ROOT / "index.html"
ANALYSIS_DIR = RELEASE_ROOT / "analysis"

errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - reported as a release failure
        errors.append(f"cannot read JSON {path.relative_to(RELEASE_ROOT)}: {exc}")
        return {}


def class_xpath(class_name: str) -> str:
    return (
        "//*[contains(concat(' ', normalize-space(@class), ' '), "
        f"' {class_name} ')]"
    )


def class_nodes(root, class_name: str):
    return root.xpath(
        ".//*[contains(concat(' ', normalize-space(@class), ' '), "
        f"' {class_name} ')]"
    )


def exact_token_match(value: str, forbidden: set[str]) -> bool:
    tokens = {token for token in re.split(r"[-_\s]+", value.lower()) if token}
    return bool(tokens & forbidden)


def extract_js_function(source: str, function_name: str) -> str | None:
    """Extract one function declaration using balanced braces."""

    match = re.search(rf"\bfunction\s+{re.escape(function_name)}\s*\(", source)
    if not match:
        return None
    brace = source.find("{", match.end())
    if brace < 0:
        return None
    depth = 0
    quote: str | None = None
    escaped = False
    for index in range(brace, len(source)):
        char = source[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in {'"', "'", "`"}:
            quote = char
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return source[match.start() : index + 1]
    return None


try:
    source = HTML_PATH.read_text(encoding="utf-8")
    document = html.document_fromstring(source)
except Exception as exc:  # pragma: no cover - reported cleanly in CI
    print(f"FAIL: cannot parse {HTML_PATH}: {exc}", file=sys.stderr)
    raise SystemExit(1)

screening = load_json(ANALYSIS_DIR / "screening-results.json")
manifest = load_json(ANALYSIS_DIR / "map-manifest.json")
private_registry = load_json(ANALYSIS_DIR / "competitor-registry.json")

expected_candidates = {
    item["candidate_id"]: {
        "rank": str(item["rank"]),
        "score": str(item["overall_score"]),
    }
    for item in screening.get("candidates", [])
}
expected_candidate_ids = set(expected_candidates)

# Report/map structure -------------------------------------------------------

wrappers = document.xpath("//*[@data-location-map]")
check(len(wrappers) == 1, f"expected 1 data-location-map wrapper; found {len(wrappers)}")
if wrappers:
    wrapper = wrappers[0]
    check(wrapper.tag == "main", "data-location-map wrapper must be the main report root")
    manifest_ref = wrapper.get("data-map-manifest")
    check(manifest_ref == "analysis/map-manifest.json", "map wrapper has wrong manifest reference")
    if manifest_ref:
        check((RELEASE_ROOT / manifest_ref).is_file(), "referenced map manifest does not exist")

overviews = document.xpath("//figure[@data-map-role='overview']")
check(len(overviews) == 1, f"expected 1 overview map; found {len(overviews)}")

cards = document.xpath(class_xpath("candidate-card"))
check(len(cards) == 10, f"expected 10 candidate cards; found {len(cards)}")
card_by_id: dict[str, object] = {}
for card in cards:
    candidate_id = card.get("data-candidate-id", "")
    check(bool(candidate_id), "candidate card missing data-candidate-id")
    check(candidate_id not in card_by_id, f"duplicate candidate card: {candidate_id}")
    card_by_id[candidate_id] = card
    expected = expected_candidates.get(candidate_id)
    check(expected is not None, f"unknown candidate card: {candidate_id}")
    if expected:
        check(card.get("data-rank") == expected["rank"], f"{candidate_id}: data-rank mismatch")
        check(card.get("data-score") == expected["score"], f"{candidate_id}: data-score mismatch")
    check(
        card.get("id") == f"candidate-{candidate_id}",
        f"{candidate_id}: card id is not the stable candidate anchor",
    )

check(
    set(card_by_id) == expected_candidate_ids,
    "candidate-card IDs do not match the canonical screening output",
)

detail_maps = [
    node
    for node in document.xpath("//figure[@data-map-candidate-id]")
    if "clean-map" in (node.get("class") or "").split()
]
check(len(detail_maps) == 10, f"expected 10 detail maps; found {len(detail_maps)}")
detail_by_candidate: dict[str, object] = {}
for detail in detail_maps:
    candidate_id = detail.get("data-map-candidate-id", "")
    check(bool(candidate_id), "detail map missing data-map-candidate-id")
    check(candidate_id not in detail_by_candidate, f"duplicate detail map: {candidate_id}")
    detail_by_candidate[candidate_id] = detail
    ancestors = detail.xpath(
        "ancestor::article[contains(concat(' ', normalize-space(@class), ' '), "
        "' candidate-card ')][1]"
    )
    check(len(ancestors) == 1, f"{candidate_id}: detail map is not inside one candidate card")
    if ancestors:
        check(
            ancestors[0].get("data-candidate-id") == candidate_id,
            f"{candidate_id}: detail-map/card candidate mismatch",
        )
    check(len(detail.xpath("./svg")) == 1, f"{candidate_id}: detail map must contain one SVG")
    check(
        len(class_nodes(detail, "analysis-extent")) == 1,
        f"{candidate_id}: detail map missing analytical extent",
    )
    check(
        len(class_nodes(detail, "candidate-center")) == 1,
        f"{candidate_id}: detail map missing candidate center",
    )
    check(len(class_nodes(detail, "north")) == 1, f"{candidate_id}: detail map missing north mark")
    check(len(class_nodes(detail, "scale")) == 1, f"{candidate_id}: detail map missing scale bar")
    card = ancestors[0] if ancestors else None
    if card is not None:
        check(
            len(card.xpath(".//*[@data-map-fallback]")) == 1,
            f"{candidate_id}: expected one non-map fallback",
        )

check(
    set(detail_by_candidate) == expected_candidate_ids,
    "detail-map IDs do not match the canonical screening output",
)

if overviews:
    overview = overviews[0]
    overview_links = overview.xpath(
        ".//a[contains(concat(' ', normalize-space(@class), ' '), ' overview-candidate ')]"
    )
    overview_targets = {
        (link.get("href") or "").removeprefix("#candidate-") for link in overview_links
    }
    check(len(overview_links) == 10, f"overview must contain 10 candidate links; found {len(overview_links)}")
    check(
        overview_targets == expected_candidate_ids,
        "overview candidate links do not match the canonical candidates",
    )
    check(
        not class_nodes(overview, "competitor-marker"),
        "overview must not contain competitor markers",
    )

# Marker hooks and manifest parity ------------------------------------------

markers = document.xpath(class_xpath("competitor-marker"))
check(bool(markers), "no competitor markers found")
impact_classes = {"high", "medium_high", "medium"}
for marker in markers:
    competitor_id = marker.get("data-competitor-id", "")
    candidate_id = marker.get("data-map-candidate-id", "")
    impact_class = marker.get("data-impact-class", "")
    size_basis = marker.get("data-size-basis", "")
    check(bool(competitor_id), "competitor marker missing data-competitor-id")
    check(candidate_id in expected_candidate_ids, f"{competitor_id}: invalid data-map-candidate-id")
    check(impact_class in impact_classes, f"{competitor_id}: invalid data-impact-class")
    check(bool(size_basis.strip()), f"{competitor_id}: missing data-size-basis")
    ancestor_maps = marker.xpath(
        "ancestor::figure[contains(concat(' ', normalize-space(@class), ' '), "
        "' clean-map ')][1]"
    )
    check(len(ancestor_maps) == 1, f"{competitor_id}: marker is not inside one detail map")
    if ancestor_maps:
        check(
            ancestor_maps[0].get("data-map-candidate-id") == candidate_id,
            f"{competitor_id}: marker/map candidate mismatch",
        )
    target = (marker.get("href") or "").removeprefix("#")
    check(bool(target), f"{competitor_id}: marker missing detail target")
    if target:
        check(
            len(document.xpath(f"//*[@id={json.dumps(target)}]")) == 1,
            f"{competitor_id}: marker target is missing or duplicated",
        )
    hit_targets = class_nodes(marker, "marker-hit")
    check(len(hit_targets) == 1, f"{competitor_id}: marker must have one touch target")
    if hit_targets:
        try:
            radius = float(hit_targets[0].get("r", "0"))
        except ValueError:
            radius = 0
        check(radius >= 22, f"{competitor_id}: marker touch diameter is below 44 px")

manifest_maps = manifest.get("maps", [])
overview_manifest = [item for item in manifest_maps if item.get("role") == "overview"]
detail_manifest = [item for item in manifest_maps if item.get("role") == "detail"]
check(len(overview_manifest) == 1, "map manifest must contain one overview map")
check(len(detail_manifest) == 10, "map manifest must contain ten detail maps")

allowed_layer_kinds = {"candidate_marker", "standardized_catchment", "poi_sample"}
for map_item in manifest_maps:
    for layer in map_item.get("layers", []):
        check(
            layer.get("kind") in allowed_layer_kinds,
            f"{map_item.get('id')}: prohibited/unknown map layer {layer.get('kind')}",
        )
for map_item in detail_manifest:
    site_ids = map_item.get("site_ids", [])
    check(len(site_ids) == 1, f"{map_item.get('id')}: detail map must have one site_id")
    omitted = map_item.get("omitted_context", {})
    for key in ("roads", "rail", "stations"):
        check(
            omitted.get(key) == "omitted_unverified",
            f"{map_item.get('id')}: {key} must remain omitted_unverified",
        )
    if site_ids:
        candidate_id = site_ids[0]
        expected_marker_count = sum(
            len(layer.get("geometry_ids", []))
            for layer in map_item.get("layers", [])
            if layer.get("kind") == "poi_sample" and layer.get("visible") is not False
        )
        actual_marker_count = sum(
            1 for marker in markers if marker.get("data-map-candidate-id") == candidate_id
        )
        check(
            actual_marker_count == expected_marker_count,
            f"{candidate_id}: HTML marker count {actual_marker_count} != manifest {expected_marker_count}",
        )

expected_total_markers = sum(
    len(layer.get("geometry_ids", []))
    for map_item in detail_manifest
    for layer in map_item.get("layers", [])
    if layer.get("kind") == "poi_sample" and layer.get("visible") is not False
)
check(
    len(markers) == expected_total_markers,
    f"total HTML markers {len(markers)} != manifest {expected_total_markers}",
)

# No rendered road/rail/station layers --------------------------------------

forbidden_map_tokens = {"road", "roads", "rail", "rails", "railway", "station", "stations"}
all_map_figures = overviews + detail_maps
for figure in all_map_figures:
    check(not figure.xpath(".//image|.//foreignObject|.//iframe"), "map contains an embedded external layer")
    for element in figure.xpath(".//svg//*"):
        for attribute in (
            "class",
            "id",
            "data-layer",
            "data-kind",
            "data-feature",
            "data-feature-type",
        ):
            value = element.get(attribute, "")
            check(
                not exact_token_match(value, forbidden_map_tokens),
                f"rendered map feature uses prohibited {attribute}={value!r}",
            )

style_text = "\n".join(document.xpath("//style/text()"))
for css_class in re.findall(r"\.([A-Za-z_][\w-]*)", style_text):
    check(
        not exact_token_match(css_class, forbidden_map_tokens),
        f"stylesheet defines prohibited map-feature class .{css_class}",
    )

# Public image/file hygiene --------------------------------------------------

lower_source = source.lower()
check("base64" not in lower_source, "HTML must not contain base64 content")
check("data:image" not in lower_source, "HTML must not embed image data URIs")

reference_patterns = (
    "project_sources/",
    "img_2284",
    "img_2280",
    "img_2282",
    "img_2279",
    "img_2283",
)
for pattern in reference_patterns:
    check(pattern not in lower_source, f"HTML references excluded source image/path: {pattern}")

for image_ref in document.xpath("//img/@src"):
    parsed = urlparse(image_ref)
    check(not parsed.scheme and not parsed.netloc, f"image must be a local external asset: {image_ref}")
    check(Path(parsed.path).suffix.lower() == ".png", f"non-PNG image reference: {image_ref}")
    check(".." not in Path(parsed.path).parts, f"image escapes release root: {image_ref}")

logo_nodes = document.xpath("//*[@id='brand-logo']")
check(len(logo_nodes) == 1, f"expected one brand logo; found {len(logo_nodes)}")
if logo_nodes:
    logo = logo_nodes[0]
    logo_refs = {
        "src": logo.get("src", ""),
        "positive": logo.get("data-logo-positive", ""),
        "reverse": logo.get("data-logo-reverse", ""),
    }
    check(logo_refs["src"] == logo_refs["positive"], "default logo must use the positive asset")
    opened_images: dict[str, Image.Image] = {}
    alpha_bytes: dict[str, bytes] = {}
    for label, reference in logo_refs.items():
        parsed = urlparse(reference)
        check(not parsed.scheme and not parsed.netloc, f"{label} logo must be an external local PNG")
        check(Path(parsed.path).suffix.lower() == ".png", f"{label} logo is not PNG")
        check(".." not in Path(parsed.path).parts, f"{label} logo escapes release root")
        path = (RELEASE_ROOT / parsed.path).resolve()
        try:
            path.relative_to(RELEASE_ROOT.resolve())
        except ValueError:
            check(False, f"{label} logo resolves outside release root")
            continue
        check(path.is_file(), f"{label} logo file does not exist: {reference}")
        if not path.is_file():
            continue
        try:
            image = Image.open(path).convert("RGBA")
        except Exception as exc:
            check(False, f"{label} logo cannot be decoded: {exc}")
            continue
        alpha = image.getchannel("A")
        alpha_min, alpha_max = alpha.getextrema()
        check(alpha_min == 0 and alpha_max > 0, f"{label} logo lacks real alpha transparency")
        corners = (
            alpha.getpixel((0, 0)),
            alpha.getpixel((image.width - 1, 0)),
            alpha.getpixel((0, image.height - 1)),
            alpha.getpixel((image.width - 1, image.height - 1)),
        )
        check(all(value == 0 for value in corners), f"{label} logo corners are not transparent")
        opened_images[label] = image
        alpha_bytes[label] = alpha.tobytes()
    if "positive" in opened_images and "reverse" in opened_images:
        check(
            opened_images["positive"].size == opened_images["reverse"].size,
            "positive/reverse logo dimensions differ",
        )
        check(
            alpha_bytes["positive"] == alpha_bytes["reverse"],
            "positive/reverse logo alpha geometry differs",
        )

# Internal connector identifiers must not leak into the public HTML.
connector_patterns = {
    r"\blibfile_[a-z0-9]+\b": "Library file ID",
    r"\bfile_[0-9a-f]{12,}\b": "opaque file ID",
    r"\bmcp__[a-z0-9_]+\b": "MCP tool ID",
    r"\bconnector_id\b": "connector_id field",
    r"\bspreadsheet_id\b": "spreadsheet_id field",
    r"\bsheet_name\b": "sheet_name field",
    r"\bapp://": "app connector URI",
}
for pattern, label in connector_patterns.items():
    check(not re.search(pattern, source, flags=re.IGNORECASE), f"HTML leaks {label}")

private_values: set[str] = set()
coordinate_registry = private_registry.get("venue_coordinate_registry", {})
for key in ("spreadsheet_id", "sheet_name"):
    value = coordinate_registry.get(key)
    if isinstance(value, str) and value:
        private_values.add(value)
for competitor in private_registry.get("competitors", []):
    source_meta = competitor.get("location", {}).get("coordinate_source", {})
    for key in ("source_id", "spreadsheet_id", "sheet_name"):
        value = source_meta.get(key)
        if isinstance(value, str) and value:
            private_values.add(value)
for value in private_values:
    check(value not in source, f"HTML leaks private connector value: {value}")
check(
    "analysis/competitor-registry.json" not in source,
    "HTML references the private competitor registry instead of the public derivative",
)

# Theme-cycle state machine --------------------------------------------------

theme_buttons = document.xpath("//*[@id='theme-cycle']")
check(len(theme_buttons) == 1, "expected one theme-cycle button")
if theme_buttons:
    button = theme_buttons[0]
    check(button.tag == "button", "theme-cycle control must be a native button")
    check(button.get("data-theme-mode") == "system", "fresh theme state must be System")
    check(bool(button.get("aria-label")), "theme-cycle button needs an accessible name")

icons = document.xpath("//*[@data-mode-icon]")
icon_modes = [icon.get("data-mode-icon") for icon in icons]
check(icon_modes == ["system", "light", "dark"], "theme icons must be System, Light, Dark")
for icon in icons:
    mode = icon.get("data-mode-icon")
    if mode == "system":
        check(icon.get("hidden") is None, "System icon must be visible by default")
    else:
        check(icon.get("hidden") is not None, f"{mode} icon must be hidden by default")

theme_status = document.xpath("//*[@id='theme-status']")
check(
    len(theme_status) == 1
    and theme_status[0].get("role") == "status"
    and theme_status[0].get("aria-live") == "polite",
    "theme status must be a polite live region",
)
check(
    re.search(r"let\s+state\s*=\s*\{\s*mode\s*:\s*[\"']system[\"']\s*,\s*step\s*:\s*0\s*\}", source)
    is not None,
    "theme boot state is not fresh System",
)
check(
    'matchMedia("(prefers-color-scheme: dark)")' in source,
    "theme cycle does not read the device color preference",
)
check(
    "parc-theme-cycle-v1" in source and "JSON.stringify(state)" in source,
    "theme cycle does not persist explicit state and phase",
)
check(
    "if (state.mode === \"system\") render(true)" in source
    and 'addEventListener("change", onSystemChange)' in source,
    "System mode does not follow later device-theme changes",
)

theme_function = extract_js_function(source, "nextThemeState")
check(theme_function is not None, "cannot extract nextThemeState from final HTML")
if theme_function:
    node_test = f"""
{theme_function}
function run(osDark) {{
  let state = {{mode:"system", step:0}};
  const sequence = [state.mode];
  for (let index = 0; index < 3; index++) {{
    state = nextThemeState(state, osDark);
    sequence.push(state.mode);
  }}
  return sequence;
}}
process.stdout.write(JSON.stringify({{light:run(false), dark:run(true)}}));
"""
    try:
        result = subprocess.run(
            ["node", "-e", node_test],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        cycles = json.loads(result.stdout)
        check(
            cycles.get("light") == ["system", "dark", "light", "system"],
            f"OS-light theme cycle is wrong: {cycles.get('light')}",
        )
        check(
            cycles.get("dark") == ["system", "light", "dark", "system"],
            f"OS-dark theme cycle is wrong: {cycles.get('dark')}",
        )
    except Exception as exc:
        check(False, f"cannot statically execute nextThemeState: {exc}")

# General HTML integrity -----------------------------------------------------

element_ids = document.xpath("//*[@id]/@id")
check(len(element_ids) == len(set(element_ids)), "HTML contains duplicate element IDs")
for placeholder in ("TODO", "TBD", "lorem ipsum", "REPLACE_", "{{"):
    check(placeholder not in source, f"HTML contains placeholder token {placeholder!r}")

if errors:
    print(f"FAIL: {len(errors)} static QA error(s)", file=sys.stderr)
    for item in errors:
        print(f"- {item}", file=sys.stderr)
    raise SystemExit(1)

print(
    "PASS:",
    json.dumps(
        {
            "location_map_wrappers": len(wrappers),
            "overview_maps": len(overviews),
            "detail_maps": len(detail_maps),
            "candidate_cards": len(cards),
            "competitor_markers": len(markers),
            "logo_alpha": "positive+reverse external PNG",
            "forbidden_map_layers": 0,
            "internal_connector_ids": 0,
            "theme_cycles": {
                "os_light": ["system", "dark", "light", "system"],
                "os_dark": ["system", "light", "dark", "system"],
            },
        },
        ensure_ascii=False,
    ),
)
