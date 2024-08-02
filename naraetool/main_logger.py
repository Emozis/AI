import logging

class MainLogger:
    def __init__(self):
        self.formatter = logging.Formatter('[%(levelname)s] %(message)s')
        self.logger = self._get_logger()

    def _set_handler(self):
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(self.formatter)

        return handler 
    
    def _get_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self._set_handler())
    
        return logger
    
    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message, exc_info=False)

logger = MainLogger()