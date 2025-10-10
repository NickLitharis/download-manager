import os
from typing import Iterable
from yt_dlp import YoutubeDL


def VideoDownloader(urls: Iterable[str], destination: str) -> None:
    os.makedirs(destination, exist_ok=True)

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(destination, '%(title)s.%(ext)s'),
        'concurrent_fragment_downloads': 4,
        'retries': 3,
        'quiet': False,
        'noprogress': False,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(list(urls))
