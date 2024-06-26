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
import re
from typing import List
import os
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ A function that returns the log message obfuscated."""

    pattern = '|'.join(fields)
    return re.sub(f'({pattern})=[^{separator}]*', f'\\1={redaction}', message)


def get_logger() -> logging.Logger:
    """Get a logger object named 'user_data'."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(fields=PII_FIELDS)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connect to the MySQL database and
       return the connection object.
    """
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    if not db_name:
        raise ValueError("PERSONAL_DATA_DB_NAME environment variable not set.")

    try:
        connection = mysql.connector.connection.MySQLConnection(
            user=db_username,
            password=db_password,
            host=db_host,
            database=db_name
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL database: {err}")
        raise


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize RedactingFormatter object."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Filter values in incoming log records,
            Fromats the log record as text.
        """
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


def main():
    """Retrieve user data from database"""

    # Configure logger
    logger = get_logger()

    # Connect to the database
    try:
        db_connection = get_db()
        cursor = db_connection.cursor()

        # Fetch all rows from the users table
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        # Log each user data with redacted PII fields
        for user in users:
            filtered_user = {key: "***" if key in PII_FIELDS else value
                             for key, value in zip(cursor.column_names, user)}
            logger.info("Filtered user data: %s", filtered_user)

    except mysql.connector.Error as err:
        logger.error("Error connecting to database: %s", err)
    finally:
        if 'db_connection' in locals() and db_connection.is_connected():
            cursor.close()
            db_connection.close()


if __name__ == '__main__':
    main()
