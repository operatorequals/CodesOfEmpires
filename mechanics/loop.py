from models.units import TO_ADD, TO_REMOVE, GAME_OBJECTS, delete_unit


def update(dt):

    while not TO_ADD.empty():
        obj = TO_ADD.get(block=False)
        GAME_OBJECTS.append(obj)
        TO_ADD.task_done()

    while not TO_REMOVE.empty():
        obj = TO_REMOVE.get(block=False)
        GAME_OBJECTS.remove(obj)
        TO_REMOVE.task_done()


    for i in range(len(GAME_OBJECTS)):
        obj = GAME_OBJECTS[i]
        obj.update(dt)
        # If object is dead
        # make it to_delete and skip
        # its exploration
        if obj.dead:
            delete_unit(obj)
#            TO_REMOVE.put(obj, block=False)
            continue
        
        for j in range(i+1, len(GAME_OBJECTS)):
            obj2 = GAME_OBJECTS[j]
            if 'Unit' in str(obj):
                obj.in_visible_range(obj2)
            if 'Unit' in str(obj2):
                obj2.in_visible_range(obj)


