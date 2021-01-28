from http import HTTPStatus
from typing import Any, Callable, Coroutine, List

from aiohttp import ClientSession

from tele2client import containers, enums, exceptions, time_utils
from tele2client.api import ApiTele2, create_session
from tele2client.wrappers import LoggerWrap

SmsCodeGetterType = Callable[[], Coroutine[Any, Any, str]]


class Tele2Client(object):
    ENTER_SMS_CODE_TIMEOUT = 60

    api: ApiTele2
    session: ClientSession
    phone_number: str
    access_token: containers.AccessToken

    def __init__(self, phone_number: str):
        self.phone_number = phone_number
        self.access_token = containers.AccessToken()
        self._create_session()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def close(self):
        if self.session is not None:
            await self.session.close()

    def _create_session(self):
        self.session = create_session(self.access_token.token)
        self.api = ApiTele2(self.session, self.phone_number)

    async def _refresh_session(self):
        await self.close()
        self._create_session()

    async def auth_with_params(self, access_token: containers.AccessToken, phone_number: str = None):
        if phone_number is not None:
            self.phone_number = phone_number
        self.access_token = access_token
        await self._refresh_session()

    async def auth(self, sms_code_getter: SmsCodeGetterType) -> bool:
        try:
            self.access_token = await self._get_access_token(sms_code_getter)
        except exceptions.BaseTele2ClientException as e:
            LoggerWrap().get_logger().exception(str(e))
            return False
        await self._refresh_session()
        return True

    async def _get_access_token(self, sms_code_getter: SmsCodeGetterType) -> containers.AccessToken:
        await self.api.request_sms_code()
        deadline = time_utils.future_timestamp(self.ENTER_SMS_CODE_TIMEOUT)
        while not time_utils.is_expired_timestamp(deadline):
            sms_code = await sms_code_getter()
            try:
                return await self.api.get_access_token(sms_code)
            except exceptions.IncorrectFormatResponse as e:
                LoggerWrap().get_logger().exception(str(e))
                continue
            except exceptions.ApiException as e:
                if e.response.status != HTTPStatus.UNAUTHORIZED:
                    LoggerWrap().get_logger().exception(str(e))
                continue

        raise exceptions.TimeExpired('Истекло время на получение токена достута')

    async def is_authorized(self) -> bool:
        try:
            await self.get_balance()
        except exceptions.BaseTele2ClientException as e:
            LoggerWrap().get_logger().exception(str(e))
            return False
        return True

    async def get_balance(self) -> float:
        """
        :raises:
            ApiException: если не удалось выполнить запрос
            IncorrectFormatResponse: если не удалось загрузить данные из ответа
        """
        return await self.api.get_balance()

    async def create_lot(self, lot: containers.Lot) -> containers.LotInfo:
        """
        :raises:
           ApiException: если не удалось выполнить запрос
           IncorrectFormatResponse: если не удалось загрузить данные из ответа
           FailedConversion: если не удалось создать тело запроса
        """
        return await self.api.create_lot(lot)

    async def edit_lot(self, lot_info: containers.LotInfo) -> containers.LotInfo:
        """
        :raises:
           ApiException: если не удалось выполнить запрос
           IncorrectFormatResponse: если не удалось загрузить данные из ответа
           FailedConversion: если не удалось преобразовать данные из ответа
        """
        return await self.api.edit_lot(lot_info)

    async def delete_lot(self, lot_id: str) -> bool:
        return await self.api.delete_lot(lot_id)

    async def get_lots(self) -> List[containers.LotInfo]:
        """
        :raises:
            ApiException: если не удалось выполнить запрос
            IncorrectFormatResponse: если не удалось загрузить данные из ответа
            FailedConversion: если не удалось преобразовать данные из ответа
        """
        return await self.api.get_lots()

    async def get_rests(self) -> List[containers.Remain]:
        """
        Получить остатки тарифа

        :raises:
            ApiException: если не удалось выполнить запрос
            IncorrectFormatResponse: если не удалось загрузить данные из ответа
        """
        return await self.api.get_rests()

    async def get_sellable_rests(self) -> List[containers.Remain]:
        """
        :raises:
            ApiException: если не удалось выполнить запрос
            IncorrectFormatResponse: если не удалось загрузить данные из ответа
        """
        rests = await self.get_rests()
        return [remain for remain in rests if remain.type == enums.RemainType.TARIFF and not remain.rollover]
