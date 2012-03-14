#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config.settings import db
from config.settings import alldbname, infodbname

def add_record(dbname, name = 'N/A', typeL1 = 'none', typeL2 = 'none', magnet = '', size = 'Unknown'):
    "插入记录"
    db.insert(dbname, resource_name = name, typeL1 = typeL1, typeL2 = typeL2, magnet = magnet, size = size)

def get_top_records(typeL1 = 'Audio', typeL2 = None, limit = 100):
    "取得指定类别的记录"
    if typeL2:
        """
        return db.select(dbname, what = '*, count(distinct magnet)', group = 'magnet', vars = dict(typeL1=typeL1, 
            typeL2=typeL2, currtime=time.strftime('%Y-%m-%d',time.localtime(time.time()))), 
            where = 'typeL1=$typeL1 and typeL2=$typeL2 and fetch_time > $currtime', limit=limit).list()
        """
        return db.select(alldbname, what = '*, count(distinct magnet)', group = 'magnet', vars = dict(typeL1=typeL1, 
            typeL2 = typeL2), where = 'typeL1=$typeL1 and typeL2=$typeL2', order = 'hotrank DESC, fetch_time DESC', limit=limit).list()
    else:
        return db.select(alldbname, what = '*, count(distinct magnet)', group = 'magnet', vars = dict(typeL1=typeL1), 
            where = 'typeL1=$typeL1', order = 'hotrank DESC, fetch_time DESC', limit=limit).list()


def search_all_resource(name, resource_type = 'All', limit=100):
    "全站搜索"
    if resource_type == 'All':
        return db.select(alldbname, where = 'resource_name like "%' + name + '%"', limit = limit).list()
    else:
        return db.select(alldbname, 
            where = 'typeL1 = "' + resource_type + '" and resource_name like "%' + name + '%"', limit = limit).list()

def get_extern_info(resource_id = -1):
    "获取资源的详细信息"
    return db.select(infodbname, where = 'resource_id = ' + str(resource_id)).list()
