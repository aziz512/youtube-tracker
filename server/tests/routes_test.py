import os
import json

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
