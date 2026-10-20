from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/company':
            self.path = '/company.html'
        elif self.path == '/teen':
            self.path = '/index.html'
        return super().do_GET()

def app(environ, start_response):
    """WSGI entrypoint for Vercel Python runtime fallback"""
    path = environ.get('PATH_INFO', '/')
    base_dir = os.path.dirname(__file__)

    if path == '/styles.css':
        file_path = os.path.join(base_dir, 'styles.css')
        content_type = 'text/css; charset=utf-8'
    elif path in ('/company', '/company.html'):
        file_path = os.path.join(base_dir, 'company.html')
        content_type = 'text/html; charset=utf-8'
    else:
        file_path = os.path.join(base_dir, 'index.html')
        content_type = 'text/html; charset=utf-8'

    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            content = f.read()
        headers = [
            ('Content-Type', content_type),
            ('Content-Length', str(len(content))),
            ('Cache-Control', 'public, max-age=3600')
        ]
        start_response('200 OK', headers)
        return [content]

    start_response('404 Not Found', [('Content-Type', 'text/plain')])
    return [b'Not Found']

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f"Serving at http://localhost:{port}")
    server.serve_forever()
