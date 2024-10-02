import os

from aws_lambda_powertools import Logger as Logging


class Logger:
    @staticmethod
    def get_logger():
        log = Logging(
            service=os.getenv("AWS_LAMBDA_FUNCTION_NAME", "pd2-lambda"),
            level=os.getenv("LOGLEVEL", "DEBUG"),
        )
        return log
