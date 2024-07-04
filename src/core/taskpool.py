# -*- coding: utf-8 -*-

import asyncio
import logging
from inspect import Traceback
from typing import Any, AsyncGenerator

logger = logging.getLogger(__name__)


class TaskPoolExecutor:
    """A task pool executor that allows a fixed number of tasks to be run concurrently.
    
    Args:
        max_size: The maximum number of tasks that can be run concurrently.
        collect_results: A flag indicating whether or not to collect the results of the tasks that are run.
    """
    
    def __init__(self, max_size: int, collect_results: bool = False):
        self._semaphore = asyncio.Semaphore(max_size)  # Semaphore to control the number of concurrent tasks
        self._tasks = set()  # Set of tasks being tracked by the executor
        self.results = [] if collect_results else None  # List to collect the results of the tasks, if specified

    async def submit(self, coro, *args, **kwargs) -> asyncio.Task:
        """Submit a task to the task pool executor.
        
        Args:
            coro: A coroutine function or coroutine to be run by the executor.
            *args: Arguments to pass to the coroutine function.
            **kwargs: Keyword arguments to pass to the coroutine function.
            
        Returns:
            An asyncio.Task representing the submitted task.
        """
        await self._semaphore.acquire()  # Acquire semaphore to ensure that the maximum number of concurrent tasks is not exceeded
        if asyncio.iscoroutinefunction(coro):
            coro = coro(*args, **kwargs)  # Create coroutine if a coroutine function was provided
        task = asyncio.create_task(coro)  # Create a task to run the coroutine
        self._tasks.add(task)  # Add the task to the set of tasks being tracked by the executor
        task.add_done_callback(self._on_task_done)  # Add a callback to be called when the task is completed
        return task

    async def map(self, coro, *iterables, timeout: float = None) -> AsyncGenerator[Any, None]:
        """Submit multiple tasks to the task pool executor and yield the results as they are completed.
        
        Args:
            coro: A coroutine function to be called with each set of arguments.
            *iterables: Iterables containing the arguments to pass to the coroutine function.
            timeout: The maximum time to wait for tasks to complete, in seconds.
            
        Yields:
            The results of the tasks, in the order that they were submitted.
        """
        # Create a task for each set of arguments and submit them to the task pool executor
        tasks = [await self.submit(coro, *args) for args in zip(*iterables)]
        tasks.reverse()  # Reverse the list of tasks to process them in the order they were submitted
        # Yield the results of the tasks as they are completed, up to the specified timeout
        for task in asyncio.as_completed(tasks, timeout=timeout):
            yield await task

    async def shutdown(self, *, wait: bool = True) -> None:
        """Shut down the task pool executor.
        
        Args:
            wait: A flag indicating whether or not to wait for all tasks to complete before shutting down.
        """
        if self._tasks:  # If there are tasks being tracked by the executor
            if wait:  # Wait for all tasks to complete
                await asyncio.wait(self._tasks)
            else:  # Cancel all tasks
                for task in self._tasks:
                    task.cancel()

    def _on_task_done(self, task: asyncio.Task) -> None:
        """A callback function that is called when a task is completed.
        
        Args:
            task: The completed task.
        """
        exception = task.exception()  # Get the exception raised by the task, if any
        result = task.result()  # Get the result of the task
        logger.debug(f'Task result: {result}')
        self._tasks.remove(task)  # Remove the task from the set of tasks being tracked by the executor
        self._semaphore.release()  # Release the semaphore
        if self.results is not None:  # If collecting results, append the result or exception to the results list
            self.results.append(exception or result)
        elif exception:  # If not collecting results, raise the exception if one occurred
            logger.exception(f'Task result: exception {type(exception).__name__}: {str(exception)}')
            raise exception

    async def __aenter__(self) -> "TaskPoolExecutor":
        """Enter the context manager and return the task pool executor."""
        return self

    async def __aexit__(self, exc_type: type, exc_val: Exception, exc_tb: Traceback) -> bool:
        """Shut down the task pool executor when exiting the context manager."""
        await self.shutdown()  # Shut down the executor
        return False  # Do not suppress any exceptions
