#!/usr/bin/env node
/**
 * Console.log Warning Hook
 *
 * Runs on PostToolUse for Edit tool on JS/TS files.
 * Warns if console.log statements were added.
 */

const fs = require('fs');

async function main() {
  // Read tool input from stdin (Claude Code passes context via stdin)
  let input = '';

  try {
    input = fs.readFileSync(0, 'utf-8');
  } catch {
    // No stdin available
    process.exit(0);
  }

  // Check if the edit added console.log
  if (input.includes('console.log')) {
    console.error('[ConsoleLogWarning] WARNING: console.log detected in edit');
    console.error('[ConsoleLogWarning] Consider removing before commit or use proper logging');
  }

  process.exit(0);
}

main().catch(err => {
  console.error('[ConsoleLogWarning] Error:', err.message);
  process.exit(0);
});
