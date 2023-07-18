import os
import glob
import logging
import threading
from time import sleep
from ...common.tools import SVCObj
from ...common.models import Ebook
from ...common.db.base import EbookNotFound

logger = logging.getLogger()

class WatchDirectory(threading.Thread, SVCObj):
    """
    Watch a directory for ebooks
    """
    def __init__(self):
        super().__init__()
        self.name = f"{self.__class__.__name__}"
        self.daemon = True

    def run(self):
        logging.debug(f"Starting up")
        folder = self.svc.config.get('watch_directory', '.')
        logging.debug(f"Watching directory {folder}")
        while not self.svc.shutdown:
            try:
                sleep(1)
                for discovered_file in self._scan(folder):
                    ebook = Ebook.from_file(discovered_file)
                    try:
                        self.svc.db.get_ebook(ebook.serialize()['sha256sum'])
                    except EbookNotFound:
                        logging.debug(f"Saving {ebook}")
                        ebook.save(self.svc.db)
            except Exception as e:
                logging.warning(f"Unknown failure scanning {folder}: {e}", exc_info=1)
                sleep(1)
    
    def _scan(self, watch_directory, suffixes=None):
        _suffixes = suffixes or ['.epub']
        for s in _suffixes:
            logging.debug(f"Scanning for files ending in {s} in {watch_directory}")
            for f in glob.glob(f"*{s}", root_dir=watch_directory, recursive=True):
                logging.debug(f"Found file {f} in {watch_directory}")
                yield os.path.join(watch_directory, f)
