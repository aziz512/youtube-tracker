import asyncio
import re
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

class DownloadVideo:
	def __init__(self, opts):
		self.ydl_opts = opts

	async def download_video(self, id):
		URL = f'https://www.youtube.com/watch?v={id}'
		ydl_opts = self.ydl_opts
		with YoutubeDL(ydl_opts) as ydl:
			try:
				await asyncio.to_thread(lambda: ydl.download([URL]))
			except DownloadError:
				return "DownloadError"
		return "Done"

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
		except DownloadError: #pragma: nocover
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
