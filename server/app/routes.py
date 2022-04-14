from flask import jsonify
from . import rss

def add_routes(app):
	@app.route('/hello_world')
	def hello_world():
		return 'Hello World!'

	@app.route('/videos_raw')
	def videos_raw():
		return jsonify(rss.summery(app.config['watchlist']))
