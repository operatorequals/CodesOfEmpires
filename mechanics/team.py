import util

from models.units import create_unit, delete_unit
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
                        # max population
                        population=30,
                ):
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
        # Create the default units
        for k,v in units.items():
            for i in range(v):
                self.__create(k)


    def init_script(self, script):
        for unit in self.members:
            unit.init_script(script)


    def __len__(self):
        return len(self.members)


    def empty(self):
        return 0 == len(self.members)


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

                     
    def __init_unit(self, unit):
        unit.locals_['createWorker']=self.createWorker
        unit.locals_['WOOD'] = lambda : self.WOOD
        unit.locals_['FOOD'] = lambda : self.FOOD
        unit.locals_['IRON'] = lambda : self.IRON
        unit.locals_['POPULATION']=lambda : len(self)

 
    @util.synchronized
    def __create(self, type_):
        unit = create_unit(type_,
                           batch=self.batch,
                           team=self,
                          )
        self.__init_unit(unit)
        self.members.add(unit)
 

    def reached_population(self):
        if len(self) >= self.max_population:
            return True
        return False


    def member(self, obj):
        return obj in self.members


    @util.synchronized
    def createWorker(self):
        if not self.afford('worker'):
            return False
        if self.reached_population():
            return False
        self.__pay_unit('worker')
        self.__create('worker')
        return True


    def update(self, td):

        for unit in self.members:
            unit.update(td)
            if unit.dead:
                delete_unit(unit)

    def delete(self):
        for obj in self.members:
            delete_unit(obj)
        self.members = set()
        

Gaia = Team()


