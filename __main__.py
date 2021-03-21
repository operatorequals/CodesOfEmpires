import pyglet

from models import unit
#
# Tell pyglet where to find the resources
pyglet.resource.path = ['.']
pyglet.resource.reindex()

ai = """
while True:
    x = random.randint(0,600)
    y = random.randint(0,600)
    move(x,y)
    sleep(1)

"""

#sprite = unit.Unit(img=pyglet.resource.image("assasin.png"),x=250)
sprite = unit.Unit(img=pyglet.resource.image("knob.png"),x=250)

movable_locals = {
    "move" : sprite.move,
    "stop" : sprite.stop,
}
 


sprite.init_script(ai, movable_locals)

# Set up a window
game_window = pyglet.window.Window(800, 600)



@game_window.event
def on_draw():
    game_window.clear()

    sprite.draw()
    if sprite.target_sprite:
        sprite.target_sprite.draw()



def update(dt):
    sprite.update(dt)



if __name__ == "__main__":

    # Update the game 120 times per second
    pyglet.clock.schedule_interval(update, 1 / 120.0)

    # Tell pyglet to do its thing
    pyglet.app.run()
