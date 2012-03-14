#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
import time
from xml.dom import minidom


class CFetchDouban():
    
    _movie_info = {}
    _music_info = {}
    _book_info = {}
    
    support_type = {'Audio':'http://api.douban.com/music/subjects',
                    'Movie':'http://api.douban.com/movie/subjects',
                    'Other':'http://api.douban.com/book/subjects'
                    }
    
    def __init__(self, resource_name, resource_type):
        self.rname = resource_name
        self.rtype = resource_type
        #音乐(Audio)，电影(Movie)，书籍 (other)
        query_url = self.support_type[self.rtype] + '?q=' + self.rname + '&max-results=1'
        try:
            self.rxml = minidom.parseString(urllib2.urlopen(query_url, timeout=10).read()) 
        except:
            print 'Search url failed, url:%s' % (query_url)
            
    def get_movie_info(self):
        try:
            real_xml_url = self.rxml.documentElement.getElementsByTagName('id')[0].childNodes[0].data
            doc = urllib2.urlopen(real_xml_url, timeout=10).read()
            real_xml_dom = minidom.parseString(doc).documentElement
    
            #获取信息
            db_attribute_list = real_xml_dom.getElementsByTagName('db:attribute')
            for item in db_attribute_list:
                if item.getAttribute('name') == u'pubdate':
                    self._movie_info['pubdate'] = item.childNodes[0].data
                elif item.getAttribute('name') == u'country':
                    self._movie_info['country'] = item.childNodes[0].data
                elif item.getAttribute('name') == u'director':
                    self._movie_info['director'] = item.childNodes[0].data 
                elif item.getAttribute('name') == u'aka':
                    self._movie_info['aka'] = item.childNodes[0].data                 
    
            try:
                self._movie_info['summary'] = real_xml_dom.getElementsByTagName('summary')[0].childNodes[0].data
                self._movie_info['doubanURL'] = real_xml_dom.getElementsByTagName('link')[1].getAttribute('href')
                self._movie_info['imgURL'] = real_xml_dom.getElementsByTagName('link')[2].getAttribute('href')
                self._movie_info['rating'] = real_xml_dom.getElementsByTagName('gd:rating')[0].getAttribute('average')
            except:
                print 'get movie info Err, url:%s' % (real_xml_url)
                return None

            return self._movie_info
        except:
            print "Err, Don't find the movie"
            return None
    
import web
 
if __name__ == '__main__':
    database = "../database/tpbmirror.db"
    db = web.database(dbn='sqlite', db=database)   
    res = db.select('allsource', where='resource_id>10300 and typeL2="TV shows" or typeL2="Movies" and resource_id>10300').list()
    #res = db.query('select * from allsource where allsource.resource_id not in (select resource_id from doubaninfo) and typeL1="Video" and typeL2="Movies" or typeL2="TV shows"')
    for item in res:
        if db.select('doubaninfo', where='resource_id = "' + str(item['resource_id']) + '"'):
            continue;
        name = item['resource_name']
        pattern = re.compile(r'\w{4,}(?=(\-|\[|1080p|BDRip|\(HD|\(\d+|\(720|TS|DvDRip|720p)*)')
        match = pattern.match(name) and pattern.match(name).group() or name
        print match
        movie_info = CFetchDouban(match, 'Movie').get_movie_info()
        if movie_info:
            try:
                print movie_info
                db.insert('doubaninfo', resource_id=item['resource_id'], typeL1='Video',
                          pubdate=movie_info['pubdate'], summary=movie_info['summary'], country=movie_info['country'],
                          director=movie_info['director'], aka=movie_info['aka'], doubanURL=movie_info['doubanURL'],
                          imgURL=movie_info['imgURL'], rating=float(movie_info['rating']))
            except:           
                print 'Err, insert db failed' 
                pass
            
        time.sleep(8)

