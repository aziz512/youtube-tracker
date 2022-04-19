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
		assert summary['channel']['name'] == 'YouTube'
		assert summary['channel']['id'] == 'UCBR8-60-B28hp2BmDPdntcQ'
		assert summary['channel']['url'] == url

def test_summarize_feed_videos_youtube(youtube_feed):
	summary = summarize_feed(youtube_feed)
	videos = summary['videos']
	assert len(videos) == 15
	videos[0]['id'] == 'MfWpA5ZV6Lo'
	videos[0]['title'] == 'ready for front row access to Coachella? 🌴'
	videos[0]['thumbnail'] == 'https://i2.ytimg.com/vi/MfWpA5ZV6Lo/hqdefault.jpg'
	videos[0]['summary'] == 'catch the livestream, follow the artists, &amp; get front row access to @Coachella with YouTube, starting April 15 at 4PM PT 🎶'

def test_summarize_feed_videos_invidious(invidious_feed):
	summary = summarize_feed(invidious_feed)
	videos = summary['videos']
	assert len(videos) == 15
	videos[6]['id'] == 'EYXDuiLcWsY'
	videos[6]['title'] == '#youtubecoachellasweepstakes | Enter to win liftetime Coachella tickets from YouTube Shorts #Shorts'
	videos[6]['thumbnail'] == 'https://vid.puffyan.us/vi/EYXDuiLcWsY/mqdefault.jpg'
	videos[6]['summary'] == """Get your chance to win lifetime tickets to Coachella from YouTube Shorts. To enter, just create a Short telling us who your dream +1 would be if you won Coachella tickets for life, and use the hashtag #youtubecoachellasweepstakes. See full rules at the link below.

No purchase necessary. US only. 14+. Ends 4/30/22. See official rules here: yt.be/coachellasweeps"""

def test_summarize_feed_borked(borked_feed):
	try:
		summarize_feed(borked_feed, raise_error=True)
	except ValueError:
		pass
	assert summarize_feed(borked_feed) is None
