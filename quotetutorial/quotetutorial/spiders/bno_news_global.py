import scrapy
from ..items import BNONewsItem


class ECDCEuropa(scrapy.Spider):
    name = 'bno_news'
    start_urls = [
        'https://docs.google.com/spreadsheets/d/e/2PACX-1vR30F8lYP3jG7YOq8es0PBpJIE5yvRVZffOyaqC0GgMBN6yt0Q-NI8pxS7hd1F9dYXnowSC6zpZmW9D/pubhtml?gid=0&amp;single=true&amp;widget=true&amp;headers=false&amp;range=A1:I208#'
    ]

    def parse(self, response):
        item = BNONewsItem()

        rows = response.css('div#0 table tbody tr')
        rows = rows[7:-3]

        for row in rows:
            item['country_name'] = row.css('td::text')[0].extract()
            item['total_cases'] = row.css('td::text')[1].extract()
            item['new_cases'] = row.css('td::text')[2].extract()
            item['total_deaths'] = row.css('td::text')[3].extract()
            item['new_deaths'] = row.css('td::text')[4].extract()
            item['recovered'] = row.css('td::text')[7].extract()
            item['region'] = 'global'

            yield item

        rows = response.css('div#1902046093 table tbody tr')
        rows = rows[5:-3]

        for row in rows:
            item['country_name'] = row.css('td::text')[0].extract()
            item['total_cases'] = row.css('td::text')[1].extract()
            item['new_cases'] = row.css('td::text')[2].extract()
            item['total_deaths'] = row.css('td::text')[3].extract()
            item['new_deaths'] = row.css('td::text')[4].extract()
            item['recovered'] = row.css('td::text')[7].extract()
            item['region'] = 'United States'

            yield item

        rows = response.css('div#572527899 table tbody tr')
        rows = rows[5:-2]

        for row in rows:
            item['country_name'] = row.css('td::text')[0].extract()
            item['total_cases'] = row.css('td::text')[1].extract()
            item['new_cases'] = row.css('td::text')[2].extract()
            item['total_deaths'] = row.css('td::text')[3].extract()
            item['new_deaths'] = row.css('td::text')[4].extract()
            item['recovered'] = row.css('td::text')[7].extract()
            item['region'] = 'Australia'

            yield item

        rows = response.css('div#338130207 table tbody tr')
        rows = rows[5:-1]

        for row in rows:
            item['country_name'] = row.css('td::text')[0].extract()
            item['total_cases'] = row.css('td::text')[1].extract()
            item['new_cases'] = row.css('td::text')[2].extract()
            item['total_deaths'] = row.css('td::text')[3].extract()
            item['new_deaths'] = row.css('td::text')[4].extract()
            item['recovered'] = row.css('td::text')[7].extract()
            item['region'] = 'Canada'

            yield item

        rows = response.css('div#108415730 table tbody tr')
        rows = rows[5:-1]

        for row in rows:
            item['country_name'] = row.css('td::text')[0].extract()
            item['total_cases'] = row.css('td::text')[1].extract()
            item['new_cases'] = '0'
            item['total_deaths'] = row.css('td::text')[2].extract()
            item['new_deaths'] = '0'
            item['recovered'] = row.css('td::text')[5].extract()
            item['region'] = 'Mainland China'

            yield item
