from dataclasses import dataclass
from typing import List, Dict, Union


@dataclass
class TimingTable:
    """
    This is a dataclass for the timing table
    """
    position: int
    pic: int  # Not sure what this is tbh
    car_num: int
    _class: str
    laps: int
    dr: str  # Not sure what this is... samples include A, B, C and D...?
    driver_name: str
    machine_name: str  # Seems to tbe the team name?
    last_lap_time: str  # This is a string because it can be "DNF" or "LAP"
    best_lap_time: str
    gaps: str
    int_full_stop: str  # Not sure what this is
    s1: str
    s2: str
    s3: str
    s4: str
    speed: str
    in_pit: bool
    pit: int
    last_pit: int

    def to_dict(self) -> Dict:
        """
        This converts the dataclass to a dictionary
        """
        return self.__dict__


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


if __name__ == "__main__":
    main()
