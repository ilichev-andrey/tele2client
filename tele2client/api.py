from typing import List, NoReturn

from aiohttp import ClientSession

from tele2client import containers, exceptions, response_loader, request_creator


def create_session(access_token: str = ''):
    return ClientSession(headers=request_creator.create_headers(access_token))


class ApiTele2(object):
    created_lots_url: str
    rests_url: str
    balance_url: str
    validation_number_url: str
    auth_url: str
    session: ClientSession
    phone_number: str

    def __init__(self, session: ClientSession, phone_number: str):
        base_url = f'https://my.tele2.ru/api/subscribers/{phone_number}'
        self.created_lots_url = f'{base_url}/exchange/lots/created'
        self.rests_url = f'{base_url}/rests'
        self.balance_url = f'{base_url}/balance'
        self.validation_number_url = f'https://my.tele2.ru/api/validation/number/{phone_number}'
        self.auth_url = 'https://my.tele2.ru/auth/realms/tele2-b2c/protocol/openid-connect/token'

        self.session = session
        self.phone_number = phone_number

    async def get_access_token(self, sms_code: str) -> containers.AccessToken:
        request_json = request_creator.create_for_access(self.phone_number, sms_code)
        response = await self.session.post(self.auth_url, data=request_json)

        if response.ok:
            return response_loader.load_access_token(await response.json())

        raise exceptions.ApiException(f'Не удалось получить токен для: {self.phone_number}', response, request_json)

    async def request_sms_code(self) -> NoReturn:
        request_json = request_creator.create_for_request_sms()
        response = await self.session.post(self.validation_number_url, json=request_json)
        if not response.ok:
            message = f'Не удалось отправить смс подтверждение для: {self.phone_number}'
            raise exceptions.ApiException(message, response, request_json)

    async def get_balance(self) -> float:
        response = await self.session.get(self.balance_url)
        if response.ok:
            return response_loader.load_balance(response_loader.get_data(await response.json()))

        raise exceptions.ApiException(f'Не удалось получить баланс для: {self.phone_number}', response)

    async def create_lot(self, lot: containers.Lot) -> containers.LotInfo:
        request_json = request_creator.create_for_lot_creation(lot)
        response = await self.session.put(self.created_lots_url, json=request_json)
        if response.ok:
            return response_loader.load_lot_info(response_loader.get_data(await response.json()))

        raise exceptions.ApiException(f'Не удалось создать лот для: {self.phone_number}', response, request_json)

    async def edit_lot(self, lot_info: containers.LotInfo) -> containers.LotInfo:
        request_json = request_creator.create_for_edit_lot(lot_info)
        response = await self.session.put(self._get_lot_url(lot_info.id), json=request_json)

        if response.ok:
            return response_loader.load_lot_info(response_loader.get_data(await response.json()))

        message = f'Не удалось отредактировать лот для: {self.phone_number}'
        raise exceptions.ApiException(message, response, request_json)

    async def delete_lot(self, lot_id: str) -> bool:
        response = await self.session.delete(self._get_lot_url(lot_id))
        return response.ok

    def _get_lot_url(self, lot_id: str):
        return f'{self.created_lots_url}/{lot_id}'

    async def get_lots(self) -> List[containers.LotInfo]:
        response = await self.session.get(self.created_lots_url)
        if response.ok:
            return response_loader.load_lots_info(response_loader.get_data(await response.json()))

        raise exceptions.ApiException(f'Не удалось получить лоты для: {self.phone_number}', response)

    async def get_rests(self) -> List[containers.Remain]:
        """Получение остатков тарифа"""
        response = await self.session.get(self.rests_url)
        if response.ok:
            return response_loader.load_rests(response_loader.get_data(await response.json()))

        raise exceptions.ApiException('Не удалось получить инфтрмацию об остатках для: {self.phone_number}', response)
