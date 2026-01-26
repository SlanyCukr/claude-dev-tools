#!/usr/bin/env node
/**
 * SessionEnd Hook - Persist session state when session ends
 *
 * Creates/updates session log file with timestamp for continuity tracking.
 * Stdout is shown in verbose mode for SessionEnd.
 */

const path = require('path');
const fs = require('fs');
const {
  getSessionsDir,
  getDateString,
  getTimeString,
  ensureDir,
  writeFile,
  replaceInFile
} = require('../lib/utils');

function main() {
  const sessionsDir = getSessionsDir();
  const today = getDateString();
  const sessionFile = path.join(sessionsDir, `${today}-session.tmp`);

  ensureDir(sessionsDir);

  const currentTime = getTimeString();

  if (fs.existsSync(sessionFile)) {
    replaceInFile(
      sessionFile,
      /\*\*Last Updated:\*\*.*/,
      `**Last Updated:** ${currentTime}`
    );
    console.log(`[SessionEnd] Updated: ${sessionFile}`);
  } else {
    const template = `# Session: ${today}
**Date:** ${today}
**Started:** ${currentTime}
**Last Updated:** ${currentTime}

---

## Current State

[Session context goes here]

### Completed
- [ ]

### In Progress
- [ ]

### Notes for Next Session
-

### Context to Load
\`\`\`
[relevant files]
\`\`\`
`;

    writeFile(sessionFile, template);
    console.log(`[SessionEnd] Created: ${sessionFile}`);
  }

  process.exit(0);
}

main();
