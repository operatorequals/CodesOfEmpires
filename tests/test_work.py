from time import sleep
from random import randint

from models.units import workerunit
from models.resources import resource, wood, food, iron
from mechanics.team import createTeam

import tests
from models.units import TO_ADD, TO_REMOVE
from mechanics.game import BATCH, WINDOW
import util

point0 = (0,0)
point1 = WINDOW.get_size()
v = 250
x = util.distance(point0,point1)
max_t = x/v


class Work(tests.GameTest):

    def setUp(self):
        super().setUp()
        self.team = createTeam(units={'worker':1}, batch=BATCH)
        # Hack to retrive the first element of a set:
        # https://stackoverflow.com/a/59841
        while not self.team.members: continue
        self.unit = list(self.team.members)[0]
        self.unit.x = 200
        self.unit.y = 200

        # Initializing in 50px area around unit to be all in 'explored'
        self.wood = wood.Wood(wood=50, batch=BATCH, x= 200, y=300)
        self.iron = iron.Iron(iron=50, batch=BATCH, x= 300, y=200)
        self.food = food.Food(food=50, batch=BATCH, x= 300, y=300)
        TO_ADD.put(self.wood, block=False)
        TO_ADD.put(self.iron, block=False)
        TO_ADD.put(self.food, block=False)
        

    def tearDown(self):
        super().tearDown()
        self.team.delete()
        TO_REMOVE.put(self.wood, block=True)
        TO_REMOVE.put(self.iron, block=True)
        TO_REMOVE.put(self.food, block=True)


    def test_timber(self):
        ai = '''
sleep(0.2)
for e in explored:
    if e.isWood:
        timber(e)
        while WOOD() < 20:
            sleep(0.1)
stop_script()
        '''
        self.unit.init_script(ai)
        self.unit.script.join()
       # sleep(2.5)
        self.assertTrue(
            25 >= self.unit.team.WOOD >= 20 
        )

    def test_extract(self):
        ai = '''
sleep(0.2)
for e in explored:
    if e.isIron:
        extract(e)
        while IRON() < 20:
            sleep(0.1)
stop_script()
        '''
        self.unit.init_script(ai)
        sleep(2.5)
        self.assertTrue(
            25 >= self.unit.team.IRON >= 20 
        )

    def test_collect(self):
        ai = '''
sleep(0.2)
for e in explored:
    if e.isFood:
        collect(e)
        while FOOD() < 20:
            sleep(0.1)
stop_script()
        '''
        self.unit.init_script(ai)
        sleep(2.5)
        self.assertTrue(
            25 >= self.unit.team.FOOD >= 20 
        )


    def test_work_while_move(self):
        self.unit.x=0
        self.unit.y=0
        ai = '''
sleep(0.2)
eta=move(400,400)
while not explored:
    sleep(0.2)

for e in explored:
    if e.isIron:
        stop()
        extract(e)
        while IRON() < 12:
            sleep(0.5)
        eta=move(400,400)
        sleep(eta)
        stop_script()
        '''
        self.unit.init_script(ai)
        sleep(5)
        self.assertTrue(
            20 >= self.team.IRON >= 12
        )


    def test_stop_work(self):
        ai = '''
sleep(0.2)
for e in explored:
    if e.isFood:
        collect(e)
        sleep(2.5)
        eta=move(400,400)
        sleep(eta)
    sleep(0.1)
stop_script()
        '''
        self.unit.init_script(ai)
        self.unit.script.join()#       sleep(2.5)
        self.assertTrue(
            25 >= self.team.FOOD >= 20 
        )


    def test_deplete(self):
        self.unit.x = 500
        self.unit.y = 200
        food2 = food.Food(food=20, batch=BATCH, x= 500, y=300)
        TO_ADD.put(food2, block=True)
        ai = '''
sleep(0.2)
for e in explored:
    if e.isFood:
        collect(e)
        while not finished():
            sleep(0.2)
        break
eta=move(500,500)
sleep(eta)
stop_script()
        '''
        self.assertTrue(
            0 == self.unit.team.FOOD
        )
        self.unit.init_script(ai)
        sleep(5.5)
        self.assertTrue(
            20 >= self.unit.team.FOOD
        )
        self.assertTrue(
            self.unit.arrived((500,500))
        )


    def test_work_rate(self):
        wr = self.unit.work_rate
        clock = 120 # 120 updates per second
        target_resource = 40

        self.unit.x = 250
        self.unit.y = 550
        food3 = food.Food(food=50, batch=BATCH, x= 200, y=500)
        TO_ADD.put(food3, block=True)
        # time - resources
        # 1    - wr
        # X    - target_resourse 
        target_time = target_resource*wr
        ai = f'''
sleep(0.2)
for e in explored:
    if e.isFood:
        collect(e)
        sleep({target_time})
stop_script()
        '''
        self.unit.init_script(ai)
        sleep(target_time+0.5)

        self.assertTrue(50 > self.unit.team.FOOD >= 40)

