from time import sleep
from random import randint

from mechanics.game import BATCH
from mechanics.team import createTeam
from models.resources import food
from resources import load

import tests
import util

from models.units import TO_ADD, TO_REMOVE, delete_unit

class Combat(tests.GameTest):

    def setUp(self):

        super().setUp()
        self.team = createTeam(units={'worker':1}, batch=BATCH)
        while not self.team.members: continue
        self.unit = list(self.team.members)[0]
#        self.unit.x = 500
#        self.unit.y = 500


    def tearDown(self):
        super().tearDown()
        self.team.delete()


    def test_hp_script(self):
        ai = """
type(HP()) == int
type(HP_PERCENT()) == int
stop_script()
"""
        self.team.init_script(ai)
        self.unit.script.join()

        self.assertTrue(type(self.unit.hp) == int)
        self.assertTrue(type(self.unit.hp_percent) == int)

    def test_damage(self):
        ai = """
while HP_PERCENT() == 100:
    sleep(1)
stop_script()
"""
        self.team.init_script(ai)
        self.unit.apply_damage(5)
        self.unit.script.join()

        self.assertTrue(
            (self.unit._max_hp - 5) == self.unit._hp
        )


    def test_dead(self):
        ai = """
sleep(1)
"""
        self.team.init_script(ai)
        self.unit.apply_damage(self.unit.hp)
        self.unit.script.join()

        self.assertTrue(
            self.unit.dead
        )


    def test_dead_stuck_in_loop(self):
        ai = """
while True:
    sleep(1)
"""
        self.team.init_script(ai)
        self.unit.apply_damage(self.unit.hp)
        self.unit.script.join()

        self.assertTrue(
            self.unit.dead
        )


