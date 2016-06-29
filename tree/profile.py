import re
import traceback
from getopt import getopt
from sys import argv
from datetime import datetime
from datetime import timedelta
from operator import itemgetter

from tree import TreeNode


class FunctionTrace:
    def __init__(self, func_name, start_time=None, stop_time=None):
        self.func_name = func_name
        self.setStartTime(start_time)
        self.setStopTime(stop_time)

    def __repr__(self):
        # s = '"name": "' + self.func_name.split()[1] + '", '
        # s += '"start_time": "' + str(self.start_time) + '", '
        # s += '"stop_time": "' + str(self.stop_time) + '", '
        # s += '"duration": ' + str(self.duration())
        s = '"' + self.func_name.split()[1] + '": '
        s += str(self.duration())
        return s


    def setStartTime(self, start_time=None):
        if start_time is None:
            self.start_time = datetime.now()
        else:
            # the input is millisecond, need to times 1000 to get microsecond
            self.start_time = datetime.strptime(start_time+"000", "%d%b%Y_%H:%M:%S.%f")

    def setStopTime(self, stop_time=None):
        if stop_time is None:
            self.stop_time = datetime.now()
        else:
            self.stop_time = datetime.strptime(stop_time+"000", "%d%b%Y_%H:%M:%S.%f")

    def duration(self):
        delta = self.stop_time - self.start_time
        return delta.total_seconds() * 1000

class TreeBuilder:
    # construct a tree structure from log file
    # each tree node is a 3 element list, the 1st element is the key of node,
    # the 2nd element is the parent node id of current node, -1 means no parent
    # the 3rd element is a list of child node id, empty means no child

    def __init__(self, file_name):
        self.file_name = file_name
        self.storage = []   # an empty tree
        self.begin_time = None        # begin time of entire file
        self.end_time = None          # end time of entire file

    def __repr__(self):
        s = '{"log": '
        s += self.printNode(0)
        s += '}'
        return s

    def printNode(self, node_id):
        # 1. print the element
        s = '{' + str(self.storage[node_id][0])

        # 2. recurrsively print children
        children = self.storage[node_id][2]
        if (children):
            s += ', "subfunction": ['
            s += self.printNode(children[0])

            for child in children[1:]:
                s += ', '
                s += self.printNode(child)
            s += ']'

        # 3. print close tag
        s += '}'

        return s


    def addChild(self, node_id, element):
        # add a new node as a child of node_id
        child = [element, node_id, []]
        child_id = len(self.storage)
        self.storage.append(child)
        self.storage[node_id][2].append(child_id)

        # return the node id of new element
        return child_id

    def parseTrace(self, line, node_id):
        # the log file has below format:
        # 27JUN2016_16:29:25.894 17083:140013532595968 TRACE ibarbutil_functrace.h:27 IBARBUTIL.FUNCTIONTRACE  Enter 6300971995367997599 RequestHelper::processCloseRoomRequest

        # we will need column 1, 6 and 7-
        # column 1 is timestamp
        # column 6 is entry/exit flag
        # column 7 and rest are the function signature and uuid
        fields = line.split()
        timestamp = fields[0]
        entry = fields[5] == "Enter"

        if self.begin_time is None:
            self.begin_time = timestamp

        if self.end_time is None:
            self.end_time = timestamp
        elif self.end_time < timestamp:
            self.end_time = timestamp

        if (entry):
            # get function signature from the 6th space
            func_name = line[[x.start() for x in re.finditer(" ", line)][6]+1:]
            element = FunctionTrace(func_name, timestamp)

            # create a child and add to current tree node
            # return the new created node id
            return self.addChild(node_id, element)
        else:
            # update end time
            # return parent node id
            self.storage[node_id][0].setStopTime(timestamp)
            return self.storage[node_id][1]

    def loadFromLog(self):
        try:
            file = open(self.file_name, 'r')

            del self.storage[:]  # cleanup the node list

            root = [FunctionTrace("-1 Log"), -1, []]  # root element
            self.storage.append(root)              # save in the storage
            current_node = 0                       # current node id

            for line in file:
                current_node = self.parseTrace(line.strip(), current_node)

            root[0].setStartTime(self.begin_time)
            root[0].setStopTime(self.end_time)

            file.close()
        except:
            traceback.print_exc()
            print "Error in reading file: " + str(self.file_name)

    def selfTime(self, node_id):
        # self time is the total execution elapse time of a function minus time consumed by its sub functions
        total = self.storage[node_id][0].duration()
        sub = 0
        for subnode in self.storage[node_id][2]:
            sub += self.storage[subnode][0].duration()
        return total - sub

    def stat(self, node_id, table):
        # analyze the tree to get statistic date of each function
        # function_name, execute_times, total_time
        element = self.storage[node_id][0]
        key = element.func_name.split()[1]
        duration = element.duration()

        if key in table:
            table[key]['count'] += 1
            table[key]['time'] += duration
            table[key]['selftime'] += self.selfTime(node_id)
        else:
            table[key] = {'count':1, 'time':duration, 'selftime':self.selfTime(node_id)}

        for child in self.storage[node_id][2]:
            # go through all the children
            self.stat(child, table)

### end of class TreeBuilder

def help():
    print 'Usage: profile.py -l <logfile>'

def printStat(table, outfile):
    array = []
    for func in table:
        array.append((func, table[func]['count'], table[func]['time'], table[func]['selftime']))
    array.sort(key=itemgetter(1,3), reverse=True)

    s = 'function name, calls, total time, self time\n'
    for name, calls, total_time, self_time in array:
        s += name + ', '
        s += str(calls) + ', '
        s += str(total_time) + ', '
        s += str(self_time) + '\n'

    if outfile:
        try:
            out = open(outfile, 'w')
            out.write(s)
            out.close()
        except:
            traceback.print_exc()
            print "Error in writting file: " + outfile
    else:
        print s

def printTree(tree, outfile):
    if outfile:
        try:
            out = open(outfile, 'w')
            out.write(str(tree))
            out.close()
        except:
            traceback.print_exc()
            print "Error in writting file: " + outfile
    else:
        print tree

def main(argv):
    infile = ''
    statfile = ''
    callfile = ''

    try:
        opts, args = getopt(argv, 'hl:c:s:', ['log=', 'call=', 'stat='])
    except:
        help()
        return -1

    for opt, arg in opts:
        if opt == '-h':
            help()
            return 0
        elif opt in ('-l', '--log'):
            infile = arg
        elif opt in ('-c', '--call'):
            callfile = arg
        elif opt in ('-s', '--stat'):
            statfile = arg
        else:
            help()
            return -1

    tree = TreeBuilder(infile)
    tree.loadFromLog()

    table = {}
    tree.stat(0, table)

    printStat(table, statfile)
    printTree(tree, callfile)

    return 0

if __name__ == '__main__':
    main(argv[1:])
