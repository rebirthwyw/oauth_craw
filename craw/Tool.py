#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

class Queue:
    def __init__(self):
        self.items = []

    def empty(self):
        return self.items == []

    def put(self,item):
        self.items.insert(0,item)

    def pop(self):
        return self.items.pop()

    def size(self):
        return len(self.items)