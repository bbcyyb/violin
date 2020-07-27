from scrapy.cmdline import execute
from utility.common import running_path
from utility.file import File
from utility.redis import Redis
from utility.di import service, get_ctx 

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
    spiders.append('slct')
    # spiders.append('example')
    # spiders.append('proxy')

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

# ================ DI Test ================== #


@service
class TestService(object):
    def __init__(self, context):
        self.num = 0

    def add(self, num):
        self.num += num
        print('current num is {}'.format(self.num))


def test_di_1():
    ctx = get_ctx()
    if isinstance(TestService.get(ctx), TestService):
        print("It's a instance of TestService")
    else:
        print("It isn't a instance of TestService")

    test = TestService.get(ctx)
    test.add(1)


def test_di_2():
    ctx = get_ctx()
    test = TestService.get(ctx)
    test.add(1)


def test_redis():
    ctx = get_ctx()
    r = Redis.get(ctx)
    if not r.is_connected():
        r.connect(password='mypass')
    r.set_str('abc', 'Kevin.Yu')
    r.set_str('zzz', 'This is a example.')


def test_redis_2():
    ctx = get_ctx()
    r = Redis.get(ctx)
    if not r.is_connected():
        r.connect(password='mypass')
    print(r.get_str('abc'))
    print(r.get_str('zzz'))


# =========================================== #

if __name__ == "__main__":
    run()
    # test_file()
    # Child.from_init()
    # test_headless_chrome()
    # test_di_1()
    # test_di_2()
    # test_redis()
    # test_redis_2()
