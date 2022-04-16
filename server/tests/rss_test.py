import os
from app.rss import get_rss_url
from app.rss import from_watchlist_item
from app.rss import summarize_feed

def test_get_rss_feed(watchlist):
	feed = [
		'https://www.youtube.com/feeds/videos.xml?channel_id=UCBR8-60-B28hp2BmDPdntcQ',
		'https://vid.puffyan.us/feed/channel/UCsBjURrPoezykLs9EqgamOA',
		'https://inv.riverside.rocks/feed/channel/UCYO_jab_esuFRV4b17AJtAw',
	]
	assert feed == list(map(get_rss_url, watchlist))

def test_get_feed_data(youtube_feed, invidious_feed):
	feeds = [
		( youtube_feed, 'https://www.youtube.com/channel/UCBR8-60-B28hp2BmDPdntcQ' ),
		( invidious_feed, 'https://vid.puffyan.us/channel/UCBR8-60-B28hp2BmDPdntcQ' ),
	]
	for feed, url in feeds:
		assert feed['feed']['title'] == 'YouTube'
		assert feed['feed']['author'] == 'YouTube'
		assert feed['feed']['link'] == url

def test_from_watchlist_item(watchlist):
	if os.getenv('FETCH_TEST') != 'true': return
	item = {
		'name': 'Youtube',
		'id': 'UCBR8-60-B28hp2BmDPdntcQ',
		'source': 'youtube',
		'site': 'www.youtube.com',
	}
	feed = from_watchlist_item(item)
	url = 'https://www.youtube.com/channel/UCBR8-60-B28hp2BmDPdntcQ'
	assert feed['feed']['title'] == 'YouTube'
	assert feed['feed']['author'] == 'YouTube'
	assert feed['feed']['link'] == url

def test_summarize_feed(youtube_feed, invidious_feed):
	feeds = (
		( youtube_feed, 'https://www.youtube.com/channel/UCBR8-60-B28hp2BmDPdntcQ' ),
		( invidious_feed, 'https://vid.puffyan.us/channel/UCBR8-60-B28hp2BmDPdntcQ' ),
	)
	for feed, url in feeds:
		summary = summarize_feed(feed, raise_error=True)
		assert summary['title'] == 'YouTube'
		assert summary['author'] == 'YouTube'
		assert summary['channel_id'] == 'UCBR8-60-B28hp2BmDPdntcQ'
		assert summary['channel_url'] == url

def test_summarize_feed_borked(borked_feed):
	try:
		summarize_feed(borked_feed, raise_error=True)
	except ValueError:
		pass
	assert summarize_feed(borked_feed) is None
