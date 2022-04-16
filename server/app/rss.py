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

def raw_feed(watchlist_path):
	watchlist = Watchlist(watchlist_path)
	feeds = list(map(from_watchlist_item, watchlist))
	return feeds

def _flatten(summery, feed, summery_key, feed_path, optional=False):
	cursor = feed
	for feed_key in feed_path:
		is_correct_type = isinstance(cursor, list) or isinstance(cursor, dict)
		if not is_correct_type or feed_key not in cursor:
			if not optional:
				raise ValueError('invalid rss feed')
			summery[summery_key] = None
			return
		cursor = cursor[feed_key]
	summery[summery_key] = cursor

def summarize_feed(feed, raise_error=False):
	summery = {}
	def reword(summery_key, feed_path, optional=False):
		_flatten(summery, feed, summery_key, feed_path, optional=optional)

	try:
		if feed.get('bozo', None) is not False:
			raise ValueError('invalid rss feed')
		reword('title', ('feed', 'title'))
		reword('author', ('feed', 'author'))
		reword('channel_id', ('feed', 'yt_channelid'))
		reword('channel_url', ('feed', 'href'))
	except ValueError as e:
		if raise_error:
			raise e
		return None
	return summery

def summerize_watchlist(watchlist_path):
	watchlist = Watchlist(watchlist_path)
	feeds = map(from_watchlist_item,watchlist)
	summaries = [ feed for feed in map(summarize_feed, feeds)
				if feed is not None ]
	return summaries
