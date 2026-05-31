"""Simple Tkinter GUI for the LAN file-sharing server.

Provides a single Start/Stop button and shows the server URL plus a QR code so
non-technical users can share files without touching the command line.

The actual server logic lives in ``file_share.py``; this file only drives it.
"""

from __future__ import annotations

import os
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

from file_share import DEFAULT_PORT, FileShareServer, make_qr

# Fixed defaults for the "simple" mode. Adjust here if needed.
SHARE_DIRECTORY = os.getcwd()
SHARE_PORT = DEFAULT_PORT


class FileShareApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.server: FileShareServer | None = None
        self._qr_image: ImageTk.PhotoImage | None = None

        root.title("File Sharing")
        root.resizable(False, False)

        frame = ttk.Frame(root, padding=20)
        frame.grid(sticky="nsew")

        self.status_label = ttk.Label(frame, text="Stopped", font=("", 11, "bold"))
        self.status_label.grid(row=0, column=0, pady=(0, 8))

        self.url_label = ttk.Label(frame, text="", foreground="#0a58ca")
        self.url_label.grid(row=1, column=0, pady=(0, 8))

        self.qr_label = ttk.Label(frame)
        self.qr_label.grid(row=2, column=0, pady=(0, 12))

        self.toggle_button = ttk.Button(frame, text="Start", command=self.toggle)
        self.toggle_button.grid(row=3, column=0)

        root.protocol("WM_DELETE_WINDOW", self.on_close)

    def toggle(self) -> None:
        if self.server and self.server.is_running:
            self.stop()
        else:
            self.start()

    def start(self) -> None:
        self.server = FileShareServer(directory=SHARE_DIRECTORY, port=SHARE_PORT)
        url = self.server.start()

        qr_path = make_qr(url, print_ascii=False)
        image = Image.open(qr_path)
        image = image.resize((220, 220))
        self._qr_image = ImageTk.PhotoImage(image)

        self.qr_label.configure(image=self._qr_image)
        self.url_label.configure(text=url)
        self.status_label.configure(text=f"Running — sharing {SHARE_DIRECTORY}")
        self.toggle_button.configure(text="Stop")

    def stop(self) -> None:
        if self.server:
            self.server.stop()
            self.server = None
        self._qr_image = None
        self.qr_label.configure(image="")
        self.url_label.configure(text="")
        self.status_label.configure(text="Stopped")
        self.toggle_button.configure(text="Start")

    def on_close(self) -> None:
        if self.server and self.server.is_running:
            self.server.stop()
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    FileShareApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
