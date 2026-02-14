#!/usr/bin/env node

/**
 * session-memory-loader.js - SessionStart hook
 * Instruct Claude to load memories on session start.
 */

const fs = require('fs');

function main() {
  // No need to read stdin for SessionStart
  console.log(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: 'SessionStart',
      additionalContext: 'IMPORTANT: Before doing anything else, call list_recent_memories_tool(hours_back=48) to load context from previous sessions. Review the memories and use them to inform your work.'
    }
  }));

  process.exit(0);
}

main();
