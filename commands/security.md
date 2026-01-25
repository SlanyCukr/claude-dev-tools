---
description: Run security review on code. Checks for OWASP Top 10 vulnerabilities, hardcoded secrets, injection flaws, and authentication issues.
---

# /security

Invokes the **security-reviewer** agent to perform a security audit.

## What This Command Does

1. **Vulnerability Detection** - OWASP Top 10 issues
2. **Secrets Scanning** - Hardcoded API keys, passwords, tokens
3. **Input Validation** - SQL injection, XSS, command injection
4. **Auth/Authz Review** - Broken authentication, missing authorization
5. **Dependency Audit** - Known vulnerable packages

## When to Use

Use `/security` when:
- New API endpoints added
- Authentication/authorization code changed
- User input handling added
- Database queries modified
- File upload features added
- Payment/financial code changed
- External API integrations added
- Dependencies updated
- Before major releases

## Severity Levels

- **CRITICAL** - Fix immediately (hardcoded secrets, SQL injection, auth bypass)
- **HIGH** - Fix before production (XSS, SSRF, missing auth checks)
- **MEDIUM** - Fix when possible (logging sensitive data, missing rate limiting)

## Security Tools

```bash
# Check for vulnerable dependencies
npm audit

# Check for secrets in files
grep -r "api[_-]?key\|password\|secret" --include="*.ts" .

# Scan for hardcoded secrets
npx trufflehog filesystem . --json
```

## Related

- Agent: agents/security-reviewer.md
- Rules: rules/security.md
