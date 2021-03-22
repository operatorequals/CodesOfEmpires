import pyglet

from models.resources import resource

from resources import load


class Food(resource.Resource):

    def __init__(self, *args, img=load.food, **kwargs):
        super(Food,self).__init__(*args, img=img, **kwargs)


