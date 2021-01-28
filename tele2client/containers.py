from datetime import datetime
from typing import NamedTuple, List

from tele2client import enums


class AccessToken(NamedTuple):
    token: str = ''
    expired_dt: datetime = None


class LotVolume(NamedTuple):
    count: int
    unit: enums.Unit


class Lot(NamedTuple):
    type: enums.LotType
    volume: LotVolume
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
    volume: LotVolume
    cost: LotCost
    status: enums.LotStatus
    create_dt: datetime


class Remain(NamedTuple):
    type: enums.RemainType
    status: enums.RemainStatus
    value: int
    unit: enums.Unit
    rollover: bool
