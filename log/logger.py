import logging

def create_logger():
    logger = logging.getLogger('p1_logger')

    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler('log/p1.log')
    file_handler.setLevel(logging.DEBUG)

    form = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(form)

    logger.addHandler(file_handler)

    logger.info("Logger successfully created.")
    return logger
