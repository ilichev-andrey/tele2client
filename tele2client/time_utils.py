import os

from datetime import datetime
from time import time


def set_tim_zone():
    os.environ['TZ'] = 'Europe/Moscow'


def now_timestamp() -> float:
    return time()


def is_expired(dt: datetime) -> bool:
    return datetime.now() >= dt


def is_expired_timestamp(time_us: float) -> bool:
    return now_timestamp() >= time_us


def future_timestamp(time_us: float) -> float:
    return now_timestamp() + time_us


def timestamp2datetime(timestamp: int or float) -> datetime:
    return datetime.fromtimestamp(timestamp)
