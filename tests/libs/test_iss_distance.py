from datetime import datetime, timezone
from unittest.mock import patch, call

from data_structures.geo_location import GeoLocation
from data_structures.tle import Tle
from libs.iss_distance import IssDistance


@patch('libs.iss_distance.HttpRequest')
def test_get_tle(http_request):
    tested = IssDistance

    # no ISS record
    http_request.get.return_value = [
        'AEROCUBE 12A',
        '1 43556U 18046C   22310.31064535  .00036429  00000+0  73980-3 0  9990',
        '2 43556  51.6350 209.5382 0008169 177.7338 182.3687 15.45946985241204',
        'AEROCUBE 12B',
        '1 43557U 18046D   22310.15913582  .00028708  00000+0  66123-3 0  9990',
        '2 43557  51.6365 217.4339 0007904 173.8650 186.2433 15.42345084241034',
    ]
    result = tested.get_tle()
    expected = Tle(title='', line_1='', line_2='')
    assert result == expected
    calls = [
        call.get('http://celestrak.org/NORAD/elements/stations.txt'),
    ]
    assert http_request.mock_calls == calls
    http_request.reset_mock()

    # ISS record
    http_request.get.return_value = [
        'AEROCUBE 12A',
        '1 43556U 18046C   22310.31064535  .00036429  00000+0  73980-3 0  9990',
        '2 43556  51.6350 209.5382 0008169 177.7338 182.3687 15.45946985241204',
        'ISS(ZARYA)',
        '1 25544U 98067A   22310.62286084  .00017184  00000+0  31024-3 0  9997',
        '2 25544  51.6453 350.9803 0006494  46.4928  41.5169 15.49816683367272',
        'AEROCUBE 12B',
        '1 43557U 18046D   22310.15913582  .00028708  00000+0  66123-3 0  9990',
        '2 43557  51.6365 217.4339 0007904 173.8650 186.2433 15.42345084241034',
    ]
    # -- result is cached
    result = tested.get_tle()
    expected = Tle(title='', line_1='', line_2='')
    assert result == expected
    assert http_request.mock_calls == []
    http_request.reset_mock()
    # -- cache cleared
    tested.get_tle.cache_clear()
    result = tested.get_tle()
    expected = Tle(
        title='ISS(ZARYA)',
        line_1='1 25544U 98067A   22310.62286084  .00017184  00000+0  31024-3 0  9997',
        line_2='2 25544  51.6453 350.9803 0006494  46.4928  41.5169 15.49816683367272',
    )
    assert result == expected
    calls = [
        call.get('http://celestrak.org/NORAD/elements/stations.txt'),
    ]
    assert http_request.mock_calls == calls
    http_request.reset_mock()


def test_get_location():
    tested = IssDistance
    tests = [
        (datetime(2022, 2, 28, 17, 0, tzinfo=timezone.utc), GeoLocation(latitude=18.399686095651855, longitude=18.399686095651855)),
        (datetime(2022, 8, 3, 17, 0, tzinfo=timezone.utc), GeoLocation(latitude=-48.00652416637905, longitude=-48.00652416637905)),
        (datetime(2022, 11, 8, 17, 0, tzinfo=timezone.utc), GeoLocation(latitude=-24.29006001889107, longitude=-24.29006001889107)),
    ]
    for now, expected in tests:
        result = tested.get_location(now)
        assert result == expected, f'--> {now.date().isoformat()}'


def test_get_distance_from():
    tested = IssDistance
    tests = [
        (datetime(2022, 2, 28, 17, 0, tzinfo=timezone.utc), GeoLocation(latitude=18.399686095651855, longitude=18.399686095651855), 0.0),
        (datetime(2022, 8, 3, 17, 0, tzinfo=timezone.utc), GeoLocation(latitude=-48.0, longitude=-48.0), 49.29617699094003),
        (datetime(2022, 11, 8, 17, 0, tzinfo=timezone.utc), GeoLocation(latitude=-20.0, longitude=-20.0), 15839.071058513526),
    ]
    for now, location, expected in tests:
        result = tested.get_distance_from(location, now)
        assert result == expected, f'--> {now.date().isoformat()}'
