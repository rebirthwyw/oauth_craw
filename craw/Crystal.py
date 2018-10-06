#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import re
import threading
import time

from lxml import etree
from Tool import Queue
import requests
from Downloader import Downloader
from Parser import Parser
from Configer import Configer
from LogUtil import LogUtil
import random
import traceback
from pybloom import BloomFilter
import urllib
reload(sys)  
sys.setdefaultencoding('utf8') 


class Crystal:
    def __init__(self,projectName,taskId):
        self._projectName = projectName
        self._taskId = taskId
        self._parser = None
        self._downloader = None
        self._config = None
        self._queue = None
        self._hostInfo = None
        self._bloom = None
        self._lock = threading.Lock()
        self._num = 0

    def initComponents(self):
        self._num = 0
        self.initConfig()
        self.initQueue()
        self.initBloom()
        self.initParser()

    def run(self):
        #self.threadAdd()
        LogUtil.start_log()
        #empty_count = 0
        _downloader = self.newDownloader()
        while True:
            if not self._queue.empty():
                pagelink = self._queue.pop()
                self._num = self._num + 1
                if (self._num >= 7):
                    break
                host = self._hostInfo["host"]
                proxy = {"http":"http://127.0.0.1:8000"}
                try:
                    r = requests.get("http://127.0.0.1/a_new_req_here_rebirth?url="+urllib.pathname2url(str(pagelink)) , proxies=proxy, timeout=5)
                except Exception,e:
                    LogUtil.e(traceback.format_exc())
                LogUtil.n("开始下载页面："+pagelink,self._taskId)
                try:
                    page = _downloader.get(pagelink)
                except Exception,e:
                    LogUtil.e(traceback.format_exc())
                    continue    
                LogUtil.n("下载页面完成："+pagelink,self._taskId)
                pagelink = pagelink.encode("UTF-8")
                try:
                    self._parser.process_item(host=host,pagelink=pagelink,page=page)
                except Exception,e:
                    LogUtil.e(traceback.format_exc()) 
                #_downloader.tryClick(pagelink)
            else:
                # if empty_count < 3:
                #     empty_count = empty_count + 1
                #     time.sleep(3)
                # else:
                #     break
                break
            # ran = 0.5 - random.random()
            # time.sleep(self._config["DOWNLOAD_DELAY"] * (1 + ran))

        #self.threadReduce()
        _downloader.closeDownloader()
        LogUtil.end_log()

    def initStartUrl(self, targetUrl):
        self.start_url = targetUrl
        self._hostInfo = self.parseUrl(self.start_url[0])
        self._parser.setProto(self._hostInfo["proto"]) # 默认为https://
        self._parser.setDomain(self._hostInfo["fir"])
        for each in self.start_url:
            self._queue.put(each)
        proxy = {"http":"http://127.0.0.1:8000"}
        try:
            r = requests.get("http://127.0.0.1/a_new_task_here_rebirth?url="+urllib.pathname2url(str(self.start_url[0])) , proxies=proxy, timeout=5)
        except Exception,e:
            LogUtil.e(traceback.format_exc())
        LogUtil.i("设置URL完成")

    def initConfig(self):
        self._config = {}
        localConfig = Configer.getConfig()
        for row in localConfig:
            self._config[row] = localConfig[row]

    def initBloom(self):
        self._bloom = BloomFilter(capacity=1000, error_rate=0.001)
        LogUtil.i("初始化Bloom完成")

    def newDownloader(self):
        downloader = Downloader()
        CHROME_ENABLE = self._config["CHROME_ENABLE"]
        downloader.setChromeEnable(CHROME_ENABLE)
        LogUtil.i("初始化Downloader完成")
        return downloader

    def initQueue(self):
        self._queue = Queue()
        LogUtil.i("初始化Queue完成")

    def initParser(self):
        self._parser = Parser(self)
        LogUtil.i("初始化Parser完成")

    def parseUrl(self,url):
        reobj = re.compile(r"""(?xi)\A
        ([a-z][a-z0-9+\-.]*://)
        (([a-z0-9\-_~%]+)\.)?
        (([a-z0-9\-_~%]+)\.)?
        ([a-z0-9\-._~%]+)
        """)
        match = reobj.search(url)
        res = {}
        if match:
            if match.group(5) is None:
                res["sec"] = None
                res["fir"] = match.group(3)
            else:
                res["sec"] = match.group(3)
                res["fir"] = match.group(5)
            res["all"] = match.group(0)
            res["proto"] = match.group(1)
            res["top"] = match.group(6)
            res["host"] = res["all"][len(res["proto"]):]
            return res
        else:
            return False

    def threadAdd(self):
        self._lock.acquire()
        self._threadCount = self._threadCount + 1
        self._lock.release()

    def threadReduce(self):
        self._lock.acquire()
        self._threadCount = self._threadCount - 1
        self._lock.release()

    def getThreadCount(self):
        self._lock.acquire()
        res = self._threadCount
        self._lock.release()
        return res

    def start_single(self,targetUrl):
        self.initComponents()
        self.initStartUrl(targetUrl)
        self.run()

