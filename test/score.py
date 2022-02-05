import os,sys
import unittest

from unittest.mock import patch
from unittest.mock import Mock
from unittest.mock import MagicMock

sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()

from elevator.score import calculate_score


class MockElevator():
    def __init__(self,floor,speed):
        self.floor = floor
        self.speed = speed

class TestScore(unittest.TestCase):

    def test_score(self):
        """ Test score according to elevator status"""
        fastElevator = MockElevator(0,2)
        slowElevator = MockElevator(0,1)
        """ Case when fast elevator wins """
        self.assertTrue(calculate_score(fastElevator,5,0,12) > calculate_score(slowElevator,5,0,12) )
        #TODO: More tests

if __name__ == '__main__':
    unittest.main()

