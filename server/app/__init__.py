from flask import Flask
from flask_cors import CORS

def create_app():
	app = Flask(__name__)
	CORS(app, origins='http://localhost:*')

	@app.route('/hello_world')
	def hello_world():
		return 'Hello World!'
	return app
