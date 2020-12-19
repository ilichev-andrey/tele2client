from datetime import datetime
from typing import NamedTuple, List

from tele2client import enums


class AccessToken(NamedTuple):
    token: str = ''
    expired_dt: datetime = None


class Lot(NamedTuple):
    type: enums.LotType
    count: int
    count_unit: enums.Unit
    cost: int


class SellerLot(NamedTuple):
    name: str = ''
    emojis: List[str] = []


class LotCost(NamedTuple):
    amount: int
    currency: str


class LotInfo(NamedTuple):
    id: str
    seller: SellerLot
    type: enums.LotType
    traffic_type: enums.TrafficType
    cost: LotCost
    status: enums.LotStatus
    create_dt: datetime


class Remain(NamedTuple):
    type: enums.RemainType
    status: enums.RemainStatus
    value: int
    unit: enums.Unit


class RemainCounter(object):
    __slots__ = ('minutes', 'gigabytes', 'sms')

    minutes: int
    gigabytes: float
    sms: int

    def __init__(self, minutes: int = 0, gigabytes: float = 0.0, sms: int = 0):
        self.minutes = minutes
        self.gigabytes = gigabytes
        self.sms = sms

    def __repr__(self):
        return f'{self.__class__.__name__}(minutes={self.minutes}, gigabytes={self.gigabytes}, sms={self.sms})'

    def increment_minutes(self, minutes: int):
        self.minutes += int(minutes)

    def increment_gigabytes(self, gigabytes: float):
        self.gigabytes += float(gigabytes)

    def increment_sms(self, sms: int):
        self.sms += int(sms)
