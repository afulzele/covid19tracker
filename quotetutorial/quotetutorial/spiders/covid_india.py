import scrapy
import json
from ..items import CovidIndiaItem


class ECDCEuropa(scrapy.Spider):
    name = 'covid_india'
    start_urls = [
        'https://api.covid19india.org/data.json'
    ]

    state_district_dict = {}

    def parse(self, response, s_d_dict=state_district_dict):
        rows = response.body
        data = json.loads(rows)

        statewise = (data.get("statewise"))

        for states in statewise:
            get_state_name = states.get("state")
            s_d_dict[get_state_name] = {"_cases_": states.get("confirmed"), "_deaths_": states.get("deaths"),
                                        "_recovered_": states.get("recovered")}

        yield response.follow('https://api.covid19india.org/state_district_wise.json', callback=self.parse_core)

    def parse_core(self, response, s_d_dict=state_district_dict):
        rows = response.body
        data = json.loads(rows)

        for k, v in data.items():
            dist = v.get("districtData")
            for k1, v1 in dist.items():
                if k in s_d_dict and "confirmed" in v1:
                    print(k, k1, v1)
                    s_d_dict.get(k)[k1] = v1.get("confirmed")

        yield response.follow(
            'https://docs.google.com/spreadsheets/d/e/2PACX-1vSc_2y5N0I67wDU38DjDh35IZSIS30rQf7_NYZhtYYGU1jJYT6_kDx4YpF-qw0LSlGsBYP8pqM_a1Pd/pubhtml',
            callback=self.parse_dists)

    def parse_dists(self, response, s_d_dict=state_district_dict):
        item = CovidIndiaItem()
        rows = response.css('div#1207378023 table tbody tr')
        rows = rows[2:-21]

        for row in rows:
            state_name = row.css('td div::text').extract_first()
            if state_name is None:
                state_name = row.css('td::text')[2].extract()
                if state_name == "Daman And Diu":
                    state_name = "Daman and Diu"
            district_name = row.css('td::text')[1].extract()

            if state_name in s_d_dict:
                # print(state_name, s_d_dict.get(state_name), district_name)
                if district_name not in s_d_dict.get(state_name).keys():
                    s_d_dict.get(state_name)[district_name] = '0'

        for key, value in s_d_dict.items():
            for k, v in value.items():
                if k != '_cases_' and k != '_deaths_' and k != '_recovered_':
                    item["state_name"] = key
                    item["state_cases"] = value.get('_cases_')
                    item["state_deaths"] = value.get('_deaths_')
                    item["state_recovered"] = value.get('_recovered_')
                    item["district"] = k
                    item["district_case"] = v

                    yield item
