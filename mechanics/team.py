import util

from models.units import create_unit
from models.resources.resource import ResourceTypes


UNIT_COSTS = {
    "worker" : {
        'food': 50
    }
}

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


    def __init__(self,  units={'worker':1},
                        batch=None,
                        # In case objects get updates from
                        # a central list
                 # This creates a race condition as the object_list
                 # is used bu update 
                        object_list=[],
                ):
        self.__capacity = {}
        for type_ in ResourceTypes:
            self.__capacity[type_.lower()] = 0
        self.knowledge_base = {}

        self.__members = set()
        self.batch = batch 
        self.object_list = object_list
        for k,v in units.items():
            for i in range(v):
                self.__create(k)


    def init_script(self, script):
        for unit in self.__members:
            unit.init_script(script)


    def __len__(self):
        return len(self.__members)

    def empty(self):
        return 0 == len(self.__members)


    @util.synchronized
    def _stockpile(self, value, type_):
#        print(f"Stockpiled {value} - {self.__capacity[type_.lower()]}")
        self.__capacity[type_.lower()] += value


    @util.synchronized
    def afford(self, unit_type):
        cost = UNIT_COSTS[unit_type]
        for k,v in cost.items():
            if self.__capacity[k] < v:
                return False
        return True


    @util.synchronized
    def __pay_unit(self,unit_type):
        cost = UNIT_COSTS[unit_type]
        for k,v in cost.items():
            self.__capacity[k] -= v
                     

    @util.synchronized
    def __create(self, type_):
       unit = create_unit(type_,
                         batch=self.batch,
                         team=self,
                         )
       self.__members.add(unit)
       self.object_list.append(unit)


    def member(self, obj):
        return obj in self.__members


    @util.synchronized
    def createWorker(self):
        if not self.afford('worker'):
            return False
        self.__pay_unit('worker')
        self.__create('worker')
        return True


    def update(self, td):
        for unit in self.__members:
            unit.update(td)


Gaia = Team()


