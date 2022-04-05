import pytest
import feedparser
from app import create_app

@pytest.fixture()
def app():
	app = create_app()
	return app

@pytest.fixture()
def client(app):
	return app.test_client()

@pytest.fixture()
def feed():
	"""
	Test data is from the official Youtube channel
	https://www.youtube.com/feeds/videos.xml?channel_id=UCBR8-60-B28hp2BmDPdntcQ

	This channel features videos from other channels as well as their
	own. This makes it useful for testing edge cases.
	"""
	return feedparser.parse('tests/testdata/rss_feed.txt')
