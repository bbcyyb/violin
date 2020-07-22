import scrapy
from violin_scraper.base_spider import BaseSpider
from violin_scraper.items import ProxyItem

import re
import datetime


class ProxySpider(BaseSpider):
    name = 'proxy'
    _page_threshold = 1

    start_urls = ['http://www.66ip.cn/']
    allowed_domains = ['66ip.cn']

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'violin_scraper.middlewares.exception_downloader.ExceptionMiddlware': 120,
            'violin_scraper.middlewares.proxy_downloader.ProxyMiddleware': 543,
            'violin_scraper.middlewaresua_downloader.UAMiddleware': 544,
        },
        'ITEM_PIPELINES': {
            'violin_scraper.pipelines.ProxyPipeline': 543,
        },
        'IMAGES_STORE': None,
    }

    def parse(self, response):
        # area page
        atags = response.xpath('/html/body/div[3]/table/tr/td/ul/li/a')[1:]
        # if self.debug_mode:
            # atags = atags[0:1]

        from violin_scraper.utils import inspect
        inspect(response, self)

        for atag in atags:
            area_url = atag.xpath('@href').extract_first()
            if area_url is not None:
                area_url = response.urljoin(area_url)
                yield scrapy.Request(area_url, callback=self.parse_ips)

    def parse_ips(self, response):
        # next page, take the first three pages.
        page_name = response.url.split('/')[-1]
        try:
            num = int(page_name.split('.')[0])
            if num < self._page_threshold:
                next_page = '{}.html'.format(num + 1)
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse_ips)
        except Exception as ex:
            self.logger.error(str(ex))

        # extract IP information
        ip_list_selector = response.xpath('//*[@id="footer"]/div/table/tr')[1:]

        proxies = []
        for ip in ip_list_selector:
            ip_content = ip.xpath('td/text()').extract()
            proxy = ProxyItem()
            proxy['ip'] = ip_content[0]
            proxy['port'] = ip_content[1]
            proxy['location'] = ip_content[2]
            proxy['kind'] = ip_content[3]
            proxy['last_verify_time'] = self._extract_verify_time(ip_content[4])
            proxies.append(proxy)

        proxy_set = self._remove_duplicates(proxies)
        for proxy in proxy_set:
            yield proxy

    def _extract_verify_time(self, str):
        """
        A sample input:
        2020年06月27日09时 验证

        Output:
        datetime.datetime(2020, 6, 27, 9, 0, 0)
        """

        # [2020, 6, 27, 9]
        array = [int(s) for s in re.findall(r'\d+\.?\d*', str)]
        return datetime.datetime(array[0], array[1], array[2], array[3], 0, 0)

    def _remove_duplicates(self, proxies):
        """
        Keep only the latest verified record for each IP+Port+Location+Kind.
        """
        new_proxies = []
        self.logger.debug("There are {} original proxies before removeing duplicates".format(len(proxies)))
        for p in proxies:
            replaced = False
            for index in range(len(new_proxies)):
                if new_proxies[index]['ip'] == p['ip'] and \
                        new_proxies[index]['port'] == p['port'] and \
                        new_proxies[index]['location'] == p['location'] and \
                        new_proxies[index]['kind'] == p['kind']:
                    replaced = True
                    if new_proxies[index]['last_verify_time'] < p['last_verify_time']:
                        new_proxies[index] = p

            if not replaced:
                new_proxies.append(p)

        self.logger.debug("There are {} remaining proxies after removeing duplicates".format(len(new_proxies)))
        return new_proxies
