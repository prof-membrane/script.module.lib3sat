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
	videoUrl,subUrl,offset = xmlservice.getVideoUrl(params['url'])
	listitem = xbmcgui.ListItem(path=videoUrl)
	xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
	
def list():	
	
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
	}
views = {
	'lib3satListShows': 'shows',
	'lib3satListVideos': 'videos',
	'lib3satListDate': 'videos',
	'lib3satListDateVideos': 'videos',
	'lib3satListSearch': 'videos'
	}
	