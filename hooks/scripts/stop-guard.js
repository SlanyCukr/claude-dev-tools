#!/usr/bin/env node

/**
 * stop-guard.js - Stop event hook
 * Part 1: Check for incomplete plan tasks
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

function main() {
  let data;
  try {
    data = JSON.parse(fs.readFileSync('/dev/stdin', 'utf8'));
  } catch {
    process.exit(0);
  }

  // CRITICAL: Prevent infinite loops
  if (data.stop_hook_active) {
    process.exit(0);
  }

  const cwd = data.cwd || process.cwd();
  const plansDir = path.join(os.homedir(), '.claude', 'plans');

  try {
    if (!fs.existsSync(plansDir)) {
      process.exit(0);
    }

    const planFiles = fs.readdirSync(plansDir).filter(f => f.endsWith('.md'));

    for (const planFile of planFiles) {
      const planPath = path.join(plansDir, planFile);
      const content = fs.readFileSync(planPath, 'utf8');

      // Check if plan mentions current working directory
      const planMatchesCwd = content.includes(cwd) ||
                            content.includes(path.basename(cwd)) ||
                            content.includes('./' + path.basename(cwd));

      if (!planMatchesCwd) continue;

      // Look for unchecked task markers
      const lines = content.split('\n');
      const uncheckedTasks = lines.filter(line => {
        const trimmed = line.trim();
        return trimmed.startsWith('- [ ]') || trimmed.startsWith('* [ ]');
      });

      if (uncheckedTasks.length > 0) {
        console.log(JSON.stringify({
          decision: 'block',
          reason: `Cannot stop: ${uncheckedTasks.length} incomplete task(s) in plan (${planFile}). Complete the tasks or use /pause first.`
        }));
        process.exit(0);
      }
    }
  } catch (err) {
    // On error, allow stop to avoid blocking
  }

  process.exit(0);
}

main();
