from datetime import date, datetime
from unittest import mock
from unittest.mock import patch, MagicMock

from server import Server


@mock.patch('server.datetime', wraps=datetime)
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
