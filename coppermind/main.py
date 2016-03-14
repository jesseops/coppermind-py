import os
import sys
import logging
from time import sleep
from coppermind.tools import SVC, SVCObj, Config


class Coppermind():
    """
    Main daemon thread
    Starts WS and Catalog workers
    Handles shutdown procedures
    Sets main logger instance
    """
    def __init__(self):
        self.svc = SVC()
        SVCObj.svc = self.svc  # Allows any object to access SVC
        self.svc.shutdown = False

    def run(self):
        self.setup_config()
        self.setup_logging()
        while not self.svc.shutdown:
            sleep(1)


    def setup_config(self):
        filename = "coppermind.conf"
        paths = ['/etc', '.', '..', '../..']
        for p in paths:
            if os.path.exists(os.path.join(p, filename)):
                self.svc.config = Config(os.path.join(p, filename))
                self.svc.config.refresh()
                break
        else:
            raise Exception("Failed to get config!")

    def setup_logging(self):
        log = logging.getLogger(__name__)
        log.setLevel(getattr(logging, self.svc.config.logging.level.upper()))

        file_handler = logging.FileHandler(self.svc.config.logging.filename)
        stream_handler = logging.StreamHandler()

        log.addHandler(file_handler)
        log.addHandler(stream_handler)
        logging.root = log
        logging.debug("Logging Setup Complete")
