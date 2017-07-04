import logging


def config_logging(level_name, file_path):
    level_name = level_name.upper()
    level = getattr(logging, level_name, 'DEBUG')

    logger = logging.getLogger()
    log_file_path = str(file_path)

    if log_file_path:
        handler = logging.FileHandler(log_file_path, encoding='utf-8')
    else:
        handler = logging.StreamHandler()

    handler.setLevel(level)

    logger.setLevel(level=level)
    logger.addHandler(handler)
    return logger
