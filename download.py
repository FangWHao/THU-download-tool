# -*- coding: utf-8 -*-
import requests
from urllib import parse
from jsonpath import jsonpath
import os

pypath=os.path.dirname(os.path.realpath(__file__))
url=input("请输入要下载的链接: ")
try:
    response = requests.get(url)
    print("正在解析下载链接")
    userpath=url.split('/d/')[1].split('/')[0]
    #print(response.text)
    dirname=response.text.split('dirName: \'')[1].split('\',')[0]
    relativepath=response.text.split('dirPath: \'')[1].split('\',')[0]
    path=dirpath
    print(userpath)
    print(path)

except:
    print("无法解析该链接")
    exit()

def makeurl(targetpath):
    return "https://cloud.tsinghua.edu.cn/api/v2.1/share-links/"+userpath+"/dirents/?thumbnail_size=48&path="+parse.quote(targetpath)
print("开始建立文件树")

tmp=requests.get(makeurl(path))
data=tmp.json()
#print(data)
subfolder=jsonpath(data,'$..folder_path')
subfile=jsonpath(data,'$..file_path')
print("建立文件树完成")
#print(subfolder)
#print(subfile)
print("--------------------------------------")
#将文件用树状结构展示并建立文件夹
print(path)
#print(pypath)
#print(pypath+path)
if not os.path.exists(pypath+path):
    #记得处理文件夹名称中的空格
    os.system("mkdir -p "+pypath+path.replace(" ","\ "))
if(subfolder!=False):
    for i in range(0,len(subfolder)):
        if not os.path.exists(pypath+"/"+subfolder[i]):
            os.system("mkdir -p "+pypath+"/"+subfolder[i].replace(" ","\ "))
        print("--"+subfolder[i])
if (subfile!=False):
    for i in range(0,len(subfile)):
        print("--"+subfile[i])

# 真正开始下载，递归下载
print("开始下载")
def download(targetpath):
    tmp=requests.get(makeurl(targetpath))
    data=tmp.json()
    subfolder=jsonpath(data,'$..folder_path')
    subfile=jsonpath(data,'$..file_path')
    #print(subfolder)
    #print(subfile)
    if (subfile!=False):
        for i in range(0,len(subfile)):
            #如果有了就不下载了
            if os.path.exists(pypath+subfile[i]):
                print("已存在: "+subfile[i])
                continue
            print("正在下载: "+subfile[i])
            downloadpath="https://cloud.tsinghua.edu.cn/d/"+userpath+"/files/?p="+parse.quote(subfile[i])+"&dl=1"
            r=requests.get(downloadpath,stream=True)
            #open 的时候记得处理文件夹名称中的空格和下划线
            #print(downloadpath)
            with open(pypath+subfile[i], "wb") as code:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        code.write(chunk)

            code.close()
    if(subfolder!=False):
        for i in range(0,len(subfolder)):
            if not os.path.exists("\""+pypath+subfolder[i]+"\""):
                os.system("mkdir -p "+"\""+pypath+subfolder[i]+"\"")
            download(subfolder[i])

download(path)
print("下载完成")
