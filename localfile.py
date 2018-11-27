# -*- coding: utf-8 -*-
import os
from ftplib import FTP

class FTP_Dfs(object):
    def __init__(self, ip_usr_pas=None):
        self.ftp = FTP()
        self.ftp.encoding = 'utf-8'
        self.ip_usr_pas = ip_usr_pas

    def search_file(self, start_dir, fp, HOST):
        self.ftp.cwd(start_dir)
        dir_res = []
        self.ftp.dir('.', dir_res.append)  # 对当前目录进行dir()，将结果放入列表
        fileType_list = self.fileType_list()
        for i in dir_res:
            if i.startswith("d"):
                self.search_file(self.ftp.pwd() + "/" + i.split(" ")[-1], fp, HOST)
                self.ftp.cwd('..')
            else:
                val = i.split(" ")[-1]
                if self.fileType_filter(val, fileType_list):
                    if self.ftp.pwd().endswith('/'):
                        fp.writelines(HOST + self.ftp.pwd() + val + "\n")
                    else:
                        fp.writelines(HOST + self.ftp.pwd() + "/" + val + "\n")
                        self.fileDownload(self.ftp.pwd() + "/" + val,val)
                        print(HOST + self.ftp.pwd() + "/" + val)

    def run(self):
        try:
            if not len(self.ip_usr_pas):
                print('请将目标ip以及账号密码填进去')
            else:
                fp = open('filepath.txt', 'w', encoding='utf-8')
                for i in self.ip_usr_pas:
                    HOST = i[0]
                    user = i[1]
                    password = i[2]
                    self.ftp.connect(HOST)
                    self.ftp.login(user, password)
                    self.search_file(start_dir='', fp=fp, HOST=HOST)
                fp.close()
        except Exception as e:
            print(e)

    def fileType_list(self, fileType=None):
        typelist = []
        with open('FileType.txt', 'a+', encoding='utf-8') as fp:
            fp.seek(0)
            while True:
                content = fp.readline()
                if not content:
                    break
                typelist.append(content.strip())
            if fileType and isinstance(fileType, str) and fileType not in typelist:
                fp.writelines(fileType + '\n')
        return typelist

    def fileType_filter(self, filename, fileTpye_list):
        filetype = filename.split('.')[-1]
        if filetype in fileTpye_list:
            return True
        else:
            return False

    def fileDownload(self, targetpath, localpath):
        # self.ftp.connect(self.ip_usr_pas[0][0])
        # self.ftp.login(self.ip_usr_pas[0][1], self.ip_usr_pas[0][2])
        # self.ftp.cwd(os.path.split(targetpath)[0])
        fp = open(localpath, 'wb')
        self.ftp.retrbinary('RETR %s' % targetpath, fp.write)

    def quit(self):
        self.ftp.quit()

if __name__ == '__main__':
    ftp = FTP_Dfs()
    ftp.ip_usr_pas = [['192.168.80.13', "ftp1", "ftp"],['192.168.80.5',"ftp", "ftp"]]
    ftp.run()

