# Security Guidelines

## Mandatory Security Checks

Before ANY commit:
- [ ] No hardcoded secrets (API keys, passwords, tokens)
- [ ] All user inputs validated
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (sanitized HTML)
- [ ] CSRF protection enabled
- [ ] Authentication/authorization verified
- [ ] Rate limiting on all endpoints
- [ ] Error messages don't leak sensitive data

## Secret Management

```typescript
// NEVER: Hardcoded secrets
const apiKey = "sk-proj-xxxxx"

// ALWAYS: Environment variables
const apiKey = process.env.OPENAI_API_KEY

if (!apiKey) {
  throw new Error('OPENAI_API_KEY not configured')
}
```

## Input Validation

```typescript
// ALWAYS validate user input at system boundaries
import { z } from 'zod'

const UserInputSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
})

// Validate before use
const validated = UserInputSchema.parse(userInput)
```

## SQL Injection Prevention

```typescript
// NEVER: String interpolation in queries
const query = `SELECT * FROM users WHERE id = ${userId}`

// ALWAYS: Parameterized queries
const { data } = await supabase
  .from('users')
  .select('*')
  .eq('id', userId)
```

## XSS Prevention

```typescript
// NEVER: Direct HTML insertion
element.innerHTML = userInput

// ALWAYS: Use textContent or sanitize
element.textContent = userInput
// OR
import DOMPurify from 'dompurify'
element.innerHTML = DOMPurify.sanitize(userInput)
```

## Security Response Protocol

If security issue found:
1. STOP immediately
2. Use **security-reviewer** agent
3. Fix CRITICAL issues before continuing
4. Rotate any exposed secrets
5. Review entire codebase for similar issues

## Agent Support

- **security-reviewer** - Use PROACTIVELY for security audits
