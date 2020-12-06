from typing import Dict

from tele2client import containers, converter


def create_headers(access_token: str = '') -> Dict:
    return {
        'Authorization': f'Bearer {access_token}',
        'Connection': 'keep-alive',
        'X-API-Version': '1',
        'User-Agent': 'okhttp/4.2.0',
        'Tele2-User-Agent': '"mytele2-app/3.17.0"; "unknown"; "Android/9"; "Build/12998710"',
    }


def create_for_edit_lot(lot_info: containers.LotInfo) -> Dict:
    return {
        'showSellerName': True,
        'emojis': lot_info.seller.emojis,
        'cost': converter.cost2dict(lot_info.cost)
    }


def create_for_access(phone_number: str, sms_code: str) -> Dict:
    return {
        'client_id': 'digital-suite-web-app',
        'grant_type': 'password',
        'username': phone_number,
        'password': sms_code,
        'password_type': 'sms_code'
    }


def create_for_request_sms() -> Dict:
    return {'sender': 'Tele2'}


def create_for_create_lot(lot: containers.Lot) -> Dict:
    return {
        'trafficType': lot.type.value,
        'cost': {'amount': lot.cost, 'currency': 'rub'},
        'volume': {'value': lot.count, 'uom': lot.count_unit.value}
    }
