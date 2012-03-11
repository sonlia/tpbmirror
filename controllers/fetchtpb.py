#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
from BeautifulSoup import BeautifulSoup as BSoup

from config.settings import topdbname, alldbname
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
        urls = ["http://labaia.ws/"+url for url in urls]
        topfp.close()
        return urls

def getallURL(startURL):
    "获取startURL页面上的所有链接"
    print startURL
    allfp = urllib2.urlopen(startURL)
    pattern = re.compile("browse/[0-9]+")
    s = allfp.read()
    urls = pattern.findall(s)
    urls = ["http://labaia.ws/"+url+'/' for url in urls]
    allfp.close()

    totalurls = []
    for url in urls:
        for i in range(100):
            totalurls.append(url + str(i) + '/3/')
    return totalurls

def fetch(url, dbname = alldbname):
    """
    根据指定的url抓取资源信息，存到数据库中
    此页面必须是直接有链接的页面
    """ 
    try:
        doc = urllib2.urlopen(url)
        soup = BSoup(doc.read())
        souptrs = BSoup(str(soup.findAll('tr')))
        for tr in souptrs.contents[2:]:
            if hasattr(tr, 'name'):
                #获取资源名称，类别，链接地址及大小
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
                    print "name:%s, typeL1:%s, typeL2:%s, size:%s" %(name, typeL1, typeL2, size)
                    mirrordb.add_record(dbname ,name, typeL1, typeL2, magnetlink, size)
                except:
                    print 'fetch resouce url Err, url:%s' %(url) 
    except:
        print 'open url Err, url:%s' %(url)

if __name__ == '__main__':
    #fetch('http://labaia.ws/top/602')
    print getURL('http://labaia.ws/top')
