import pyglet
from threading import Thread, Event

from models import physicalobject

# Code that runs in the beginning of every script
preamble = """
from time import sleep
import random
"""

class ScriptedObject(physicalobject.PhysicalObject):
    def __init__(self, *args, script=None, locals_={}, **kwargs):
        super(ScriptedObject, self).__init__(*args, **kwargs)

        self.script = None
        if script:
            self.init_script(code, locals_)


    def init_script(self, code=None, locals_={}):
        if self.script:
            # Kill it with fire for now
            self.script._running = False

        if code is None:
            code = self.code

        if locals_ is None:
            locals_ = {}

        code = preamble + code

        self.script = Thread(
            target=exec,
            args=(code, locals_),
            daemon=True
        )
        self.script.start()


