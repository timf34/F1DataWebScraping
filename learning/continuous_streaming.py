import asyncio
from copy import deepcopy
import time

from typing import Dict, List, Generator

# We will now use Generators to make this a continuous stream


class ContinuousStreaming:
    def __init__(self):
        self.sample_dict: Dict = {"S1": {"Brake": [1, 2, 3], "Throttle": [4, 5, 6], "Steering": [7, 8, 9]},
                                  "S2": {"Brake": [1, 2, 3], "Throttle": [4, 5, 6], "Steering": [7, 8, 9]},
                                  "S3": {"Brake": [1, 2, 3], "Throttle": [4, 5, 6], "Steering": [7, 8, 9]},
                                  "S4": {"Brake": [1, 2, 3], "Throttle": [4, 5, 6], "Steering": [7, 8, 9]}}

        self.sample_dict_with_nums: Dict[str, Dict] = {"1": deepcopy(self.sample_dict), "2": deepcopy(self.sample_dict)}

        self.sectors: List[str] = ["S1", "S2", "S3", "S4"]
        self.actions: List[str] = ["Brake", "Throttle", "Steering"]

    def loop_through_dict_forever(self) -> None:
        """
        This function loops through self.sample_dict on a loop forever. Iterating through S1, S2 ..., S4 and back again
        """

        while True:
            for sector in self.sectors:
                for action in self.actions:  # Brake -> Speed, etc.
                    for num in self.sample_dict_with_nums.keys():
                        print(num, action, sector, self.sample_dict_with_nums[num][sector][action])
                        time.sleep(0.1)

        # Lets rewrite the loop above, so that it iterates through the dict at each index for each action at the same
        # time (i.e. it steps through the indices of all the actions in order)
        # i.e. 1 Brake S1 1, 2 Brake S2 1, 1 Throttle

    def yield_list(self):
        temp_dict = deepcopy(self.sample_dict)

        for sector in self.sectors:
            for action in self.actions:
                for i in zip([*temp_dict[sector][action]]):
                    yield i, sector, action

    def print_yield_list(self):
        for i in self.yield_list():
            print(i)


def main():
    x = ContinuousStreaming()
    # x.loop_through_dict_forever()
    x.print_yield_list()


if __name__ == '__main__':
    main()