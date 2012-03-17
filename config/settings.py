#!/usr/bin/env python
# coding: utf-8
import web
import models

database = "database/tpbmirror.db"
#database = "database/tpbmirror.db"
db = web.database(dbn='sqlite', db=database)

#数据表名
alldbname = 'all_resource'
infodbname = 'resource_info'

render = web.template.render('templates/', cache=False)

web.config.debug = True

config = web.storage(
    static='/static',
    site_name='simpletpb',
)

web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render

