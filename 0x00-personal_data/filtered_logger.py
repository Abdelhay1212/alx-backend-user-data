#!/usr/bin/env python3
''' Regex-ing '''
import re
from typing import List


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    ''' filter datum '''
    pattern = f"({'|'.join(fields)})=([^{separator}]+)"
    return re.sub(pattern,r"\1=" + redaction, message)
