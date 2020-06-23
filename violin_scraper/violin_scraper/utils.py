from scrapy import shell

def inspect(response, spider):
    spider.logger.info('========> Start inspecting')
    shell.inspect_response(response, spider)
    spider.logger.info('<======== Finish inspecting')
