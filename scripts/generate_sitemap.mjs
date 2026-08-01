#!/usr/bin/env node
/**
 * Regenerates sitemap.xml from the pages actually on disk.
 *
 * Every page on this site is an index.html inside its own directory, so the
 * sitemap is fully derivable — there is no list to keep in sync by hand. It
 * used to be maintained manually, which is how /research/action1-forensics-windows
 * ended up published but unindexed.
 *
 * Run it directly (`node scripts/generate_sitemap.mjs`) after adding a page, or
 * let the Pages workflow run it before deploying. Writes only when the content
 * changes, and exits non-zero on --check if the committed file is stale.
 *
 * Usage:
 *   node scripts/generate_sitemap.mjs           # rewrite sitemap.xml
 *   node scripts/generate_sitemap.mjs --check   # verify only, no write
 */

import { readdirSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join, dirname, relative, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
const ORIGIN = 'https://chicken0248.fyi';
const OUT = join(ROOT, 'sitemap.xml');

// Directories that hold source, tooling or assets rather than pages.
const SKIP_DIRS = new Set([
  '.git', '.github', '.claude', 'node_modules', 'assets', 'scripts', 'themes', 'data',
]);

// Section hubs rank above their detail pages. Anything unlisted is a detail page.
const PRIORITY = { '/': '1.0', '/reviews/': '0.9', '/research/': '0.9', '/ir-reports/': '0.9', '/siem-labs/': '0.8', '/cloud-labs/': '0.8' };
const DETAIL_PRIORITY = '0.7';

function findPages(dir = ROOT, found = []) {
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      if (SKIP_DIRS.has(entry.name) || entry.name.startsWith('.')) continue;
      findPages(join(dir, entry.name), found);
    } else if (entry.name === 'index.html') {
      // Root .html files other than index.html are internal (architecture.html)
      // and deliberately stay out of the sitemap.
      const rel = relative(ROOT, dir).split(sep).filter(Boolean).join('/');
      found.push(rel ? `/${rel}/` : '/');
    }
  }
  return found;
}

const paths = findPages().sort((a, b) => {
  const pa = PRIORITY[a] ?? DETAIL_PRIORITY;
  const pb = PRIORITY[b] ?? DETAIL_PRIORITY;
  if (pa !== pb) return Number(pb) - Number(pa);   // hubs before detail pages
  return a.localeCompare(b);
});

const xml = [
  '<?xml version="1.0" encoding="UTF-8"?>',
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
  ...paths.map(p => `  <url><loc>${ORIGIN}${p}</loc><priority>${PRIORITY[p] ?? DETAIL_PRIORITY}</priority></url>`),
  '</urlset>',
  '',
].join('\n');

const current = existsSync(OUT) ? readFileSync(OUT, 'utf8') : '';

if (process.argv.includes('--check')) {
  if (current === xml) {
    console.log(`sitemap.xml is up to date (${paths.length} pages)`);
  } else {
    console.error('sitemap.xml is stale — run: node scripts/generate_sitemap.mjs');
    process.exit(1);
  }
} else if (current === xml) {
  console.log(`sitemap.xml unchanged (${paths.length} pages)`);
} else {
  writeFileSync(OUT, xml);
  console.log(`sitemap.xml written (${paths.length} pages)`);
}
