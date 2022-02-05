from flask.json import JSONEncoder
from abc import ABC, abstractmethod

class JSONSerilizable(ABC):
    @abstractmethod
    def toJSON(self):
        pass

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, JSONSerilizable):
            return obj.toJSON()
        return super(CustomJSONEncoder, self).default(obj)


