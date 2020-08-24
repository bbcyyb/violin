import random


class ProxyMiddleware:
    def process_request(self, request, spider):
        proxy_pool = spider.settings['PROXIES']
        if proxy_pool and len(proxy_pool) > 0:
            proxy = random.choice(proxy_pool)
            request.meta['proxy'] = proxy