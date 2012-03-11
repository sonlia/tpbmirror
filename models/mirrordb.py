#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import time
from BeautifulSoup import BeautifulSoup as BSoup

from config.settings import db
from config.settings import alldbname

def add_record(dbname, name = 'N/A', typeL1 = 'none', typeL2 = 'none', magnet = '', size = 'Unknown'):
    "插入记录"
    db.insert(dbname, resource_name = name, typeL1 = typeL1, typeL2 = typeL2, magnet = magnet, size = size)

def get_records(dbname, typeL1 = 'Audio', typeL2 = None, limit = 200):
    "取得指定类别的记录"
    if typeL2:
        return db.select(dbname, what = '*, count(distinct magnet)', group = 'magnet', vars = dict(typeL1=typeL1, 
            typeL2=typeL2, currtime=time.strftime('%Y-%m-%d',time.localtime(time.time()))), 
            where = 'typeL1=$typeL1 and typeL2=$typeL2 and fetch_time > $currtime', limit=limit).list()
    else:
        return db.select(dbname, what = '*, count(distinct magnet)', group = 'magnet', vars = dict(typeL1=typeL1), 
            where = 'typeL1=$typeL1', limit=limit).list()


def search_all_resource(name, type):
    "全站搜索"
    if type == 'All':
        return db.select(alldbname, where = 'resource_name like "%' + name + '%"', limit = 100).list()
    else:
        return db.select(alldbname, 
            where = 'typeL1 = "' + type + '" and resource_name like "%' + name + '%"', limit = 100).list()

