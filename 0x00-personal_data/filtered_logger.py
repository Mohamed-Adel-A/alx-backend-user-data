#!/usr/bin/env python3
"""
Module for filtering sensitive data in log messages.
"""

import re
import typing


def filter_datum(fields: typing.List[str], redaction: str, message: str, separator: str) -> str:
    """
    Replace occurrences of certain field values in a log message.
    """
    for field in fields:
        pattern = f'{re.escape(field)}=.+?{re.escape(separator)}'
        message = re.sub(pattern, f'{field}={redaction}{separator}', message)
    return message


if __name__ == "__main__":
    fields = ["password", "date_of_birth"]
    messages = ["name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;",
                "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"]
    separator = ";"
    for message in messages:
        print(filter_datum(fields, 'xxx', message, separator))
