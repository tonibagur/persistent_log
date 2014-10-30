from persistent_log import PersistentLog
import datetime
from pprint import pprint

def main(argv):
	pl=PersistentLog(argv[1])
	txid=pl.log_start({'hello':'world'})
	pprint([x for x in pl.get_log_days()])
	pl.log_stop(txid)

if __name__=='__main__':
	import sys
	main(sys.argv)