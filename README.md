A simple persistent log backed by the ZODB object database. The logs are indexed by date and can be any serializable Python object:

pl=persistent_log.PersistentLog('/home/test/test.fs')
pl.log({'hello':'world'})
pl.log({'good bye':'world'})
for x in pl.root.log.keys():
    print x , ":" , pl.root.log[x]
pl.close()


