# fastlog
轻量级的机器学习实验记录工具。内部开发中

## Note
现已并入 [fitlog](https://github.com/choosewhatulike/fitlog)

## 使用方法

使用`Logger`记录实验信息
```python
from fastlog import Logger
w = Logger(log_dir='...') # 传入log保存目录

# 记录实验参数
cfg = {'lr': 3e-4,
       'hidden': 400,
       'weight_decay': 1e-5,
       'lr_decay': 0.95, }
w.add_config(cfg)

# 随着实验进行，记录不同的值
w.add_scalar('c1', 1, step=1)
w.add_scalar('v2', 2.2, step=2)
w.add_scalar('v3', 0.3, step=3)
w.add_loss('corss_loss', 10.3, step=4)
w.add_metric('f1', 2.3, step=5)
w.add_metric('acc', 4.3, step=6)
w.close()
```

使用`LogReader`读取实验信息
```python
from fastlog import LogReader
r = LogReader(log_dir='...') # 传入log保存目录
meta = r.read_metas() # 读取meta信息
hyper = r.read_hypers() # 读取实验参数
events = r.read_events() # 读取实验中数据，loss，metrics等

print(meta)
'''{'commit-id': 'xxxxxx',
    'rng-seed': 863621506, 
    'start-time': '2019-03-29 16:15:00'}
'''
print(hyper)
'''{'lr': 0.0003, 
    'hidden': 400,
    'weight_decay': 1e-05,
    'lr_decay': 0.95}
'''
print(events[0:2])
'''[{'name': 'c1', 'val': 1, 'time': 0, 'step': 1}, 
    {'name': 'v2', 'val': 2.2, 'time': 0, 'step': 2}]
'''
```
