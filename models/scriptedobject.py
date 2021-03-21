import pyglet
from threading import Thread, Event

from models import physicalobject

# Code that runs in the beginning of every script
preamble = """
from time import sleep
import random


while not stop_event.is_set():
    pass
"""

def linter(code):
    ret = ''
    for i in code.splitlines():
        ret += '    ' + i + '\n'
    return ret


class ScriptedObject(physicalobject.PhysicalObject):
    def __init__(self, *args, script=None, locals_={}, **kwargs):
        super(ScriptedObject, self).__init__(*args, **kwargs)

        self.stop_event = Event()
        self.script = None
        if script:
            self.init_script(code, locals_)


    def init_script(self, code=None, locals_={}):
        if self.script:
            self.stop_script()

        if code is None:
            code = self.code

        if locals_ is None:
            locals_ = {}

        code = preamble + linter(code)
        locals_['stop_event'] = self.stop_event
        self.script = Thread(
            target=exec,
            args=(code, locals_),
            daemon=True
        )
        self.script.start()


    def stop_script(self):
        self.stop_event.set()

