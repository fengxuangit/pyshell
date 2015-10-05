#! /usr/bin/env python
#! -*-coding:utf-8 -*-

import time
import datetime

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