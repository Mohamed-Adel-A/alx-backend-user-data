#!/usr/bin/env python3
"""
Module for filtering sensitive data in log messages.
"""

import re
import typing


def filter_datum(fields: typing.List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Replace occurrences of certain field values in a log message.
    """
    for field in fields:
        pattern = f'{re.escape(field)}=.+?{re.escape(separator)}'
        message = re.sub(pattern, f'{field}={redaction}{separator}', message)
    return message
