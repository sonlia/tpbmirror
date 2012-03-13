#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config.settings import db
from config.settings import render
from fetchtpb import gettopURL
import scheming


class testdb():
    
    def GET(self):
        db.insert('top', resource_name = u'MagicZhang', typeL1 = 'movie',typeL2 = 'kongfu', magnet='zz', size='10B')

class testgetURL():
    
    def GET(self):
        return render.test(gettopURL('http://labaia.ws/top'))

class testfetchtop():
    
    def GET(self):
        scheming.scheming_fetch_top()

class testfetchall():

    def GET(self):
        scheming.scheming_fetch_all()

if __name__ == '__main__':
    a = testfetchall()
    a.GET()