from flask import Flask

def create_app():
	app = Flask(__name__)

	@app.route('/hello_world')
	def hello_world():
		return 'Hello World!'
	return app
