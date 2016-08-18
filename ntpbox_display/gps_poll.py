import gps
import threading
import time
import logging

logger = logging.getLogger(__name__)


class GpsPoller(threading.Thread):
    def __init__(self, host="localhost"):
        super(GpsPoller, self).__init__()
        self._stop = threading.Event()
        self._host = host
        self._gpsd = None

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        try:
            self._gpsd = gps.gps(mode=gps.WATCH_ENABLE, host=self._host)
            self._gpsd.stream()
            while not self.stopped():
                self._gpsd.read()
                time.sleep(0.5)
        except:
            logger.exception("Error in GPS update")

    def value(self):
        return self._gpsd
