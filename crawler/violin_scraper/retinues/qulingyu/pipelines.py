
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class ImgDownloadPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):

        req = scrapy.Request(
            url=item['url'],
        )

        req.item_obj = item
        yield req

    def file_path(self, request, response=None, info=None):
        return request.item_obj['path']

    def item_completed(self, results, item, info):
        return item
