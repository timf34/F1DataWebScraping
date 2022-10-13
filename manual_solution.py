import asyncio
import itertools
import json
import sys
import time
import tkinter as tk

from copy import deepcopy
from itertools import zip_longest
from typing import List, Dict, Generator, Union, Tuple

from utils import find_indices_of_string, get_initialized_car_timing_dict, get_initialized_car_sector_dict, open_json_as_dict, create_a_larger_extrapolated_x_y_axis, get_initializied_car_dict_no_generator
from send_mqtt import SendTimingTableToMQTT


class ManualSolution:
    def __init__(self):
        self.action_baselines: Dict = open_json_as_dict("data/okayama_action_baselines.json")
        self.car_sector_timings: Dict = get_initializied_car_dict_no_generator()
        self.temp_json_path: str = "data/temp.json"

    def read_input(self) -> Dict[str, str]:
        """
            This function reads in the user input and returns a list of tuples.
            The first element of the tuple is the car number, and the second element is the sector time.
        """
        temp_dict = {"car_num": "", "S1": ""}

        # Prompt the user
        print("Please enter the following separated by spaces: car_number S1 s2 s3, s4 and gap_to_leader")
        print("However, while we are just practicing, just enter car number and S2")

        # Read in the user input
        user_input = input()

        # Split the user input into a list of tuples
        user_input = user_input.split(" ")
        temp_dict["car_num"] = user_input[0]
        temp_dict["S1"] = user_input[1]
        return temp_dict


    def read_file_continuously(self):
        while True:
            with open(self.temp_json_path, "r") as f:
                print(json.load(f))
                time.sleep(0.25)

    def get_action_baselines(self, sector: str = None, sector_time: str = None) -> Dict:
        """
            This function iterates will return the actionBaselines dict that we will store in self.update_car_dict.

            We can adjust the underlying dict here using the sector and sector_time args when we are ready.
        """
        for sector_num, action_baseline in self.action_baselines.items():
            print(f"Sector number: {sector_num}, Sector time: {action_baseline}")

        # Note: going forward I would adjust (i.e. expand/ contract) the baselines within this function
        return self.action_baselines

    def update_car_dict(self, car_num: str, sector: str, sector_time: str):
        """
            This function updates the car dict with the new sector time.

            This is where we will feed any input we get from the user.

            This creates a dict of the form {"104": {"S1": {"Brake": [0, ...], "Speed": [1,...], ...}, "S2": {...}},
                                             "11": {...}}

        :param car_num: The car number
        :param sector: The sector number
        :param sector_time: The sector time
        """
        self.car_sector_timings[car_num] = deepcopy(self.get_action_baseline(sector, sector_time))
        self.car_sector_timings[car_num]["sector"] = sector
        self.car_sector_timings[car_num]["action_baselines"] = sector_time


def main():
    manual_solution = ManualSolution()
    # manual_solution.read_input()
    manual_solution.read_file_continuously()
    # manual_solution.get_action_baselines()


if __name__ == "__main__":
    main()

