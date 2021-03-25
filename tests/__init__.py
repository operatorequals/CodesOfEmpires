import pyglet
import unittest

from threading import Thread

WINDOW = pyglet.window.Window(800, 600, visible=False)
WINDOW.set_location(1120,200)
WINDOW.set_visible(True)

BATCH = pyglet.graphics.Batch()

GAME_OBJECTS = []
APP = pyglet.app

def refresh():
    global BATCH, APP, GAME_OBJECTS 
    for obj in GAME_OBJECTS:
        obj.delete()
    GAME_OBJECTS = []
    BATCH.invalidate()
    BATCH = pyglet.graphics.Batch()


@WINDOW.event
def on_draw():
    WINDOW.clear()
    BATCH.draw()


def update(dt):
    for obj in GAME_OBJECTS:
        obj.update(dt)


pyglet.clock.schedule_interval(update, 1 / 120.0)

# ==================================================

class GameTest(unittest.TestCase):

    def setUp(self):
        WINDOW.set_caption(self._testMethodName)
        GAME_OBJECTS.append(self.unit)
        self.thr = Thread(target=APP.run, daemon=False)
        self.thr.start()

    def tearDown(self):
        #for obj in GAME_OBJECTS:
        #    obj.delete()
        #refresh()
        APP.exit()
        self.thr.join()


