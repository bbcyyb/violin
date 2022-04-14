import os
import scrapy
from violin_scraper.base_spider import BaseSpider
from violin_scraper.utility.common import running_path
from violin_scraper.utility.file import File

category_ = os.environ.get('spider_category', '')

class QuLingYuScanSpider(BaseSpider):
    """
    趣领域
    https://qulingyu1.com/
    """

    name = 'qulingyu_scan'

    # keyword = 'lingyu'  # 领域
    # keyword = 'wanghong'  # 动漫
    # keyword = 'taotu'  # 唯美
    # keyword = 'laosiji'

    keyword = category_

    entry_url = f'https://qulingyu1.com/{keyword}/'
    allowed_domains = ['quliangyu1.com']

    stored_items = []

    main_folder = ''
    temp_folder = ''
    csv_file = ''

    home_url = 'https://qulingyu1.com'
    username = 'bbcyyb@163.com'
    password = 'Vsts@1433'

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

    # 爬虫运行的起始位置
    def start_requests(self):
        """
        第一步：直接进入Login页面
        """
        print('start qulingyu clawer, go to login page')

        self.main_folder = os.path.dirname(running_path())
        self.temp_folder = os.path.join(self.main_folder, "temp")
        self.csv_file = os.path.join(self.temp_folder, f"{self.keyword}.csv")

        # 登录页面
        login_page = 'https://qulingyu1.com/login/?r=https%3A%2F%2Fqulingyu1.com%2F'
        req = scrapy.Request(
            url=login_page,
            headers=self.header_data,
            callback=self.parse_login,
            dont_filter=True,  # 防止页面因为重复爬取，被过滤了
        )
        yield req

    def parse_login(self, response):
        print(f"parse login: url = {response.url}")

        # 抓取Token
        token = response.xpath('//input[@name="token"]/@value').extract_first()

        login_post_url = f'{self.home_url}/wp-admin/admin-ajax.php'
        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url=login_post_url,
            headers=self.header_data,
            method="POST",
            # post的具体数据
            formdata={
                "user_login": self.username,
                "password": self.password,
                "rememberme": "1",
                "redirect": self.home_url,
                "action": "userlogin_form",
                "token": token
            },
            callback=self.parse_login_res,
            dont_filter=True,
        )

        # response.xpath('/html/body/div/div/div/a[@class="rlogin login_hre_btn logint"]').extract_first()

    def parse_login_res(self, response):
        """
        第三步：分析登录结果，然后发起登录状态的验证请求
        """
        print(f"parse_login_res,: url = {response.url}")

        # 通过访问个人中心页面的返回状态码来判断是否为登录状态
        # 这个页面，只有登录过的用户，才能访问。否则会被重定向(302) 到登录页面
        user_profile_url = f'{self.home_url}/users/?tab=index'

        # 下面有两个关键点
        # 第一个是header，如果不设置，会返回500的错误
        # 第二个是dont_redirect，设置为True时，是不允许重定向，用户处于非登录状态时，是无法进入这个页面的，服务器返回302错误。
        #       dont_redirect，如果设置为False，允许重定向，进入这个页面时，会自动跳转到登录页面。会把登录页面抓下来。返回200的状态码
        yield scrapy.Request(
            url=user_profile_url,
            headers=self.header_data,
            meta={
                'dont_redirect': True,  # 禁止网页重定向302, 如果设置这个，但是页面又一定要跳转，那么爬虫会异常
                # 'handle_httpstatus_list': [301, 302]      # 对哪些异常返回进行处理
            },
            callback=self.parse,
            dont_filter=True,
        )

    def parse(self, response):
        """
        第四步:分析用户的登录状态, 如果登录成功，那么接着爬取其他页面
        如果登录失败，爬虫会直接终止。
        """
        print(f"isLoginStatusParse: url = {response.url}")

        # 如果能进到这一步，都没有出错的话，那么后面就可以用登录状态，访问后面的页面了
        # ………………………………
        # 不需要存储cookie
        # 其他网页爬取
        # ………………………………
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
