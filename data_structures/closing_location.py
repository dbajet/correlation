from datetime import date
from typing import NamedTuple


class ClosingLocation(NamedTuple):
    day: date
    wall_street_distance: float
    stock_close: float
