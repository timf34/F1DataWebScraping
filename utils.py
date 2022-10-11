from copy import deepcopy
import json
import numpy as np
import os

import pickle as pkl
from config import TimingTable
from typing import List, Dict, Generator, Union, Tuple


def open_json_as_dict(input_path: str) -> Dict:
    # Ensure file exists
    if not os.path.exists(input_path):
        raise Exception(f"File does not exist: {input_path}")

    with open(input_path, "r") as f:
        return json.load(f)


def save_object_using_pickle(output_path: str, object: TimingTable) -> None:
    with open(output_path, "wb") as f:
        pkl.dump(object, f)


def open_object_using_pickle(input_path: str) -> TimingTable:
    with open(input_path, "rb") as f:
        return pkl.load(f)


def find_indices_of_string(_list: List, string: str) -> List[int]:
    """
    This finds the indices of a string in a list

    Note: "\n" occurs at every 21st index -> i.e. [20, 41, 62...,1070]
    """
    return [index for index, i in enumerate(_list) if i == string]


def get_initialized_car_timing_dict() -> Dict[str, Dict[str, float]]:
    """
    This creates a dictionary of the timing table
    """
    car_timing_dict: Dict[str, Dict[str, float]] = {}

    # We have hardcoded the car numbers into a txt file for now
    # TODO: this won't work on EC2 if we get it up there!
    with open(r"C:\Users\timf3\PycharmProjects\F1DataWebScraping\data\car_nums.txt", "r") as f:
        car_nums = f.readlines()

    # Just initalize the sector times to 0 for now
    for car_num in car_nums:
        # TODO: need to be careful with the Type here. Should I keep it as a float?
        car_timing_dict[car_num.replace("\n", "")] = {"S1": "0.", "S2": "0.", "S3": "0.", "S4": "0."}

    # print(car_timing_dict)
    return car_timing_dict


def get_initialized_car_sector_dict() -> Dict[str, Dict[str, Union[str, Generator]]]:
    """
        This creates a dict to keep track of the sector the car most recently finished
    """
    car_sector_dict: Dict[str, Dict[str, str]] = {}

    with open(r"C:\Users\timf3\PycharmProjects\F1DataWebScraping\data\car_nums.txt", "r") as f:
        car_nums = f.readlines()

    def gen():
        yield "empty temp generator"

    for car_num in car_nums:
        car_sector_dict[car_num.replace("\n", "")] = {"sector": "0.", "generator": gen()}

    return car_sector_dict


def create_a_larger_extrapolated_x_y_axis(x: List[float], y: List[float], difference: float) -> Tuple[List[float], List[float]]:
    """
        This function takes in a list of x and y values and returns a new list of x and y values where the x-axis
        is 2 seconds longer, and matches the y-axis values accordingly.
    """
    interval = 0.25
    # Add the difference (in time) to the last value of x.
    x[-1] += difference # This works for adding or subtracting!

    # Create a new list of x values with this new interval
    new_x = np.arange(x[0], x[-1] + interval, interval)

    # Change the number of elements in y to match the number of elements in x
    new_y = np.interp(np.linspace(0, len(y) - 1, len(new_x)), np.arange(len(y)), y)

    return new_x, new_y


def main():
    # x = get_initialized_car_sector_dict()
    # print(x)

    x = open_json_as_dict("data/okayama_action_baselines.json")
    print(type(x["S1"]["S1SecondTiming"][2]))


if __name__ == "__main__":
    main()
