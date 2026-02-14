#!/usr/bin/env node

/**
 * file-checker.js - PostToolUse hook for Edit/Write
 * Report-only linter that runs after file edits. NO auto-fixing.
 */

const fs = require('fs');
const { execSync } = require('child_process');
const path = require('path');

function tryExec(cmd) {
  try {
    execSync(cmd, { stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
}

function findAncestorFile(dir, filenames) {
  let currentDir = dir;
  while (currentDir !== path.parse(currentDir).root) {
    for (const fname of filenames) {
      const candidate = path.join(currentDir, fname);
      if (fs.existsSync(candidate)) {
        return candidate;
      }
    }
    const parent = path.dirname(currentDir);
    if (parent === currentDir) break;
    currentDir = parent;
  }
  return null;
}

function runChecker(filePath, ext) {
  const dir = path.dirname(filePath);

  // Python files
  if (ext === '.py') {
    const projectRoot = findAncestorFile(dir, ['pyproject.toml', 'setup.py', 'setup.cfg']);
    if (!projectRoot) return null;
    if (!tryExec('command -v ruff')) return null;
    try {
      const output = execSync(`ruff check "${filePath}"`, { encoding: 'utf8', timeout: 5000 });
      if (output.trim()) {
        return `ruff check: ${output.trim()}`;
      }
    } catch (err) {
      const stderr = err.stderr || err.stdout || '';
      if (stderr.trim()) {
        return `ruff check: ${stderr.trim()}`;
      }
    }
    return null;
  }

  // TypeScript/JavaScript files
  if (['.ts', '.tsx', '.js', '.jsx'].includes(ext)) {
    const projectRoot = findAncestorFile(dir, ['package.json']);
    if (!projectRoot) return null;
    if (!tryExec('command -v eslint')) return null;
    try {
      const output = execSync(`eslint "${filePath}"`, { encoding: 'utf8', timeout: 10000 });
      if (output.trim()) {
        return `eslint: ${output.trim()}`;
      }
    } catch (err) {
      const stderr = err.stderr || err.stdout || '';
      if (stderr.trim()) {
        return `eslint: ${stderr.trim()}`;
      }
    }
    return null;
  }

  // Go files
  if (ext === '.go') {
    const projectRoot = findAncestorFile(dir, ['go.mod']);
    if (!projectRoot) return null;
    if (!tryExec('command -v golangci-lint')) return null;
    try {
      const output = execSync(`golangci-lint run --fast "${filePath}"`, { encoding: 'utf8', timeout: 15000 });
      if (output.trim()) {
        return `golangci-lint: ${output.trim()}`;
      }
    } catch (err) {
      const stderr = err.stderr || err.stdout || '';
      if (stderr.trim()) {
        return `golangci-lint: ${stderr.trim()}`;
      }
    }
    return null;
  }

  return null;
}

function main() {
  let data;
  try {
    data = JSON.parse(fs.readFileSync('/dev/stdin', 'utf8'));
  } catch {
    process.exit(0);
  }

  const filePath = data.tool_output?.file_path || data.tool_output?.path;
  if (!filePath) process.exit(0);

  const ext = path.extname(filePath);
  const result = runChecker(filePath, ext);

  if (result) {
    console.log(JSON.stringify({
      systemMessage: `${result} in ${filePath}`,
      hookSpecificOutput: {
        hookEventName: 'PostToolUse',
        additionalContext: 'Lint errors found. Fix before committing.'
      }
    }));
  }

  process.exit(0);
}

main();
