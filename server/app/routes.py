"""
Backend api

GET /videos_raw
  returns raw rss feed data

GET /videos
  returns
  [
    {
      "channel": {
                   "id": <channel_id>,
                   "name": <channel_name>,
                   "url": <channel_url>
                 },
      "videos": [
        {
          "id": <video_id>,
          "summary": <video_summary>,
          "thumbnail": <thumbnail_url>,
          "title": <video_title>
        },
        ...
      ]
    },
    ...
  ]

GET, POST /download-video
  Request arguments: "videoid".
  Returns status + (code: 400) on error.
  Returns (code: 200) on success.

POST, DELETE /watchlist
  Request arguments: "id" or "url"
    "id" is a youtube channel id.
    "url" is a url to a youtube channel page.
  Adds or removes a channel from the watchlist.
  Returns (code: 400) if arguments are invalid.
  Returns (code: 404) if channel lookup has failed.
  Returns (code: 200) on success.
"""

import asyncio
from flask import jsonify, request, send_from_directory
from .watchlist import Watchlist
from . import rss
from .video_download import DownloadVideo, url_to_video_id, async_extract_info

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
			args['id'] = json['id']
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

		download_video = DownloadVideo()
		download_status = await download_video.download_video(video_id)
		return (jsonify(download_status), 400) if download_status == 'DownloadError' else (jsonify(''), 200)

	@app.route('/download-status', methods=['GET', 'POST'])
	async def download_status():
		video_id = request.args.get('videoid')
		if len(video_id) != 11: 
			return 'invalid video id', 400
		return jsonify(DownloadVideo().download_status(video_id))
	
	@app.route('/downloads/<path:name>')
	def serve_video(name):
		return send_from_directory(
			'../downloadedvideos', name, as_attachment=False
		)

