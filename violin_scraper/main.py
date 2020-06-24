from scrapy.cmdline import execute
from violin_scraper.utils import File
from violin_scraper.utils import running_path

import sys
import os


def run():
    path = running_path()
    sys.path.append(path)
    spiders = []
    # spiders.append('slct')
    spiders.append('example')

    for spider_name in spiders:
        execute(['scrpy', 'crawl', spider_name, '-a', 'debug=1'])


def test_file():
    path = running_path()
    file = os.path.join(path, 'test.txt')
    f = File()
    f.open_file(file=file)
    f.writeline('hahahaha', True)
    f.close_file()


if __name__ == "__main__":
    run()
    # test_file()
