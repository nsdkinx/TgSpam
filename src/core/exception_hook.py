# -*- coding: utf-8 -*-

from types import TracebackType


def global_exception_hook(exc_type: Exception, exc_value: str, exc_traceback: TracebackType):
    """Low level unhandled exception handler"""
    import logging
    logger = logging.getLogger(__name__)
    logger.exception('Global exception.', exc_info=(exc_type, exc_value, exc_traceback))
    from rich import print
    print('[bold red]-|-|- CRITICAL SOFTWARE ERROR -|-|-[/]')
    print(f'[bold red]{exc_type.__name__}:[/] {exc_value}. ')
    print('Send logs to the support.')
    input()
    import sys
    sys.exit(1)
