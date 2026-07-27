#!/usr/bin/env node

const fs = require("fs");
const http = require("http");
const path = require("path");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..");
const QA_DIR = path.join(ROOT, "qa");
const EXECUTABLE = process.env.PARC_CHROMIUM_EXECUTABLE;
const EXTERNAL_BASE_URL = process.env.PARC_QA_BASE_URL;
const PROXY_SERVER = process.env.HTTPS_PROXY || process.env.https_proxy;
const VIEWPORTS = [320, 375, 768, 1024, 1440];
const SCREENSHOT_ROOT = process.env.PARC_QA_SCREENSHOT_DIR || "/tmp";

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function contrastRatio(foreground, background) {
  const luminance = (hex) => {
    const value = hex.replace("#", "");
    const channels = [0, 2, 4].map((offset) => parseInt(value.slice(offset, offset + 2), 16) / 255)
      .map((channel) => channel <= 0.04045
        ? channel / 12.92
        : ((channel + 0.055) / 1.055) ** 2.4);
    return (0.2126 * channels[0]) + (0.7152 * channels[1]) + (0.0722 * channels[2]);
  };
  const values = [luminance(foreground), luminance(background)].sort((a, b) => b - a);
  return (values[0] + 0.05) / (values[1] + 0.05);
}

function mimeType(filePath) {
  const extension = path.extname(filePath).toLowerCase();
  return {
    ".html": "text/html; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".md": "text/markdown; charset=utf-8",
    ".png": "image/png",
    ".woff2": "font/woff2",
    ".txt": "text/plain; charset=utf-8",
  }[extension] || "application/octet-stream";
}

function startServer() {
  const server = http.createServer((request, response) => {
    const requestPath = decodeURIComponent((request.url || "/").split("?")[0]);
    const relativePath = requestPath === "/" ? "index.html" : requestPath.replace(/^\/+/, "");
    const filePath = path.resolve(ROOT, relativePath);
    if (!(filePath === ROOT || filePath.startsWith(`${ROOT}${path.sep}`))) {
      response.writeHead(403).end("Forbidden");
      return;
    }
    fs.readFile(filePath, (error, data) => {
      if (error) {
        response.writeHead(error.code === "ENOENT" ? 404 : 500).end("Not found");
        return;
      }
      response.writeHead(200, {
        "Content-Type": mimeType(filePath),
        "Cache-Control": "no-store",
      });
      response.end(data);
    });
  });
  return new Promise((resolve) => {
    server.listen(0, "127.0.0.1", () => {
      const address = server.address();
      resolve({
        server,
        baseURL: `http://127.0.0.1:${address.port}/`,
      });
    });
  });
}

function attachDiagnostics(page) {
  const diagnostics = [];
  page.on("console", (message) => {
    if (message.type() === "error") diagnostics.push(`console: ${message.text()}`);
  });
  page.on("pageerror", (error) => diagnostics.push(`pageerror: ${error.message}`));
  page.on("requestfailed", (request) => {
    const errorText = request.failure()?.errorText || "unknown";
    if (errorText === "net::ERR_ABORTED") return;
    diagnostics.push(`requestfailed: ${request.url()} · ${errorText}`);
  });
  page.on("response", (response) => {
    if (response.status() >= 400) {
      diagnostics.push(`http ${response.status()}: ${response.url()}`);
    }
  });
  return diagnostics;
}

async function openPage(browser, baseURL, options = {}) {
  const context = await browser.newContext({
    viewport: options.viewport || { width: 1440, height: 900 },
    colorScheme: options.colorScheme || "light",
    reducedMotion: options.reducedMotion || "no-preference",
    javaScriptEnabled: options.javaScriptEnabled !== false,
    ignoreHTTPSErrors: Boolean(EXTERNAL_BASE_URL),
  });
  const page = await context.newPage();
  const diagnostics = attachDiagnostics(page);
  await page.goto(baseURL, {
    waitUntil: EXTERNAL_BASE_URL ? "domcontentloaded" : "networkidle",
    timeout: EXTERNAL_BASE_URL ? 60000 : 30000,
  });
  if (options.javaScriptEnabled !== false) {
    await page.evaluate(() => document.fonts.ready);
  }
  return { context, page, diagnostics };
}

async function structuralChecks(page, viewportWidth) {
  const result = await page.evaluate(() => {
    const visible = (element) => {
      const style = getComputedStyle(element);
      return style.display !== "none" && style.visibility !== "hidden";
    };
    const targetSelectors = [
      "#theme-cycle",
      ".filter-bar button",
      ".evidence-disclosure > summary",
    ];
    const targetFailures = [];
    for (const selector of targetSelectors) {
      for (const element of document.querySelectorAll(selector)) {
        if (!visible(element)) continue;
        const rect = element.getBoundingClientRect();
        if (rect.width < 44 || rect.height < 44) {
          targetFailures.push(`${selector}:${rect.width.toFixed(1)}x${rect.height.toFixed(1)}`);
        }
      }
    }
    const markerFailures = [...document.querySelectorAll(".competitor-marker .marker-hit")]
      .filter((circle) => Number(circle.getAttribute("r")) * 2 < 44).length;
    return {
      reportRoots: document.querySelectorAll("[data-location-report]").length,
      candidateCards: document.querySelectorAll(".candidate-card[data-candidate-id]").length,
      overviewMaps: document.querySelectorAll('[data-map-role="overview"]').length,
      detailMaps: document.querySelectorAll('[data-map-role="detail"]').length,
      competitorMarkers: document.querySelectorAll(".competitor-marker").length,
      mapFallbacks: document.querySelectorAll("[data-map-fallback]").length,
      heldDetails: document.querySelectorAll(".competitor-detail.withheld").length,
      overflow: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) -
        document.documentElement.clientWidth,
      targetFailures,
      markerFailures,
      bodyFontSize: getComputedStyle(document.body).fontSize,
      bodyFontFamily: getComputedStyle(document.body).fontFamily,
      filterFontFamily: getComputedStyle(document.querySelector(".filter-bar button")).fontFamily,
      headingFontFamily: getComputedStyle(document.querySelector("h1")).fontFamily,
      headingTracking: getComputedStyle(document.querySelector("h1")).letterSpacing,
      headerBackground: getComputedStyle(document.querySelector(".site-header")).backgroundColor,
      headerBackdrop: getComputedStyle(document.querySelector(".site-header")).backdropFilter,
      fonts: {
        anuphan: document.fonts.check('300 48px "Anuphan"', "ภาษาไทย PARC Bangna"),
        plex400: document.fonts.check('400 18px "IBM Plex Sans Thai Looped"', "การวิเคราะห์ทำเล"),
        plex500: document.fonts.check('500 16px "IBM Plex Sans Thai Looped"', "เปิดหลักฐาน"),
      },
      logoLoaded: document.querySelector("#brand-logo").complete &&
        document.querySelector("#brand-logo").naturalWidth > 0,
      mapAlternatives: [...document.querySelectorAll('[data-map-role="detail"]')].every((figure) => {
        const svg = figure.querySelector('svg[role="img"][aria-labelledby]');
        const id = figure.dataset.mapCandidateId;
        return Boolean(svg && document.getElementById(`${id}-competitor-table`));
      }),
      numberedMarkers: [...document.querySelectorAll(".competitor-marker")].every((marker) =>
        Boolean(marker.querySelector("text")?.textContent.trim())
      ),
    };
  });

  assert(result.reportRoots === 1, `${viewportWidth}px: report root mismatch`);
  assert(result.candidateCards === 10, `${viewportWidth}px: candidate card mismatch`);
  assert(result.overviewMaps === 1, `${viewportWidth}px: overview map mismatch`);
  assert(result.detailMaps === 10, `${viewportWidth}px: detail map mismatch`);
  assert(result.competitorMarkers === 45, `${viewportWidth}px: competitor marker mismatch`);
  assert(result.mapFallbacks === 10, `${viewportWidth}px: fallback mismatch`);
  assert(result.heldDetails === 2, `${viewportWidth}px: held-detail mismatch`);
  assert(result.overflow <= 1, `${viewportWidth}px: horizontal overflow ${result.overflow}px`);
  assert(result.targetFailures.length === 0, `${viewportWidth}px: undersized targets ${result.targetFailures.join(", ")}`);
  assert(result.markerFailures === 0, `${viewportWidth}px: marker hit target below 44px`);
  assert(result.bodyFontSize === "18px", `${viewportWidth}px: body font is ${result.bodyFontSize}`);
  assert(result.bodyFontFamily.includes("IBM Plex Sans Thai Looped"), `${viewportWidth}px: wrong body font`);
  assert(result.filterFontFamily.includes("IBM Plex Sans Thai Looped"), `${viewportWidth}px: wrong filter font`);
  assert(result.headingFontFamily.includes("Anuphan"), `${viewportWidth}px: wrong heading font`);
  assert(result.headingTracking === "normal" || result.headingTracking === "0px", `${viewportWidth}px: Thai heading tracking ${result.headingTracking}`);
  assert(result.headerBackground !== "rgba(0, 0, 0, 0)", `${viewportWidth}px: header is transparent`);
  assert(result.headerBackdrop === "none", `${viewportWidth}px: header uses backdrop filter`);
  assert(result.fonts.anuphan && result.fonts.plex400 && result.fonts.plex500, `${viewportWidth}px: required fonts not loaded`);
  assert(result.logoLoaded, `${viewportWidth}px: logo did not load`);
  assert(result.mapAlternatives, `${viewportWidth}px: missing map summary/fallback`);
  assert(result.numberedMarkers, `${viewportWidth}px: marker lacks non-colour label`);
  return result;
}

async function themeCycleChecks(browser, baseURL, osScheme) {
  const { context, page, diagnostics } = await openPage(browser, baseURL, {
    viewport: { width: 1024, height: 768 },
    colorScheme: osScheme,
  });
  const expected = osScheme === "dark"
    ? [["system", "dark"], ["light", "light"], ["dark", "dark"], ["system", "dark"]]
    : [["system", "light"], ["dark", "dark"], ["light", "light"], ["system", "light"]];
  const actual = [];
  for (let index = 0; index < expected.length; index += 1) {
    actual.push(await page.evaluate(() => {
      const button = document.querySelector("#theme-cycle");
      const visibleIcon = button.querySelector("[data-mode-icon]:not([hidden])")?.dataset.modeIcon;
      const logo = document.querySelector("#brand-logo").getAttribute("src");
      return {
        mode: button.dataset.themeMode,
        resolved: button.dataset.resolvedTheme,
        visibleIcon,
        logo,
        dataTheme: document.documentElement.dataset.theme || null,
        label: button.getAttribute("aria-label"),
        tokens: {
          canvas: getComputedStyle(document.documentElement).getPropertyValue("--canvas").trim(),
          ink: getComputedStyle(document.documentElement).getPropertyValue("--ink").trim(),
          muted: getComputedStyle(document.documentElement).getPropertyValue("--muted").trim(),
          garden: getComputedStyle(document.documentElement).getPropertyValue("--garden").trim(),
          focus: getComputedStyle(document.documentElement).getPropertyValue("--focus").trim(),
          actionBg: getComputedStyle(document.documentElement).getPropertyValue("--action-bg").trim(),
          actionInk: getComputedStyle(document.documentElement).getPropertyValue("--action-ink").trim(),
        },
      };
    }));
    if (index < expected.length - 1) await page.click("#theme-cycle");
  }
  expected.forEach(([mode, resolved], index) => {
    assert(actual[index].mode === mode, `${osScheme}: theme mode ${index} is ${actual[index].mode}`);
    assert(actual[index].resolved === resolved, `${osScheme}: resolved theme ${index} is ${actual[index].resolved}`);
    assert(actual[index].visibleIcon === mode, `${osScheme}: icon ${actual[index].visibleIcon} does not match ${mode}`);
    assert(actual[index].label.includes(mode === "system" ? "System" : mode === "light" ? "Light" : "Dark"), `${osScheme}: aria label mismatch`);
    assert(
      resolved === "dark" ? actual[index].logo.includes("reverse") : !actual[index].logo.includes("reverse"),
      `${osScheme}: logo contrast derivative mismatch`
    );
    const expectedTokens = resolved === "dark"
      ? { canvas: "#1B2522", ink: "#F7F1E6", muted: "#D8CDBE", garden: "#AFC6BC", focus: "#F19AC3" }
      : { canvas: "#F7F2E9", ink: "#24312F", muted: "#45514D", garden: "#365E55", focus: "#A94372" };
    Object.entries(expectedTokens).forEach(([key, value]) => {
      assert(actual[index].tokens[key].toUpperCase() === value, `${osScheme}: token ${key} mismatch`);
    });
    assert(contrastRatio(actual[index].tokens.ink, actual[index].tokens.canvas) >= 7, `${osScheme}: primary text contrast`);
    assert(contrastRatio(actual[index].tokens.muted, actual[index].tokens.canvas) >= 7, `${osScheme}: secondary text contrast`);
    assert(contrastRatio(actual[index].tokens.actionInk, actual[index].tokens.actionBg) >= 7, `${osScheme}: action contrast`);
    assert(contrastRatio(actual[index].tokens.garden, actual[index].tokens.canvas) >= 3, `${osScheme}: control boundary contrast`);
  });

  const changedScheme = osScheme === "dark" ? "light" : "dark";
  await page.emulateMedia({ colorScheme: changedScheme });
  await page.waitForFunction((scheme) => {
    return document.querySelector("#theme-cycle").dataset.resolvedTheme === scheme;
  }, changedScheme);
  const systemFollow = await page.evaluate(() => ({
    mode: document.querySelector("#theme-cycle").dataset.themeMode,
    resolved: document.querySelector("#theme-cycle").dataset.resolvedTheme,
  }));
  assert(systemFollow.mode === "system" && systemFollow.resolved === changedScheme, `${osScheme}: System did not follow OS change`);
  assert(diagnostics.length === 0, `${osScheme}: ${diagnostics.join(" | ")}`);
  await context.close();
  return actual.map(({ mode, resolved }) => ({ mode, resolved }));
}

async function interactionChecks(browser, baseURL) {
  const { context, page, diagnostics } = await openPage(browser, baseURL, {
    viewport: { width: 375, height: 812 },
    colorScheme: "light",
  });

  await page.click('[data-filter="opportunity"]');
  assert(await page.locator(".candidate-card:not([hidden])").count() === 3, "filter: expected 3 Tier A–B cards");
  assert((await page.locator(".filter-status").textContent()).includes("3 จาก 10"), "filter: aria-live status mismatch");
  await page.click('[data-filter="all"]');

  const marker = page.locator(".competitor-marker").first();
  const targetSelector = await marker.getAttribute("href");
  await marker.focus();
  await page.keyboard.press("Enter");
  assert(await page.locator(targetSelector).getAttribute("open") !== null, "marker: linked details did not open");
  assert(await page.evaluate(() => document.activeElement?.tagName === "SUMMARY"), "marker: focus did not move to summary");
  await page.keyboard.press("Escape");
  assert(await page.locator(targetSelector).getAttribute("open") === null, "marker: Escape did not close details");
  assert(await page.evaluate(() => document.activeElement?.classList.contains("competitor-marker")), "marker: focus did not return");

  const disclosure = page.locator(".evidence-disclosure").first();
  const disclosureSummary = disclosure.locator("summary");
  await disclosureSummary.focus();
  await page.keyboard.press("Enter");
  assert(await disclosure.getAttribute("open") !== null, "evidence disclosure: Enter did not toggle");

  await page.evaluate(() => scrollTo(0, 0));
  await page.screenshot({
    path: path.join(SCREENSHOT_ROOT, "parc-release16-mobile-375.png"),
    fullPage: false,
  });
  await page.locator(".candidate-card").first().scrollIntoViewIfNeeded();
  await page.locator(".candidate-card").first().screenshot({
    path: path.join(SCREENSHOT_ROOT, "parc-release16-candidate-mobile.png"),
  });

  assert(diagnostics.length === 0, `interaction diagnostics: ${diagnostics.join(" | ")}`);
  await context.close();
}

async function reducedMotionAndZoomChecks(browser, baseURL) {
  const reduced = await openPage(browser, baseURL, {
    viewport: { width: 1024, height: 768 },
    colorScheme: "light",
    reducedMotion: "reduce",
  });
  const reducedStyles = await reduced.page.evaluate(() => ({
    scroll: getComputedStyle(document.documentElement).scrollBehavior,
    transition: getComputedStyle(document.querySelector(".marker-shape")).transitionDuration,
  }));
  assert(reducedStyles.scroll === "auto", `reduced motion: scroll behavior is ${reducedStyles.scroll}`);
  assert(reducedStyles.transition === "0s", `reduced motion: transition is ${reducedStyles.transition}`);
  assert(reduced.diagnostics.length === 0, `reduced motion diagnostics: ${reduced.diagnostics.join(" | ")}`);
  await reduced.context.close();

  const zoomed = await openPage(browser, baseURL, {
    viewport: { width: 1440, height: 900 },
    colorScheme: "light",
  });
  const zoomResult = await zoomed.page.evaluate(() => {
    document.documentElement.style.fontSize = "200%";
    return new Promise((resolve) => requestAnimationFrame(() => resolve({
      overflow: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) -
        document.documentElement.clientWidth,
      clippedControls: [...document.querySelectorAll("button, summary")]
        .filter((element) => element.scrollWidth > element.clientWidth + 1).length,
    })));
  });
  assert(zoomResult.overflow <= 1, `200% text zoom: horizontal overflow ${zoomResult.overflow}px`);
  assert(zoomResult.clippedControls === 0, `200% text zoom: ${zoomResult.clippedControls} clipped controls`);
  assert(zoomed.diagnostics.length === 0, `zoom diagnostics: ${zoomed.diagnostics.join(" | ")}`);
  await zoomed.context.close();
}

async function printChecks(browser, baseURL) {
  const { context, page, diagnostics } = await openPage(browser, baseURL, {
    viewport: { width: 1024, height: 768 },
    colorScheme: "dark",
  });
  await page.evaluate(() => window.dispatchEvent(new Event("beforeprint")));
  const before = await page.evaluate(() => ({
    allDetailsOpen: [...document.querySelectorAll("details")].every((item) => item.open),
    logo: document.querySelector("#brand-logo").getAttribute("src"),
  }));
  assert(before.allDetailsOpen, "print: not all details opened");
  assert(!before.logo.includes("reverse"), "print: reverse logo would disappear on paper");
  await page.emulateMedia({ media: "print" });
  const headerDisplay = await page.locator(".site-header").evaluate((element) => getComputedStyle(element).display);
  assert(headerDisplay === "none", `print: header display is ${headerDisplay}`);
  const pdfPath = path.join(SCREENSHOT_ROOT, "parc-release16-print.pdf");
  await page.pdf({ path: pdfPath, format: "A4", printBackground: true });
  assert(fs.statSync(pdfPath).size > 10000, "print: PDF output is unexpectedly small");
  await page.evaluate(() => window.dispatchEvent(new Event("afterprint")));
  assert(diagnostics.length === 0, `print diagnostics: ${diagnostics.join(" | ")}`);
  await context.close();
}

async function noScriptChecks(browser, baseURL) {
  const { context, page, diagnostics } = await openPage(browser, baseURL, {
    viewport: { width: 320, height: 720 },
    colorScheme: "dark",
    javaScriptEnabled: false,
  });
  const result = await page.evaluate(() => ({
    candidates: document.querySelectorAll(".candidate-card").length,
    detailMaps: document.querySelectorAll('[data-map-role="detail"]').length,
    fallbacks: document.querySelectorAll("[data-map-fallback]").length,
    overflow: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) -
      document.documentElement.clientWidth,
  }));
  assert(result.candidates === 10 && result.detailMaps === 10 && result.fallbacks === 10, "no-JS: core report content missing");
  assert(result.overflow <= 1, `no-JS: horizontal overflow ${result.overflow}px`);
  assert(diagnostics.length === 0, `no-JS diagnostics: ${diagnostics.join(" | ")}`);
  await context.close();
}

async function manifestChecks(page) {
  const manifest = JSON.parse(fs.readFileSync(path.join(ROOT, "analysis", "map-manifest.json"), "utf8"));
  const tableIds = manifest.maps
    .filter((map) => map.role === "detail")
    .map((map) => map.accessibility.data_table_id);
  const missing = await page.evaluate((ids) => ids.filter((id) => !document.getElementById(id)), tableIds);
  assert(missing.length === 0, `manifest: missing fallback IDs ${missing.join(", ")}`);
  const interactions = manifest.geometries
    .filter((geometry) => geometry.vocabulary === "poi_sample")
    .map((geometry) => geometry.interaction?.trigger);
  assert(interactions.length === 45 && interactions.every((trigger) => trigger === "svg_link"), "manifest: marker interaction semantics mismatch");
}

async function main() {
  assert(EXECUTABLE && fs.existsSync(EXECUTABLE), "Set PARC_CHROMIUM_EXECUTABLE to a Chromium executable");
  fs.mkdirSync(QA_DIR, { recursive: true });
  let server = null;
  let baseURL = EXTERNAL_BASE_URL;
  if (!baseURL) {
    ({ server, baseURL } = await startServer());
  }
  const browser = await chromium.launch({
    executablePath: EXECUTABLE,
    headless: true,
    args: [
      "--no-sandbox",
      "--disable-dev-shm-usage",
      ...(EXTERNAL_BASE_URL && PROXY_SERVER ? [`--proxy-server=${PROXY_SERVER}`] : []),
    ],
  });
  const results = {
    status: "PASS",
    checked_at: new Date().toISOString(),
    target: EXTERNAL_BASE_URL ? "production" : "local",
    base_url: baseURL,
    chromium: await browser.version(),
    viewports: {},
    theme_cycles: {},
    checks: [
      "source-to-render structure",
      "responsive overflow and 44px targets",
      "bundled fonts and opaque header",
      "single-button theme cycle and OS-follow",
      "transparent logo derivative switching",
      "filter, marker, focus, Escape, and disclosure interaction",
      "screen-reader map summaries and table fallbacks",
      "non-colour marker labels",
      "reduced motion and 200% text zoom",
      "print expansion and positive logo",
      "no-JavaScript core reading",
    ],
  };

  try {
    for (const width of VIEWPORTS) {
      const { context, page, diagnostics } = await openPage(browser, baseURL, {
        viewport: { width, height: width <= 375 ? 812 : 900 },
        colorScheme: "light",
      });
      results.viewports[width] = await structuralChecks(page, width);
      if (width === 1440) {
        await manifestChecks(page);
        await page.screenshot({
          path: path.join(SCREENSHOT_ROOT, "parc-release16-desktop-light.png"),
          fullPage: false,
        });
      }
      assert(diagnostics.length === 0, `${width}px diagnostics: ${diagnostics.join(" | ")}`);
      await context.close();
    }

    results.theme_cycles.os_light = await themeCycleChecks(browser, baseURL, "light");
    results.theme_cycles.os_dark = await themeCycleChecks(browser, baseURL, "dark");
    await interactionChecks(browser, baseURL);
    await reducedMotionAndZoomChecks(browser, baseURL);
    await printChecks(browser, baseURL);
    await noScriptChecks(browser, baseURL);

    const dark = await openPage(browser, baseURL, {
      viewport: { width: 1440, height: 900 },
      colorScheme: "dark",
    });
    await dark.page.screenshot({
      path: path.join(SCREENSHOT_ROOT, "parc-release16-desktop-dark.png"),
      fullPage: false,
    });
    assert(dark.diagnostics.length === 0, `dark diagnostics: ${dark.diagnostics.join(" | ")}`);
    await dark.context.close();

    fs.writeFileSync(
      path.join(QA_DIR, "rendered-qa-results.json"),
      `${JSON.stringify(results, null, 2)}\n`,
      "utf8"
    );
    console.log(`PASS: ${JSON.stringify({
      chromium: results.chromium,
      viewports: VIEWPORTS,
      markers: 45,
      theme_cycles: {
        os_light: results.theme_cycles.os_light.map((item) => item.mode),
        os_dark: results.theme_cycles.os_dark.map((item) => item.mode),
      },
    })}`);
  } finally {
    await browser.close();
    if (server) await new Promise((resolve) => server.close(resolve));
  }
}

main().catch((error) => {
  fs.mkdirSync(QA_DIR, { recursive: true });
  fs.writeFileSync(
    path.join(QA_DIR, "rendered-qa-results.json"),
    `${JSON.stringify({
      status: "FAIL",
      checked_at: new Date().toISOString(),
      error: error.message,
    }, null, 2)}\n`,
    "utf8"
  );
  console.error(`FAIL: ${error.stack || error.message}`);
  process.exit(1);
});
