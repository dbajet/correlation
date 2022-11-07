from datetime import datetime
from functools import lru_cache
from math import degrees
from math import sin, cos, acos
from typing import List

import ephem

from immutables.geo_location import GeoLocation
from libs.http_request import HttpRequest
from immutables.tle import Tle


class IssDistance:
    @classmethod
    @lru_cache  # real production code would limit the cache to prevent memory leak
    def get_tle(cls) -> Tle:
        """
        Return the ISS part of the TLE from http://celestrak.org/NORAD/elements/stations.txt

        The result is memoize

        The code below is totally inspired by https://github.com/open-notify/Open-Notify-API/blob/master/iss.py

        :return: Tles
        """
        iss_tle: List[str] = []
        url = 'http://celestrak.org/NORAD/elements/stations.txt'
        count = 3
        for line in HttpRequest.get(url):
            if line.startswith('ISS') is True or count < 3:
                count -= 1
                iss_tle.append(line.strip())
            if count <= 0:
                return Tle(title=iss_tle[0].strip(), line_1=iss_tle[1].strip(), line_2=iss_tle[2].strip())
        return Tle(title='', line_1='', line_2='')

    @classmethod
    def get_location(cls, now: datetime) -> GeoLocation:
        """
        Compute the location of the ISS at the time provided

        :param now: datetime
        :return: GeoLocation
        """
        tle = cls.get_tle()
        iss = ephem.readtle(tle.title, tle.line_1, tle.line_2)
        iss.compute(now)
        return GeoLocation(latitude=degrees(iss.sublat), longitude=degrees(iss.sublat))

    @classmethod
    def get_distance_from(cls, location: GeoLocation, now: datetime) -> float:
        """
        compute the approximate distance in kilometers between the ISS and the provided location at the provided time

        :param location: GeoLocation
        :param now: datetime
        :return: float
        """
        """"""
        earth_radius = 6371.0
        iss = cls.get_location(now)
        return (earth_radius * acos(
            (
                    sin(iss.latitude) * sin(location.latitude)
            )
            + (
                    cos(iss.latitude)
                    * cos(location.latitude)
                    * cos(iss.longitude - location.longitude)
            )
        ))
