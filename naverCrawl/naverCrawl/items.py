# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NavercrawlItem(scrapy.Item):
    title = scrapy.Field()
    context = scrapy.Field()
    reporter = scrapy.Field()
    date = scrapy.Field()
    link = scrapy.Field()
    category = scrapy.Field()
    img = scrapy.Field()
    pass
