"""Staticky server pre mockup-v2 s vypnutou cache (aby sa vzdy zobrazila aktualna verzia)."""
import functools
import http.server
import os

ROOT = os.path.dirname(os.path.abspath(__file__))  # cely projekt: /mockup-v5-smaragd/, /mockup-v4-hravy/ ...


class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, max-age=0')
        super().end_headers()


handler = functools.partial(NoCache, directory=ROOT)
http.server.ThreadingHTTPServer(('127.0.0.1', 8765), handler).serve_forever()
