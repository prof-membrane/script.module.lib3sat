# -*- coding: utf-8 -*-
#Python 3.5!!!!!!
#import xbmc
#import _utils
import urllib
import re
from urllib.request import urlopen
#import dateutil.parser

def getUrl(url):
	r = urlopen(url)
	#print(r.read().decode('utf-8'))
	return r.read().decode('utf-8')
def unesc(string):
	from HTMLParser import HTMLParser  # python 2.x
	return HTMLParser().unescape(string)
	
def cleanString(s):
  s = s.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&#034;", "\"").replace("&#039;", "'").replace("&quot;", "\"").replace("&szlig;", "ß").replace("&ndash;", "-")
  s = s.replace("&Auml;", "Ä").replace("&Uuml;", "Ü").replace("&Ouml;", "Ö").replace("&auml;", "ä").replace("&uuml;", "ü").replace("&ouml;", "ö").replace("&eacute;", "é").replace("&egrave;", "è")
  s = s.replace("&#x00c4;","Ä").replace("&#x00e4;","ä").replace("&#x00d6;","Ö").replace("&#x00f6;","ö").replace("&#x00dc;","Ü").replace("&#x00fc;","ü").replace("&#x00df;","ß")
  s = s.replace("&apos;","'").strip()
  return s
def scrapeAZ(url='http://www.3sat.de/mediathek/?mode=sendungenaz'):
	url = 'http://www.3sat.de/mediathek/?mode=sendungenaz1'
	response = getUrl(url)
	#match = re.compile('<item>(.+?)</item>', re.DOTALL).findall(response)
	#match = re.compile('<div class="mediatheklistboxfirst_hover">.+?href="(.+?)".+?src="(.+?)".+?<a.+?>(.+?)</a>.+?<a.+?>(.+?)</a>', re.DOTALL).findall(response)
	match = re.compile('<div class="BoxPicture MediathekListPic">.+?href="(.+?)".+?src="(.+?)".+?<a.+?>(.+?)</a>.+?<a.+?>(.+?)</a>', re.DOTALL).findall(response)
	letter = ''
	string = ''
	for url,thumb,name,plot in match:
		if name[0].lower() != letter:
			if letter != '':
				print('	]')
			letter = name[0].lower()
			
			print(letter + ' = [')
		print('	{"name":"' + cleanString(name) + '", "url":"' + url + '", "thumb":"http://www.3sat.de' + thumb.replace('161x90.jpg','big.jpg') + '", "plot":"' + cleanString(plot) + '"},')
		#print(url)
		#print(thumb)
		#print(cleanString(name))
		#print(cleanString(plot))
	print('	]')
scrapeAZ()
