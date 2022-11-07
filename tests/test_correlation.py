from datetime import date, timezone, datetime, time
from unittest import mock
from unittest.mock import patch, call

from correlation import Correlation
from immutables.closing_location import ClosingLocation
from immutables.geo_location import GeoLocation
from immutables.quote import Quote


@mock.patch('correlation.datetime', wraps=datetime)
def test___init__(mock_datetime):
    mock_datetime.now.return_value = datetime(2022, 11, 9, 15, 37, 21, 123456, tzinfo=None)  # now is offset-naive
    tests = [
        (date(2022, 11, 7), 'SYM', date(2022, 11, 7)),
        (date(2022, 11, 8), 'SYM', date(2022, 11, 8)),
        (date(2022, 11, 9), 'SYM', date(2022, 11, 8)),
        (date(2022, 11, 10), 'SYM', date(2022, 11, 8)),

        (date(2022, 6, 7), 'SYM', date(2022, 6, 7)),
        #
        (date(2021, 11, 9), 'SYM', date(2021, 11, 9)),
        (date(2021, 11, 8), 'SYM', date(2021, 11, 8)),
        (date(2021, 11, 7), 'SYM', date(2022, 11, 8)),
        (date(2021, 11, 6), 'SYM', date(2022, 11, 8)),
        (date(2021, 11, 5), 'SYM', date(2022, 11, 8)),
    ]
    for on_day, symbol, exp_on_day in tests:
        tested = Correlation(symbol, on_day)
        assert tested.symbol == symbol
        assert tested.on_day == exp_on_day, f'---> {on_day}'
        calls = [call.now()]
        assert mock_datetime.mock_calls == calls
        mock_datetime.reset_mock()


@patch('correlation.IssDistance.get_distance_from')
@patch('correlation.StockQuote.last_year_quotes')
@mock.patch('correlation.datetime', wraps=datetime)
def test_data(mock_datetime, last_year_quotes, get_distance_from):
    mock_datetime.now.return_value = datetime(2022, 11, 9, 15, 37, 21, 123456, tzinfo=None)  # now is offset-naive
    last_year_quotes.return_value = [
        Quote(day=date(2022, 11, 7), close=351.3, open=347.9),
        Quote(day=date(2022, 11, 6), close=358.3, open=353.9),
        Quote(day=date(2022, 11, 3), close=319.3, open=357.9),
    ]
    get_distance_from.side_effect = [101.2, 102.7, 103.5]

    tested = Correlation('SYM', date(2022, 11, 7))
    result = tested.data()
    expected = [
        ClosingLocation(day=date(2022, 11, 7), wall_street_distance=101.2, stock_close=351.3),
        ClosingLocation(day=date(2022, 11, 6), wall_street_distance=102.7, stock_close=358.3),
        ClosingLocation(day=date(2022, 11, 3), wall_street_distance=103.5, stock_close=319.3),
    ]
    assert result == expected
    calls = [
        call.now(),
        call.now(),
        call.combine(date(2022, 11, 7), time(16, 0)),
        call.combine(date(2022, 11, 6), time(16, 0)),
        call.combine(date(2022, 11, 3), time(16, 0)),
    ]
    assert mock_datetime.mock_calls == calls
    calls = [call('SYM', date(2022, 11, 8))]
    assert last_year_quotes.mock_calls == calls
    calls = [
        call(GeoLocation(latitude=40.706005, longitude=-74.008827), datetime(2022, 11, 7, 20, 56, tzinfo=timezone.utc)),
        call(GeoLocation(latitude=40.706005, longitude=-74.008827), datetime(2022, 11, 6, 20, 56, tzinfo=timezone.utc)),
        call(GeoLocation(latitude=40.706005, longitude=-74.008827), datetime(2022, 11, 3, 20, 56, tzinfo=timezone.utc)),
    ]
    assert get_distance_from.mock_calls == calls
    mock_datetime.reset_mock()
    last_year_quotes.reset_mock()
    get_distance_from.reset_mock()


def test_matrix():
    data = [
        ClosingLocation(day=date(2022, 11, 7), wall_street_distance=101.2, stock_close=351.3),
        ClosingLocation(day=date(2022, 11, 6), wall_street_distance=102.7, stock_close=358.3),
        ClosingLocation(day=date(2022, 11, 3), wall_street_distance=103.5, stock_close=319.3),
    ]
    tested = Correlation
    result = tested.matrix(data)
    expected = [
        ['1.000000', '-0.647366'],
        ['-0.647366', '1.000000'],
    ]
    assert [[f'{column:1.6f}' for column in row] for row in result] == expected
