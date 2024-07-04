# -*- coding: utf-8 -*-

import asyncio
import inspect
from typing import Callable, Union


def expects(condition: bool, callback: Union[Exception, Callable], *args, **kwargs) -> None:
    """Check is the condition is true. Otherwise raise an exception or call a function"""
    if condition:
        return None

    if isinstance(callback, BaseException):
        raise callback
    elif callable(callback):
        return callback(*args, **kwargs)


def only_once(func: Callable):
    """Allows a function or a coroutine to run only once."""

    def wrapper(*args, **kwargs):
        if not wrapper.called:
            wrapper.called = True
            if inspect.iscoroutinefunction(func):
                return asyncio.create_task(func(*args, **kwargs))
            else:
                return func(*args, **kwargs)
        else:
            raise RuntimeError(f'{func.__name__} has been called twice')

    wrapper.called = False
    return wrapper
