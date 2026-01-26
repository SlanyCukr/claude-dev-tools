#!/usr/bin/env node
/**
 * SessionStart Hook - Load previous context on new session
 *
 * For SessionStart, stdout is added to Claude's context.
 * Checks for recent sessions and learned skills.
 */

const path = require('path');
const {
  getSessionsDir,
  getLearnedSkillsDir,
  findFiles,
  ensureDir
} = require('../lib/utils');

function main() {
  const sessionsDir = getSessionsDir();
  const learnedDir = getLearnedSkillsDir();

  ensureDir(sessionsDir);
  ensureDir(learnedDir);

  const messages = [];

  // Check for recent session files (last 7 days)
  const recentSessions = findFiles(sessionsDir, '*.tmp', { maxAge: 7 });
  if (recentSessions.length > 0) {
    messages.push(`Found ${recentSessions.length} recent session(s). Latest: ${recentSessions[0].path}`);
  }

  // Check for learned skills
  const learnedSkills = findFiles(learnedDir, '*.md');
  if (learnedSkills.length > 0) {
    messages.push(`${learnedSkills.length} learned skill(s) available in ${learnedDir}`);
  }

  // Output to stdout - gets added to Claude's context for SessionStart
  if (messages.length > 0) {
    console.log('[SessionStart] ' + messages.join('. '));
  }

  process.exit(0);
}

main();
