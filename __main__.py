import pyglet

from models.units import unit, workerunit
from models.resources import resource, wood, food, iron
from resources import load


ai = """
x = random.randint(0,600)
y = random.randint(0,600)
move(x,y)
while not arrived():
    sleep(1)

if not explored:
    continue

a = last_explored()
if a.isWood:
    move(a.x,a.y)

while not arrived():
    sleep(1)
"""


main_batch = pyglet.graphics.Batch()

sprite = workerunit.WorkerUnit(x=250, batch = main_batch)
sprite.locals_['isWood'] = models.isWood

wood_spr = wood.Wood(wood=1000, batch=main_batch, x= 400, y=400)
iron_spr = iron.Iron(iron=1000, batch=main_batch, x= 600, y=600)
food_spr = food.Food(food=1000, batch=main_batch, x= 200, y=200)
#game_objects = [sprite, sprite2]
game_objects = [sprite, wood_spr, food_spr, iron_spr]

sprite.init_script(ai)
#sprite2.init_script(ai)
# Set up a window
game_window = pyglet.window.Window(1024, 720)



@game_window.event
def on_draw():
    game_window.clear()

    main_batch.draw()


def update(dt):
    
    for i in range(len(game_objects)):
        obj = game_objects[i]
        obj.update(dt)
        
        for j in range(i+1, len(game_objects)):
            obj2 = game_objects[j]
            if 'Unit' in str(obj):
                obj.in_visible_range(obj2)
            if 'Unit' in str(obj2):
                obj2.in_visible_range(obj)


if __name__ == "__main__":

    # Update the game 120 times per second
    pyglet.clock.schedule_interval(update, 1 / 120.0)

    # Tell pyglet to do its thing
    pyglet.app.run()

