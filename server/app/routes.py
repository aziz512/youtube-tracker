from flask import jsonify, request
from .watchlist import Watchlist
from . import rss
from . import video_download

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
			return '', 400 # bad request
		args = {}
		_copy_values(args, json, ('id', 'source', 'site', 'name'))

		watchlist = Watchlist(app.config['watchlist'])
		if request.method == 'POST':
			watchlist.add_channel(**args)
		if request.method == 'DELETE':
			watchlist.remove_channel(args['id'])
		watchlist.write()
		return '', 200 # ok
	
	@app.route('/download-video', methods=['GET', 'POST'])
	def download_video():
		video_id = request.args.get('videoid')
		if len(video_id) != 11: # yt vids are 11 chars
			return '', 400
		download_status = video_download.download_video(video_id)
		if download_status == 'DownloadError':
			return download_status, 400
		return '', 200
