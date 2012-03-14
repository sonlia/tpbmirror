#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
from bs4 import BeautifulSoup
from getopt import *
import sys

from models import mirrordb

def gettopURL(startURL):
    "获取startURL页面上的所有链接"
    topfp = urllib2.urlopen(startURL)
    pattern = re.compile("top/[0-9]+")
    while True:
        s = topfp.read()
        if not s:
            break
        urls = pattern.findall(s)
        urls = ["http://labaia.ws/" + url for url in urls]
        topfp.close()
        return urls

def getallURL(startURL):
    "获取startURL页面上的所有链接"
    print startURL
    allfp = urllib2.urlopen(startURL)
    pattern = re.compile("browse/[0-9]+")
    s = allfp.read()
    urls = pattern.findall(s)
    urls = ["http://labaia.ws/" + url + '/' for url in urls]
    allfp.close()

    totalurls = []
    for url in urls:
        for i in range(100):
            for ii in range(2, 15):
                totalurls.append(url + str(i) + '/' + str(ii) + '/')
    return totalurls

def fetch(url, dbname, begin, end):
    """
    根据指定的url抓取资源信息，存到数据库中
    此页面必须是直接有链接的页面
    """ 
    print int(url[24:27])
    if int(url[24:27]) >= end or int(url[24:27]) < begin:
        return 
    
    try:
        doc = urllib2.urlopen(url, timeout=10)
    except:
        print 'open url Err, url:%s' % (url)
        return    
    try:
        soup = BeautifulSoup.BeautifulSoup(doc.read())
        souptrs = BeautifulSoup.BeautifulSoup(str(soup.findAll('tr'))) 
    except:
        print 'BeautifulSoup Err' 
        return
    
    for tr in souptrs.contents[2:]:
        if hasattr(tr, 'name'):
            #获取资源名称，类别，链接地址及大小
            i = 0
            try:
                acollect = tr.findAll('a')
                typeL1 = ''.join(acollect[0].contents)
                typeL2 = ''.join(acollect[1].contents)
                name = ''.join(acollect[2].contents)
                magnetlink = acollect[3]['href']
                font = tr.findAll('font')
                sizelazy = ''.join(font[0].contents[0])
                #获取大小，不用费心看了，严重依赖于格式
                size = sizelazy[sizelazy.find('Size') + 5:sizelazy.find('iB') + 2].replace(ur'&nbsp;', '')
                print "name:%s, typeL1:%s, typeL2:%s, size:%s" % (name, typeL1, typeL2, size)
                mirrordb.add_record(dbname , name, typeL1, typeL2, magnetlink, size)
            except:
                i = i + 1
                print 'fetch resouce url Err, url:%s' % (url) 
                if i > 3:
                    break
                
#just for test                
def fetch_all(urllist, begin, end):
    for url in urllist:
        try:
            fetch(url, dbname='allsource', begin=begin, end=end)
        except:
            print 'fetch err url:%s' % (url)
            continue

if __name__ == '__main__':
    opts, args = getopt(sys.argv[1:], "limit=")
    print args[0], args[1]
    #fetch('http://labaia.ws/top/602')
    startURL = 'http://labaia.ws/browse/'
    urllist = getallURL(startURL) 
    fetch_all(urllist, int(args[0]), int(args[1]))


