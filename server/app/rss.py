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

def _assign_path(dic, path, item):
	cursor = dic
	for key in path[:-1]:
		if key in cursor:
			cursor = cursor[key]
		else:
			cursor[key] = {}
			cursor = cursor[key]
	cursor[path[-1]] = item

def _flatten(summary, feed, summary_path, feed_path, optional=False):
	cursor = feed
	for feed_key in feed_path:
		is_correct_type = isinstance(cursor, list) or isinstance(cursor, dict)
		if not is_correct_type or feed_key not in cursor:
			if not optional:
				raise ValueError('invalid rss feed')
			_assign_path(summary, summary_path, None)
			return
		cursor = cursor[feed_key]
	_assign_path(summary, summary_path, cursor)

def summarize_feed(feed, raise_error=False):
	summary = {}
	def reword(summary_path, feed_path, optional=False):
		_flatten(summary, feed, summary_path, feed_path, optional=optional)

	try:
		if feed.get('bozo', None) is not False:
			raise ValueError('invalid rss feed')
		reword(('channel', 'name'), ('feed', 'title'))
		reword(('channel', 'id')  , ('feed', 'yt_channelid'))
		reword(('channel', 'url') , ('feed', 'href'))
	except ValueError as e:
		if raise_error:
			raise e
		return None
	return summary

def summarize_watchlist(watchlist_path):
	watchlist = Watchlist(watchlist_path)
	feeds = map(from_watchlist_item,watchlist)
	summaries = [ feed for feed in map(summarize_feed, feeds)
				if feed is not None ]
	return summaries
