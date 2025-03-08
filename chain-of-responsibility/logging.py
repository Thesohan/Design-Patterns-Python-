from abc import ABC, abstractmethod
from enum import Enum


class LogLevel(Enum):
    DEBUG = 5
    INFO = 4
    WARNING = 3
    EXCEPTION = 2
    ERROR = 1


class LogProcessor(ABC):
    
    def __init__(self,next_logger):
        self.next_logger = next_logger

    def log_message(self, level: LogLevel, message: str) -> None:
        if self.level.value >= level.value:  # Corrected comparison logic
            self.log(message=message)
        if self.next_logger:
            self.next_logger.log_message(level, message)  # Pass both level and message

    def set_next_logger(self, next_logger):
        self.next_logger = next_logger

    @abstractmethod
    def log(self, message: str):
        breakpoint()
        pass


class InfoLog(LogProcessor):

    def __init__(self,next_logger):
        self.level = LogLevel.INFO
        super().__init__(next_logger)

    def log(self, message: str):
        print(f"{LogLevel.INFO}: {message}")


class ErrorLog(LogProcessor):
    def __init__(self,next_logger):
        self.level = LogLevel.ERROR
        super().__init__(next_logger)

    def log(self, message: str):
        print(f"{LogLevel.ERROR}: {message}")


class ExceptionLog(LogProcessor):
    def __init__(self,next_logger):
        self.level = LogLevel.EXCEPTION
        super().__init__(next_logger)

    def log(self, message: str):
        print(f"{LogLevel.EXCEPTION}: {message}")


class WarningLog(LogProcessor):
    def __init__(self,next_logger):
        self.level = LogLevel.WARNING
        super().__init__(next_logger)

    def log(self, message: str):
        print(f"{LogLevel.WARNING}: {message}")


if __name__ == "__main__":
    # Creating loggers
    warning_logger = WarningLog(next_logger=None)
    exception_logger = ExceptionLog(next_logger=warning_logger)
    error_logger = ErrorLog(next_logger=exception_logger)
    logger = InfoLog(next_logger=error_logger)

    # info_logger.set_next_logger(error_logger)
    # error_logger.set_next_logger(exception_logger)
    # exception_logger.set_next_logger(warning_logger)


    # Testing log processing
    logger.log_message(LogLevel.INFO, "This is an info message")
    logger.log_message(LogLevel.ERROR, "This is an error message")
    logger.log_message(LogLevel.EXCEPTION, "This is an exception message")
    logger.log_message(LogLevel.WARNING, "This is a warning message")
