#! ../env_correlation/bin/python
from datetime import datetime, date, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from numpy import ndarray

from correlation import Correlation


class Server(BaseHTTPRequestHandler):
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

    def table_html(self, correlation: Correlation):
        closings = correlation.data()
        matrix = correlation.matrix(closings)
        self.write('<html>')
        self.write('<head>')
        self.write('<title>Correlation AAPL - ISS</title>')
        self.write('</head>')
        self.write('<body>')
        # matrix
        self.write('<p>Correlation Matrix</p>')
        self.write('<table border="1">')
        for row in matrix:
            self.write('<tr>')
            self.write(''.join([f'<td>{column:1.3f}</td>' for column in row]))
            self.write('</tr>')
        self.write('</table>')
        # data
        self.write('<p>Data</p>')
        self.write('<table border="1">')
        self.write('<tr>')
        self.write(''.join(['<th></th>'] + [f'<th>{closing.day.isoformat()}</th>' for closing in closings]))
        self.write('</tr>')
        self.write('<tr>')
        self.write(''.join([f'<td>{correlation.symbol}</td>'] + [f'<td>{closing.stock_close:1.3f}</td>' for closing in closings]))
        self.write('</tr>')
        self.write('<tr>')
        self.write(''.join([f'<td>Distance to Wall Street</td>'] + [f'<td>{closing.wall_street_distance:1.3f}</td>' for closing in closings]))
        self.write('</tr>')
        self.write('</table>')
        self.write('</body>')
        self.write('</html>')

    def table_csv(self, correlation: Correlation):
        closings = correlation.data()
        matrix = correlation.matrix(closings)
        self.write(','.join(['dates'] + [f'{closing.day.isoformat()}' for closing in closings]))
        self.write(','.join(['quotes'] + [f'{closing.stock_close:1.3f}' for closing in closings]))
        self.write(','.join(['distances'] + [f'{closing.wall_street_distance:1.3f}' for closing in closings]))
        for index, row in enumerate(matrix):
            self.write(','.join([f'row{index + 1:02d}'] + [f'{column:1.3f}' for column in row]))

    def write(self, line: str):
        self.wfile.write(bytes(f'{line}\n', 'utf-8'))

    def do_GET(self):
        content_type = 'text/html' if self.requested_format() == self.HTML else 'text/plain'
        correlation = Correlation('AAPL', self.requested_date())
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.send_header('Content-type', content_type)
        self.end_headers()
        if self.requested_format() == self.HTML:
            self.table_html(correlation)
        else:
            self.table_csv(correlation)


if __name__ == "__main__":
    hostname = "localhost"
    server_port = 8080
    webServer = HTTPServer((hostname, server_port), Server)
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
