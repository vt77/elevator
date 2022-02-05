import os,sys
import unittest

from unittest.mock import patch
from unittest.mock import Mock
from unittest.mock import MagicMock

sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()

from events import fireStatusChange, statuschange

status = {}

@statuschange
def status_change_handler(name,event):
    global status
    logger.debug("[TEST]Got status change %s => %s " % (name,event))
    status['name'] = name
    status['event'] = event

class TestController(unittest.TestCase):

    def test_eventcall(self):
        fireStatusChange("test",{"floor_from":1,"floor_to":10,"busy_till":123445})
        self.assertEqual(status['name'],"test")


if __name__ == '__main__':
    unittest.main()
