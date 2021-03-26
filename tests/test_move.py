from time import sleep
from random import randint

from models.units import unit
from resources import load

import tests
from tests import GAME_OBJECTS, APP, BATCH, WINDOW, refresh
import util

point0 = (0,0)
point1 = WINDOW.get_size()
v = 250
x = util.distance(point0,point1)
max_t = x/v


class Movement(tests.GameTest):

    def setUp(self):

        self.unit = unit.Unit(
            img=load.worker,
            x=250, y=0,
            batch = BATCH
        )
        super().setUp()
        GAME_OBJECTS.append(self.unit)

    def test_move(self):
        point = (500,500)
        ai = f"move({point[0]},{point[1]}); sleep(3)"
        self.unit.init_script(ai)
        sleep(4)
        self.assertTrue(
            self.unit.arrived()
        )


    def test_move_random(self):
        point = (randint(0,800),randint(0,600))
        ai = f"move({point[0]},{point[1]}); sleep(2)"
        self.unit.init_script(ai)
        sleep(4)
        self.assertTrue(
            self.unit.arrived()
        )


    def test_velocity(self):
        v = self.unit.max_velocity 
        x = util.distance(point0,point1)
        self.unit.x, self.unit.y = point0
        ai = f'''
move({point1[0]}, {point1[1]})
while not arrived():
    sleep(0.1)
        '''
        self.unit.init_script(ai)
        # Wait exactly how much is needed:
        # v = x/t
        sleep(x/v)
        self.assertTrue(
            self.unit.arrived()
        )

    def test_eta(self):
        v = self.unit.max_velocity 
        x = util.distance(point0,point1)
        self.unit.x, self.unit.y = point0
        ai = f'''
eta = move({point1[0]}, {point1[1]})
sleep(eta)
        '''
        self.unit.init_script(ai)
        sleep(max_t+0.2)
        self.assertTrue(
            self.unit.arrived()
        )

