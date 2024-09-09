from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Route handling for GET requests
        if self.path == "/":
            self.handle_root()
        elif self.path == "/tasks":
            self.get_tasks()
        else:
            self.handle_404()

    def do_POST(self):
        # Route handling for POST requests
        if self.path == "/notify":
            self.handle_data_post()
        else:
            self.handle_404()

    def handle_root(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            'message': 'Welcome to the root endpoint!'
        }
        self.wfile.write(json.dumps(response).encode())

    def get_tasks(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = [
            {
                "cameraIp": "1.1.1.1",
                "cameraName": "camera1",
                "stream_url": "movie.avi",
                "taskId": "id001",
                "model": "yolov8n.pt",
                "algorithm": "on_duty"
            },
            {
                "cameraIp": "1.1.1.1",
                "cameraName": "camera1",
                "stream_url": "rtsp://camera1/stream",
                "taskId": "id002",
                "model": "yolov8n.pt",
                "algorithm": "yolo"
            }
        ]

        self.wfile.write(json.dumps(response).encode())

    def handle_data_post(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Assuming the incoming data is JSON
        try:
            data = json.loads(post_data)
            print(data)
            response = {
                "code": 0,
                'message': '',
                'received_data': data
            }
            self.send_response(200)
        except json.JSONDecodeError:
            response = {
                'error': 'Invalid JSON'
            }
            self.send_response(400)

        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def handle_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            'error': 'Not Found',
            'path': self.path
        }
        self.wfile.write(json.dumps(response).encode())

# Define server address and port
server_address = ('', 50080)  # Serve on all addresses, port 8000

# Create and start the server
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
print('Starting server on port 50080...')
httpd.serve_forever()

