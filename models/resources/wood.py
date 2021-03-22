import pyglet

from models.resources import resource

from resources import load


class Wood(resource.Resource):

    def __init__(self, *args, img=load.wood, **kwargs):
        super(Wood,self).__init__(*args, img=img, **kwargs)


