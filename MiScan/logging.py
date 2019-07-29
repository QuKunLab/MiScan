import logging

logger = logging.getLogger('MiScan')
logger.propagate = False
logger.setLevel('INFO')
logger.addHandler(logging.StreamHandler())
logger.handlers[-1].setFormatter(logging.Formatter('==>%(message)s'))
logger.handlers[-1].setLevel('INFO')


def get_logger(name):
    """
    generate child logger

    :param name: the name of logger
    :return: child_logger
    """
    child_logger = logger.manager.getLogger(name)
    return child_logger
