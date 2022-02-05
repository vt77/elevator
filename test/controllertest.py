import os,sys
import unittest

from unittest.mock import patch
from unittest.mock import Mock
from unittest.mock import MagicMock

sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()

from elevator.controller import ElevatorScript


class MockElevator():
    def __init__(self,floor,speed):
        self.floor = floor
        self.speed = speed

    def idle(self):
        logger.debug("[ELIVATOR]Idle")

    def goto(self,floor,callback):
        self.floor = floor
        logger.debug("[ELIVATOR]Goto %s" % floor )
        callback()
    
    def light(self,action):
        logger.debug("[ELEVATOR]Light %s" % action )

    def door(self,action):
        logger.debug("[ELEVATOR]Door %s" % action )

class TestController(unittest.TestCase):

    def test_script(self):
        elevator = MockElevator(0,2)
        controller = ElevatorScript(elevator)
        """ Send elevator to 8 floor """
        controller.run(8)
        self.assertEqual(controller.state,"complete")
        controller.process()
        self.assertEqual(controller.state,"lighton")
        controller.process()
        self.assertEqual(controller.state,"opendoor")
        controller.process()
        controller.timer.finish()
        controller.process()
        self.assertEqual(controller.state,"closedoor")
        controller.process()
        self.assertEqual(controller.state,"lightoff")
        controller.process()
        self.assertEqual(controller.state,"idle")


if __name__ == '__main__':
    unittest.main()
