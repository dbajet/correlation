from datetime import date
from typing import NamedTuple


class Quote(NamedTuple):
    day: date
    open: float
    close: float
