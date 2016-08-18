import threading
import time
import logging
import subprocess

logger = logging.getLogger(__name__)


class NTPPoller(threading.Thread):

    def __init__(self, host="localhost"):
        super(NTPPoller, self).__init__()
        self._stop = threading.Event()
        self.jitter = None
        self.ntp_status = '?'
        self.host = host

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        while not self.stopped():
            try:
                out = subprocess.check_output(['ntpq', '-c', 'rv', self.host])
                params = [x for x in out.decode('utf-8').replace('\n', ' ').split(', ')]
                self.jitter = float([x for x in params if x.startswith('sys_jitter')][0].split('=')[1]) / 1000.0
            except Exception as e:
                logger.exception('Failed to get ntp system status')
                self.jitter = None

            try:
                out = subprocess.check_output(['ntpq', '-p', self.host])
                ntp_status = [x[0] for x in out.decode('utf-8').split('\n')[2:-1]]
                prio = [' ', 'x', '-', '+', '*', 'o']
                max_p = 0
                for s in ntp_status:
                    if prio.index(s) > max_p:
                        max_p = prio.index(s)
                self.ntp_status = prio[max_p]
            except Exception as e:
                logger.exception('Failed to get ntp peer status')
                self.ntp_status = '?'

            time.sleep(1)
