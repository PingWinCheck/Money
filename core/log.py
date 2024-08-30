import logging


def get_logger(level=logging.INFO):
    logging.basicConfig(level=level,
                        format='[%(levelname)-8s] - [%(asctime)s] - [%(module)s:%(lineno)-3s] - %(message)s',
                        # filename='core/logging.log',
                        # filemode='a',
                        encoding='utf-8'
                        )
    logger = logging.getLogger(__name__)
    return logger
