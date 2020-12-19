from http import HTTPStatus
from typing import List

from aiohttp import ClientSession

from tele2client import containers, converter, enums, event, exceptions, time_utils
from tele2client.api import ApiTele2, create_session
from tele2client.wrappers import LoggerWrap


class Tele2Client(object):
    ENTER_SMS_CODE_TIMEOUT = 60

    api: ApiTele2
    session: ClientSession = None
    phone_number: str
    access_token: containers.AccessToken

    def __init__(self, phone_number: str):
        self.phone_number = phone_number
        self.access_token = containers.AccessToken()
        self._refresh_session()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def close(self):
        if self.session is not None:
            await self.session.close()

    def _refresh_session(self):
        self.session = create_session(self.access_token.token)
        self.api = ApiTele2(self.session, self.phone_number)

    async def auth(self, sms_waiter: event.ValueWaiter) -> bool:
        try:
            self.access_token = await self._get_access_token(sms_waiter)
        except exceptions.BaseTele2ClientException as e:
            LoggerWrap().get_logger().exception(str(e))
            return False
        self._refresh_session()
        return True

    async def _get_access_token(self, sms_waiter: event.ValueWaiter) -> containers.AccessToken:
        await self.api.request_sms_code()
        deadline = time_utils.future_timestamp(self.ENTER_SMS_CODE_TIMEOUT)
        while not time_utils.is_expired_timestamp(deadline):
            sms_code = await sms_waiter.wait()
            try:
                return await self.api.get_access_token(sms_code)
            except exceptions.ApiException as e:
                if e.response.status != HTTPStatus.UNAUTHORIZED:
                    LoggerWrap().get_logger().exception(str(e))
                continue

        raise exceptions.TimeExpired('Истекло время на получение токена достута')

    async def is_authorized(self) -> bool:
        try:
            await self.get_balance()
        except exceptions.ApiException as e:
            LoggerWrap().get_logger().exception(str(e))
            return False
        return True

    async def get_balance(self) -> float:
        return await self.api.get_balance()

    async def create_lot(self, lot: containers.Lot) -> containers.LotInfo:
        return await self.api.create_lot(lot)

    async def edit_lot(self, lot_info: containers.LotInfo) -> containers.LotInfo:
        return await self.api.edit_lot(lot_info)

    async def delete_lot(self, lot_id: str) -> bool:
        return await self.api.delete_lot(lot_id)

    async def get_lots(self) -> List[containers.LotInfo]:
        try:
            return await self.api.get_lots()
        except exceptions.ApiException as e:
            LoggerWrap().get_logger().exception(str(e))
        return []

    async def get_active_lots(self) -> List[containers.LotInfo]:
        lots = await self.get_lots()
        return [lot_info for lot_info in lots if lot_info.status == enums.LotStatus.ACTIVE]

    async def get_rests(self) -> List[containers.Remain]:
        try:
            return await self.api.get_rests()
        except exceptions.ApiException as e:
            LoggerWrap().get_logger().exception(str(e))
        return []

    async def get_sellable_rests(self) -> containers.RemainCounter:
        rests = await self.get_rests()
        counter = containers.RemainCounter()
        for remain in rests:
            if remain.type != enums.RemainType.TARIFF:
                continue

            if remain.unit == enums.Unit.MINUTES:
                counter.increment_minutes(remain.value)
            elif remain.unit == enums.Unit.MEGABYTES:
                counter.increment_gigabytes(converter.megabytes2gigabytes(remain.value))
            else:
                LoggerWrap().get_logger().warning('Неизвестная единица измерения', remain)

        return counter
