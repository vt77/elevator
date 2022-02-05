import os,sys
import unittest

from unittest.mock import patch
from unittest.mock import Mock
from unittest.mock import MagicMock

sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()

from elevator import features

class TestFeatures(unittest.TestCase):


    def test_match(self):
        f1d = {"num_persons":5,"cargo_weight":0,"floors":[0,10,11,12,13,14,17,16]}
        f1 = features(**f1d)
        logger.debug("Checking features %s" % f1)
        logger.debug("Check cargo_weight high")
        self.assertFalse(f1.match(1,100,10))
        logger.debug("Check floor not in list")
        self.assertFalse(f1.match(2,0,5))
        logger.debug("Check good match")
        self.assertTrue(f1.match(2,0,11))

        #TODO: Make more tests


if __name__ == '__main__':
    unittest.main()

