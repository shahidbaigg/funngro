from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import sys

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Route clean URLs to HTML files
        if self.path == '/company':
            self.path = '/company.html'
        elif self.path == '/teen':
            self.path = '/index.html'
        return super().do_GET()

def app(environ, start_response):
    """WSGI entrypoint for Vercel Python runtime fallback"""
    status = '200 OK'
    path = environ.get('PATH_INFO', '/')
    
    if path == '/company' or path == '/company.html':
        file_path = os.path.join(os.path.dirname(__file__), 'company.html')
    else:
        file_path = os.path.join(os.path.dirname(__file__), 'index.html')
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            content = f.read()
        headers = [('Content-Type', 'text/html; charset=utf-8'), ('Content-Length', str(len(content)))]
        start_response(status, headers)
        return [content]
    
    status = '404 Not Found'
    start_response(status, [('Content-Type', 'text/plain')])
    return [b'Not Found']

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f"Serving at http://localhost:{port}")
    server.serve_forever()
