import scrapy
from ..items import WorldMeterItem


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


class ECDCEuropa(scrapy.Spider):
    name = 'scrape_all'
    start_urls = [
        'https://www.worldometers.info/coronavirus/'
    ]

    data_list = {}

    def parse(self, response, d_list=data_list):
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
            if place_name == "USA":
                place_name = "United States"
            if place_name == "S. Korea":
                place_name = "South Korea"
            if place_name == "Bosnia and Herzegovina":
                place_name = "Bosnia"
            if place_name == "UAE":
                place_name = "United Arab Emirates"
            if place_name == "Czechia":
                place_name = "Czech Republic"
            if place_name == "UK":
                place_name = "United Kingdom"
            if place_name == "UK":
                place_name = "United Kingdom"
            if place_name == "CAR":
                place_name = "Central African Republic"

            d_list[place_name] = {
                'cases': int(row.css('td::text')[0].extract().replace(",", "").strip()) - int(new_cases),
                'new_cases': int(new_cases),
                'total_cases': int(row.css('td::text')[0].extract().replace(",", "").strip()),
                'deaths': int(deaths) - int(new_deaths),
                'new_deaths': int(new_deaths),
                'total_deaths': int(deaths),
                'recovered': int(recovered),
                'region': 'global'
            }

        yield response.follow('https://www.worldometers.info/coronavirus/country/us/',
                              callback=self.parse_world_meter_usa)

    def parse_world_meter_usa(self, response, d_list=data_list):
        rows = response.css('table tbody')
        rows = rows[0].css('tr')

        for row in rows[1:]:

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
                'cases': int(row.css('td::text')[1].extract().replace(",", "").strip()) - int(new_cases),
                'new_cases': int(new_cases),
                'total_cases': int(row.css('td::text')[1].extract().replace(",", "").strip()),
                'deaths': int(deaths) - int(new_deaths),
                'new_deaths': int(new_deaths),
                'total_deaths': int(deaths),
                'recovered': int(recovered),
                'region': 'United States'
            }

        yield response.follow(
            'https://docs.google.com/spreadsheets/d/e/2PACX-1vR30F8lYP3jG7YOq8es0PBpJIE5yvRVZffOyaqC0GgMBN6yt0Q-NI8pxS7hd1F9dYXnowSC6zpZmW9D/pubhtml?gid=0&amp;single=true&amp;widget=true&amp;headers=false&amp;range=A1:I208#',
            callback=self.parse_bno_news)

    def parse_bno_news(self, response, d_list=data_list):
        item = WorldMeterItem()

        rows = response.css('div#0 table tbody tr')
        rows = rows[7:-3]

        for row in rows:
            country_name = row.css('td::text')[0].extract()

            cases = 0
            if row.css('td::text')[1].extract() != 'N/A':
                cases = int(row.css('td::text')[1].extract().replace(",", ""))

            new_cases = 0
            if row.css('td::text')[2].extract() != 'N/A':
                new_cases = int(row.css('td::text')[2].extract().replace(",", ""))

            total_cases_bno = cases + new_cases

            deaths = 0
            if row.css('td::text')[3].extract() != 'N/A':
                deaths = int(row.css('td::text')[3].extract().replace(",", ""))

            new_deaths = 0
            if row.css('td::text')[4].extract() != 'N/A':
                new_deaths = int(row.css('td::text')[4].extract().replace(",", ""))

            recovered = 0
            if row.css('td::text')[7].extract() != 'N/A':
                recovered = int(row.css('td::text')[7].extract().replace(",", ""))

            region = 'global'

            if country_name == "Congo":
                country_name = "DR Congo"

            if country_name in d_list:
                total_cases_wm = d_list.get(country_name).get('total_cases')
                if total_cases_bno > total_cases_wm:
                    d_list[country_name] = {
                        'cases': cases,
                        'new_cases': new_cases,
                        'total_cases': total_cases_bno,
                        'deaths': deaths,
                        'new_deaths': new_deaths,
                        'total_deaths': deaths + new_deaths,
                        'recovered': recovered,
                        'region': region
                    }

        rows = response.css('div#1902046093 table tbody tr')
        rows = rows[5:-4]

        for row in rows:
            country_name = row.css('td::text')[0].extract()

            cases = 0
            if row.css('td::text')[1].extract() != 'N/A':
                cases = int(row.css('td::text')[1].extract().replace(",", ""))

            new_cases = 0
            if row.css('td::text')[2].extract() != 'N/A':
                new_cases = int(row.css('td::text')[2].extract().replace(",", ""))

            total_cases_bno = cases + new_cases

            deaths = 0
            if row.css('td::text')[3].extract() != 'N/A':
                deaths = int(row.css('td::text')[3].extract().replace(",", ""))

            new_deaths = 0
            if row.css('td::text')[4].extract() != 'N/A':
                new_deaths = int(row.css('td::text')[4].extract().replace(",", ""))

            recovered = 0
            if row.css('td::text')[7].extract() != 'N/A':
                recovered = int(row.css('td::text')[7].extract().replace(",", ""))

            region = 'United States'

            if country_name in d_list:
                total_cases_wm = d_list.get(country_name).get('total_cases')
                if total_cases_bno > total_cases_wm:
                    d_list[country_name] = {
                        'cases': cases,
                        'new_cases': new_cases,
                        'total_cases': total_cases_bno,
                        'deaths': deaths,
                        'new_deaths': new_deaths,
                        'total_deaths': deaths + new_deaths,
                        'recovered': recovered,
                        'region': region
                    }

        for k, v in d_list.items():
            item["place"] = k
            item["cases"] = v.get("cases")
            item["new_cases"] = v.get("new_cases")
            item["total_cases"] = v.get("total_cases")
            item["deaths"] = v.get("deaths")
            item["new_deaths"] = v.get("new_deaths")
            item["total_deaths"] = v.get("total_deaths")
            item["recovered"] = v.get("recovered")
            item["region"] = v.get("region")

            yield item