---
description: Security review - quick check or full audit with fixes
---

# /security

Security review ranging from quick file check to full audit with fixes.

## Usage

```
/security src/auth/login.ts
/security Review the payment processing flow
/security Full audit before production deploy
/security Check API endpoints for injection
```

## Scope Determines Depth

| Scope | What Happens |
|-------|--------------|
| Single file | Quick review, report issues |
| Directory/flow | Thorough review, map entry points |
| "Full audit" | Complete OWASP scan + fixes + verification |

## Quick Review Workflow

```
1. security-reviewer → Scan for vulnerabilities
```

## Full Audit Workflow

```
1. security-reviewer → Full OWASP audit
2. codebase-explorer → Map all input entry points
3. build-agent      → Fix vulnerabilities
4. security-reviewer → Verify fixes
```

## What Gets Checked

**OWASP Top 10:**
- Injection (SQL, NoSQL, command, LDAP)
- Broken authentication
- Sensitive data exposure
- XXE (XML external entities)
- Broken access control
- Security misconfiguration
- XSS (cross-site scripting)
- Insecure deserialization
- Vulnerable components
- Insufficient logging

**Additional Checks:**
- Hardcoded secrets (API keys, passwords)
- Missing input validation
- CSRF protection
- Rate limiting
- Auth/authz bypasses

## Severity Levels

- **CRITICAL** - Fix immediately (secrets, SQL injection, auth bypass)
- **HIGH** - Fix before production (XSS, SSRF, missing auth)
- **MEDIUM** - Fix when possible (logging PII, missing rate limits)

## When to Use

- Before production deployment
- After adding auth/authz code
- When handling user input
- After adding payment/financial code
- When integrating external APIs
- Regular security reviews

## Related

- Agent: agents/security-reviewer.md
- Rules: rules/security.md
