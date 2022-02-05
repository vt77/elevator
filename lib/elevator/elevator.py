
import logging
logger = logging.getLogger(__name__)

from .features import Features

import time
import json

from serilizer.json import JSONSerilizable
from .score import calculate_score
from .timer import Timer as timer

from events import fireStatusChange


class Elevator(JSONSerilizable):

    def __init__(self,name:str,features:Features,speed=1,floor=0):
        self.name = name
        self.features = features
        self.busy = 0
        self.floor = floor
        self.speed = speed
        self.timer = None

    def on_timer(self):
        if self.timer is None:
            return
        if self.timer.process():
            self.timer = None

    def set_busy(self,until):
        self.busy = until

    def idle(self):
        self.set_busy(0)
        logger.info("[ELEVATOR][%s] Idle" % self.name )

    def complete(self,floor,callback):
        self.floor = floor
        callback()

    def goto(self,floor,callback):
        if floor == self.floor:
            return callback()
        logger.info("[ELEVATOR][%s][GOTO]%s " % (self.name,floor))
        delay = int(floor * 3 / self.speed)
        """ Just a dummy value in the future"""
        self.set_busy(int(time.time()) + 200 )
        fireStatusChange(self.name,{
            "time": int(time.time()),
            "floor_from":self.floor,
            "floor_to":floor,
            "busy_till": int(time.time()) + delay
        })
        logger.info("[ELEVATOR][%s][TRIPTIME]%s " % (self.name,delay))
        self.timer = timer( delay,lambda : self.complete(floor,callback) )
    
    def light(self,state):
        logger.info("[ELEVATOR][%s][LIGHT]%s " % (self.name,state))

    def door(self,state):
        logger.info("[ELEVATOR][%s][DOOR]%s " % (self.name,state))

    def inuse(self):
        return self.busy > int(time.time())

    def match(self,*args,**kwargs):
        """ Returns score of elevator """
        if not self.features.match(**kwargs):
            logger.debug("[ELEVATOR][%s] not match" % self.name )
            return 0
        if self.inuse() :
            logger.debug("[ELEVATOR][%s] match but in use" % self.name )
            return 0

        score = calculate_score(self,**kwargs)
        logger.info("[ELEVATOR][%s] got score %d" % (self.name,score) )
        return score

    def toJSON(self):
        return {
            "name":self.name,
            "inuse" : self.inuse(),
            "speed" : self.speed,
            "floor" : self.floor
            #"features" : self.features
        }
