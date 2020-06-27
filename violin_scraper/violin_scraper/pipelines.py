# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
from violin_scraper.items import ProxyItem
from violin_scraper.utils import (File, str_to_datetime)
import re
import os
import datetime
from pathlib import Path


class ViolinScraperPipeline:
    def process_item(self, item, spider):
        return item


class ImagespiderPipeline(ImagesPipeline):
    #
    # def file_path(self, request, response=None, info=None):
    #     """
    #     :param request: 每一个图片下载管道请求
    #     :param response:
    #     :param info:
    #     :param strip :清洗Windows系统的文件夹非法字符，避免无法创建目录
    #     :return: 每套图的分类目录
    #     """
    #     item = request.meta['item']
    #     folder = item['name']
    #
    #     folder_strip = re.sub(r'[？\\*|“<>:/]', '', str(folder))
    #     image_guid = request.url.split('/')[-1]
    #     filename = u'full/{0}/{1}'.format(folder_strip, image_guid)
    #     return filename
    def get_media_requests(self, item, info):
        for img_url in item['img_url']:
            yield Request(img_url, meta={'item': item['name']})

    def file_path(self, request, response=None, info=None):
        name = request.meta['item']
        # name = filter(lambd x: x not in '()0123456789', name)
        name = re.sub(r'[？ \\*]“<>:/()0123456789', '', name)
        img_guid = request.url.split('/')[-1]
        file_name = u'full/{0}/{1}'.format(name, img_guid)
        return file_name

    def item_completed(self, results, item, info):
        img_path = [x['path'] for ok, x in results if ok]
        if not img_path:
            raise DropItem('Item container no images')
        # item['img_paths'] = img_path
        return item


class ProxyPipeline:
    def process_item(self, item, spider):
        folder_path = r'./proxy_pool'
        if isinstance(item, ProxyItem):
            path = Path(folder_path)
            if not path.is_dir():
                path.mkdir(parents=True)

            content = '{},{},{},{},{}'.format(item.ip, item.port, item.location, item.kind, str_to_datetime(item.verify_time))
            f = File(spider.logger)
            date_now = datetime.datetime.now()
            full_path = path.joinpath('66ip_cn_{}{}{}{}{}.proxy'.format(date_now.year, date_now.month, date_now.day, date_now.hour, date_now.minute))
            if full_path.is_file:
                os.remove(str(full_path.resolve()))

            f.open_file(str(full_path.resolve()), mode='a')
            f.writeline(content, True)
            f.close_file()

        return item
