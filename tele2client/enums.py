from enum import Enum


class TrafficType(Enum):
    MINUTES = 'voice'
    INTERNET = 'data'


class LotStatus(Enum):
    ACTIVE = 'active'
    REVOKED = 'revoked'
    BOUGHT = 'bought'
    EXPIRED = 'expired'


class RemainType(Enum):
    TARIFF = 'tariff'


class RemainStatus(Enum):
    ACTIVE = 'active'


class Unit(Enum):
    MEGABYTES = 'mb'
    GIGABYTES = 'gb'
    MINUTES = 'min'


class Emoji(Enum):
    COOL = 'cool'
    DEVIL = 'devil'
    RICH = 'rich'
