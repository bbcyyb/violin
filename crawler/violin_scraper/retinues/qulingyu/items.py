import scrapy


class QulingyuItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    path = scrapy.Field()
