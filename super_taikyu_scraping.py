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
from utils import open_object_using_pickle, find_indices_of_string


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
            self.html = self.get_html_using_selenium(delay=1)
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
        temp_short_car = ['' for _ in range(11)]

        indices_we_want = [2, 16, 8]
        indices_we_want_to_fill = [0, 1, 9]

        for i in find_indices_of_string(_list=full_list, string="\n"):
            full_car = full_list[i - 20:i]
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
