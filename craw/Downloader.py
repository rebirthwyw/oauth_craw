#!/usr/bin/env python
#-*- coding:utf-8 -*- 

from selenium import webdriver
import requests
from LogUtil import LogUtil
import time
import sys
import traceback
reload(sys)  
sys.setdefaultencoding('utf8')


class Downloader:
	# 1.requests  2.chrome-headless
	_downloader = None
	chrome_enable = False
	page_load_time = 30
	script_time = 30
	max_wait_time = 30
	min_wait_time = 1

	def __init__(self):
		self.options = webdriver.ChromeOptions()
		prefs = {"profile.managed_default_content_settings.images": 2}
		self.options.add_experimental_option("prefs", prefs)
		self.options.binary_location = '/opt/google/chrome-unstable/google-chrome-unstable'
		#self.options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
		self.options.add_argument('headless')
		self.options.add_argument('no-sandbox')
		self.options.add_argument('window-size=1200x600')
		self.options.add_argument('load-images=no')
		self.options.add_argument("--proxy-server=http://127.0.0.1:8000")
		self.options.add_argument('--user-agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"')
		self.driver = webdriver.Chrome(chrome_options=self.options)
		self.driver.set_page_load_timeout(Downloader.page_load_time)
		self.driver.set_script_timeout(Downloader.script_time)
		self.driver.implicitly_wait(Downloader.max_wait_time)
		self.click_event = ["button"]
		self.cnt = 0

	@classmethod
	def getInstance(cls):
		if cls._downloader is None:
			cls._downloader = Downloader()
		return cls._downloader

	def get(self,url):
		page = ""
		if self.chrome_enable :
			page = self.getByChrome(url)
		else:
			page = self.getByRequests(url)
		return page

	def setChromeEnable(self,enable):
		self.chrome_enable = enable

	# 1.requests
	def getByRequests(self,url):
		LogUtil.n( str(self.cnt)+' '+url)
		self.cnt = self.cnt + 1
		headers = {"user-agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"}
		page = requests.get(url,verify=False,headers=headers).content.decode("utf-8")
		return page

	# 2.chrome-headless
	def getByChrome(self,url):
		page = ""
		LogUtil.n( str(self.cnt)+' '+url)
		self.cnt = self.cnt + 1
		try:
			self.driver.get(url)
		except Exception,e:
			LogUtil.e(traceback.format_exc())
		#LogUtil.d(str(self.driver.page_source))
		try:
			page = self.driver.find_elements_by_xpath("/html")[0].get_attribute("innerHTML")
		except Exception,e:
			LogUtil.e(traceback.format_exc())
		self.driver.quit()
		self.driver = webdriver.Chrome(chrome_options=self.options)
		self.driver.set_page_load_timeout(Downloader.page_load_time)
		self.driver.set_script_timeout(Downloader.script_time)
		self.driver.implicitly_wait(Downloader.max_wait_time)
		return page

	def tryClick(self,url,start=0):
		if not self.chrome_enable :
			return
		LogUtil.i("start try click")
		try:
			self.driver.get(url)
		except Exception,e:
			LogUtil.e(traceback.format_exc())
		(targets, length) = self.find_targets()
		for index in range(start,length):
			element = targets[length-1-index]
			if(element.is_displayed() and element.is_enabled()):
				try:
					element.click()
				except Exception,e:
					LogUtil.e(traceback.format_exc())
				self.driver.get(url)
				(targets, length) = self.find_targets()
		self.driver.quit()
		self.driver = webdriver.Chrome(chrome_options=self.options)
		self.driver.set_page_load_timeout(Downloader.page_load_time)
		self.driver.set_script_timeout(Downloader.script_time)
		self.driver.implicitly_wait(Downloader.max_wait_time)
		LogUtil.i("finish try click")
		return

	def find_targets(self):
		targets = []
		for tagname in self.click_event:
			elements = self.driver.find_elements_by_tag_name(tagname)
			for element in elements:
				targets.append(element)
		length = len(targets)
		return (targets, length)

	def closeDownloader(self):
		self.driver.quit()