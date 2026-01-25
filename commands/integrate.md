---
description: Library integration workflow - research, design, implement, test
---

# /integrate

New library or service integration workflow.

## Workflow

```
1. context7-docs    → Get official library documentation
2. web-research     → Find best practices and examples
3. architect        → Design integration approach
4. build-agent      → Implement integration
5. tdd-guide        → Add tests with mocked externals
```

## Usage

```
/integrate Stripe for payment processing
/integrate SendGrid for transactional emails
/integrate Prisma ORM to replace raw SQL
/integrate NextAuth for authentication
```

## What Happens

1. **Context7 Docs** retrieves official documentation for the library
2. **Web Research** finds:
   - Best practices
   - Common pitfalls
   - Example implementations
   - Security considerations
3. **Architect** designs how to integrate:
   - Where to put the code
   - How to handle errors
   - Configuration approach
4. **Build Agent** implements the integration
5. **TDD Guide** writes tests with mocked external calls

## Parallel Research Phase

These run simultaneously for speed:
```
├── context7-docs  → Official docs
├── web-research   → Best practices
└── codebase-explorer → Existing patterns
```

## When to Use

- Adding new npm/pip packages
- Integrating third-party APIs
- Replacing one library with another
- Adding infrastructure (Redis, S3, etc.)

## Tips

- Always mock external services in tests
- Store API keys in environment variables
- Add retry logic for network calls
- Log integration errors for debugging
