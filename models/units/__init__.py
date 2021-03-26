from models.units.workerunit import WorkerUnit


def create_unit(type_, location=(0,0), team=None, batch=None):
    if 'worker' in type_:
        unit_class = WorkerUnit

    return unit_class(
        x=location[0],
        y=location[1],
        batch = batch,
        team=team
        )
 
