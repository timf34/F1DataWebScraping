import asyncio
import itertools
import sys
import time


from copy import deepcopy
from itertools import zip_longest
from typing import List, Dict, Generator, Union

# Import from the utils.py file in the parent directory
sys.path.append("")
from utils import find_indices_of_string, get_initialized_car_timing_dict, get_initialized_car_sector_dict, open_json_as_dict, create_a_larger_extrapolated_x_y_axis
from send_mqtt import SendTimingTableToMQTT
from super_taikyu_scraping import LiveOrchestrator

# Note: I believe I am going with the OkayamaDatset project to stream everything.

STREAMING_DELAY = 0.23


class ActionsBaseline:
    def __init__(self):
        # This is the web scraped short list... just hardcoding for now for testing.
        self.hardcoded_list = ['104', '169.1', '', '', '', '', '', '', '', "2'23.911", '36.344', '38.589', '37.780', '31.198', '\n', '11', '', '', '', '', '', '', '', '', "2'27.173", '37.444', '39.418', '\\xa0', '\\xa0', '\n', '111', '212.6', '', '', '', '', '', '', '', "2'10.381", '33.680', '34.850', '33.452', '28.399', '\n', '12', '', '', '', '', '', '', '', '', "2'28.173", '36.845', '39.326', '\\xa0', '\\xa0', '\n', '13', '101.4', '', '', '', '', '', '', '', "2'21.319", '34.471', '37.027', '36.595', '33.226', '\n', '16', '', '', '', '', '', '', '', '', "1'59.846", '29.650', '32.489', '\\xa0', '\\xa0', '\n', '17', '133.7', '', '', '', '', '', '', '', "2'24.351", '36.905', '38.615', '37.480', '31.351', '\n', '18', '181.2', '', '', '', '', '', '', '', "2'21.566", '35.741', '38.169', '37.430', '30.226', '\n', '19', '105.4', '', '', '', '', '', '', '', "2'10.971", '33.336', '35.223', '33.805', '28.607', '\n', '2', '122.9', '', '', '', '', '', '', '', "2'08.129", '33.319', '33.656', '32.265', '28.889', '\n', '21', '125.2', '', '', '', '', '', '', '', "2'06.313", '32.145', '33.933', '\\xa0', '\\xa0', '\n', '216', '180.3', '', '', '', '', '', '', '', "2'20.060", '35.105', '37.252', '36.638', '31.065', '\n', '22', '129.7', '', '', '', '', '', '', '', "2'06.256", '32.093', '34.544', '32.379', '27.240', '\n', '222', '131.9', '', '', '', '', '', '', '', "2'29.243", '37.333', '39.287', '\\xa0', '\\xa0', '\n', '225', '195.0', '', '', '', '', '', '', '', "2'17.510", '34.091', '36.116', '35.043', '32.260', '\n', '23', '117.9', '', '', '', '', '', '', '', "1'57.915", '\\xa0', '\\xa0', '30.398', '25.515', '\n', '244', '216.0', '', '', '', '', '', '', '', "2'07.485", '32.719', '34.090', '32.796', '27.880', '\n', '28', '190.2', '', '', '', '', '', '', '', "2'17.735", '34.532', '36.367', '35.749', '31.087', '\n', '3', '216.9', '', '', '', '', '', '', '', "2'05.106", '31.677', '33.586', '32.789', '27.054', '\n', '31', '232.3', '', '', '', '', '', '', '', "1'59.516", '30.584', '31.768', '31.100', '26.064', '\n', '310', '212.6', '', '', '', '', '', '', '', "2'10.562", '32.404', '34.410', '33.216', '30.532', '\n', '32', '94.9', '', '', '', '', '', '', '', "2'21.407", '36.127', '38.323', '36.604', '30.353', '\n', '34', '203.8', '', '', '', '', '', '', '', "2'07.392", '32.162', '34.067', '33.158', '28.005', '\n', '37', '165.4', '', '', '', '', '', '', '', "2'28.514", '36.965', '39.526', '38.262', '33.761', '\n', '38', '217.3', '', '', '', '', '', '', '', "2'04.204", '31.528', '33.367', '32.388', '26.921', '\n', '4', '170.9', '', '', '', '', '', '', '', "2'25.696", '37.115', '39.231', '38.344', '31.006', '\n', '47', '223.6', '', '', '', '', '', '', '', "2'06.404", '31.780', '33.591', '32.500', '28.533', '\n', '50', '167.2', '', '', '', '', '', '', '', "2'28.237", '37.279', '39.725', '38.997', '32.236', '\n', '500', '162.9', '', '', '', '', '', '', '', "2'06.838", '31.975', '34.017', '\\xa0', '\\xa0', '\n', '55', '106.2', '', '', '', '', '', '', '', "2'26.105", '36.654', '38.980', '38.412', '32.059', '\n', '56', '115.7', '', '', '', '', '', '', '', "2'23.939", '35.203', '38.507', '38.069', '32.160', '\n', '59', '62.6', '', '', '', '', '', '', '', "2'18.504", '35.330', '54.085', "1'09.625", '\\xa0', '\n', '6', '99.8', '', '', '', '', '', '', '', "2'17.984", '34.068', '35.967', '35.309', '32.640', '\n', '60', '', '', '', '', '', '', '', '', "2'20.107", '35.685', '37.420', '\\xa0', '\\xa0', '\n', '61', '191.5', '', '', '', '', '', '', '', "2'14.133", '33.830', '36.059', '35.453', '28.791', '\n', '62', '233.8', '', '', '', '', '', '', '', "1'57.178", '29.671', '31.506', '30.428', '25.573', '\n', '65', '', '', '', '', '', '', '', '', "2'27.869", '37.097', '39.463', '\\xa0', '\\xa0', '\n', '66', '', '', '', '', '', '', '', '', "2'26.196", '36.751', '40.872', '\\xa0', '\\xa0', '\n', '67', '159.1', '', '', '', '', '', '', '', "2'25.966", '36.827', '38.930', '38.402', '31.807', '\n', '7', '86.7', '', '', '', '', '', '', '', '\\xa0', "1'00.982", '40.156', "1'20.664", '\\xa0', '\n', '72', '76.6', '', '', '', '', '', '', '', "2'24.098", '36.265', '38.745', '37.721', '31.367', '\n', '743', '99.3', '', '', '', '', '', '', '', "2'17.120", '34.450', '36.116', '34.833', '31.721', '\n', '75', '136.9', '', '', '', '', '', '', '', "2'11.737", '32.789', '34.435', '34.534', '29.979', '\n', '777', '229.3', '', '', '', '', '', '', '', "1'56.964", '29.837', '31.169', '30.646', '25.312', '\n', '81', '233.3', '', '', '', '', '', '', '', "1'57.170", '29.938', '31.446', '30.466', '25.320', '\n', '86', '141.4', '', '', '', '', '', '', '', "2'16.023", '34.214', '36.275', '35.891', '29.643', '\n', '88', '131.1', '', '', '', '', '', '', '', "2'28.547", '36.794', '39.299', '38.914', '33.540', '\n', '884', '', '', '', '', '', '', '', '', "2'18.287", '34.386', '36.645', '\\xa0', '\\xa0', '\n', '885', '213.1', '', '', '', '', '', '', '', "2'11.070", '32.562', '34.459', '33.848', '30.201', '\n', '888', '127.2', '', '', '', '', '', '', '', "1'59.628", '30.815', '32.613', '30.554', '25.646', '\n', '97', '207.7', '', '', '', '', '', '', '', "2'08.508", '32.507', '34.392', '33.706', '27.903', '\n']
        self.car_timing_dict = get_initialized_car_timing_dict()
        self.car_sector_dict = get_initialized_car_sector_dict()
        self.sectors: List[str] = ["S1", "S2", "S3", "S4"]

        self.action_baselines: Dict = open_json_as_dict("data/okayama_action_baselines.json")
        self.actions: List[str] = ["Brake", "Throttle", "Speed", "RPM", "Gear"]

        self.loop = asyncio.get_event_loop()

        self.web_scraper = LiveOrchestrator(use_time_delay=True, our_loop=self.loop)  # We will use our own `await asyncio.sleep(1)` instead of the `time.sleep(1)` in the original code
        self.scraped_list = []

        self.mqtt_sender = SendTimingTableToMQTT()

        self.sector_baseline_times = {"S1": 29.5, "S2": 25.75, "S3": 36.25, "S4": 17.25}

    def car_iterator(self, short_list: List[str], use_live_list: bool = True) -> Generator[List[str], None, None]:

        print("car iterator", time.ctime(), short_list)
        first_backslash_n = find_indices_of_string(short_list, "\n")[0]

        _list = self.scraped_list if use_live_list else self.hardcoded_list

        for i in find_indices_of_string(_list=_list, string="\n"):
            yield short_list[i - first_backslash_n:i]  # This is a List with the info for one car

    def compare_scraped_data_with_car_timing_dict(self, use_live_list: bool = True) -> List[str]:
        """
        This function compares the SectorTiming values from the scrapred data, to the values stored in the car_timing_dict.
        If the values are different, the car_timing_dict is updated, and we add the car_numer and sector to a stack.
        """
        print("We are in the start of compaire_scraped_data_with_car_timing_dict, time:", time.ctime())
        _stack = []

        _list = self.scraped_list if use_live_list else self.hardcoded_list

        for count, car in enumerate(self.car_iterator(_list, use_live_list=True)):
            car_num = car[0]
            for sector in self.sectors:
                scraped_data = car[self.sectors.index(sector) + 10]  # This gets the time for a specific sector. We only compare the sector times.
                if scraped_data != str(self.car_timing_dict[car_num][sector]):
                    # print(f"scraped_data {scraped_data} != self.car_timing_dict[car_num][sector] {self.car_timing_dict[car_num][sector]}")
                    # print(f"Updated car_num {car_num} {sector} to {scraped_data}")
                    self.car_timing_dict[car_num][sector] = str(scraped_data)
                    # TODO: This is where I will also need to append sector timing data + gap lead time data.
                    # print("this is our car: ", car)
                    # print("here  is a given car... the scraped data is just the sector time. ", car)
                    # Note: we walso need the sector times here! So we can expand/ contract the data.
                    _stack.append((car_num, sector, car[6], car[9], car[10:14])) # Car number, sector, gap lead time, last lap time.
                    # print("and here is the _stack")

        return _stack

    def iterate_through_stack(self, _stack) -> None:
        """
        This function uses the stack to start streaming data to our MQTT topic - it sends the last sector present for
        each car number, removing the car number and previous sectors (if there's multiple) once its been sent.

        It iterates through the stack, while the car_num is the same.

        This implementation was kinda tricky cause we were deleting from the stack while iterating through it.
        In hindsight I realize we could have just deleted the list afterwards... ah well (I'm very tired still).
        I didn't even need to strictly delete the values from the list either!
        """
         # TODO: right now this just works with car_numer and sector number... next I need to add the timing so I can
         #  can stretch/ contract the data.

        length = len(_stack)
        i = 0
        while i < length:
            if i < length - 1:
                if _stack[i][0] != _stack[i + 1][0]:

                    # If _stack[i][1] is "S1", then we need to change it to "S2". If its "S2" -> "S3", etc. If its "S4" -> "S1"
                    next_sector = self.sectors[self.sectors.index(_stack[i][1]) + 1] if _stack[i][1] != "S4" else "S1"

                    print(f"Sending {_stack[i][0]} {next_sector} {_stack[i][2]} {_stack[i][3]}")

                    # Note: _stack[i][4] is a list of the sector times. We will match the time with the sector number.
                    sector_time = _stack[i][4][self.sectors.index(next_sector)]

                    self.update_car_sector_dict(_stack[i][0], next_sector, deepcopy(_stack[i][2]), deepcopy(_stack[i][3]), sector_time)  #_stack[i][0] is the car number, next_sector is the next nexsector, _stack[i][2] is the gap lead time, _stack[i][3] is the last lap time.
            else:
                print(f"Sending last one! {_stack[i][0]} {next_sector}")
                sector_time = _stack[i][4][self.sectors.index(next_sector)]
                self.update_car_sector_dict(_stack[i][0], next_sector, deepcopy(_stack[i][2]), deepcopy(_stack[i][3]), sector_time)

            length -= 1
            _stack.pop(i)  # Empties the _stack (although we didn't strictly need to here)

        # self.start_streaming()  # This needs to be asynchronous

    def update_car_sector_dict(self, car_number: Union[str, int], sector: str, gap_lead_time: str, last_lap_time: str, sector_time: str) -> None:
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
            self.car_sector_dict[car_number]["generator"] = self.yield_list(sector, car_number, sector_time=sector_time)  # TODO: its here that I can probably add the gap lead timing, and most recent lap time. It will be static/ only updated every sector.
            self.car_sector_dict[car_number]["gap_lead_time"] = gap_lead_time
            self.car_sector_dict[car_number]["last_lap_time"] = last_lap_time
            # print(f"We have updated car {car_number} to sector {sector} in our car_sector_dict: {self.car_sector_dict}")

    def yield_list(self, sector: str, car_number: str, sector_time: str, basic: bool = False) -> Generator[List[str], None, None]:

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
                # yield from zip(*[self.action_baselines[sector][action] for action in temp_actions])
                temp_dict = deepcopy(temp_dict)
                for i in zip(*[temp_dict[sector][action] for action in temp_actions]):
                    yield [car_number, i[2], i[1], i[0], i[3], i[4], "", "", "", "", "\n"]  # Car_num, speed, throttle, brake, rpm, gear, leader_gap, position_ahead_gap, updated, most_recent_lap_time
        else:
            while True:
                yield ["no sector... huh?"]

    async def scrape(self):  # This needs to be asynchronous. Async 1.1
        self.scraped_list = await self.web_scraper.async_run()
        print("here is our scraped list:", time.ctime(), self.scraped_list)

    def start_streaming(self) -> None:
        gen_list = []
        for i in self.car_sector_dict:
            print(f"Starting streaming for car {i}")
            # self.mqtt_sender.publish_to_topic(self.car_sector_dict[i]["generator"].__next__())
            # TODO: note that this doesn't raise a StopIteration error.
            try:
                print(f"yas bitches its car number {i}: ", self.car_sector_dict[i]["generator"].__next__())
            # If we want to prevent StopIteration now we should...
                gen_list.extend(self.car_sector_dict[i]["generator"].__next__())
            except StopIteration:
                print(f"We have reached the end of car number {i} for this sector")

        # for i in zip_longest(*gen_list):
        #     print(i)  # Come back to this.

    def async_start_streaming(self):
        print("We are in async_start_streaming at time: ", time.ctime())
        gen_list = []
        gap_lead_time_index = 6
        last_lap_time_index = 9
        for i in self.car_sector_dict:
            # print(f"Streaming car number {i}")
            try:
                car_info = self.car_sector_dict[i]["generator"].__next__()
            # print(f"yas bitches its car number {i}: ", car_info)
                gen_list.extend(car_info)  # Get the Okayama baseline info.
                # gen_list[gap_lead_time_index] = self.car_sector_dict[i]["gap_lead_time"]
                # gen_list[last_lap_time_index] = self.car_sector_dict[i]["last_lap_time"]
            except StopIteration:
                print(f"We have reached the end of car number {i} for this sector")
                # So lets make a copy of the generator, and get the last value from that to use instead
                # Note: its already spent here, I'll need to do something else... For now lets just default to 0 values!
                # copy_of_gen = itertools.tee(self.car_sector_dict[i]["generator"], 1)[0]
                # *_, last = copy_of_gen
                gen_list.extend((i, "", "", "", "", "", "", "", "", "", "\n"))  # Get the Okayama baseline info.

            gen_list[gap_lead_time_index] = self.car_sector_dict[i]["gap_lead_time"]
            gen_list[last_lap_time_index] = self.car_sector_dict[i]["last_lap_time"]
            gap_lead_time_index += 10
            last_lap_time_index += 10

        gen_list.extend(("timestamp", time.ctime()))
        print("this is the list btw and time", time.ctime(), gen_list)
        self.mqtt_sender.publish_to_topic(gen_list)

    async def scrape_and_process_data(self):
        while True:

            # We will print the time at the start and end of each of these functions, to try and see where the lag is.
            await self.scrape()  # This should be scraping every few seconds. "here is our list" will print when this is.
            # await asyncio.sleep(3)
            self.iterate_through_stack(self.compare_scraped_data_with_car_timing_dict(use_live_list=True))  # This part should be continuous. But follow after we scrape.  car_iterator will be called as this is!
            # await asyncio.sleep(1)

    async def stream_data(self):
        await asyncio.sleep(20)  # Initial sleep to allow web scraper to load stuff up. This could probs be shorter.
        while True:
            self.async_start_streaming()  # This should be near continuous. Just 0.25 seconds between each publish.
            await asyncio.sleep(STREAMING_DELAY)  # Note: this is the correct place. The above func iterates through all cars for a given timestamp.

    def _run(self):
        task_1 = self.loop.create_task(self.scrape_and_process_data())
        task_2 = self.loop.create_task(self.stream_data())

        self.loop.run_until_complete(asyncio.gather(task_1, task_2))
        self.loop.close()


def main():
    actions_baslines = ActionsBaseline()
    # actions_baslines.parse_sector_timing()
    # print(actions_baslines.car_timing_dict)
    # print(actions_baslines.compare_scraped_data_with_car_timing_dict())

    # actions_baslines.iterate_through_stack(actions_baslines.compare_scraped_data_with_car_timing_dict(use_live_list=False))

    actions_baslines._run()


if __name__ == "__main__":
    main()
