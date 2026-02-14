#!/usr/bin/env node

/**
 * tool-redirect.js - PreToolUse hook (*)
 * Suggest better tool alternatives for common bash commands.
 */

const fs = require('fs');

function getPrimaryCommand(cmd) {
  if (!cmd) return '';
  const firstSegment = cmd.split(/[|;&]/).shift().trim();
  return firstSegment.split(/\s+/)[0];
}

function main() {
  let data;
  try {
    data = JSON.parse(fs.readFileSync('/dev/stdin', 'utf8'));
  } catch {
    process.exit(0);
  }

  const toolName = data.tool_name;
  const toolInput = data.tool_input || {};

  if (toolName !== 'Bash') {
    process.exit(0);
  }

  const command = toolInput.command || '';
  const primary = getPrimaryCommand(command);

  const redirects = {
    'grep': 'Use the Grep tool instead of bash grep/rg. For semantic code search, use mcp__semvex__search_code_tool.',
    'rg': 'Use the Grep tool instead of bash grep/rg. For semantic code search, use mcp__semvex__search_code_tool.',
    'find': 'Use the Glob tool instead of bash find/fd.',
    'fd': 'Use the Glob tool instead of bash find/fd.',
    'cat': 'Use the Read tool instead.',
    'head': 'Use the Read tool instead.',
    'tail': 'Use the Read tool instead.',
    'sed': 'Use the Edit tool instead.',
    'awk': 'Use the Edit tool instead.',
  };

  if (redirects[primary]) {
    console.error(redirects[primary]);
    process.exit(2);
  }

  process.exit(0);
}

main();
