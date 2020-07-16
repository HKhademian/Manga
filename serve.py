import http.server
import socketserver
import os

PORT = 8000

serve_dir = os.path.join(os.path.dirname(__file__), 'output')
os.chdir(serve_dir)

handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), handler) as httpd:
	print(f"Server started at (http://localhost:{PORT})")
	httpd.serve_forever()
