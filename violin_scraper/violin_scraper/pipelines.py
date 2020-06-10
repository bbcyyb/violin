# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ViolinScraperPipeline:
    def process_item(self, item, spider):
        return item

class ImagespiderPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for url in item['url']:
            yield Request(url)
