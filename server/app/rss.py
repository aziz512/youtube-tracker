import feedparser
from .watchlist import Watchlist
from .watchlist import unpack_entry
from .watchlist import url_formats

def get_rss_url(watchlist_item):
	channel_id, source, site = unpack_entry(watchlist_item)
	return url_formats[source]['template'].format(site, channel_id)

def from_file(filename):
	return feedparser.parse(filename)

def from_watchlist_item(watchlist_item):
	return feedparser.parse(get_rss_url(watchlist_item))

def summery(watchlist_path):
	watchlist = Watchlist(watchlist_path)
	feeds = list(map(from_watchlist_item,watchlist))
	return feeds
