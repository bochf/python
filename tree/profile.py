from getopt import getopt
from sys import argv
from datetime import datetime
from datetime import timedelta

import tree


class FunctionTrace:
    def __init__(self, func_name, start_time, end_time=None):
        self.func_name = func_name

        # the input is millisecond, need to times 1000 to get microsecond
        self.start_time = datetime.strptime(start_time+"000", "%d%b%Y_%H:%M:%S.%f")
        if end_time is not None:
            self.end_time = datetime.strptime(end_time+"000", "%d%b%Y_%H:%M:%S.%f")
            self.duration = self.end_time - self.start_time
        else:
            self.end_time = None
            self.duration = 0

def help():
    print 'Usage: profile.py -l <logfile>'

def loadFromLog(file_name):
    try:
        print "### reading file " + file_name
        file = open(file_name, 'r')
        print file.read()
    except:
        print "Error in reading file: " + str(file_name)

def main(argv):
    file_name = ''

    try:
        opts, args = getopt(argv, 'hl:', ['log='])
    except GetoptError:
        help()
        return -1

    for opt, arg in opts:
        if opt == '-h':
            help()
            return 0
        elif opt in ('-l', '--log'):
            file_name = arg
        else:
            help()
            return -1

    loadFromLog(file_name)
    return 0

if __name__ == '__main__':
    main(argv[1:])
