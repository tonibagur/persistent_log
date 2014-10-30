
import persistent
import transaction
import ZODB
import ZODB.FileStorage
import BTrees.OOBTree
import datetime


import random

import sys

class PersistentLog(object):
    def __init__(self,db_path='log_db.fs'):
        self.db = ZODB.DB(ZODB.FileStorage.FileStorage(db_path))
        self.root = self.db.open().root()
        if not hasattr(self.root,'log'):
            self.root.log=BTrees.OOBTree.BTree()
        if not hasattr(self.root,'log_map'):
            self.root.log_map=BTrees.OOBTree.BTree()

    def get_log_days(self):
        return self.root.log.keys()

    def iter_logs_from_day(self,day):
        for x in self.root.log[day]:
            yield self.root.log_map[x]

    def log_start(self,object_to_log):
        date_str=str(datetime.date.today())
        now=datetime.datetime.now()
        if date_str not in self.root.log:
            self.root.log[date_str]=persistent.list.PersistentList()
        txid=self.get_txid()
        self.root.log[date_str].append(txid)
        self.root.log_map[txid]=persistent.mapping.PersistentMapping({'object':object_to_log,'start_time':now})
        transaction.commit()
        return txid

    def get_txid(self):
        txid=None
        while not txid:
            temp=random.randint(0,sys.maxint)
            if self.root.log_map.get(temp)==None:
                txid=temp
        return txid

    def log_stop(self,txid):
        if self.root.log_map.get(txid):
            now=datetime.datetime.now()
            elapsed=(now-self.root.log_map[txid]['start_time']).total_seconds()
            self.root.log_map[txid]['stop_time']=now
            self.root.log_map[txid]['elapsed']=elapsed
            transaction.commit()


    def close(self):
        self.db.close()



if __name__=='__main__':
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
    

        

