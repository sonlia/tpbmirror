#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import fetchtpb
from config.settings import render
from config.settings import topdbname, alldbname

def scheming_fetch_top():
    "抓取Top100功能"
    
    urllist = []
    dbname = topdbname

    startURL = 'http://labaia.ws/top/'
    urllist = fetchtpb.gettopURL(startURL) 
    print urllist

    for url in urllist:
        fetchtpb.fetch(url, dbname)

def scheming_fetch_all():
    "抓取所有页面功能"
    
    urllist = []
    dbname = alldbname

    startURL = 'http://labaia.ws/browse/'
    urllist = fetchtpb.getallURL(startURL) 

    for url in urllist:
        try:
            fetchtpb.fetch(url, dbname)
        except:
            print 'fetch err url:%s' %(url)
            continue

