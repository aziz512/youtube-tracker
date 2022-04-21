from flask import jsonify, request
from .watchlist import Watchlist
from . import rss

def _copy_values(target, source, keys):
	for key in keys:
		if key in source:
			target[key] = source[key]

def add_routes(app):
	@app.route('/hello_world')
	def hello_world():
		return 'Hello World!'

	@app.route('/videos_raw')
	def videos_raw():
		return jsonify(rss.raw_feed(app.config['watchlist']))

	@app.route('/videos')
	def videos():
		return jsonify(rss.summarize_watchlist(app.config['watchlist']))

	@app.route('/watchlist', methods=['POST', 'DELETE'])
	def modify_watchlist():
		# only required value is 'id'
		json = request.get_json()
		if 'id' not in json:
			return 'invalid json'
		args = {}
		_copy_values(args, json, ('id', 'source', 'site', 'name'))

		watchlist = Watchlist(app.config['watchlist'])
		if request.method == 'POST':
			watchlist.add_channel(**args)
		if request.method == 'DELETE':
			watchlist.remove_channel(**args)
		watchlist.write()
		return 'success'
