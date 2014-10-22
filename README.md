#PersistentLog for Python

A simple persistent log backed by the ZODB object database. The logs are indexed by date and can be any serializable Python object:

```python
pl=PersistentLog()
a=pl.log_start({'hola':'mon'})
b=pl.log_start({'hola3':'mon2'})
for x in pl.root.log.keys():
    print x , ":-----------"
    for y in pl.root.log[x]:
        print y,pl.root.log_map[y]
import time
time.sleep(3)
pl.log_stop(a)
pl.log_stop(b)
for x in pl.root.log.keys():
    print x , ":-----------"
    for y in pl.root.log[x]:
        print y,pl.root.log_map[y]    
pl.close()
```

