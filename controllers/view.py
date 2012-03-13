#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
from config.settings import render
from config.settings import topdbname
from models import mirrordb

class index():
    "显示主页面"
    def GET(self):
        return render.index()

class topview():
    "显示Top100的检索页面"
    def GET(self):
        results = mirrordb.get_records(topdbname)
        return render.view(results)

class searchview():
    "显示搜索结果页"
    def GET(self):
        search_type = web.input().searchtype
        search_name = web.input().searchname 
        results = mirrordb.search_all_resource(type = search_type, name = search_name)
        return render.view(results)

class typeview():
    "根据传入的url决定检索的类别，如访问toptpb/Audio/Music，则表示检索/Audio/Music项"
    def GET(self):
        urltypes = web.ctx.path.split('/')[2:]
        typeL1 = urltypes[0] 
        typeL2 = (len(urltypes) > 1) and urltypes[1] or None

        #如果url中有'_'符号，替换为空格
        typeL1 = typeL1.replace('_', ' ')
        if typeL2:
            typeL2 = typeL2.replace('_', ' ')

        results = mirrordb.get_records(topdbname, typeL1, typeL2)
        return render.view(results)
    
class resource_info():
    "根据传入的resource_id检索资源信息"
    def GET(self):
        try:
            resource_id = int(web.ctx.path.split('/')[2])
            result = mirrordb.get_extern_info(resource_id)
            return render.resource_info(result[0])
        except:
            pass
            return render.error("没有找到您要的信息，我们会尽快录入", None)
        

if __name__ == '__main__':
    topview.GET()
