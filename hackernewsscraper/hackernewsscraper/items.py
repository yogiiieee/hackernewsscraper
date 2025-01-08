# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HackernewsscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    points = scrapy.Field()
    username = scrapy.Field()
    comments = scrapy.Field()
    date = scrapy.Field()
