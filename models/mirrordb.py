#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config.settings import db
from config.settings import alldbname, infodbname
from hashlib import md5
import memcache

mc = memcache.Client(['127.0.0.1:11211'], debug=0)

def add_record(dbname, name = 'N/A', typeL1 = 'none', typeL2 = 'none', magnet = '', size = 'Unknown'):
    "插入记录"
    db.insert(dbname, resource_name = name, typeL1 = typeL1, typeL2 = typeL2, magnet = magnet, size = size)

def get_top_records(typeL1 = 'Audio', typeL2 = None, limit = 100):
    "取得指定类别的记录"
    sql_query = ''
    if typeL2:
#        return db.select(dbname, what = '*, count(distinct magnet)', group = 'magnet', vars = dict(typeL1=typeL1, 
#            typeL2=typeL2, currtime=time.strftime('%Y-%m-%d',time.localtime(time.time()))), 
#            where = 'typeL1=$typeL1 and typeL2=$typeL2 and fetch_time > $currtime', limit=limit).list()
#        return db.select(alldbname, what = '*, count(distinct magnet)', group = 'magnet', vars = dict(typeL1=typeL1, 
#            typeL2 = typeL2), where = 'typeL1=$typeL1 and typeL2=$typeL2', order = 'hotrank DESC, fetch_time DESC', limit=limit).list()            
        
        sql_query = 'select * from ' + alldbname +  ' where typeL1=="' + typeL1 + '" and typeL2=="' + typeL2 + '" order by hotrank DESC,  fetch_time DESC, resource_name ASC limit ' + str(limit) 
    else:
        sql_query = 'select * from ' + alldbname +  ' where typeL1=="' + typeL1 + '" order by hotrank DESC, fetch_time DESC, resource_name ASC limit ' + str(limit) 

    #memcache缓存  
    return _memchache_get_records(sql_query)

def get_hot_types():
    "取得当前热门分类(typeL2)"
    sql_query = 'select typeL1,typeL2,avg(hotrank) from all_resource group by typeL2 order by avg(hotrank) DESC limit 18'
    return _memchache_get_records(sql_query, time = 300)

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

def set_score_value(resource_id, score_type):
    "设置用户评分"
    sql_query = "update " + alldbname +" set " + score_type + "= " + score_type + "+1 where resource_id==" + resource_id
    db.query(sql_query)
    
def get_score_value(resource_id, score_type):
    "获取用户评分"
    sql_query = "select " + score_type + " from " + alldbname + " where resource_id==" + resource_id
    res =   db.query(sql_query).list()[0]
    return str(res[score_type])
        
    
def _memchache_get_records(sql_query, time = 100):
    "memcache缓存,time默认为100分钟"
    
    #hash一下，为了key键分布更均衡
    key = md5(sql_query.encode('UTF-16')).hexdigest()
    res = mc.get(key)
    if not res:
        res = db.query(sql_query).list()
        mc.set(key, res, 60 * time) #存100分钟
        
    return res
