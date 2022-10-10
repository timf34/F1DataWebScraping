import pickle as pkl
from config import TimingTable
from typing import List, Dict


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
    with open("../data/car_nums.txt", "r") as f:
        car_nums = f.readlines()

    # Just initalize the sector times to 0 for now
    for car_num in car_nums:
        car_timing_dict[car_num.replace("\n", "")] = {"S1": 0., "S2": 0., "S3": 0., "S4": 0.}

    # print(car_timing_dict)
    return car_timing_dict
