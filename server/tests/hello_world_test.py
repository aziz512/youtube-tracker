import sys

def test_hello_world(client):
	response = client.get("/hello_world")
	assert response.data == b'Hello World!'
