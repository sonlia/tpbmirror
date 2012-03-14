#!/usr/bin/env python
# coding: utf-8
import web

database = "database/tpbmirror.db"
db = web.database(dbn='sqlite', db=database)

#数据表名
topdbname = 'top'
alldbname = 'allsource'
infodbname = 'doubaninfo'

render = web.template.render('templates/', cache=False)

web.config.debug = True

config = web.storage(
    static='/static',
    site_name='tpbmirror',
)


web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render

