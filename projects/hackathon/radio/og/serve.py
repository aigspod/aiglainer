import http.server, os, sys
OUT = sys.argv[1]
class H(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers['Content-Length']); open(OUT, 'wb').write(self.rfile.read(n))
        self.send_response(200); self.end_headers(); self.wfile.write(b'ok')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
http.server.ThreadingHTTPServer(('127.0.0.1', 8778), H).serve_forever()
