import os
import json

def test_hello_world(client):
	response = client.get("/hello_world")
	assert response.data == b'Hello World!'

def test_videos(client):
	# [TODO] REMOVE this line after caching is implemented
	if os.getenv('FETCH_TEST') != 'true': return

	response = client.get('/videos')
	data = json.loads(response.data)
	youtube, fireship, three_blue = list(map(lambda x: x['feed'], data))
	assert youtube['title'] == 'YouTube'
	assert youtube['author'] == 'YouTube'

	assert fireship['title'] == 'Fireship'
	assert fireship['author'] == 'Fireship'

	assert three_blue['title'] == '3Blue1Brown'
	assert three_blue['author'] == '3Blue1Brown'
