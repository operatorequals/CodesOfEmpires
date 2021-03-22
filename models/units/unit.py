
from models.base import scriptedobject
from models.base import movableobject

from mechanics.team import Team, Gaia

class Unit(scriptedobject.ScriptedObject, movableobject.MovableObject):
    def __init__(self, *args, team=Gaia, **kwargs):
        super(Unit, self).__init__(*args,
            locals_= {
                "move" : self.move,
                "stop" : self.stop,
                "arrived" : self.arrived,
                "stop_script" : self.stop_script,
            },
            **kwargs)

        self.team = team
        self.locals_['team'] = team # huge security issue 


