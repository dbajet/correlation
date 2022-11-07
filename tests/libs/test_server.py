from datetime import date, datetime
from unittest import mock
from unittest.mock import patch, MagicMock, call

from immutables.closing_location import ClosingLocation
from libs.server import Server


@mock.patch('libs.server.datetime', wraps=datetime)
@patch.object(Server, '__init__', (lambda a, b, c, d: None))
def test_requested_date(mock_datetime):
    mock_datetime.now.return_value = datetime(2022, 11, 6, 15, 37, 21, 123456, tzinfo=None)  # now is offset-naive
    mock_server = MagicMock()
    tested = Server(b'', ('', 200), mock_server)
    tests = [
        ('/?date=2022-11-01&format=html', date(2022, 11, 1)),
        ('/?date=2022-11-01', date(2022, 11, 1)),
        ('/?date=2022-11-37', date(2022, 11, 6)),
        ('/?format=html', date(2022, 11, 6)),
    ]
    for path, expected in tests:
        tested.path = path
        result = tested.requested_date()
        assert result == expected
        assert [] == mock_server.mock_calls
        mock_server.reset_mock()


@mock.patch('libs.server.datetime', wraps=datetime)
@patch.object(Server, '__init__', (lambda a, b, c, d: None))
def test_requested_format(mock_datetime):
    mock_datetime.now.return_value = datetime(2022, 11, 6, 15, 37, 21, 123456, tzinfo=None)  # now is offset-naive
    mock_server = MagicMock()
    tested = Server(b'', ('', 200), mock_server)
    tests = [
        ('/?date=2022-11-01&format=html', 'html'),
        ('/?date=2022-11-01&format=other', 'csv'),
        ('/?date=2022-11-01', 'csv'),
        ('/', 'csv'),
    ]
    for path, expected in tests:
        tested.path = path
        result = tested.requested_format()
        assert result == expected
        assert [] == mock_server.mock_calls
        mock_server.reset_mock()


@patch.object(Server, '__init__', (lambda a, b, c, d: None))
@patch('libs.server.Server.write')
def test_table_html(write):
    mock_server = MagicMock()
    mock_correlation = MagicMock()
    mock_correlation.symbol = 'SBL'

    tested = Server(b'', ('', 200), mock_server)

    # no data
    mock_correlation.data.return_value = []
    mock_correlation.matrix.return_value = []
    result = tested.table_html(mock_correlation)
    assert result is None

    calls = [
        call('<html>'),
        call('<head>'),
        call('<title>Correlation AAPL - ISS</title>'),
        call('</head>'),
        call('<body>'),
        call('<p>Correlation Matrix</p>'),
        call('<table border="1">'),
        call('</table>'),
        call('<p>Data</p>'),
        call('<table border="1">'),
        call('<tr>'),
        call('<th></th>'),
        call('</tr>'),
        call('<tr>'),
        call("<td>SBL</td>"),
        call('</tr>'),
        call('<tr>'),
        call('<td>Distance to Wall Street</td>'),
        call('</tr>'),
        call('</table>'),
        call('</body>'),
        call('</html>'),
    ]
    assert calls == write.mock_calls
    calls = [
        call.data(),
        call.matrix([]),
    ]
    assert calls == mock_correlation.mock_calls
    assert [] == mock_server.mock_calls
    write.reset_mock()
    mock_correlation.reset_mock()
    mock_server.reset_mock()

    # data
    mock_correlation.data.return_value = [
        ClosingLocation(day=date(2022, 11, 7), wall_street_distance=101.2, stock_close=351.3),
        ClosingLocation(day=date(2022, 11, 6), wall_street_distance=102.7, stock_close=358.3),
        ClosingLocation(day=date(2022, 11, 3), wall_street_distance=103.5, stock_close=319.3),
    ]
    mock_correlation.matrix.return_value = [[1.0, 0.75], [0.75, 1]]
    result = tested.table_html(mock_correlation)
    assert result is None

    calls = [
        call('<html>'),
        call('<head>'),
        call('<title>Correlation AAPL - ISS</title>'),
        call('</head>'),
        call('<body>'),
        call('<p>Correlation Matrix</p>'),
        call('<table border="1">'),
        call('<tr>'),
        call('<td>1.000</td><td>0.750</td>'),
        call('</tr>'),
        call('<tr>'),
        call('<td>0.750</td><td>1.000</td>'),
        call('</tr>'),
        call('</table>'),
        call('<p>Data</p>'),
        call('<table border="1">'),
        call('<tr>'),
        call('<th></th><th>2022-11-07</th><th>2022-11-06</th><th>2022-11-03</th>'),
        call('</tr>'),
        call('<tr>'),
        call('<td>SBL</td><td>351.300</td><td>358.300</td><td>319.300</td>'),
        call('</tr>'),
        call('<tr>'),
        call('<td>Distance to Wall Street</td><td>101.200</td><td>102.700</td><td>103.500</td>'),
        call('</tr>'),
        call('</table>'),
        call('</body>'),
        call('</html>'),
    ]
    assert calls == write.mock_calls
    calls = [
        call.data(),
        call.matrix([
            ClosingLocation(day=date(2022, 11, 7), wall_street_distance=101.2, stock_close=351.3),
            ClosingLocation(day=date(2022, 11, 6), wall_street_distance=102.7, stock_close=358.3),
            ClosingLocation(day=date(2022, 11, 3), wall_street_distance=103.5, stock_close=319.3),
        ]),
    ]
    assert calls == mock_correlation.mock_calls
    assert [] == mock_server.mock_calls
    write.reset_mock()
    mock_correlation.reset_mock()
    mock_server.reset_mock()


@patch.object(Server, '__init__', (lambda a, b, c, d: None))
@patch('libs.server.Server.write')
def test_table_csv(write):
    mock_server = MagicMock()
    mock_correlation = MagicMock()
    mock_correlation.symbol = 'SBL'

    tested = Server(b'', ('', 200), mock_server)

    # no data
    mock_correlation.data.return_value = []
    mock_correlation.matrix.return_value = []
    result = tested.table_csv(mock_correlation)
    assert result is None

    calls = [
        call('dates'),
        call('quotes'),
        call('distances'),
    ]
    assert calls == write.mock_calls
    calls = [
        call.data(),
        call.matrix([]),
    ]
    assert calls == mock_correlation.mock_calls
    assert [] == mock_server.mock_calls
    write.reset_mock()
    mock_correlation.reset_mock()
    mock_server.reset_mock()

    # data
    mock_correlation.data.return_value = [
        ClosingLocation(day=date(2022, 11, 7), wall_street_distance=101.2, stock_close=351.3),
        ClosingLocation(day=date(2022, 11, 6), wall_street_distance=102.7, stock_close=358.3),
        ClosingLocation(day=date(2022, 11, 3), wall_street_distance=103.5, stock_close=319.3),
    ]
    mock_correlation.matrix.return_value = [[1.0, 0.75], [0.75, 1]]
    result = tested.table_csv(mock_correlation)
    assert result is None

    calls = [
        call('dates,2022-11-07,2022-11-06,2022-11-03'),
        call('quotes,351.300,358.300,319.300'),
        call('distances,101.200,102.700,103.500'),
        call('row01,1.000,0.750'),
        call('row02,0.750,1.000'),
    ]
    assert calls == write.mock_calls
    calls = [
        call.data(),
        call.matrix([
            ClosingLocation(day=date(2022, 11, 7), wall_street_distance=101.2, stock_close=351.3),
            ClosingLocation(day=date(2022, 11, 6), wall_street_distance=102.7, stock_close=358.3),
            ClosingLocation(day=date(2022, 11, 3), wall_street_distance=103.5, stock_close=319.3),
        ]),
    ]
    assert calls == mock_correlation.mock_calls
    assert [] == mock_server.mock_calls
    write.reset_mock()
    mock_correlation.reset_mock()
    mock_server.reset_mock()


@patch.object(Server, '__init__', (lambda a, b, c, d: None))
def test_write():
    mock_wfile = MagicMock()
    mock_server = MagicMock()
    tested = Server(b'', ('', 200), mock_server)
    tested.wfile = mock_wfile

    tested.write('some text')
    calls = [call.write(b'some text\n')]
    assert calls == mock_wfile.mock_calls


@patch.object(Server, '__init__', (lambda a, b, c, d: None))
@patch('libs.server.Correlation')
@patch('libs.server.Server.table_html')
@patch('libs.server.Server.table_csv')
def test_do_GET(table_csv, table_html, correlation):
    mock_server = MagicMock()
    mock_attributes = MagicMock()
    tested = Server(b'', ('', 200), mock_server)

    # add attributes they are
    tested.log_request = mock_attributes
    tested.requestline = mock_attributes
    tested.client_address = mock_attributes
    tested.request_version = mock_attributes
    tested.wfile = mock_attributes
    tested.version_string = lambda: 'server version'
    tested.date_time_string = lambda: 'time now'
    tested.request_version = 'HTTP/1.0'

    mock_attributes.requestline.return_value = 'requested line'
    mock_attributes.client_address.return_value = 'client address'

    # HTML
    tested.path = '/?date=2022-11-03&format=html'
    tested.do_GET()
    calls = [
        call(200),
        call.write(b'HTTP/1.0 200 OK\r\nServer: server version\r\nDate: time now\r\nContent-type: text/html\r\n\r\n'),
    ]
    assert calls == mock_attributes.mock_calls
    calls = []
    assert calls == table_csv.mock_calls
    calls = [call(correlation.return_value)]
    assert calls == table_html.mock_calls
    calls = [call('AAPL', date(2022, 11, 3))]
    assert calls == correlation.mock_calls
    mock_attributes.reset_mock()
    table_csv.reset_mock()
    table_html.reset_mock()
    correlation.reset_mock()

    # csv
    tested.path = '/?date=2022-11-03'
    tested.do_GET()
    calls = [
        call(200),
        call.write(b'HTTP/1.0 200 OK\r\nServer: server version\r\nDate: time now\r\nContent-type: text/plain\r\n\r\n'),
    ]
    assert calls == mock_attributes.mock_calls
    calls = [call(correlation.return_value)]
    assert calls == table_csv.mock_calls
    calls = []
    assert calls == table_html.mock_calls
    calls = [call('AAPL', date(2022, 11, 3))]
    assert calls == correlation.mock_calls
    mock_attributes.reset_mock()
    table_csv.reset_mock()
    table_html.reset_mock()
    correlation.reset_mock()
