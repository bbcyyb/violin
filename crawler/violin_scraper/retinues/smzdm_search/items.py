import scrapy


class SmzdmSearchItem(scrapy.Item):
    create_user = scrapy.Field()
    create_time = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    search_keyword = scrapy.Field()
    platform = scrapy.Field()
