import scrapy


class SlctItem(scrapy.Item):
    name = scrapy.Field()
    img_url = scrapy.Field()
    image_paths = scrapy.Field()
