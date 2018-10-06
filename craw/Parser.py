#!/usr/bin/env python
# -*- coding:utf-8 -*-

from lxml import etree
import re
from LogUtil import LogUtil
import weakref
import traceback
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

class Parser:

    _parser = None

    def __init__(self,crystal,proto="https://"):
        self.proto = proto
        self.crystal = weakref.ref(crystal)
        self.queue = crystal._queue
        self.lock = crystal._lock
        self.bloom = crystal._bloom
        if self.queue is None:
            raise QueueNotInit
        if self.bloom is None:
            raise BloomNotInit

    @classmethod
    def getInstance(cls):
        if cls._parser is None:
            cls._parser = Parser()
        return cls._parser

    def setProto(self,proto):
        self.proto = proto

    def setDomain(self,domainFir):
        self.domainFir = domainFir

    def getDomain(self):
        return self.domainFir

    def process_item(self,host,pagelink,page):
        LogUtil.n("开始解析页面："+pagelink,self.crystal()._taskId)
        try:
            dom = etree.HTML(page)
            self.collectURLs(dom=dom,pagelink=pagelink,host=host)
        except Exception,e:
            LogUtil.e(traceback.format_exc())
        LogUtil.n("该页面收集URL结束："+pagelink,self.crystal()._taskId)

    def collectURLs(self,dom,pagelink,host):
        LogUtil.n("开始初始化爬出url："+pagelink,self.crystal()._taskId)
        urls = dom.xpath('//a[not(contains(@href,"javasc"))]/@href')
        for url in urls:
            try:
                url = self.standardizeUrl(host,url)
            except Exception,e:
                LogUtil.e(traceback.format_exc())
                url = False
            if url is not False:
                patterns = ["login","signin","oauth"]
                for pattern in patterns:
                    if re.search(pattern, url):
                        if (url not in self.bloom):
                            self.bloom.add(url)
                            self.queue.put(url)
                        break

    def standardizeUrl(self,host,url):
        
        # www.amazon.cn => proto+www.amazon.cn
        if (url.find(host) != -1):
            pat = re.compile(r'^([\w-]+(\.\w+)+)',re.S)
            url = pat.sub(self.proto + r'\1',url)
            return url
        # /gp/help/display.html => proto+host+/gp/help/display.html
        # gp/help/display.html => proto+host+gp/help/display.html
        pat = re.compile(r'^/{0,1}([^/])')
        url = pat.sub(self.proto + host +r'/\1',url)
        # //channel.jd.com => proto+channel.jd.com
        pat = re.compile(r'^//',re.S)
        url = pat.sub(self.proto , url)
        pat = re.compile(r'(.*)(#.*$)',re.S)
        url = pat.sub(r'\1' , url)
        return url

class QueueNotInit(Exception):
    value="You have not initialized Queue,please construct Parser with a complete Crystal instance"
    def __init__(self, value=""):
        super(Exception, self).__init__()
        if value is not "":
            self.value = value
    def __str__(self):
        return repr(self.value)

class BloomNotInit(Exception):
    value="You have not initialized Bloom,please construct Parser with a complete Crystal instance"
    def __init__(self, value=""):
        super(Exception, self).__init__()
        if value is not "":
            self.value = value
    def __str__(self):
        return repr(self.value)