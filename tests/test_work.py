from time import sleep
from random import randint

from models.units import workerunit
from models.resources import resource, wood, food, iron
from mechanics import team

import tests
from tests import GAME_OBJECTS, APP, BATCH, WINDOW, refresh
import util

point0 = (0,0)
point1 = WINDOW.get_size()
v = 250
x = util.distance(point0,point1)
max_t = x/v


class Work(tests.GameTest):

    def setUp(self):
        global GAME_OBJECTS
        # Initializing in 50px area to be all in 'explored'
        self.unit = workerunit.WorkerUnit(
            x=250, y=250,
            batch = BATCH,
            team = team.Team()
        )
        self.wood = wood.Wood(wood=50, batch=BATCH, x= 200, y=300)
        self.iron = iron.Iron(iron=50, batch=BATCH, x= 300, y=200)
        self.food = food.Food(food=50, batch=BATCH, x= 300, y=300)
        GAME_OBJECTS.extend( [
            self.unit,
            self.wood,
            self.iron,
            self.food
        ])
        super().setUp()


    def test_timber(self):
        ai = '''
sleep(0.2)
for e in explored:
    if e.isWood:
        timber(e)
        while team.WOOD < 20:
            sleep(0.1)
stop_script()
        '''
        self.unit.init_script(ai)
        sleep(2.5)
        self.assertTrue(
            25 >= self.unit.team.WOOD >= 20 
        )

    def test_extract(self):
        ai = '''
sleep(0.2)
for e in explored:
    if e.isIron:
        extract(e)
        while team.IRON < 20:
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
        while team.FOOD < 20:
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
        extract(e)
        while team.IRON < 12:
            sleep(0.1)
        break
eta=move(400,400)
sleep(eta)
stop_script()
        '''
        self.unit.init_script(ai)
        sleep(4)
        self.assertTrue(
            20 >= self.unit.team.IRON >= 12
        )


    def test_stop_work(self):
        ai = '''
sleep(0.2)
for e in explored:
    if e.isFood:
        collect(e)
        sleep(1)
    move(400,400)
stop_script()
        '''
        self.unit.init_script(ai)
        sleep(2.5)
        self.assertTrue(
            25 >= self.unit.team.FOOD >= 20 
        )


    def test_deplete(self):
        self.unit.x = 500
        self.unit.y = 200
        self.food2 = food.Food(food=20, batch=BATCH, x= 500, y=300)
        GAME_OBJECTS.append(self.food2)
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
        self.food3 = food.Food(food=50, batch=BATCH, x= 200, y=500)
        GAME_OBJECTS.append(self.food3)
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

