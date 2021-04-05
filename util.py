
import threading
import functools
import math


def distance(point_1=(0, 0), point_2=(0, 0)):
    """Returns the distance between two points"""
    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)

# Trigonometry vector angle:
#  https://stackoverflow.com/a/2827475
def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

lock_ring = {}
'''
    lock = lock_ring.get(lock_key, threading.Lock())
    if lock_key is not None:
        lock_ring[lock_key] = lock
'''

# Python decorator for parameterizing
# decorators:
#  https://stackoverflow.com/a/26151604
def parameterized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer


# Python thread safety:
#  https://stackoverflow.com/a/29163532
LOCK_RING = {}
# Taken from:
#  https://stackoverflow.com/a/490090
# for methods
def synchronized(lock_key=None, func_type='method'):
    """ Synchronization decorator """
    def wrap(f):
        @functools.wraps(f)
        def newFunction(*args, **kw):
            if func_type == 'method':
                self = args[0]
                lock_ring = self.__dict__
            else:
                global LOCK_RING
                lock_ring = LOCK_RING
            if lock_key is not None:
                lock = lock_ring.get(lock_key, threading.Lock())
                lock_ring[lock_key] = lock
            else:
                lock = threading.Lock()
            assert lock_key in self.__dict__
#            print('trying to access', lock, "for", f) 
            with lock:
                return f(*args, **kw)
        return newFunction
    return wrap

