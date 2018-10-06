#!/usr/bin/env python
#-*- coding:utf-8 -*- 
# author: rebirth
# e-mail: rebirthwyw@gmail.com
# time: 2018-05-08 19:17:05 


import pymysql

class OauthCraw(object):
    def __init__(self):
        host = '127.0.0.1'
        db = 'OauthCraw'
        user = 'root'
        password = '123'
        self._db = pymysql.connect(host, user, password, db, charset='utf8' )
        return

    def insert(self, url, isUse, oauthService, oauthLink, loginLink):
        cursor = self._db.cursor()
        sql = "INSERT into `result` VALUES (null, '%s', %d, '%s', '%s', '%s')" % (pymysql.escape_string(url), isUse, pymysql.escape_string(oauthService), pymysql.escape_string(oauthLink), pymysql.escape_string(loginLink))
        try:
            cursor.execute(sql)
            self._db.commit()
        except Exception as e:
            print(repr(e))
            self._db.rollback()