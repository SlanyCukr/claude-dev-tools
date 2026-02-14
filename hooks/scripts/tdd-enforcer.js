#!/usr/bin/env node

/**
 * tdd-enforcer.js - PostToolUse hook for Edit/Write
 * Non-blocking reminder when implementation files edited without failing tests.
 */

const fs = require('fs');
const path = require('path');

function isTestFile(filePath) {
  const base = path.basename(filePath);
  const dir = path.dirname(filePath);

  if (base.includes('.test.') || base.includes('.spec.')) return true;
  if (base.startsWith('test_') || base.includes('_test.')) return true;
  if (dir.includes('__tests__') || dir.includes('/tests/')) return true;

  return false;
}

function isConfigOrDocs(filePath) {
  const ext = path.extname(filePath);
  const configExts = ['.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf'];
  const docsExts = ['.md', '.txt', '.rst'];
  const base = path.basename(filePath);

  if (configExts.includes(ext) || docsExts.includes(ext)) return true;
  if (base === 'Dockerfile' || base === 'Makefile') return true;
  if (base.includes('config') || base.includes('migration')) return true;

  return false;
}

function isTrivialEdit(newString) {
  if (!newString) return true;
  const lines = newString.split('\n').filter(line => line.trim() && !line.trim().startsWith('//'));
  return lines.length < 5;
}

function hasFailingTests(filePath) {
  const dir = path.dirname(filePath);
  const ext = path.extname(filePath);

  // Python: check pytest cache
  if (ext === '.py') {
    const pytestCache = path.join(dir, '.pytest_cache', 'v', 'cache', 'lastfailed');
    try {
      if (fs.existsSync(pytestCache)) {
        const content = fs.readFileSync(pytestCache, 'utf8');
        if (content.trim() && content.includes('{}') === false) {
          return true;
        }
      }
    } catch {}
    return false;
  }

  // JS/TS: check for corresponding test file existence
  if (['.ts', '.tsx', '.js', '.jsx'].includes(ext)) {
    const base = path.basename(filePath, ext);
    const testPaths = [
      path.join(dir, `${base}.test.ts`),
      path.join(dir, `${base}.test.js`),
      path.join(dir, `${base}.spec.ts`),
      path.join(dir, `${base}.spec.js`),
    ];

    for (const testPath of testPaths) {
      if (fs.existsSync(testPath)) {
        return true;
      }
    }

    // Check __tests__ directory
    const testsDir = path.join(path.dirname(filePath), '__tests__');
    try {
      if (fs.existsSync(testsDir)) {
        const files = fs.readdirSync(testsDir);
        const baseName = base.replace(/\.(test|spec)$/, '');
        if (files.some(f => f.includes(baseName))) {
          return true;
        }
      }
    } catch {}
  }

  return false;
}

function main() {
  let data;
  try {
    data = JSON.parse(fs.readFileSync('/dev/stdin', 'utf8'));
  } catch {
    process.exit(0);
  }

  const filePath = data.tool_output?.file_path || data.tool_output?.path;
  const newString = data.tool_input?.new_string;

  if (!filePath) process.exit(0);

  if (isTestFile(filePath) || isConfigOrDocs(filePath) || isTrivialEdit(newString)) {
    process.exit(0);
  }

  if (!hasFailingTests(filePath)) {
    console.log(JSON.stringify({
      systemMessage: 'TDD: No failing tests found for this file. Consider writing tests first.',
      hookSpecificOutput: {
        hookEventName: 'PostToolUse',
        additionalContext: 'TDD reminder: RED → GREEN → REFACTOR'
      }
    }));
  }

  process.exit(0);
}

main();
