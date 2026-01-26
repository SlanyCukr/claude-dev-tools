#!/usr/bin/env node
/**
 * Strategic Compact Suggester
 *
 * Suggests manual compaction at logical intervals to preserve context.
 * Outputs JSON to stdout with systemMessage to show suggestion while allowing tool call.
 */

const path = require('path');
const os = require('os');
const fs = require('fs');

function main() {
  const sessionId = process.env.CLAUDE_SESSION_ID || process.ppid || 'default';
  const counterFile = path.join(os.tmpdir(), `claude-tool-count-${sessionId}`);
  const threshold = parseInt(process.env.COMPACT_THRESHOLD || '50', 10);

  let count = 1;

  // Read existing count
  try {
    const existing = fs.readFileSync(counterFile, 'utf-8');
    count = parseInt(existing.trim(), 10) + 1;
  } catch (err) {
    if (err.code !== 'ENOENT') throw err;
  }

  // Save updated count
  fs.writeFileSync(counterFile, String(count));

  // Output system message at threshold points
  let message = null;

  if (count === threshold) {
    message = `📊 ${threshold} tool calls - consider /compact if transitioning between phases`;
  } else if (count > threshold && count % 25 === 0) {
    message = `📊 ${count} tool calls - good checkpoint for /compact if context feels stale`;
  }

  if (message) {
    // Output JSON to stdout with additionalContext so Claude sees it
    console.log(JSON.stringify({
      hookSpecificOutput: {
        additionalContext: message
      }
    }));
  }

  process.exit(0);
}

main();
