
from models import scriptedobject
from models import movableobject

class Unit(scriptedobject.ScriptedObject, movableobject.MovableObject):
    def __init__(self, *args, **kwargs):
        super(Unit, self).__init__(*args, **kwargs)

