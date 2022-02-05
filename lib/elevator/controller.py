

from .elevator import Elevator
from .predicate import predict 

import functools
import logging
logger = logging.getLogger(__name__)

"""
Elevator state machine 
"""

#States description 
""" Elevator in Idle state """
IDLE = "idle"
""" Pass elevator to service """
GOFLOOR = "gofloor"
""" Elevator lights """
LIGHTON = "lighton"
LIGHTOFF = "lightoff"
OPENDOOR = "opendoor"
CLOSEDOOR = "closedoor"
WAIT = "wait"
""" Run elevator to predicated floor to minimize wait time """
GOTOPREDICT = "gotopredict"
COMPLETE = "complete"
WAITDONE="waitdone"

script = {
    (IDLE,GOFLOOR),
    (COMPLETE,LIGHTON),
    (LIGHTON,OPENDOOR),
    (OPENDOOR,WAIT),
    (WAITDONE,CLOSEDOOR),
    (CLOSEDOOR,LIGHTOFF),
    (LIGHTOFF,GOTOPREDICT),
}


from .timer import Timer as timer

class ElevatorScript():
    
    def __init__(self,elevator:Elevator):    
        
        self.actions = {
            IDLE  : elevator.idle,
            GOFLOOR : self.gofloor,
            LIGHTON : functools.partial(elevator.light,"on"),
            LIGHTOFF : functools.partial(elevator.light,"off"),
            OPENDOOR: functools.partial(elevator.door,"open"),
            CLOSEDOOR: functools.partial(elevator.door,"close"),
            WAIT: self.wait,
            GOTOPREDICT: self.predicate_idle_floor
        }
        self.state = IDLE
        self.elevator = elevator
        self.timer = None



    def predicate_idle_floor(self):
        """ 
            This strange function will use predicate procedures 
            to send elevator to most usefull floor to minimize next time witing
        """
        floor = predict.get_floor(self.elevator)
        self.elevator.goto(floor, lambda: self.finish() )

    def finish(self):
        self.setState(IDLE)
        self.elevator.idle()


    def wait(self):
        logger.info("[CONTROLLER]Setup timer for 5 seconds ")
        self.timer = timer(5,lambda : self.waitcomplete())        


    def waitcomplete(self):
        logger.info("[CONTROLLER]WAIT Done")
        self.setState(WAITDONE)
        self.timer = None        

    def gofloor(self):
        self.elevator.goto(self.target_floor, lambda: self.setState(COMPLETE) )

    def setState(self,state):
        logger.debug("[CONTROLLER]Got callback state %s " % state)
        self.state = state

    def enterState(self,state):
        logger.debug("[CONTROLLER]Enter state %s" % state )
        if not state in self.actions:
            raise Exception("State has no action %s" % state)
        self.state = state
        self.actions[state]()

    def process(self):
        if self.state == IDLE:
            return
        logger.debug("[CONTROLLER]Lookup next state for %s" % self.state ) 
        for s in script:
            if s[0] == self.state:
                return self.enterState(s[1])

    def on_timer(self):
        if self.timer is not None:
            self.timer.process()

    def run(self,floor:int):
        """ Starts statemachine controller  """
        if self.state != IDLE :
            raise Exception("Can't start . Elevator in use (%s)" % self.state)
        self.target_floor = floor
        self.enterState(GOFLOOR)
