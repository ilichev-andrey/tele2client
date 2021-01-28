from typing import Dict, Iterable, Tuple, List, NoReturn

from dateutil import parser

from tele2client import containers, converter, exceptions, time_utils
from tele2client.enums import LotStatus, RemainType, RemainStatus, TrafficType, Unit


def _has_keys(sequence: Iterable, keys: Tuple[str, ...]) -> bool:
    for key in keys:
        if key not in sequence:
            return False
    return True


def _assert_has_data(data: Dict) -> NoReturn:
    """
    :raises:
        IncorrectFormatResponse: если отсутствует параметр 'data'
    """
    if 'data' not in data:
        raise exceptions.IncorrectFormatResponse('Не найден параметр: data', data)


def _assert_keys(data: Dict, keys: Tuple[str, ...]) -> NoReturn:
    """
    :raises:
        IncorrectFormatResponse: если один из ключей отсутствует
    """
    if not _has_keys(data, keys):
        raise exceptions.IncorrectFormatResponse(f'Не найдены параметры: {keys}', data)


def get_data(response: Dict) -> List[Dict] or Dict:
    """
    :raises:
        IncorrectFormatResponse: если отсутствует параметр 'data'
    """
    _assert_has_data(response)
    return response['data']


def load_access_token(data: Dict) -> containers.AccessToken:
    """
    :raises:
        IncorrectFormatResponse: если отсутствуют параметры: 'access_token' и 'expires_in'
    """
    _assert_keys(data, ('access_token', 'expires_in'))

    return containers.AccessToken(
        token=data['access_token'],
        expired_dt=time_utils.timestamp2datetime(time_utils.future_timestamp(data['expires_in']))
    )


def load_balance(data: Dict) -> float:
    """
    :raises:
        IncorrectFormatResponse: если отсутствует параметр 'value'
    """
    _assert_keys(data, ('value',))
    return data['value']


def load_seller_lot(data: Dict) -> containers.SellerLot:
    """
    :raises:
        IncorrectFormatResponse: если отсутствуют параметры: 'name' и 'emojis'
    """
    _assert_keys(data, ('name', 'emojis'))
    return containers.SellerLot(name=data['name'], emojis=data['emojis'])


def load_lot_volume(data: Dict) -> containers.LotVolume:
    """
    :raises:
        IncorrectFormatResponse: если отсутствуют параметры: 'value' и 'uom'
    """
    _assert_keys(data, ('value', 'uom'))
    return containers.LotVolume(count=data['value'], unit=data['uom'])


def load_lot_cost(data: Dict) -> containers.LotCost:
    """
    :raises:
        IncorrectFormatResponse: если отсутствуют параметры: 'amount' и 'currency'
    """
    _assert_keys(data, ('amount', 'currency'))
    return containers.LotCost(amount=data['amount'], currency=data['currency'])


def load_lot_info(data: Dict) -> containers.LotInfo:
    """
    :raises:
        IncorrectFormatResponse: если отсутствуют параметры
        FailedConversion: если не удалось преобразовать данные
    """

    _assert_keys(data, ('id', 'seller', 'trafficType', 'cost', 'status', 'creationDate'))
    traffic_type = TrafficType(data['trafficType'])
    return containers.LotInfo(
        id=data['id'],
        seller=load_seller_lot(data['seller']),
        type=converter.get_lot_type_by_traffic_type(traffic_type),
        traffic_type=traffic_type,
        volume=load_lot_volume(data['volume']),
        cost=load_lot_cost(data['cost']),
        status=LotStatus(data['status']),
        create_dt=parser.parse(data['creationDate'], ignoretz=True)
    )


def load_lots_info(data: List[Dict]) -> List[containers.LotInfo]:
    """
    :raises:
        IncorrectFormatResponse: если отсутствуют параметры
        FailedConversion: если не удалось преобразовать данные
    """
    return [load_lot_info(item) for item in data]


def load_remain(data: Dict) -> containers.Remain:
    """
    :raises:
        IncorrectFormatResponse: если отсутствуют параметры
    """
    _assert_keys(data, ('type', 'rollover', 'status', 'remain', 'uom'))
    return containers.Remain(
        type=RemainType(data['type']),
        status=RemainStatus(data['status']),
        value=data['remain'],
        unit=Unit(data['uom']),
        rollover=data['rollover']
    )


def load_rests(data: Dict) -> List[containers.Remain]:
    """
    :raises:
        IncorrectFormatResponse: если отсутствует параметр 'rests'
    """
    _assert_keys(data, ('rests',))
    return [load_remain(remain) for remain in data['rests']]
