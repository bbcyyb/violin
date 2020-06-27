# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ViolinScraperItem(scrapy.Item):
    pass


class SlctItem(scrapy.Item):
    name = scrapy.Field()
    img_url = scrapy.Field()
    image_paths = scrapy.Field()


class ProxyItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    location = scrapy.Field()
    kind = scrapy.Field()
    last_verify_time = scrapy.Field()
