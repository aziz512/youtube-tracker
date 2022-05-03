import os.path
from sys import stderr
from configparser import ConfigParser

url_formats = {
	'youtube': {
		'template': 'https://{}/feeds/videos.xml?channel_id={}',
		'default_site': 'www.youtube.com',
	},
	'invidious': {
		'template': 'https://{}/feed/channel/{}',
		'default_site': 'vid.puffyan.us',
	},
}

class Watchlist:
	def __init__(self, file_path):
		self.__is_invalid = False
		self.path = file_path
		parser = ConfigParser()
		parser.read(file_path)
		channels = {}
		for id in parser.sections():
			if not self.is_valid_id(id):
				continue
			entry = parser[id]

			if 'name' not in entry:
				name = 'channel' #pragma nocover
			else:
				name = entry['name']

			if 'source' not in entry:
				source = 'youtube'
			else:
				source = entry['source'].lower()

			if source not in url_formats:
				self.__is_invalid = True
				continue

			if 'site' not in entry:
				site = url_formats[source]['default_site']
			else:
				site = entry['site']

			channels[id] = {
				'name': name,
				'source': source,
				'site': site,
			}
		self.channels = channels

	def __iter__(self):
		for id in self.channels:
			channel = self.channels[id].copy()
			channel['id'] = id
			yield channel

	def __contains__(self, id):
		return id in self.channels

	def __getitem__(self, id):
		channel = self.channels[id].copy()
		channel['id'] = id
		return channel

	def is_invalid(self):
		return self.__is_invalid

	def write(self):
		self.write_watchlist(self, self.path)

	def add_channel(self, id=None, source='youtube', site=None, name='channel'):
		if id is None:
			raise TypeError('Missing keyword argument "id", string expected')
		source = source.lower()
		if source not in url_formats:
			raise ValueError('source not in url formats')
		if site is None:
			site = url_formats[source]['default_site']
		self.channels[id] = {
			'name': name,
			'source': source,
			'site': site,
		}

	def remove_channel(self, id):
		if id in self.channels:
			del self.channels[id]
			return True
		return False

	@staticmethod
	def is_valid_id(id):
		if len(id) != 24:
			return False
		for char in id.lower():
			if char not in 'abcdefghijklmnopqrstuvwxyz0123456789-_':
				return False
		return True

	@staticmethod
	def write_watchlist(watchlist, path):
		config = ConfigParser()
		for channel in watchlist:
			config[channel['id']] = {
				'name': channel['name'],
				'source': channel['source'],
				'site': channel['site'],
			}
		with open(path, 'w') as file:
			config.write(file)

	@staticmethod
	def create_if_not_exist(file_path):
		if not os.path.exists(file_path):
			config = ConfigParser()
			id = 'UCBR8-60-B28hp2BmDPdntcQ'
			config[id] = {
				'name': 'Youtube',
			}
			with open(file_path, 'w') as file:
				comments = [
					'; Example watchlist',
					'; Section name can be anything you want',
					'; Value "id" is mandatory',
					'; Values "source" and "site" are optional',
					'',
					'; Available options',
					'; source = youtube|invidious',
					'; site = <domain name>',
					'',
					'',
				]
				file.write('\n'.join(comments))
				config.write(file)
		elif os.path.isdir(file_path):
			raise IsADirectoryError("watchlist must be a file")

def unpack_entry(watchlist_item):
	channel_id = watchlist_item['id']
	source = watchlist_item['source']
	site = watchlist_item['site']
	return (channel_id, source, site)
