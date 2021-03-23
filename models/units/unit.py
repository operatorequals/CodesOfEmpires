
from models.base import movableobject
from models.base import scriptedobject

from models.base import gameobject

from mechanics.team import Team, Gaia

import util


class Unit(scriptedobject.ScriptedObject, movableobject.MovableObject, gameobject.GameObject):
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
        self.visibility_radius = 100
        self.explored_objects = []
        gameobject.GameObject.__init__(self, *args, **kwargs)

        self.locals_['team'] = team # huge security issue 
        self.locals_['last_explored'] = self.last_explored
        self.locals_['explored'] = self.explored_objects
 

#    def update(self, dt):
#        pass

    def in_visible_range(self, game_object):
        d = util.distance(
            (self.x, self.y),
            (game_object.x, game_object.y)
        )
        if d <= self.visibility_radius:
            if game_object not in self.explored_objects:
                self.explored_objects.append(game_object)
            return True
        return False


    def last_explored(self):
        if not self.explored_objects:
            return None
        return self.explored_objects[-1]

