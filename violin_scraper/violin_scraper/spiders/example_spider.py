import scrapy

class ExampleSpider(scrapy.Spider):
    name = 'example'
    start_urls = [
         'http://lab.scrapyd.cn/'
         ]

    def parse_(self, response):
        for quote in response.css('div.quote'):
            yield {
                '内容': quote.css('span.text::text').extract_first(),
                '作者': quote.xpath('span/small/text()').extract_first(),
            }

        next_page = response.css('li.next a::attr("href")').extract_first()
        if next_page is not None:
            yield scrapy.Request(next_page, self.parse)

    def parse(self, response):
        mingyan = response.css('div.quote')

        for v in mingyan:
            text = v.css('.text::text').extract_first()
            autor = v.css('.author::text').extract_first()
            tags = v.css('.tags .tag::text').extract()
            tags = ','.join(tags)

        fileName = '%s-语录.txt' % autor

        with open(fileName, "a+", encoding="utf-8") as f:
            self.logger.info('[======>] %s' % text)
            f.write(text)
            f.write('\n')
            f.write('标签：' + tags)
            f.write('\n------\n')
            f.close()
    