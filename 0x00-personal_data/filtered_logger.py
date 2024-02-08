#!/usr/bin/env python3
''' Regex-ing '''
import re
from typing import List


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    ''' filter datum '''
    for field in fields:
        message = re.sub(f'(?<={field}=)[^;]+', redaction, message)
    message = message.replace(';', separator)
    return message
