

import sqlite3 as sqlite
import time
import json

from elevator import Elevator
from elevator import features
from .history import History

import logging
logger = logging.getLogger(__name__)


def init_database(dsn):
    logger.info("[DATABASE][INIT]")
    con = sqlite.connect(dsn, isolation_level=None)
    cur = con.cursor()
    logger.debug("[DATABASE][INIT]Create table elevators")
    cur.execute(
        """
        CREATE TABLE elevators (
            id INTEGER PRIMARY KEY,
            speed INTEGER,
            property VARCHAR(255)
        )
        """        
    )

    logger.debug("[DATABASE][INIT]Insert elevators data")
    cur.executemany("INSERT INTO elevators VALUES (?,?,?)",
        [
            ( 1, 2,'{"num_persons":5,"cargo_weight":0,"floors":[0,10,11,12,13,14,17,16]}' ),
            ( 2, 1,'{"num_persons":10,"cargo_weight":150,"floors":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,17,16]}' ),
            ( 3, 1,'{"num_persons":0,"cargo_weight":550,"floors":[0,2,4,6,8,10,12,14,16]}' )
        ]
    )

    logger.debug("[DATABASE][INIT]Create table stats")
    cur.execute(
        """
        CREATE TABLE stats (
            id INTEGER,
            datetime,
            floor_from,
            floor_to,
            busy_till
        )
        """        
    )

    logger.debug("[DATABASE][INIT]Commit")
    con.commit()
    con.close()


class Backend():
    
    def __init__(self,dsn):
          self.con = sqlite.connect(dsn, isolation_level=None)
          self.con.row_factory = sqlite.Row

    def elevators(self):
          cur = self.con.cursor()
          cur.execute("select id,floor_to,MAX(busy_till) from stats group by id")
          stats = {}
          for row in cur.fetchall():
              stats[row[0]] = (row[1],row[2])

          cur.execute("select * from elevators")
          elevators = []
          for row in cur.fetchall():
              busy = stats[row['id']][1] if row['id'] in stats.keys() else 0
              floor = stats[row['id']][0] if row['id'] in stats.keys() else 0
              prop = features(**json.loads(row['property']))
              e = Elevator(row['id'],prop,row['speed'],floor)
              e.set_busy(busy)
              elevators.append(e)
          return elevators

    def save_action(self,elevator,floor_from,floor_to):
          logger.debug("[DATABASE][ACTION]Elevator %s going from %d to %d" % (elevator.name,floor_from,floor_to))  
          datetime = int(time.time())
          """ 
            10 seconds delay emulates elevator moving.
            But better it should be 
            ( max(floor_from,floor_to) - min(floor_from,floor_to) ) * elevator.speed
            where elevator.speed seconds per floor
          """
          busy_till = int(time.time()) + 10  

          cur = self.con.cursor()      
          cur.execute(
              "INSERT INTO stats VALUES(?,?,?,?,?)",
              (elevator.name,datetime,floor_from,floor_to,busy_till)
          )
          self.con.commit()

    def history(self,name):
        cur = self.con.cursor()
        cur.execute("select datetime as time,floor_from,floor_to,busy_till from stats where  id = ? order by busy_till desc limit 10",(name))
        ret = []
        for row in cur.fetchall():
            ret.append(History(**dict(row)))
        return ret

    