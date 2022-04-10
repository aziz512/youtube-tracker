class Watchlist:
	@staticmethod
	def parse_watchlist(file_path):
		channel_ids = []
		with open(file_path, 'r') as file:
			for line in file:
				line = line.strip()
				if len(line) == 0:
					continue
				if line[0] == '#':
					continue
				channel_ids.append(line)
		return channel_ids

	def __init__(self, file_path):
		self.channel_ids = self.parse_watchlist(file_path)

	def __iter__(self):
		for id in self.channel_ids:
			yield id
