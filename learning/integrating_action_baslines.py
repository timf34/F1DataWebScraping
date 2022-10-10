import sys

from typing import List, Dict, Generator

# Import from the utils.py file in the parent directory
sys.path.append("..")
from utils import find_indices_of_string, get_initialized_car_timing_dict

# Note: I believe I am going with the OkayamaDatset project to stream everything.


class ActionsBaseline:
    def __init__(self):
        # This is the web scraped short list... just hardcoding for now for testing.
        self.short_list = ['104', '169.1', '', '', '', '', '', '', '', "2'23.911", '36.344', '38.589', '37.780', '31.198', '\n', '11', '', '', '', '', '', '', '', '', "2'27.173", '37.444', '39.418', '\\xa0', '\\xa0', '\n', '111', '212.6', '', '', '', '', '', '', '', "2'10.381", '33.680', '34.850', '33.452', '28.399', '\n', '12', '', '', '', '', '', '', '', '', "2'28.173", '36.845', '39.326', '\\xa0', '\\xa0', '\n', '13', '101.4', '', '', '', '', '', '', '', "2'21.319", '34.471', '37.027', '36.595', '33.226', '\n', '16', '', '', '', '', '', '', '', '', "1'59.846", '29.650', '32.489', '\\xa0', '\\xa0', '\n', '17', '133.7', '', '', '', '', '', '', '', "2'24.351", '36.905', '38.615', '37.480', '31.351', '\n', '18', '181.2', '', '', '', '', '', '', '', "2'21.566", '35.741', '38.169', '37.430', '30.226', '\n', '19', '105.4', '', '', '', '', '', '', '', "2'10.971", '33.336', '35.223', '33.805', '28.607', '\n', '2', '122.9', '', '', '', '', '', '', '', "2'08.129", '33.319', '33.656', '32.265', '28.889', '\n', '21', '125.2', '', '', '', '', '', '', '', "2'06.313", '32.145', '33.933', '\\xa0', '\\xa0', '\n', '216', '180.3', '', '', '', '', '', '', '', "2'20.060", '35.105', '37.252', '36.638', '31.065', '\n', '22', '129.7', '', '', '', '', '', '', '', "2'06.256", '32.093', '34.544', '32.379', '27.240', '\n', '222', '131.9', '', '', '', '', '', '', '', "2'29.243", '37.333', '39.287', '\\xa0', '\\xa0', '\n', '225', '195.0', '', '', '', '', '', '', '', "2'17.510", '34.091', '36.116', '35.043', '32.260', '\n', '23', '117.9', '', '', '', '', '', '', '', "1'57.915", '\\xa0', '\\xa0', '30.398', '25.515', '\n', '244', '216.0', '', '', '', '', '', '', '', "2'07.485", '32.719', '34.090', '32.796', '27.880', '\n', '28', '190.2', '', '', '', '', '', '', '', "2'17.735", '34.532', '36.367', '35.749', '31.087', '\n', '3', '216.9', '', '', '', '', '', '', '', "2'05.106", '31.677', '33.586', '32.789', '27.054', '\n', '31', '232.3', '', '', '', '', '', '', '', "1'59.516", '30.584', '31.768', '31.100', '26.064', '\n', '310', '212.6', '', '', '', '', '', '', '', "2'10.562", '32.404', '34.410', '33.216', '30.532', '\n', '32', '94.9', '', '', '', '', '', '', '', "2'21.407", '36.127', '38.323', '36.604', '30.353', '\n', '34', '203.8', '', '', '', '', '', '', '', "2'07.392", '32.162', '34.067', '33.158', '28.005', '\n', '37', '165.4', '', '', '', '', '', '', '', "2'28.514", '36.965', '39.526', '38.262', '33.761', '\n', '38', '217.3', '', '', '', '', '', '', '', "2'04.204", '31.528', '33.367', '32.388', '26.921', '\n', '4', '170.9', '', '', '', '', '', '', '', "2'25.696", '37.115', '39.231', '38.344', '31.006', '\n', '47', '223.6', '', '', '', '', '', '', '', "2'06.404", '31.780', '33.591', '32.500', '28.533', '\n', '50', '167.2', '', '', '', '', '', '', '', "2'28.237", '37.279', '39.725', '38.997', '32.236', '\n', '500', '162.9', '', '', '', '', '', '', '', "2'06.838", '31.975', '34.017', '\\xa0', '\\xa0', '\n', '55', '106.2', '', '', '', '', '', '', '', "2'26.105", '36.654', '38.980', '38.412', '32.059', '\n', '56', '115.7', '', '', '', '', '', '', '', "2'23.939", '35.203', '38.507', '38.069', '32.160', '\n', '59', '62.6', '', '', '', '', '', '', '', "2'18.504", '35.330', '54.085', "1'09.625", '\\xa0', '\n', '6', '99.8', '', '', '', '', '', '', '', "2'17.984", '34.068', '35.967', '35.309', '32.640', '\n', '60', '', '', '', '', '', '', '', '', "2'20.107", '35.685', '37.420', '\\xa0', '\\xa0', '\n', '61', '191.5', '', '', '', '', '', '', '', "2'14.133", '33.830', '36.059', '35.453', '28.791', '\n', '62', '233.8', '', '', '', '', '', '', '', "1'57.178", '29.671', '31.506', '30.428', '25.573', '\n', '65', '', '', '', '', '', '', '', '', "2'27.869", '37.097', '39.463', '\\xa0', '\\xa0', '\n', '66', '', '', '', '', '', '', '', '', "2'26.196", '36.751', '40.872', '\\xa0', '\\xa0', '\n', '67', '159.1', '', '', '', '', '', '', '', "2'25.966", '36.827', '38.930', '38.402', '31.807', '\n', '7', '86.7', '', '', '', '', '', '', '', '\\xa0', "1'00.982", '40.156', "1'20.664", '\\xa0', '\n', '72', '76.6', '', '', '', '', '', '', '', "2'24.098", '36.265', '38.745', '37.721', '31.367', '\n', '743', '99.3', '', '', '', '', '', '', '', "2'17.120", '34.450', '36.116', '34.833', '31.721', '\n', '75', '136.9', '', '', '', '', '', '', '', "2'11.737", '32.789', '34.435', '34.534', '29.979', '\n', '777', '229.3', '', '', '', '', '', '', '', "1'56.964", '29.837', '31.169', '30.646', '25.312', '\n', '81', '233.3', '', '', '', '', '', '', '', "1'57.170", '29.938', '31.446', '30.466', '25.320', '\n', '86', '141.4', '', '', '', '', '', '', '', "2'16.023", '34.214', '36.275', '35.891', '29.643', '\n', '88', '131.1', '', '', '', '', '', '', '', "2'28.547", '36.794', '39.299', '38.914', '33.540', '\n', '884', '', '', '', '', '', '', '', '', "2'18.287", '34.386', '36.645', '\\xa0', '\\xa0', '\n', '885', '213.1', '', '', '', '', '', '', '', "2'11.070", '32.562', '34.459', '33.848', '30.201', '\n', '888', '127.2', '', '', '', '', '', '', '', "1'59.628", '30.815', '32.613', '30.554', '25.646', '\n', '97', '207.7', '', '', '', '', '', '', '', "2'08.508", '32.507', '34.392', '33.706', '27.903', '\n']
        self.car_timing_dict = get_initialized_car_timing_dict()
        self.sectors: List[str] = ["S1", "S2", "S3", "S4"]

    def car_iterator(self, short_list: List[str]) -> Generator[List[str], None, None]:

        first_backslash_n = find_indices_of_string(short_list, "\n")[0]

        for i in find_indices_of_string(_list=self.short_list, string="\n"):
            yield short_list[i - first_backslash_n:i]  # This is a List with the info for one car

    def parse_sector_timing(self):
        for count, car in enumerate(self.car_iterator(self.short_list)):
            print(car)

            # Let's just practice on the first car for now.
            if count == 0:
                break

    def compare_scraped_data_with_car_timing_dict(self) -> List[str]:
        """
        This function compares the SectorTiming values from the scrapred data, to the values stored in the car_timing_dict.
        If the values are different, the car_timing_dict is updated, and we add the car_numer and sector to a stack.
        """
        _stack = []

        for count, car in enumerate(self.car_iterator(self.short_list)):
            car_num = car[0]
            for sector in self.sectors:
                scraped_data = car[self.sectors.index(sector) + 10]
                if scraped_data != str(self.car_timing_dict[car_num][sector]):
                    # print(f"scraped_data {scraped_data} != self.car_timing_dict[car_num][sector] {self.car_timing_dict[car_num][sector]}")
                    # print(f"Updated car_num {car_num} {sector} to {scraped_data}")
                    self.car_timing_dict[car_num][sector] = str(scraped_data)
                    _stack.append((car_num, sector))

        return _stack

    def start_streaming_from_stack(self, _stack) -> None:
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
                    print(f"Sending {_stack[i][0]} {_stack[i][1]}")
                    # self.mqtt_sender.publish_to_topic(f"{_stack[i][0]} {_stack[i][1]}")
            else:
                print(f"Sending last one! {_stack[i][0]} {_stack[i][1]}")

            length -= 1
            _stack.pop(i)


def main():
    actions_baslines = ActionsBaseline()
    # actions_baslines.parse_sector_timing()
    # print(actions_baslines.car_timing_dict)
    # print(actions_baslines.compare_scraped_data_with_car_timing_dict())
    actions_baslines.start_streaming_from_stack(actions_baslines.compare_scraped_data_with_car_timing_dict())


if __name__ == "__main__":
    main()
