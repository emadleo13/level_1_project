"""Simple LAN file-sharing server.

Hosts a directory over HTTP so other devices on the same local network can
browse and download files, and upload files back to this computer. A QR code
pointing at the server URL is generated so a phone can connect by just scanning
it.

This module exposes reusable building blocks (``get_local_ip``, ``make_qr``,
``FileShareServer``) that are used by both the command line entry point in this
file and the Tkinter GUI in ``gui.py``.
"""

from __future__ import annotations

import argparse
import html
import os
import socket
import threading
import webbrowser
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import quote

import qrcode

DEFAULT_PORT = 8000
QR_FILENAME = "share_qr.png"


def get_local_ip() -> str:
    """Return the LAN IP address of this machine.

    Opens a UDP socket toward a public address (no data is actually sent) and
    reads back the local endpoint the OS picked. This is more reliable than
    ``socket.gethostbyname(socket.gethostname())``, which often returns
    ``127.0.0.1``.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        sock.close()


def make_qr(url: str, filename: str = QR_FILENAME, print_ascii: bool = True) -> str:
    """Generate a QR code image for ``url`` and save it as a PNG.

    Optionally also prints a scannable ASCII version to the terminal. Returns
    the path of the saved PNG file.
    """
    qr = qrcode.QRCode(border=2)
    qr.add_data(url)
    qr.make(fit=True)

    if print_ascii:
        qr.print_ascii(invert=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    return filename


class FileShareHandler(SimpleHTTPRequestHandler):
    """Request handler that serves a directory and accepts file uploads.

    Download and directory listing come for free from
    ``SimpleHTTPRequestHandler``. We override ``list_directory`` to inject an
    upload form and add ``do_POST`` to receive uploaded files.
    """

    def do_GET(self):  # noqa: N802 (http.server naming convention)
        if self.path.rstrip("/") == "" or self.path.endswith("/"):
            self._send_listing()
        else:
            super().do_GET()

    def _send_listing(self) -> None:
        """Send a directory listing page that includes an upload form."""
        local_path = self.translate_path(self.path)
        if not os.path.isdir(local_path):
            super().do_GET()
            return

        try:
            entries = sorted(os.listdir(local_path))
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND, "No permission to list directory")
            return

        display_path = html.escape(self.path)
        rows = []
        for name in entries:
            full = os.path.join(local_path, name)
            display_name = name + ("/" if os.path.isdir(full) else "")
            link = quote(name) + ("/" if os.path.isdir(full) else "")
            rows.append(
                f'<li><a href="{link}">{html.escape(display_name)}</a></li>'
            )

        body = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>File Sharing &mdash; {display_path}</title>
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 640px; margin: 2rem auto; padding: 0 1rem; }}
  h1 {{ font-size: 1.2rem; }}
  ul {{ line-height: 1.8; }}
  .upload {{ border: 1px solid #ccc; border-radius: 8px; padding: 1rem; margin-bottom: 1.5rem; }}
  button {{ padding: 0.4rem 1rem; }}
</style>
</head>
<body>
<h1>Index of {display_path}</h1>
<div class="upload">
  <form enctype="multipart/form-data" method="post">
    <p>Upload file(s) to this folder:</p>
    <input name="file" type="file" multiple>
    <button type="submit">Upload</button>
  </form>
</div>
<ul>
{os.linesep.join(rows)}
</ul>
</body>
</html>
"""
        encoded = body.encode("utf-8", "surrogateescape")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_POST(self):  # noqa: N802 (http.server naming convention)
        """Receive uploaded files from a multipart/form-data request."""
        content_type = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in content_type:
            self.send_error(HTTPStatus.BAD_REQUEST, "Expected multipart/form-data")
            return

        boundary = self._parse_boundary(content_type)
        if boundary is None:
            self.send_error(HTTPStatus.BAD_REQUEST, "Missing multipart boundary")
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        saved = self._save_uploaded_files(body, boundary)

        # Redirect back to the directory the upload was posted to.
        self.send_response(HTTPStatus.SEE_OTHER)
        self.send_header("Location", self.path)
        self.end_headers()
        self.wfile.write(f"Uploaded {saved} file(s).".encode("utf-8"))

    @staticmethod
    def _parse_boundary(content_type: str) -> bytes | None:
        for part in content_type.split(";"):
            part = part.strip()
            if part.startswith("boundary="):
                return part[len("boundary="):].strip('"').encode("utf-8")
        return None

    def _save_uploaded_files(self, body: bytes, boundary: bytes) -> int:
        """Parse a multipart body and write each uploaded file to disk.

        A small hand-rolled parser is used so we don't depend on the ``cgi``
        module, which was removed in Python 3.13.
        """
        target_dir = self.translate_path(self.path)
        if not os.path.isdir(target_dir):
            target_dir = os.path.dirname(target_dir)

        delimiter = b"--" + boundary
        saved = 0
        for part in body.split(delimiter):
            if not part or part in (b"--\r\n", b"--", b"\r\n"):
                continue
            # Separate part headers from part content.
            header_blob, _, content = part.partition(b"\r\n\r\n")
            if not content:
                continue
            filename = self._extract_filename(header_blob)
            if not filename:
                continue
            # Strip the trailing CRLF that precedes the next boundary.
            content = content[:-2] if content.endswith(b"\r\n") else content
            dest = os.path.join(target_dir, os.path.basename(filename))
            with open(dest, "wb") as fh:
                fh.write(content)
            saved += 1
        return saved

    @staticmethod
    def _extract_filename(header_blob: bytes) -> str | None:
        headers = header_blob.decode("utf-8", "replace")
        for line in headers.split("\r\n"):
            if line.lower().startswith("content-disposition"):
                for token in line.split(";"):
                    token = token.strip()
                    if token.startswith("filename="):
                        return token[len("filename="):].strip('"') or None
        return None


class FileShareServer:
    """Reusable wrapper around the HTTP server.

    Runs the server in a background thread so callers (notably the GUI) are not
    blocked. Used by both the CLI entry point and the Tkinter GUI.
    """

    def __init__(self, directory: str | None = None, port: int = DEFAULT_PORT):
        self.directory = os.path.abspath(directory or os.getcwd())
        self.port = port
        self._httpd: ThreadingHTTPServer | None = None
        self._thread: threading.Thread | None = None

    @property
    def url(self) -> str:
        return f"http://{get_local_ip()}:{self.port}"

    @property
    def is_running(self) -> bool:
        return self._httpd is not None

    def start(self) -> str:
        """Start serving in a background thread and return the server URL."""
        if self._httpd is not None:
            return self.url

        directory = self.directory

        def handler_factory(*args, **kwargs):
            return FileShareHandler(*args, directory=directory, **kwargs)

        self._httpd = ThreadingHTTPServer(("0.0.0.0", self.port), handler_factory)
        self._thread = threading.Thread(
            target=self._httpd.serve_forever, daemon=True
        )
        self._thread.start()
        return self.url

    def stop(self) -> None:
        """Shut the server down cleanly."""
        if self._httpd is None:
            return
        self._httpd.shutdown()
        self._httpd.server_close()
        if self._thread is not None:
            self._thread.join(timeout=5)
        self._httpd = None
        self._thread = None


def main() -> None:
    parser = argparse.ArgumentParser(description="Share files over your local network.")
    parser.add_argument(
        "--port", type=int, default=DEFAULT_PORT, help="Port to listen on (default: 8000)."
    )
    parser.add_argument(
        "--dir", default=os.getcwd(), help="Directory to share (default: current directory)."
    )
    parser.add_argument(
        "--no-browser", action="store_true", help="Do not open the QR image in a browser."
    )
    args = parser.parse_args()

    server = FileShareServer(directory=args.dir, port=args.port)
    url = server.start()

    print(f"Serving '{server.directory}' at {url}")
    print("Scan this QR code with a device on the same network:\n")
    qr_path = make_qr(url)
    print(f"\nQR code saved to {os.path.abspath(qr_path)}")
    print("Press Ctrl+C to stop.")

    if not args.no_browser:
        webbrowser.open(f"file://{os.path.abspath(qr_path)}")

    try:
        # Keep the main thread alive while the daemon server thread runs.
        threading.Event().wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.stop()


if __name__ == "__main__":
    main()
