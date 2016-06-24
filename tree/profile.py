import re
import traceback
from getopt import getopt
from sys import argv
from datetime import datetime
from datetime import timedelta

from tree import TreeNode


class FunctionTrace:
    def __init__(self, func_name, start_time=None, end_time=None):
        self.func_name = func_name
        self.setStartTime(start_time)
        self.setEndTime(end_time)

    def __repr__(self):
        duration = self.end_time - self.start_time
        s = r'<NODE name="' + self.func_name + '"'
        s += ' start_time="' + str(self.start_time) + '"'
        s += ' end_time="' + str(self.end_time) + '"'
        s += ' duration="' + str(duration.total_seconds()*1000 + duration.microseconds/1000) + '">'
        return s

    def setStartTime(self, start_time=None):
        if start_time is None:
            self.start_time = datetime.now()
        else:
            # the input is millisecond, need to times 1000 to get microsecond
            self.start_time = datetime.strptime(start_time+"000", "%d%b%Y_%H:%M:%S.%f")

    def setEndTime(self, end_time=None):
        if end_time is None:
            self.end_time = datetime.now()
        else:
            self.end_time = datetime.strptime(end_time+"000", "%d%b%Y_%H:%M:%S.%f")

def help():
    print 'Usage: profile.py -l <logfile>'

def parseTrace(line, tree_node):
    # the log file has below format:
    # 23JUN2016_15:19:16.465 61504:140484032833280 TRACE ibarbutil_functrace.h:27 IBARBUTIL.FUNCTIONTRACE  Enter void BloombergLP::s_ibrarbpost::RequestHelper::processCloseRoomRequest(bsl::shared_ptr<BloombergLP::ibrarbpostmsgs::GenericPostRequestWrapper>, bsl::shared_ptr<BloombergLP::s_ibrarbpost::RequestContext>, bsl::shared_ptr<BloombergLP::ibarbdispatcher::RequestCompletionGuard>, bool) 6299469577153151008

    # we will need column 1, 6 and 7-
    # column 1 is timestamp
    # column 6 is entry/exit flag
    # column 7 and rest are the function signiture and uuid
    fields = line.split()
    if (fields[5] == 'Enter'):
        # get function signature from the 6th space
        func_name = line[[x.start() for x in re.finditer(" ", line)][6]+1:]
        element = FunctionTrace(func_name, fields[0])

        # create a child and add to current tree node
        child = tree_node.addChild(element)
        tree_node = child
    else:
        tree_node.element.setEndTime(fields[0])
        tree_node = tree_node.parent

def loadFromLog(file_name):
    try:
        print "### reading file " + file_name
        file = open(file_name, 'r')

        root_element = FunctionTrace("Log")
        root = TreeNode(root_element)
        stack = [root]
        current = root
        for line in file:
            parseTrace(line.strip(), current)

        return root
    except:
        traceback.print_exc()
        print "Error in reading file: " + str(file_name)

def main(argv):
    file_name = ''

    try:
        opts, args = getopt(argv, 'hl:', ['log='])
    except:
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

    root = loadFromLog(file_name)
    print root

    return 0

if __name__ == '__main__':
    main(argv[1:])
