#! ../env_correlation/bin/python

from datetime import datetime, timedelta
from http.server import HTTPServer

from libs.server import Server

hostname = "0.0.0.0"
server_port = 8080
web_server = HTTPServer((hostname, server_port), Server)
print(f'Server started...')
yesterday = (datetime.now() + timedelta(days=-1))
print(f'usage: http://{hostname}:{server_port}?date={yesterday.date().isoformat()}')
print(f'usage: http://{hostname}:{server_port}?date={yesterday.date().isoformat()}&format=html')
try:
    web_server.serve_forever()
except KeyboardInterrupt:
    pass
web_server.server_close()
print('Server stopped.')
