import asyncio
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
