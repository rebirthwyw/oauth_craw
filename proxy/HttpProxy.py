#!/usr/bin/env python
#-*- coding:utf-8 -*- 
# author: rebirth
# e-mail: rebirthwyw@gmail.com
# time: 2018-05-07 19:12:32

import mitmproxy
from model import OauthCraw
import re
import urllib.parse

class HandleReq:
	def __init__(self):
		self.db = OauthCraw()
		self.task = ""
		self.req= ""
		self.patterns = [{"service":"500px","pattern":"api\.500px\.com\/v[0-9\.]+\/oauth\/request_token"},
{"service":"Amazon","pattern":"www\.amazon\.com\/ap\/oa"},
{"service":"AOL","pattern":"api\.login\.aol\.com\/oauth2\/request_auth"},
{"service":"Autodesk","pattern":"developer\.api\.autodesk\.com\/authentication\/v[0-9\.]+\/authorize"},
{"service":"Basecamp","pattern":"launchpad\.37signals\.com\/authorization\/new"},
{"service":"Battle\.net","pattern":"battle\.net\/oauth\/authorize|www\.battlenet\.com\.cn\/oauth\/authorize"},
{"service":"Bitbucket","pattern":"bitbucket\.org\/site\/oauth2\/authorize"},
{"service":"bitly","pattern":"bitly\.com\/oauth\/authorize"},
{"service":"Box","pattern":"account\.box\.com\/api\/oauth2\/authorize"},
{"service":"Dailymotion","pattern":"www\.dailymotion\.com\/oauth\/authorize"},
{"service":"Deutsche Telekom","pattern":"accounts\.login\.idm\.telekom\.com\/oauth2\/auth"},
{"service":"deviantART","pattern":"www\.deviantart\.com\/oauth2\/authorize"},
{"service":"Discogs","pattern":"api\.discogs\.com\/oauth\/request_token"},
{"service":"Dropbox","pattern":"www\.dropbox\.com\/oauth2\/authorize"},
{"service":"Etsy","pattern":"openapi\.etsy\.com\/v[0-9\.]+\/oauth\/request_token"},
{"service":"Evernote","pattern":"sandbox\.evernote\.com\/oauth"},
{"service":"Facebook","pattern":"www\.facebook\.com\/v[0-9\.]+\/dialog\/oauth"},
{"service":"Fitbit","pattern":"www\.fitbit\.com\/oauth2\/authorize"},
{"service":"Flickr","pattern":"www\.flickr\.com\/services\/oauth\/request_token"},
{"service":"Formstack","pattern":"www\.formstack\.com\/api\/v[0-9\.]+\/oauth2\/authorize"},
{"service":"Foursquare","pattern":"foursquare\.com\/oauth2\/authenticate"},
{"service":"GitHub","pattern":"github\.com\/login\/oauth\/authorize"},
{"service":"Goodreads","pattern":"www\.goodreads\.com\/oauth\/request_token"},
{"service":"Google","pattern":"accounts\.google\.com\/signin\/oauth"},
{"service":"Groundspeak","pattern":"geocaching\.com\/oauth\/authorize\.aspx"},
{"service":"Huddle","pattern":"login\.huddle\.net\/request"},
{"service":"Imgur","pattern":"api\.imgur\.com\/oauth2\/authorize"},
{"service":"Instagram","pattern":"api\.instagram\.com\/oauth\/authorize"},
{"service":"LinkedIn","pattern":"www\.linkedin\.com\/oauth\/v[0-9\.]+\/authorization"},
{"service":"Microsoft","pattern":"login\.microsoftonline\.com\/[a-z0-9A-Z\.-]+\/oauth2\/authorize"},
{"service":"Mixi","pattern":"mixi\.jp\/connect_authorize\.pl"},
{"service":"Passport","pattern":"www\.provider\.com\/oauth\/request_token|www\.provider\.com\/oauth2\/authorize"},
{"service":"Plurk","pattern":"www\.plurk\.com\/OAuth\/request_token"},
{"service":"Reddit","pattern":"www\.reddit\.com\/api\/v[0-9\.]+\/authorize"},
{"service":"Salesforce","pattern":"login\.salesforce\.com\/_nc_external\/system\/security\/oauth\/RequestTokenHandler|login\.salesforce\.com\/services\/oauth2\/authorize"},
{"service":"Sina Weibo","pattern":"api\.weibo\.com\/oauth2\/authorize"},
{"service":"Stack Exchange","pattern":"stackoverflow\.com\/oauth|stackoverflow\.com\/oauth\/dialog"},
{"service":"Strava","pattern":"www\.strava\.com\/oauth\/authorize"},
{"service":"Stripe","pattern":"connect\.stripe\.com\/oauth\/authorize"},
{"service":"Trello","pattern":"trello\.com\/1\/OAuthGetRequestToken"},
{"service":"Tumblr","pattern":"www\.tumblr\.com\/oauth\/request_token"},
{"service":"Twitch","pattern":"id\.twitch\.tv\/oauth2\/authorize"},
{"service":"Twitter","pattern":"api\.twitter\.com\/oauth\/request_token|api\.twitter\.com\/oauth\/authenticate"},
{"service":"Vimeo","pattern":"api\.vimeo\.com\/oauth\/authorize|api\.vimeo\.com\/oauth\/authorize\/client"},
{"service":"Vk","pattern":"oauth\.vk\.com\/authorize"},
{"service":"Withings","pattern":"account\.withings\.com\/oauth2_user\/authorize2"},
{"service":"Yahoo!","pattern":"api\.login\.yahoo\.com\/oauth2\/request_auth"},
{"service":"Yammer","pattern":"www\.yammer\.com\/oauth2\/authorize"},
{"service":"Yandex","pattern":"oauth\.yandex\.com\/authorize"},
{"service":"Zendesk","pattern":"zendesk\.com\/oauth\/authorizations\/new"},
{"service":"Tecent QQ","pattern":"graph\.qq\.com\/oauth2\.0\/show"},
{"service":"Wechat","pattern":"open\.weixin\.qq\.com\/connect\/qrconnect"},
{"service":"mail\.ru","pattern":"connect\.mail\.ru\/oauth\/authorize"},
{"service":"jd","pattern":"openlogin\.jd\.com\/oauth2\/login"},
{"service":"baidu","pattern":"openapi\.baidu\.com\/oauth\/2\.0\/authorize"}]
		return

	def request(self, flow: mitmproxy.http.HTTPFlow):
		uri = flow.request.path
		if uri.find("a_new_task_here_rebirth") != -1:
			ref = flow.request.path
			pos = ref.find("?url=")
			if (pos != -1):
				ref = ref[pos+5:]
			self.task = ref
			self.task = urllib.parse.unquote(self.task)
			flow.response = mitmproxy.http.HTTPResponse.make(404)
			#print("bingo")
			return
		if uri.find("a_new_req_here_rebirth") != -1:
			ref = flow.request.path
			pos = ref.find("?url=")
			if (pos != -1):
				ref = ref[pos+5:]
			self.req = ref
			self.req = urllib.parse.unquote(self.req)
			flow.response = mitmproxy.http.HTTPResponse.make(404)
			#print("bingo")
			return
		# if self.task != "":
		# 	print(self.task)
		# 	flow.request.headers["Referer"] = self.task
		url = flow.request.host + uri
		for pattern in self.patterns:
			if re.search(pattern["pattern"], url):
				self.db.insert(self.task, 1, pattern["service"], url, self.req)
				break
		return


addons = [
    HandleReq()
]