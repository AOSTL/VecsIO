import functools
from typing import Callable, Any, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

def decorator_wrapper(checker: Callable[P, Any]) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(fn)
        def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
            if not checker(*args, **kwargs):
                return fn(*args, **kwargs)
            else:
                raise SystemExit(1)
        return wrapped
    return decorator