# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuotetutorialItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    author = scrapy.Field()
    tag = scrapy.Field()


class EcdcEuropaItemCovidDeaths(scrapy.Item):
    country_name_death = scrapy.Field()
    country_name_number_death = scrapy.Field()


class EcdcEuropaItemCovidReported(scrapy.Item):
    country_name_reported = scrapy.Field()
    country_name_number_reported = scrapy.Field()


class BNONewsItem(scrapy.Item):
    country_name = scrapy.Field()
    total_cases = scrapy.Field()
    new_cases = scrapy.Field()
    total_deaths = scrapy.Field()
    new_deaths = scrapy.Field()
    recovered = scrapy.Field()
    region = scrapy.Field()
