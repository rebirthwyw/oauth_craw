#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import threading
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

class LogUtil:
    ENABLE_LEVEL = 5  #
    ERROR = 1
    WARNING = 2
    DEBUG = 3
    NOTICE = 4
    INFO = 5
    start = None
    end = None
    lock = threading.Lock()
    workName = "work1"

    @classmethod
    def setLogLevel(cls,level):
        cls.ENABLE_LEVEL = level

    @classmethod
    def start_log(cls):
        cls.start = datetime.datetime.now()
        cls.lock.acquire()
        print "start~",cls.start
        cls.lock.release()

    @classmethod
    def end_log(cls):
        cls.end = datetime.datetime.now()
        used = cls.end - cls.start
        cls.lock.acquire()
        print " end ~",cls.end
        print "used ~",used
        cls.lock.release()
        
    # level : info
    @classmethod
    def i(cls,info):
        if cls.ENABLE_LEVEL >= LogUtil.INFO:
            nowdate = datetime.datetime.now()
            cls.lock.acquire()
            print "[Crystal|Info   ]~"+str(nowdate)+":",info
            cls.lock.release()

    # level : notice
    @classmethod
    def n(cls,info,taskId = -1):
        if cls.ENABLE_LEVEL >= LogUtil.NOTICE:
            nowdate = datetime.datetime.now()
            cls.lock.acquire()
            print "[Crystal|Notice ]~"+str(nowdate)+":",info
            cls.lock.release()

    # level : debug
    @classmethod
    def d(cls,info):
        if cls.ENABLE_LEVEL >= LogUtil.DEBUG:
            nowdate = datetime.datetime.now()
            cls.lock.acquire()
            print "[Crystal|Debug  ]~"+str(nowdate)+":",info
            cls.lock.release()

    # level : warning
    @classmethod
    def w(cls,info):
        if cls.ENABLE_LEVEL >= LogUtil.WARNING:
            nowdate = datetime.datetime.now()
            cls.lock.acquire()
            print "[Crystal|Warning]~"+str(nowdate)+":",info
            cls.lock.release()

    # level : error
    @classmethod
    def e(cls,info):
        if cls.ENABLE_LEVEL >= LogUtil.ERROR:
            nowdate = datetime.datetime.now()
            cls.lock.acquire()
            print "[Crystal|Error  ]~"+str(nowdate)+":",info
            cls.lock.release()
