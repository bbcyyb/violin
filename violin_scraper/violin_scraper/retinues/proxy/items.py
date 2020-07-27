import scrapy


class ProxyItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    location = scrapy.Field()
    kind = scrapy.Field()
    last_verify_time = scrapy.Field()
