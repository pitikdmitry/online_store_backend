from uuid import uuid4

import marshmallow as ma


def get_file_format(s: str) -> str:
    arr = s.split('/')
    if len(arr) == 0:
        raise ma.ValidationError(message=f"Bad file format {s}")

    return '.' + s.split('/')[-1]


def get_random_filename() -> str:
    return uuid4().hex
