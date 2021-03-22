import pyglet

from enum import Enum

class Type(Enum):
    WOOD='wood'
    FOOD='food'
    IRON='iron'

class Resource(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                food=0,
                wood=0,
                iron=0,
                food_gen=0.0, # N per DT
                wood_gen=0.0,
                iron_gen=0.0,
                destroy_empty=True
                **kwargs)

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
        if not sum(self.__capacity.values()) and self.__destroy_empty:
            self.delete()
            return

        for r in self.__generate:
            self.__capacity[r] += self.__generate[r]

    def _collect(self, value, type):
        if self.__capacity[type] >= value:
            self.__capacity[type] -= value
        else:
            self.__capacity[type] = 0

        return value