import os
import json
from app import create_app
from app.watchlist import Watchlist

def test_hello_world(client):
	response = client.get("/hello_world")
	assert response.data == b'Hello World!'

def test_videos_raw(client):
	# [TODO] REMOVE this line after caching is implemented
	if os.getenv('FETCH_TEST') != 'true': return

	response = client.get('/videos_raw')
	data = json.loads(response.data)
	youtube, fireship, three_blue = list(map(lambda x: x['feed'], data))
	assert youtube['title'] == 'YouTube'
	assert youtube['yt_channelid'] == 'UCBR8-60-B28hp2BmDPdntcQ'

	assert fireship['title'] == 'Fireship'
	assert fireship['yt_channelid'] == 'UCsBjURrPoezykLs9EqgamOA'

	assert three_blue['title'] == '3Blue1Brown'
	assert three_blue['yt_channelid'] == 'UCYO_jab_esuFRV4b17AJtAw'

def test_videos(client):
	# [TODO] REMOVE this line after caching is implemented
	if os.getenv('FETCH_TEST') != 'true': return

	response = client.get('/videos')
	data = json.loads(response.data)

	youtube, fireship, three_blue = data

	assert youtube['channel']['name'] == 'YouTube'
	assert youtube['channel']['id'] == 'UCBR8-60-B28hp2BmDPdntcQ'

	assert fireship['channel']['name'] == 'Fireship'
	assert fireship['channel']['id'] == 'UCsBjURrPoezykLs9EqgamOA'

	assert three_blue['channel']['name'] == '3Blue1Brown'
	assert three_blue['channel']['id'] == 'UCYO_jab_esuFRV4b17AJtAw'

	for entry in data:
		for video in entry['videos']:
			assert type(video['id']) is str
			assert type(video['summary']) is str
			assert type(video['thumbnail']) is str
			assert type(video['title']) is str

def test_modify_watchlist():
	path = 'tests/testdir/test_modify_watchlist.ini'
	if os.path.exists(path):
		os.remove(path)
	app = create_app(rss_watchlist=path)
	client = app.test_client()

	response = client.post('/watchlist', json={
		'name': '3Blue1Brown',
	})
	assert response.data == b''
	assert response.status == '400 BAD REQUEST'

	response = client.post('/watchlist', json={
		'id': 'UCYO_jab_esuFRV4b17AJtAw',
		'name': '3Blue1Brown',
	})
	assert response.data == b''
	assert response.status == '200 OK'

	# add Fireship, default name is channel
	response = client.post('/watchlist', json={
		'id': 'UCsBjURrPoezykLs9EqgamOA',
	})
	assert response.data == b''
	assert response.status == '200 OK'

	response = client.post('/watchlist', json={
		'id': 'UCBR8-60-B28hp2BmDPdntcQ',
		'name': 'Youtube',
	})
	assert response.data == b''
	assert response.status == '200 OK'

	# delete Youtube
	response = client.delete('/watchlist', json={
		'id': 'UCBR8-60-B28hp2BmDPdntcQ',
	})
	assert response.data == b''
	assert response.status == '200 OK'

	# delete 3Blue1Brown
	response = client.delete('/watchlist', json={
		'id': 'UCYO_jab_esuFRV4b17AJtAw',
	})
	assert response.data == b''
	assert response.status == '200 OK'

	watchlist = Watchlist(app.config['watchlist'])
	assert watchlist.channels == [
		{
			'name': 'channel',
			'id': 'UCsBjURrPoezykLs9EqgamOA',
			'source': 'youtube',
			'site': 'www.youtube.com',
		}
	]
	os.remove(path)
