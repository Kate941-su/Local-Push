#!/usr/bin/env python3
# @author Cursor
import json
import socket
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


HOST = "0.0.0.0"
PORT = 8888


def get_local_ip() -> str:
    # Determine the primary local network IP without sending traffic.
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            return str(sock.getsockname()[0])
    except OSError:
        return "127.0.0.1"


class AppHandler(SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path in ("/server-info", "/server-info/"):
            payload = {
                "local_ip": get_local_ip(),
                "port": PORT,
            }
            body = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        super().do_GET()


def run() -> None:
    server_address = (HOST, PORT)
    with ThreadingHTTPServer(server_address, AppHandler) as httpd:
        local_ip = get_local_ip()
        print(f"Serving index.html at http://localhost:{PORT}")
        print(f"Local network address: http://{local_ip}:{PORT}")
        httpd.serve_forever()


if __name__ == "__main__":
    run()
