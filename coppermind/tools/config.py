import yaml
from threading import Lock
from configure import Configuration
from datetime import datetime, timedelta


class Config():
    """
    Configuration wrapper
    Handles reading & updating config
    """
    def __init__(self, config_file):
        self.config_file = config_file
        self.ts_updated = None
        self._lock = Lock()

    def refresh(self):
        with self._lock:
            #with open(self.config_file, 'r') as cfg:
                #self._config = yaml.load(cfg)
            self._config = Configuration.from_file(self.config_file).configure()
            self.ts_updated = datetime.utcnow()

    def __getattr__(self, attr):
        if attr not in dir(self):
            with self._lock:
                return getattr(self._config, attr)
