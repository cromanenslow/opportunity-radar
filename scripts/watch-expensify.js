#!/usr/bin/env node

/**
 * Expensify/App $250 Bounty Issue Watcher
 *
 * Searches GitHub for unassigned External $250 issues on Expensify/App.
 * Tracks seen issues in seen.json to only report new ones.
 *
 * Usage:
 *   node scripts/watch-expensify.js
 *
 * Env vars:
 *   GITHUB_TOKEN  - Optional, for higher API rate limits
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const SEEN_FILE = `${__dirname}/seen.json`;
const GITHUB_API = 'https://api.github.com';

const QUERY = 'repo:Expensify/App is:issue is:open label:External no:assignee $250';
// Note on the query: The '$250' is a label-search term; GitHub treats it as a
// literal string search across labels. We URL-encode properly below.

const SEARCH_URL = `${GITHUB_API}/search/issues?q=${encodeURIComponent(QUERY)}&sort=created&order=desc&per_page=100`;

const headers = {
  'Accept': 'application/vnd.github.v3+json',
  'User-Agent': 'opportunity-radar-watcher/1.0',
};

// Add auth if GITHUB_TOKEN is set
if (process.env.GITHUB_TOKEN) {
  headers['Authorization'] = `token ${process.env.GITHUB_TOKEN}`;
}

/**
 * Load the seen issues database from disk.
 */
function loadSeen() {
  try {
    if (existsSync(SEEN_FILE)) {
      const raw = readFileSync(SEEN_FILE, 'utf-8');
      return JSON.parse(raw);
    }
  } catch (err) {
    console.error(`[WARN] Could not load seen.json: ${err.message}`);
  }
  return { seen: {} };
}

/**
 * Save the seen issues database to disk.
 */
function saveSeen(data) {
  try {
    mkdirSync(dirname(SEEN_FILE), { recursive: true });
    writeFileSync(SEEN_FILE, JSON.stringify(data, null, 2), 'utf-8');
  } catch (err) {
    console.error(`[ERROR] Could not save seen.json: ${err.message}`);
  }
}

/**
 * Fetch issues from GitHub Search API, handling pagination.
 * Returns array of issue objects.
 */
async function fetchIssues(url) {
  const results = [];

  while (url) {
    let response;
    try {
      response = await fetch(url, { headers });
    } catch (err) {
      console.error(`[ERROR] Network error fetching ${url}: ${err.message}`);
      return results;
    }

    // Rate limit handling
    if (response.status === 403 || response.status === 429) {
      const resetEpoch = response.headers.get('x-ratelimit-reset');
      const remaining = response.headers.get('x-ratelimit-remaining');
      const resetTime = resetEpoch
        ? new Date(parseInt(resetEpoch) * 1000).toISOString()
        : 'unknown';
      console.error(`[WARN] Rate limited! (status ${response.status}, remaining: ${remaining}, resets at: ${resetTime})`);
      if (results.length > 0) {
        return results;
      }
      return results;
    }

    if (!response.ok) {
      console.error(`[ERROR] GitHub API error: ${response.status} ${response.statusText}`);
      const body = await response.text().catch(() => '(no body)');
      console.error(`[ERROR] Response body: ${body.substring(0, 500)}`);
      return results;
    }

    const data = await response.json();

    if (data.items) {
      results.push(...data.items);
    }

    // Check for next page via Link header
    const linkHeader = response.headers.get('link');
    url = null;
    if (linkHeader) {
      const links = parseLinkHeader(linkHeader);
      if (links.next) {
        url = links.next;
      }
    }
  }

  return results;
}

/**
 * Parse RFC 5988 Link header into an object of { rel: url }.
 */
function parseLinkHeader(header) {
  const links = {};
  if (!header) return links;

  const parts = header.split(',');
  for (const part of parts) {
    const match = part.match(/<([^>]+)>;\s*rel="([^"]+)"/);
    if (match) {
      links[match[2]] = match[1];
    }
  }
  return links;
}

async function main() {
  const seen = loadSeen();
  const issues = await fetchIssues(SEARCH_URL);

  const newIssues = [];
  const updatedSeen = { ...seen.seen };

  for (const issue of issues) {
    const number = issue.number;
    const title = issue.title;
    const url = issue.html_url;
    const createdAt = issue.created_at;

    // Record it in seen
    if (!updatedSeen[number]) {
      updatedSeen[number] = title;
    }

    // Check if it's new
    if (!seen.seen[number]) {
      newIssues.push({
        number,
        title,
        url,
        created_at: createdAt,
      });
    } else if (seen.seen[number] !== title) {
      // Title changed — still report as updated
      newIssues.push({
        number,
        title,
        url,
        created_at: createdAt,
        updated: true,
      });
    }
  }

  // Save updated seen list
  saveSeen({ seen: updatedSeen });

  // Build output
  const output = {
    timestamp: new Date().toISOString(),
    total_open: issues.length,
    new_count: newIssues.length,
    new_issues: newIssues,
    query: QUERY,
  };

  // Print JSON to stdout for machine parsing
  console.log(JSON.stringify(output, null, 2));

  // Exit with code 1 if new issues found (for CI/alerting), code 0 otherwise
  if (newIssues.length > 0) {
    process.exit(0); // Exit 0 — we just want to report, not fail
  }
}

main().catch((err) => {
  console.error(`[ERROR] Unhandled error: ${err.message}`);
  process.exit(1);
});
