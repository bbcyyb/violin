from scrapy.cmdline import execute
from violin_scraper.utils import File
from violin_scraper.utils import running_path

import sys
import os

DEBUG = 1
os.environ['debug'] = str(DEBUG)


def run():
    path = running_path()
    sys.path.append(path)
    spiders = []
    # spiders.append('slct')
    # spiders.append('example')
    spiders.append('proxy')

    for spider_name in spiders:
        execute(['scrpy', 'crawl', spider_name, '-a', 'debug={}'.format(DEBUG)])


def test_file():
    path = running_path()
    file = os.path.join(path, 'test.txt')
    f = File()
    f.open_file(file=file)
    f.writeline('hahahaha', True)
    f.close_file()


class Base:

    settings = {}

    @classmethod
    def from_init(cls):
        print("Hello, I'm Base")


class Child(Base):
    @classmethod
    def from_init(cls):
        print("Hello, I'm Child")


if __name__ == "__main__":
    run()
    # test_file()
    # Child.from_init()
