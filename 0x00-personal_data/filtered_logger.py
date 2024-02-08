#!/usr/bin/env python3
''' Regex-ing '''
import re
from typing import List


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
    ) -> List[str]:
    ''' filter datum '''

    for field in fields:
        pattern = f'(?<={field}=)[^;]+'
        message = re.sub(pattern, redaction, message)

    return message
