import asyncio
import os
import re
from yt_dlp import YoutubeDL


download_percentage = {}

class DownloadVideo:
	def __init__(self, opts=None):
		def download_hook(d):
			if(d['status'] == 'downloading'):
				download_percentage[self.id] = round(float(d['downloaded_bytes'])/float(d['total_bytes']) * 100, 2)

		default_ydl_opts = {
			'format': 'mp4/bestaudio/best',
			'outtmpl': './downloadedvideos/%(id)s.%(ext)s',
			'progress_hooks': [download_hook]
		}
		self.ydl_opts = opts if opts is not None else default_ydl_opts

	async def download_video(self, id):
		self.id = id
		URL = f'https://www.youtube.com/watch?v={id}'
		ydl_opts = self.ydl_opts
		with YoutubeDL(ydl_opts) as ydl:
			try:
				await asyncio.to_thread(lambda: ydl.download([URL]))
			except:
				return "DownloadError"
		return "Done"
	
	def download_status(self, id):
		res = { "status": "not_found" }
		filename = id + ".mp4"
		try:
			downloaded = os.listdir('./downloadedvideos')
			if filename in downloaded:
				res = { "status": "downloaded", "filename": filename}
			elif id in download_percentage:
				res = { "status": "downloading", "download_percentage": download_percentage[id] }
		except FileNotFoundError as err:
			pass
		return res


class Extractor:
	def __init__(self, regex, group_names):
		# group_names are the names of the values returned by
		# <re.Match>.groups()
		self.regex = re.compile(regex)
		self.group_names = group_names

	def match(self, string):
		result = self.regex.match(string)
		if not result: return None

		attributes = {}
		for name, group in zip(self.group_names, result.groups()):
			if not name: continue
			attributes[name] = group
		return attributes

class ChannelUrlMatcher(Extractor):
	format_string = '{protocol}://{site}/{path}/({target})(/{suffix})?/?'
	path = 'channel'
	target_regex = '[a-zA-Z0-9_-]{24}'
	target_name = 'id'

	def __init__(self, *, protocol='https', site='www.youtube.com', suffix=''):
		# suffix should not have beginning or ending slashes
		self.protocol = protocol
		self.site = site
		regex = self.format_string.format(
			protocol=protocol,
			site=site,
			path=self.path,
			target=self.target_regex,
			suffix=suffix,
		)
		super().__init__(regex, (self.target_name, None))

	async def match_async(self, url):
		return self.match(url)

class ChannelNamedUrlMatcher(ChannelUrlMatcher):
	path = 'c'
	target_regex = '[a-zA-Z0-9_-]+'
	target_name = 'name'

	# This method may make an http(s) request.
	# Use match_async instead.
	def match(self, url):
		result = super().match(url)
		if not result:
			return result
		name = result['name']

		url = f'{self.protocol}://{self.site}/{self.path}/{name}/videos'
		info = extract_info(url)
		if 'uploader_id' in info:
			result['id'] = info['uploader_id']
			return result
		return None #pragma: nocover

	def match_async(self, url):
		return asyncio.to_thread(lambda: self.match(url))

def extract_info(url, opts=None, process=False):
	opts = {} if opts is None else opts
	with YoutubeDL(opts) as ydl:
		try:
			info = ydl.extract_info(url, download=False, process=False)
		except: #pragma: nocover
			return None
		return info
	return None #pragma: nocover

def async_extract_info(*args, **kwargs):
	return asyncio.to_thread(lambda: extract_info(*args, **kwargs))

url_matchers = [
	ChannelUrlMatcher(),
	ChannelUrlMatcher(suffix='featured'),
	ChannelUrlMatcher(suffix='videos'),
	ChannelNamedUrlMatcher(),
	ChannelNamedUrlMatcher(suffix='featured'),
	ChannelNamedUrlMatcher(suffix='videos'),
]

async def url_to_video_id(url):
	for matcher in url_matchers:
		result = await matcher.match_async(url)
		if not result:
			continue
		return result['id']
