# File Sharing App

A simple file-sharing application written in Python. It starts a local HTTP
server so any device on the same network can **download** files from this
computer and **upload** files back to it — just by scanning a QR code.

Built with Python's standard library (`http.server`, `socketserver`, `socket`,
`webbrowser`, `tkinter`) plus [`qrcode`](https://pypi.org/project/qrcode/) and
[`Pillow`](https://pypi.org/project/Pillow/) for QR generation.

## Features

- 📥 Download files from the shared folder via the browser.
- 📤 Upload files from a phone/laptop back to this computer.
- 📱 QR code so a phone can connect without typing the address.
- 🖥️ A minimal Tkinter GUI (Start/Stop button) and a command-line mode.

## Installation

```bash
pip install -r requirements.txt
```

> On some Linux distributions Tkinter is not bundled with Python. If you get a
> `ModuleNotFoundError: No module named 'tkinter'`, install it with your system
> package manager, e.g. `sudo apt install python3-tk`.

## Usage

### GUI (easiest)

```bash
python gui.py
```

Click **Start**, then scan the QR code with a device on the same Wi-Fi network.
Click **Stop** (or close the window) to shut the server down.

### Command line

```bash
# Share the current directory on port 8000
python file_share.py

# Share a specific folder on a specific port
python file_share.py --dir ./shared --port 9000

# Don't open the QR image in a browser
python file_share.py --no-browser
```

Press `Ctrl+C` to stop the server.

## Security note

This server has **no authentication or encryption**. Anyone on the same network
can browse, download, and upload files in the shared folder. Only run it on a
**trusted local network**, and stop it when you are done. You may also need to
allow the port through your firewall for other devices to connect.
