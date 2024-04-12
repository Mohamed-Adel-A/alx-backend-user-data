#!/usr/bin/env python3
"""
Module for filtering sensitive data in log messages.
"""

import re
import typing
import logging


def filter_datum(fields: typing.List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Replace occurrences of certain field values in a log message.
    """
    for field in fields:
        pattern = f'{re.escape(field)}=.+?{re.escape(separator)}'
        message = re.sub(pattern, f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: typing.List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log message"""
        message = super().format(record)
        for field in self.fields:
            message = re.sub(f'{field}=.*?{self.SEPARATOR}',
                             f'{field}={self.REDACTION}{self.SEPARATOR}',
                             message)
        return message
