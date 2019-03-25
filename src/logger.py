from src.writer import FileWriter, Event
import os
from os import path
import datetime
import time as T


class LogWriter():
    def __init__(self, root_dir='.'):
        self._start_time = None
        self._commit_id = None
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
            time = T.time() - self.get_start_time()
        e = Event(time=time, step=step, name=name, val=value)
        self._event_writer.add_event(e)

    def add_scalar_dict(self, scalar_dict, step=None):
        for name, val in scalar_dict.items():
            time = T.time() - self.get_start_time()
            self.add_scalar(name, val, time, step)

    def add_config(self, cfg_dict):
        for name, val in cfg_dict.items():
            e = Event(name=name, val=val)
            self._meta_writer.add_event(e)

    def add_commit_id(self, id):
        if not isinstance(id, str):
            raise TypeError('commit id must be str')
        e = Event(name='$commit-id$', val=id)
        self._meta_writer.add_event(e)

    def close(self):
        self._event_writer.close()
        self._meta_writer.close()

    def get_start_time(self):
        if self._start_time is None:
            self.add_start_time()
        return self._start_time

    def add_start_time(self, time=None):
        if time is None:
            self._start_time = T.time()
        else:
            if not isinstance(time, (int, float)):
                raise TypeError('time must be int or float')
            self._start_time = time
        t = datetime.datetime.fromtimestamp(self._start_time)
        e = Event(name='$start-time$', val=t.strftime('%Y-%m-%d %H:%M:%S'))
        self._meta_writer.add_event(e)

    def add_rng_seed(self, seed):
        if not isinstance(seed, int):
            raise TypeError('seed must be int')
        e = Event(name='$rng-seed$', val=seed)
        self._meta_writer.add_event(e)
