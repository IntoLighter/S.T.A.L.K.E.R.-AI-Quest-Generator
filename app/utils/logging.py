from collections.abc import Callable
from functools import wraps

from loguru import logger


def log_execution[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    name = getattr(func, "__name__", repr(func))

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        logger.info(f"{name} started")
        result = func(*args, **kwargs)
        logger.info(f"{name} completed")
        return result

    return wrapper
