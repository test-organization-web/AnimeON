class TFCClientException(Exception):
    pass


class APIException(TFCClientException):

    def __init__(self, message, response):
        self.message = message
        self.response = response


class TokenMissing(Exception):
    def __init__(self):
        super().__init__('Спочатку треба отримати токен авторизації')