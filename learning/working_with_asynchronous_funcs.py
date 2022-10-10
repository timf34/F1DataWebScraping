import asyncio
import time

class WorkingWIthAsyncFuncs:
    """
        This is just a class for practice.

        We need to have one function running continuously in the background, while we do other things.

        This continuously running function needs to print "yolo" to the terminal.

        Our other function, which is not continuous/ asynchronous, needs to print "hello world" to the terminal after
        a delay of 5 seconds.
    """
    def __init__(self):
        self._loop = asyncio.get_event_loop()
        self._loop.create_task(self._async_func())
        self._loop.run_until_complete(self._non_async_func())

    async def _async_func(self):
        while True:
            print("yolo")
            await asyncio.sleep(1)

    async def _non_async_func(self):
        await asyncio.sleep(5)
        print("hello world")


if __name__ == "__main__":
    WorkingWIthAsyncFuncs()
