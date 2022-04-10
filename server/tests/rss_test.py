from app.rss import get_rss_url

def test_get_rss_feed(watchlist):
	feed = [
		'https://www.youtube.com/feeds/videos.xml?channel_id=UCBR8-60-B28hp2BmDPdntcQ',
		'https://www.youtube.com/feeds/videos.xml?channel_id=UCsBjURrPoezykLs9EqgamOA',
		'https://www.youtube.com/feeds/videos.xml?channel_id=UCYO_jab_esuFRV4b17AJtAw',
	]
	assert feed == list(map(get_rss_url, watchlist))
