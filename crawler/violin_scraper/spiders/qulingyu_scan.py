import os
import scrapy
from violin_scraper.base_spider import BaseSpider
from violin_scraper.utility.common import running_path
from violin_scraper.utility.file import File


class QuLingYuScanSpider(BaseSpider):
    """
    趣领域
    https://qulingyu1.com/
    """

    name = 'qulingyu_scan'

    keyword = 'lingyu'
    entry_url = f'https://qulingyu1.com/{keyword}/'
    allowed_domains = ['quliangyu1.com']

    stored_items = []

    main_folder = ''
    temp_folder = ''
    csv_file = ''

    # 这里使用header_data而不用中间件每次动态获取headers,是因为登录后有上下文信息了，随意更换header信息可能导致账号被查出异常
    header_data = {
        'Referer': entry_url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
        'Upgrade-Insecure-Requests': '1'
    }

    custom_settings = {
        'LOG_LEVEL': 'DEBUG',  # Log等级，默认是最低级别debug
        'ROBOTSTXT_OBEY': False,  # default Obey robots.txt rules，因为很多网站都禁止爬虫爬取
        'DOWNLOAD_DELAY': 2,  # 下载延时，默认是0，防止过快，导致IP和帐号被封
        'COOKIES_ENABLED': True,  # 默认enable，爬取登录后的数据时需要启用。 会增加流量，因为request和response中会多携带cookie的部分
        'COOKIES_DEBUG': True,  # 默认值为False,如果启用，Scrapy将记录所有在request(Cookie 请求头)发送的cookies及response接收到的cookies(Set-Cookie 接收头)。
        'DOWNLOAD_TIMEOUT': 25,  # 下载超时，既可以是爬虫全局统一控制，也可以在具体请求中填入到Request.meta中，Request.meta['download_timeout']
        'DOWNLOADER_MIDDLEWARES': {
            'violin_scraper.middlewares.exception_downloader.ExceptionMiddleware': 120,
        },
        'ITEM_PIPELINES': {},
        'IMAGES_STORE': {}
    }

    def __generate_to_scan_item(self, line):
        """
        name, url, num_of_scan, num_of_download, flag
        """
        dict_ = {}
        arr = line.split(',')
        if len(arr) == 5:
            dict_['name'] = arr[0]
            dict_['url'] = arr[1]
            dict_['num_of_scan'] = arr[2]
            dict_['num_of_download'] = arr[3]
            dict_['flag'] = arr[4]

        return dict_

    def start_requests(self):
        """
        爬虫运行的起始位置
        第一步：直接进入目标页面
        """
        print(f'start qulingyu clawer, get into URL: {self.entry_url}')
        self.main_folder = os.path.dirname(running_path())
        self.temp_folder = os.path.join(self.main_folder, "temp")
        self.csv_file = os.path.join(self.temp_folder, f"{self.keyword}.csv")

        if not os.path.isfile(self.csv_file):
            fw = File()
            fw.open_file(file=self.csv_file, mode='w')
            fw.close_file()

        fr = File()
        fr.open_file(file=self.csv_file, mode='r')
        lst = fr.read_lines()
        fr.close_file()

        self.stored_items = [self.__generate_to_scan_item(line) for line in lst]

        req = scrapy.Request(
            url=self.entry_url,
            headers=self.header_data,
            callback=self.parse_summary,
            dont_filter=True,  # 防止页面因为重复爬取，被过滤了
        )
        yield req

    def parse_summary(self, response):
        print(f"parse_summary: URL = {response.url}")
        a_links = response.xpath('body/div[@class="update_area"]/div[@class="update_area_content"]/ul[@class="update_area_lists cl"]/li/a')

        for a_link in a_links:
            """
            name, url, num_of_scan, num_of_download, flag
            """
            url = a_link.xpath('@href').extract_first()
            name = a_link.xpath('img/@alt').extract_first()

            hit = False
            for item in self.stored_items:
                if item['name'] == name:
                    item['url'] = url
                    item['num_of_scan'] = int(item['num_of_scan']) + 1
                    hit = True
                    break

            if not hit:
                new_item = {'name': name, 'url': url, 'num_of_scan': 0, 'num_of_download': 0, 'flag': ''}
                self.stored_items.append(new_item)
        next_page_url = response.xpath('//a[@class="next page-numbers"]/@href').extract_first();
        if next_page_url:
            req = scrapy.Request(
                url=next_page_url,
                headers=self.header_data,
                callback=self.parse_summary,
                dont_filter=True,  # 防止页面因为重复爬取，被过滤了
            )
            yield req
        else:
            # 所有页面抓取完毕，开始写回到csv文件，采用全部覆写的模式
            fw = File()
            fw.open_file(file=self.csv_file, mode='w')
            for index, item in enumerate(self.stored_items):
                print(f'Writing the line {index}, name 【{item["name"]}】')
                fw.writeline(u'{},{},{},{},{}'.format(item["name"], item["url"], item["num_of_scan"], item["num_of_download"], item["flag"]), True)
            fw.close_file()
