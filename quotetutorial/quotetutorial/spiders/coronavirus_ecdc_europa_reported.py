import scrapy
from ..items import EcdcEuropaItemCovidReported
import re


class ECDCEuropa(scrapy.Spider):
    name = 'ecdc_europa_reported'
    start_urls = [
        'https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases'
    ]

    def parse(self, response):
        item_reported = EcdcEuropaItemCovidReported()

        reported_total_string = [response.css("div p:nth-child(6)::text")[1].extract(),
                                 response.css("div p:nth-child(7)::text")[1].extract(),
                                 response.css("div p:nth-child(8)::text")[1].extract(),
                                 response.css("div p:nth-child(9)::text")[1].extract(),
                                 response.css("div p:nth-child(10)::text")[1].extract(),
                                 response.css("div p:nth-child(11)::text")[1].extract()]

        countries_reported_list = []

        for i in reported_total_string:
            temp_list = str(i).split(", ")
            last_elem = temp_list[-1]

            if len(temp_list) != 1:
                del temp_list[-1]

            countries_reported_list = countries_reported_list + temp_list

            if last_elem.count('and') == 1:
                last_elem_temp_list = last_elem.split(' and ')
                countries_reported_list = countries_reported_list + last_elem_temp_list
            elif last_elem.count('and') > 1:
                last_elem_temp_list = last_elem.split(') and ')
                countries_reported_list = countries_reported_list + last_elem_temp_list

        countries_reported_list.remove("Bonaire")

        for i in countries_reported_list:
            m = re.search(r"[^:\s][^0-9]+", i)
            item_reported["country_name_reported"] = m.group().strip()[:-2]
            m = re.search(r"[0-9]+\s?[0-9]*", i)
            item_reported["country_name_number_reported"] = int(m.group().replace(u"\xa0", u""))

            yield item_reported
