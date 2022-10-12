import asyncio
import time

from copy import deepcopy


class WorkingWIthAsyncFuncs:
    """
        This is just a class for practice.
        We need two asynchronous functions, with different delays. For now, they just print different things to the
        terminal
    """
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.shared_dict = {"a": 1, "b": 2}

    def run(self):
        self.loop.run_until_complete(self.async_func_1())
        self.loop.run_until_complete(self.async_func_2())
        self.loop.close()

    async def async_func_1(self):
        """
        We have set this up so that this function edits a copy of the shared dictionary, and then updates the shared
        one only when it's done.
        """

        print("Starting async_func_1")
        for _ in range(10):
            temp_dict = deepcopy(self.shared_dict)  # Make a copy of the shared dict
            temp_dict["a"] += 2  # Edit the copy
            await asyncio.sleep(1)
            temp_dict["b"] += 2
            print("Time before asyncio.sleep(4): ", time.time())
            await asyncio.sleep(4)
            print("Time after asyncio.sleep(4): ", time.time())
            # Update the shared dict once finished with the copy, and delete the copy
            # Note that we need to use deepcopy, as otherwise self.shared_dict would be updated with the changes to
            # temp_dict, and then temp_dict would be deleted! self.shared_dict would hold a reference to temp_dict.
            self.shared_dict = deepcopy(temp_dict)
            del temp_dict
        print("Finished async_func_1")

    async def async_func_2(self):
        while True:
            print("Starting async_func_2")
            self.print_info(self.shared_dict)
            await asyncio.sleep(0.5)
            print("Finished async_func_2")

    @staticmethod
    def print_info(string):
        print(f"{string}")

    def run_using_tasks(self):
        task_1 = self.loop.create_task(self.async_func_1())
        task_2 = self.loop.create_task(self.async_func_2())

        self.loop.run_until_complete(asyncio.gather(task_1, task_2))
        self.loop.close()

    def run_using_tasks_with_time(self):
        start_time = time.time()
        task_1 = self.loop.create_task(self.async_func_1())
        task_2 = self.loop.create_task(self.async_func_2())

        self.loop.run_until_complete(asyncio.gather(task_1, task_2))
        self.loop.close()
        print(f"Time taken: {time.time() - start_time}")


def first_main():
    working_with_async_funcs = WorkingWIthAsyncFuncs()
    print("Running using tasks")
    working_with_async_funcs.run_using_tasks_with_time()

    print("Running using run")
    # working_with_async_funcs.run()


if __name__ == "__main__":
    first_main()
