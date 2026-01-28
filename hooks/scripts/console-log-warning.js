#!/usr/bin/env node
/**
 * Console.log Warning Hook
 *
 * Runs on PostToolUse for Edit tool.
 * Warns if console.log statements were added.
 */

const fs = require('fs');

function main() {
  let input = '';

  try {
    input = fs.readFileSync(0, 'utf-8');
  } catch {
    process.exit(0);
  }

  // Only check JS/TS files
  let data;
  try {
    data = JSON.parse(input);
  } catch {
    process.exit(0);
  }

  const filePath = data?.tool_input?.file_path || '';
  if (!/\.(js|jsx|ts|tsx|mjs|cjs)$/.test(filePath)) {
    process.exit(0);
  }

  const newString = data?.tool_input?.new_string || '';
  if (newString.includes('console.log')) {
    const message = '⚠️ console.log detected - remember to remove before commit';
    console.log(JSON.stringify({
      systemMessage: message,
      hookSpecificOutput: {
        hookEventName: "PostToolUse",
        additionalContext: message
      }
    }));
  }

  process.exit(0);
}

main();
