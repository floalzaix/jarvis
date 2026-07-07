#
#   Imports
#

import streamlit as st
import asyncio
import threading

from typing import Any, Coroutine, TypeVar

#
#   Async Worker
#

T = TypeVar("T")

class AsyncWorker:
    """
        Runs a dedicated asyncio event loop in a background thread
        so coroutines can be executed from synchronous code.
    """

    def __init__(self):
        #
        #   Event loop thread
        #

        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(
            target=self._run_loop,
            name="async-worker",
            daemon=True,
        )
        self._thread.start()

    def _run_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def run(self, coro: Coroutine[Any, Any, T]) -> T:
        """
            Runs a coroutine on the background event loop and
            blocks until it completes.

            Params:
                - coro: The coroutine to execute.

            Returns:
                - The result of the coroutine.
        """

        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return future.result()

    def stop(self):
        """
            Stops the background event loop and joins the worker thread.
        """

        self._loop.call_soon_threadsafe(self._loop.stop)
        self._thread.join()

#
#   Bootstrap the async worker
#

@st.cache_resource
def bootstrap_async_worker() -> AsyncWorker:
    return AsyncWorker()
