__author__ = 'vladimir'

import os
import sys
from uuid import uuid4
import logging
from logging import DEBUG, INFO, ERROR


reload(sys)
sys.setdefaultencoding("utf8")


COLORS = {
    'pink': '\033[95m',
    'blue': '\033[94m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'red': '\033[91m',
    'underline': '\033[4m',
    'bold': '\033[1m',
    'reset': '\033[0m',
}


class ColorizedFormatter(logging.Formatter):
    """Special trigger to colorize only system stdout"""

    def __init__(self, msg, use_color):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        record = logging.Formatter.format(self, record)
        for name in COLORS.keys():
            if "{{ %s }}" % name in record:
                if self.use_color:
                    record = record.replace("{{ %s }}" % name, COLORS[name])
                else:
                    record = record.replace("{{ %s }}" % name, "")
        return record


class Logger(object):
    DEFAULT_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"
    DEFAULT_LEVEL = INFO
    BASE_DIR = "log"

    def __init__(self, name):
        self.logger_id = str(uuid4())
        self.filename = os.path.join(self.BASE_DIR, "{}.log".format(name))
        if not os.path.isdir(self.BASE_DIR):
            os.mkdir(self.BASE_DIR)

        self.console_formatter = ColorizedFormatter(self.DEFAULT_FORMAT, use_color=True)
        self.syslog = logging.StreamHandler(sys.stdout)
        self.syslog.setFormatter(self.console_formatter)
        self.syslog.setLevel(self.DEFAULT_LEVEL)

        self.file_formatter = ColorizedFormatter(self.DEFAULT_FORMAT, use_color=False)
        self.file_handler = logging.FileHandler(self.filename, encoding="utf8")
        self.file_handler.setFormatter(self.file_formatter)
        self.file_handler.setLevel(self.DEFAULT_LEVEL)

        self.logger = logging.getLogger("{}-{}".format(self.logger_id, self.filename))
        self.logger.setLevel(self.DEFAULT_LEVEL)
        self.logger.addHandler(self.syslog)
        self.logger.addHandler(self.file_handler)

    def info(self, msg, extra=None):
        self.logger.info(msg, extra=extra)

    def error(self, msg, extra=None):
        self.logger.error(msg, extra=extra)

    def debug(self, msg, extra=None):
        self.logger.debug(msg, extra=extra)

    def warn(self, msg, extra=None):
        self.logger.warn(msg, extra=extra)
