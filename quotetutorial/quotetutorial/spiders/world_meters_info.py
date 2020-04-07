import scrapy
from ..items import WorldMeterItem


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


class ECDCEuropa(scrapy.Spider):
    name = 'world_meter'
    start_urls = [
        'https://www.worldometers.info/coronavirus/'
    ]

    data_list = {}

    def parse(self, response, d_list=data_list):
        # item = WorldMeterItem()

        rows = response.css('table tbody')
        rows = rows[0].css('tr')

        region = rows[0].css('td')[0].css('::text').extract_first()

        for row in rows[1:]:

            new_cases = 0
            get_second_element = row.css('td')[2].extract().split('</td>')[0].strip()
            if represents_int(get_second_element[-1:]):
                new_cases = (get_second_element.split(
                    '<td style="font-weight: bold; text-align:right;background-color:#FFEEAA;">+')[1].replace(",",
                                                                                                              "").strip())

            deaths = 0
            get_third_element = row.css('td')[3].extract().split('</td>')[0].strip()
            if represents_int(get_third_element[-1:]):
                deaths = (get_third_element.split('<td style="font-weight: bold; text-align:right;">')[1].replace(",",
                                                                                                                  "").strip())

            new_deaths = 0
            get_fourth_element = row.css('td')[4].extract().split('</td>')[0].strip()
            if represents_int(get_fourth_element[-1:]):
                new_deaths = (
                    get_fourth_element.split('text-align:right;background-color:red; color:white">+')[1].replace(",",
                                                                                                                 "").strip())

            recovered = 0
            get_fifth_element = row.css('td')[5].extract().split('</td>')[0].strip()
            if represents_int(get_fifth_element[-1:]):
                recovered = (get_fifth_element.split('<td style="font-weight: bold; text-align:right">')[1].replace(",",
                                                                                                                    "").strip())

            place_name = row.css('td a::text').extract_first()
            print(place_name)
            if place_name == "USA":
                place_name = "United States"

            d_list[place_name] = {
                'cases': row.css('td::text')[0].extract().replace(",", "").strip(),
                'new_cases': new_cases,
                'deaths': deaths,
                'new_deaths': new_deaths,
                'recovered': recovered,
                'region': 'global'
            }

        yield response.follow('https://www.worldometers.info/coronavirus/country/us/', callback=self.parse_usa)

        # print(d_list)

    def parse_usa(self, response, d_list=data_list):
        item = WorldMeterItem()

        rows = response.css('table tbody')
        rows = rows[0].css('tr')

        region = rows[0].css('td')[0].css('::text').extract_first()

        for row in rows[1:]:

            # print(row.css('td::text')[0].extract().strip())

            new_cases = 0
            get_second_element = row.css('td')[2].extract().split('</td>')[0].strip()
            if represents_int(get_second_element[-1:]):
                new_cases = (get_second_element.split('+')[1].replace(",", "").strip())

            deaths = 0
            get_third_element = row.css('td')[3].extract().split('</td>')[0].strip()
            if represents_int(get_third_element[-1:]):
                deaths = (get_third_element.split(';">')[1].replace(",", "").strip())

            new_deaths = 0
            get_fourth_element = row.css('td')[4].extract().split('</td>')[0].strip()
            if represents_int(get_fourth_element[-1:]):
                new_deaths = (get_fourth_element.split('+')[1].replace(",", "").strip())

            recovered = 0

            d_list[row.css('td::text').extract_first().strip()] = {
                'cases': row.css('td::text')[1].extract().replace(",", "").strip(),
                'new_cases': new_cases,
                'deaths': deaths,
                'new_deaths': new_deaths,
                'recovered': recovered,
                'region': 'United States'
            }


        for k,v in d_list.items():
            item["place"] = k
            item["cases"] = v.get("cases")
            item["new_cases"] = v.get("new_cases")
            item["deaths"] = v.get("deaths")
            item["new_deaths"] = v.get("new_deaths")
            item["recovered"] = v.get("recovered")
            item["region"] = v.get("region")

            yield item
