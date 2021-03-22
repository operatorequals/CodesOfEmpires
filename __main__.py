import pyglet

from models.units import unit
from models.resources import resource
#
# Tell pyglet where to find the resources
pyglet.resource.path = ['./resources']
pyglet.resource.reindex()

ai = """
x = random.randint(0,600)
y = random.randint(0,600)
move(x,y)
while not last_explored:
    sleep(0.5)

work(last_explored)
"""


main_batch = pyglet.graphics.Batch()

sprite = unit.Unit(img=pyglet.resource.image("knob.png"),x=250, batch = main_batch)
sprite2 = unit.Unit(img=pyglet.resource.image("knob.png"),x=250, batch = main_batch)

wood = resource.Resource(img=pyglet.resource.image("knob.png"), wood=1000, batch=main_batch, x= 400, y=400)

game_objects = [sprite, sprite2, wood]

sprite.init_script(ai)
sprite2.init_script(ai)

# Set up a window
game_window = pyglet.window.Window(800, 600)



@game_window.event
def on_draw():
    game_window.clear()

    main_batch.draw()


def update(dt):

    for obj in game_objects:
        obj.update(dt)


if __name__ == "__main__":

    # Update the game 120 times per second
    pyglet.clock.schedule_interval(update, 1 / 120.0)

    # Tell pyglet to do its thing
    pyglet.app.run()
