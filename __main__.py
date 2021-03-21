import pyglet

from models import unit
#
# Tell pyglet where to find the resources
pyglet.resource.path = ['.']
pyglet.resource.reindex()

ai = """
x = random.randint(0,600)
y = random.randint(0,600)
move(x,y)
sleep(1)
if arrived():
    stop_script()
"""


main_batch = pyglet.graphics.Batch()

sprite = unit.Unit(img=pyglet.resource.image("knob.png"),x=250, batch = main_batch)
sprite2 = unit.Unit(img=pyglet.resource.image("knob.png"),x=250, batch = main_batch)

game_objects = [sprite, sprite2]

sprite.init_script(ai)
sprite2.init_script(ai)

# Set up a window
game_window = pyglet.window.Window(800, 600)



@game_window.event
def on_draw():
    game_window.clear()

    main_batch.draw()
    sprite.draw()
    if sprite.target_sprite:
        sprite.target_sprite.draw()



def update(dt):
    sprite.update(dt)
    sprite2.update(dt)



if __name__ == "__main__":

    # Update the game 120 times per second
    pyglet.clock.schedule_interval(update, 1 / 120.0)

    # Tell pyglet to do its thing
    pyglet.app.run()
