#!/usr/bin/env python3
''' Regex-ing '''
import re


def filter_datum(fields, redaction, message, separator):
    ''' filter datum '''
    for field in fields:
        pattern = f'(?<={field}=)[^;]+'
        message = re.sub(pattern, redaction, message)
    return message
