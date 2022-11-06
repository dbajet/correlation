import json
import re
from datetime import datetime, timedelta, date, time
from functools import lru_cache
from typing import List, Dict

from data_structures.quote import Quote
from libs.http_request import HttpRequest


class StockQuote:

    @classmethod
    @lru_cache
    def last_year_quotes(cls, symbol: str, until: date) -> List[Quote]:
        """
        Retrieve the quotes from the Nasdaq of the provided symbol for one year until the provided date

        The call is memoize.

        :param until: date
        :param symbol: str
        :return: ascendant sorted list of Quotes
        """
        result: Dict[date, Quote] = {}
        date_to = min(datetime.now() + timedelta(days=-1), datetime.combine(until, time(0, 0))).date()
        date_from = date_to.replace(year=date_to.year - 1)

        url = (f'https://api.nasdaq.com/api/quote/{symbol}/historical?'
               f'assetclass=stocks&'
               f'fromdate={date_from.isoformat()}&'
               f'limit=9999&'
               f'todate={date_to.isoformat()}')

        for line in HttpRequest.get(url):
            # extract the list of the quotes
            table = json.loads(line).get('data', {}).get('tradesTable', {}).get('rows', [])
            # regular expression to remove the first characters that are the devise
            pattern = r'[~0-9]+(?P<value>\d+\.\d+)'
            for record in table:
                day = datetime.strptime(record['date'], '%m/%d/%Y').date()
                opening = re.search(pattern, record['open'])
                closing = re.search(pattern, record['close'])
                if opening and closing:
                    result[day] = Quote(day=day, open=float(opening['value']), close=float(closing['value']))

        return [result[day] for day in sorted(result, reverse=True)]
