from enum import Enum


class TrafficType(Enum):
    VOICE = 'voice'
    INTERNET = 'data'
    SMS = 'sms'


class LotType(Enum):
    INTERNET = 'internet'
    VOICE = 'voice'
    SMS = 'sms'


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
    SMS = 'sms'


class Emoji(Enum):
    COOL = 'cool'
    DEVIL = 'devil'
    RICH = 'rich'
