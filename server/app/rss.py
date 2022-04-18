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

def _in_cursor(key, cursor):
	if isinstance(cursor, list) or isinstance(cursor, tuple):
		if type(key) is int:
			return key >= 0 and key < len(cursor)
	if isinstance(cursor, dict):
		return key in cursor
	return False #pragma: nocover

def _flatten(target, source, target_path, source_path, optional=False):
	if type(target_path) is int or type(target_path) is str:
		target_path = (target_path,)
	if type(source_path) is int or type(source_path) is str:
		source_path = (source_path,)

	cursor = source
	for source_key in source_path:
		correct_types = (list, tuple, dict)
		is_correct_type = any(map(lambda t: isinstance(cursor, t), correct_types))
		if not is_correct_type or not _in_cursor(source_key, cursor): #pragma: nocover
			if not optional:
				raise ValueError('invalid rss feed')
			_assign_path(target, target_path, None)
			return
		cursor = cursor[source_key]
	_assign_path(target, target_path, cursor)

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

		videos = ( summarize_entry(entry, raise_error=raise_error)
					for entry in feed.get('entries', tuple()) )
		videos = list(filter(lambda x: x is not None, videos))
		summary['videos'] = videos

	except ValueError as e:
		if raise_error:
			raise e
		return None
	return summary

# Called by summarize_feed.
# Summarizes an entry in a feed. Each entry is tied to a video.
# Where a feed is tied to a youtube channel.
def summarize_entry(entry, raise_error=False):
	summary = {}
	def reword(summary_path, entry_path, optional=False):
		_flatten(summary, entry, summary_path, entry_path, optional=optional)

	try:
		reword('id', 'yt_videoid')
		reword('title', 'title')
		reword('summary', 'summary')
		reword('thumbnail', ('media_thumbnail', 0, 'url'), optional=True)
	except ValueError as e: #pragma: nocover
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
