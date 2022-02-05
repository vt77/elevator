

def calculate_score(elevator,num_persons:int,cargo_weight:int,floor:int):
    """ 
    This function calculates score according to :
    1. Elevator speed 
    2. Current floor elevator located on
    3. Some other score properties may be applied 
    TODO: This is creative task. Many options can be appied here
    """

    """ Case when elevator on same floor """
    if elevator.floor == int(floor):
        return 100

    """ Otherwise calculate score according to number of floors to go """
    floors = max(elevator.floor,int(floor)) - min(elevator.floor,int(floor))
    score = int( 100 / floors ) * elevator.speed 
    return score
