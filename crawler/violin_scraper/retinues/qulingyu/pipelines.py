
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class ImgDownloadPipeline(ImagesPipeline):
    item = {}

    def get_media_requests(self, item, info):
        self.item = item
        req = scrapy.Request(
            url=self.item['url'],
        )
        yield req

    def file_path(self, request, response=None, info=None):
        return self.item['path']

    def item_completed(self, results, item, info):
        return item
