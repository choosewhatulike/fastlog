import json
import _pickle as pickle
import threading
import queue


class Event():
    def __init__(self, name=None, val=None, time=None, step=None):
        self.time = time
        self.step = step
        self.name = name
        self.val = val

    def to_json(self):
        data = {
            'name':self.name,
            'val':self.val,
        }
        if self.time is not None:
            data['time'] = self.time
        if self.step is not None:
            data['step'] = self.step
        return json.dumps(data)

class FileWriter():
    def __init__(self, fn:str):
        self._fn = fn
        self._fp = open(fn, 'w', encoding='utf-8')
        self._q = queue.Queue()
        self._thread = FileWriterThreading(self._fp, self._q)
        self._thread.daemon = True
        self._thread.start()

    def add_event(self, e:Event):
        self._q.put(e.to_json(), timeout=60)

    def add_str(self, s:str):
        self._q.put(s, timeout=60)

    def close(self):
        try:
            self._q.put(None, timeout=60)
            self._thread.join(timeout=60)
        finally:
            self._fp.close()


class FileWriterThreading(threading.Thread):
    def __init__(self, fp, q:queue.Queue):
        super(FileWriterThreading, self).__init__()
        self._fp = fp
        self._q = q

    def run(self):
        while 1:
            msg = self._q.get()
            if msg is None:
                break
            self._fp.write(msg+'\n')

