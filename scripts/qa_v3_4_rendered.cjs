#!/usr/bin/env node
"use strict";

const fs = require("fs");
const http = require("http");
const path = require("path");
const { chromium } = require("playwright");

const root = path.resolve(__dirname, "..");
const screenshots = path.join("/tmp", "parc-v3.4-qa");
fs.mkdirSync(screenshots, { recursive: true });

const types = {
  ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8", ".json": "application/json; charset=utf-8",
  ".png": "image/png", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".geojson": "application/geo+json"
};

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function serve() {
  return new Promise((resolve) => {
    const server = http.createServer((request, response) => {
      const pathname = decodeURIComponent(new URL(request.url, "http://localhost").pathname);
      const relative = pathname === "/" ? "index.html" : pathname.replace(/^\/+/, "");
      const file = path.resolve(root, relative);
      if (!file.startsWith(root + path.sep) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
        response.writeHead(404).end("Not found"); return;
      }
      response.setHeader("Content-Type", types[path.extname(file)] || "application/octet-stream");
      response.end(fs.readFileSync(file));
    });
    server.listen(0, "127.0.0.1", () => resolve(server));
  });
}

async function contrast(page, selector) {
  return page.$eval(selector, (node) => {
    const parse = (value) => value.match(/[\d.]+/g).slice(0, 3).map(Number);
    const luminance = (rgb) => {
      const linear = rgb.map((channel) => {
        const value = channel / 255;
        return value <= .04045 ? value / 12.92 : ((value + .055) / 1.055) ** 2.4;
      });
      return .2126 * linear[0] + .7152 * linear[1] + .0722 * linear[2];
    };
    const style = getComputedStyle(node);
    let backgroundNode = node;
    let background = style.backgroundColor;
    while (backgroundNode.parentElement && (!background.match(/[\d.]+/g) || Number(background.match(/[\d.]+/g)[3] || 1) === 0)) {
      backgroundNode = backgroundNode.parentElement;
      background = getComputedStyle(backgroundNode).backgroundColor;
    }
    const values = [luminance(parse(style.color)), luminance(parse(background))].sort((a, b) => b - a);
    return (values[0] + .05) / (values[1] + .05);
  });
}

(async () => {
  const server = await serve();
  const port = server.address().port;
  const executablePath = process.env.PARC_CHROMIUM_EXECUTABLE || chromium.executablePath();
  if (!fs.existsSync(executablePath)) throw new Error(`Chromium executable not found: ${executablePath}`);
  const browser = await chromium.launch({ headless: true, executablePath });
  const errors = [];
  try {
    const context = await browser.newContext({ viewport: { width: 1366, height: 900 }, colorScheme: "light" });
    const page = await context.newPage();
    page.on("pageerror", (error) => errors.push(error.message));
    await page.route(/^https?:\/\/(?!127\.0\.0\.1)/, (route) => route.abort());
    await page.goto(`http://127.0.0.1:${port}/`, { waitUntil: "load" });
    await page.waitForTimeout(300);

    assert(await page.locator("[data-decision-view]").count() === 5, "rendered decision view count is not five");
    assert(await page.locator('input[type="range"][data-weight]').count() === 4, "rendered slider count is not four");
    assert(await page.locator("[data-live-rank-body] tr").count() === 10, "live table does not contain ten candidates");
    assert((await page.locator("[data-live-rank-body] tr").first().innerText()).includes("A · ตลาดพลู-ใต้"), "base A-J leader is not A");
    assert(await page.locator('[data-benchmark-status="unscored"]').isVisible(), "benchmark gap is not visible");
    assert((await page.locator(".benchmark-row").innerText()).includes("—"), "PARC reference row implies a numeric score");

    await page.locator('.overview-visual-markers .candidate-dot').first().click({ force: true });
    await page.waitForTimeout(150);
    assert(new URL(page.url()).hash === "#detail-A", "overview marker A is still intercepted by overlapping marker G");
    assert(await page.locator("#detail-A").isVisible(), "overview marker A does not reveal detail A");
    await page.goto(`http://127.0.0.1:${port}/`, { waitUntil: "load" });

    const lightContrast = await contrast(page, ".decision-bar .button.primary");
    const lightPillContrast = await contrast(page, ".benchmark-gap .status-pill");
    const lightBenchmarkContrast = await contrast(page, ".benchmark-slot span");
    assert(lightContrast >= 4.5, `light CTA contrast ${lightContrast.toFixed(2)} is below 4.5`);
    assert(lightPillContrast >= 4.5, `light benchmark pill contrast ${lightPillContrast.toFixed(2)} is below 4.5`);
    assert(lightBenchmarkContrast >= 4.5, `light benchmark slot contrast ${lightBenchmarkContrast.toFixed(2)} is below 4.5`);
    await page.locator("[data-theme-toggle]").click();
    const darkContrast = await contrast(page, ".decision-bar .button.primary");
    const darkPillContrast = await contrast(page, ".benchmark-gap .status-pill");
    const darkBenchmarkContrast = await contrast(page, ".benchmark-slot span");
    assert(darkContrast >= 4.5, `dark CTA contrast ${darkContrast.toFixed(2)} is below 4.5`);
    assert(darkPillContrast >= 4.5, `dark benchmark pill contrast ${darkPillContrast.toFixed(2)} is below 4.5`);
    assert(darkBenchmarkContrast >= 4.5, `dark benchmark slot contrast ${darkBenchmarkContrast.toFixed(2)} is below 4.5`);
    await page.locator("[data-theme-toggle]").click();

    const presets = await page.locator('[data-scenario-select] option:not([value="custom"])').evaluateAll((options) => options.map((option) => option.value));
    for (const preset of presets) {
      await page.locator("[data-scenario-select]").selectOption(preset);
      const displayedTotal = await page.locator("[data-weight-share]").evaluateAll((nodes) => nodes.reduce((sum, node) => sum + Number(node.textContent.replace("%", "")), 0));
      assert(Math.abs(displayedTotal - 100) < .001, `${preset} displayed shares total ${displayedTotal}%`);
    }
    await page.locator("[data-reset-tool]").click();

    for (const key of ["resident", "routine", "access", "market"]) await page.locator(`[data-weight="${key}"]`).fill("0");
    const zeroShares = await page.locator("[data-weight-share]").allTextContents();
    assert(zeroShares.every((value) => value === "25.00%"), `all-zero fallback is not equal shares: ${zeroShares.join(", ")}`);
    assert((await page.locator("[data-weight-total]").innerText()).includes("ทุกค่าเป็นศูนย์"), "all-zero fallback is not explained");

    await page.locator('[data-weight="resident"]').fill("0");
    await page.locator('[data-weight="access"]').fill("0");
    await page.locator('[data-weight="market"]').fill("0");
    await page.locator('[data-weight="routine"]').fill("100");
    assert((await page.locator("[data-live-rank-body] tr").first().innerText()).includes("B · วังหิน-ใต้"), "routine-only slider does not move B to first");
    assert(await page.locator("[data-scenario-select]").inputValue() === "custom", "slider move does not mark the model custom");

    await page.locator('[data-market-mode][value="observed"]').check();
    await page.locator('[data-weight="routine"]').fill("0");
    await page.locator('[data-weight="market"]').fill("100");
    assert((await page.locator("[data-live-rank-body] tr").first().innerText()).includes("I · คลองจั่น"), "observed-supply mode does not move I to first");

    await page.locator("[data-reset-tool]").click();
    assert(await page.locator("[data-scenario-select]").inputValue() === "base", "reset does not restore base preset");
    await page.locator('[data-live-detail="B"]').click();
    await page.waitForTimeout(150);
    assert(new URL(page.url()).hash === "#detail-B", "detail link does not create a working #detail-B URL");
    assert(await page.locator("#detail-B").isVisible(), "detail B panel is not visible after navigation");
    const bAnchorPosition = await page.evaluate(() => ({
      header: document.querySelector(".site-header").getBoundingClientRect().bottom,
      title: document.querySelector("#detail-B h3").getBoundingClientRect().top
    }));
    assert(bAnchorPosition.title >= bAnchorPosition.header, "detail B title is hidden under the sticky header");

    await page.goto(`http://127.0.0.1:${port}/#detail-J`, { waitUntil: "load" });
    await page.waitForTimeout(250);
    assert(await page.locator("#detail-J").isVisible(), "direct #detail-J load does not reveal J");
    assert(!(await page.locator("#detail-A").isVisible()), "direct #detail-J load leaves A visible");
    const jAnchorPosition = await page.evaluate(() => ({
      header: document.querySelector(".site-header").getBoundingClientRect().bottom,
      title: document.querySelector("#detail-J h3").getBoundingClientRect().top
    }));
    assert(jAnchorPosition.title >= jAnchorPosition.header, "detail J title is hidden under the sticky header");

    const anchorAudit = await page.evaluate(() => {
      const ids = new Set([...document.querySelectorAll("[id]")].map((node) => node.id));
      return [...document.querySelectorAll('a[href^="#"]')].map((node) => node.getAttribute("href").slice(1)).filter((id) => !ids.has(id));
    });
    assert(anchorAudit.length === 0, `dead rendered anchors: ${anchorAudit.join(", ")}`);

    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto(`http://127.0.0.1:${port}/`, { waitUntil: "load" });
    const spacing = await page.evaluate(() => {
      const steps = document.querySelector(".decision-steps").getBoundingClientRect();
      const heading = document.querySelector("#lenses .section-head").getBoundingClientRect();
      return heading.top - steps.bottom;
    });
    assert(spacing < 130, `dead spacing below decision strip remains ${Math.round(spacing)}px`);

    await page.setViewportSize({ width: 1366, height: 768 });
    const shortViewportPosition = await page.locator(".tool-controls").evaluate((node) => getComputedStyle(node).position);
    assert(shortViewportPosition === "static", `short desktop controls remain ${shortViewportPosition}`);

    await page.setViewportSize({ width: 834, height: 1112 });
    await page.goto(`http://127.0.0.1:${port}/#lenses`, { waitUntil: "load" });
    const cardBoxes = await page.locator("[data-decision-view]").evaluateAll((nodes) => nodes.map((node) => {
      const box = node.getBoundingClientRect(); return { left: Math.round(box.left), width: Math.round(box.width) };
    }));
    assert(new Set(cardBoxes.map((box) => box.left)).size === 1, "834px decision cards leave empty half-rows");
    await page.screenshot({ path: path.join(screenshots, "desktop-top.png"), fullPage: false });
    await page.locator("#sensitivity").scrollIntoViewIfNeeded();
    await page.screenshot({ path: path.join(screenshots, "desktop-tool.png"), fullPage: false });

    for (const viewport of [{ width: 390, height: 844 }, { width: 320, height: 720 }]) {
      await page.setViewportSize(viewport);
      await page.goto(`http://127.0.0.1:${port}/#sensitivity`, { waitUntil: "load" });
      await page.waitForTimeout(200);
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      assert(overflow <= 1, `${viewport.width}px viewport overflows horizontally by ${overflow}px`);
      assert(await page.locator("[data-live-ranking]").isVisible(), `${viewport.width}px live ranking is not visible`);
      if (viewport.width === 390) {
        await page.locator('[data-live-detail="B"]').click();
        assert(await page.locator("#detail-B .back-to-tool").isVisible(), "mobile detail has no return-to-tool action");
        await page.locator("#detail-B .back-to-tool").click();
        assert(new URL(page.url()).hash === "#sensitivity", "mobile return action does not restore the tool URL");
        assert(await page.locator("[data-live-ranking]").isVisible(), "mobile return action does not restore the live tool");
      }
      await page.screenshot({ path: path.join(screenshots, `mobile-${viewport.width}.png`), fullPage: false });
    }

    assert(errors.length === 0, `page errors: ${errors.join(" | ")}`);
    console.log(`PASS — rendered 1920/1366×768/834/390/320 · CTA ${lightContrast.toFixed(2)}:1 light / ${darkContrast.toFixed(2)}:1 dark · spacing ${Math.round(spacing)}px`);
    console.log(`Screenshots: ${screenshots}`);
  } finally {
    await browser.close();
    await new Promise((resolve) => server.close(resolve));
  }
})().catch((error) => { console.error(`FAIL — ${error.stack || error}`); process.exit(1); });
