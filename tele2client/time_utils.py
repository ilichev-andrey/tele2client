import os

from datetime import datetime
from time import time


def set_tim_zone():
    os.environ['TZ'] = 'Europe/Moscow'


def now() -> float:
    return time()


def is_expired(time_us: float) -> bool:
    return now() - time_us > 0


def future(time_us: float) -> float:
    return now() + time_us


def timestamp2datetime(timestamp: int or float) -> datetime:
    return datetime.fromtimestamp(timestamp)
