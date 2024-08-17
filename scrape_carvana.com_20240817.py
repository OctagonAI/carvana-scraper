import asyncio
import json
import csv
from datetime import datetime
import argparse

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy_playwright.page import PageMethod
from twisted.internet import asyncioreactor

class GenericPlaywrightSpider(scrapy.Spider):
    name = "generic_playwright_spider"

    def __init__(self, url_list=None, limit=None, *args, **kwargs):
        super(GenericPlaywrightSpider, self).__init__(*args, **kwargs)

        self.config = {
        "domain": "https://www.carvana.com/cars/filters?cvnaid=eyJmaWx0ZXJzIjp7Im1ha2VzIjpbeyJuYW1lIjoiVGVzbGEifV19fQ%3D%3D",
        "xpaths": {
                "car_name": "//p[contains(@class, 'kOnSqV')]",
                "car_make": "//a[contains(@href, '/cars/filters?cvnaid=eyJmaWx0ZXJzIjp7Im1ha2VzIjpbeyJuYW1lIjoiVGVzbGEifV19fQ%3D%3D')]",
                "car_model": "//a[contains(@href, '/cars/filters?cvnaid=eyJmaWx0ZXJzIjp7Im1ha2VzIjpbeyJuYW1lIjoiVGVzbGEiLCJtb2RlbHMiOlt7Im5hbWUiOiJNb2RlbCAzIn1dfV19fQ%3D%3D')]",
                "car_year": "//p[contains(@class, 'kOnSqV')]",
                "car_price": "//div[contains(@class, 'text-blue-6 tl-header-m')]",
                "car_mileage": "//span[@data-qa='mileage']",
                "car_location": "//p[@data-analytics-id='Earliest Delivery open Geolocation Modal']"
        }
}

        self.url_list = url_list
        self.limit = int(limit) if limit else None
        self.all_scraped_data = []

    def start_requests(self):
        with open(self.url_list, 'r') as f:
            urls = [line.strip() for line in f]

        if self.limit:
            urls = urls[:self.limit]

        for url in urls:
            yield scrapy.Request(
                url,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod("wait_for_selector", "body"),
                    ],
                ),
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]

        scraped_data = {}
        for field, xpath in self.config["xpaths"].items():
            if xpath:  # Only attempt to query if xpath is not None
                elements = await page.query_selector_all(xpath)
                if elements:
                    scraped_data[field] = await elements[0].inner_text()
                else:
                    scraped_data[field] = None
            else:
                scraped_data[field] = None

        if any(scraped_data.values()):  # Only append if at least one field has data
            self.all_scraped_data.append(scraped_data)

        await page.close()

    def closed(self, reason):
        # Prepare the output data
        timestamp = datetime.now().isoformat()
        output_data = {"domain": self.config["domain"], "scrape_date": timestamp, "output_data": self.all_scraped_data}

        # Output the scraped data as JSON
        json_output_file = "scraped_carvana.com_20240817_061732.json"
        with open(json_output_file, "w") as f:
            json.dump(output_data, f, indent=2)

        # Output the scraped data as CSV
        csv_output_file = "scraped_carvana.com_20240817_061732.csv"
        keys = self.config["xpaths"].keys()
        with open(csv_output_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            if self.all_scraped_data:
                writer.writerows(self.all_scraped_data)


def main():
    parser = argparse.ArgumentParser(description='Scrape data from a list of URLs.')
    parser.add_argument('--list', required=True, help='File containing list of URLs to scrape')
    parser.add_argument('--limit', type=int, help='Limit the number of URLs to scrape')

    args = parser.parse_args()

    # Install the asyncio reactor
    asyncioreactor.install()

    # Set up the Scrapy settings
    settings = get_project_settings()
    settings.set(
        "DOWNLOAD_HANDLERS",
        {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
    )
    settings.set("TWISTED_REACTOR", "twisted.internet.asyncioreactor.AsyncioSelectorReactor")

    # Create the CrawlerProcess
    process = CrawlerProcess(settings)

    # Add our spider to the process with the command-line arguments
    process.crawl(GenericPlaywrightSpider, url_list=args.list, limit=args.limit)

    # Start the crawling process
    process.start()


if __name__ == "__main__":
    main()

# To run the spider:
# 1. Install required modules:
#    pip install scrapy scrapy-playwright argparse
# 2. Run the script:
#    python scrape_carvana.com_20240817_061732.py --list=carvana.com_20240817_061732_detail_pages.txt --limit=1000
