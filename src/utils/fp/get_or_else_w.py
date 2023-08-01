from typing import Any, Callable, TypeVar

from returns.pipeline import is_successful

F = TypeVar("F")
R = TypeVar("R")
S = TypeVar("S")


def get_or_else_w(on_failure: Callable[[F], Any]) -> Callable[[R], S]:
    def func(result) -> S:
        if is_successful(result):
            return result.unwrap()
        return on_failure(result.failure())

    return func
