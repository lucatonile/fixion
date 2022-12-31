# Fixion

Useful for adding assertions for cross-file pytest fixtures (e.g. fixtures in `conftest.py`). It provides a standard way of handling breaking fixture changes and gives pretty and informative exception messages.

## Example

Given:

```python
def mult_10(x):
    return x * 10

@pytest.fixture
def some_fixture() -> int:
    return 10
```

you can do:

```python
@fixion.assertions(some_fixture, [
    lambda v: v > 5,
    lambda v: v > 10, # this one fails
])
def test_mult_10(some_fixture):
    assert mult_10(some_fixture) == some_fixture * 10
```

instead of:

```python
def test_mult_10(some_fixture):
    assert v > 5
    assert v > 10 # this one fails
    assert mult_10(some_fixture) == some_fixture * 10
```
