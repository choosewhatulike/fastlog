from src.writer import FileWriter, Event
from src.logger import LogWriter
import os

events = [
    Event(step=1, time=None, name='loss', val=10.2),
    Event(step=2, time='00:00:01', name='loss', val=20.5),
    Event(step=3, time=None, name='loss', val=13.2),
    Event(step=4, time='00:00:01', name='loss', val=4.2),
    Event(step=5, time='00:00:01', name=None, val=50.2),
    Event(step=6, time='00:00:01', name='loss', val=6.2),
    Event(step=7, time='00:00:01', name='loss', val=None),
    Event(step=8, time='00:00:01', name='loss', val=8.2),
]


class TestWriter():
    fn = 'test_writer.log'
    def test1(self):
        w = FileWriter(self.fn)
        try:
            w.add_str('='*10)
            for e in events:
                w.add_event(e)
            w.add_str('='*10)
        finally:
            w.close()

        with open(self.fn, 'r', encoding='utf-8') as f:
            true_lines = ['='*10] + [e.to_json() for e in events] + ['='*10]
            test_lines = f.readlines()
            for l1, l2 in zip(true_lines, test_lines):
                assert l1 + '\n' == l2

    def teardown(self):
        os.remove(self.fn)
        pass


class TestLogger():
    fn = 'test_logger'
    meta_fn = fn + '/meta.log'
    event_fn = fn + '/event.log'
    def test1(self):
        w = LogWriter(self.fn)
        w.add_id('abcd12345')

        cfg = {'lr':3e-4,
               'hidden':400,
               'weight_decay': 1e-5,
               'lr_decay':0.95,}
        w.add_config(cfg)

        w.add_scalar('loss', 1, step=1)
        w.add_scalar('loss', 2.2, step=2)
        w.add_scalar('loss', 0.3, step=3)
        w.add_scalar('loss', 10.3, step=4)
        w.add_scalar('loss', 2.3, step=5)
        w.add_scalar('loss', 4.3, step=6)
        w.close()

        with open(self.event_fn, 'r') as f:
            text = ''.join(f.readlines())
        true_text = """{"name": "loss", "val": 1, "time": "00:00:00", "step": 1}
{"name": "loss", "val": 2.2, "time": "00:00:00", "step": 2}
{"name": "loss", "val": 0.3, "time": "00:00:00", "step": 3}
{"name": "loss", "val": 10.3, "time": "00:00:00", "step": 4}
{"name": "loss", "val": 2.3, "time": "00:00:00", "step": 5}
{"name": "loss", "val": 4.3, "time": "00:00:00", "step": 6}
"""
        assert text == true_text
        with open(self.meta_fn, 'r') as f:
            text = ''.join(f.readlines())
        true_text = """{"name": "commit-id", "val": "abcd12345"}
{"name": "lr", "val": 0.0003}
{"name": "hidden", "val": 400}
{"name": "weight_decay", "val": 1e-05}
{"name": "lr_decay", "val": 0.95}
"""
        assert text == true_text

    def teardown(self):
        os.remove(self.event_fn)
        os.remove(self.meta_fn)
        os.rmdir(self.fn)
        pass
