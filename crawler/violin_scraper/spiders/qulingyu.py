import scrapy
from violin_scraper.base_spider import BaseSpider
from violin_scraper.retinues.slct.items import SlctItem
from violin_scraper.utility.common import running_path

import os


class QuLingYuSpider(BaseSpider):
    """
    趣领域
    https://qulingyu1.com/
    """

    name = 'qulingyu'

    host = ['https://qulingyu1.com/?post_type=post&s=%E6%A3%AE%E8%90%9D%E8%B4%A2%E5%9B%A2']
    allowed_domains = ['quliangyu1.com']

    home_url = 'https://qulingyu1.com'
    username = 'bbcyyb@163.com'
    password = 'Vsts@1433'
    # 这里使用header_data而不用中间件每次动态获取headers,是因为登录后有上下文信息了，随意更换header信息可能导致账号被查出异常
    header_data = {
        'Referer': 'https://qulingyu1.com',
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
        'ITEM_PIPELINES': {
        },
        'IMAGES_STORE':
        os.path.join(os.path.dirname(os.path.dirname(running_path())), 'images'),
    }

    # 爬虫运行的起始位置
    def start_requests(self):
        """
        第一步：直接进入Login页面
        """
        print('start qulingyu clawer, go to login page')
        # 登录页面
        login_page = 'https://qulingyu1.com/login/?r=https%3A%2F%2Fqulingyu1.com%2F'
        req = scrapy.Request(
            url=login_page,
            headers=self.header_data,
            callback=self.parseLoginPage,
            dont_filter=True,  # 防止页面因为重复爬取，被过滤了
        )
        yield req


    def parseLoginPage(self, response):
        print(f"parseLoginPage: url = {response.url}")

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
                "token": "bc7b821409"
            },
            callback=self.loginResParse,
            dont_filter=True,
        )

        # response.xpath('/html/body/div/div/div/a[@class="rlogin login_hre_btn logint"]').extract_first()

    def loginResParse(self, response):
        """
        第三步：分析登录结果，然后发起登录状态的验证请求
        """
        print(f"loginResParse: url = {response.url}")

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
            callback=self.isLoginStatusParse,
            dont_filter=True,
        )

    def isLoginStatusParse(self, response):
        """
        第五步:分析用户的登录状态, 如果登录成功，那么接着爬取其他页面
        如果登录失败，爬虫会直接终止。
        """
        print(f"isLoginStatusParse: url = {response.url}")


        # 如果能进到这一步，都没有出错的话，那么后面就可以用登录状态，访问后面的页面了
        # ………………………………
        # 不需要存储cookie
        # 其他网页爬取
        # ………………………………
        # TODO: 读取文件获取url并发起请求

    # parse list -> detail -> image
    def parse_(self, response):
        # next page
        next_url = response.css(
            'div.update_area div.update_area_content nav.navigation div.nav-links a.next::attr(href)'
        ).extract_first()
        if next_url is not None:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse)

        # detail page
        detail_list = response.css(
            'div.update_area div.update_area_content ul.update_area_lists li a::attr(href)'
        ).extract()
        for detail_url in detail_list:
            detail_url = response.urljoin(detail_url)
            yield scrapy.Request(detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        # next page
        next_url = response.css(
            'div.content_left div.nav-links a.prev::attr(href)').extract_first()
        if next_url is not None:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse_detail)

        # image page
        img_selector_list = response.css('div.content_left p img')
        title = response.css('div.item_title h1::text').extract_first()
        for img_selector in img_selector_list:
            item = SlctItem()
            item['name'] = title
            img_url = response.urljoin(
                img_selector.css('img::attr(src)').extract_first())
            item['img_url'] = [img_url]
            yield item
