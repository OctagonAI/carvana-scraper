# Carvana Scraper
### Updated on: Aug 16, 2024
This Python script will scrape data from Carvana.com. It extracts data at the detail view by providing a list of URLs of the detail pages of each car listing. This script and the list of URLs are dynamically generated using Octagon AI and contain self healing properties. This means that if any part of the site changes, the script is able to automatically adapt and is dynamically updated to reflect those changes. 

![Screenshot 2024-08-16 at 10 45 35 PM](https://github.com/user-attachments/assets/21cc2f69-3e51-4678-825a-d4d6d7e4d291)

## Getting Started
You can use this script to extract the following data from Carvana website. You can also modify the script to extract other fields if you desire:

1. “name": "2023 Tesla Model 3"
2. "make": "Tesla"
3. "model": "Model 3 Long Range"
4. "vehicle_price": “$28,323”
5. "mileage": "7,353 miles"
6. "location": "Haven, KS"

## Installation
This code was written using Python 3.5.

PIP to install the following packages in Python:

	pip install scrapy scrapy-playwright

## Usage
You must run the script using Python with two arguments --list="URL-list" --limit="limit"
- "URL-list": A list of URLs of the detail pages [Required]
- "limit": Maximum number of items to scrape [Optional]

As an example, I want to build a list of of all Tesla cars for sale:

	python scrape_data_carvana.com_20240817.py --list=carvana.com_20240817_detail_pages.txt --limit=1000

## Output
This will create both json and csv files:

![Screenshot 2024-08-16 at 10 49 00 PM](https://github.com/user-attachments/assets/02b914cc-981d-4ca0-bfef-ef094211f7f5)

## How should I update the script?
You can use Octagon AI to generate a new script in real time. To do so, simply go to https://octagonai.co and sign up.

## Can Octagon AI scrape for me?
Yes, you can use Octagon AI to schedule the scraping to automatically run daily, weekly, or monthly. To do so, simply go to https://octagonai.co and sign up.






