from src.writer import FileWriter, Event
import os
from os import path

def get_time():
    return '00:00:00'

class LogWriter():
    def __init__(self, root_dir='.'):
        self._root_dir = root_dir
        self._step_dict = {}
        os.makedirs(root_dir, exist_ok=True)
        self._event_writer = FileWriter(fn=path.join(self._root_dir, 'event.log'))
        self._meta_writer = FileWriter(fn=path.join(self._root_dir, 'meta.log'))

    def add_scalar(self, name, value, time=None, step=None):
        if step is None:
            if name in self._step_dict:
                step = self._step_dict[name]
                self._step_dict[name] += 1
            else:
                step = 0
                self._step_dict[name] = 1
        if time is None:
            time = get_time()
        e = Event(time=time, step=step, name=name, val=value)
        self._event_writer.add_event(e)

    def add_scalar_dict(self, scalar_dict, step=None):
        for name, val in scalar_dict.items():
            time = get_time()
            self.add_scalar(name, val, time, step)

    def add_config(self, cfg_dict):
        for name, val in cfg_dict.items():
            e = Event(name=name, val=val)
            self._meta_writer.add_event(e)

    def add_id(self, id):
        e = Event(name='commit-id', val=id)
        self._meta_writer.add_event(e)

    def close(self):
        self._event_writer.close()
        self._meta_writer.close()
