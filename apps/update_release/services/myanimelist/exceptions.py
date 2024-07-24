class TFCClientException(Exception):
    pass


class APIException(TFCClientException):

    def __init__(self, status_code, message, response):
        self.message = message
        self.response = response
        self.status_code = status_code


class TokenMissing(Exception):
    def __init__(self):
        super().__init__('Спочатку треба отримати токен авторизації')