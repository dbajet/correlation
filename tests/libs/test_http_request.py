from unittest.mock import patch, call, Mock
from urllib.request import Request

from libs.http_request import HttpRequest


@patch('libs.http_request.urlopen')
def test_get(urlopen):
    tested = HttpRequest

    # no line
    urlopen.return_value.__enter__.return_value.read.return_value = b''
    result = [line for line in tested.get('http://go.to.no.where')]
    expected = ['']
    assert result == expected
    request = urlopen.mock_calls[0].args[0]
    assert isinstance(request, Request)
    assert 'http://go.to.no.where' == request.full_url
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0)',
    }
    assert headers == request.headers
    calls = [
        call(request),
        call().__enter__(),
        call().__enter__().read(),
        call().__exit__(None, None, None),
    ]
    assert urlopen.mock_calls == calls
    urlopen.reset_mock()

    # some response
    urlopen.return_value.__enter__.return_value.read.return_value = (
        b'line 1\n'
        b'line 2\n'
        b'line 3\n'
    )
    result = [line for line in tested.get('http://go.to.no.where')]
    expected = [
        'line 1',
        'line 2',
        'line 3',
        '',
    ]
    assert result == expected
    request = urlopen.mock_calls[0].args[0]
    assert isinstance(request, Request)
    assert 'http://go.to.no.where' == request.full_url
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0)',
    }
    assert headers == request.headers
    calls = [
        call(request),
        call().__enter__(),
        call().__enter__().read(),
        call().__exit__(None, None, None),
    ]
    assert urlopen.mock_calls == calls
    urlopen.reset_mock()
