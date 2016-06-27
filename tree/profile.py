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
        s = '"name": "' + self.func_name + '", '
        s += '"start_time": "' + str(self.start_time) + '", '
        s += '"end_time": "' + str(self.end_time) + '", '
        s += '"duration": ' + str(self.duration())
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

    def duration(self):
        delta = self.end_time - self.start_time
        return delta.total_seconds() * 1000

class TreeBuilder:
    # construct a tree structure from log file
    # each tree node is a 3 element list, the 1st element is the key of node,
    # the 2nd element is the parent node id of current node, -1 means no parent
    # the 3rd element is a list of child node id, empty means no child

    def __init__(self, file_name):
        self.file_name = file_name
        self.storage = []   # an empty tree

    def __repr__(self):
        s = '{"log": '
        s += self.printNode(0)
        s += '}'
        return s

    def printNode(self, node_id):
        # 1. print the element
        s = '{"function": {' + str(self.storage[node_id][0])

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
        s += '}}'

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
        # 23JUN2016_15:19:16.465 61504:140484032833280 TRACE ibarbutil_functrace.h:27 IBARBUTIL.FUNCTIONTRACE  Enter void BloombergLP::s_ibrarbpost::RequestHelper::processCloseRoomRequest(bsl::shared_ptr<BloombergLP::ibrarbpostmsgs::GenericPostRequestWrapper>, bsl::shared_ptr<BloombergLP::s_ibrarbpost::RequestContext>, bsl::shared_ptr<BloombergLP::ibarbdispatcher::RequestCompletionGuard>, bool) 6299469577153151008

        # we will need column 1, 6 and 7-
        # column 1 is timestamp
        # column 6 is entry/exit flag
        # column 7 and rest are the function signature and uuid
        fields = line.split()
        timestamp = fields[0]
        entry = fields[5] == "Enter"

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
            self.storage[node_id][0].setEndTime(timestamp)
            return self.storage[node_id][1]

    def loadFromLog(self):
        try:
            print "### reading file " + self.file_name
            file = open(self.file_name, 'r')

            del self.storage[:]  # cleanup the node list

            root = [FunctionTrace("Log"), -1, []]  # root element
            self.storage.append(root)              # save in the storage
            current_node = 0                       # current node id

            for line in file:
                current_node = self.parseTrace(line.strip(), current_node)
        except:
            traceback.print_exc()
            print "Error in reading file: " + str(self.file_name)
        finally:
            file.close()

    def stat(self, node_id, table):
        # analyze the tree to get statistic date of each function
        # function_name, execute_times, total_time
        key = self.storage[node_id][0]
        element = self.storage[node_id][0]
        key = element.func_name
        duration = element.duration()
        if key in table:
            table[key]['count'] += 1
            table[key]['time'] += duration
        else:
            table[key] = {'count':1, 'time':duration}

        for child in self.storage[node_id][2]:
            # go through all the children
            self.stat(child, table)

### end of class TreeBuilder

def help():
    print 'Usage: profile.py -l <logfile>'

def printStat(table, outfile):
    s = ""
    for func in table:
        s = func + ', ' + str(table[func]['count']) + ', ' + str(table[func]['time']) + '\n'

    if outfile:
        try:
            out = open(outfile, 'w')
            out.write(s)
        except:
            traceback.print_exc()
            print "Error in writting file: " + outfile
        finally:
            out.close()
    else:
        print s

def printTree(tee, outfile):
    if outfile:
        try:
            out = open(outfile, 'w')
            out.write(tree)
        except:
            traceback.print_exc()
            print "Error in writting file: " + outfile
        finally:
            out.close()
    else:
        print tree

def main(argv):
    infile = ''
    outfile = ''

    try:
        opts, args = getopt(argv, 'hl:o:', ['log=', 'out='])
    except:
        help()
        return -1

    for opt, arg in opts:
        if opt == '-h':
            help()
            return 0
        elif opt in ('-l', '--log'):
            infile = arg
        elif opt in ('-o', '--out'):
            outfile = arg
        else:
            help()
            return -1

    tree = TreeBuilder(infile)
    tree.loadFromLog()

    table = {}
    tree.stat(0, table)
    printStat(table, outfile)

    return 0

if __name__ == '__main__':
    main(argv[1:])
