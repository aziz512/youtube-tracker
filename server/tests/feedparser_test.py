def test_get_feed_data(feed):
	uri = 'https://www.youtube.com/channel/UCBR8-60-B28hp2BmDPdntcQ'
	assert feed['feed']['title'] == 'YouTube'
	assert feed['feed']['author'] == 'YouTube'
	assert feed['feed']['link'] == uri
