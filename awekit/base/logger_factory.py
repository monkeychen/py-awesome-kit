import sys
import logging

DEF_LOG_FMT = "%(asctime)s[%(levelname)s][%(lineno)d] %(name)s.%(funcName)s - %(message)s"
DEF_LOG_LEVEL = logging.INFO


def new_logger(logger_name: str, log_file_path: str = None, log_fmt=DEF_LOG_FMT, log_level=DEF_LOG_LEVEL,
               stdout_enable: bool = True) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(level=log_level)

    formatter = logging.Formatter(fmt=log_fmt)

    if log_file_path is not None:
        file_handler = logging.FileHandler(filename=log_file_path)
        file_handler.setLevel(level=log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if stdout_enable:
        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_handler.setLevel(level=log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


if __name__ == "__main__":
    log = new_logger("logger_factory_logger")
    log.info("This is a logger test message ...")
