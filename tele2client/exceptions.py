from typing import Dict

from aiohttp import ClientResponse


class BaseTele2ClientException(Exception):
    pass


class InputDataException(BaseTele2ClientException):
    """Введены некорректные данные"""
    pass


class IncorrectPhoneNumber(InputDataException):
    """Введен некорректный номер телефона"""
    pass


class ApiException(BaseTele2ClientException):
    """Не удачное выполнение API-метода"""
    request_json: Dict
    response: ClientResponse

    def __init__(self, message: str, response: ClientResponse, request_json: Dict = None, *args, **kwargs):
        super().__init__(message, args, kwargs)
        self.request_json = request_json
        self.response = response


class IncorrectFormatResponse(BaseTele2ClientException):
    """Неожидаемый формат ответа API-метода"""
    pass


class TimeExpired(BaseTele2ClientException):
    """Истекло время выполнения"""
    pass
