


class Predicate():
    """ 
    This class should predicate most usefull floor to send elevator in idle state
    The purpose to minimize wait time om next call. And just for fun
    Predication may be performed by external tools, based on statistics table

    For now it do nothing.
    """

    def get_floor(self,elevator):
        return elevator.floor



predict =  Predicate()