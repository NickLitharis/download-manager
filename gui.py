from tkinter import Frame, Tk, Entry, Button, Label, StringVar, filedialog, ttk
from pathlib import Path
import os
from typing import Optional

from controller import download_files
from tkinter import messagebox

# UI constants to keep things modular and easy to tweak
WINDOW_GEOMETRY = '560x360'
PANEL_BG = '#f8fafc'
FORMATS = ["mp3", "m4a", "mp4"]


def choose_destination(root: Tk, title: str = "Choose destination") -> Optional[str]:
    """Open a folder picker and return the chosen path or None if cancelled."""
    dest = filedialog.askdirectory(title=title)
    return dest or None


def run_ui():
    root = Tk()
    root.geometry(WINDOW_GEOMETRY)
    root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())
    # root.iconbitmap(r"Icon\\wave.ico")
    root.resizable(0, 0)
    root.title("Download Manager")

    # Ensure the app fully terminates when the window is closed
    def on_close():
        try:
            root.quit()
        finally:
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    options = FORMATS  # file supported formats

    # Layout: top navigation + content area (stacked frames)
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)

    nav = Frame(root)
    nav.grid(row=0, column=0, sticky="ew")
    # Make three equal-width columns
    for i in range(3):
        nav.grid_columnconfigure(i, weight=1, uniform="nav")

    content = Frame(root)
    content.grid(row=1, column=0, sticky="nsew")
    content.grid_columnconfigure(0, weight=1)
    content.grid_rowconfigure(0, weight=1)

    # Panels with readable light background
    search_frame = Frame(content, bg=PANEL_BG)
    link_frame = Frame(content, bg=PANEL_BG)
    playlist_frame = Frame(content, bg=PANEL_BG)
    for f in (search_frame, link_frame, playlist_frame):
        f.grid(row=0, column=0, sticky="nsew")
        # make room to center content vertically and horizontally
        f.grid_columnconfigure(0, weight=1)
        f.grid_rowconfigure(0, weight=1)
        f.grid_rowconfigure(2, weight=1)

    def show_panel(name: str):
        btn_map = {
            'search': btn_search,
            'link': btn_link,
            'playlist': btn_playlist,
        }
        frame_map = {
            'search': search_frame,
            'link': link_frame,
            'playlist': playlist_frame,
        }
        for b in btn_map.values():
            b.config(state='normal')
        btn_map[name].config(state='disabled')
        frame_map[name].tkraise()

    # Search panel (centered inner container)
    search_inner = Frame(search_frame, bg=PANEL_BG)
    search_inner.grid(row=1, column=0)

    Label(search_inner, text="Song name:", bg=PANEL_BG).grid(row=0, column=0, padx=16, pady=(8, 4))
    search_entry = Entry(search_inner, width=32)
    search_entry.grid(row=1, column=0, padx=16)

    Label(search_inner, text="Format:", bg=PANEL_BG).grid(row=2, column=0, padx=16, pady=(12, 4))
    search_format = ttk.Combobox(search_inner, width=10, values=options, state="readonly")
    search_format.current(0)
    search_format.grid(row=3, column=0, padx=16)

    def search_download():
        query = search_entry.get().strip()
        if not query:
            messagebox.showinfo('Friendly Remainder', "Please enter a title", parent=root)
            return
        dest = choose_destination(root)
        if not dest:
            return
        download_files('1', search_format.get(), query, dest, root)

    search_button = Button(search_inner, width=20, text="Download", command=search_download,
                           border=0, bg='#ffffff', fg='#000000')
    search_button.grid(row=4, column=0, padx=16, pady=16)

    def _search_validate(*_):
        search_button.config(state='normal' if search_entry.get().strip() else 'disabled')

    search_var = StringVar()
    search_var.trace_add('write', _search_validate)
    search_entry.config(textvariable=search_var)
    _search_validate()
    search_entry.bind('<Return>', lambda e: search_download())

    # Link panel (centered inner container)
    link_inner = Frame(link_frame, bg=PANEL_BG)
    link_inner.grid(row=1, column=0)

    Label(link_inner, text="YouTube link:", bg=PANEL_BG).grid(row=0, column=0, padx=16, pady=(8, 4))
    link_entry = Entry(link_inner, width=32)
    link_entry.grid(row=1, column=0, padx=16)

    Label(link_inner, text="Format:", bg=PANEL_BG).grid(row=2, column=0, padx=16, pady=(12, 4))
    link_format = ttk.Combobox(link_inner, width=10, values=options, state="readonly")
    link_format.current(0)
    link_format.grid(row=3, column=0, padx=16)

    def link_download():
        link = link_entry.get().strip()
        if not link:
            messagebox.showinfo('Friendly Remainder', "Please enter a link", parent=root)
            return
        dest = choose_destination(root)
        if not dest:
            return
        download_files('2', link_format.get(), link, dest, root)

    link_button = Button(link_inner, width=20, text="Download", command=link_download,
                         border=0, bg='#ffffff', fg='#000000')
    link_button.grid(row=4, column=0, padx=16, pady=16)

    def _link_validate(*_):
        link_button.config(state='normal' if link_entry.get().strip() else 'disabled')

    link_var = StringVar()
    link_var.trace_add('write', _link_validate)
    link_entry.config(textvariable=link_var)
    _link_validate()
    link_entry.bind('<Return>', lambda e: link_download())

    # Playlist panel (centered inner container)
    playlist_frame.directory = None
    playlist_selected = StringVar(value="No file selected")

    playlist_inner = Frame(playlist_frame, bg=PANEL_BG)
    playlist_inner.grid(row=1, column=0)

    Label(playlist_inner, text="Custom playlist (.txt):", bg=PANEL_BG).grid(row=0, column=0, padx=16, pady=(8, 4))
    selected_label = Label(playlist_inner, textvariable=playlist_selected, bg=PANEL_BG)
    selected_label.grid(row=1, column=0, padx=16)

    Label(playlist_inner, text="Format:", bg=PANEL_BG).grid(row=2, column=0, padx=16, pady=(12, 4))
    playlist_format = ttk.Combobox(playlist_inner, width=10, values=options, state="readonly")
    playlist_format.current(0)
    playlist_format.grid(row=3, column=0, padx=16)

    def pick_playlist_file():
        path = filedialog.askopenfilename()
        if not path:
            return
        if path.endswith('.txt'):
            if os.path.getsize(path) == 0:
                messagebox.showinfo('Friendly Remainder', "This file is empty", parent=root)
                return
            p = Path(path)
            playlist_frame.directory = p.parent
            playlist_selected.set(str(p.name))
            _playlist_validate()
        else:
            messagebox.showinfo('Friendly Remainder', "Please use a .txt file", parent=root)

    def playlist_download():
        if playlist_frame.directory is None:
            messagebox.showinfo('Friendly Remainder', "Please use a .txt file", parent=root)
            return
        dest = choose_destination(root)
        if not dest:
            return
        download_files('3', playlist_format.get(), str(playlist_frame.directory), dest, root)

    Button(playlist_inner, width=20, text="Select File", command=pick_playlist_file,
        border=0, bg='#ffffff', fg='#000000').grid(row=4, column=0, padx=16, pady=(8, 8))

    playlist_button = Button(playlist_inner, width=20, text="Download", command=playlist_download,
                 border=0, bg='#ffffff', fg='#000000')
    playlist_button.grid(row=5, column=0, padx=16, pady=(0, 16))

    def _playlist_validate():
        playlist_button.config(state='normal' if playlist_frame.directory is not None else 'disabled')

    _playlist_validate()

    # Top navigation
    # High-contrast, readable nav buttons
    btn_search = Button(nav, width=19, height=0, text="Search", command=lambda: show_panel('search'),
                        border=0, bg='#2563eb', pady=4, fg='#ffffff', activebackground='#1e40af', activeforeground='#ffffff')
    btn_link = Button(nav, width=19, height=0, text="Link", command=lambda: show_panel('link'),
                      border=0, bg='#16a34a', pady=4, fg='#ffffff', activebackground='#166534', activeforeground='#ffffff')
    btn_playlist = Button(nav, width=19, height=0, text="Playlist", command=lambda: show_panel('playlist'),
                          border=0, bg='#f59e0b', pady=4, fg='#111111', activebackground='#b45309', activeforeground='#111111')

    btn_search.grid(row=0, column=0, sticky="ew")
    btn_link.grid(row=0, column=1, sticky="ew")
    btn_playlist.grid(row=0, column=2, sticky="ew")

    # Keyboard shortcut to close
    root.bind('<Escape>', lambda e: on_close())

    # Start with Search panel active
    show_panel('search')

    root.mainloop()
