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
    "locals","globals",
]

def security_check(code):
    for word in escape_words:
        if word in code:
            raise IllegalArgumentException(
                f"'{word}' is not allowed in the objects script"
            )
        
def linter(code, definitions='', constants=''):
    indented_code = ''
    for i in code.splitlines():
        indented_code += '    ' + i + '\n'
    payload = f'''
{constants}
{definitions}
{indented_code}
    '''
    security_check(payload)
    return preamble + payload


class ScriptedObject(physicalobject.PhysicalObject):
    def __init__(self, *args, code=None, locals_={}, definitions='', constants='', **kwargs):
        super(ScriptedObject, self).__init__(*args, **kwargs)

        self.stop_event = Event()
        self.script = None
        self.running = False
        self.locals_ = locals_
        self.locals_['stop_event'] = self.stop_event
        if code:
            self.init_script(code)


    def init_script(self, code=None, definitions='', constants=''):
        if self.running:
            self.stop_script()

        if not code or code.isspace():
            return

        code = linter(code)
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

