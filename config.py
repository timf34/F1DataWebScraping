from dataclasses import dataclass
from typing import List, Dict, Union


@dataclass
class TimingTable:
    """
    This is a dataclass for the timing table
    """
    # TODO: this is definitely bad practice. Sort this out later.

    position: int = None
    pic: int = None  # Not sure what this is tbh
    car_num: int = None
    _class: str = None
    laps: int = None
    dr: str = None  # Not sure what this is... samples include A, B, C and D...?
    driver_name: str = None
    machine_name: str = None  # Seems to tbe the team name?
    last_lap_time: str = None  # This is a string because it can be "DNF" or "LAP"
    best_lap_time: str = None
    gaps: str = None
    int_full_stop: str = None  # Not sure what this is
    s1: str = None
    s2: str = None
    s3: str = None
    s4: str = None
    speed: str = None
    in_pit: bool = None
    pit: int = None
    last_pit: int = None

    def to_dict(self) -> Dict:
        """
        This converts the dataclass to a dictionary
        """
        return self.__dict__

    def __setitem__(self, key, value):
        """
        This allows the dataclass to be accessed by index
        """
        if isinstance(key, str):
            self.__dict__[key] = value
        elif isinstance(key, int):
            # We can set a value using an int index
            # This is a bit hacky but it works
            # We can't use the __dict__ because the keys are not valid python identifiers
            # So we have to use the __dict__ to get the keys and then use the __dict__ to set the values
            keys = list(self.__dict__.keys())
            self.__dict__[keys[key]] = value
        else:
            raise TypeError("Key must be a string or an int")


def main() -> None:
    """
    This is the main function
    """

    x = TimingTable(position=1,
                    pic=1,
                    car_num=888,
                    _class="4",
                    laps=5,
                    dr="6",
                    driver_name="Joe",
                    machine_name="Joe the Machine",
                    last_lap_time="9",
                    best_lap_time="10",
                    gaps="",
                    int_full_stop="",
                    s1="13",
                    s2="14",
                    s3="15",
                    s4="16",
                    speed="17",
                    in_pit=True,
                    pit=18,
                    last_pit=19)
    print(x)

    x[18] = 5
    print(x)
    # print(type(x.__annotations__))
    # for i in x.__annotations__:
    #     print(i)

if __name__ == "__main__":
    main()
