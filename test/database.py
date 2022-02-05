import os,sys
import unittest

from unittest.mock import patch
from unittest.mock import Mock
from unittest.mock import MagicMock

sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()

from storage.sqlite import Backend


class MockElevator(object):
    def __init__(self,name):
        self.name = name


class TestSQLite(unittest.TestCase):
    
    def test_Elevators(self):
        backend = Backend('./app.db')
        elevator = MockElevator(1)
        backend.save_action(elevator,0,11)
        elevators = {str(elevator.name) : elevator for elevator in backend.elevators()}
        self.assertTrue(elevators["1"].inuse())
        self.assertFalse(elevators["2"].inuse())
        self.assertFalse(elevators["3"].inuse())
        self.assertEqual(elevators["1"].match(**{"num_persons":5,"cargo_weight":0,"floor":11}),0)
        self.assertEqual(elevators["2"].match(**{"num_persons":7,"cargo_weight":100,"floor":5}),33)
        self.assertFalse(elevators["3"].match(**{"num_persons":7,"cargo_weight":100,"floor":5}),0)
        #TODO: More tests

    def test_history(self):
        backend = Backend('./app.db')
        h = backend.history("1")
        self.assertEqual(type(h[0]).__name__,"History")


if __name__ == '__main__':
    unittest.main()