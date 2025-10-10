from pathlib import Path


def SongList(user_input: str):
    directory = Path(user_input)
    for file in directory.iterdir():
        if file.suffix.lower() == ".txt":
            with file.open(encoding="utf-8") as f:
                songs = [line.strip() for line in f if line.strip()]
                urls = GetURLS(songs)
            return urls
    return []


def GetURLS(songlist):
    urls = [f"ytsearch1:{song}" for song in songlist]
    return urls
