#!/usr/bin/env python3
''' Regex-ing '''
import re
import os
import logging
import mysql.connector
from typing import List
from mysql.connector import Error


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
) -> str:
    ''' filter datum '''
    pattern = f"({'|'.join(fields)})=([^{separator}]+)"
    return re.sub(pattern, r"\1=" + redaction, message)


def get_logger() -> logging.Logger:
    ''' Creates a new logger for user data. '''
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    ''' returns a connector to the database '''
    config = {
        'host': os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost'),
        'user': os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root'),
        'passwd': os.environ.get('PERSONAL_DATA_DB_PASSWORD', ''),
        'database': os.environ['PERSONAL_DATA_DB_NAME']
    }
    try:
        connection = mysql.connector.connect(**config)
        return connection
    except Error as e:
        print(e)
        return None


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        ''' formats a LogRecord. '''
        msg = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
