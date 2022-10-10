import bs4
import boto3
import time
import sys

from bs4 import BeautifulSoup
from dataclasses import asdict
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from typing import List, Union

from aws_keys import ACCESS_KEY, SECRET_ACCESS_KEY
from config import TimingTableCar, TimingTable
from utils import open_object_using_pickle, find_indices_of_string, get_initialized_car_timing_dict


class SuperTaikyuScraping:
    def __init__(self, use_local_html: bool = False, headless: bool = True):
        self.url: str = "https://www.supertaikyu.live/timings/"
        if use_local_html:
            self.html: str = open("data/supertaikyu.html", "r", encoding="utf-8").read()
        elif not headless:
            self.driver = webdriver.Edge()
            self.html: str = self.get_html_using_selenium()
        else:
            self.html = ""
            pass
            # raise NotImplementedError("Headless scraping is implemented in a child class")
        self.soup: BeautifulSoup = BeautifulSoup(self.html, "html.parser")

        self.tables: List[str] = self.soup.find_all("table")
        self.headless: bool = headless
        self.timing_table: bs4.ResultSet = self.soup.find_all("table", {"class": "table01", "id": "timing_table"})  # This will work for any of the id's in the tables

    def get_html_using_selenium(self, delay: int = 3) -> str:
        self.driver.get(self.url)
        time.sleep(delay)
        html = self.driver.page_source
        # Note: we are using headless mode solely for continuous updates here... although we could probs use it in general.
        if not self.headless:
            self.driver.close()
        return html

    def save_html(self) -> None:
        """
        This saves the html file to the current directory
        """
        with open("data/supertaikyu.html", "w", encoding="utf-8") as f:
            f.write(self.html)

    def save_soup(self) -> None:
        with open("data/supertaikyu_soup.txt", "w", encoding="utf-8") as f:
            f.write(self.soup.prettify())

    def print_soup(self) -> None:
        # print("html: \n", self.html)
        print("soup: \n", self.soup.prettify())

    def working_with_rows(self) -> None:
        for table in self.tables:
            rows = table.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                for col in cols:
                    print(col.text)  # Note that this will print blank lines when there is no text
                print("new row")

    def working_with_headers(self) -> None:
        for table in self.tables:
            headers = table.find_all("th")
            for header in headers:
                print(header.text)
            print("\nnew table")

    def get_timing_table(self, print_tables: bool = False ) -> TimingTable:

        # Initialize our table data store
        table_db: TimingTable = TimingTable()

        # Find all rows in self.timing_table[0] that contain the 'data-name' attribute
        rows = self.timing_table[0].find_all("tr", {"data-name": True})
        for row in rows:
            car_db = TimingTableCar()  # Initialize a new TimingTableCar
            cols = row.find_all("td")   # Find all columns in the row (all data cells within the row)
            for index, col in enumerate(cols):
                car_db[index] = col.text  # Add the text of the column to the TimingTableCar via the index
            table_db.cars[car_db.car_num] = car_db  # Add the car to the table, where the key is the car_number

        if print_tables:
            print(f"table_db.cars: \n {table_db.cars}")
            print(f"len(table_db.cars): {len(table_db.cars)}")

        if len(table_db.cars) == 0:
            print("No cars found in the table. Increase the delay in get_html_using_selenium()!")
        return table_db


class SuperTaikyuScrapingHeadless(SuperTaikyuScraping):
    def __init__(self, print_table: bool = False):
        super().__init__(headless=True)
        options = Options()
        options.headless = True
        self.driver = webdriver.Edge(options=options)
        self.print_table = print_table

    def continuous_update(self, print_time: bool = True) -> TimingTable:
        while True:
            self.html = self.get_html_using_selenium(delay=2)
            self.soup: BeautifulSoup = BeautifulSoup(self.html, "html.parser")
            self.timing_table: bs4.ResultSet = self.soup.find_all("table", {"class": "table01", "id": "timing_table"})
            table_db = self.get_timing_table(print_tables=self.print_table)
            if print_time:
                print("The time is: ", time.ctime())
            return table_db


class ConvertTimingTableToList:
    """
        This class is for converting the TimingTable object to a List object suitable for sending to our device
        via MQTT.
        This works for live timing data as well (i.e. straight from our web scraper) as from a pickle file.
    """
    def __init__(self, live_data: bool = False):
        self.timing_table: TimingTable = None if live_data else open_object_using_pickle("data/timing_table_object.pkl")

        # This is just for testing/ debugging purposes.
    def convert_timing_table_to_full_list(self, timing_table: TimingTable = None, list_of_lists: bool = False) -> Union[List[str], List[List[str]]]:
        """
           This function adds every item in TimingTable to a list, and returns the list. This list is too large for us
           though in its entirety, so we trim it down before sending to MQTT using the
           `convert_timing_table_to_short_list` function.
        """

        if self.timing_table is None:
            if timing_table is None:
                raise ValueError("Not passing a TimingTable object - we got None")
            else:
                self.timing_table = timing_table

        # Reinitialize self.timing_table_cars as the same dict but with the keys sorted alphabetically
        self.timing_table.cars = dict(sorted(self.timing_table.cars.items(), key=lambda item: item[0]))

        if list_of_lists:
            return [list(asdict(car).values()) for car in self.timing_table.cars.values()]
        else:
            # big_list = []
            # for car in self.timing_table.cars.values():
            #     big_list.extend(list(asdict(car).values()))
            #     big_list.extend("\n")
            # return big_list
            # Make a faster version of the above loop, including the newline (copilot is amazing)
            return [item for sublist in [[*asdict(car).values(), "\n"] for car in self.timing_table.cars.values()] for item in sublist]

    @staticmethod
    def convert_timing_table_to_short_list(full_list: List, print_info: bool = False) -> List:
        """
            This function takes the full list, and converts it to a shorter list, like the one in the OG F1 dataset.
            There will be some blank values where we don't have the info, there will also be blank values where we
            will merge data from the scraped data and the action baseline (i.e. braking, speed, rpm, etc.)
        """
        new_shorter_list = []
        temp_short_car = ['' for _ in range(15)]

        indices_we_want = [2, 16, 8, 12, 13, 14, 15]
        indices_we_want_to_fill = [0, 1, 9, 10, 11, 12, 13]

        first_backslash_n = find_indices_of_string(_list=full_list, string="\n")[0]

        for i in find_indices_of_string(_list=full_list, string="\n"):
            full_car = full_list[i - first_backslash_n:i]
            for retrieval_index, index_to_fill in zip(indices_we_want, indices_we_want_to_fill):
                temp_short_car[index_to_fill] = (full_car[retrieval_index])
                if print_info and full_car[retrieval_index] == '':
                    print(f"car number {full_car[2]} is missing index {index_to_fill}")
            temp_short_car[-1] = "\n"

            if print_info:
                print(temp_short_car)
            new_shorter_list.extend(temp_short_car)

        return new_shorter_list


class SendTimingTableToMQTT:
    def __init__(self, topic: str = "RACE/3"):
        self.access_key: str = ACCESS_KEY
        self.secret_key: str = SECRET_ACCESS_KEY
        self.topic: str = topic
        self.iot_client = boto3.client('iot-data', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_ACCESS_KEY, region_name='eu-west-1')

    def publish_to_topic(self, data) -> None:
        response = self.iot_client.publish(
            topic=self.topic,
            qos=1,
            payload=str(data)
        )


class ActionsBaseline:
    def __init__(self):
        # This is the web scraped short list... just hardcoding for now for testing.
        self.short_list = ['104', '169.1', '', '', '', '', '', '', '', "2'23.911", '36.344', '38.589', '37.780', '31.198', '\n', '11', '', '', '', '', '', '', '', '', "2'27.173", '37.444', '39.418', '\\xa0', '\\xa0', '\n', '111', '212.6', '', '', '', '', '', '', '', "2'10.381", '33.680', '34.850', '33.452', '28.399', '\n', '12', '', '', '', '', '', '', '', '', "2'28.173", '36.845', '39.326', '\\xa0', '\\xa0', '\n', '13', '101.4', '', '', '', '', '', '', '', "2'21.319", '34.471', '37.027', '36.595', '33.226', '\n', '16', '', '', '', '', '', '', '', '', "1'59.846", '29.650', '32.489', '\\xa0', '\\xa0', '\n', '17', '133.7', '', '', '', '', '', '', '', "2'24.351", '36.905', '38.615', '37.480', '31.351', '\n', '18', '181.2', '', '', '', '', '', '', '', "2'21.566", '35.741', '38.169', '37.430', '30.226', '\n', '19', '105.4', '', '', '', '', '', '', '', "2'10.971", '33.336', '35.223', '33.805', '28.607', '\n', '2', '122.9', '', '', '', '', '', '', '', "2'08.129", '33.319', '33.656', '32.265', '28.889', '\n', '21', '125.2', '', '', '', '', '', '', '', "2'06.313", '32.145', '33.933', '\\xa0', '\\xa0', '\n', '216', '180.3', '', '', '', '', '', '', '', "2'20.060", '35.105', '37.252', '36.638', '31.065', '\n', '22', '129.7', '', '', '', '', '', '', '', "2'06.256", '32.093', '34.544', '32.379', '27.240', '\n', '222', '131.9', '', '', '', '', '', '', '', "2'29.243", '37.333', '39.287', '\\xa0', '\\xa0', '\n', '225', '195.0', '', '', '', '', '', '', '', "2'17.510", '34.091', '36.116', '35.043', '32.260', '\n', '23', '117.9', '', '', '', '', '', '', '', "1'57.915", '\\xa0', '\\xa0', '30.398', '25.515', '\n', '244', '216.0', '', '', '', '', '', '', '', "2'07.485", '32.719', '34.090', '32.796', '27.880', '\n', '28', '190.2', '', '', '', '', '', '', '', "2'17.735", '34.532', '36.367', '35.749', '31.087', '\n', '3', '216.9', '', '', '', '', '', '', '', "2'05.106", '31.677', '33.586', '32.789', '27.054', '\n', '31', '232.3', '', '', '', '', '', '', '', "1'59.516", '30.584', '31.768', '31.100', '26.064', '\n', '310', '212.6', '', '', '', '', '', '', '', "2'10.562", '32.404', '34.410', '33.216', '30.532', '\n', '32', '94.9', '', '', '', '', '', '', '', "2'21.407", '36.127', '38.323', '36.604', '30.353', '\n', '34', '203.8', '', '', '', '', '', '', '', "2'07.392", '32.162', '34.067', '33.158', '28.005', '\n', '37', '165.4', '', '', '', '', '', '', '', "2'28.514", '36.965', '39.526', '38.262', '33.761', '\n', '38', '217.3', '', '', '', '', '', '', '', "2'04.204", '31.528', '33.367', '32.388', '26.921', '\n', '4', '170.9', '', '', '', '', '', '', '', "2'25.696", '37.115', '39.231', '38.344', '31.006', '\n', '47', '223.6', '', '', '', '', '', '', '', "2'06.404", '31.780', '33.591', '32.500', '28.533', '\n', '50', '167.2', '', '', '', '', '', '', '', "2'28.237", '37.279', '39.725', '38.997', '32.236', '\n', '500', '162.9', '', '', '', '', '', '', '', "2'06.838", '31.975', '34.017', '\\xa0', '\\xa0', '\n', '55', '106.2', '', '', '', '', '', '', '', "2'26.105", '36.654', '38.980', '38.412', '32.059', '\n', '56', '115.7', '', '', '', '', '', '', '', "2'23.939", '35.203', '38.507', '38.069', '32.160', '\n', '59', '62.6', '', '', '', '', '', '', '', "2'18.504", '35.330', '54.085', "1'09.625", '\\xa0', '\n', '6', '99.8', '', '', '', '', '', '', '', "2'17.984", '34.068', '35.967', '35.309', '32.640', '\n', '60', '', '', '', '', '', '', '', '', "2'20.107", '35.685', '37.420', '\\xa0', '\\xa0', '\n', '61', '191.5', '', '', '', '', '', '', '', "2'14.133", '33.830', '36.059', '35.453', '28.791', '\n', '62', '233.8', '', '', '', '', '', '', '', "1'57.178", '29.671', '31.506', '30.428', '25.573', '\n', '65', '', '', '', '', '', '', '', '', "2'27.869", '37.097', '39.463', '\\xa0', '\\xa0', '\n', '66', '', '', '', '', '', '', '', '', "2'26.196", '36.751', '40.872', '\\xa0', '\\xa0', '\n', '67', '159.1', '', '', '', '', '', '', '', "2'25.966", '36.827', '38.930', '38.402', '31.807', '\n', '7', '86.7', '', '', '', '', '', '', '', '\\xa0', "1'00.982", '40.156', "1'20.664", '\\xa0', '\n', '72', '76.6', '', '', '', '', '', '', '', "2'24.098", '36.265', '38.745', '37.721', '31.367', '\n', '743', '99.3', '', '', '', '', '', '', '', "2'17.120", '34.450', '36.116', '34.833', '31.721', '\n', '75', '136.9', '', '', '', '', '', '', '', "2'11.737", '32.789', '34.435', '34.534', '29.979', '\n', '777', '229.3', '', '', '', '', '', '', '', "1'56.964", '29.837', '31.169', '30.646', '25.312', '\n', '81', '233.3', '', '', '', '', '', '', '', "1'57.170", '29.938', '31.446', '30.466', '25.320', '\n', '86', '141.4', '', '', '', '', '', '', '', "2'16.023", '34.214', '36.275', '35.891', '29.643', '\n', '88', '131.1', '', '', '', '', '', '', '', "2'28.547", '36.794', '39.299', '38.914', '33.540', '\n', '884', '', '', '', '', '', '', '', '', "2'18.287", '34.386', '36.645', '\\xa0', '\\xa0', '\n', '885', '213.1', '', '', '', '', '', '', '', "2'11.070", '32.562', '34.459', '33.848', '30.201', '\n', '888', '127.2', '', '', '', '', '', '', '', "1'59.628", '30.815', '32.613', '30.554', '25.646', '\n', '97', '207.7', '', '', '', '', '', '', '', "2'08.508", '32.507', '34.392', '33.706', '27.903', '\n']
        self.car_timing_dict = get_initialized_car_timing_dict

    def parse_sector_timing(self, short_list: List[str]) -> None:
        for i in find_indices_of_string(_list=self.short_list, string="\n"):
            car_number = self.short_list[i - 20]
            car_timing = self.short_list[i - 19]
            self.car_timing_dict[car_number].append(car_timing)


class LiveOrchestrator:
    def __init__(self):
        self.continuous_scraping = SuperTaikyuScrapingHeadless(print_table=False)
        self.convert_to_list = ConvertTimingTableToList(live_data=True)
        self.mqtt_client = SendTimingTableToMQTT()

    def run(self):
        count = 0
        while True:
            # Get our Timing Table object
            table_db = self.continuous_scraping.continuous_update()

            # Get our Timing Table object
            short_list = self.convert_to_list.convert_timing_table_to_short_list(self.convert_to_list.convert_timing_table_to_full_list(timing_table=table_db))

            # Send to MQTT topic
            self.mqtt_client.publish_to_topic(data=short_list)
            print(short_list)

            count += 1


def live_loop() -> None:
    orchestrator = LiveOrchestrator()
    orchestrator.run()


def main():
    # web_scraper = SuperTaikyuScraping(use_local_html=False)
    # web_scraper.save_soup()
    # # web_scraper.working_with_rows()
    # # web_scraper.working_with_headers()
    # web_scraper.working_with_timing_table()

    # continous_scraper = SuperTaikyuScrapingHeadless()
    # continous_scraper.continuous_update()

    # converter = ConvertTimingTableToList()
    # sample_list = converter.convert_timing_table_to_full_list()
    # print(sample_list)
    #
    # # Print the memory usage of the list
    # print("Memory usage of list: ", sys.getsizeof(sample_list))
    #
    # # Initialize our MQTT client
    # mqtt_client = SendTimingTableToMQTT()
    # mqtt_client.publish_to_topic(sample_list)

    live_loop()


if __name__ == "__main__":
    main()
    print("Done.")
