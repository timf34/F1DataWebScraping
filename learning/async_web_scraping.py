import asyncio
import bs4

from selenium import webdriver


class AsyncWebScraping:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.driver = webdriver.Edge()
        self.url: str = "https://www.supertaikyu.live/timings/"

    def run(self):
        self.loop.run_until_complete(self.async_get_page())
        self.loop.close()

    async def async_get_page(self):
        self.driver.get(self.url)
        await asyncio.sleep(5)
        print(self.driver.page_source)
        self.driver.close()

    async def async_return_page(self) -> str:
        self.driver.get(self.url)
        await asyncio.sleep(5)
        page_source = self.driver.page_source
        self.driver.close()
        return page_source

    def print_bs4_object(self):
        self.loop.run_until_complete(self.async_print_bs4_object())
        self.loop.close()


def main():
    async_web_scraping = AsyncWebScraping()

    # Get the page source using async_return_page
    page_source = async_web_scraping.loop.run_until_complete(async_web_scraping.async_return_page())
    print(page_source)


if __name__ == "__main__":
    main()



