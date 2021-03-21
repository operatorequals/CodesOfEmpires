
from models import scriptedobject
from models import movableobject

class Unit(scriptedobject.ScriptedObject, movableobject.MovableObject):
    def __init__(self, *args, **kwargs):
        super(Unit, self).__init__(*args,
            locals_= {
                "move" : self.move,
                "stop" : self.stop,
                "arrived" : self.arrived,
                "stop_script" : self.stop_script
            },
            **kwargs)

 


