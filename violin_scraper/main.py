from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# os.path.abspath(__file__) get current py file location
# os.path.dirname() get location of parent

spiders = []
spiders.append('slct')

for spider_name in spiders:
    execute(['scrpy', 'crawl', spider_name])