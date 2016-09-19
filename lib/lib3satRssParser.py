# -*- coding: utf-8 -*-
import xbmc
import _utils
import urllib
import re
#import dateutil.parser

def parseVideos(url):
	response = _utils.getUrl(url)
	items = re.compile('<item>(.+?)</item>', re.DOTALL).findall(response)
	list = []
	for item in items:
		if 'media:player' in item:
			xbmc.log(str(item))
			dict = {}
			dict['name'] = re.compile('<title>(.+?)</title>', re.DOTALL).findall(item)[0]
			dict['plot'] = re.compile('<description>(.+?)</description>', re.DOTALL).findall(item)[0]
			dict['url'] = 'http://www.3sat.de/mediathek/xmlservice/web/beitragsDetails?ak=web&id=' + re.compile('<link>(.+?)</link>', re.DOTALL).findall(item)[0].split('?obj=')[-1]
			#dict['url'] = re.compile('<link>(.+?)</link>', re.DOTALL).findall(item)[0]
			dict['duration'] = re.compile('duration="(.+?)"', re.DOTALL).findall(item)[0]
			dict['thumb'] = re.compile('<media:thumbnail url="(.+?)"', re.DOTALL).findall(item)[0]
			dict['type'] = 'video'
			dict['mode'] = 'lib3satPlay'
			list.append(dict)
			xbmc.log(str(dict))
	return list