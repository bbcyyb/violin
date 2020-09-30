import scrapy


class SmzdmSearchItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    keyword = scrapy.Field()
    channel = scrapy.Field()
    platform = scrapy.Field()
    brand = scrapy.Field()
