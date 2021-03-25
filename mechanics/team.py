import util

from models.resources.resource import ResourceTypes

class Team:

    # TODO: make this dynamically for the
    # case mpre resources get added
    @property
    def WOOD(self):
        return self.__capacity['wood']

    @property
    def FOOD(self):
        return self.__capacity['food']

    @property
    def IRON(self):
        return self.__capacity['iron']


    def __init__(self):
        self.__capacity = {}
        for type_ in ResourceTypes:
            self.__capacity[type_.lower()] = 0


    @util.synchronized
    def _stockpile(self, value, type_):
#        print(f"Stockpiled {value} - {self.__capacity[type_.lower()]}")
        self.__capacity[type_.lower()] += value


Gaia = Team()

#for type_ in ResourceTypes:
#    setattr(Team, type_.upper(),
#property( lambda self : self.___capacity.get(type_.lower()) )
#        property( lambda self : print(f"Asked for {type_}") )
#    )


