from queue import Queue

from models.base import movableobject
from models.base import scriptedobject

from models.base import gameobject


import util


class Unit(scriptedobject.ScriptedObject, movableobject.MovableObject, gameobject.GameObject):
    def __init__(self, *args, team=None, max_hp=100, **kwargs):
        super(Unit, self).__init__(*args,
            locals_= {
                "move" : self.move,
                "stop" : self.stop,
                "arrived" : self.arrived,
                "stop_script" : self.stop_script,
            },
            **kwargs)
        gameobject.GameObject.__init__(self, *args, **kwargs)
        self._hp     = max_hp
        self._max_hp = max_hp
        self.damage = Queue()

        self.team = team
        self.visibility_radius = 180
        self.explored_objects = []

        self.locals_['last_explored'] = self.last_explored
        self.locals_['explored'] = self.explored_objects
        self.locals_['HP'] = lambda : self.hp
        self.locals_['HP_PERCENT'] = lambda : self.hp_percent
 

    @property
    def hp(self):
        return self._hp

    @property
    def hp_percent(self):
        return int((self._hp / self._max_hp) * 100)


    def apply_damage(self, damage_pts):
        if damage_pts <= 0:
            raise IllegalArgumentException("Damage Points less than 0")
        self.damage.put(damage_pts)


    def in_visible_range(self, game_object):
        if game_object.dead:
            return False
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


    def update(self, td):
        super().update(td)
        while not self.damage.empty():
            pts = self.damage.get()
            self._hp -= pts
            self.damage.task_done()
            if self.hp <= 0:
                self.dead = True

        to_remove = []
        for gm in self.explored_objects:
            if gm.dead:
                to_remove.append(gm)

        for gm in to_remove:
            self.explored_objects.remove(gm)

