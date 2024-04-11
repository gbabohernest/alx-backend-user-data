#!/usr/bin/env python3
"""
Write a function called filter_datum that returns the
log message obfuscated:

    Arguments:
        fields: a list of strings representing all fields
                to obfuscate
        redaction: a string representing by what the field
                   will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character
                   is separating all fields in the log line (message)

    The function should use a regex to replace occurrences of
    certain field values.
    filter_datum should be less than 5 lines long and use re.sub
    to perform the substitution with a single regex.
"""

import logging
from logging import Logger, StreamHandler
import re
from typing import List, Tuple

PII_FIELDS: Tuple = ("email", "phone", "ssn", "password", "ip")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] or Tuple[str]):
        """ Initialize"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Filter values in incoming log records"""
        def filter_datum(fields: List[str], redaction: str,
                         message: str, separator: str) -> str:
            """ A function that returns the log message obfuscated."""
            pattern = '|'.join(fields)
            return re.sub(f'({pattern})=[^{separator}]*',
                          f'\\1={redaction}', message)
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


def get_logger() -> Logger:
    """ Return a logging.Logger object."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(fields=PII_FIELDS)

    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger