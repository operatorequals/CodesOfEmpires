import pyglet

import os

# Tell pyglet where to find the resources

pyglet.resource.path = [os.path.dirname(os.path.realpath(__file__))]
pyglet.resource.reindex()


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


knob=pyglet.resource.image("knob.png")
center_image(knob)

worker=pyglet.resource.image("worker.png")
worker.width  = 42
worker.height = 42
center_image(worker)

archer=pyglet.resource.image("archer.png")
archer.width  = 42
archer.height = 42
center_image(archer)

infantry=pyglet.resource.image("infantry.png")
infantry.width  = 42
infantry.height = 42
center_image(infantry)

cavalry=pyglet.resource.image("cavalry.png")
cavalry.width  = 42
cavalry.height = 42
center_image(cavalry)



wood=pyglet.resource.image("wood.png")
wood.width  = 32
wood.height = 32
center_image(wood)

food=pyglet.resource.image("food.png")
food.width  = 32
food.height = 32
center_image(food)

iron=pyglet.resource.image("iron.png")
iron.width  = 32
iron.height = 32
center_image(iron)


