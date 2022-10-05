import pickle as pkl
from config import TimingTable


def save_object_using_pickle(output_path: str, object: TimingTable) -> None:
    with open(output_path, "wb") as f:
        pkl.dump(object, f)


def open_object_using_pickle(input_path: str) -> TimingTable:
    with open(input_path, "rb") as f:
        return pkl.load(f)
