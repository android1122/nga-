#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
测试demo2,抓取大漩涡内标题含有法王的帖子,然后保存帖子内容,并下载其法王到对应的文件夹
'''
import os
import tqdm
import pymysql
import requests
from lxml import etree
import time
import js2xml
import urllib
import socket
socket.setdefaulttimeout(3) 

request_headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'None',
    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'None',
    'Host':'nga.178.com',
    'Cookie':'UM_distinctid=16149b7eb4637b-0fba0f7150fc1a-393d5f0e-140000-16149b7eb629a; ngacn0comUserInfo=%25CD%25FC%25BC%25C7%25BB%25BB%25BA%25C5%09%25E5%25BF%2598%25E8%25AE%25B0%25E6%258D%25A2%25E5%258F%25B7%0939%0939%09%090%090%094%090%090%09; taihe=0a4362bfaa584fded8dfc70739d42dfc; CNZZDATA1256638858=415566152-1524204629-http%253A%252F%252Fnga.178.com%252F%7C1524204629; CNZZDATA1262314555=845042104-1525660703-http%253A%252F%252Fnga.178.com%252F%7C1525660703; CNZZDATA1256638919=446724459-1520556255-http%253A%252F%252Fnga.178.com%252F%7C1526015903; ngaPassportUid=19644119; ngaPassportUrlencodedUname=%25CD%25FC%25BC%25C7%25BB%25BB%25BA%25C5; ngaPassportCid=Z8hg3lsvcjped8oj43ci74u8ghc0foqh5v7u5iad; _178i=1; CNZZDATA1256638874=982244982-1517790853-http%253A%252F%252Fnga.178.com%252F%7C1528086753; CNZZDATA1261107574=1230478298-1528347443-http%253A%252F%252Fnga.178.com%252F%7C1528347443; bbsmisccookies=%7B%22insad_refreshid%22%3A%7B0%3A%22/152810434069920%22%2C1%3A1528937449%7D%7D; Hm_lvt_5adc78329e14807f050ce131992ae69b=1528361782,1528418922,1528678917,1528765624; CNZZDATA30043604=cnzz_eid%3D2118460049-1517356534-%26ntime%3D1528778921; CNZZDATA1256638820=2033589022-1517356856-http%253A%252F%252Fnga.178.com%252F%7C1528778976; CNZZDATA30039253=cnzz_eid%3D846422142-1517356502-%26ntime%3D1528778938; CNZZDATA1256638828=299812912-1517358470-http%253A%252F%252Fnga.178.com%252F%7C1528779194; CNZZDATA1256638851=319304006-1517356797-http%253A%252F%252Fnga.178.com%252F%7C1528781115; lastvisit=1528784133; lastpath=/read.php?tid=14279914&_ff=-7; ngacn0comUserInfoCheck=39f7e940020cd5594922e69a10380909; ngacn0comInfoCheckTime=1528784133; Hm_lpvt_5adc78329e14807f050ce131992ae69b=1528784136',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}

def getxpath(html):#结构化网页
    return etree.HTML(html)

def download(name,title):#下载模块
    path='D:\\BaiduNetdiskDownload\\%s\\%s'%(title.replace('/','').replace(':',''),name.replace('/',''))
    downloadurl=picturesite_change(name)
    urllib.urlretrieve(downloadurl,path)
    print 1



    
def content_spider(url,title):#爬取js内容,并进行拼接,然后导入数据库
    z=requests.get(url,headers=request_headers,timeout=3)
    s = getxpath(z.content)
    js=s.xpath('//tr[@id="post1strow0"]/td[@class="c2"]/script/text()')#获取js语句
    for i in range(len(js)):
        jscode=js2xml.parse(js[i])#xml化js语句
        picurl=jscode.xpath('//property[@name="url"]/string/text()')#获取js语句内容特定部分
        if len(picurl)==0:
            pass
        else:
            for i in range (0,len(picurl)):
                try:
                    path='D:\\BaiduNetdiskDownload\\%s'%(title.replace('/','').replace(':',''))
                    isExists=os.path.exists(path)
                    if not isExists:
                        os.mkdir(path)
                        download(picurl[i],title)
                    else:
                        pass
                except BaseException as erro:
                    print erro
                    print title
                    pass

def picturesite_change(site):#图片网址转换
    site="http://img.nga.178.com/attachments/"+site
    return site
    
def site_change(site):#帖子内容地址转换主体
    for i in range(len(site)):
        site[i]="http://nga.178.com"+site[i]
    s=map(str,site)
    return s
    
def url_spider(url,page):#爬虫主体
    z=requests.get(url,headers=request_headers,timeout=3)
    s1 = getxpath(z.content)
    title=s1.xpath('//table[@id="topicrows"]/tbody/tr/td[@class="c2"]/a[@class="topic"]/text()')
    userid=s1.xpath('//table[@id="topicrows"]/tbody/tr/td[@class="c3"]/a[@class="author"]/@title')
    username=s1.xpath('//table[@id="topicrows"]/tbody/tr/td[@class="c3"]/a[@class="author"]/text()')
    site=s1.xpath('//table[@id="topicrows"]/tbody/tr/td[@class="c2"]/a[@class="topic"]/@href')#获取帖子内容链接地址
    newsite=site_change(site)#转换帖子链接地址
    for i in range(len(title)):
        try:
            content_spider(newsite[i],title[i])
        except BaseException as erro:
            print erro
            pass
    del title[:]
    del userid[:]
    del username[:]
    del newsite[:]
    del site[:]

for m in range(1,200):
    if m == 1:
        print u'扫描第',m
        url="http://nga.178.com/thread.php?fid=-7&_ff=-7"
        url_spider(url,m)
    else:
        print u'扫描页数:',m
        url="http://nga.178.com/thread.php?fid=-7&page="+str(m)
        url_spider(url,m)





