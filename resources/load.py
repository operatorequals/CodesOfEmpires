import pyglet

# Tell pyglet where to find the resources
pyglet.resource.path = ['./resources']
pyglet.resource.reindex()


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


knob=pyglet.resource.image("knob.png")
center_image(knob)

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



worker=pyglet.resource.image("knob.png")
#worker=pyglet.resource.animation("worker1.gif")
worker.width /= 2
worker.height /= 2
center_image(worker)

