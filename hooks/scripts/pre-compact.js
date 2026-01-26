#!/usr/bin/env node
/**
 * PreCompact Hook - Save state before context compaction
 *
 * Logs compaction events and marks session files.
 * Stdout is shown in verbose mode for PreCompact.
 */

const path = require('path');
const {
  getSessionsDir,
  getDateTimeString,
  getTimeString,
  findFiles,
  ensureDir,
  appendFile
} = require('../lib/utils');

function main() {
  const sessionsDir = getSessionsDir();
  const compactionLog = path.join(sessionsDir, 'compaction-log.txt');

  ensureDir(sessionsDir);

  const timestamp = getDateTimeString();
  appendFile(compactionLog, `[${timestamp}] Context compaction triggered\n`);

  const sessions = findFiles(sessionsDir, '*.tmp');
  if (sessions.length > 0) {
    const activeSession = sessions[0].path;
    const timeStr = getTimeString();
    appendFile(activeSession, `\n---\n**[Compaction at ${timeStr}]** - Context summarized\n`);
  }

  console.log(`[PreCompact] State saved at ${timestamp}`);
  process.exit(0);
}

main();
