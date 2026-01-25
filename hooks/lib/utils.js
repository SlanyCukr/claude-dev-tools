/**
 * Shared utilities for hook scripts
 * Cross-platform (Windows, macOS, Linux)
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

/**
 * Get the base directory for session data
 */
function getSessionsDir() {
  const claudeHome = process.env.CLAUDE_HOME || path.join(os.homedir(), '.claude');
  return path.join(claudeHome, 'sessions');
}

/**
 * Get the directory for learned skills
 */
function getLearnedSkillsDir() {
  const claudeHome = process.env.CLAUDE_HOME || path.join(os.homedir(), '.claude');
  return path.join(claudeHome, 'learned-skills');
}

/**
 * Get temp directory (cross-platform)
 */
function getTempDir() {
  return os.tmpdir();
}

/**
 * Get current date as YYYY-MM-DD string
 */
function getDateString() {
  return new Date().toISOString().split('T')[0];
}

/**
 * Get current time as HH:MM:SS string
 */
function getTimeString() {
  return new Date().toTimeString().split(' ')[0];
}

/**
 * Get current datetime as ISO string
 */
function getDateTimeString() {
  return new Date().toISOString();
}

/**
 * Ensure a directory exists
 */
function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

/**
 * Read a file, return null only if file doesn't exist
 * Throws on other errors (permission denied, etc.)
 */
function readFile(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf-8');
  } catch (err) {
    if (err.code === 'ENOENT') {
      return null; // File not found is expected
    }
    throw err; // Propagate other errors
  }
}

/**
 * Write content to a file
 */
function writeFile(filePath, content) {
  ensureDir(path.dirname(filePath));
  fs.writeFileSync(filePath, content, 'utf-8');
}

/**
 * Append content to a file
 */
function appendFile(filePath, content) {
  ensureDir(path.dirname(filePath));
  fs.appendFileSync(filePath, content, 'utf-8');
}

/**
 * Replace pattern in file
 * Throws on errors
 */
function replaceInFile(filePath, pattern, replacement) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const newContent = content.replace(pattern, replacement);
  fs.writeFileSync(filePath, newContent, 'utf-8');
  return true;
}

/**
 * Find files matching a pattern in a directory
 * @param {string} dir - Directory to search
 * @param {string} pattern - Glob pattern (simple: *.md, *.tmp)
 * @param {object} options - Optional { maxAge: days }
 * @returns {Array<{path: string, mtime: Date}>}
 */
function findFiles(dir, pattern, options = {}) {
  const results = [];

  if (!fs.existsSync(dir)) {
    return results;
  }

  const ext = pattern.replace('*', '');
  const maxAgeMs = options.maxAge ? options.maxAge * 24 * 60 * 60 * 1000 : null;
  const now = Date.now();

  const files = fs.readdirSync(dir); // Let errors propagate
  for (const file of files) {
    if (file.endsWith(ext)) {
      const filePath = path.join(dir, file);
      const stats = fs.statSync(filePath);

      if (maxAgeMs && (now - stats.mtimeMs) > maxAgeMs) {
        continue;
      }

      results.push({
        path: filePath,
        mtime: stats.mtime
      });
    }
  }

  // Sort by mtime, newest first
  return results.sort((a, b) => b.mtime - a.mtime);
}

/**
 * Log a message to stderr (visible in hook output)
 */
function log(message) {
  console.error(message);
}

module.exports = {
  getSessionsDir,
  getLearnedSkillsDir,
  getTempDir,
  getDateString,
  getTimeString,
  getDateTimeString,
  ensureDir,
  readFile,
  writeFile,
  appendFile,
  replaceInFile,
  findFiles,
  log
};
