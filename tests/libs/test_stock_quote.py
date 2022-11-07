from datetime import date
from unittest.mock import patch, call

from data_structures.quote import Quote
from libs.stock_quote import StockQuote


@patch('libs.stock_quote.HttpRequest')
def test_last_year_quotes(http_request):
    tested = StockQuote

    # no response
    http_request.get.return_value = []
    result = tested.last_year_quotes('SYM', date(2022, 11, 8))
    assert result == []
    calls = [call.get('https://api.nasdaq.com/api/quote/SYM/historical?assetclass=stocks&fromdate=2021-11-05&limit=9999&todate=2022-11-05')]
    assert http_request.mock_calls == calls
    http_request.reset_mock()

    # response
    http_request.get.return_value = [(
        '{"data": {"symbol": "AAPL", "totalRecords": 251, "tradesTable":{'
        '"headers": {"date": "Date", "close": "Close/Last", "volume": "Volume", "open": "Open", "high": "High", "low": "Low"},'
        '"rows": ['
        '{"date": "11/04/2022", "close": "$138.38", "volume": "140,814,800", "open": "$142.09", "high": "$142.67", "low": "$134.38"},'
        '{"date": "11/03/2022", "close": "$138.88", "volume": "97,918,520", "open": "$142.06", "high": "$142.8", "low": "$138.75"},'
        '{"date": "11/02/2022", "close": "$145.03", "volume": "93,604,620", "open": "$148.945", "high": "$152.17", "low": "$145"},'
        '{"date": "11/01/2022", "close": "$150.65", "volume": "80,379,350", "open": "$155.08", "high": "$155.45", "low": "$149.13"},'
        '{"date": "10/31/2022", "close": "$153.34", "volume": "97,943,170", "open": "$153.155", "high": "$154.24", "low": "$151.92"}'
        ']'
        '}}}'
    )]
    # -- result is cached
    result = tested.last_year_quotes('SYM', date(2022, 11, 8))
    assert result == []
    assert http_request.mock_calls == []
    http_request.reset_mock()
    # -- cache is cleared
    tested.last_year_quotes.cache_clear()
    result = tested.last_year_quotes('SYM', date(2022, 11, 8))
    expected = [
        Quote(day=date(2022, 11, 4), open=2.09, close=8.38),
        Quote(day=date(2022, 11, 3), open=2.06, close=8.88),
        Quote(day=date(2022, 11, 2), open=8.945, close=5.03),
        Quote(day=date(2022, 11, 1), open=5.08, close=0.65),
        Quote(day=date(2022, 10, 31), open=3.155, close=3.34),
    ]
    assert result == expected
    calls = [call.get('https://api.nasdaq.com/api/quote/SYM/historical?assetclass=stocks&fromdate=2021-11-05&limit=9999&todate=2022-11-05')]
    assert http_request.mock_calls == calls
    http_request.reset_mock()
