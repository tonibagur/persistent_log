from persistent_log import PersistentLog
import datetime
from pprint import pprint

def main(argv):
	if len(argv)==1:
		print "Usage:"
		print "persistent_log_report listdays <file>"
		print "persistent_log_report listlogs <day> <file>"
	else:
		if argv[1]=='listdays':
			pl=PersistentLog(argv[2])
			pprint([x for x in pl.get_log_days()])
		if argv[1]=='listlogs':
			pl=PersistentLog(argv[3])
			pprint([x for x in pl.iter_logs_from_day(sys.argv[2])])

if __name__=='__main__':
	import sys
	main(sys.argv)