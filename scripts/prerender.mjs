/**
 * Prerender every index.html so crawlers that don't run JavaScript (Bing,
 * DuckDuckGo, social unfurlers, LLM search) can read the article text.
 *
 * Runs in CI only: loads each page in headless Chrome, waits for React to
 * finish, and bakes the rendered #root back into the file. React still takes
 * over on load for real visitors. Any page that fails is left as-is (CSR) so a
 * single bad render can never break the whole deploy.
 *
 * Requires a local server for the site root at http://localhost:8080.
 */
import { readFile, writeFile } from 'node:fs/promises';
import { glob } from 'glob';
import puppeteer from 'puppeteer';

const BASE = process.env.PRERENDER_BASE || 'http://localhost:8080';
const EMPTY_ROOT = '<div id="root"></div>';

// Whole thing is wrapped so a catastrophic failure (e.g. Chromium can't launch
// in CI) logs and exits 0 -> the deploy still proceeds with plain CSR, exactly
// as before. Prerendering is strictly additive and can never break the build.
let browser;
try {
  const files = await glob('**/index.html', {
    ignore: ['node_modules/**', '.git/**'],
  });

  browser = await puppeteer.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  let done = 0;
  let skipped = 0;

  for (const file of files.sort()) {
    const url = BASE + '/' + file.replace(/index\.html$/, '');
    try {
      const page = await browser.newPage();
      await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });
      // Wait until React (after Babel compiles + any /data fetches) fills #root.
      await page.waitForFunction(
        () => document.querySelector('#root')?.children.length > 0,
        { timeout: 30000 },
      );
      const rendered = await page.$eval('#root', (el) => el.innerHTML);
      await page.close();

      if (!rendered || !rendered.trim()) {
        console.warn('  skip (empty render):', url);
        skipped++;
        continue;
      }

      const html = await readFile(file, 'utf8');
      if (!html.includes(EMPTY_ROOT)) {
        console.warn('  skip (no empty #root):', url);
        skipped++;
        continue;
      }

      // Function replacer avoids $-sequences in rendered HTML (e.g. "$MFT",
      // "$STANDARD_INFORMATION") being treated as replacement patterns.
      const out = html.replace(
        EMPTY_ROOT,
        () => `<div id="root">${rendered}</div>`,
      );
      await writeFile(file, out);
      console.log('  ok:', url);
      done++;
    } catch (err) {
      // Leave this page as client-side rendered; do not fail the build.
      console.warn('  skip (left as CSR):', url, '-', err.message);
      skipped++;
    }
  }

  console.log(`\nPrerendered ${done} pages, skipped ${skipped}, of ${files.length} total.`);
} catch (err) {
  console.warn('Prerender aborted, deploying as-is (CSR):', err.message);
} finally {
  if (browser) await browser.close().catch(() => {});
}
