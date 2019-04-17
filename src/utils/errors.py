# -*- coding: utf-8 -*-


class ImproperlyConfigured(Exception):
    pass


class FilterValidationError(Exception):
    pass


class RequestError(Exception):
    """
    Base user exception class
    """
    def __init__(self, message: str, status: int = 400, payload: dict = None) -> None:
        super().__init__()
        self.message = message
        self.status = status
        self.payload = payload

    def __str__(self):
        return self.message
