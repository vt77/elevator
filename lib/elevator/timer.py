

import time

import logging
logger = logging.getLogger(__name__)

class Timer():

    def __init__(self,period,callback):
        self.time = int(time.time()) + period
        logger.info("[Timer]Start for period %d sec (%s)" % (period,self.time))
        self.callback = callback

    def process(self):
        if self.time < int(time.time()):
            return self.finish()
        return False

    def finish(self):
        self.callback()
        return True