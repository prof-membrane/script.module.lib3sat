# -*- coding: utf-8 -*-
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib
import lib3satRssParser
import libMediathek
import mediathekxmlservice as xmlservice

from datetime import date, timedelta

translation = xbmcaddon.Addon(id='script.module.libMediathek').getLocalizedString

baseXml = 'http://www.3sat.de/mediathek'


def lib3satListMain():
	list = []
	list.append({'name':translation(31030), 'mode':'lib3satListNew'})
	list.append({'name':translation(31031), 'mode':'lib3satListMV'})
	list.append({'name':translation(31032), 'mode':'lib3satListLetters'})
	list.append({'name':translation(31033), 'mode':'lib3satListDate'})
	#list.append({'name':translation(31034), 'mode':'lib3satListRubrics', 'url':'http://www.zdf.de/ZDFmediathek/xmlservice/web/rubriken'})
	#list.append({'name':translation(31035), 'mode':'lib3satListTopics', 'url':'http://www.zdf.de/ZDFmediathek/xmlservice/web/themen'})
	list.append({'name':translation(31039), 'mode':'lib3satSearch'})
	libMediathek.addEntries(list)
	
	
def lib3satListNew():
	libMediathek.addEntries(xmlservice.getNew(baseXml))
	
def lib3satListMV():
	libMediathek.addEntries(xmlservice.getMostViewed(baseXml))

def lib3satListLetters():
	libMediathek.populateDirAZ('lib3satListShows',['d','e','g','i','j','l','o','p','q','r','u','x','y','z'])
def lib3satListShows():
	letter = params['name'].replace('#','0%2D9')
	libMediathek.addEntries(xmlservice.getXML('http://www.3sat.de/mediathek/xmlservice/web/sendungenAbisZ?characterRangeEnd='+letter+'&detailLevel=2&characterRangeStart='+letter))
	
def lib3satListDate():
	libMediathek.populateDirDate('lib3satListDateVideos')
def lib3satListDateVideos():
	from datetime import date, timedelta
	day = date.today() - timedelta(int(params['datum']))
	ddmmyy = day.strftime('%d%m%y')
	url = 'http://www.3sat.de/mediathek/xmlservice/web/sendungVerpasst?startdate='+ddmmyy+'&enddate='+ddmmyy+'&maxLength=50'
	libMediathek.addEntries(xmlservice.getXML(url,type='date')[::-1])
	
def lib3satListRubrics():#not supported by the mediathek
	libMediathek.addEntries(xmlservice.getRubrics(baseXml))
	
def lib3satListTopics():#not supported by the mediathek
	libMediathek.addEntries(xmlservice.getTopics(baseXml))
	
def lib3satSearch():
	keyboard = xbmc.Keyboard('', translation(31039))
	keyboard.doModal()
	if keyboard.isConfirmed() and keyboard.getText():
		search_string =  urllib.quote_plus(keyboard.getText())
		libMediathek.addEntries(xmlservice.getXML("http://www.zdf.de/ZDFmediathek/xmlservice/web/detailsSuche?maxLength=50&types=Video&properties=HD%2CUntertitel%2CRSS&searchString="+search_string))
def xmlListPage():
	libMediathek.addEntries(xmlservice.getXML(params['url']))
	
def xmlPlay():
	xbmc.log('xmlplay')
	videoUrl,subUrl,offset = xmlservice.getVideoUrl(params['url'])
	listitem = xbmcgui.ListItem(path=videoUrl)
	xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
	

"""	
def lib3satListShows():
	letter = params['name'].replace('#','0%2D9')
	libMediathek.addEntries(xmlservice.getXML('http://www.3sat.de/mediathek/xmlservice/web/sendungenAbisZ?characterRangeEnd='+letter+'&detailLevel=2&characterRangeStart='+letter))
	import lib3satAZ
	letters2shows = {
	'#':lib3satAZ.number,
	'a':lib3satAZ.a,
	'b':lib3satAZ.b,
	'c':lib3satAZ.c,
	'f':lib3satAZ.f,
	'h':lib3satAZ.h,
	'k':lib3satAZ.k,
	'm':lib3satAZ.m,
	'n':lib3satAZ.n,
	's':lib3satAZ.s,
	't':lib3satAZ.t,
	'v':lib3satAZ.v,
	'w':lib3satAZ.w,
	}
	#xbmc.log(str(letters2shows.get(params['name'].lower(),[])))
	libMediathek.addEntries(letters2shows.get(params['name'].lower(),[]))
"""

"""	
def lib3satListVideos():
	show = params['url'].split('?red=')[-1]
	url = 'http://www.3sat.de/mediaplayer/rss/mediathek_' + show + '.xml'
	libMediathek.addEntries(parseRss(url))
"""
	

"""
def lib3satSearch():
	keyboard = xbmc.Keyboard('', translation(31039))
	keyboard.doModal()
	if keyboard.isConfirmed() and keyboard.getText():
		search_string = keyboard.getText()
		lib3satListSearch(search_string)
"""
"""
def lib3satListSearch(searchString=False):
	if not searchString:
		searchString = params['searchString']
	libMediathek.addEntries(search(searchString))
"""
"""
def lib3satPlay():
	import libZdf
	libZdf.libZdfPlay(params)
"""
"""
def parseRss(url):
	return lib3satRssParser.parseVideos(url)
"""
"""
def play(dict):
	url = getVideoUrl(dict["url"])
	#listitem = xbmcgui.ListItem(label=video["name"],thumbnailImage=video["thumb"],path=url)
	listitem = xbmcgui.ListItem(label=dict["name"],path=url)
	xbmc.Player().play(url, listitem)	
"""
"""
def lib3satPvrPlay(dict):
	import lib3satPvr
	lib3satPvr.play(dict)
"""	
def list():	
	modes = {
	'lib3satListNew': lib3satListNew,
	'lib3satListMV': lib3satListMV,
	'xmlListPage': xmlListPage,
	'xmlPlay': xmlPlay,
	'lib3satListRubrics': lib3satListRubrics,
	'lib3satListTopics': lib3satListTopics,
	'lib3satListLetters': lib3satListLetters,
	'lib3satListShows': lib3satListShows,
	'lib3satListDate': lib3satListDate,
	'lib3satListDateVideos': lib3satListDateVideos,
	'lib3satSearch': lib3satSearch,
	
	#'lib3satListVideos': lib3satListVideos,
	#'lib3satListSearch': lib3satListSearch,
	#'lib3satPlay': lib3satPlay
	}
	views = {
	'lib3satListShows': 'shows',
	'lib3satListVideos': 'videos',
	'lib3satListDate': 'videos',
	'lib3satListDateVideos': 'videos',
	'lib3satListSearch': 'videos'
	}
	global params
	params = libMediathek.get_params()
	global pluginhandle
	pluginhandle = int(sys.argv[1])
	
	if not params.has_key('mode'):
		lib3satListMain()
	else:
		modes.get(params['mode'],lib3satListMain)()
		libMediathek.setView(views.get(params['mode'],'default'))
	xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=True)	