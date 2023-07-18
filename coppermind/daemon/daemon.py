import os
import sys
import yact
import logging
from time import sleep
from ..common.tools import SVC, SVCObj
from ..common.db.filesystem import FileSystem
from .threads.watch_directory import WatchDirectory


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
        self.setup_db()
        self._dir_watcher = WatchDirectory()
        self._dir_watcher.start()
        while not self.svc.shutdown:
            sleep(1)
        self._dir_watcher.join(1)

    def setup_db(self):
        self.svc.db = FileSystem()

    def setup_config(self):
        filename = "coppermind.conf"
        config = yact.from_file(filename)
        self.svc.config = config

    def setup_logging(self):
        log = logging.getLogger(__name__)
        log.setLevel(getattr(logging, self.svc.config.get('logging.level').upper()))
        logformat = logging.Formatter(fmt='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logformat)
        log.addHandler(stream_handler)
        try:
            file_handler = logging.FileHandler(self.svc.config['logging.filename'])
            file_handler.setFormatter(logformat)
            log.addHandler(file_handler)
        except KeyError:
            log.info("No logfile configured, skipping persistent log output")
        logging.root.handlers.clear()
        logging.root = log
        log.addHandler(stream_handler)
        log.debug("Logging Setup Complete")
