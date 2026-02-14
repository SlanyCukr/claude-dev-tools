---
globs: ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx"]
---

# TypeScript/JavaScript Standards

## Strict Mode

TypeScript must use `strict: true` in tsconfig.json.

```typescript
// tsconfig.json
{
  "compilerOptions": {
    "strict": true
  }
}
```

Never use `// @ts-ignore` without a comment explaining why.

```typescript
// BAD - Unjustified ts-ignore
// @ts-ignore
const data = fetchData();

// BETER - With justification
// @ts-ignore - Legacy API, migration planned Q2
const data = fetchData();
```

## Explicit Return Types

Public API functions and exported functions must have explicit return types.

```typescript
// BAD - Implicit return type
export function getUser(id: string) {
  return db.find(id);
}

// GOOD - Explicit return type
export function getUser(id: string): User | null {
  return db.find(id);
}
```

Internal functions can use inference when the type is obvious.

## ESLint Conventions

Follow project's ESLint config. No `eslint-disable` without justification.

```typescript
// BAD - Unjustified eslint-disable
// eslint-disable-next-line
const unused = 42;

// GOOD - With justification
// eslint-disable-next-line no-console -- Temporary debug log
console.log(data);
```

## Prefer Const

Use `const` by default, `let` only when reassignment is needed. Never use `var`.

```typescript
// BAD - Using var
var name = "Alice";

// BAD - Using let without reassignment
let age = 30;

// GOOD - Using const
const name = "Alice";
const age = 30;

// GOOD - Using let when reassigning
let counter = 0;
counter += 1;
```

## No Any

Use `unknown` with type guards instead of `any`.

```typescript
// BAD - Using any
function processData(data: any) {
  return data.value;
}

// GOOD - Using unknown with type guard
function processData(data: unknown): string | null {
  if (typeof data === 'object' && data !== null && 'value' in data) {
    return String((data as { value: unknown }).value);
  }
  return null;
}
```

## Async/Await

Prefer async/await over raw Promises. Handle errors properly.

```typescript
// BAD - Raw Promise chains
fetchUser(id)
  .then(user => user.name)
  .then(name => console.log(name))
  .catch(err => console.error(err));

// GOOD - Async/await with error handling
async function displayUserName(id: string): Promise<void> {
  try {
    const user = await fetchUser(id);
    console.log(user.name);
  } catch (error) {
    console.error('Failed to fetch user:', error);
    throw error;
  }
}
```

## React Patterns

For `.tsx` files:

### Functional Components

```typescript
// GOOD - Functional component with TypeScript
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

export function Button({ label, onClick, disabled }: ButtonProps) {
  return (
    <button onClick={onClick} disabled={disabled}>
      {label}
    </button>
  );
}
```

### Custom Hooks

Extract shared logic into custom hooks:

```typescript
// GOOD - Custom hook for data fetching
function useUserData(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUser(userId).then(setUser).finally(() => setLoading(false));
  }, [userId]);

  return { user, loading };
}
```

### Proper Key Props

Always provide stable keys for lists:

```typescript
// BAD - Using index as key
{items.map((item, index) => (
  <Item key={index} {...item} />
))}

// GOOD - Using unique ID
{items.map((item) => (
  <Item key={item.id} {...item} />
))}
```

## Verification Checklist

Before committing TypeScript/JavaScript code:
- [ ] TypeScript compiles (`npx tsc --noEmit`)
- [ ] No ESLint errors (`npx eslint path/to/file`)
- [ ] No `any` types (use `unknown`)
- [ ] Explicit return types on exports
- [ ] Proper error handling on async code
- [ ] React components have proper prop types

## Agent Support

- **react-nextjs-agent** - React/Next.js implementation with TypeScript patterns
- **tdd-guide** - Test-driven development for TypeScript features
