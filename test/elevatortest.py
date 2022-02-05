import os,sys
import unittest
import time

from unittest.mock import patch
from unittest.mock import Mock
from unittest.mock import MagicMock

sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()

from elevator import Elevator,features

from config import elevator1,elevator2,elevator3

elevators = [
    Elevator("fast",features(**elevator1),2,0),
    Elevator("slow",features(**elevator2),1,0),
    Elevator("cargo",features(**elevator3),1,0),
]

class TestController(unittest.TestCase):

    def test_fast_elevator(self):
        elevator = elevators[0]
        elevator.idle()
        elevator.light("on")
        elevator.light("off")
        elevator.door("open")
        elevator.door("close")
        m = { "num_persons": "4", "cargo_weight": "0", "floor": "11"} 
        self.assertNotEqual(elevator.match(**m),0)
        elevator.set_busy(int(time.time())+20)
        self.assertTrue(elevator.inuse())
        elevator.idle()
        self.assertFalse(elevator.inuse())
        #TODO: Make mor tests :
        # 1 - If same floor called, just stop
        # 2 - Got from floor to floor
        # 3 - Calculate time according to speed and floor



if __name__ == '__main__':
    unittest.main()
