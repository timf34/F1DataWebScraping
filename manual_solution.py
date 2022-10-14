import asyncio
import itertools
import json
import sys
import time
import tkinter as tk

from copy import deepcopy
from itertools import zip_longest
from typing import List, Dict, Generator, Union, Tuple

from utils import find_indices_of_string, get_initialized_car_timing_dict, get_initialized_car_sector_dict, open_json_as_dict, create_a_larger_extrapolated_x_y_axis
from send_mqtt import SendTimingTableToMQTT


class ManualSolution:
    def __init__(self):
        self.action_baselines: Dict = open_json_as_dict("data/okayama_action_baselines.json")
        self.car_timing_dict: Dict = get_initialized_car_timing_dict()
        self.car_sector_dict: Dict = get_initialized_car_sector_dict()
        self.temp_json_path: str = "data/manual_soln_dict.json"

        self.car_info_list = []  # Continuously read from the file
        self.sectors: List[str] = ["S1", "S2", "S3", "S4"]
        self.actions: List[str] = ["Brake", "Throttle", "Speed", "RPM", "Gear"]
        self.sector_baseline_times = {"S1": 29.5, "S2": 25.75, "S3": 36.25, "S4": 17.25}

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

    def read_file_continuously(self, not_continuous: bool = False) -> None:
        """
        Convert data from the json file, into a list of strings. Each car is separated by "\n"
        :return:
        """
        while True:
            temp_list = []
            with open(self.temp_json_path, "r") as f:
                temp_dict = json.load(f)
                for car_num in temp_dict["car_number"]:
                    temp_list.append(car_num)
                    temp_list.extend([temp_dict["car_number"][car_num][-1]]) # Speed
                    temp_list.extend(['', '', '', '', '', '', '', '', temp_dict["car_number"][car_num][0], temp_dict["car_number"][car_num][1], temp_dict["car_number"][car_num][2], temp_dict["car_number"][car_num][3], temp_dict["car_number"][car_num][4]]) # Sector times
                    temp_list.extend("\n")
                time.sleep(0.2)

            self.car_info_list = deepcopy(temp_list)
            print(self.car_info_list)
            if not_continuous:
                return

    def iterate_car_sector_timings(self) -> None:
        print(self.car_sector_dict)
        print(self.car_timing_dict)

    def car_iterator(self) -> Generator[List[str], None, None]:
        """
        This func parses the scraped data (a list of strings, with each car separted by "\n") and yields a list of each
        each car's data (as a generator!)
        :param short_list:
        :param use_live_list:
        :return:
        """
        _list = self.car_info_list

        first_backslash_n = find_indices_of_string(_list, "\n")[0]

        for i in find_indices_of_string(_list=_list, string="\n"):
            yield _list[i - first_backslash_n:i]  # This is a List with the info for one car

    def compare_scraped_data_with_car_timing_dict(self) -> List[Tuple[str]]:
        """
        This function compares the SectorTiming values from the scraped data, to the values stored in the car_timing_dict.
        If the values are different, the car_timing_dict is updated, and we add the car_number and sector to a stack.
        """
        print("We are in the start of compare_scraped_data_with_car_timing_dict, time:", time.ctime())
        _stack = []

        for car in self.car_iterator():
            car_num = car[0]
            for sector in self.sectors:
                scraped_data = car[self.sectors.index(sector) + 10]  # This gets the time for a specific sector. We only compare the sector times.
                if scraped_data != str(self.car_timing_dict[car_num][sector]):
                    self.car_timing_dict[car_num][sector] = str(scraped_data)
                    _stack.append((car_num, sector, car[1], car[9], car[10:14])) # Car number, sector, gap lead time, last lap time, sector times (S1, S2, S3, S4) (for expandnig/ contracting)
                    # Current format: (car num, sector, gap to leader, "", [S1, S2, S3, S4])
        return _stack

    def iterate_through_stack(self, _stack) -> None:
        """
        This function uses the stack to start streaming data to our MQTT topic - it sends the last sector present for
        each car number, removing the car number and previous sectors (if there's multiple) once its been sent.

        It iterates through the stack, while the car_num is the same.
        """
        length = len(_stack)
        i = 0
        while i < length:
            if i < length - 1:
                if _stack[i][0] != _stack[i + 1][0]:

                    next_sector = self.sectors[self.sectors.index(_stack[i][1]) + 1] if _stack[i][1] != "S4" else "S1"

                    # Note: _stack[i][4] is a list of the sector times. We will match the time with the sector number.
                    sector_time = _stack[i][4][self.sectors.index(next_sector)]

                    self.update_car_sector_dict(_stack[i][0], next_sector, deepcopy(_stack[i][2]), deepcopy(_stack[i][3]), sector_time)  #_stack[i][0] is the car number, next_sector is the next nexsector, _stack[i][2] is the gap lead time, _stack[i][3] is the last lap time.
            else:
                print(f"Sending last one! {_stack[i][0]} {next_sector}")
                sector_time = _stack[i][4][self.sectors.index(next_sector)]
                self.update_car_sector_dict(_stack[i][0], next_sector, deepcopy(_stack[i][2]), deepcopy(_stack[i][3]), sector_time)

            length -= 1
            _stack.pop(i)  # Empties the _stack (although we didn't strictly need to here)

    def update_car_sector_dict(self, car_number: Union[str, int], sector: str, gap_lead_time: str, last_lap_time: str,
                               sector_time: str) -> None:
        """
        This function starts the streaming of data to our MQTT topic.
        """
        # Check if car_number is int
        if isinstance(car_number, int):
            car_number = str(car_number)

        # Check if sector is equal to the relevant value in self.car_sector_dict. If not, update + add new generator
        if sector != self.car_sector_dict[car_number]["sector"]:
            # We can't use deepcopy with generators, so we can just leave it as is for the time being. It should work.
            self.car_sector_dict[car_number]["sector"] = sector
            self.car_sector_dict[car_number]["generator"] = self.yield_list(sector, car_number,
                                                                            sector_time=sector_time)  # TODO: its here that I can probably add the gap lead timing, and most recent lap time. It will be static/ only updated every sector.
            self.car_sector_dict[car_number]["gap_lead_time"] = gap_lead_time
            self.car_sector_dict[car_number]["last_lap_time"] = last_lap_time

    def yield_list(self, sector: str, car_number: str, sector_time: str, basic: bool = False) -> Generator[List[str], None, None]:
        """
            Yields from self.action_baselines

            This contracts/ exapands the baseline for the generator.
        :param sector:
        :param car_number:
        :param sector_time:
        :param basic:
        :return:
        """

        temp_dict = deepcopy(self.action_baselines)
        # Convert sector_time to a float

        # Now we get the difference between the last sector time and the baseline sector time
        try:
            difference = float(sector_time) - float(self.sector_baseline_times[sector])
        except Exception:
            print(f"Wasn't able to find the time delta between baseline and car_number {car_number}, the sector time was {sector_time}")
            difference = 0

        for action in self.actions:
            temp_dict[sector][f"{sector}SecondTiming"], temp_dict[sector][action] = create_a_larger_extrapolated_x_y_axis(temp_dict[sector][f"{sector}SecondTiming"], temp_dict[sector][action], difference)

        if sector:
            if basic:
                while True:
                    yield [sector]
            else:
                if isinstance(sector, int):
                    sector = f"S{sector}"
                # Ensure that sector_number is a valid sector (i.e. ["S1", "S2", "S3", "S4"])
                if sector not in self.action_baselines:
                    raise KeyError(
                        f"Invalid sector number: {sector}. Must be one of: {list(self.action_baselines.keys())}")

                temp_actions = deepcopy(self.actions)
                temp_actions.append(f"{sector}SecondTiming")

                # Yields the data from the action baselines...
                temp_dict = deepcopy(temp_dict)
                for i in zip(*[temp_dict[sector][action] for action in temp_actions]):
                    yield [car_number, i[2], i[1], i[0], i[3], i[4], "", "", "", "", "\n"]  # Car_num, speed, throttle, brake, rpm, gear, leader_gap, position_ahead_gap, updated, most_recent_lap_time
        else:
            while True:
                yield ["no sector... huh?"]

    def start_streaming(self) -> None:
        gen_list = []
        for i in self.car_sector_dict:
            print(f"Starting streaming for car {i}")
            try:
                print(f"yas bitches its car number {i}: ", self.car_sector_dict[i]["generator"].__next__())
            # If we want to prevent StopIteration now we should...
                gen_list.extend(self.car_sector_dict[i]["generator"].__next__())
            except StopIteration:
                print(f"We have reached the end of car number {i} for this sector")


def main():
    manual_solution = ManualSolution()
    # manual_solution.read_input()
    manual_solution.read_file_continuously(not_continuous=True)
    # manual_solution.iterate_car_sector_timings()
    manual_solution.iterate_through_stack(manual_solution.compare_scraped_data_with_car_timing_dict())

    while True:
        manual_solution.start_streaming()
        time.sleep(0.1)


if __name__ == "__main__":
    main()

