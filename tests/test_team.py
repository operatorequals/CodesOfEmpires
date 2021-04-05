from time import sleep
from random import randint

from mechanics.game import BATCH
from mechanics.team import createTeam
from models.resources import food
from resources import load

import tests
import util

from models.units import TO_ADD, TO_REMOVE, delete_unit

class Team(tests.GameTest):

    def setUp(self):

        super().setUp()
        self.team = createTeam(units={'worker':1}, batch=BATCH)
        while not self.team.members: continue
        self.unit = list(self.team.members)[0]
        self.unit.x = 0
        self.unit.y = 0

        self.food = food.Food(food=500, batch=BATCH, x=200, y=200)
        TO_ADD.put(self.food, block=True)


    def tearDown(self):
        super().tearDown()
        self.team.delete()
        TO_REMOVE.put(self.food, block=True)


    def test_add_worker(self):
        ai = f"""
sleep(0.2)
move(100,300)
while not explored:
    sleep(0.5)
a = explored[-1]

if a.isFood:
    collect(a)

    while FOOD() < 50:
        sleep(0.1)
    stop_work()
    createWorker()
else:
    continue
stop_script()
        """
        self.team.init_script(ai)
        sleep(6)
        self.assertTrue(
            len(self.team) == 2
        )
        self.assertTrue(
            self.team.FOOD < 20
        )


    def test_not_afford(self):
        ai = f"""
sleep(0.2)
move(200,200)
while not explored:
    sleep(0.5)
a = explored[-1]
if a.isFood:
    collect(a)

    while FOOD() < 20:
        sleep(0.5)
    #stop_work()
    created = createWorker()
sleep(2)
stop_script()
        """
        self.team.init_script(ai)
        sleep(3)
        self.unit.script.join()
        self.assertTrue(
            self.team.FOOD < 20
        )

        self.assertTrue(
            len(self.team) == 1
        )


    def test_use_second_worker(self):
        ai = f"""
move(300,100)
while not explored:
    sleep(0.5)
a = explored[-1]
guard = False
if a.isFood and not guard:
    guard = True
    collect(a)

    while FOOD() < 50:
        sleep(0.1)
    stop_work()
    created=createWorker()
    #print(created)
else:
    sleep(0.1)
    continue
stop_script()
        """
        self.team.init_script(ai)
        self.unit.script.join()
        sleep(0.2) # Wait for Team's update to add the unit
        self.assertTrue(
            len(self.team) == 2
        )
        # A second worker exists by now
        ai2 = """
eta=move(400,600)
sleep(eta)
stop_script()
"""
        self.team.init_script(ai2)
        # wait indefinitely for both to finish
        for unit in self.team.members:
            unit.script.join()
        
        for unit in self.team.members:
            self.assertTrue(
                unit.arrived((400, 600))
            )


    def test_up_to_n(self, N=3):
        ai2= 'move(500,500)'
        ai = f'''
sleep(0.8)
while POPULATION() < {N}:
    eta=move(200,400)
    for e in explored:
        if e.isFood:
            collect(e)
            while FOOD() < 50 and POPULATION() < {N}:
                sleep(0.3)
            created=createWorker()
    sleep(0.3)
stop_script()
'''
        self.team.init_script(ai)
        while len(self.team) < N:
            sleep(1)
        sleep(0.2) # Wait for Team's update to add the unit
#        self.team.init_script('stop_script()')
#        for unit in team.members:
#            unit.stop_script()
        self.assertTrue(len(self.team) >= N)
