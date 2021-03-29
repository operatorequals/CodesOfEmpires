import unittest
import pyglet

from threading import Thread

from mechanics.game import WINDOW, BATCH, APP

# This moves the window to the perfect
# location on screen for debugging
WINDOW.set_visible(False)
WINDOW.set_location(1120,200)
WINDOW.set_visible(True)

TEXT_BATCH = pyglet.graphics.Batch()

@WINDOW.event
def on_draw():
    WINDOW.clear()
    BATCH.draw()
    TEXT_BATCH.draw()

# ==================================================

class GameTest(unittest.TestCase):

    label_pos = [10, 550]
    def setUp(self):
        WINDOW.set_caption(f'{self._testMethodName}')
 
        self.label = pyglet.text.Label(self._testMethodName,
                                 x = GameTest.label_pos[0],
                                 y = GameTest.label_pos[1],
                                 batch=TEXT_BATCH
                                )
        GameTest.label_pos[1] -= 15
        self.thr = Thread(target=APP.run, daemon=False)
        self.thr.start()
#        self.objects = []


    def tearDown(self):
        BATCH.invalidate()
#        for obj in objects:
#            obj.delete()
        APP.exit()
        self.thr.join()

