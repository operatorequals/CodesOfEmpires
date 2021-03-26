import pyglet
import unittest

from threading import Thread

WINDOW = pyglet.window.Window(800, 600, visible=False)
WINDOW.set_location(1120,200)
WINDOW.set_visible(True)

BATCH = pyglet.graphics.Batch()
#TEXT_BATCH = pyglet.graphics.Batch()

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
#    TEXT_BATCH.draw()


def update(dt):
    
    for i in range(len(GAME_OBJECTS)):
        obj = GAME_OBJECTS[i]
        obj.update(dt)
        
        for j in range(i+1, len(GAME_OBJECTS)):
            obj2 = GAME_OBJECTS[j]
            if 'Unit' in str(obj):
                obj.in_visible_range(obj2)
            if 'Unit' in str(obj2):
                obj2.in_visible_range(obj)



pyglet.clock.schedule_interval(update, 1 / 120.0)

 
# ==================================================

class GameTest(unittest.TestCase):

    label_pos = [10, 550]
    def setUp(self):
        WINDOW.set_caption(self._testMethodName)
        '''
        self.label = pyglet.text.Label(self._testMethodName,
                                 x = GameTest.label_pos[0],
                                 y = GameTest.label_pos[1],
                                 batch=TEXT_BATCH
                                )
        GameTest.label_pos[1] -= 15
        '''
        self.thr = Thread(target=APP.run, daemon=False)
        self.thr.start()

    def tearDown(self):
        #self.label.text = self.label.text + self._outcome
#        for obj in GAME_OBJECTS:
#            obj.delete()
        #refresh()
        APP.exit()
        self.thr.join()


