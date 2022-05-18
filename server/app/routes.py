import asyncio
from flask import jsonify, request
from .watchlist import Watchlist
from . import rss
from .video_download import DownloadVideo, url_to_video_id, async_extract_info

def _copy_values(target, source, keys):
	for key in keys:
		if key in source:
			target[key] = source[key]

def add_routes(app):
	@app.route('/hello_world')
	def hello_world():
		return 'Hello World!'

	@app.route('/videos_raw')
	async def videos_raw():
		feed = await asyncio.to_thread(lambda: rss.raw_feed(app.config['watchlist']))
		return jsonify(feed)

	@app.route('/videos')
	async def videos():
		summarize_func = lambda: rss.summarize_watchlist(app.config['watchlist'])
		summary = await asyncio.to_thread(summarize_func)
		return jsonify(summary)

	async def is_invalid_id(id):
		url = f'https://www.youtube.com/channel/{id}'
		info = await async_extract_info(url)
		return info is None or 'uploader_id' not in info or info['uploader_id'] != id

	@app.route('/watchlist', methods=['POST', 'DELETE'])
	async def modify_watchlist():
		# only required value is 'id'
		json = request.get_json()
		if 'id' not in json and 'url' not in json:
			return 'requires the fields "id" or "url" to specify which channel to add', 400 # bad request
		if 'id' in json and 'url' in json:
			return '"id" and "url" are mutually exclusive', 400 # bad request

		args = {}
		if 'id' in json:
			_copy_values(args, json, ('id', 'source', 'site', 'name'))
		if 'url' in json:
			id = await url_to_video_id(json['url'])
			if id is None: #pragma: nocover
				# channel id is not found
				return "couldn't extract channel id from url", 404 # Not Found
			args['id'] = id

		watchlist = Watchlist(app.config['watchlist'])
		if request.method == 'POST':
			if 'id' in json and await is_invalid_id(args['id']):
				return 'Channel id is invalid', 404
			watchlist.add_channel(**args)
			feed = await asyncio.to_thread(lambda: rss.from_watchlist_item(watchlist[args['id']]))
			watchlist.write()
			return jsonify(rss.summarize_feed(feed)), 200 # ok
		if request.method == 'DELETE':
			watchlist.remove_channel(args['id'])
		watchlist.write()
		return '', 200 # ok
	
	@app.route('/download-video', methods=['GET', 'POST'])
	async def download_video():
		video_id = request.args.get('videoid')
		if len(video_id) != 11: # yt vids are 11 chars
			return 'invalid video id', 400

		def download_hook(d):
			if(d['status'] == 'downloading'):
				percentage = round(float(d['downloaded_bytes'])/float(d['total_bytes']) * 100, 2)

		ydl_opts = {
			'format': 'mp4/bestaudio/best',
			'outtmpl': './downloadedvideos/%(id)s.%(ext)s',
			'progress_hooks': [download_hook]
		}
		download_video = DownloadVideo(ydl_opts)
		download_status = await download_video.download_video(video_id)
		return jsonify(download_status, 400) if download_status == 'DownloadError' else jsonify('', 200)

	@app.route('/download-status', methods=['GET', 'POST'])
	async def download_status():
		video_id = request.args.get('videoid')
		if len(video_id) != 11: 
			return 'invalid video id', 400
		return jsonify(DownloadVideo().download_status(video_id))
		

