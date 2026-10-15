# Desktop Download Manager — YouTube media downloader

Welcome — this is a compact Tkinter desktop app used in the university course "Python Programming" for learning practical Python, GUI programming, and working with third‑party tools.

The app lets you download audio and video from YouTube using yt-dlp and ffmpeg. It focuses on clarity and a small codebase so students can study the whole project.

Quick start

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Install system ffmpeg (required for audio conversion):

```bash
sudo apt install ffmpeg    # Debian/Ubuntu
```

4. Run the app:

```bash
python main.py
```

Project layout (canonical files)

- `main.py` — program entrypoint (calls `gui.run_ui()`).
- `gui.py` — Tkinter graphical interface, dialogs and the `run_ui()` entrypoint.
- `controller.py` — orchestrates user requests and routes work to downloaders.
- `audio_downloader.py` — audio download/FFmpeg conversion logic (yt-dlp wrapper).
- `video_downloader.py` — video download logic (yt-dlp wrapper).
- `playlist_parser.py` — parses a `.txt` playlist into search queries for batch downloads.


Notes for students

- This project demonstrates using `yt-dlp` programmatically and integrating `ffmpeg` for audio extraction.
- The UI is intentionally small so you can trace the flow from `gui.py` -> `controller.py` -> `*_downloader.py`.


Contributing
- Feel free to open issues or submit PRs. If you want to reintroduce transliteration of input strings, add a small helper in `gui.py` or a new module and import it where needed.


## Development Team

- [@olumpiaalexopoulou](https://github.com/olumpiaalexopoulou)
- [@NickLitharis](https://github.com/NickLitharis)
- [@NaskosAthanasios](https://github.com/NaskosAthanasios)
- [@tilav](https://github.com/tilav)
