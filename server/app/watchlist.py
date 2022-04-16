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
		parser = ConfigParser()
		parser.read(file_path)
		channels = []
		for section in parser.sections():
			entry = parser[section]

			if 'id' not in entry:
				self.__is_invalid = True
				continue
			id = entry['id']

			if 'source' not in entry:
				source = 'youtube'
			else:
				source = entry['source'].lower()

			if source not in url_formats:
				self.__is_invalid = True
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
		self.channels = channels

	def __iter__(self):
		for channel in self.channels:
			yield channel

	def is_invalid(self):
		return self.__is_invalid

	@staticmethod
	def create_if_not_exist(file_path):
		if not os.path.exists(file_path):
			config = ConfigParser()
			config['Youtube'] = {
				'id': 'UCBR8-60-B28hp2BmDPdntcQ',
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
