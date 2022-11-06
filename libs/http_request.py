from typing import Generator
from urllib.request import Request, urlopen


class HttpRequest:
    @classmethod
    def get(cls, url: str) -> Generator[str, None, None]:
        """
        Retrieve the content of the url and provide it line by line

        No exception is handled

        :param url: str
        :return: generator of strings
        """
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0)',
        }
        request = Request(url)
        for header, value in headers.items():
            request.add_header(header, value)

        with urlopen(request) as f:
            for line in f.read().decode('utf-8').split('\n'):
                yield line
