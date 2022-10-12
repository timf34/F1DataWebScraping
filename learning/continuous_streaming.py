import asyncio
import time

from typing import Dict, List



class ContinuousStreaming:
    def __init__(self):
        self.sample_dict: Dict = {"S1": {"Brake": [1, 2, 3], "Throttle": [4, 5, 6], "Steering": [7, 8, 9]},
                                  "S2": {"Brake": [1, 2, 3], "Throttle": [4, 5, 6], "Steering": [7, 8, 9]},
                                  "S3": {"Brake": [1, 2, 3], "Throttle": [4, 5, 6], "Steering": [7, 8, 9]},
                                  "S4": {"Brake": [1, 2, 3], "Throttle": [4, 5, 6], "Steering": [7, 8, 9]}}

        self.actions: List[str] = ["Brake", "Throttle", "Steering"]

    def loop_through_dict_forever(self) -> None:
        """
        This function loops through self.sample_dict on a loop forever. Iterating through S1, S2 ..., S4 and back again
        """
        while True:
            for key in self.sample_dict:
                # Loop through all the actions at once using unpacking and zip
                for action, values in zip(self.actions, self.sample_dict[key].values()):
                    print(action, values, key)
                    time.sleep(0.1)



def main():
    x = ContinuousStreaming()
    x.loop_through_dict_forever()


if __name__ == '__main__':
    main()