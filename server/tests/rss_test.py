import os
from app.rss import get_rss_url
from app.rss import from_channel_id

def test_get_rss_feed(watchlist):
	feed = [
		'https://www.youtube.com/feeds/videos.xml?channel_id=UCBR8-60-B28hp2BmDPdntcQ',
		'https://www.youtube.com/feeds/videos.xml?channel_id=UCsBjURrPoezykLs9EqgamOA',
		'https://www.youtube.com/feeds/videos.xml?channel_id=UCYO_jab_esuFRV4b17AJtAw',
	]
	assert feed == list(map(get_rss_url, watchlist))

	invidious_feed = [
		'https://vid.puffyan.us/feed/channel/UCBR8-60-B28hp2BmDPdntcQ',
		'https://vid.puffyan.us/feed/channel/UCsBjURrPoezykLs9EqgamOA',
		'https://vid.puffyan.us/feed/channel/UCYO_jab_esuFRV4b17AJtAw',
	]
	assert invidious_feed == list(map(lambda x: get_rss_url(x, source='Invidious'), watchlist))

def test_get_feed_data(youtube_feed, invidious_feed):
	feeds = [
		( youtube_feed, 'https://www.youtube.com/channel/UCBR8-60-B28hp2BmDPdntcQ' ),
		( invidious_feed, 'https://vid.puffyan.us/channel/UCBR8-60-B28hp2BmDPdntcQ' ),
	]
	for feed, url in feeds:
		assert feed['feed']['title'] == 'YouTube'
		assert feed['feed']['author'] == 'YouTube'
		assert feed['feed']['link'] == url

def test_from_channel_id():
	if os.getenv('FETCH_TEST') != 'true': return
	channel_id = 'UCBR8-60-B28hp2BmDPdntcQ'
	feed = from_channel_id(channel_id)
	test_get_feed_data(feed)
