import gps
import threading


class GpsPoller(threading.Thread):
    def __init__(self, host="localhost"):
        super(GpsPoller, self).__init__()
        self._gpsd = gps.gps(mode=gps.WATCH_ENABLE, host=host)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        while not self.stopped():
            self._gpsd.next()

    def value(self):
        return self._gpsd
