import feedparser
from .watchlist import Watchlist

rss_url_formats = {
	'youtube': {
		'template': 'https://{}/feeds/videos.xml?channel_id={}',
		'default_site': 'www.youtube.com',
	},
	'invidious': {
		'template': 'https://{}/feed/channel/{}',
		'default_site': 'vid.puffyan.us',
	},
}

def get_rss_url(channel_id, source='youtube', site=None):
	source = source.lower()
	if site is None:
		site = rss_url_formats[source]['default_site']
	return rss_url_formats[source]['template'].format(site, channel_id)

def from_file(filename):
	return feedparser.parse(filename)

def from_channel_id(channel_id):
	return feedparser.parse(get_rss_url(channel_id))

def summery(watchlist_path):
	watchlist = Watchlist(watchlist_path)
	feeds = list(map(from_channel_id,watchlist))
	return feeds
