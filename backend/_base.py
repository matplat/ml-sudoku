import sys
import logging


class SudokuBase:
    """ Base object for the project, handling logging and most common operations.

    Attributes:
        logger (logging.Logger): Logger instance
        logger_name (str): logger name
        logging_level (int): logging level
    """

    LOGGING_FORMAT = "[%(asctime)s.%(msecs)03d][%(levelname)s][%(name)s]\t %(message)s"
    LOGGING_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

    def __init__(self, logger_name: str = "SudokuBase", logging_level: int = logging.DEBUG):
        """ Initialize with given logger name and level

        Args:
            logger_name (str): name of the logger
            logging_level (int): logging level
        """
        self.logger = None
        self.logger_name = logger_name
        self.logging_level = logging_level

        self.logger = self.get_logger()

    def get_logger(self) -> logging.Logger:
        """ Return Logger for logging messages

        Returns:
             (logging.Logger): Logger object, with given formatter, date format and handlers
        """
        if self.logger:
            self.logger.setLevel(self.logging_level)
            return self.logger
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.logging_level)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt=SudokuBase.LOGGING_FORMAT, datefmt=SudokuBase.LOGGING_TIME_FORMAT))
        logger.addHandler(handler)
        return logger

    def log(self, message: str, level: int = logging.DEBUG):
        """ Log message with given level

        Args:
            message (str): message
            level (int): logging level
        """
        self.get_logger().log(level, message)

    def log_debug(self, message):
        """ Log debug message

        Args:
            message (str): message
        """
        self.log(message, logging.DEBUG)

    def log_info(self, message):
        """ Log info message

        Args:
            message (str): message
        """
        self.log(message, logging.INFO)

    def log_warning(self, message):
        """ Log warning message

        Args:
            message (str): message
        """
        self.log(message, logging.WARNING)

    def log_error(self, message):
        """ Log error message

        Args:
            message (str): message
        """
        self.log(message, logging.ERROR)

    def log_critical(self, message):
        """ Log critical message

        Args:
            message (str): message
        """
        self.log(message, logging.CRITICAL)
