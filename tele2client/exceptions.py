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

    def __init__(self, message: str, response: ClientResponse, request_json: Dict = None):
        super().__init__(message)
        self.request_json = request_json
        self.response = response

    def __str__(self):
        return f'{super().__str__()}\nrequest_json={self.request_json}\nresponse: {self._response_to_str()}'

    def _response_to_str(self):
        return f'status={self.response.status} ({self.response.reason}) content={self.response.content}'


class IncorrectFormatResponse(BaseTele2ClientException):
    """Неожидаемый формат ответа API-метода"""
    pass


class TimeExpired(BaseTele2ClientException):
    """Истекло время выполнения"""
    pass


class FailedConversion(BaseTele2ClientException):
    """Не удалось преоразовать данные"""
    pass
