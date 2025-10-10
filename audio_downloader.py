import os
from typing import Iterable
from yt_dlp import YoutubeDL


def AudioDownloader(urls: Iterable[str], destination: str, audio_format: str) -> None:
    if audio_format not in ("mp3", "m4a"):
        raise ValueError("audio_format must be 'mp3' or 'm4a'")

    os.makedirs(destination, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(destination, '%(title)s.%(ext)s'),
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': '0'
            }
        ],
        'concurrent_fragment_downloads': 4,
        'retries': 3,
        'quiet': False,
        'noprogress': False,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(list(urls))
