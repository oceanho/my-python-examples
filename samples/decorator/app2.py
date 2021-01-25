from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

from urllib import parse

from functools import wraps

class Counter:
    def __init__(self, f):
        self.f = f
        self.num_calls = 0
        print(f)
    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print('num of calls is: {}, {}'.format(self.num_calls, id(self)))
        return self.f(*args, **kwargs)

@Counter
def example(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapper

class Handler(BaseHTTPRequestHandler):
    @example
    def do_GET(self):
        parsed_path = parse.urlparse(self.path)
        message_parts = [
            'CLIENT VALUES:',
            'client_address={} ({})'.format(
                self.client_address,
                self.address_string()),
            'command={}'.format(self.command),
            'path={}'.format(self.path),
            'real path={}'.format(parsed_path.path),
            'query={}'.format(parsed_path.query),
            'request_version={}'.format(self.request_version),
            '',
            'SERVER VALUES:',
            'server_version={}'.format(self.server_version),
            'sys_version={}'.format(self.sys_version),
            'protocol_version={}'.format(self.protocol_version),
            '',
            'HEADERS RECEIVED:',
        ]
        for name, value in sorted(self.headers.items()):
            message_parts.append(
                '{}={}'.format(name, value.rstrip())
            )
        message_parts.append('')
        message = '\r\n'.join(message_parts)
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))

server = HTTPServer(('0.0.0.0',8000), Handler)
print('Starting server, use <Ctrl-C> to stop')
server.serve_forever()
#http.run

