import copy
import threading

_queue = []
_queue_lock = threading.RLock()

def as_list():
  with _queue_lock:
    return copy.copy(_queue)

def push(val):
  with _queue_lock:
    return _queue.append(val)

def pop():
  with _queue_lock:
    if empty():
      return None
    return _queue.pop()

def size():
  with _queue_lock:
    return len(_queue)

def empty():
  with _queue_lock:
    return not len(_queue)

def remove(media_id):
  with _queue_lock:
    for i, item in enumerate(_queue):
      if item.media_id == media_id:
        del _queue[i]
        return
