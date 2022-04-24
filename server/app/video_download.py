import threading
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

def download_video(id):
  URL = f'https://www.youtube.com/watch?v={id}'
  ydl_opts = {
    'format': 'mp4/bestaudio/best',
    'outtmpl': './downloadedvideos/%(title)s.%(ext)s',
  }
  with YoutubeDL(ydl_opts) as ydl:
      try:
        threading.Thread(target=ydl.download([URL]))
      except DownloadError:
        return "DownloadError"
