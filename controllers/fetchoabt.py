#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import time
import web
from bs4 import BeautifulSoup


class CFetchoabt():
    
    _movie_info = {}
    
    def __init__(self, url):
        self.url = url

    def magic_fetch_and_insert(self):
        database = "../database/tpbmirror.db"
        db = web.database(dbn='sqlite', db=database)
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh-cn,zh;q=0.5',
                   'Connection': 'keep-alive',
                   'Cookie': '37cs_user=37cs13650143833; Hm_lvt_ce396a90f02f136fc25a1bfc9138c834=1331695718366; 37cs_show=1%2C26; PHPSESSID=r3okpuu9o47bt9u32epkii08i2; 37cs_pidx=4; Hm_lpvt_ce396a90f02f136fc25a1bfc9138c834=1331695718366',
                   'Host': 'oabt.org',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.2) Gecko/20100101 Firefox/10.0.2'}
        req = urllib2.Request(self.url, headers=headers)
        doc = urllib2.urlopen(req).read()

        page_soup = BeautifulSoup(doc)
        tables = page_soup.findAll('table', cellspacing="0")
        tables = tables[3].contents[4:]
        for tr in tables:
            try:
                size = tr.contents[1].contents[9].contents[0] #size
                typeL2 = tr.contents[1].contents[1].contents[0].contents[0] #type
                resource_name = tr.contents[1].contents[3].contents[0].contents[0] #name
                magnet = tr.contents[1].contents[5].contents[1]['href'] #magnet
                ed2k = tr.contents[1].contents[5].contents[2]['ed2k'] #ed2k
                db.insert('oabt', size=size, typeL1='Video', typeL2=typeL2, resource_name=resource_name, magnet=magnet, ed2k=ed2k)
            except:
                continue
        
        print 'OK'
        pass

if __name__ == '__main__':
    urllist = ['http://oabt.org/index.php?page=' + str(i) for i in range(331)]
    for url in urllist:
        try:
            oabt = CFetchoabt(url)
            oabt.magic_fetch_and_insert()
            time.sleep(10)
        except:
            continue
            
        
