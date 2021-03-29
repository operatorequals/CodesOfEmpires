import pyglet
from threading import Thread, Event

from models.base import physicalobject

# Code that runs in the beginning of every script
preamble = """
from time import sleep
wait=sleep
import random


while not stop_event.is_set():
    pass
"""

escape_words = [
    "setattr", "getattr",
    "import",
    "exec", "eval",
    "__attr__",
    "__",
    "open",
]

def security_check(code):
    for word in escape_words:
        if word in code:
            raise IllegalArgumentException(
                f"'{word}' is not allowed in the objects script"
            )
        
def linter(code):
    ret = ''
    for i in code.splitlines():
        ret += '    ' + i + '\n'
    security_check(ret)
    return ret


class ScriptedObject(physicalobject.PhysicalObject):
    def __init__(self, *args, script=None, locals_={}, **kwargs):
        super(ScriptedObject, self).__init__(*args, **kwargs)

        self.stop_event = Event()
        self.script = None
        self.running = False
        self.locals_ = locals_
        self.locals_['stop_event'] = self.stop_event
        if script:
            self.init_script(code, locals_)
            self.running = True


    def init_script(self, code=None):
        if self.running:
            self.stop_script()

        if code is None:
            code = self.code

        if not code or code.isspace():
            return

        code = preamble + linter(code)
        self.stop_event.clear()
        self.script = Thread(
            target=exec,
            args=(code, self.locals_),
            daemon=True
        )
        self.script.start()
        self.running = True


    def stop_script(self):
        if not self.running:
            return
        self.stop_event.set()
        try:
            self.script.join()
        except RuntimeError:
            pass
        self.running = False 

    
    def delete(self):
        self.stop_script()
        super().delete()

