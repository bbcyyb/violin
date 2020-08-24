import random


class UAMiddleware:
    def process_request(self, request, spider):
        ua_pool = spider.settings['USER_AGENT_LIST']
        if ua_pool and len(ua_pool) > 0:
            ua = random.choice(ua_pool)
            request.headers['User-Agent'] = ua