#! /usr/bin/env python
#! -*-coding:utf-8 -*-

import time
import urllib2
import urllib
import datetime
import requests
import hashlib
import platform

class Tools:
    @staticmethod
    def timestamp_datetime(value):  #将时间戳转为正常时间
        format = '%Y-%m-%d %H:%M:%S'
        value = time.localtime(value)
        dt = time.strftime(format, value)
        return dt
        
    @staticmethod
    def datetime_timestamp(dt):  #将正常时间转为时间戳
         time.strptime(dt, '%Y-%m-%d %H:%M:%S')
         s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
         return int(s)
         
    @staticmethod    
    def GetUnixDate():
        return int(time.mktime(datetime.datetime.now().timetuple()))
        
        
class Spider:
    @staticmethod
    def post(url, data):
        header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN;'
        'rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14'}
        req = requests.post(url, data=data, headers=header)
        return req.content
      
    @staticmethod
    def oldpost(url, data):
        header = {'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN;'
        ' rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14'}
        # data = "w=%s" % data
        req = urllib2.Request(url, data=data)
        req.add_header('User-Agent', header)
        html = urllib2.urlopen(req)
        data = html.read()
        html.close()
        return data
        
    @staticmethod
    def downfile(url, file):
        pass

    @staticmethod
    def get(url, data):
        html = urllib2.urlopen(url)
        return html.read()


def printf(info):
    print "\n{0}\n".format(info)


def md5(info):
    tmp = hashlib.md5()
    tmp.update(info)
    return tmp.hexdigest()
    
def IsWin():
    str = platform.platform()[0:3]
    if str.lower() == 'win':
        return True
    return False
    
    

    
    