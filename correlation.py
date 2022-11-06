from datetime import datetime, date, time, timedelta
from typing import List

from numpy import corrcoef, ndarray

from data_structures.closing_location import ClosingLocation
from data_structures.geo_location import GeoLocation
from libs.iss_distance import IssDistance
from libs.stock_quote import StockQuote


class Correlation:
    def __init__(self, symbol: str, on_day: date):
        """
        Create an instance of the Correlation class

        The days are limited between yesterday and one year before yesterday:
        + we cannot know the closing for today and future dates (we wish)
        + the TLE information retrieved allows only one year of computation

        Note, that historical TLEs could be retrieved in the page https://celestrak.org/NORAD/archives/ (https://celestrak.org/NORAD/archives/zarya.zip)
        It would just take more time to implement the solution while not providing more insights about our skills.

        :param symbol: str
        :param on_day: date
        """
        # limit the possible day to dates between yesterday and 1 year ago
        yesterday = (datetime.now() + timedelta(days=-1))
        last_year = yesterday.replace(year=yesterday.year - 1)
        if not (last_year.date() <= on_day <= yesterday.date()):
            on_day = yesterday.date()
        #
        self.symbol = symbol
        self.on_day = on_day

    def data(self) -> List[ClosingLocation]:
        """
        Identify for 5 consecutive business days, the tuples stock close / distance of the ISS to Wall Street at the closing time.
        The 5 business days are the 5 successive business days with the 5th being the provided day or the first one before.

        :return: list of ClosingLocation
        """

        wall_street_location = GeoLocation(latitude=40.706005, longitude=-74.008827)
        wall_street_end_time = time(14, 0)

        # retrieve the quotes for APPL from yesterday and for 1 year back
        yesterday = (datetime.now() + timedelta(days=-1))
        quotes = StockQuote.last_year_quotes(self.symbol, yesterday.date())
        # the quotes are sorted from the most recent to the oldest: retrieve the first date equals or before
        # the provided date, then the 4 following dates
        closings: List[ClosingLocation] = []
        for idx, quote in enumerate(quotes):
            if quote.day <= self.on_day:
                closings = [
                    ClosingLocation(
                        day=quote.day,
                        stock_close=quote.close,
                        wall_street_distance=IssDistance.get_distance_from(wall_street_location, datetime.combine(quote.day, wall_street_end_time))
                    )
                    for quote in quotes[idx:idx + 4]
                ]
                break

        return closings

    def matrix(self) -> ndarray:
        """
        Compute the correlation matrix out of the tuples stock close / distance of the ISS to Wall street at the closing time
        :return: ndarray
        """
        closings = self.data()
        x = [closing.stock_close for closing in closings]
        y = [closing.wall_street_distance for closing in closings]
        return corrcoef(x, y)
