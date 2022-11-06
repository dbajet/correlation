#! ../env_correlation/bin/python
from datetime import datetime, date, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from numpy import ndarray

from correlation import Correlation


class MyServer(BaseHTTPRequestHandler):
    HTML = 'html'

    def requested_date(self) -> date:
        query = urlparse(self.path).query
        # sanitization through parsing
        result = datetime.now().date()
        try:
            parameter = parse_qs(query).get('date', [])
            if parameter:
                result = date.fromisoformat(parameter[0])
        except ValueError:
            result = datetime.now().date()
        return result

    def requested_format(self) -> str:
        query = urlparse(self.path).query
        # sanitization by forcing one value or the other
        result = parse_qs(query).get('format', [])
        if result and result[0] == 'html':
            return 'html'
        return 'csv'

    def table_html(self, closings: ndarray):
        self.write('<html>')
        self.write('<head>')
        self.write('<title>Correlation AAPL - ISS</title>')
        self.write('</head>')
        self.write('<body>')
        self.write('<table border="1">')
        for row in closings:
            self.write('<tr>')
            self.write(''.join([f'<td>{column:1.3f}</td>' for column in row]))
            self.write('</tr>')
        self.write('</table>')
        self.write('</body>')
        self.write('</html>')

    def table_csv(self, closings: ndarray):
        for row in closings:
            self.write(','.join([f'{column:1.3f}' for column in row]))
            self.write('\n')

    def write(self, line: str):
        self.wfile.write(bytes(line, 'utf-8'))

    def do_GET(self):
        content_type = 'text/html' if self.requested_format() == self.HTML else 'text/plain'
        closings = Correlation('AAPL', self.requested_date()).matrix()

        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.send_header('Content-type', content_type)
        self.end_headers()
        if self.requested_format() == self.HTML:
            self.table_html(closings)
        else:
            self.table_csv(closings)


if __name__ == "__main__":
    hostname = "localhost"
    server_port = 8080
    webServer = HTTPServer((hostname, server_port), MyServer)
    print(f'Server started...')
    yesterday = (datetime.now() + timedelta(days=-1))
    print(f'usage: http://{hostname}:{server_port}?date={yesterday.date().isoformat()}')
    print(f'usage: http://{hostname}:{server_port}?date={yesterday.date().isoformat()}&format=html')
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print('Server stopped.')
