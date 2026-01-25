---
description: Add tests - TDD for unit/integration, E2E for user flows
---

# /test

Add tests using the right approach for the situation.

## Usage

```
/test Add validation for email field
/test Cover the payment processing logic
/test Test the complete checkout flow end-to-end
/test Add regression test for the login bug
```

## What Happens

The agent determines the best testing approach:

**Unit/Integration Tests (TDD)**
- Write failing test first (RED)
- Implement minimal code (GREEN)
- Refactor if needed
- Target 80%+ coverage

**E2E Tests (Playwright)**
- Analyze the user flow
- Generate Page Object Model
- Create test scenarios
- Handle flaky test patterns

## Workflow

```
1. codebase-explorer → Find existing test patterns
2. tdd-guide OR e2e-runner → Based on scope
3. bash-commands    → Run tests
4. code-reviewer    → Verify test quality
```

## Choosing Test Type

| Keyword/Scope | Test Type |
|---------------|-----------|
| "unit test", "function", "class" | TDD |
| "flow", "journey", "end-to-end", "E2E" | Playwright |
| "regression test for bug" | TDD |
| "user can...", "verify that..." | Playwright |
| Business logic, algorithms | TDD |
| UI interactions, multi-page flows | Playwright |

## Test Quality Standards

- Tests should be independent
- Clear arrange-act-assert structure
- Mock external services
- Descriptive test names
- No flaky tests (quarantine if needed)
