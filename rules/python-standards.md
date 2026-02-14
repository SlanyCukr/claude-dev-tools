---
globs: ["**/*.py"]
---

# Python Standards

## Type Hints Mandatory

All function signatures must have type annotations.

```python
# BAD - No type hints
def calculate_total(items, tax_rate):
    return sum(item.price for item in items) * (1 + tax_rate)

# GOOD - Complete type hints
from typing import List

def calculate_total(items: List[Item], tax_rate: float) -> float:
    """Calculate total with tax."""
    return sum(item.price for item in items) * (1 + tax_rate)
```

## Ruff Conventions

Follow Ruff's default rules. Common issues to avoid:

- **E501** - Line too long (> 88 characters)
- **F401** - Unused import
- **F841** - Unused variable
- **W503** - Line break before binary operator

```bash
# Check your code
ruff check path/to/file.py

# Auto-fix issues
ruff check --fix path/to/file.py
```

## Pytest Patterns

Use pytest for testing with these conventions:

```python
# GOOD - Descriptive test name, parametrized
@pytest.mark.parametrize("input,expected", [
    ("hello", "hello"),
    ("", ""),
    (None, ""),
])
def test_sanitize_input(input, expected):
    assert sanitize(input) == expected

# GOOD - Fixture for setup
@pytest.fixture
def user(db):
    return User.objects.create(username="test")

def test_user_can_login(user, client):
    response = client.post("/login", {"username": user.username})
    assert response.status_code == 200
```

## Import Ordering

Imports must follow this order:

1. Standard library imports
2. Third-party imports
3. Local application imports

One import per line for clarity.

```python
# GOOD - Proper ordering
import os
import sys

from typing import Optional

import pytest
import requests

from myapp.models import User
from myapp.utils import calculate_total
```

## No Bare Except

Always catch specific exceptions.

```python
# BAD - Bare except
try:
    data = fetch_data()
except:
    pass

# GOOD - Specific exception
try:
    data = fetch_data()
except ConnectionError as e:
    logger.error(f"Connection failed: {e}")
    raise
```

## Docstrings

Use Google style for public APIs:

```python
def create_user(email: str, name: str) -> User:
    """Create a new user.

    Args:
        email: User's email address.
        name: User's full name.

    Returns:
        The created User instance.

    Raises:
        ValueError: If email is already registered.
    """
    ...
```

## Dataclasses/Pydantic

Prefer dataclasses or Pydantic models over plain dicts:

```python
# BAD - Plain dict
user = {"name": "Alice", "age": 30}

# GOOD - Dataclass
@dataclass
class User:
    name: str
    age: int

# GOOD - Pydantic for validation
class User(BaseModel):
    name: str
    age: int
```

## Verification Checklist

Before committing Python code:
- [ ] All functions have type hints
- [ ] No Ruff errors (`ruff check`)
- [ ] Tests pass (`pytest`)
- [ ] No bare except clauses
- [ ] Imports properly ordered
- [ ] Docstrings on public APIs

## Agent Support

- **python-build-agent** - Python implementation with type hints and Ruff conventions
- **tdd-guide** - Test-driven development for Python features
