---
description: Security audit workflow - full OWASP review, fix vulnerabilities, verify
---

# /audit

Comprehensive security audit and hardening workflow.

## Workflow

```
1. security-reviewer → Full OWASP Top 10 audit
2. codebase-explorer → Find all input entry points
3. build-agent      → Fix identified vulnerabilities
4. security-reviewer → Verify fixes are complete
```

## Usage

```
/audit Review the authentication system
/audit Check API endpoints for injection vulnerabilities
/audit Full security review before production deploy
```

## What Happens

1. **Security Reviewer** performs comprehensive audit:
   - OWASP Top 10 vulnerabilities
   - Hardcoded secrets
   - SQL/command injection
   - XSS vulnerabilities
   - CSRF protection
   - Authentication flaws
   - Authorization bypasses
2. **Codebase Explorer** maps all entry points:
   - API endpoints
   - Form handlers
   - File uploads
   - WebSocket handlers
3. **Build Agent** fixes vulnerabilities with secure patterns
4. **Security Reviewer** verifies all fixes

## OWASP Top 10 Checked

| Category | Examples |
|----------|----------|
| Injection | SQL, NoSQL, command, LDAP |
| Broken Auth | Weak passwords, session issues |
| Sensitive Data | Unencrypted storage, logging secrets |
| XXE | XML external entity attacks |
| Broken Access | IDOR, privilege escalation |
| Misconfig | Default creds, verbose errors |
| XSS | Reflected, stored, DOM-based |
| Insecure Deserialization | Untrusted data parsing |
| Vulnerable Components | Outdated dependencies |
| Logging Gaps | Missing audit trails |

## When to Use

- Before production deployment
- After adding authentication/authorization
- When handling payment or PII data
- Regular security reviews
- After a security incident

## Difference from /security

- `/security` - Quick single-file review
- `/audit` - Full workflow with fixes and verification
