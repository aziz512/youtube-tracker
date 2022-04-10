import pytest
import feedparser
from app import create_app
from app.watchlist import Watchlist

@pytest.fixture()
def app():
	app = create_app(rss_watchlist='tests/testdata/watchlist')
	return app

@pytest.fixture()
def client(app):
	return app.test_client()

@pytest.fixture()
def feed():
	"""
	Test data is from the official Youtube channel
	https://www.youtube.com/feeds/videos.xml?channel_id=UCBR8-60-B28hp2BmDPdntcQ
	"""
	return feedparser.parse('tests/testdata/rss_feed.txt')

@pytest.fixture()
def watchlist(app):
	return Watchlist(app.config['watchlist'])
