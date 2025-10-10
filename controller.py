from __future__ import unicode_literals
from typing import List
from audio_downloader import AudioDownloader
from video_downloader import VideoDownloader
from playlist_parser import SongList
from tkinter import messagebox


# Main program function
def download_files(download_method: str, video_type: str, user_input: str, destinationPath: str, parent=None) -> None:
    """High-level download dispatcher using existing modules only.

    Args:
        download_method: '1' search, '2' direct url, '3' playlist dir
        video_type: 'mp3' | 'm4a' | 'mp4'
        user_input: query, url, or directory path (for playlist)
        destinationPath: folder to save downloads
        parent: optional Tk parent for dialogs
    """
    # Build URL list depending on method
    if download_method == '1':
        urls: List[str] = [f"ytsearch1:{user_input}"]
    elif download_method == '2':
        urls = [user_input]
    else:
        urls = SongList(user_input)

    if video_type in ("mp3", "m4a"):
        AudioDownloader(urls, destinationPath, video_type)
    else:
        VideoDownloader(urls, destinationPath)

    # Display "save" directory
    messagebox.showinfo('Friendly Remainder', "Your file is at: " + destinationPath, parent=parent)
