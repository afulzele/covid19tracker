import scrapy
from ..items import EcdcEuropaItemCovidDeaths
import re


class ECDCEuropa(scrapy.Spider):
    name = 'ecdc_europa_deaths'
    start_urls = [
        'https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases'
    ]

    def parse(self, response):
        item_death = EcdcEuropaItemCovidDeaths()

        countries_death = response.css("div p:nth-child(4)::text").extract_first()

        countries_death_list = str(countries_death).split(", ")

        for i in countries_death_list:
            m = re.search(r"[^0-9]+", i)
            item_death["country_name_death"] = m.group().strip()[:-2]
            m = re.search(r"[0-9]+\s?[0-9]*", i)
            item_death["country_name_number_death"] = int(m.group().replace(u"\xa0", u""))

            yield item_death

