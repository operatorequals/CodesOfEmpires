import pyglet

from models.resources import resource

from resources import load


class Iron(resource.Resource):

    def __init__(self, *args, img=load.iron, **kwargs):
        super(Iron,self).__init__(*args, img=img, **kwargs)


