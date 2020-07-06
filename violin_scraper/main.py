from scrapy.cmdline import execute
from violin_scraper.utils import File
from violin_scraper.utils import running_path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import sys
import os
import time

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

def test_headless_chrome():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable_gpu')
    driver = webdriver.Chrome(options=chrome_options)
    driver.minimize_window()

    print(1)
    driver.get('https://www.baidu.com/')
    print(2)
    time.sleep(3)
    print(3)
    # driver.find_element_by_id("kw").send_keys('chrome')
    driver.get_screenshot_as_file('./a.png')
    print(4)
    driver.quit()
    print(5)


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
    # run()
    # test_file()
    # Child.from_init()
    test_headless_chrome()
