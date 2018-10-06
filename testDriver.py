#!/usr/bin/env python
#-*- coding:utf-8 -*- 
# author: rebirth
# e-mail: rebirthwyw@gmail.com
# time: 2018-05-10 13:34:44

from selenium import webdriver
import datetime
import requests

class Driver:

	def __init__(self):
		options = webdriver.ChromeOptions()
		options.binary_location = '/opt/google/chrome-unstable/google-chrome-unstable'
		options.add_argument('headless')
		options.add_argument('no-sandbox')
		options.add_argument('window-size=1200x600')
		options.add_argument('load-images=no')
		options.add_argument("--proxy-server=http://127.0.0.1:8000")
		options.add_argument('--user-agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"')
		self.driver = webdriver.Chrome(chrome_options=options)
		return

d = Driver()
d.driver.implicitly_wait(5)
time_start=datetime.datetime.now()
d.driver.get("https://www.baidu.com")
time_end=datetime.datetime.now()
print d.driver.page_source
print "used ",(time_end - time_start)
# page = d.driver.find_elements_by_xpath("/html")[0].get_attribute("innerHTML")
d.driver.quit()

proxy = {"http":"http://127.0.0.1:8000"}
r = requests.get("http://www.freebuf.com/a_new_task_here_rebirth",proxies=proxy, timeout=1, verify=False)
print r.text
