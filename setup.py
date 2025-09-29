import screen_brightness_control as sbc
import http.server
import socketserver
import json
import webbrowser
import os
from threading import Timer

PORT = 9096

class BrightnessHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(current_dir)
        super().__init__(*args, **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-type', 'application/json')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        brightness = data.get('brightness', 50)

        try:
            sbc.set_brightness(brightness+20)
            self.send_response(200)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode('utf-8'))

def open_browser():
    webbrowser.open(f'http://localhost:{PORT}/index.html')

with socketserver.TCPServer(("", PORT), BrightnessHandler) as httpd:
    print(f"Server has started at port: {PORT}")
    Timer(1.5, open_browser).start()
    httpd.serve_forever()