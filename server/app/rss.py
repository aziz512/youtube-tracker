import feedparser

def get_rss_url(channel_id):
	return f'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}'

def from_file(filename):
	return feedparser.parse(filename)

def from_channel_id(channel_id):
	return feedparser.parse(get_rss_url(channel_id))
