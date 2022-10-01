import requests
from bs4 import BeautifulSoup

# Practice from this YT vid: https://youtu.be/15f4JhJ8SiQ


class SkySportsScraper:
    def __init__(self):
        self.url: str = 'https://www.supertaikyu.live/timings/'

        # TODO: See if the the database can be picked up from this url
        self.r = requests.get(self.url)
        self.soup = BeautifulSoup(self.r.text, 'html.parser')
        print(self.soup)


def main():
    scraper = SkySportsScraper()


if __name__ == '__main__':
    main()

