#!/usr/bin/env python3
"""
Module for filtering sensitive data in log messages.
"""

import re
import typing
import logging
import os
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: typing.List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Replace occurrences of certain field values in a log message.
    """
    for field in fields:
        pattern = f'{re.escape(field)}=.+?{re.escape(separator)}'
        message = re.sub(pattern, f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """
    Return a Logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Creates a connector to a database.
    """
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "my_db")
    connection = mysql.connector.connect(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )
    return connection


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
