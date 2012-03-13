#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web

db = web.database(dbn='sqlite', db='../database/tpbmirror.db')

def change_allsource_extern_info():
    "修改记录"
    res = db.query('select * from doubaninfo').list()
    for item in res:
        #修改top及allsource 表中的extern_info字段
        db.query('update allsource set extern_info="True" where resource_id =' + str(item['resource_id']))

def change_top_resource_id():
    res = db.query('select * from top').list()
    for item in res:
        re_res = db.select('allsource', where= 'magnet = "' + item['magnet'] + '"').list()
        if re_res:
            db.query('update top set resource_id=' + str(re_res[0]['resource_id']))

if __name__ == '__main__':
    #change_allsource_extern_info()
    change_top_resource_id()
