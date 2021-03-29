import pyglet

from threading import Thread

from mechanics import team
from mechanics.loop import update

WINDOW = pyglet.window.Window(800, 600, visible=False)
WINDOW.set_location(1120,200)
WINDOW.set_visible(True)


BATCH = pyglet.graphics.Batch()
APP = pyglet.app

TEAMS=[
]


pyglet.clock.schedule_interval(update, 1 / 120.0)

