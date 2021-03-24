import math
import pyglet 

from models.base import physicalobject
from resources import load
import util


class MovableObject(physicalobject.PhysicalObject):

    def __init__(self, *args, **kwargs):
        super(MovableObject, self).__init__(*args, **kwargs)

        self.target_sprite = physicalobject.PhysicalObject(
            load.knob, 
            batch=self.batch
        )

        self.stop()
        self.max_velocity = 250 # Pixel Per DT


    def move(self, x, y):
        self.target = x, y
        self.target_sprite.x = x
        self.target_sprite.y = y
        self.target_sprite.visible = True


    def stop(self):
        self.target = None
        self.target_sprite.visible = False

        self.velocity_x = 0
        self.velocity_y = 0


    def arrived(self, where=None):
        if where is None:
            where = self.target
        if not self.target:
            return True

        d = util.distance((self.x, self.y), where)
        if d < 10:  # Close enough to target
            return True

        return False


    def update(self, dt):
        super().update(dt)
        self.target_sprite.update(dt)

        if self.arrived():
            self.stop()
            self.target_sprite.visible = False
            return

        dx = self.target[0] - self.x
        dy = self.target[1] - self.y

        a = util.angle((1,0), (dx, dy))
        self.velocity_x = self.max_velocity * math.cos(a) 
        self.velocity_y = self.max_velocity * math.sin(a)

        if dy != abs(dy): 
            self.velocity_y *= -1 


    def delete(self):
        self.target_sprite.delete()
        super().delete()


