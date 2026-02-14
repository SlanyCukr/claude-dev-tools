#!/usr/bin/env node

/**
 * context-monitor.js - PostToolUse hook (*)
 * Track real context usage via transcript JSONL. Replaces suggest-compact.js.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const STATE_DIR = process.env.TMPDIR || '/tmp';
const MAX_TOKENS = 200000;

function readLastUsage(transcriptPath) {
  try {
    const content = fs.readFileSync(transcriptPath, 'utf8');
    const lines = content.trim().split('\n');

    for (let i = lines.length - 1; i >= 0; i--) {
      try {
        const entry = JSON.parse(lines[i]);
        if (entry.role === 'assistant' && entry.usage) {
          return entry.usage;
        }
      } catch {}
    }
  } catch {}
  return null;
}

function calculateContextUsage(usage) {
  if (!usage) return 0;
  return (usage.input_tokens || 0)
    + (usage.cache_creation_input_tokens || 0)
    + (usage.cache_read_input_tokens || 0);
}

function loadState(sessionId) {
  const stateFile = path.join(STATE_DIR, `claude-context-${sessionId}.json`);
  try {
    const content = fs.readFileSync(stateFile, 'utf8');
    return JSON.parse(content);
  } catch {
    return null;
  }
}

function saveState(sessionId, state) {
  const stateFile = path.join(STATE_DIR, `claude-context-${sessionId}.json`);
  const tmpFile = `${stateFile}.tmp`;

  try {
    fs.writeFileSync(tmpFile, JSON.stringify(state), 'utf8');
    fs.renameSync(tmpFile, stateFile);
  } catch {}
}

function shouldThrottle(state) {
  if (!state || !state.lastWarningTime) return false;
  const now = Date.now();
  const elapsed = (now - state.lastWarningTime) / 1000;
  return elapsed < 30;
}

function getWarningLevel(usagePercent) {
  if (usagePercent >= 95) return 95;
  if (usagePercent >= 85) return 85;
  if (usagePercent >= 75) return 75;
  if (usagePercent >= 60) return 60;
  return null;
}

function getMessage(level) {
  const messages = {
    60: 'Context at 60% — consider /compact if transitioning between phases',
    75: 'Context at 75% — store discoveries with store_memory_tool, then /compact',
    85: 'Context at 85% — use /pause to save state, then compact or start new session',
    95: 'CRITICAL: Context at 95% — /pause NOW before context is exhausted'
  };
  return messages[level] || '';
}

function main() {
  let data;
  try {
    data = JSON.parse(fs.readFileSync('/dev/stdin', 'utf8'));
  } catch {
    process.exit(0);
  }

  const transcriptPath = data.transcript_path;
  const sessionId = data.session_id;

  if (!transcriptPath || !sessionId) process.exit(0);

  const latestUsage = readLastUsage(transcriptPath);
  if (!latestUsage) process.exit(0);

  const currentContext = calculateContextUsage(latestUsage);
  const usagePercent = (currentContext / MAX_TOKENS) * 100;
  const warningLevel = getWarningLevel(usagePercent);

  if (!warningLevel) process.exit(0);

  const state = loadState(sessionId) || {};

  // No throttle at 85%+
  if (warningLevel < 85 && shouldThrottle(state)) {
    process.exit(0);
  }

  state.lastWarningLevel = warningLevel;
  state.lastWarningTime = Date.now();
  saveState(sessionId, state);

  console.log(JSON.stringify({
    systemMessage: getMessage(warningLevel),
    hookSpecificOutput: {
      hookEventName: 'PostToolUse',
      additionalContext: `Context usage: ${usagePercent.toFixed(1)}%`
    }
  }));

  process.exit(0);
}

main();
