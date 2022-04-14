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
	@staticmethod
	def parse_watchlist(file_path):
		parser = ConfigParser()
		parser.read(file_path)
		channels = []
		for section in parser.sections():
			entry = parser[section]

			if 'id' not in entry:
				continue
			id = entry['id']

			if 'source' not in entry:
				source = 'youtube'
			else:
				source = entry['source'].lower()

			if source not in url_formats:
				print(source, 'not found in url_formats', file=stderr)
				continue

			if 'site' not in entry:
				site = url_formats[source]['default_site']
			else:
				site = entry['site']

			channel = {}
			channel['name'] = section
			channel['id'] = id
			channel['source'] = source
			channel['site'] = site
			channels.append(channel)
		return channels

	def __init__(self, file_path):
		self.channels = self.parse_watchlist(file_path)

	def __iter__(self):
		for channel in self.channels:
			yield channel

def create_if_not_exist(file_path):
	if not os.path.exists(file_path):
		config = ConfigParser()
		config['Youtube'] = {
			'id': 'UCBR8-60-B28hp2BmDPdntcQ',
			'source': 'invidious',
			'site': 'inv.riverside.rocks',
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
