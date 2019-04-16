# -*- coding: utf-8 -*-
import re


class ImproperlyConfigured(Exception):
    pass


class ClickhouseFormatterError(Exception):
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


class ClickHouseError(Exception):
    default_error_msg = "ClickHouse internal error"

    def __init__(self, code: int, message: str = None) -> None:
        super().__init__()
        self.message = message
        self.code = code

    def __str__(self):
        return f"({self.code}): {self.message}"

    @classmethod
    def from_raw_error_string(cls, raw_error: str):
        err_regex = re.compile(r"^code:\s+(?P<error_code>\d+)", re.IGNORECASE)

        found = re.search(err_regex, raw_error)
        error_code = found.group('error_code') if found else "-1"

        return cls(code=int(error_code), message=raw_error)
