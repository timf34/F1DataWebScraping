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
        # TODO: need to be careful with the Type here. Should I keep it as a float?
        car_timing_dict[car_num.replace("\n", "")] = {"S1": "0.", "S2": "0.", "S3": "0.", "S4": "0."}

    # print(car_timing_dict)
    return car_timing_dict


def quick_test():
    x = [("a", 1), ("a", 2), ("b", 3), ("c", 4)]

    for index, i in enumerate(x):
        _char = i[0]
        if index < len(x) - 1:
            next_char = x[index + 1][0]
            if _char != next_char:
                print("Not equal - this is the last one", i)
                x.pop(0)
            else:
                print("Equal")
                x.pop(0)
                # x = x[index + 1:]
        else:
            print("This is the last one", i)
            x.pop(0)

    print(x)

    print("\nnew method")

    x = [("a", 1), ("a", 2), ("b", 3), ("c", 4)]
    length = len(x)
    i = 0
    while i < length:
        if i < length - 1:
            if x[i][0] != x[i + 1][0]:
                print("Not equal babe", x[i])
                x.pop(i)
                length -= 1
            else:
                print("Equal")
                x.pop(i)
                length -= 1

        else:
            print("This is the last one", x[i])
            print("here is the whole list: ", x)
            x.pop()
            length -= 1

    print("and here dawg", x)





def main():
    quick_test()


if __name__ == "__main__":
    main()
