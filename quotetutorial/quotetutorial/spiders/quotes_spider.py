import scrapy
from ..items import QuotetutorialItem


class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    def parse(self, response):
        item = QuotetutorialItem()

        all_div_quotes = response.xpath("//div[@class='quote']")

        for q in all_div_quotes:
            title = str(q.css("span.text::text").extract_first())
            author = q.css(".author::text").extract()
            tag = q.css(".tags").css(".tag::text").extract()

            item["title"] = title
            item['author'] = author
            item['tag'] = tag

            yield item

        check_next_page = response.css("li.next a").xpath("@href").extract_first()
        if check_next_page is not None:
            next_page = "http://quotes.toscrape.com" + check_next_page
            yield response.follow(next_page, callback=self.parse)
