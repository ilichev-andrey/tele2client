from typing import Dict

from tele2client import containers, enums, exceptions


def cost2dict(cost: containers.LotCost) -> Dict:
    return cost._asdict()


def megabytes2gigabytes(megabytes):
    return megabytes / 1024


def get_traffic_type_by_lot_type(lot_type: enums.LotType) -> enums.TrafficType:
    """
    :raises:
        FailedConversion: если некоректный тип лота
    """
    if lot_type == enums.LotType.INTERNET:
        return enums.TrafficType.INTERNET
    if lot_type == enums.LotType.VOICE:
        return enums.TrafficType.VOICE
    if lot_type == enums.LotType.SMS:
        return enums.TrafficType.SMS
    raise exceptions.FailedConversion('Некорректный тип лота', lot_type)


def get_lot_type_by_traffic_type(traffic_type: enums.TrafficType) -> enums.LotType:
    """
    :raises:
        FailedConversion: если некоректный тип трафика
    """
    if traffic_type == enums.TrafficType.INTERNET:
        return enums.LotType.INTERNET
    if traffic_type == enums.TrafficType.VOICE:
        return enums.LotType.VOICE
    if traffic_type == enums.TrafficType.SMS:
        return enums.LotType.SMS
    raise exceptions.FailedConversion('Некорректный тип трафика лота', traffic_type)


def lot_volume2dict(lot_volume: containers.LotVolume) -> Dict:
    return {'value': lot_volume.count, 'uom': lot_volume.unit.value}
