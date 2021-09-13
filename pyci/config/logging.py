import datetime
import logging
import logging.handlers


class ISO6801Formatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        if datefmt:
            dt = datetime.datetime.now().astimezone().strftime(
                datefmt
            )
        else:
            dt = datetime.datetime.now().astimezone().strftime(
                "%Y-%m-%d %D:%M:%s"
            )

        return dt


class PasswordMaskingFilter(logging.Filter):
    def __init__(self, param=None):
        self.param = param

    def filter(self, record):
        """
        The call signature matches string interpolation: args can be a tuple or
        a lone dict
        """
        if isinstance(record.args, dict):
            record.args = self.sanitize_dict(record.args)
        else:
            record.args = tuple(self.sanitize_dict(i) for i in record.args)

        return True

    @staticmethod
    def sanitize_dict(dictionary):
        """sanitize the given dictionary"""
        if not isinstance(dictionary, dict):
            return dictionary

        if any(i for i in dictionary.keys() if 'password' in i):
            # Ensure that we won't clobber anything critical
            dictionary = dictionary.copy()

            for key in dictionary.items():
                if 'password' in key:
                    dictionary[key] = '*** PASSWORD ***'

        return dictionary


formatter_iso6801 = ISO6801Formatter(
    fmt="%(asctime)s  %(name)-10s %(levelname)-10s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S.%f%z"
)

formatter_default = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

filter_passwords = PasswordMaskingFilter()

handler_stdout = logging.StreamHandler(
    stream="ext://sys.stdout"
)

handler_file = logging.handlers.TimedRotatingFileHandler(
    filename="/var/log/pyci/log",
    when="midnight",
    utc=True,
    encoding="utf-8",
    backupCount=30
)
