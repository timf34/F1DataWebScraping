import pickle as pkl
from config import TimingTable
from typing import List


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