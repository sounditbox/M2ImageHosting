import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from uuid import uuid4

SERVER_ADDRESS = ('0.0.0.0', 8000)
STATIC_PATH = 'static/'
IMAGES_PATH = 'images/'
ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']
MAX_FILE_SIZE = 5 * 1024 * 1024


class ImageHostingHttpRequestHandler(BaseHTTPRequestHandler):
    server_version = 'Image Hosting Server v0.1'

    # ВСЕ get-запросы обрабатываются здесь
    def do_GET(self):
        if self.path == '/':
            self.send_html('index.html')
        if self.path.startswith('/images/') and any(self.path.endswith(ext) for ext in ALLOWED_EXTENSIONS):
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            filename = self.path.split('/')[-1]
            with open(IMAGES_PATH + filename, 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/api/images':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'images': next(os.walk(IMAGES_PATH))[2]
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))

        elif self.path == '/images':
            self.send_html('images.html')
        elif self.path == '/upload':
            self.send_html('upload.html')
        else:
            self.send_html('404.html', 404)

    def do_POST(self):
        if self.path == '/upload':
            length = int(self.headers.get('Content-Length'))
            if length > MAX_FILE_SIZE:
                self.send_html('upload_failed.html', 413)
                return

            data = self.rfile.read(length)
            _, ext = os.path.splitext(self.headers.get('Filename'))
            image_id = uuid4()
            if ext not in ALLOWED_EXTENSIONS:
                self.send_html('upload_failed.html', 400)
                return

            with open(IMAGES_PATH + f'{image_id}{ext}', 'wb') as file:
                file.write(data)
            self.send_html('upload_success.html')
        else:
            self.send_html('404.html', 404)

    def send_html(self, file_path, code=200):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(STATIC_PATH + file_path, 'rb') as file:
            self.wfile.write(file.read())


def run(server_class=HTTPServer, handler_class=ImageHostingHttpRequestHandler):
    httpd = server_class(SERVER_ADDRESS, handler_class)
    print(f'Serving on http://{SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Keyboard interrupt received, exiting.')
        httpd.server_close()
    finally:
        print('Server stopped.')


if __name__ == '__main__':
    run()
