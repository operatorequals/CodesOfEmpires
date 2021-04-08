import pyglet

from time import sleep
from threading import Thread

from mechanics.team import createTeam
from mechanics.loop import update


SIZE = {'X':800, 'Y':600}
#SIZE = {'X':1024, 'Y':768}
WINDOW = pyglet.window.Window(SIZE['X'], SIZE['Y'], visible=False)
#WINDOW.set_location(1120,200)
WINDOW.set_visible(True)
BATCH = pyglet.graphics.Batch()
APP = pyglet.app
#pyglet.gl.glClearColor(0.8, 0.8, 0.8, 1.0)


@WINDOW.event
def on_draw():
    WINDOW.clear()
    BATCH.draw()





pyglet.clock.schedule_interval(update, 1 / 120.0)

APP_THREAD = Thread(target=APP.run)




if __name__ == '__main__':
    APP_THREAD.start()
    from resources import load
    t = createTeam(batch=BATCH, units={'worker':100}, population=1000)
    sleep(1)
    for unit in t.members:
        unit.image = load.cavalry

    for i in range(0,100):
        t.init_script(f"""
x = random.randint(0,{SIZE['X']})
y = random.randint(0,{SIZE['Y']})
eta=move(x, y)
sleep(eta)
        """)
        sleep(5)

