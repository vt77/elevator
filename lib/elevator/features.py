
from serilizer.json import JSONSerilizable


class Features(JSONSerilizable):
    def __init__(self,num_persons,cargo_weight,floors):
        self.num_persons = int(num_persons)
        self.cargo_weight = int(cargo_weight)
        self.floors = floors

    def match(self,num_persons,cargo_weight,floor):
        if int(num_persons) > self.num_persons:
            return False
        if int(cargo_weight) > self.cargo_weight:
            return False
        if int(floor) not in  self.floors:
            return False
        return True

    def toJSON(self):
        return {
            "num_persons":self.num_persons,
            "cargo_weight" : self.cargo_weight,
            "floors" : self.floors
        }


    def __repr__(self):
        return ("Features Set : num_persons %d , cargo_weight %d, floors %s" % 
            (self.num_persons,self.cargo_weight,self.floors))