#!/usr/bin/env python3
''' Regex-ing '''
import re
import logging
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'ip')


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    ''' filter datum '''
    pattern = f"({'|'.join(fields)})=([^{separator}]+)"
    return re.sub(pattern, r"\1=" + redaction, message)


def get_logger() -> logging.Logger:
    ''' Create logger '''
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    return logger


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
