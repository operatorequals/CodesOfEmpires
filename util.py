
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

# Python thread safety:
#  https://stackoverflow.com/a/29163532
def synchronized(wrapped):
    lock = threading.Lock()
    @functools.wraps(wrapped)
    def _wrap(*args, **kwargs):
#        print "Calling '%s' with Lock %s" % (wrapped.__name__, id(lock))
        with lock:
            return wrapped(*args, **kwargs)
    return _wrap
