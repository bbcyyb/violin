import time
import json
import redis
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def proform():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable_gpu')
    driver = webdriver.Chrome(options=chrome_options)
    driver.minimize_window()

    url = 'http://exercise.kingname.info/exercise_login.html'
    print(1)
    driver.get(url)

    user = driver.find_element_by_xpath('//input[@name="username"]')
    user.clear()
    user.send_keys('kingname')

    password = driver.find_element_by_xpath('//input[@name="password"]')
    password.clear()
    password.send_keys('genius')

    remember = driver.find_element_by_xpath('//input[@name="rememberme"]')
    remember.click()

    login = driver.find_element_by_xpath('//button[@class="login"]')
    login.click()
    print(2)
    time.sleep(3)
    print(3)
    cookies = driver.get_cookies()
    print(cookies)
    # TODO: 将cookies完整写入redis中，将spider name作为key
    print(4)
    driver.quit()
    print(5)


if __name__ == "__main__":
    proform()