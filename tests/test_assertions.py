import pytest
import fixion

@pytest.fixture
def some_fixture() -> int:
    return 10

def mult_10(x):
    return x * 10

@fixion.assertions(some_fixture, [
    lambda v: v > 50,
    lambda v: v > 10
])
def test_mult_10(some_fixture):
    assert mult_10(some_fixture) == some_fixture * 10

