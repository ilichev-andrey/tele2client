from typing import Dict, Iterable, Tuple, List, NoReturn

from dateutil import parser

from tele2client import containers, exceptions, time_utils
from tele2client.enums import LotStatus, RemainType, RemainStatus, TrafficType, Unit


def _has_keys(sequence: Iterable, keys: Tuple[str, ...]) -> bool:
    for key in keys:
        if key not in sequence:
            return False
    return True


def _assert_has_data(data: Dict) -> NoReturn:
    if 'data' not in data:
        raise exceptions.IncorrectFormatResponse('Не найден параметр: data', data)


def _assert_keys(data: Dict, keys: Tuple[str, ...]) -> NoReturn:
    if not _has_keys(data, keys):
        raise exceptions.IncorrectFormatResponse(f'Не найдены параметры: {keys}', data)


def get_data(response: Dict) -> List[Dict] or Dict:
    _assert_has_data(response)
    return response['data']


def load_access_token(data: Dict) -> containers.AccessToken:
    _assert_keys(data, ('access_token', 'expires_in'))

    return containers.AccessToken(
        token=data['access_token'],
        expired_dt=time_utils.timestamp2datetime(time_utils.future(data['expires_in']))
    )


def load_balance(data: Dict) -> float:
    _assert_keys(data, ('value',))
    return data['value']


def load_seller_lot(data: Dict) -> containers.SellerLot:
    _assert_keys(data, ('name', 'emojis'))
    return containers.SellerLot(name=data['name'], emojis=data['emojis'])


def load_lot_cost(data: Dict) -> containers.LotCost:
    _assert_keys(data, ('amount', 'currency'))
    return containers.LotCost(amount=data['amount'], currency=data['currency'])


def load_lot_info(data: Dict) -> containers.LotInfo:
    _assert_keys(data, ('id', 'seller', 'trafficType', 'cost', 'status', 'creationDate'))
    return containers.LotInfo(
        id=data['id'],
        seller=load_seller_lot(data['seller']),
        traffic_type=TrafficType(data['trafficType']),
        cost=load_lot_cost(data['cost']),
        status=LotStatus(data['status']),
        create_dt=parser.parse(data['creationDate'])
    )


def load_lots_info(data: List[Dict]) -> List[containers.LotInfo]:
    return [load_lot_info(item) for item in data]


def load_remain(data: Dict) -> containers.Remain:
    _assert_keys(data, ('type', 'status', 'remain', 'uom'))
    return containers.Remain(
        type=RemainType(data['type']),
        status=RemainStatus('active'),
        value=data['remain'],
        unit=Unit(data['uom'])
    )


def load_rests(data: Dict) -> List[containers.Remain]:
    _assert_keys(data, ('rests',))
    return [load_remain(remain) for remain in data['rests']]
