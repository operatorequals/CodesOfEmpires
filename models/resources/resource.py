import pyglet

import util
from models.base import gameobject

ResourceTypes = [
    "Wood",
    "Food",
    "Iron"
]

class Resource(pyglet.sprite.Sprite, gameobject.GameObject ):

    def __init__(self, *args,
                food=0,
                wood=0,
                iron=0,
                food_gen=0.0, # N per DT
                wood_gen=0.0,
                iron_gen=0.0,
                destroy_empty=True,
                 **kwargs):
        super().__init__(*args, **kwargs)
        gameobject.GameObject.__init__(self, *args, **kwargs)

        self.__capacity = {
            "food" : food,
            "wood" : wood,
            "iron" : iron
        }
        self.__destroy_empty=destroy_empty
        
        self.__generate = {
            "food" : food_gen,
            "wood" : wood_gen,
            "iron" : iron_gen
        }


    def update(self, dt):
        if self.dead:
            return 

        if not sum(self.__capacity.values()) and self.__destroy_empty:
            self.visible = False
            self.dead = True
            return

        for r in self.__generate:
            self.__capacity[r] += self.__generate[r]


    @util.synchronized
    def _collect(self, value, type):
        if self.__capacity[type] == 0:
            return 0    
        if self.__capacity[type] >= value:
            self.__capacity[type] -= value
            return value
        else:
            ret = self.__capacity[type]
            self.__capacity[type] = 0
            return ret

