import logging as log
log.basicConfig(filename='/tmp/persistent_log.log',level=log.DEBUG)
logger=log.getLogger('persistent_log')
logger.debug('loading module')

import persistent
import transaction
import ZODB
import ZODB.FileStorage
import BTrees.OOBTree
import datetime
import sqlite3
import StringIO
import re
import pickle

import sys

class PersistentLog(object):
    
    def __init__(self,db_path='log_db.db'):
        self.table = 'Logs'
        self.db_path = db_path
        conn = sqlite3.connect(self.db_path)
        query = 'create table if not exists ' + self.table + '(id INTEGER PRIMARY KEY AUTOINCREMENT, pickle BLOB, date TEXT, dateTime_start TEXT, dateTime_stop TEXT, elapsed INTEGER)'
        conn.execute(query)
        query = 'create index if not exists date_index on ' + self.table + '(dateTime_start)'
        conn.commit()
        conn.close()

    def iterate_logs(self, date_ini, date_end):
        query = 'select pickle from ' + self.table + ' where dateTime_start between \'' + date_ini + '\'  and \'' +  date_end + '\';'
        print query
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        for row in cur.execute(query):
            yield pickle.loads(row[0])
        cur.close()
        conn.close()

    def log_start(self,object_to_log):
        logger.debug('start start')
        query = 'insert into ' + self.table + ' (pickle, date, dateTime_start) values (?, ?, ?)'
        dateTime_start = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        date = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        data_binary=pickle.dumps(object_to_log)
        conn = sqlite3.connect(self.db_path)
        conn.text_factory = str
        conn.execute(query, (data_binary, date, dateTime_start))
        conn.commit()
        conn.close()
        id = self.get_last_id()
        logger.debug('start stop')
        return id

    def get_last_id(self):
        conn = sqlite3.connect(self.db_path)
        query = 'select max(id) from ' + self.table
        cur = conn.cursor()
        cur.execute(query)
        last_id = cur.fetchone()[0]
        cur.close()
        conn.close()
        return last_id

    def get_datetime_start(self, id):
        conn = sqlite3.connect(self.db_path)
        query = 'select dateTime_start from ' + self.table + ' where id=' + str(id)
        cur = conn.cursor()
        cur.execute(query)
        dateTime_start = cur.fetchone()[0]
        cur.close()
        conn.close()
        return dateTime_start

    def calculate_seconds(self, dateTime_start, dateTime_stop):
        d1 = re.sub('-| ', ':', dateTime_start).split(':')
        d2 = re.sub('-| ', ':', dateTime_stop).split(':')
        d_start = datetime.datetime(int(d1[0]), int(d1[1]), int(d1[2]), int(d1[3]), int(d1[4]), int(d1[5]))
        d_stop = datetime.datetime(int(d2[0]), int(d2[1]),int(d2[2]), int(d2[3]), int(d2[4]), int(d2[5]))
        seconds = d_stop - d_start
        return seconds.seconds

    def log_stop(self,id):
        logger.debug('stop start')
        dateTime_stop = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        dateTime_start = self.get_datetime_start(id)
        elapsed = self.calculate_seconds(dateTime_start, dateTime_stop)
        conn = sqlite3.connect(self.db_path)
        query = 'update ' + self.table + ' set dateTime_stop=\'' + dateTime_stop +'\', elapsed=' + str(elapsed) + ' where id=' + str(id)
        conn.execute(query)
        conn.commit()
        conn.close()
        logger.debug('stop stop')

    def close(self):
        pass

if __name__=='__main__':
    pl=PersistentLog() 
    a=pl.log_start({'hola':'mon'})
    b=pl.log_start({'hola3':'mon2'})
    pl.log_stop(a)
    import time 
    time.sleep(5)
    pl.log_stop(b)
    pl.iterate_logs('2014-01-01 00:00:00', '2014-12-31 00:00:00')
    pl.close()