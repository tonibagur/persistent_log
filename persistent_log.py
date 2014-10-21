

import persistent
import transaction
import ZODB
import ZODB.FileStorage
import BTrees.OOBTree
import datetime



class PersistentLog(object):
    def __init__(self,db_path='log_db.fs'):
        self.db = ZODB.DB(ZODB.FileStorage.FileStorage(db_path))
        self.root = self.db.open().root()
        if not hasattr(self.root,'log'):
            self.root.log=BTrees.OOBTree.BTree()

    def log(self,object_to_log):
        date_str=str(datetime.date.today())
        if date_str not in self.root.log:
            self.root.log[date_str]=persistent.list.PersistentList()
        self.root.log[date_str].append(object_to_log)
        transaction.commit()

    def close(self):
        self.db.close()



if __name__=='__main__':
    pl=PersistentLog()
    pl.log({'hola':'mon'})
    pl.log({'hola3':'mon2'})
    for x in pl.root.log.keys():
        print x , ":" , pl.root.log[x]
    pl.close()

        

