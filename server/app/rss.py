import feedparser
from .watchlist import Watchlist

def get_rss_url(channel_id):
	return f'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}'

def from_file(filename):
	return feedparser.parse(filename)

def from_channel_id(channel_id):
	print(channel_id)
	return feedparser.parse(get_rss_url(channel_id))

def summery(watchlist_path):
	watchlist = Watchlist(watchlist_path)
	feeds = list(map(from_channel_id,watchlist))
	return feeds
