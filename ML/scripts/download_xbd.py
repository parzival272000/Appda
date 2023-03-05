"""
Script to download XBD dataset from https://xview2.org/
"""
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)

from selenium.webdriver.common.keys import Keys
import time

driver.get('https://xview2.org/auth/signin')

time.sleep(3)

username = driver.find_element_by_name('email')
username.send_keys('EMAIL_HERE')
username.send_keys(Keys.ENTER)

time.sleep(3)

password = driver.find_element_by_name('password')
password.send_keys('PASSWORD_HERE')
password.send_keys(Keys.ENTER)

time.sleep(30)

driver.find_element_by_xpath('//a[@href="/download"]').click()

time.sleep(1)

driver.find_element_by_xpath('//a[@href="/download-links"]').click()

time.sleep(10)

driver.find_elements_by_link_text('Download Challenge test set')[0].click()

time.sleep(200)
