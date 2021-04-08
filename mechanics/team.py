import threading
import queue

import util

from models.units import create_unit, delete_unit
from models.resources.resource import ResourceTypes

TEAMS = []


UNIT_COSTS = {
    "worker" : {
        'food': 50,
#        'time': 5    # seconds
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
                        # max population
                        population=30,
                        # code initialization
                        code=None,
                        definitions='',
                        constants='',
                ):
        self.to_add_members    = queue.Queue()
        self.to_remove_members = queue.Queue()

        self.__capacity = {}
        for type_ in ResourceTypes:
            self.__capacity[type_.lower()] = 0
        self.knowledge_base = {}

        self.members = set()
        self.batch = batch

        self.max_population = population
        # Check if initial units exceed population
        if population < sum(units.values()):
            raise IllegalArgumentException(
                "The initial 'units' of the team exceed the max population"
            )
        self.init_script(code, definitions, constants)
        # Create the default units
        for k,v in units.items():
            for i in range(v):
                self.__create(k)


    def init_script(self, code, definitions='', constants=''):
        self.code = code
        self.definitions = definitions
        self.constants = constants

        for unit in self.members:
            unit.init_script(code,
                             definitions = definitions,
                             constants   = constants,
                            )


    def __len__(self):
        return len(self.members)


    def empty(self):
        return 0 == len(self.members)


    @util.synchronized('resource')
    def _stockpile(self, value, type_):
        self.__capacity[type_.lower()] += value


    def afford(self, unit_type):
        cost = UNIT_COSTS[unit_type]
        for k,v in cost.items():
            if self.__capacity[k] < v:
                return False
        return True


    @util.synchronized('resource')
    def __pay_unit(self,unit_type):
        cost = UNIT_COSTS[unit_type]
        for k,v in cost.items():
            self.__capacity[k] -= v

                     
    def __init_unit(self, unit):
        unit.locals_['createWorker']=self.createWorker
        unit.locals_['WOOD'] = lambda : self.WOOD
        unit.locals_['FOOD'] = lambda : self.FOOD
        unit.locals_['IRON'] = lambda : self.IRON
        unit.locals_['POPULATION']=lambda : len(self)

 
    def __create(self, type_):
        unit = create_unit(type_,
                           batch=self.batch,
                           team=self,
                         )
        self.__init_unit(unit)
        self.to_add_members.put(unit) 
        unit.init_script(self.code,
                         self.definitions,
                         self.constants)


    def reached_population(self):
        if len(self) >= self.max_population:
            return True
        return False


    def member(self, obj):
        return obj in self.members


    def createWorker(self):
        if not self.afford('worker'):
            return False
        if self.reached_population():
            return False
        self.__pay_unit('worker')
        self.__create('worker')
        return True


    def update(self, dt):

        while not self.to_add_members.empty():
            unit = self.to_add_members.get()
            self.members.add(unit)

        while not self.to_remove_members.empty():
            unit = self.to_remove_members.get()
            assert unit in self.members
            self.members.remove(unit)
        '''
        for unit in self.members:
            unit.update(td)
            if unit.dead:
                delete_unit(unit)
        '''


    def delete_member(self, unit):
        self.to_remove_members.put(unit) 


    def delete(self):
        for obj in self.members:
            self.delete_member(obj)
            # If the object is dead, it is going to be
            # removed from the gameloop
            if obj.dead:
                continue
            delete_unit(obj)
        


def createTeam(*args, **kwargs):
    t = Team(*args, **kwargs)
    TEAMS.append(t)
    return t


