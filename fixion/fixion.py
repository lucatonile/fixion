from typing import TypeVar, Any, Generic, Callable, List, Optional, Tuple
from functools import partial, wraps
import inspect

T = TypeVar("T", bound=Any)
PytestFixture = Callable[..., T]
Predicate = Callable[[T], bool]

class Assertion(Generic[T]):
    def __init__(self: "Assertion", fixture_val: T, predicate: Predicate):
        self._fixture_val = fixture_val
        self._predicate = predicate
        self.failed = False

    def __str__(self: "Assertion") -> str:
        try:
            funcString = str(inspect.getsourcelines(self._predicate)[0])
            # TODO regex this shiet?
            return (
                funcString
                .replace("\\n", "")
                .replace("'", "")
                .replace("[", "")
                .replace("]", "")
                .replace(",", "")
                .strip()
            )
        except:
            return self._predicate


    def apply(self: "Assertion") -> "Assertion":
        self.failed = not self._predicate(self._fixture_val)
        return self

class Assertions(Generic[T]):
    """
        Note: Order of assertions list during instantiation is used
        in string represenation.
    """
    def __init__(self: "Assertions", assertions: List[Assertion]):
        self._assertions = assertions
    
    def __str__(self: "Assertions"):
        msgs = [
            f"Predicate [{a}] at index {i} failed"
            for i, a in enumerate(self.failed_assertions)
        ]

        return "Fixture assertions failed!\n" + "\n".join(msgs)
    
    @property
    def raw(self: "Assertions") -> List[Assertion]:
        return self._assertions

    @property
    def failed(self: "Assertions") -> bool:
        return any(a.failed for a in self._assertions)
    
    @property
    def failed_assertions(self: "Assertions") -> List["Assertions"]:
        return [a for a in self._assertions if a.failed]

    def apply(self: "Assertions") -> None:
        self._assertions = [a.apply() for a in self._assertions]

def _do_assertions(fixture_val: T, predicates: List[Predicate]) -> None:
    assertion_generator = partial(Assertion, fixture_val)
    assertions = Assertions(
        [assertion_generator(p) for p in predicates]
    )
    assertions.apply()

    if not assertions.failed:
        return

    raise AssertionError(assertions)

def assertions(fixture: PytestFixture[T], predicates: List[Predicate]):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _fixture_val: Optional[T] = kwargs.get(fixture.__name__)
            if not _fixture_val:
                raise ValueError(
                    f"Couldn't find fixture '{fixture.__name__}' in test parameters"
                )

            _do_assertions(_fixture_val, predicates)
            return func(*args, **kwargs)

        return wrapper

    return inner
