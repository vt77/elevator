

from serilizer.json import JSONSerilizable

class History(JSONSerilizable):

    def __init__(self,time,floor_from,floor_to,busy_till):
        self.time = time
        self.floor_from = floor_from
        self.floor_to = floor_to
        self.busy_till = busy_till


    def toJSON(self):
        return {
            "time" : self.time,
            "floor_from" : self.floor_from,
            "floor_to" : self.floor_to,
            "busy_till" : self.busy_till
        }
