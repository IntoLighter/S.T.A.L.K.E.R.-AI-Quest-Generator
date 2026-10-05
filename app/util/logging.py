from collections.abc import Callable
from functools import wraps

from loguru import logger


def log_execution[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        logger.info(f"{func.__name__} started")
        result = func(*args, **kwargs)
        logger.info(f"{func.__name__} completed")
        return result

    return wrapper
