from queue import Queue

from models.units.workerunit import WorkerUnit

GAME_OBJECTS = []
TO_ADD = Queue()
TO_REMOVE = Queue()

def create_unit(type_, location=(0,0), team=None, batch=None):
    if 'worker' in type_:
        unit_class = WorkerUnit

    unit = unit_class(
        x=location[0],
        y=location[1],
        batch = batch,
        team=team
        )
 
    TO_ADD.put(unit) 
    return unit


def delete_unit(unit):
    TO_REMOVE.put(unit)
    unit.delete()

